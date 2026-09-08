"""Content part B: §3 → §7.

REBUILT 07-09-2026, SECOND PASS. The comparison and the caveats are rewritten against the
answer the study now publishes: one class primary with two branches, no weighted blend, no
complexity discount, no normalised-earnings lens. Every figure is read from the committed
record.
"""
from docx_base import *                                              # noqa: F401,F403
from docx_A import (pc, sgn, n0, n1, paren, longdate, spot, SPOT_DATE, TA_CLOSE,
                    TA_DATE_L, SH, EDITION_STAMP, STAKE, STAKE_PRIOR,
                    STAKE_STATEMENTS, STAKE_STATEMENTS_PRIOR,
                    B_LO, B_HI, V_LO, V_HI, GAP_LO, GAP_HI, MARK_LO, MARK_HI,
                    EQ_LO, EQ_HI, REL, BOOK, CAP, PRICE_MARK, PRICE_ASSOC, PRICE_MNT_USD,
                    MNT_USD_AT_CARRYING, OPERATING_EQ, RATE_LO, RATE_HI,
                    SHARE_OF_PROFIT)

pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
eng = D['engine']; touch = D['mc']['touch']; zones = D['mc']['zones']
sotp = D['sotp']; dcf = D['dcf']; COC = D['cost_of_capital_record']; MAC = D['macro']
s0 = D['step0']; HIS = D['history']['income_statement']

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
      ('Neither branch of §1 is in the drift. §3 maps where price could go from here, not where value sits. The '
       'upward median is this stock’s own measured behaviour surviving a calibration test — never a target, and '
       'never the §1 disagreement smuggled in through a side door.', {})])
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
_inside = [b for b in (V_LO, V_HI) if b <= q60['95']]
figure('fig4_fan.png', 6.4,
       'Figure 4 — Forward price cone to three months. The median drifts up with the calibrated secular term; the two '
       'brass dashed lines mark the two branches of the fundamental answer. At three months the cone’s 95th percentile '
       f'reaches EGP {q60["95"]:.2f}, so '
       + ('both branches sit above the whole cone.' if not _inside else
          (f'the lower branch (EGP {V_LO:.2f}) sits inside the cone’s upper tail and the higher (EGP {V_HI:.2f}) above '
           'it entirely.' if len(_inside) == 1 else 'both branches sit inside the cone’s upper tail.'))
       + ' The two are on different clocks and the picture is a comparison, not a forecast of the value.')
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
P(f"Three readings sit side by side and they genuinely disagree. The fundamental primary reads EGP {V_LO:.2f} and "
  f"{V_HI:.2f} — {sgn(GAP_LO)} and {sgn(GAP_HI)} against the price — on the two bases GB Corp itself publishes for "
  f"one asset, while its cross-checks sit either side of the traded price at EGP {REL['value']:.2f} on forward earnings "
  f"and EGP {BOOK['value']:.2f} on disclosed book. The technical picture has turned: the price came off its short "
  "averages with negative momentum and sits in the middle of its own 52-week range. The probabilistic map is the one "
  f"piece untouched by any of this: its median ({q60['50']:.2f}) sits above the anchor because the repricing that "
  "carried this stock over the sample period has not yet statistically died. That is a description of measured price "
  "behaviour, not a claim about value, and it does not know what an associate stake is worth.")
rows = [
 ['Lens', 'What it reads', 'Central / implication'],
 ['Fundamental — primary, carrying-value branch', 'The associate at its reviewed carrying value', f"EGP {V_LO:.2f} ({sgn(GAP_LO)})"],
 ['Fundamental — primary, round-price branch', 'The associate at the June-2026 round price', f"EGP {V_HI:.2f} ({sgn(GAP_HI)})"],
 ['Fundamental — cross-checks', 'Forward earnings multiple · disclosed book floor', f"EGP {REL['value']:.2f} · {BOOK['value']:.2f}"],
 ['Technical', 'Momentum lost, long trend intact', 'Below the 20- and 50-day averages; above the 100- and 200-day'],
 ['Simulation (three months)', 'Drift up, right-skewed', f"Median {q60['50']:.2f}; p5–p95 {q60['5']:.2f}–{q60['95']:.2f}"],
]
table(rows, [2.3, 2.3, 2.3], first_col_bold=True)
rich([('A fair-value read, not a recommendation. ', dict(bold=True)),
      (f"GB Corp trades below both branches of its primary lens, and the distance between those branches rests on a "
       f"basis question rather than a fact: the company states a {pc(STAKE,2)} holding in MNT-Halan, carries it at EGP "
       f"{MARK_LO/1000:.1f} bn in its own reviewed balance sheet, and announced a funding round in June 2026 that marks "
       f"the same holding at EGP {MARK_HI/1000:.1f} bn. What the traded price leaves for ALL the associates together is "
       f"EGP {PRICE_ASSOC/1000:.1f} bn. Strip the associate leg out and what remains — the auto business and the lender "
       f"— is {pc(OPERATING_EQ/D['mktcap'],0)} of the entire market capitalisation, which is close to what the tape and "
       "the earnings multiple already say. The honest summary is that the operating businesses are priced about right, "
       "and whether the shares are cheap depends on how much of a discount an unlisted minority financial-services stake "
       "is entitled to — a question this study poses precisely rather than settles. The envelope of the "
       f"present-value reads, EGP {ENVELOPE['low']:.2f} to {ENVELOPE['high']:.2f}, is wide enough on its own to demand "
       "real humility. We publish the distribution, not a target.", {})])

# ================= §5 catalysts ==============================================
H1('5  Catalysts to watch')
for head, body in [
 ('The next results release. ', 'The reviewed half to 30 June 2026 is the anchor this forecast is struck on; the next '
  'print is the first test of whether the auto gross margin holds where that half left it, and of whether the finance-cost '
  'line responds as policy eases.'),
 ('Policy meetings. ', 'Each cut lowers GB Capital’s funding cost, the customer’s instalment and this study’s '
  'discount rate at once — the single most mechanical catalyst on the list.'),
 ('An audited MNT-Halan financial statement. ', 'The one disclosure that would collapse the gap between this study’s two '
  'branches. The reviewers of GB Corp’s own 30 June 2026 statements were not given that company’s accounts and said so; '
  'until somebody is, the carrying value and the round price are two claims with nothing between them.'),
 ('A secondary transaction in the associate’s shares. ', 'A real trade at a real price is the only thing that would tell '
  'a reader which of the two branches — or neither — the market should be using. Any further disclosure bearing on how '
  'an unlisted minority stake of this size should be marked is the most value-relevant event available.'),
 ('The second closing of that round. ', 'It would test whether the round’s valuation holds or moves; it does not '
  'change the ownership percentage, which the company has already stated.'),
 ('The assembly-plant ramp and new models. ', 'Added capacity and local content, and the inventory unwind behind them, are '
  'the visible working-capital catalysts.'),
 ('Competitive pricing from new entrants. ', 'The clearest threat to passenger-car prices and share in a recovering market.'),
 ('Regional normalisation. ', 'Part of passenger-car revenue is Iraq and Jordan. This study does not hold a sourced split '
  'of that revenue for the reviewed half, so the exposure is named and not priced; any de-escalation restores the '
  'fastest-margin sales in the mix.'),
 ('The pound. ', 'A step devaluation is the compound risk — assembly costs, rates, and the pound value of the round-price '
  'mark at once; continued stability is the quiet tailwind.'),
 ('The dividend decision. ', 'A payout step-up would mark the cash-conversion inflection this study is waiting for. The '
  'model’s own forecast cash flows carry the constraint: the first forecast year converts EGP '
  f"{dcf['rows'][0]['fcff']:,.0f} mn of free cash flow against EGP {dcf['rows'][-1]['fcff']:,.0f} mn in the last."),
]:
    bullet(body, bold_head=head)

# ================= §6 zones ==================================================
H1('6  Reading the probability zones')
_bounds = [26, 30, 34, 38]
P(f'Translating the three-month distribution into plain zones, anchored on the EGP {TA_CLOSE:.2f} session the cone was '
  f'struck from and on the fundamental reads of §1:')
rows = [
 ['Zone (3 months)', 'Range', 'Probability', 'What it would mean'],
 ['Deep downside', f'below EGP {_bounds[0]}', pc(zones[0], 0), 'Regional escalation or a devaluation; tests the lower shelf'],
 ['Lower band', f'EGP {_bounds[0]}–{_bounds[1]}', pc(zones[1], 0), 'Margin proof delayed; the earnings multiple dominates'],
 ['Around the anchor', f'EGP {_bounds[1]}–{_bounds[2]}', pc(zones[2], 0), 'Status quo; the price sits near disclosed book and pays nothing for the associate'],
 ['Upper band', f'EGP {_bounds[2]}–{_bounds[3]}', pc(zones[3], 0), 'Cuts and the working-capital release credited'],
 ['Strong upside', f'above EGP {_bounds[3]}', pc(zones[4], 0), 'The market begins to pay something for the associate line'],
]
table(rows, [1.5, 1.3, 1.2, 2.9], first_col_bold=True)
P(f'The distribution is right-skewed by construction: the calibrated secular drift plus fat-tailed innovations put '
  f'{pc(zones[4],0)} of terminal mass above EGP {_bounds[3]}. Read that with Appendix B open. The drift term is what the '
  f'calibration test accepted, and that appendix states the margin rather than flattering it. This is the spread of '
  'outcomes consistent with the stock’s own measured behaviour and the factor stack; it is not a forecast.')

# ================= §7 caveats ================================================
H1('7  Caveats and what would change our mind')
for head, body in [
 ('The answer has two sides, and neither is a hedge. ',
  f'GB Corp carries its MNT-Halan interest at EGP {MARK_LO/1000:.1f} bn in its own reviewed balance sheet at 30 June 2026 '
  f'and announced a June-2026 funding round that marks the same interest at EGP {MARK_HI/1000:.1f} bn. Both are the '
  f'company’s own disclosures; the filings do not decide between them and neither does this study. The two answers, EGP '
  f'{V_LO:.2f} and {V_HI:.2f}, differ in that one line and in nothing else — the auto leg, the lender and the residual '
  'associates are identical. Averaging them would produce a figure neither disclosure supports.'),
 ('The lower branch is not a safe harbour, and this is the most important sentence in the study. ',
  'The limited review of the 30 June 2026 consolidated statements reaches a QUALIFIED conclusion, and it is qualified at '
  'exactly this line: the reviewers state they “were not provided with the consolidated financial statements for one of '
  'the associate companies (MNT – BV)” and were therefore “unable to verify the accuracy of the Group’s share of the '
  f'profits” — EGP {n1(SHARE_OF_PROFIT)} mn recorded in the period. The same qualification stood on the '
  '31 December 2025 audited statements. So the conservative branch of this study rests on a carrying value that the '
  'reviewers of that balance sheet could not verify. That is a disclosure rather than a remeasurement — nothing in the '
  'valuation changes because of it — and it is the strongest available argument for discounting BOTH marks.'),
 ('The ownership percentage is disclosed twice and the two disclosures differ. ',
  f'The press release of 9 June 2026 gives {pc(STAKE,2)} from {pc(STAKE_PRIOR,2)}; the reviewed statements and the review '
  f'report give {pc(STAKE_STATEMENTS,2)} from {pc(STAKE_STATEMENTS_PRIOR,2)} for the same transaction, most likely at a '
  f'different level of the structure. This study adopts the lower, because it is the figure the round it is applied to was '
  'announced with, and prints the other rather than leaving it out. It is worth a little over one and a half per cent of '
  'the round-price branch and exactly nothing on the other.'),
 ('There is no complexity discount, and its removal is a correction rather than an opinion. ',
  'The superseded edition deducted a typed ten per cent from the sum of the parts and then weighted the discounted and '
  'undiscounted sums, applying an effective four. Both figures were parameters with nothing observable behind them and '
  'nothing in GB Corp’s filings discloses a basis for either. They are gone. What such a discount was standing in for is '
  'now named instead — the uncertainty is in the associate mark and is published as two branches.'),
 ('There is no weighted blend either. ',
  'The superseded edition published a central that averaged four reads at weights that had never been tested against any '
  'alternative. One class primary is the answer and the other reads are cross-checks; a number produced by averaging '
  'several methods is a new method with untested parameters, wearing the appearance of caution.'),
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
 ('The gap can be read as a rate rather than as a mark, and that reading is milder. ',
  f'Solving the traded price for the auto leg’s cost of capital instead of the associate mark implies {pc(RATE_HI,2)} on '
  f'the round-price branch against this study’s {pc(dcf["wacc"],2)}, and {pc(RATE_LO,2)} on the carrying-value branch. '
  'The second is an ordinary disagreement about the cost of capital in this market. Both figures are solved from the '
  'price and used nowhere; they are printed because a binary between “the market is wrong about the associate” and “our '
  'auto leg is wrong” is too neat.'),
 ('The drift is empirical, and it is thin. ', 'The secular drift is what the calibration test accepted where zero drift '
  f'did not, and the record is published rather than summarised: over {BAND["n"]} resolved three-month forecasts on this '
  f'stock the price finished inside the 90% band {pc(BAND["hits"]/BAND["n"],0)} of the time, against a 90% target. The '
  f'band is {BAND["width"]:.2f} times as wide as a naive carry-anchored one, which is disclosed here and is not a pass '
  'mark: a wider band is not automatically wrong where the tail is real. A regime turn would flip the median read; the '
  'drift is re-tested at every roll-forward and cut the moment it fails.'),
 ('The lender is a credit cycle, and its mark is a return the cycle sets. ',
  f'GB Capital is marked at {CAP["justified_pb"]:.2f}× its operating equity because a reviewed return of '
  f'{pc(CAP["roe_adopted"],2)} against a terminal cost of equity of {pc(CAP["ke_terminal"],2)} supports that and no more. '
  f'On the FY2025 full-year return of {pc(CAP["roe_fy25"],2)} the same arithmetic gives EGP {n0(CAP["value_fy25_framing"])} '
  'mn instead. The study took the reviewed half because a near-term reviewed actual outranks a stale full-year rate, and '
  'that is also the lower number; a funding-market seizure or a deterioration in credit would take it lower again.'),
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
