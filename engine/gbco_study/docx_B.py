"""Content part B: §3 → §7."""
from docx_base import *

pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
L = D['lenses']; eng = D['engine']; touch = D['mc']['touch']; zones = D['mc']['zones']
spot = D['spot']

# ================= §3 Monte Carlo ===========================================
H1('3  Monte Carlo — a probabilistic price map')
P('The probability read below opens the section, per house presentation: computed from the same 50,000 paths as everything '
  'that follows, it is a summary of the distribution, not an input to it.', size=9.8, space_after=4)
rows = [
 ['The probability read (T+60)', ''],
 ['P(price above spot)', f"{pr['p_above']*100:.0f}%"],
 ['P(+10%) vs P(−10%) — the odds', f"{pr['p_up10']*100:.0f}% vs {pr['p_dn10']*100:.0f}%  ·  {pr['odds']:.1f} : 1"],
 ['Median level, and its move', f"EGP {pr['median']:.2f}  ({pr['med_move']*100:+.1f}%)"],
 ['The 50% band (25th–75th)', f"EGP {pr['band50'][0]:.1f} – {pr['band50'][1]:.1f}   ({pr['band50_pct'][0]*100:+.0f}% / {pr['band50_pct'][1]*100:+.0f}% of spot)"],
 ['Touch(+10%) / touch(−10%) at any point', f"{pr['touch_up10']*100:.0f}%  /  {pr['touch_dn10']*100:.0f}%"],
]
table(rows, [3.3, 3.3], first_col_bold=True, band_rows=[0], header=False)
P('We simulate 50,000 three-month price paths (seed 42) with the house YZ-HAR v2 engine: width from a pooled log-HAR '
  'cascade (variance lags 1/5/22) on a gap-aware Yang-Zhang variance proxy, projecting the average daily variance over the '
  'next 60 sessions (annualized ≈ ' + f"{eng['anchor_vol']*100:.1f}%" + ' at this origin — regime-conditional by construction, '
  'with no calibration multiplier: the retired KVOL floor is replaced by the HAR width itself); shape from unit-variance '
  'Student-t(5) innovations via a per-path chi-square mixture (tighter interquartile body, honest tails); and drift that is '
  'asset-class-conditional — here the secular expanding-window drift (+' + f"{eng['drift_daily']*60*100:.1f}%" + ' per '
  'quarter), because that is the configuration that passed the Step 0 gate on this name while zero drift failed it '
  '(Appendix B). A sixteen-factor stack layers on top: seven continuous macro/operating drivers contributing a small net '
  'forward drift and nine discrete events that each fire with a probability and an impact, together adding a modest '
  f"+{eng['factor_drift_q']*100:.1f}% over the quarter.")
rich([('By design the paths diffuse from spot as near-term price and deliberately do not embed the fundamental NAV — the '
       'value gap of §1 is kept out of the drift. ', dict(bold=True)),
      ('The fundamental gap lives in §1, not here; §3 maps where price could go from today, not where value sits. The upward '
       'median you see is the stock\u2019s own measured secular behaviour surviving a calibration test — never a target, and '
       'never the §1 value gap smuggled in.', {})])
rows = [
 ['Continuous factor (7)', 'Dir.', 'Discrete event (9)', 'Prob.', 'Mean impact'],
 ['Egypt PC demand / rate-cut cycle', '+', '2Q26 results (11 Aug 2026)', '90%', '+0.5%'],
 ['EGP/USD drift (CKD import content)', '±', 'MNT-Halan second closing ≥ $1.4 bn', '45%', '+1.5%'],
 ['CBE easing (affordability + Capital NIM)', '+', 'CBE cut ≥ 100 bp (Aug/Oct MPC)', '50%', '+1.0%'],
 ['Iraq / Jordan regional-conflict drag', '−', 'Regional escalation spillover', '25%', '−2.5%'],
 ['Chinese grey-import competition', '−', 'BYD Egypt entry / price shock', '35%', '−1.0%'],
 ['Localization / CKD mix & Sadat ramp', '+', 'Sadat ramp / new CKD model', '55%', '+0.6%'],
 ['Funding-cost & provisioning cycle', '−', 'Dividend / capital-return surprise', '15%', '+0.8%'],
 ['', '', 'EGP step-devaluation', '12%', '−2.0%'],
 ['', '', 'EGX flows / index event', '25%', '+0.8%'],
]
table(rows, [2.15, 0.5, 2.2, 0.7, 0.95], size=8.7)
H2('Percentile map (EGP/share)')
rows = [['Horizon', 'p5', 'p25', 'p50', 'p75', 'p95'],
 ['T+20 sessions', f"{q20['5']:.1f}", f"{q20['25']:.1f}", f"{q20['50']:.1f}", f"{q20['75']:.1f}", f"{q20['95']:.1f}"],
 ['T+60 sessions', f"{q60['5']:.1f}", f"{q60['25']:.1f}", f"{q60['50']:.1f}", f"{q60['75']:.1f}", f"{q60['95']:.1f}"]]
table(rows, [1.9, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True)
P('Lead with the 50% band, not the tails: a quarter ahead, half of all paths finish between roughly EGP '
  f"{q60['25']:.0f} and {q60['75']:.0f}; at one month the band is ~EGP {q20['25']:.0f}–{q20['75']:.0f} (width ≈ ÷√3). "
  'The 5–95% cone is context, not a forecast.', size=9.8)
figure('fig4_fan.png', 6.4, 'Figure 4 — Forward price cone to T+60. The median drifts up with the calibrated secular term; '
       'the gold dashed line marks the EGP 30 fundamental central, deliberately below the median path.')
figure('fig5_dist.png', 5.2, 'Figure 5 — Price distribution at T+20.')
figure('fig6_dist.png', 5.2, 'Figure 6 — Price distribution at T+60.')
H2('Level-touch ladder')
P('The probability that price touches a level at any point by the horizon (running max for upside, running min for '
  'downside):', size=9.8)
rows = [['Level (EGP)', 'T+20 touch', 'T+60 touch', 'Note']]
notes = {40: 'Blue-sky; +28%', 38: 'Upper zone gateway', 36: 'Above the Feb high zone', 34: 'New-high territory',
         32: 'Just above spot', 30: 'The 20-day / round number', 28: 'The 50/100-day shelf', 26: 'April-low zone'}
for lv in [40, 38, 36, 34, 32, 30, 28, 26]:
    tv = touch[str(lv)]
    rows.append([f'{lv}', f"{tv['t20']*100:.0f}%", f"{tv['t60']*100:.0f}%", notes[lv]])
table(rows, [1.2, 1.2, 1.2, 3.0], first_col_bold=True)

# ================= §4 comparison =============================================
H1('4  Comparison of the lenses, and a verdict')
P(f"Three readings sit side by side, and for once they genuinely disagree. The fundamental lenses spread "
  f"{L['relative']['base']:.0f}–{L['sotp']['base']:.1f} with a central {L['central']['base']:.1f} — meaningfully below spot "
  "— but that reading is now dominated by a confirmed input (the MNT-Halan stake, 41.61%, §1.1) whose mark, not its "
  "existence, is the open question. The technical picture sits closer to the middle: above every average, momentum "
  "positive, six percent from an all-time high, but not pricing in anything like the fundamental lenses' implied "
  "re-rating. The probabilistic map is the one piece entirely unaffected by any of this: its median "
  f"({q60['50']:.0f}) sits above spot because the engine\u2019s calibrated secular drift — the EGX repricing that has "
  "carried this stock thirteen-fold in five years — has not yet statistically died; that is a description of measured "
  "price behaviour, not a claim about value, and it does not know or care what GB Corp\u2019s associate stake is worth.")
rows = [
 ['Lens', 'Reads', 'Central / implication'],
 ['Fundamental (4-lens)', 'Meaningfully undervalued — if the mark holds', f"EGP {L['central']['base']:.1f} ({(L['central']['base']/spot-1)*100:+.0f}%)"],
 ['Technical', 'Strong / extended', 'Support 30.0 / 28.2 (20d/50d); resistance 33.4 (ATH)'],
 ['Monte Carlo (3-month)', 'Drift-up, right-skewed', f"Median {q60['50']:.0f}; p5–p95 {q60['5']:.0f}–{q60['95']:.0f}"],
]
table(rows, [1.9, 1.9, 3.1], first_col_bold=True)
rich([('Verdict (a fair-value read, not a recommendation). ', dict(bold=True)),
      (f"GBCO reads meaningfully undervalued on fundamentals ({(L['central']['base']/spot-1)*100:+.0f}% central) — and "
       "unlike the first draft of this study, that verdict now rests on a confirmed number: GB Corp's own 9-June-2026 "
       "press release states its MNT-Halan stake as 41.61%. What is not confirmed is what that stake is actually worth "
       "to the market: taking the round's USD 1.4bn valuation at face value implies the stake alone is worth roughly "
       "three quarters of GB Corp's market cap, which the market plainly does not credit. Strip the associate leg out "
       "and the remaining business — Auto plus GB Capital — reads close to fairly valued against spot, in line with "
       "what the tape and the Monte Carlo distribution already show. The honest summary is: the operating business is "
       "priced about right; whether the shares are cheap depends on how much of a discount the market is entitled to "
       "apply to an unlisted, minority financial-services stake — a legitimate valuation question this study raises "
       "rather than settles. The bear–bull span "
       f"(EGP {L['central']['bear']:.0f}–{L['central']['bull']:.0f}) is wide enough on its own to demand real humility, and "
       "readers should treat the stake-sensitivity table in §1.1 as showing where the discount debate lives, not the "
       f"single central number. We publish the distribution, not a target.", {})])

# ================= §5 catalysts ==============================================
H1('5  Catalysts to watch')
for head, body in [
 ('2Q26 results (11 Aug 2026). ', 'First read on whether the 1Q26 margin dip (12.4% Auto GPM) was the regional-drag trough; '
  'watch Egypt PC volumes vs the +42% 1Q pace and the finance-cost line as CBE cuts feed through.'),
 ('CBE MPC meetings (Aug / Oct 2026). ', 'Each 100 bp cut lowers GB Capital funding costs, customer instalments and this '
  'study\u2019s discount rate — the single most mechanical catalyst.'),
 ('The MNT-Halan mark and discount — no longer the stake. ', 'GB Corp confirmed its current stake (41.61%, 9-Jun-2026); '
  'the open question now is whether the market accepts the round\u2019s USD 1.4bn valuation at face value or applies a '
  'steeper illiquidity/minority discount. Any secondary transaction, analyst note, or further disclosure bearing on how '
  'the market should mark an unlisted 41.61% stake is the single most value-relevant catalyst left.'),
 ('MNT-Halan second closing. ', 'The round\u2019s first close (9 Jun 2026) already fixed GB Corp\u2019s post-transaction '
  'stake at 41.61%; a second closing would mainly test whether the USD 1.4bn valuation holds or moves, not the '
  'ownership percentage itself.'),
 ('Sadat ramp and new CKD models. ', 'The June-2026 inauguration adds capacity and local content; model announcements and '
  'the inventory unwind are the visible working-capital catalysts.'),
 ('BYD entry pricing. ', 'The clearest competitive threat to PC ASPs and share in the recovering Egyptian market.'),
 ('Iraq / Jordan normalization. ', '~19.5% of PC revenue; any de-escalation restores the fastest-margin sales in the mix.'),
 ('The pound. ', 'A step-devaluation is the compound risk (CKD costs, rates, the EGP value of every mark); continued '
  'stability is the quiet tailwind.'),
 ('Dividend decision. ', 'FY25 paid ~EGP 0.35/share (~13% payout); with Auto deleveraging to 2.14× ND/EBITDA, a payout step-up '
  'would mark the cash-conversion inflection this study is waiting for (device A-2 schedule in Appendix A).'),
]:
    bullet(body, bold_head=head)

# ================= §6 zones ==================================================
H1('6  Reading the probability zones')
P('Translating the three-month distribution into plain zones, anchored on spot EGP 31.25 and the fair-value cluster:')
rows = [
 ['Zone (T+60)', 'Range', 'Approx. probability', 'What it would mean'],
 ['Deep downside', '< EGP 26', f'~{zones[0]*100:.0f}%', 'Regional escalation / devaluation; tests the April shelf'],
 ['Lower band', 'EGP 26–30', f'~{zones[1]*100:.0f}%', 'Margin proof delayed; relative-multiple lens dominates'],
 ['Around spot', 'EGP 30–34', f'~{zones[2]*100:.0f}%', 'Status quo; fair value and price coexist'],
 ['Upper band', 'EGP 34–38', f'~{zones[3]*100:.0f}%', 'Cuts + WC release credited; new-high extension'],
 ['Strong upside', '> EGP 38', f'~{zones[4]*100:.0f}%', 'Secular repricing continues; discount narrows toward NAV'],
]
table(rows, [1.5, 1.3, 1.5, 2.6], first_col_bold=True)
P('The distribution is right-skewed by construction — the calibrated secular drift plus fat-tailed innovations put roughly a '
  'third of terminal mass above EGP 38, more than any other single zone. Read that with Appendix B open: the drift term '
  'passed its test, but on 17 non-overlapping windows with a thin margin. It is the spread of outcomes consistent with the '
  'stock\u2019s own measured behaviour and the factor stack; it is not a forecast.')

# ================= §7 caveats ================================================
H1('7  Caveats and what would change our mind')
for head, body in [
 ('The MNT-Halan stake is confirmed; what it is worth is not. ', 'GB Corp\u2019s own 9-June-2026 press release states its '
  'current stake directly: 41.61%, down from 42.58% pre-transaction. That removes the sourcing uncertainty this study '
  'originally flagged. What remains genuinely open is the mark: taking the round\u2019s USD 1.4bn valuation at face value '
  'implies the stake alone is worth \u2248EGP 27.7bn — roughly three quarters of GB Corp\u2019s entire market cap. If the '
  'market is right to discount that mark far more heavily than this study\u2019s uniform 10%, the SOTP compresses toward '
  'the relative and normalized lenses, i.e. toward fair value, not undervalued.'),
 ('Working capital is the second-order model. ', 'The DCF\u2019s Auto-leg value lives in the glide from 28.5% to 21.5% WC '
  'intensity; if 26–28% is the new structural cost of holding share (import finance, CKD stock), the Auto leg is worth '
  'EGP 4–8/share less — a real but now secondary lever next to the mark-and-discount question above.'),
 ('Terminal-value dependency. ', f"{D['dcf']['tv_pct']*100:.0f}% of the Auto EV is terminal value at a 10.5-pt WACC−g spread; "
  'the §1.9 grid is the honest statement that this is partly a bet on Egyptian nominal normalization.'),
 ('The drift is empirical, and thin. ', 'Secular drift passed Step 0 (CRPS skill +3.2% non-overlapping, +9.6% monthly) where '
  'zero drift failed — but the bootstrap CI spans zero (P(skill>0) ≈ 0.62 on 17 windows). A regime turn — the exact failure '
  'mode that killed trend drift on Samsung and Tata — would flip the median read; we will re-test every quarter and cut the '
  'drift the moment it fails.'),
 ('The associate mark is real but private, and now the study\u2019s central bet. ', 'MNT-Halan\u2019s USD 1.4bn is a genuine '
  'transaction price — cash changed hands — but for an unlisted company and, per public reporting, only an initial '
  'tranche of an ongoing round (a second closing remains open, size and terms undisclosed). The stake applied to it '
  '(41.61%) is now confirmed and current, not the uncertainty it was; the bear case in the football field instead applies '
  'a much heavier discount to the mark itself, which is why its EGP 24 floor sits far below the base case.'),
 ('The lender is a credit cycle. ', 'GB Capital\u2019s 15% adjusted ROAE and 2.1–2.5% NPLs are cycle-friendly numbers struck '
  'in an easing cycle; a funding-market seizure or NPL spike would break the 1.0× book mark.'),
 ('Consolidation approximations. ', 'The consolidated forecast maps eliminations, minority interests and the grouped '
  'balance-sheet layout with stated simplifications (flagged in the model); segment disclosure, not audited consolidation '
  'schedules, is the source.'),
 ('Technical reminder. ', 'An extended tape above every average mean-reverts routinely; the strong chart says nothing about '
  'value and can unwind 10% without touching the thesis. The technical read is context, not a trigger.'),
]:
    bullet(body, bold_head=head)
