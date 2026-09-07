"""Content part B: §3 → §7.

REBUILT 07-09-2026. Every figure is read from study_numbers.json; the superseded edition
typed its spot into the zone table, its terminal-value dependency into §7 and a factor
stack whose dates had passed.
"""
from docx_base import *
from docx_A import (pc, sgn, n0, n1, paren, longdate, spot, SPOT_DATE, TA_CLOSE,
                    TA_DATE_L, GAP, SH, EDITION_STAMP, STAKE)

pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
L = D['lenses']; eng = D['engine']; touch = D['mc']['touch']; zones = D['mc']['zones']
sotp = D['sotp']; dcf = D['dcf']; COC = D['cost_of_capital_record']; MAC = D['macro']
s0 = D['step0']

# ================= §3 Monte Carlo ===========================================
H1('3  A probabilistic price map')
P('The probability read below opens the section: computed from the same 50,000 paths as everything that follows, it is a '
  'summary of the distribution rather than an input to it.', size=9.8, space_after=4)
rows = [
 ['The probability read (3 months)', ''],
 ['Probability the price finishes above the anchor', pc(pr['p_above'], 0)],
 ['Probability of +10% against −10% — the odds', f"{pc(pr['p_up10'],0)} against {pc(pr['p_dn10'],0)}  ·  {pr['odds']:.2f} : 1"],
 ['Median level, and its move', f"EGP {pr['median']:.2f}  ({sgn(pr['med_move'],1)})"],
 ['The 50% band (25th–75th percentile)', f"EGP {pr['band50'][0]:.2f} – {pr['band50'][1]:.2f}   ({sgn(pr['band50_pct'][0],0)} / {sgn(pr['band50_pct'][1],0)} of the anchor)"],
 ['Probability of touching +10% / −10% at any point', f"{pc(pr['touch_up10'],0)}  /  {pc(pr['touch_dn10'],0)}"],
]
table(rows, [3.3, 3.3], first_col_bold=True, band_rows=[0], header=False)
P(f'We simulate 50,000 three-month price paths from the exchange library’s last session, EGP {TA_CLOSE:.2f} on '
  f'{TA_DATE_L}. Width comes from a pooled cascade on a gap-aware variance proxy, projecting the average daily variance '
  f'over the window — {pc(eng["anchor_vol"],1)} annualised at this origin, regime-conditional by construction and with '
  'no calibration multiplier bolted on. Shape comes from unit-variance fat-tailed innovations through a per-path mixture: '
  'a tighter interquartile body and honest tails. Drift is the expanding-window secular term measured on this stock’s '
  f'own history ({sgn(eng["drift_q"],1)} per quarter), which is the configuration that passed the calibration test in '
  f'Appendix B where zero drift did not. A sixteen-factor stack layers on top — seven continuous drivers and nine '
  f'discrete events, each firing with a probability and an impact — together adding {sgn(eng["factor_drift_q"],2)} '
  'over the quarter.')
rich([('By design the paths diffuse from the anchor as near-term price and deliberately do not embed the fundamental value. ',
       dict(bold=True)),
      ('The value gap of §1 is kept out of the drift. §3 maps where price could go from here, not where value sits. The '
       'upward median is this stock’s own measured behaviour surviving a calibration test — never a target, and '
       'never the §1 value gap smuggled in through a side door.', {})])
rows = [
 ['Continuous factor (7)', 'Direction', 'Discrete event (9)', 'Probability', 'Mean impact'],
 ['Egyptian passenger-car demand and the rate-cut cycle', '+', 'A results release inside the window', '90%', '+0.5%'],
 ['Currency drift through imported assembly content', '±', 'MNT-Halan second closing at or above the round', '45%', '+1.5%'],
 ['Policy easing — affordability and lender margin', '+', 'A policy cut of 100 basis points or more', '50%', '+1.0%'],
 ['Regional conflict drag on Iraq and Jordan', '−', 'Regional escalation spillover', '25%', '−2.5%'],
 ['Chinese grey-import competition', '−', 'A new entrant resetting price points', '35%', '−1.0%'],
 ['Localisation and the assembly-plant ramp', '+', 'Plant ramp or a new assembled model', '55%', '+0.6%'],
 ['Funding cost and the provisioning cycle', '−', 'Dividend or capital-return surprise', '15%', '+0.8%'],
 ['', '', 'A step devaluation of the pound', '12%', '−2.0%'],
 ['', '', 'Index flows or an index event', '25%', '+0.8%'],
]
table(rows, [2.15, 0.6, 2.2, 0.8, 0.85], size=8.7)
caption('The factor stack is the preparer’s own judgment, stated so a reader can disagree with each line. It is '
        'deliberately modest in aggregate: the whole stack moves the quarter by less than two per cent.')

H2('Percentile map (EGP per share)')
rows = [['Horizon', 'p5', 'p25', 'p50', 'p75', 'p95'],
 ['1 month', f"{q20['5']:.2f}", f"{q20['25']:.2f}", f"{q20['50']:.2f}", f"{q20['75']:.2f}", f"{q20['95']:.2f}"],
 ['3 months', f"{q60['5']:.2f}", f"{q60['25']:.2f}", f"{q60['50']:.2f}", f"{q60['75']:.2f}", f"{q60['95']:.2f}"]]
table(rows, [1.9, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True)
P(f"Lead with the 50% band rather than the tails: a quarter ahead, half of all paths finish between EGP "
  f"{q60['25']:.2f} and {q60['75']:.2f}; at one month the band is EGP {q20['25']:.2f}–{q20['75']:.2f}. The 5th-to-95th "
  'cone is context, not a forecast.', size=9.8)
figure('fig4_fan.png', 6.4, 'Figure 4 — Forward price cone to three months. The median drifts up with the calibrated '
       'secular term; the brass dashed line marks the fundamental central, which sits above the whole cone.')
figure('fig5_dist.png', 5.2, 'Figure 5 — Price distribution at one month.')
figure('fig6_dist.png', 5.2, 'Figure 6 — Price distribution at three months.')

H2('Level-touch ladder')
P('The probability that price touches a level at any point by the horizon — the running maximum for levels above the '
  'anchor, the running minimum for levels below it:', size=9.8)
rows = [['Level (EGP)', '1-month touch', '3-month touch', 'Against the anchor']]
for lv in sorted((int(k) for k in touch), reverse=True):
    tv = touch[str(lv)]
    rows.append([f'{lv}', pc(tv['t20'], 0), pc(tv['t60'], 0), sgn(lv / TA_CLOSE - 1, 1)])
table(rows, [1.2, 1.4, 1.4, 2.6], first_col_bold=True)
caption('Every rung and every probability in this ladder is computed from the same 50,000 paths; the distance column is '
        'measured against the session the cone was struck on, not against the later price the valuation uses.')

# ================= §4 comparison =============================================
H1('4  Comparison of the lenses')
P(f"Three readings sit side by side and they genuinely disagree. The fundamental reads spread EGP "
  f"{L['relative']['base']:.2f} to {L['sotp']['base']:.2f} with a central of {L['central']['base']:.2f}, "
  f"{sgn(GAP)} against the price — and that spread is dominated by one line, the MNT-Halan mark, whose "
  "value rather than whose existence is the open question. The technical picture has turned: the price came off its short "
  "averages with negative momentum and sits in the middle of its own 52-week range. The probabilistic map is the one piece "
  f"untouched by any of this: its median ({q60['50']:.2f}) sits above the anchor because the repricing that carried this "
  "stock over the sample period has not yet statistically died. That is a description of measured price behaviour, not a "
  "claim about value, and it does not know what an associate stake is worth.")
rows = [
 ['Lens', 'What it reads', 'Central / implication'],
 ['Fundamental (four reads)', 'Below the central — if the mark holds', f"EGP {L['central']['base']:.2f} ({sgn(GAP)})"],
 ['Fundamental (primary read alone)', 'The sum-of-the-parts on its own', f"EGP {L['sotp']['base']:.2f} ({sgn(L['sotp']['base']/spot-1)})"],
 ['Technical', 'Momentum lost, long trend intact', f"Below the 20- and 50-day averages; above the 100- and 200-day"],
 ['Simulation (three months)', 'Drift up, right-skewed', f"Median {q60['50']:.2f}; p5–p95 {q60['5']:.2f}–{q60['95']:.2f}"],
]
table(rows, [1.9, 1.9, 3.1], first_col_bold=True)
rich([('A fair-value read, not a recommendation. ', dict(bold=True)),
      (f"GB Corp reads below its central estimate on fundamentals ({sgn(GAP)}), and that reading rests on a number the "
       f"company itself stated: a {pc(STAKE,2)} holding in MNT-Halan. What is not stated anywhere is what that stake is "
       f"worth to the market. Taking the round's valuation at face value makes the stake alone "
       f"{pc(sotp['mnt_halan_value']*(1-sotp['disc'])/D['mktcap'],0)} of GB Corp's market capitalisation, which the market "
       "plainly does not credit. Strip the associate leg out and what remains — the auto business and the lender — "
       f"reads within {max(abs(L['relative']['base']/spot-1), abs(L['normalized']['base']/spot-1))*100:.0f}% of the traded "
       "price, in line with what the tape and the distribution already show. The honest summary is that the operating "
       "business is priced about right, and whether the shares are cheap depends on how much of a discount the market is "
       "entitled to apply to an unlisted minority financial-services stake. That is a legitimate valuation question this "
       f"study raises rather than settles. The bear-to-bull span, EGP {L['central']['bear']:.2f} to "
       f"{L['central']['bull']:.2f}, is wide enough on its own to demand real humility. We publish the distribution, not a "
       "target.", {})])

# ================= §5 catalysts ==============================================
H1('5  Catalysts to watch')
for head, body in [
 ('The next results release. ', 'The reviewed half to 30 June 2026 is the anchor this forecast is struck on; the next '
  'print is the first test of whether the auto gross margin holds where that half left it, and of whether the finance-cost '
  'line responds as policy eases.'),
 ('Policy meetings. ', 'Each cut lowers GB Capital’s funding cost, the customer’s instalment and this study’s '
  'discount rate at once — the single most mechanical catalyst on the list.'),
 ('The MNT-Halan mark, not the stake. ', 'The company has stated its holding. What is open is whether the market accepts '
  'the round’s valuation at face value or applies a steeper illiquidity and minority discount. Any secondary '
  'transaction, or any further disclosure bearing on how an unlisted minority stake of this size should be marked, is the '
  'most value-relevant event available.'),
 ('The second closing of that round. ', 'It would test whether the round’s valuation holds or moves; it does not '
  'change the ownership percentage, which the company has already stated.'),
 ('The assembly-plant ramp and new models. ', 'Added capacity and local content, and the inventory unwind behind them, are '
  'the visible working-capital catalysts.'),
 ('Competitive pricing from new entrants. ', 'The clearest threat to passenger-car prices and share in a recovering market.'),
 ('Regional normalisation. ', 'Part of passenger-car revenue is Iraq and Jordan. This study does not hold a sourced split '
  'of that revenue for the reviewed half, so the exposure is named and not priced; any de-escalation restores the '
  'fastest-margin sales in the mix.'),
 ('The pound. ', 'A step devaluation is the compound risk — assembly costs, rates, and the pound value of every mark '
  'at once; continued stability is the quiet tailwind.'),
 ('The dividend decision. ', 'A payout step-up would mark the cash-conversion inflection this study is waiting for. The '
  'model’s own forecast cash flows carry the constraint: the first forecast year converts EGP '
  f"{dcf['rows'][0]['fcff']:,.0f} mn of free cash flow against EGP {dcf['rows'][-1]['fcff']:,.0f} mn in the last."),
]:
    bullet(body, bold_head=head)

# ================= §6 zones ==================================================
H1('6  Reading the probability zones')
_bounds = [26, 30, 34, 38]
P(f'Translating the three-month distribution into plain zones, anchored on the EGP {TA_CLOSE:.2f} session the cone was '
  f'struck from and on the fair-value cluster of §1:')
rows = [
 ['Zone (3 months)', 'Range', 'Probability', 'What it would mean'],
 ['Deep downside', f'below EGP {_bounds[0]}', pc(zones[0], 0), 'Regional escalation or a devaluation; tests the lower shelf'],
 ['Lower band', f'EGP {_bounds[0]}–{_bounds[1]}', pc(zones[1], 0), 'Margin proof delayed; the relative read dominates'],
 ['Around the anchor', f'EGP {_bounds[1]}–{_bounds[2]}', pc(zones[2], 0), 'Status quo; fair value and price coexist'],
 ['Upper band', f'EGP {_bounds[2]}–{_bounds[3]}', pc(zones[3], 0), 'Cuts and the working-capital release credited'],
 ['Strong upside', f'above EGP {_bounds[3]}', pc(zones[4], 0), 'Repricing continues; the discount narrows toward net asset value'],
]
table(rows, [1.5, 1.3, 1.2, 2.9], first_col_bold=True)
P(f'The distribution is right-skewed by construction: the calibrated secular drift plus fat-tailed innovations put '
  f'{pc(zones[4],0)} of terminal mass above EGP {_bounds[3]}. Read that with Appendix B open. The drift term is what the '
  f'calibration test accepted, and that appendix states the margin rather than flattering it. This is the spread of '
  'outcomes consistent with the stock’s own measured behaviour and the factor stack; it is not a forecast.')

# ================= §7 caveats ================================================
H1('7  Caveats and what would change our mind')
for head, body in [
 ('The stake is stated; what it is worth is not. ', 'GB Corp’s own 9 June 2026 press release states its holding at '
  f'{pc(STAKE,2)}, against {pc(sotp["mnt_halan_stake_prior"],2)} before that transaction. That removes the sourcing '
  f'uncertainty. What remains open is the mark: taking the round’s valuation at face value makes the stake worth EGP '
  f'{sotp["mnt_halan_value"]/1000:.1f} bn, or {pc(sotp["mnt_halan_value"]*(1-sotp["disc"])/D["mktcap"],0)} of the entire '
  'market capitalisation. If the market is right to discount that mark far more heavily than this study’s uniform '
  f'{pc(sotp["disc"],0)}, the sum-of-the-parts compresses toward the relative and normalised reads — that is, toward '
  'the price, not away from it.'),
 ('The construction of the central is itself a judgment, and it is recorded as one. ', 'The published central is a '
  f'weighted blend of four reads at weights that were chosen and written down and have never been tested out of sample. '
  f'The primary read alone is EGP {L["sotp"]["base"]:.2f}, {pc(L["sotp"]["base"]/L["central"]["base"]-1,1)} above the '
  'blend. The blend is the lower number and it is what this edition publishes; a reader who prefers the primary read '
  'should use it and can, because both are printed.'),
 ('Working capital is the second-order model. ', 'The operating leg’s value lives in the glide of working-capital '
  f'intensity from {pc(D["disclosed_drivers"]["cost_stack"]["working_capital_pct"][0],1)} of revenue to '
  f'{pc(D["disclosed_drivers"]["cost_stack"]["working_capital_pct"][-1],1)}. If the higher figure is the new structural '
  'cost of holding share — import finance and assembly stock — the auto leg is worth materially less, and the '
  '§1.9 grid rather than a single sentence is where that is priced.'),
 ('Terminal-value dependency, and a life that could not be sourced. ',
  f'{pc(dcf["tv_pct"],0)} of the auto leg’s enterprise value is terminal value, at a terminal spread of '
  f'{pc(COC["wacc_terminal"]-MAC["terminal_growth_nominal"],2)} between the cost of capital and growth. Worse, the house '
  'standard is that a terminal rests on a disclosed asset life, and none could be sourced here: the policy note gives '
  'rate ranges rather than a scalar, and the identity route depends on an undisclosed land split. The refusal is recorded '
  'in §1.2 rather than resolved by choosing a life, and it is the largest single piece of unfinished business in this '
  'study.'),
 ('The drift is empirical, and it is thin. ', 'The secular drift is what the calibration test accepted where zero drift '
  f'did not, but Appendix B publishes the margin: on {s0["nonoverlap"]["n"]} non-overlapping windows the coverage of the '
  f'90% band is {pc(s0["nonoverlap"]["cov90"],0)} against a 90% target, and the proper score against the naive benchmark '
  f'is {sgn(s0["nonoverlap"]["crps_skill"],1)}. A regime turn would flip the median read; the drift is re-tested at every '
  'roll-forward and cut the moment it fails.'),
 ('The associate mark is real but private. ', 'The round is a genuine transaction price — cash changed hands — '
  'but for an unlisted company, and on public reporting only an initial tranche of an ongoing round. The stake applied to '
  'it is stated and current; the bear case applies a much heavier discount to the mark itself, which is why its floor sits '
  'far below the base case.'),
 ('The lender is a credit cycle. ', 'GB Capital’s adjusted return and its loss rates are cycle-friendly numbers '
  'struck in an easing cycle; a funding-market seizure or a deterioration in credit would break the one-times-book mark.'),
 ('Consolidation approximations. ', 'The consolidated forecast maps eliminations, minority interests and the grouped '
  'balance-sheet layout with stated simplifications. Segment disclosure, not audited consolidation schedules, is the '
  'source for the split of the group into legs.'),
 ('The far forecast years are ranges, and thin ones. ', 'Appendix A publishes the third, fourth and fifth forecast years '
  'as ranges taken from how wrong this method has been on this company’s own history. Those ranges rest on a handful '
  'of observations each — the table prints the count beside every one — and the count is what tells a reader what '
  'the range can and cannot promise.'),
 ('Technical reminder. ', 'The technical read is context, not a trigger, and it is computed on an older session than the '
  'price the valuation is struck on. Both dates are printed wherever either figure is quoted.'),
]:
    bullet(body, bold_head=head)
