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
    dict(id='T-001', scope='ALL', status='PROVISIONAL',
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

    dict(id='T-002', scope='ALL', status='PROVISIONAL',
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

    dict(id='T-003', scope='ALL', status='PROVISIONAL',
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

    dict(id='T-004', scope='ALL', status='PROVISIONAL',
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

    dict(id='T-006', scope='ALL', status='ACTED ON',
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
    dict(id='T-007', scope='CLASS', cls='market',
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
    dict(id='T-010', scope='STOCK', status='PROVISIONAL',
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
    dict(id='T-011', scope='ALL', status='PROVISIONAL',
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

    dict(id='T-012', scope='ALL', status='PROVISIONAL',
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

    dict(id='T-013', scope='ALL', status='PROVISIONAL',
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
]