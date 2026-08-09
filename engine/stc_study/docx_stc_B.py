"""Content part B: §3 → §7."""
from docx_stc_base import *

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
 ['Median level, and its move', f"SAR {pr['median']:.2f}  ({pr['med_move']*100:+.1f}%)"],
 ['The 50% band (25th–75th)', f"SAR {pr['band50'][0]:.1f} – {pr['band50'][1]:.1f}   ({pr['band50_pct'][0]*100:+.1f}% / {pr['band50_pct'][1]*100:+.1f}% of spot)"],
 ['Touch(+10%) / touch(−10%) at any point', f"{pr['touch_up10']*100:.0f}%  /  {pr['touch_dn10']*100:.0f}%"],
]
table(rows, [3.3, 3.3], first_col_bold=True, band_rows=[0], header=False)
P('We simulate 50,000 three-month price paths (seed 42) with the house YZ-HAR v2 engine: width from a pooled log-HAR '
  'cascade (variance lags 1/5/22) on a gap-aware Yang-Zhang variance proxy, projecting the average daily variance over the '
  'next 60 sessions (annualized ≈ ' + f"{eng['anchor_vol']*100:.1f}%" + ' at this origin — modestly above the very calm 13.0% '
  'trailing figure, because the HAR reads the current regime rather than averaging the past; no calibration multiplier — '
  'the retired KVOL floor is replaced by the HAR width itself); shape from unit-variance Student-t(5) innovations via a '
  'per-path chi-square mixture (tighter interquartile body, honest tails); and drift that is asset-class-conditional — '
  'here ZERO, because stc is an international/GCC name and zero drift is the configuration that passed the Step 0 gate '
  '(secular drift failed it: CRPS skill −4.8%; the full backtest stays on file in the Calibration Ledger). A sixteen-factor stack layers on top: seven continuous '
  'macro/operating drivers and nine discrete events that each fire with a probability and an impact, together adding a '
  f"modest +{eng['factor_drift_q']*100:.1f}% over the quarter.")
rich([('By design the paths diffuse from spot as near-term price and deliberately do not embed the fundamental fair value — '
       'the value gap of §1 is kept out of the drift. ', dict(bold=True)),
      ('The fundamental gap lives in §1, not here; §3 maps where price could go from today, not where value sits. The '
       'near-even median you see is the honest consequence of zero drift on a calm tape — never a target, and never the '
       '§1 value gap smuggled in.', {})])
rows = [
 ['Continuous factor (7)', 'Dir.', 'Discrete event (9)', 'Prob.', 'Mean impact'],
 ['SAMA/Fed policy-rate path (easing)', '+', '2Q26 results (~late Jul 2026)', '90%', '+0.4%'],
 ['Oil price / fiscal impulse (govt ICT spend)', '+', 'Special dividend with 2Q/3Q results', '20%', '+2.0%'],
 ['Vision 2030 / non-oil digital demand', '+', 'SAMA/Fed cut ≥25 bp (Sep/Oct)', '55%', '+0.6%'],
 ['KSA mobile competition (Mobily/Zain)', '−', 'center3/HUMAIN AI-DC milestone', '35%', '+1.0%'],
 ['Data-centre/AI buildout economics', '±', 'TAWAL/DIIC monetization event', '10%', '+1.5%'],
 ['Subsidiary drag→contribution', '±', 'Telefónica mark deterioration', '25%', '−0.6%'],
 ['TASI flows / index weight', '±', 'KSA mobile price-war escalation', '20%', '−1.5%'],
 ['', '', 'Regional geopolitical escalation', '25%', '−2.0%'],
 ['', '', 'PIF sell-down / index-flow event', '10%', '−1.2%'],
]
table(rows, [2.15, 0.5, 2.2, 0.7, 0.95], size=8.7)
caption('All factor numbers are editable judgments (the table is the model); flagged uncalibrated pending red-pen sign-off. '
        'Net continuous drift +0.2%/quarter, expected event drift +0.5% — near-zero central drift with mildly asymmetric tails. '
        'No FX factor: the riyal is pegged.')
H2('Percentile map (SAR/share)')
rows = [['Horizon', 'p5', 'p25', 'p50', 'p75', 'p95'],
 ['T+20 sessions', f"{q20['5']:.1f}", f"{q20['25']:.1f}", f"{q20['50']:.1f}", f"{q20['75']:.1f}", f"{q20['95']:.1f}"],
 ['T+60 sessions', f"{q60['5']:.1f}", f"{q60['25']:.1f}", f"{q60['50']:.1f}", f"{q60['75']:.1f}", f"{q60['95']:.1f}"]]
table(rows, [1.9, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True)
P('Lead with the 50% band, not the tails: a quarter ahead, half of all paths finish between roughly SAR '
  f"{q60['25']:.0f} and {q60['75']:.0f} (−3.6% / +5.2%); at one month the band is ~SAR {q20['25']:.0f}–{q20['75']:.0f} "
  '(width ≈ ÷√3). The 5–95% cone is context, not a forecast — and on this name it is unusually narrow (±12%), the direct '
  'consequence of the low-volatility regime the HAR width reads.', size=9.8)
figure('fig4_fan.png', 6.4, 'Figure 4 — Forward price cone to T+60. The median tracks spot under zero drift; the brass '
       'dashed line marks the SAR 47 fundamental central, deliberately inside the upper half of the cone rather than at its centre.')
figure('fig5_dist.png', 5.2, 'Figure 5 — Price distribution at T+20.')
figure('fig6_dist.png', 5.2, 'Figure 6 — Price distribution at T+60.')
H2('Level-touch ladder')
P('The probability that price touches a level at any point by the horizon (running max for upside, running min for '
  'downside):', size=9.8)
rows = [['Level (SAR)', 'T+20 touch', 'T+60 touch', 'Note']]
notes = {50: 'Round number; +14.7%', 48: 'Above the 52-week high', 46: 'Just past the Oct-25 high zone', 44: 'First resistance above spot',
         42: 'The March base', 40: 'The 52-week-low shelf', 38: 'Stress zone', 36: 'Crisis zone'}
for lv in [50, 48, 46, 44, 42, 40, 38, 36]:
    tv = touch[str(lv)]
    rows.append([f'{lv}', f"{tv['t20']*100:.0f}%", f"{tv['t60']*100:.0f}%", notes[lv]])
table(rows, [1.2, 1.2, 1.2, 3.0], first_col_bold=True)

# ================= §4 comparison =============================================
H1('4  Comparison of the lenses, and a verdict')
P(f"Three readings, one coherent picture. The fundamental lenses cluster between {L['normalized']['base']:.0f} and "
  f"{L['dcf']['base']:.0f} with a central of {L['central']['base']:.0f} — {(L['central']['base']/spot-1)*100:+.0f}% versus "
  "spot — and, unusually for this series, the disagreement between them is small: the argument is not about what stc earns "
  "but about what its capex cycle and discount rate deserve. The technical picture is a flat, compressed, low-volatility "
  "base — no trend to confirm or fight. The probabilistic map says the market is likely to keep the stock within a few "
  f"riyals of spot over the quarter (50% band {q60['25']:.0f}–{q60['75']:.0f}), with a mild upside tilt from the factor "
  "stack and near-even odds either side of today’s price. Where the tension lives is §1.7: the locked dividend against "
  "the investment phase — a question the next few quarterly prints answer in cash, not in narrative.")
rows = [
 ['Lens', 'Reads', 'Central / implication'],
 ['Fundamental (4-lens)', 'Modestly undervalued', f"SAR {L['central']['base']:.0f} ({(L['central']['base']/spot-1)*100:+.0f}%)"],
 ['Technical', 'Flat, coiled, low-vol', 'Support ~42 (March base); resistance 45.4 (52w high)'],
 ['Monte Carlo (3-month)', 'Near-even, mild up-tilt', f"Median {q60['50']:.1f}; p5–p95 {q60['5']:.0f}–{q60['95']:.0f}"],
]
table(rows, [1.9, 1.9, 3.1], first_col_bold=True)
rich([('Verdict (a fair-value read, not a recommendation). ', dict(bold=True)),
      (f"stc reads modestly undervalued ({(L['central']['base']/spot-1)*100:+.0f}% to the central) with an unusually "
       "well-defined path to being proven right or wrong: hold the EBITDA margin glide, keep capex inside the guided band, "
       "and the locked 5% yield plus mid-single-digit cash-flow growth does the rest; let capex run at the top of the band "
       "through 2027 while consumer competition bites, and today’s price is fair. The lens cluster is tight enough "
       f"(bear–bull {L['central']['bear']:.0f}–{L['central']['bull']:.0f} driven almost wholly by terminal arithmetic) that "
       "we would characterize the stock as a bond-like core holding with two free options — the AI-infrastructure build "
       "and the fintech/bank adjacency — rather than a re-rating story. We publish the distribution, not a target.", {})])

# ================= §5 catalysts ==============================================
H1('5  Catalysts to watch')
for head, body in [
 ('2Q26 results (~late July 2026). ', 'The first full quarter to show whether Q1’s cash-flow inflection (FCF 3.9 bn, '
  '1.4× the quarterly dividend) is a run-rate or a blip; watch enterprise revenue (mega-project phasing) and capex phasing.'),
 ('Quarterly dividend declarations. ', 'SAR 0.55 is policy through Q3-2027 — the information is in any SPECIAL '
  'distribution (the policy explicitly allows quarterly assessment; FY24 paid SAR 2.00). A special would mechanically '
  're-rate the DDM lens; its absence through 2026 keeps the balance sheet funding the build.'),
 ('SAMA/Fed decisions (Sep/Oct 2026). ', 'Each 25–50 bp off the Saudi curve lowers this study’s discount rate and the '
  'marginal cost of the sukuk-funded infrastructure build — the single most mechanical catalyst.'),
 ('center3–HUMAIN milestones. ', 'The 1 GW AI-data-centre ambition (framework Dec-2025) converts to value only as '
  'contracted megawatts and disclosed economics; any capacity/offtake announcement is the option going in-the-money.'),
 ('TAWAL/DIIC monetization. ', 'stc still owns 43.06% of the region’s largest tower company; an IPO or stake sale would '
  'crystallize a mark this study carries at a conservative SAR 4.6 bn book. Speculation only — nothing announced.'),
 ('KSA mobile competitive prints. ', 'Mobily’s subscriber momentum vs stc’s +5.3%; a price response from any of the '
  'three would show first in consumer ARPU-proxy (CBU revenue per sub).'),
 ('Telefónica. ', 'The 9.97% stake (€2.1 bn cost) trades ≈7% below cost with a halved dividend; further deterioration is '
  'a mark-to-market drag, any Spanish-market recovery a small tailwind — the stake is ~3.5% of the DCF equity bridge.'),
 ('Index / flow events. ', 'PIF sold 2% in Nov-2024 at SAR 38.6 (float now ~38%); any further sell-down is a supply '
  'event, any float-driven index-weight uplift a demand event.'),
]:
    bullet(body, bold_head=head)

# ================= §6 zones ==================================================
H1('6  Reading the probability zones')
P('Translating the three-month distribution into plain zones, anchored on spot SAR 43.58 and the fair-value cluster:')
rows = [
 ['Zone (T+60)', 'Range', 'Approx. probability', 'What it would mean'],
 ['Deep downside', '< SAR 38', f'~{zones[0]*100:.0f}%', 'Regional shock / price war; below the 52-week low'],
 ['Lower band', 'SAR 38–42', f'~{zones[1]*100:.0f}%', 'Capex runs hot, cover stays sub-1×; March base retested'],
 ['Around spot', 'SAR 42–46', f'~{zones[2]*100:.0f}%', 'Status quo: yield carries the return; ~52% of all paths'],
 ['Upper band', 'SAR 46–50', f'~{zones[3]*100:.0f}%', 'Cover proven / cuts delivered; presses the 52-week high'],
 ['Strong upside', '> SAR 50', f'~{zones[4]*100:.0f}%', 'Special dividend or AI-build monetization credited'],
]
table(rows, [1.5, 1.3, 1.5, 2.6], first_col_bold=True)
P('The distribution is mildly right-skewed — the touch ladder shows a 17% chance of tagging +10% at some point against '
  '11% for −10% — but the mass is concentrated: more than half of all paths finish within ±SAR 2.5 of spot. That '
  'concentration is the calm-regime HAR width, not a view; a volatility-regime shift would widen the cone mechanically at '
  'the next quarterly re-run.')

# ================= §7 caveats ================================================
H1('7  Caveats and what would change our mind')
for head, body in [
 ('The dividend-vs-capex tension is the model. ', 'The FY26E cover of 0.86–1.04× is an estimate built on management’s own '
  'capex band and our margin glide; two consecutive quarters of FCF below the SAR 2.74 bn quarterly dividend bill would '
  'push the DDM lens toward its bear case and the balance sheet toward releveraging — watch the quarterly FCF line, '
  'not the payout announcements.'),
 ('Terminal-value dependency. ', '80% of the DCF’s enterprise value is terminal at a 5.1-point WACC−g spread; §1.9 is '
  'the honest statement that this valuation is substantially a duration bet on Saudi discount rates.'),
 ('The risk-free rate is derived, and the beta is short-window. ', 'The 5.5% rf triangulates a government-guaranteed USD '
  'print plus an officially documented SAR pickup — a screen-quoted SAR 10Y, when accessible, replaces it. The 0.48 beta '
  'passes the house gate on nine weeks of data; a 2–5-year weekly regression should replace it, and §1.9 shows the '
  'valuation at every beta to 1.2. Both are logged as open flags.'),
 ('Competition is the slow leak. ', 'stc’s consumer growth (+3%) already trails Mobily’s subscriber momentum; a price '
  'war in KSA mobile — three players, one regulator, heavy 5G capacity — is the scenario in which the margin glide '
  'reverses and every lens compresses toward the normalized floor.'),
 ('The subsidiary portfolio is an investment phase, not yet a return. ', 'stc bank (8 mn customers, SAMA-licensed '
  'Jan-2025), center3, SCCC and iot squared are guided to turn contribution-positive from 2026; if they stay dilutive '
  'through FY27, the margin glide to 32.5% is wrong by construction.'),
 ('The stake marks are point-in-time. ', 'Telefónica (9.97%) is marked at market (≈SAR 8.6 bn, ~7% below cost) and the '
  'tower stake at carrying value (SAR 4.6 bn) — the former moves daily, the latter is conservative against any '
  'transaction mark; together they are ~5% of the bridge.'),
 ('OCF conversion. ', 'Reported FY25 FCF (6.5 bn) ran well below model FCFF on receivables build and one-off cash items; '
  'we model an explicit conversion drag, but a government-receivables cycle that widens rather than narrows would make '
  'even the 0.86× bear cover optimistic.'),
 ('Technical reminder. ', 'A compressed, low-volatility tape can break either way; the narrow cone in §3 is a regime '
  'read, not a promise. The technical section is context, not a trigger.'),
]:
    bullet(body, bold_head=head)
