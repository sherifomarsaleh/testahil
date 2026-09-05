"""Content part B: §3 → §7."""
from docx_stc_base import *
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# Absolute against this file's own directory: the builders read and wrote relative
# to the working directory, so running them from the repository root — which is how
# every gate does — found no inputs and scattered the outputs.


pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
L = D['lenses']; eng = D['engine']; touch = D['mc']['touch']; zones = D['mc']['zones']
spot = D['spot']; band = D['band_record']; dcf = D['dcf']; coc = D['coc_record']
beta = D['dcf']['wacc_build']['beta_reg']
anchor = D['cone_anchor']
hz1, hz3 = eng['horizons']['1M'], eng['horizons']['3M']


def _d(iso):
    """A grade date a reader can read, from the date the engine committed to."""
    import datetime as _dt
    return _dt.date.fromisoformat(iso).strftime('%-d %b %Y')

# ================= §3 the probabilistic price map =============================
H1('3  A probabilistic price map')
P('The probability read below opens the section: computed from the same 50,000 paths as everything that follows, it is '
  'a summary of the distribution, not an input to it. Both horizons are CALENDAR — one month and three months from the '
  'anchor, graded on a stated date rather than after a count of trading sessions.', size=9.8, space_after=4)
rows = [
 [f"The probability read ({hz3['label']}, graded {_d(hz3['grade_date'])})", ''],
 ['Chance the price finishes above the anchor', f"{pr['p_above']*100:.0f}%"],
 ['Chance of +10% against −10% — the odds', f"{pr['p_up10']*100:.0f}% vs {pr['p_dn10']*100:.0f}%  ·  {pr['odds']:.1f} : 1"],
 ['Median level, and its move', f"SAR {pr['median']:.2f}  ({pr['med_move']*100:+.1f}%)"],
 ['The 50% band (25th–75th)', f"SAR {pr['band50'][0]:.1f} – {pr['band50'][1]:.1f}   ({pr['band50_pct'][0]*100:+.1f}% / {pr['band50_pct'][1]*100:+.1f}% of the anchor)"],
 ['Chance of touching ±10% at any point', f"{pr['touch_up10']*100:.0f}%  /  {pr['touch_dn10']*100:.0f}%"],
]
table(rows, [3.3, 3.3], first_col_bold=True, band_rows=[0], header=False)

# THE CONE IS THE PUBLISHED ONE. What stood here described a study-local simulation that
# was not the model this house runs — five degrees of freedom against a fitted fifteen, no
# width calibration at all, zero drift on a market that runs an active momentum lean, a
# horizon fixed at sixty sessions, and a stack of nine typed event probabilities the
# caption itself conceded were uncalibrated. It published a different cone from the one on
# the site for the same name on the same day. Every figure here is now the production run.
P('How the cone is built. We simulate 50,000 price paths from the anchor (seed 42) with the house engine: the width '
  f"comes from a cascade of this stock's own recent, medium and longer-run variation, projected forward over the horizon "
  f"(annualised {eng['horizons']['3M']['anchor_vol_ann']*100:.1f}% at three months, {eng['horizons']['1M']['anchor_vol_ann']*100:.1f}% at one), then scaled by the "
  f"calibration this market's whole panel was fitted to ({eng['width_cal']:.3f}). The shape of the tails is a "
  "Student-t drawn at the same fitted setting. The two numbers trade off against each other, so neither is quoted as "
  "precise on its own — the honest object is the cone they jointly produce, and the record of how often it has held "
  "follows below.")
rich([('The centre of the cone is not a view. ', dict(bold=True)),
      ("It is the cost of carry — what money earns while it waits — plus one small lean, described next. The paths "
       "deliberately do not know the fundamental fair value of §1: the two lenses are kept apart so that when they "
       "agree it is information rather than an echo. §1 says what the business is worth; §3 says where the price could "
       "travel from where it is.", {})])
rich([('The direction call. ', dict(bold=True)),
      (f"This market runs a measured momentum lean, and every covered name states the direction its own reading points "
       f"— including the names where the reading is too weak to move anything. stc reads {eng['signal_z']:+.2f}, which "
       f"is {'past' if eng['call_strength']=='live' else 'inside'} the {eng['dead_zone']:.2f} threshold below which no "
       f"tilt is applied at all, so the call is {eng['call'].upper()} and it {'carries' if eng['call_strength']=='live' else 'carries no'} weight: it shifts the "
       f"centre of the three-month cone by {eng['horizons']['3M']['signal_alpha']*100:+.2f}% and the one-month cone by "
       f"{eng['horizons']['1M']['signal_alpha']*100:+.2f}%. Those are small numbers on purpose. The lean is capped at the "
       "strength the evidence actually measured; past that point a bigger number is a deliberately worse forecast rather "
       "than a braver one.", {})])

H2('How often these bands have actually held')
# DEPTH-BAR STANDARD 4: the calibration evidence belongs HERE, in plain language with the
# statistics inline — there is no calibration appendix, deliberately. The sentences are
# rendered by the module that owns them rather than re-worded, because six independent
# phrasings of this claim had already drifted apart once.
P(band['record_clause'], size=10.5)
P(band['width_clause'] + ' ' +
  ('A wider band is not automatically a worse one: covering a name honestly costs width, and the number is published '
   'beside the record rather than turned into a pass mark.' if band['width'] >= 1.03 else
   'That is about as tight as the simplest possible rule would draw it.'), size=9.8)
if band['flag'] is None:
    P('No flag is raised, and that is the ordinary case rather than an omission: on a two-sided test at the 5% level, '
      f"{band['cov90']*100:.0f}% inside a 90% band over {band['n']} forecasts is what a cone that works looks like "
      f"(p = {band['p_value']:.2f}). Had the bands run persistently narrow — price escaping more often than a 90% band "
      'should allow — or persistently wide, this study would say so here in those words. It says nothing because '
      'nothing has been earned either way.', size=9.8)
P(f"The record is {band['strength']} by this study's own standard: {band['n']} resolved three-month forecasts is enough "
  "history to judge this name on its own rather than falling back on the market's, and every one of them is a forecast "
  'that was published before its outcome was known and graded on a date fixed in advance.', size=9.8)

H2('Percentile map (SAR/share)')
rows = [['Horizon', 'Graded on', 'p5', 'p25', 'p50', 'p75', 'p95']]
for k in ('1M', '3M'):
    h = eng['horizons'][k]; q = q20 if k == '1M' else q60
    rows.append([h['label'].capitalize(), _d(h['grade_date']),
                 f"{q['5']:.1f}", f"{q['25']:.1f}", f"{q['50']:.1f}", f"{q['75']:.1f}", f"{q['95']:.1f}"])
table(rows, [1.25, 1.15, 0.85, 0.85, 0.85, 0.85, 0.85], first_col_bold=True)
P('Lead with the 50% band, not the tails: three months out, half of all paths finish between roughly SAR '
  f"{q60['25']:.0f} and {q60['75']:.0f} ({(q60['25']/anchor-1)*100:+.1f}% / {(q60['75']/anchor-1)*100:+.1f}%); at one "
  f"month the band is about SAR {q20['25']:.0f}–{q20['75']:.0f}. The 5th-to-95th cone is context rather than a forecast, "
  f"and on this name it is {(q60['95']/q60['5']-1)*100:.0f}% wide from end to end — the direct consequence of the calm "
  'regime the width estimator is reading.', size=9.8)
# THE CAPTION'S CLAIM IS COMPUTED, NOT ASSERTED. "Below the whole cone" is a testable
# statement about the picture, so it is tested against the picture's own data before it is
# printed — and if the two lenses ever stop disagreeing this way, the assertion fires
# rather than the caption quietly becoming false.
import numpy as _np
_fan_low = _np.load(os.path.join(HERE, 'fan.npy'))[0]
assert D['central'] < _fan_low.min(), 'the caption below claims the central sits under the whole cone'
figure(os.path.join(HERE, 'fig4_fan.png'), 6.4,
       f"Figure 4 — The forward price cone over {hz3['label']}, from the anchor of SAR {anchor:.2f}. The median carries "
       'at the cost of money plus the small momentum lean. The brass dashed line is this study\u2019s fundamental central '
       f"of SAR {D['central']:.2f} — below every part of the cone, including its 5th percentile, which never falls under "
       f"SAR {_fan_low.min():.2f}. The two lenses disagree, and the study shows the disagreement rather than "
       'reconciling it.')
figure(os.path.join(HERE, 'fig5_dist.png'), 5.2, f"Figure 5 — Where the price lands after {eng['horizons']['1M']['label']}.")
figure(os.path.join(HERE, 'fig6_dist.png'), 5.2, f"Figure 6 — Where the price lands after {eng['horizons']['3M']['label']}.")

H2('Level-touch ladder')
P('The chance that price reaches a level at any point before the horizon, rather than finishing there (a running '
  'maximum for levels above, a running minimum for those below):', size=9.8)
rows = [['Level (SAR)', f"By {hz1['label']}", f"By {hz3['label']}", 'Note']]
notes = {50: 'Round number; +11.8% on the anchor', 48: 'Above the 52-week high', 46: 'Just past the Oct-25 high zone',
         44: 'The anchor itself', 42: 'The March base', 40: 'The 52-week-low shelf', 38: 'Stress zone', 36: 'Crisis zone'}
for lv in [50, 48, 46, 44, 42, 40, 38, 36]:
    tv = touch[str(lv)]
    rows.append([f'{lv}', f"{tv['t20']*100:.0f}%", f"{tv['t60']*100:.0f}%", notes[lv]])
table(rows, [1.2, 1.2, 1.2, 3.0], first_col_bold=True)

# ================= §4 comparison of the lenses ================================
# THE SECTION USED TO END IN A VERDICT. It was titled "Comparison of the lenses, and a
# verdict", it published a "Fundamental (4-lens)" row — the typed blend [R-LENS-03]
# retired outright — and it closed by characterising the stock as a holding of a
# particular kind with two options attached. That is a rating in prose, which this house
# does not issue in any form. What a reader is owed is the disagreement between the
# lenses and what each one would have to be wrong about; the conclusion is theirs.
H1('4  Comparison of the lenses')
P(f"Three lenses, read side by side and never averaged. The cash-flow model is the answer this study publishes — "
  f"SAR {L['central']['base']:.2f} against a market price of SAR {spot:.2f}, {(L['central']['base']/spot-1)*100:+.1f}% — "
  f"and the others sit beside it as cross-checks rather than as weights in a blend. They do not agree, and the "
  f"disagreement is the most useful thing on this page: the earnings-multiple read on this company's own trading "
  f"history lands at SAR {L['relative']['base']:.2f}, {(L['relative']['base']/L['central']['base']-1)*100:+.0f}% above "
  f"the cash-flow answer, while the disclosed book value is SAR {L['book_value']:.2f} — a floor, not a valuation. The "
  "technical picture is a firm tape trading above its whole moving-average stack. The price map says the market is "
  f"likely to keep the stock within a few riyals of where it is over the quarter (50% band {q60['25']:.0f}–{q60['75']:.0f}).")
rows = [
 ['Lens', 'Role', 'Reads', 'Value per share'],
 ['Discounted cash flow', 'THE CENTRAL', 'Below the market',
  f"SAR {L['dcf']['base']:.2f} ({(L['dcf']['base']/spot-1)*100:+.0f}%)"],
 ['Enterprise multiple on own history', 'Cross-check', 'Above the market',
  f"SAR {L['relative']['base']:.2f} ({(L['relative']['base']/spot-1)*100:+.0f}%)"],
 ['Book value', 'Disclosed floor', 'Far below — as a floor should be',
  f"SAR {L['book_value']:.2f}"],
 ['Dividend discount', 'Cross-check', 'Below the market',
  f"SAR {L['ddm']['base']:.2f} ({(L['ddm']['base']/spot-1)*100:+.0f}%)"],
 ['Normalised earnings power', 'Cross-check', 'Below the market',
  f"SAR {L['normalized']['base']:.2f} ({(L['normalized']['base']/spot-1)*100:+.0f}%)"],
 ['Technical read', 'Context', 'Above the whole moving-average stack',
  f"Support ~{D['levels']['sup'][0]:.2f}; resistance {D['levels']['res'][0]:.2f}" if 'levels' in D else 'See §2'],
 ['The price map (three months)', 'Context', 'Near-even, a small upward lean',
  f"Median {q60['50']:.1f}; 5th–95th {q60['5']:.0f}–{q60['95']:.0f}"],
]
table(rows, [1.85, 1.15, 2.0, 1.9], first_col_bold=True, size=8.9)
caption('The envelope this study publishes is the RANGE of the present-value reads, not an average of them: '
        f"SAR {D['central_range']['low']:.2f} to {D['central_range']['high']:.2f}. No weights are applied anywhere, "
        'because a number produced by averaging several methods is a new method with parameters nobody tested — it '
        'imports the weakness of the weakest lens at whatever weight somebody typed.')
rich([('Where the lenses disagree, and what would settle it. ', dict(bold=True)),
      (f"The gap between the cash-flow answer and the multiple read is not a modelling artefact — it is one question "
       f"asked two ways. The multiple lens capitalises what this company earns today at what the market has paid for "
       f"those earnings over the last three financial year ends; the cash-flow lens charges for the capital the company "
       f"must keep spending to go on earning them. The whole difference sits in the capital expenditure cycle, and §1.7 "
       f"prices it in real units: at the lowest capital intensity of the three filed years the cash-flow answer is "
       f"SAR {D['central_range']['low']:.2f}, at the highest it is lower still. So the honest statement is that this "
       "study reads stc below its market price BECAUSE it charges the company for the investment phase it is currently "
       "in, and a reader who believes that phase ends sooner, or earns more than the model credits, should hold the "
       "multiple read instead — the study publishes both rather than choosing for them. What would settle it is "
       "disclosed economics on the data-centre build and two more years of capital intensity: neither is available "
       "today, and neither is invented here.", {})])

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
P(f'Translating the three-month distribution into plain zones, anchored on the cone\'s own '
  f'origin of SAR {D["cone_anchor"]:.2f} on {D["cone_anchor_date"]} \u2014 which is the last '
  f'session in the price library and NOT the {D["spot_date"]} close of SAR {D["spot"]:.2f} the '
  f'valuation is measured against. Two clocks, and the study says which is which:')
# THE ZONE PROBABILITIES ARE COMPUTED, NOT DESCRIBED. The cell that read "~52% of all
# paths" was typed, and it disagreed with the number in the column beside it.
_zone_rows = [
 ('Deep downside', '< SAR 38', 'A regional shock or a price war; below the 52-week low'),
 ('Lower band', 'SAR 38–42', 'Capital spending runs hot and dividend cover stays below 1x; the March base is retested'),
 ('Around the anchor', 'SAR 42–46', 'The status quo: the yield carries the return'),
 ('Upper band', 'SAR 46–50', 'Cover proven or rate cuts delivered; the 52-week high is pressed'),
 ('Strong upside', '> SAR 50', 'A special dividend, or the data-centre build credited with something'),
]
rows = [[f"Zone at {hz3['label']}", 'Range', 'Probability', 'What it would mean']]
for (nm, rng, mean), pz in zip(_zone_rows, zones):
    rows.append([nm, rng, f'{pz*100:.0f}%', mean])
assert abs(sum(zones) - 1) < 1e-9
table(rows, [1.5, 1.3, 1.5, 2.6], first_col_bold=True)
_near = float(sum(z for z in zones[1:4]))
P(f"The distribution leans mildly to the upside — the ladder above gives a {pr['touch_up10']*100:.0f}% chance of "
  f"tagging +10% at some point against {pr['touch_dn10']*100:.0f}% for −10% — but the mass is concentrated: "
  f"{_near*100:.0f}% of all paths finish between SAR 38 and 50, and half of them inside the much narrower "
  f"SAR {pr['band50'][0]:.1f}–{pr['band50'][1]:.1f}. That concentration is what a calm tape produces mechanically; it "
  'is not a view about the company, and a shift in the volatility regime would widen the cone at the next re-strike '
  'without anybody deciding anything.')

# ================= §7 caveats ================================================
H1('7  Caveats and what would change our mind')
for head, body in [
 ('The dividend-vs-capex tension is the model. ',
  f"The first forecast year's dividend cover of {D['cover'][-1]['cover']:.2f}\u2013{D['cover'][0]['cover']:.2f}x is "
  'an estimate built on the range of capital intensity this company\u2019s own three filed years ran, and on a '
  f"capital-intensity range and a margin path that is FLAT rather than improving — {D['drivers']['ebitda_m'][0]*100:.2f}% "
  f"in the first forecast year against {D['drivers']['ebitda_m'][-1]*100:.2f}% in the last. Two consecutive quarters of "
  'free cash flow below the quarterly dividend bill would '
  'push the DDM lens toward its bear case and the balance sheet toward releveraging — watch the quarterly FCF line, '
  'not the payout announcements.'),
 ('Terminal-value dependency. ', f"{dcf['tv_pct']*100:.0f}% of the cash-flow model's enterprise value sits beyond the "
  f"fifth forecast year, at a spread of {(coc['wacc_terminal'] - dcf['tg'])*100:.1f} points between the terminal "
  f"discount rate and the {dcf['tg']*100:.1f}% terminal growth. §1.9 is the honest statement that this valuation is "
  "substantially a judgement about the long-run price of money in Saudi Arabia. The terminal charge for keeping the "
  f"asset base whole rests on the {dcf['terminal_life_years']:.0f}-year average life the company's own accounts imply "
  "for its plant, not on a life chosen here — but a network is a bundle of assets with very different lives, and a "
  "single average is the coarsest honest way to state it."),
 ('The sovereign quote is older than the house bound. ', coc['sovereign_staleness_disclosed']),
 ('The beta is a real regression, and it explains less than a third of the variance. ',
  f"The {beta['beta']:.2f} beta is a {beta['window_years']:.1f}-year weekly regression of this stock against the "
  f"published index of the exchange it is listed on ({beta['n']} observations, standard error {beta['se']:.2f}), which "
  "is the standard this house requires and not a stopgap. What it does NOT do is explain the stock: the regression "
  f"accounts for {beta['r2']*100:.0f}% of the variance, so roughly {(1-beta['r2'])*100:.0f}% of what moves stc is "
  "specific to stc. A beta is a statement about how a stock moves with its market, and on this name that statement is "
  "weak. §1.9 shows the valuation at every beta up to 1.2 for exactly that reason."),
 ('Competition is the slow leak. ', 'stc’s consumer growth (+3%) already trails Mobily’s subscriber momentum; a price '
  'war in Saudi mobile — three players, one regulator, heavy capacity — is the scenario in which the flat margin path '
  'reverses and every lens compresses toward the normalized floor.'),
 ('The subsidiary portfolio is an investment phase, not yet a return. ', 'stc bank (8 mn customers, SAMA-licensed '
  'Jan-2025), center3, SCCC and iot squared are guided to turn contribution-positive from 2026; if they stay dilutive '
  f"through FY27, the {D['drivers']['ebitda_m'][-1]*100:.2f}% terminal-year margin this model carries is wrong by "
  'construction — and it is worth saying that this forecast assumes NO mix improvement at all, so the risk here '
  'is a margin that falls rather than one that fails to rise.'),
 ('The stake marks are point-in-time. ', 'Telefónica (9.97%) is marked at market (≈SAR 8.6 bn, ~7% below cost) and the '
  'tower stake at carrying value (SAR 4.6 bn) — the former moves daily, the latter is conservative against any '
  'transaction mark; together they are ~5% of the bridge.'),
 ('OCF conversion. ', 'Reported FY25 FCF (6.5 bn) ran well below model FCFF on receivables build and one-off cash items; '
  'we model an explicit conversion drag, but a government-receivables cycle that widens rather than narrows would make '
  f"even the {D['cover'][-1]['cover']:.2f}x heaviest-spending cover optimistic."),
 ('Technical reminder. ', 'A compressed, low-volatility tape can break either way; the narrow cone in §3 is a regime '
  'read, not a promise. The technical section is context, not a trigger.'),
]:
    bullet(body, bold_head=head)
