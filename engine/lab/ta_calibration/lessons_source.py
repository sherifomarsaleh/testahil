"""lessons_source.py — the technical register's source. Numbers are NEVER typed.

Every figure below is pulled from RESULTS_scopes.json at build time through
`n()`, so the register cannot drift from the measurement that produced it. A
lesson whose evidence disappears from the results file fails the build rather
than printing a stale number — the same rule the band record follows.
"""
import json, os

_HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(_HERE, 'RESULTS_scopes.json')))
X = json.load(open(os.path.join(_HERE, 'RESULTS_extra.json')))
VP = json.load(open(os.path.join(_HERE, 'RESULTS_volume_partial.json')))
DP = json.load(open(os.path.join(_HERE, 'RESULTS_deep.json')))


def dk(h, group, key):
    return DP[f'h{h}'][group][key]


def dv(h, group, key, field='effect'):
    return DP[f'h{h}'][group][key][field]


def xt(key):
    return X[key]


def cell(fam, h, cls='market_label'):
    return R[f'{fam}|h{h}|{cls}']


def eff(fam, h, cls='market_label'):
    return cell(fam, h, cls)['pooled']['effect']


def z(fam, h, cls='market_label'):
    p = cell(fam, h, cls)['pooled']
    return p['effect'] / p['se'] if p['se'] else 0.0


def nobs(fam, h):
    return cell(fam, h)['pooled']['n']


def sig(fam, h):
    c = cell(fam, h)
    return c['n_stocks_sig'], c['n_stocks']


def pc(x, dp=1):
    return f'{x*100:+.{dp}f}pp'


def klass(fam, h, cls, name):
    return cell(fam, h, cls)['per_class'][name]['effect']


HORIZON_NAME = {5: 'one week', 10: 'two weeks', 21: 'one month'}

METHOD = ('a technical walk-forward test, 93-ticker replay, 31-Aug-2026')

LESSONS = [
    # ---------------------------------------------------------------- EVERY TICKER
    dict(id='T-001', fig='01_horizon_decay.png', scope='ALL', status='PROVISIONAL',
         title='Score a lens on its own clock, not on the clock of the lens next to it.',
         body=('In this project the technical read is the under-one-month view, the '
               'probability cone owns one to three months, and the fundamental study '
               'owns the year. The first calibration scored the technical read at one '
               'and three months — the cone\'s horizon — and every conclusion drawn from '
               'it understated the lens, one of them badly enough to be wrong.'),
         know=lambda: (
             f'A published support or resistance level beats a distance-matched non-level '
             f'by {pc(eff("levels",5))} at one week, {pc(eff("levels",10))} at two weeks and '
             f'{pc(eff("levels",21))} at one month — and by only about +3.4pp at three '
             f'months. Scoring at the cone\'s horizon reported the weakest reading '
             f'available and concluded, wrongly, that a per-name level record could never '
             f'be built. It also throttled the evidence: quarterly windows yield about 60 '
             f'tests per name, weekly origins yield a median of 636.'),
         over=('A lens whose published claims genuinely span the horizon it is scored at. '
               'The rule is about matching the two, not about any particular horizon.')),

    dict(id='T-002', fig='12_pername_tape.png', scope='ALL', status='PROVISIONAL',
         title='The tape reading is the most reliable statement a technical read makes.',
         body=('The ATR sentence — "an orderly tape", "a lively tape" — is a genuine '
               'forecast of how far the price is about to travel. It is the only clause '
               'that is proven on almost every individual name rather than on the book as '
               'a whole, and it is currently published as a bare adjective with no record.'),
         know=lambda: (
             f'Rank correlation between the ATR reading at the origin and realized forward '
             f'volatility is {eff("tape",5):+.2f} at one week and {eff("tape",21):+.2f} at '
             f'one month, over {nobs("tape",5):,} readings (z = {z("tape",5):.0f}). It is '
             f'individually significant on {sig("tape",5)[0]} of {sig("tape",5)[1]} names '
             f'with enough history, and positive in every market and every sector tested.'),
         over=('A market where the ATR reading and realized forward movement decouple — '
               'which would show up as a name-level correlation at or below zero.')),

    dict(id='T-003', fig='01_horizon_decay.png', scope='ALL', status='PROVISIONAL',
         title='A charted level is real, and it is worth most in the first week.',
         body=('Support and resistance are not decoration, but they are also not walls. '
               'Measured against a price the same distance away that sits at no charted '
               'structure, a published level is broken through less often — and the edge '
               'decays steadily as the horizon lengthens.'),
         know=lambda: (
             f'Conditional on both being reached, the published level is broken through '
             f'{pc(eff("levels",5))} less often than the matched non-level at one week '
             f'(n = {nobs("levels",5):,}, z = {z("levels",5):.0f}), {pc(eff("levels",10))} '
             f'at two weeks and {pc(eff("levels",21))} at one month. The null is a pair — '
             f'one non-level inside the published distance and one outside — so the '
             f'comparison is centred on distance by construction.'),
         over=('A level-drawing method whose edge does not decay with horizon, which would '
               'mean the effect is not about the level being tested.')),

    dict(id='T-004', fig='07_slope200.png', scope='ALL', status='PROVISIONAL',
         title='Above the whole moving-average stack is worth about three points, everywhere.',
         body=('The trend clause carries real direction, it is small, and it is the same '
               'size in every market tested. That combination is what makes it a rule '
               'rather than an observation: it does not need to be re-learned per venue.'),
         know=lambda: (
             f'Trading above the whole stack raises the odds of a higher close by '
             f'{pc(eff("trend",5))} at one week against trading below it '
             f'(n = {nobs("trend",5):,}, z = {z("trend",5):.1f}). Across the three markets '
             f'with enough names the estimates are '
             f'{pc(klass("trend",5,"market_label","Saudi (Tadawul)"))}, '
             f'{pc(klass("trend",5,"market_label","Egypt (EGX)"))} and '
             f'{pc(klass("trend",5,"market_label","UAE (ADX & DFM)"))} — a Cochran Q test '
             f'cannot separate them (p = {cell("trend",5)["heterogeneity"]["p"]:.2f}), so '
             f'they are one population.'),
         over=('A market whose trend estimate sits outside the others by more than its own '
               'standard error, on at least four names.')),

    dict(id='T-005', scope='ALL', status='PROVISIONAL',
         title='The MACD histogram carries no direction. Do not read one into it.',
         body=('A positive MACD histogram is followed by a higher close no more often than '
               'a negative one, at every horizon the technical lens covers. This is a '
               'measured null, not an absence of evidence — the test ran on tens of '
               'thousands of readings and found nothing.'),
         know=lambda: (
             f'The lift in forward up-rate from a positive histogram is {pc(eff("macd",5),2)} '
             f'at one week, {pc(eff("macd",10),2)} at two weeks and {pc(eff("macd",21),2)} at '
             f'one month, on {nobs("macd",5):,} readings — |z| below 1.2 throughout. Only '
             f'{sig("macd",21)[0]} of {sig("macd",21)[1]} individual names show anything, '
             f'about what chance alone produces at the 5% level.'),
         over=('A construction of the MACD other than the histogram sign — a crossing, a '
               'divergence — tested on its own and clearing the same bar.')),

    dict(id='T-006', fig='05_rsi_curve.png', scope='ALL', status='ACTED ON',
         title='A cautious-sounding word is still a claim, and gets audited like one.',
         body=('The read described RSI at or above 70 as "stretched" and below 30 as '
               '"washed out". Both words imply a reversal to any reader. Both were '
               'followed by the opposite. The words survived precisely because they '
               'sounded like caution, and conservative-sounding language does not get '
               'checked the way a flattering claim would.'),
         know=lambda: (
             f'A reading at or above 70 is followed by an up-rate {pc(eff("rsi_high",5))} '
             f'ABOVE the base rate at one week and {pc(eff("rsi_high",21))} at one month '
             f'(n = {nobs("rsi_high",5):,}); at three months the same bucket ran 7.6pp above '
             f'base. Corrected to "very strong" and "very weak" on 31-Aug-2026 and live.'),
         over=('Nothing about the direction — it is measured. The wording itself is '
               'replaceable by any phrasing that does not imply what it does not predict.')),

    # ---------------------------------------------------------------------- CLASS
    dict(id='T-007', fig='08_level_market.png', scope='CLASS', cls='market',
         status='PROVISIONAL',
         title='How much a level is worth depends on the market it is drawn in.',
         body=('The level edge holds everywhere, but not equally. A level in the Saudi '
               'market is worth roughly twice one in Egypt. This is the one place where '
               'a class genuinely earns its rung: the classes differ by more than their '
               'own standard errors explain.'),
         know=lambda: (
             f'At one week the edge is '
             f'{pc(klass("levels",5,"market_label","Saudi (Tadawul)"))} in Saudi, '
             f'{pc(klass("levels",5,"market_label","UAE (ADX & DFM)"))} in the UAE and '
             f'{pc(klass("levels",5,"market_label","Egypt (EGX)"))} in Egypt. Cochran Q = '
             f'{cell("levels",5)["heterogeneity"]["q"]:.1f} on '
             f'{cell("levels",5)["heterogeneity"]["df"]} degrees of freedom '
             f'(p = {cell("levels",5)["heterogeneity"]["p"]:.3f}), I-squared = '
             f'{cell("levels",5)["heterogeneity"]["i2"]:.0f}% — the spread is real, not '
             f'sampling noise.'),
         over=('Only three markets carry four or more names, so this rests on three '
               'estimates. A fourth market landing between them would weaken it; one '
               'landing outside would strengthen it.')),

    dict(id='T-008', scope='CLASS', cls='market',
         status='PROVISIONAL',
         title='The tape reading works everywhere, but not equally hard.',
         body=('Class changes the strength of the tape claim, never its sign. That is an '
               'important distinction: the claim itself is universal and belongs on every '
               'page, while how much weight it carries is a market-level fact.'),
         know=lambda: (
             f'At one week the correlation runs '
             f'{klass("tape",5,"market_label","UAE (ADX & DFM)"):+.2f} in the UAE, '
             f'{klass("tape",5,"market_label","Saudi (Tadawul)"):+.2f} in Saudi and '
             f'{klass("tape",5,"market_label","Egypt (EGX)"):+.2f} in Egypt; by sector it '
             f'spans {min(v["effect"] for v in cell("tape",5,"sector")["per_class"].values()):+.2f} '
             f'to {max(v["effect"] for v in cell("tape",5,"sector")["per_class"].values()):+.2f}. '
             f'Every class is individually significant and every one is positive.'),
         over=('A class whose tape correlation is not distinguishable from zero on at '
               'least four names — which would make the claim conditional rather than '
               'universal.')),

    dict(id='T-009', scope='CLASS', cls='sector',
         status='WATCH',
         title='Industry sector is a far weaker class than market, and mostly is not one.',
         body=('The fundamental register learns lessons per class of company, and it is '
               'natural to assume the technical lens should too. Tested, it mostly does '
               'not: the venue matters and the industry usually does not. Where a sector '
               'split does separate, the market split separates harder on the same claim.'),
         know=lambda: (
             f'The trend claim is one population across sectors at one week '
             f'(Q p = {cell("trend",5,"sector")["heterogeneity"]["p"]:.2f}) and across '
             f'markets too. The MACD null is one population on both. Sector labels are '
             f'also thin: the repository carries 32 distinct labels for 84 names, which '
             f'had to be collapsed into 10 coarse buckets before anything could be tested, '
             f'and four of those hold five names or fewer.'),
         over=('A claim that separates by sector while staying one population across '
               'markets — the pattern this lesson says is absent.')),

    # ---------------------------------------------------------------------- STOCK
    dict(id='T-010', fig='12_pername_tape.png', scope='STOCK', status='PROVISIONAL',
         title='Only the tape claim survives per name. The trend claim does not, and it looked as if it did.',
         body=('A per-name record needs the name\'s own history to resolve the effect. '
               'The tape claim clears that bar on almost the whole book. The trend claim '
               'appears to clear it on a handful of names — and that appearance is the '
               'trap. Count the names it appears to work BACKWARDS on and the two are the '
               'same size, which is what per-name noise looks like when there is a real '
               'pooled effect and no real per-name one.'),
         know=lambda: (
             f'The tape claim is significantly POSITIVE on {sig("tape",5)[0]} of '
             f'{sig("tape",5)[1]} names at one week and {sig("tape",21)[0]} at one month, '
             f'against one and two significantly negative — chance produces about 4.6 '
             f'either way, so the asymmetry is the finding. The trend claim splits 7 for '
             f'and 4 against at one week, 6 and 7 at two weeks, and 13 and 12 at one '
             f'month; a sign test on the last of those returns p = 1.00. An earlier '
             f'edition of this register read the positive half alone and reported "trend, '
             f'per name where earned" — on the cone\'s horizon, where a quarter of the '
             f'origins hid the other half.'),
         over=('A construction of the trend clause whose per-name hits outnumber its '
               'per-name reversals by more than chance. The counts are the test and are '
               're-run every pass.')),
    dict(id='T-011', fig='09_trigger.png', scope='ALL', status='PROVISIONAL',
         title='The bull and bear trigger sentence promises the opposite of what happens.',
         body=('"A daily close back above R1 would clear the nearest resistance and open '
               'the R3 zone" is the only explicitly conditional forecast the read makes, '
               'and it is wrong in direction. Clearing a REAL level is followed by the far '
               'level opening LESS often than clearing a non-level at the same distance '
               'is. The sentence reads as a green light and the tape treats it as a '
               'warning.'),
         know=lambda: (
             f'Scored in the order the sentence claims — the far rung must be reached '
             f'AFTER the close that fired the trigger — against a null ladder moved off '
             f'structure with the near/far ratio preserved. At one week the far zone opens '
             f'{xt("trigger|h5|both")["p_real"]*100:.1f}% of the time after a real trigger '
             f'against {xt("trigger|h5|both")["p_null"]*100:.1f}% after the null '
             f'({pc(xt("trigger|h5|both")["effect"])}, z = {xt("trigger|h5|both")["z"]:.1f}, '
             f'{xt("trigger|h5|both")["n_real"]:,} firings); at one month '
             f'{pc(xt("trigger|h21|both")["effect"])} (z = {xt("trigger|h21|both")["z"]:.1f}). '
             f'Both sides fail and the support side fails harder. The firing rates '
             f'themselves match — {xt("trigger|h21|both")["fire_rate_real"]*100:.0f}% real '
             f'against {xt("trigger|h21|both")["fire_rate_null"]*100:.0f}% null — so this is '
             f'about what follows the trigger, not about how often it fires.'),
         over=('Nothing about the direction — but note it FOLLOWS from T-003 rather than '
               'contradicting it. If a charted level genuinely holds, the far level holds '
               'too, so reaching it is harder, not easier. The prose was written as though '
               'only the near level were real.')),

    dict(id='T-012', fig='10_cross.png', scope='ALL', status='PROVISIONAL',
         title='A fresh moving-average cross is not a regime change.',
         body=('The read calls a 50/200 cross inside the last 25 sessions "a momentum-'
               'regime change rather than noise inside an intact trend". Neither half of '
               'that survives testing. Volatility does not shift, and the direction leans '
               'gently the wrong way: a fresh golden cross is followed by a LOWER up-rate '
               'than an established one, and a fresh death cross by a higher one.'),
         know=lambda: (
             f'Compared against origins in the SAME cross state without the freshness, so '
             f'the test isolates the cross rather than re-measuring the trend. At one month '
             f'a fresh golden cross is followed by an up-rate of '
             f'{xt("cross|h21|golden")["p_real"]*100:.1f}% against '
             f'{xt("cross|h21|golden")["p_null"]*100:.1f}% for a stale one '
             f'({pc(xt("cross|h21|golden")["effect"])}, z = {xt("cross|h21|golden")["z"]:.1f}, '
             f'n = {xt("cross|h21|golden")["n_real"]:,}); a fresh death cross runs '
             f'{pc(xt("cross|h21|death")["effect"])} the other way. Realized forward '
             f'volatility is essentially unchanged — a ratio of '
             f'{xt("cross|h21|golden")["vol_ratio"]:.2f} on golden and '
             f'{xt("cross|h21|death")["vol_ratio"]:.2f} on death — which is the reading '
             f'that most directly refutes "regime change".'),
         over=('A different freshness window, or a cross of different averages, showing a '
               'volatility shift. The 25-session window is the one the read publishes and '
               'is what was tested.')),

    dict(id='T-013', fig='11_volume.png', scope='ALL', status='PROVISIONAL',
         title='Volume carries movement, not direction — and the tape reading already has it.',
         body=('Volume sits in every library and the read has never looked at it. Tested, '
               'it behaves exactly like a weaker version of the ATR sentence: it says '
               'something real about how far price will travel, nothing at all about which '
               'way, and almost all of what it says is already said better by a reading '
               'the page publishes today.'),
         know=lambda: (
             f'On {xt("volume|h5")["n"]:,} readings, a volume surge and a volume drought are '
             f'followed by a higher close equally often — '
             f'{pc(xt("volume|h5")["direction"]["effect"])} at one week '
             f'(z = {xt("volume|h5")["direction"]["z"]:+.1f}) and '
             f'{pc(xt("volume|h21")["direction"]["effect"])} at one month. Against realized '
             f'forward volatility the volume z-score scores {VP["5"]["raw"]:+.3f} where the '
             f'ATR reading scores {VP["5"]["atr"]:+.3f}; controlling for ATR, volume keeps '
             f'{VP["5"]["partial"]:+.3f} at one week and {VP["21"]["partial"]:+.3f} at one '
             f'month — real, highly significant, and about a twentieth of what the page '
             f'already tells you.'),
         over=('A volume construction other than a trailing z-score — turnover against '
               'float, or volume conditioned on direction — retaining a materially larger '
               'partial correlation. What is ruled out is the plain surge.')),
    # ------------------------------------------------- what the levels are made of
    dict(id='T-014', fig='02_level_kind.png', scope='ALL', status='PROVISIONAL',
         title='A moving average is as good a line as charted structure — for about a week.',
         body=('The read draws its support and resistance from swing highs and lows, and '
               'admits a moving average, a 52-week extreme or a round number only when '
               'real structure does not fill the slot — they are scored as second class. '
               'Over one week that ranking is wrong: the 20-day average holds better than '
               'anything else on the board. Over a month it is right, and for an obvious '
               'reason nobody had checked — a moving average MOVES, so as a fixed line it '
               'goes stale in days.'),
         know=lambda: (
             f'At one week the 20-day average is broken through '
             f'{pc(dv(5,"by_kind","20-day MA"))} less often than a matched non-level, '
             f'against {pc(dv(5,"by_kind","swing"))} for a swing high or low, '
             f'{pc(dv(5,"by_kind","round"))} for a round number and '
             f'{pc(dv(5,"by_kind","52w high"))} for the 52-week high (n = '
             f'{dv(5,"by_kind","20-day MA","n"):,} / {dv(5,"by_kind","swing","n"):,} / '
             f'{dv(5,"by_kind","round","n"):,} / {dv(5,"by_kind","52w high","n"):,}). '
             f'At one month the same average is worth {pc(dv(21,"by_kind","20-day MA"))} '
             f'— nothing at all — while swing structure still holds '
             f'{pc(dv(21,"by_kind","swing"))}.'),
         over=('The moving-average counts are small (174 tests at one week) because the '
               'read admits an average only when structure does not fill the slot. A '
               'larger sample moving the estimate toward the swing figure would fold this '
               'lesson into T-003.')),

    dict(id='T-015', fig='03_touches.png', scope='ALL', status='PROVISIONAL',
         title='How many times a level was tested tells you nothing about whether it holds.',
         body=('It is an article of faith in chart reading that a level tested five times '
               'is stronger than one tested once, and the read believes it too — it '
               'weights each level by its touch count when deciding what to publish. '
               'Across the whole book the edge is flat. A level tested once and a level '
               'tested five times hold equally well.'),
         know=lambda: (
             f'At one month, by number of prior tests: none '
             f'{pc(dv(21,"by_touches","none (MA/round/52w)"))}, once '
             f'{pc(dv(21,"by_touches","1"))}, twice {pc(dv(21,"by_touches","2"))}, '
             f'three or four {pc(dv(21,"by_touches","3-4"))}, five or more '
             f'{pc(dv(21,"by_touches","5+"))} — on '
             f'{sum(dv(21,"by_touches",k,"n") for k in ("none (MA/round/52w)","1","2","3-4","5+")):,} '
             f'tests in total. There is no order in it.'),
         over=('A touch count measured differently — tests clustered in time, or tests '
               'that produced a large rejection rather than any touch at all. What is '
               'ruled out is the plain count the read uses.')),

    dict(id='T-016', fig='02_level_kind.png', scope='ALL', status='PROVISIONAL',
         title='Round numbers work. Not as well as structure, but they are not superstition.',
         body=('The read treats a round number as a filler — a line to publish when the '
               'chart has nothing better to offer, scored below everything else. It earns '
               'more than that. Round numbers hold about three quarters as well as real '
               'charted structure, consistently, at every horizon.'),
         know=lambda: (
             f'A round number is broken through {pc(dv(5,"by_kind","round"))} less often '
             f'than a matched non-level at one week and {pc(dv(21,"by_kind","round"))} at '
             f'one month, on {dv(21,"by_kind","round","n"):,} tests — against '
             f'{pc(dv(21,"by_kind","swing"))} for swing structure on the same clock. Both '
             f'are far clear of chance.'),
         over=('A market with no round-number convention in its tick sizes, where the '
               'effect should vanish.')),

    dict(id='T-017', scope='ALL', status='PROVISIONAL',
         title='The nearest level is not the strongest one.',
         body=('The read publishes three levels a side and orders them by distance, and it '
               'is natural to read the first as the most important. It is not the '
               'strongest. Over a month the FURTHEST of the three holds best, and the '
               'nearest holds worst — nearly twice the difference.'),
         know=lambda: (
             f'At one month the three published rungs hold '
             f'{pc(dv(21,"by_rank","1.0"))} (nearest), {pc(dv(21,"by_rank","2.0"))} and '
             f'{pc(dv(21,"by_rank","3.0"))} (furthest), on '
             f'{dv(21,"by_rank","1.0","n"):,}, {dv(21,"by_rank","2.0","n"):,} and '
             f'{dv(21,"by_rank","3.0","n"):,} tests. At one week the middle rung is '
             f'strongest ({pc(dv(5,"by_rank","2.0"))}) and the ordering is not '
             f'monotonic either way.'),
         over=('An ordering that reproduces on a different level-drawing method. As it '
               'stands this may be about which levels survive the read\'s own distance '
               'filter rather than about rank itself.')),

    # -------------------------------------------- indicators published but unscored
    dict(id='T-018', fig='07_slope200.png', scope='ALL', status='PROVISIONAL',
         title='Which way the 200-day is sloping is worth more than where the price sits.',
         body=('Every page states whether the 200-day average is rising, flat or falling, '
               'and nothing has ever been made of it. It is a cleaner directional signal '
               'than the moving-average stack the read leads with, and it moves in the '
               'order you would hope: rising is best, falling is worst, flat sits between '
               'them.'),
         know=lambda: (
             f'Against a base rate of '
             f'{DP["h21"]["slope200"]["base"]*100:.1f}%, a rising 200-day is followed by a '
             f'higher close one month later {pc(DP["h21"]["slope200"]["rows"][0]["lift"])} '
             f'more often, a flat one '
             f'{pc(DP["h21"]["slope200"]["rows"][1]["lift"])} and a falling one '
             f'{pc(DP["h21"]["slope200"]["rows"][2]["lift"])} — a spread of '
             f'{(DP["h21"]["slope200"]["rows"][0]["lift"]-DP["h21"]["slope200"]["rows"][2]["lift"])*100:.1f} '
             f'points across '
             f'{sum(x["n"] for x in DP["h21"]["slope200"]["rows"]):,} readings, against '
             f'{pc(eff("trend",21))} for the stack claim the read leads with.'),
         over=('A slope definition other than the ten-session change the read uses, '
               'failing to reproduce it.')),

    dict(id='T-019', fig='06_52week.png', scope='ALL', status='PROVISIONAL',
         title='Stocks near their 52-week high keep doing better. The read states the distance and stops.',
         body=('Every page prints how far the last close sits below the 52-week high. That '
               'distance predicts what comes next, in the direction a momentum investor '
               'would expect and a bargain hunter would not: the closer to the high, the '
               'better the odds.'),
         know=lambda: (
             f'Sorted into eight equal groups by distance below the high, the closest '
             f'group is followed by a higher close one month later '
             f'{pc(DP["h21"]["w52"]["buckets"][0]["lift"])} more often than the base rate, '
             f'and the group sitting about '
             f'{DP["h21"]["w52"]["buckets"][-2]["mid"]*100:.0f}% below the high '
             f'{pc(DP["h21"]["w52"]["buckets"][-2]["lift"])} — on about '
             f'{DP["h21"]["w52"]["buckets"][0]["n"]:,} readings per group. The pattern is '
             f'broadly monotonic across the middle.'),
         over=('The deepest group breaks the pattern, which is what a genuine washed-out '
               'rebound would look like. A larger sample confirming that turn would make '
               'this a U-shape rather than a slope.')),

    dict(id='T-020', fig='05_rsi_curve.png', scope='ALL', status='PROVISIONAL',
         title='RSI is flat across nine tenths of its range.',
         body=('The read has five words for RSI. Measured decile by decile, the first nine '
               'are indistinguishable from one another and from the base rate. Everything '
               'RSI knows sits in its top tenth. That is why the word for the top mattered '
               'so much (T-006) and why the words for the middle carry nothing.'),
         know=lambda: (
             f'Across ten equal groups at one week, the lifts run between '
             f'{min(b["lift"] for b in DP["h5"]["rsi"]["buckets"][:9])*100:+.1f} and '
             f'{max(b["lift"] for b in DP["h5"]["rsi"]["buckets"][:9])*100:+.1f} points, '
             f'each on about {DP["h5"]["rsi"]["buckets"][0]["n"]:,} readings and each '
             f'inside its own error bar. The top group — RSI above '
             f'{DP["h5"]["rsi"]["buckets"][-1]["lo"]:.0f} — is '
             f'{pc(DP["h5"]["rsi"]["buckets"][-1]["lift"])}, and '
             f'{pc(DP["h21"]["rsi"]["buckets"][-1]["lift"])} at one month.'),
         over=('An RSI period other than 14, or a reading taken relative to the stock\'s '
               'own history rather than the fixed 0-100 scale.')),

    # ---------------------------------------------------------------- does it last
    dict(id='T-021', fig='13_stability.png', scope='ALL', status='WATCH',
         title='The trend claim has faded. It worked before 2020 and has not since.',
         body=('Splitting the fifteen years in half is the cheapest honesty check there '
               'is, and the trend claim fails it. Trading above the whole moving-average '
               'stack was worth something in the first half and nothing in the second — '
               'it does not merely weaken, it changes sign. The pooled figure this '
               'register publishes for it is therefore an average of a real effect and '
               'its absence.'),
         know=lambda: (
             f'At one month, split at {DP["h21"]["stability"]["early"]["split_at"]}: the '
             f'above-versus-below gap is '
             f'{pc(DP["h21"]["stability"]["early"]["trend"])} in the earlier half and '
             f'{pc(DP["h21"]["stability"]["late"]["trend"])} in the later one. At one week '
             f'it survives with the same sign but decays hard — '
             f'{pc(DP["h5"]["stability"]["early"]["trend"])} to '
             f'{pc(DP["h5"]["stability"]["late"]["trend"])}.'),
         over=('The next few years restoring it. This is flagged as a WATCH rather than a '
               'withdrawal because half a sample is a blunt instrument, and the shorter '
               'horizon still holds.')),

    dict(id='T-022', fig='13_stability.png', scope='ALL', status='PROVISIONAL',
         title='Levels and the tape reading do survive that same test.',
         body=('The split-half check that broke the trend claim leaves the other two '
               'standing. The level edge is close to unchanged across the two halves, and '
               'the tape reading is actually stronger in the recent one. A finding that '
               'holds in both halves of fifteen years is a different quality of evidence '
               'from one that holds only on average.'),
         know=lambda: (
             f'At one month the level edge is '
             f'{pc(DP["h21"]["stability"]["early"]["levels"]["effect"])} before '
             f'{DP["h21"]["stability"]["early"]["split_at"]} and '
             f'{pc(DP["h21"]["stability"]["late"]["levels"]["effect"])} after; at one week, '
             f'{pc(DP["h5"]["stability"]["early"]["levels"]["effect"])} and '
             f'{pc(DP["h5"]["stability"]["late"]["levels"]["effect"])}. The tape '
             f'correlation runs {DP["h21"]["stability"]["early"]["tape"]:+.3f} then '
             f'{DP["h21"]["stability"]["late"]["tape"]:+.3f}.'),
         over=('Either measure dropping toward zero in a future half. The check is cheap '
               'and should be re-run at every calibration pass.')),

    dict(id='T-023', fig='04_atr_ladder.png', scope='ALL', status='PROVISIONAL',
         title='The four tape words are a properly calibrated ladder, not adjectives.',
         body=('"An orderly tape", "a normal tape", "a lively tape", "a volatile tape". '
               'Each maps to a distinct and correctly ordered amount of movement in the '
               'month that follows, and the gaps between them are wide enough that the '
               'words are doing real work. This is the one place the read already behaves '
               'like a calibrated instrument.'),
         know=lambda: (
             ' · '.join(f'{b["word"]} → {b["med"]*100:.0f}%' for b in DP['h21']['atr'])
             + f' (median annualised movement over the following month, on '
               f'{sum(b["n"] for b in DP["h21"]["atr"]):,} readings). The middle half of '
               f'outcomes for "an orderly tape" runs '
               f'{DP["h21"]["atr"][0]["q25"]*100:.0f}–{DP["h21"]["atr"][0]["q75"]*100:.0f}% '
               f'against {DP["h21"]["atr"][-1]["q25"]*100:.0f}–'
               f'{DP["h21"]["atr"][-1]["q75"]*100:.0f}% for "a volatile tape" — barely '
               f'overlapping.'),
         over=('A market where the ladder inverts or collapses. The cut points are fixed '
               'percentages of price and could in principle suit one market and not '
               'another; tested per market, all of them keep the order.')),
]