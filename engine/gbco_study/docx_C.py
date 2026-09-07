"""Content part C: Appendices A–D, About, Disclosure, footer.

REBUILT 07-09-2026. Appendix A's history now comes from the walk-forward panel — the
company's own filed consolidated income statement, footed year by year — and its
forecast from the committed group build, rather than from three columns typed into this
file. Appendix A also now carries the far-year RANGES [R-FCAL-01] requires, which the
superseded edition did not publish at all.
"""
import json
import os
from docx_base import *
from docx_A import (pc, sgn, n0, n1, paren, longdate, spot, SPOT_DATE, TA_CLOSE,
                    TA_DATE_L, GAP, SH, EDITION, EDITION_L, EDITION_STAMP, STAKE)

HERE = os.path.dirname(os.path.abspath(__file__))
L = D['lenses']; E = D['experts']; s0 = D['step0']; sotp = D['sotp']; dcf = D['dcf']
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
caption('Table A3 — the Auto leg’s cash flow, line for line as §1.2 discounts it. Deductions are printed as '
        'magnitudes in brackets and the labels state the operation, so the column can be followed to the result.')

H2('A.5  The balance-sheet anchors the bridge stands on')
rows = [['Item', 'Value (EGP mn)', 'As at', 'Source']]
for k, lbl in [('cash_jun2026', 'Cash and equivalents'), ('debt_jun2026', 'Borrowings, group'),
               ('debt_auto_jun2026', 'Borrowings, GB Auto segment'),
               ('eq_jun2026', 'Total equity')]:
    it = D['inputs'][k]
    rows.append([lbl, n1(it['value']), it['date'], it['layer']])
rows.append(['Auto net debt used in the bridge', n1(dcf['auto_nd']), '2026-06-30', 'segmented balance sheet, GB Auto column'])
rows.append(['Auto non-controlling interests deducted', n1(dcf['auto_nci']), '2026-06-30', 'that leg’s own minority'])
table(rows, [2.3, 1.3, 1.1, 2.4], first_col_bold=True, size=8.6)
caption('Table A4 — the bridge stands on the latest disclosed balance sheet, the reviewed statements to 30 June 2026, '
        'and not on the prior year end. The deduction is the AUTO leg’s own net debt and the AUTO leg’s own '
        'minority, because the lender’s borrowings are its raw material rather than its leverage.')

# ================= Appendix B ================================================
H1('Appendix B  Calibration — testing the price cone on this stock’s own history')
_nl = s0['nonoverlap']; _mo = s0['monthly']; _zd = s0['zerodrift']
P(f'Before any forecast we test the price cone on GB Corp’s own history. At {_nl["n"]} non-overlapping '
  'three-month origins, using only the data available at each origin, the engine generates the three-month-ahead '
  'distribution and the realised close is scored against it. What is published here is what a reader can use: how often '
  'the bands actually held, with the count printed beside every percentage.')
rows = [
 ['Configuration', 'Windows', '50% band held', '80% band held', '90% band held', 'Distribution centre'],
 ['Zero drift — non-overlapping', str(_zd['n']), pc(_zd['cov50'], 0), pc(_zd['cov80'], 0), pc(_zd['cov90'], 0), f"{_zd['pit_mean']:.2f}"],
 ['Secular drift — non-overlapping', str(_nl['n']), pc(_nl['cov50'], 0), pc(_nl['cov80'], 0), pc(_nl['cov90'], 0), f"{_nl['pit_mean']:.2f}"],
 ['Secular drift — monthly origins', str(_mo['n']), pc(_mo['cov50'], 0), pc(_mo['cov80'], 0), pc(_mo['cov90'], 0), f"{_mo['pit_mean']:.2f}"],
]
table(rows, [2.0, 0.8, 1.0, 1.0, 1.0, 1.2], first_col_bold=True, size=8.7)
figure('figB1_calibration.png', 6.6, 'Figure B-1 — the calibration replay: the quarterly cone against what actually '
       'happened, the distribution of where outcomes landed inside the cone, and coverage against target.')
P(f'Read the middle row. On {_nl["n"]} windows the 90% band contained the close {pc(_nl["cov90"],0)} of the time against '
  f'a 90% target, the 80% band {pc(_nl["cov80"],0)} against 80%, and the 50% band {pc(_nl["cov50"],0)} against 50% — '
  'a cone that held about as often as it promised at the wide end and slightly more often than promised in the middle. '
  f'The centre of the distribution sits at {_nl["pit_mean"]:.2f} against a neutral 0.50, which says outcomes landed a '
  'little higher in the cone than the middle of it: this engine has been calling this stock’s advance slightly low '
  'rather than slightly high.')
P(f'The honest caveats. The proper score against a naive benchmark is {sgn(_nl["crps_skill"],1)} on non-overlapping '
  f'windows and {sgn(_mo["crps_skill"],1)} on the denser monthly origins — that is, this cone does not beat a '
  'carry-anchored random walk on that score, and the case for the drift term rests on the coverage and the centring '
  'rather than on a score margin. The drift is re-tested at every roll-forward and cut the moment the coverage record '
  'stops holding. This is decent validation of a band, not proof of an edge, and the difference is the whole point of '
  'printing the counts.')

# ================= Appendix C ================================================
H1('Appendix C  Peer set, sector structure, and risks')
P('GB Corp has no clean single comparable — an auto assembler-distributor, a non-bank lender and a fintech '
  'associate in one wrapper. The peer set is therefore split by leg, and it is used for cross-checks only: no peer is a '
  'source for GB Corp’s own reported figures.')
rows = [
 ['Leg', 'Closest peers', 'How they are typically valued'],
 ['Auto assembly and distribution', 'Gulf and regional auto distributors; listed consumer-durables names on this exchange', 'Enterprise value against operating profit; earnings multiples'],
 ['Non-bank consumer and corporate finance', 'Listed Egyptian finance companies with a comparable book', 'Price to book against the return on that book'],
 ['Fintech associate', 'Listed payments and financial-technology names on this exchange', 'Private marks; the last round is the only observable price'],
]
table(rows, [1.9, 3.1, 2.0], first_col_bold=True, size=8.9)
P('Sector structure and principal risks. The Egyptian passenger-car market is in a policy-assisted recovery, with the '
  'easing cycle restoring affordability, localisation incentives reshaping the assembled-versus-imported mix, and new '
  'entrants resetting price points. Consumer and corporate finance is growing faster than banking credit off a low base, '
  'with securitisation deepening as a funding market. The principal risks are a structurally higher working-capital '
  'intensity; a renewed devaluation; regional conflict freezing the Iraq and Jordan lines; price competition from new '
  'entrants; credit-cycle deterioration in the lending book; a private-market re-pricing of the associate stake; and '
  'execution on the assembly ramp.')

# ================= Appendix D ================================================
H1('Appendix D  The expert valuation panel')
P('Every study closes with a panel of standing expert personas, so that each accumulates a track record across studies '
  'and an update is a re-run rather than a re-training. For GB Corp we cast the industrial trio, adding the cash-returns '
  'lens because the name is capital-heavy: Expert 1 (the accountant — net asset value and the marks), Expert 2 '
  '(earnings power — normalised mid-cycle earnings and multiples), Expert 3 (cash returns — return on capital '
  'against its cost). Each runs a different method, derives its value from shown workings, and states in advance what '
  'would falsify it.')

_e1, _e2, _e3 = E['e1'], E['e2'], E['e3']
H2('D.1  Expert 1 — the split-legs net asset value and the marks')
P('Worldview. A group is worth the sum of its parts at realisable value, less a discount for the wrapper. Mark each leg '
  'to what it would fetch on its own; then argue only about the discount.', size=9.8)
P('When it works and when it fails. Best where the legs are separable and independently markable; it fails hardest when '
  'the discount applied to a private mark is itself contestable, which is exactly his position here.', size=9.8)
rows = [
 ['Expert 1’s marks', 'EGP mn'],
 ['Auto leg (he accepts the §1.2 cash-flow value)', n0(sotp['auto_eq'])],
 ['GB Capital at one times adjusted book', n0(sotp['cap_val'])],
 ['Associates: MNT-Halan plus the residual holdings', n0(sotp['assoc'])],
 ['Σ before the discount', n0(sotp['auto_eq'] + sotp['cap_val'] + sotp['assoc'])],
 [f"less: wrapper discount at {pc(_e1['wrapper_discount'],0)} — an operator, not a passive holding company", paren((sotp['auto_eq'] + sotp['cap_val'] + sotp['assoc']) * _e1['wrapper_discount'])],
 ['Equity value', n0(_e1['base'] * SH)],
 ['Per share', f"{_e1['base']:.2f}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity — the swing is the discount on the mark, now that the stake is stated. Marking MNT-Halan at three "
  f"quarters of the round's valuation takes his number to EGP {_e1['mark_haircut']['0.75']:.2f} per share; at half, to "
  f"EGP {_e1['mark_haircut']['0.5']:.2f}. He concedes the point openly: the stake is not the argument any more, the "
  f"argument is what a {pc(STAKE,2)} minority holding in an unlisted company is worth to a public-market buyer who "
  "cannot sell it, and that is a discount-rate question rather than an ownership question. Cross-examination: he tells "
  "Expert 2 that capitalising mid-cycle earnings double-counts assets he has already marked at full value; he tells "
  "Expert 3 that a haircut on the return on capital is small next to the swing available from how hard you discount an "
  "illiquid stake.", size=9.8)
rich([('Verdict, falsification, and what the price implies. ', dict(bold=True)),
      (f"Fair value EGP {_e1['base']:.2f}, on a range of EGP {_e1['rng'][0]:.2f} to {_e1['rng'][1]:.2f} — the widest "
       "in the room, and driven by the discount debate rather than by an unconfirmed stake. He is falsified by a real "
       "secondary transaction in the associate's shares at a materially different price, or by a second closing "
       "repricing the round. The traded price implies a discount on the associate leg far steeper than his stated "
       "wrapper discount, which in his own view is evidence the market does not accept that the round's marked value "
       "transfers cleanly to a minority holder.", {})])

H2('D.2  Expert 2 — normalised earnings power')
_n = D['lens_inputs']['normalized']
P('Worldview. An operating business is worth a fair multiple of its sustainable mid-cycle earnings; peaks and troughs '
  'are noise to be stripped out.', size=9.8)
P('When it works and when it fails. Best with a through-cycle record, and three disclosed years spanning trough, '
  'windfall and normalisation is workable; it fails at structural breaks — if new entrants reset prices '
  'permanently, his normalisation is simply wrong.', size=9.8)
rows = [
 ['Expert 2’s normalisation', 'Value'],
 ['Mid-cycle group profit after tax (EGP mn)', n0(_n['pat']['base'])],
 ['Shares in issue (mn)', n1(SH)],
 ['Normalised earnings per share (EGP)', f"{_n['eps']['base']:.2f}"],
 ['Justified through-cycle multiple', f"{_n['pe']['base']:.1f}×"],
 ['Fair value per share (EGP)', f"{_e2['base']:.2f}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity — the swing is the multiple. At {_n['pe']['bear']:.1f}× his number is EGP "
  f"{_n['eps']['bear']*_n['pe']['bear']:.2f}; at {_n['pe']['bull']:.1f}×, EGP "
  f"{_n['eps']['bull']*_n['pe']['bull']:.2f}. Cross-examination: he tells Expert 1 that a net asset value struck off a "
  "trough-margin cash-flow model understates a business whose volumes are still mid-cycle; he tells Expert 3 that "
  "pessimism about cash conversion ignores that working capital is a stock rather than a perpetual flow, and it releases "
  "exactly when growth normalises.", size=9.8)
rich([('Verdict, falsification, and what the price implies. ', dict(bold=True)),
      (f"Fair value EGP {_e2['base']:.2f}, on a range of EGP {_e2['rng'][0]:.2f} to {_e2['rng'][1]:.2f} — the most "
       f"conservative in the room and the closest to the traded price, {sgn(_e2['base']/spot-1)} against it. He is "
       "falsified by the auto gross margin staying below the level the reviewed half printed through the next two years, "
       "or by the passenger-car market rolling over. His is also the one estimate in the room that never touches the "
       "associate stake, which is why it is the number a reader who distrusts that mark should look at first.", {})])

H2('D.3  Expert 3 — cash returns: return on capital against its cost')
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
 ['less: Auto net debt and minority (EGP mn)', paren(dcf['auto_nd'] + dcf['auto_nci'])],
 ['Operating-leg equity (EGP mn)', n0(E['e3']['equity_at_base'])],
 [f"Lender at {E['e3']['params']['cap_mult']:.2f}× book · associates at {E['e3']['params']['assoc_mult']:.2f}× (EGP mn)", f"{n0(sotp['cap_val']*E['e3']['params']['cap_mult'])} · {n0(sotp['assoc']*E['e3']['params']['assoc_mult'])}"],
 ['Fair value per share (EGP)', f"{_e3['base']:.2f}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity — two levers, and he ranks them himself. Moving his haircut on the associate mark from "
  f"{E['e3']['params']['assoc_mult']:.2f}× to {E['e3']['params']['assoc_mult_bear']:.2f}× costs EGP "
  f"{abs(_e3['mark_lever']):.2f} per share; marking the operating leg at "
  f"{E['e3']['params']['ev_mult_bull']:.2f}× capital employed instead of "
  f"{E['e3']['params']['ev_mult']:.2f}×, which is what a recovery in the return on capital would buy, adds EGP "
  f"{_e3['roce_lever']:.2f}. The mark is the bigger lever by more than two to one, and that is his point. "
  "Cross-examination: he tells Expert 2 that mid-cycle earnings without the capital cost of holding them is a half-truth; "
  "he tells Expert 1 that a single-digit wrapper discount does not begin to capture the illiquidity of a minority stake "
  "in a company that has never had a public exit.", size=9.8)
rich([('Verdict, falsification, and what the price implies. ', dict(bold=True)),
      (f"Fair value EGP {_e3['base']:.2f}, on a range of EGP {_e3['rng'][0]:.2f} to {_e3['rng'][1]:.2f} — even his "
       f"conservative method lands {sgn(_e3['base']/spot-1)} against the price once the stated stake is applied at the "
       "round's valuation, which he flags as the real finding: the stake was never the issue, the mark is. He is "
       "falsified by a durable recovery in the return on capital well above the FY2025 figure, or by a real secondary "
       "sale of the associate's shares meaningfully below the round's implied valuation.", {})])

H2('D.4  The three in one room')
P('The stake question that dominated an earlier draft of this study is settled — the company stated its holding in '
  'writing. What the three disagree on is what that holding is worth.', size=9.8)
P('Expert 1: “The company told us what it owns. Fine — now the argument is honest: it is about the '
  'discount, not the number. I apply a single-digit wrapper discount. If you think that is too thin for an illiquid '
  'minority stake, argue the discount, not the disclosure.”', size=9.8)
P(f'Expert 3: “Your own arithmetic says a stated {pc(STAKE,2)} stake is worth '
  f'{pc(sotp["mnt_halan_value"]*(1-sotp["disc"])/D["mktcap"],0)} of the entire market capitalisation. That was true when '
  'the number was uncertain and it is just as true now that it is not. The company being straight about its ownership '
  'does not make the market’s scepticism about the mark go away — if anything it sharpens the question.”', size=9.8)
P('Expert 2: “You are both still arguing about a number that was never in my model. Mid-cycle earnings power does '
  'not care what the associate is worth. If you want the one read immune to this whole argument, it is mine — and '
  'notice it is also the one closest to where the market actually prices the stock.”', size=9.8)

H2('D.5  Reading the divergence')
figure('figD1_experts.png', 6.0, 'Figure D-1 — the three experts’ fair-value ranges. Brass ticks are base cases; the '
       'gold band is the panel centre; the ink line is the price. The spread is almost entirely the associate mark.')
_epanel = [_e1['base'], _e2['base'], _e3['base']]
rows = [
 ['Expert', 'Method', 'The single swing assumption', 'Base fair value'],
 ['Expert 1', 'Split-legs net asset value', f"The discount on the associate mark ({pc(_e1['wrapper_discount'],0)} wrapper)", f"EGP {_e1['base']:.2f}"],
 ['Expert 2', 'Normalised earnings power', f"Mid-cycle profit × {_n['pe']['base']:.1f}× — stake-blind", f"EGP {_e2['base']:.2f}"],
 ['Expert 3', 'Cash returns against the cost of capital', f"Return-on-capital fade plus a {E['e3']['params']['assoc_mult']:.2f}× haircut on the mark", f"EGP {_e3['base']:.2f}"],
]
table(rows, [1.0, 2.2, 2.5, 1.3], first_col_bold=True, size=9.0)
P(f"The spread — EGP {min(_epanel):.2f} to {max(_epanel):.2f} at base — is wide for what is otherwise a set of "
  "broadly agreeing methods, and it is one disagreement rather than several: not the volumes, not the lender’s "
  "profitability, not the cash-conversion path, and not the ownership percentage, which all three accept. What separates "
  "them is purely how much to discount that stake’s marked value. Expert 2 sidesteps the question by never pricing "
  "the stake; Experts 1 and 3 both use the stated figure and disagree on the haircut. Unlike a business uncertainty that "
  "resolves with quarterly prints, this one may never fully resolve, because private-mark discounts are a matter of "
  "judgment rather than a fact that appears on a schedule. Until a real secondary transaction supplies an independent "
  "data point, Expert 2’s stake-blind number remains the one estimate in the room immune to the whole argument.")
caption(f'Each expert’s fair value is logged against this study’s date ({EDITION_L}) and the price it was '
        f'struck at (EGP {spot:.2f}, {SPOT_DATE}) as an internal per-expert track record.')

# ================= About / Disclaimer / footer ================================
H1('About this series')
P('Testahil publishes independent, educational valuation studies. Each is an attempt to reason transparently about what a '
  'security is worth, with every assumption shown and a companion model so readers can disagree productively. The house '
  'style is distributions, not tips: we describe ranges and probabilities, not targets, and we do not tell anyone what to '
  'do. Studies are framed as educational analysis, the preparer is not licensed by any securities regulator, and holdings '
  'are disclosed.')
H1('Disclosure & Disclaimer')
for head, body in [
 ('Not investment advice. ', 'This document is educational and informational only. It is not, and must not be relied upon '
  'as, investment, financial, legal, accounting or tax advice, nor an offer, solicitation or recommendation to buy, sell or '
  'hold any security. It contains no price target and no rating.'),
 ('No licence; no advisory relationship. ', 'The preparer is not registered or licensed with any securities or financial '
  'regulator in any jurisdiction — including Egypt’s Financial Regulatory Authority — holds no brokerage or '
  'investment-advisory authorisation, and is not acting as your adviser or fiduciary. Nothing here is personalised to your '
  'circumstances.'),
 ('Holdings disclosure. ', 'The preparer may hold, and may in the future take or dispose of, a position in the security '
  'discussed in this report, and may transact at any time without notice. This is a potential conflict of interest you '
  'should weigh.'),
 ('Sources and accuracy. ', 'Reported financial and operating figures are drawn from the company’s public disclosure '
  'and other public sources believed reliable but not independently verified; they may contain errors or be superseded. '
  'Forward-looking inputs — the leg marks including the discount applied to the associate stake, the complexity '
  'discount, projections, multiples, the cash-flow model and the simulation’s factor probabilities — are the '
  'preparer’s own judgments and are inherently uncertain.'),
 ('Forward-looking statements. ', 'Any statements about the future are estimates subject to risks and uncertainties; actual '
  'results may differ materially. The simulation models price, not value, and encodes subjective probabilities for events '
  'that have not occurred.'),
 ('No reliance; your responsibility. ', 'Do your own research and consult a licensed professional before making any '
  'decision. You are solely responsible for your investment decisions and their outcomes. To the maximum extent permitted '
  'by law, the preparer accepts no liability for any loss arising from use of this document.'),
 ('Currency and figures. ', 'Figures are in Egyptian pounds, millions unless stated; bn denotes billion. The exchange rate '
  f'used for the associate mark is EGP {sotp["egp_usd"]:.1f} to the US dollar, and it is a flagged estimate. Rounding may '
  f'cause totals to differ slightly. The price is EGP {spot:.2f} as at {SPOT_DATE}; the price cone and the technical read '
  f'are computed on the exchange library’s own last session, EGP {TA_CLOSE:.2f} on {TA_DATE_L}. Market data change '
  'continuously.'),
]:
    rich([(head, dict(bold=True, italic=True)), (body, {})], size=9.6, space_after=5)
P(f'TESTAHIL · Independent Valuation Study · Educational Analysis · GB Corp S.A.E. (EGX: GBCO) · edition '
  f'{EDITION_STAMP} · reporting currency EGP', size=8.8, color=GREY, align='center', space_before=10)
