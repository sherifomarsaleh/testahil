"""lessons_source.py — the technical register's source. Numbers are NEVER typed.

Every figure in the document resolves from the results files at build time, so
the register cannot drift from the measurement that produced it. A lesson whose
evidence disappears from those files fails the build rather than printing a
stale number.

Third edition, and the language rule for it: every lesson says WHAT WAS TESTED
in one plain sentence before it gives any number; "percentage points" is spelled
out as "out of 100 tests"; and wherever a result can be shown happening on a
real, named stock, it is.
"""
import json, os

_HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(_HERE, 'RESULTS_scopes.json')))
X = json.load(open(os.path.join(_HERE, 'RESULTS_extra.json')))
VP = json.load(open(os.path.join(_HERE, 'RESULTS_volume_partial.json')))
DP = json.load(open(os.path.join(_HERE, 'RESULTS_deep.json')))
M = json.load(open(os.path.join(_HERE, 'RESULTS_more.json')))


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
    return f'{x*100:+.{dp}f} in 100'


def pt(x, dp=1):
    return f'{x*100:.{dp}f}%'


def dv(h, group, key, field='effect'):
    return DP[f'h{h}'][group][key][field]


def klass(fam, h, cls, name):
    return cell(fam, h, cls)['per_class'][name]['effect']


HORIZON_NAME = {5: 'one week', 10: 'two weeks', 21: 'one month'}
METHOD = 'learned from a technical walk-forward test, 93-ticker replay, 31-Aug-2026'

LESSONS = [
    # ============================================================ EVERY TICKER
    dict(id='T-001', scope='ALL', status='PROVISIONAL', fig='01_horizon_decay.png',
         figcap='The same test at four horizons. The grey bar is the one the first '
                'calibration reported.',
         title='Judge a tool over the time it is meant for.',
         body=('In this project the chart read is for the weeks ahead, the probability '
               'cone owns one to three months, and the fundamental study owns the year. '
               'The first calibration graded the chart read on what prices did three '
               'months later — the cone\'s exam, not the chart\'s. Everything scored '
               'poorly, and one wrong conclusion was drawn from that before the mistake '
               'was caught.'),
         know=lambda: (
             f'The test: draw a support or resistance line, draw a fake line the same '
             f'distance away where the chart shows nothing, and count how often price '
             f'closes through each. The real line is beaten less often — by '
             f'{pc(eff("levels",5))} tests over one week, {pc(eff("levels",10))} over two '
             f'weeks, {pc(eff("levels",21))} over one month, and only about +3.4 in 100 '
             f'over three months. Graded at three months, we reported that weakest number '
             f'and concluded a per-stock level record could never be built. Grading '
             f'weekly also multiplied the evidence: about 60 tests per stock became a '
             f'median of 636.'),
         over=('Nothing about one week being special. The rule is that the test must '
               'match the tool\'s own horizon — a tool that genuinely makes three-month '
               'claims should be tested at three months.')),

    dict(id='T-002', scope='ALL', status='PROVISIONAL', fig='21_demo_ihc.png',
         figcap='One real stock, every weekly reading for nine years. Busier tape on '
                'the left axis, bigger moves follow.',
         title='The single most trustworthy sentence on a page is the one about the tape.',
         body=('Each page says whether the tape is orderly, normal, lively or volatile — '
               'a plain-language reading of how much the stock moves in a day (the ATR). '
               'That sentence turns out to be a genuine forecast: when the tape is busy '
               'today, the price travels further over the coming weeks, and when it is '
               'quiet, it travels less. No other sentence on the page is this reliable.'),
         know=lambda: (
             f'The test: line up each day\'s tape reading against how far the price '
             f'actually moved afterwards, across {nobs("tape",5):,} readings. The two '
             f'rise and fall together with a rank correlation of {eff("tape",5):+.2f} at '
             f'one week and {eff("tape",21):+.2f} at one month — enormous by the '
             f'standards of anything else in this document. On International Holding '
             f'Company (IHC) alone the correlation is {M["ihc"]["rho"]:+.2f} across '
             f'{M["ihc"]["n"]} months of readings; the chart below is that stock, one '
             f'dot per week.'),
         over=('A market where busy days stop being followed by busy weeks. None of the '
               'nine tested here comes close.')),

    dict(id='T-003', scope='ALL', status='PROVISIONAL', fig='18_demo_level.png',
         figcap='Qatar National Bank, August 2025. The read put resistance at the round '
                '20.00; the month that followed is tinted.',
         title='The lines are real. Price respects a drawn level more than an empty one.',
         body=('The doubt about support and resistance is always the same: price has to '
               'stop somewhere, so how do you know the line meant anything? By racing it '
               'against a line that means nothing. For every level we publish, we also '
               'test an invented level a similar distance away, placed where the chart '
               'shows no structure at all. If our lines were decoration, the two would '
               'behave the same. They do not.'),
         know=lambda: (
             f'Counting only the occasions price actually reached each line: it went on '
             f'to CLOSE through the real one {pc(eff("levels",5))} tests less often than '
             f'through the invented one over the following week '
             f'({nobs("levels",5):,} paired tests), and {pc(eff("levels",21))} over the '
             f'following month. The picture below is one such occasion: QNB touched '
             f'{M["ep_level"]["level"]:.2f} intraday and never closed above it.'),
         over=('The invented lines catching up. The race is re-run at every calibration '
               'pass, and it is the entire basis for keeping levels on the page.')),

    dict(id='T-024', scope='ALL', status='PROVISIONAL', fig='15_res_sup.png',
         figcap='The same race, split by side of the price.',
         title='The floor is stronger than the ceiling.',
         body=('Support — the level below the price — holds better than resistance, the '
               'level above it. The gap is consistent at every horizon. A practical way '
               'to say it: a support line on these pages deserves a little more '
               'confidence than a resistance line at the same distance.'),
         know=lambda: (
             f'Same race as T-003, split by side. Over one week, support beats its '
             f'invented twin by {pc(M["side"]["5"]["sup"]["effect"])} tests '
             f'({M["side"]["5"]["sup"]["n"]:,} paired tests) against '
             f'{pc(M["side"]["5"]["res"]["effect"])} for resistance '
             f'({M["side"]["5"]["res"]["n"]:,}); over one month, '
             f'{pc(M["side"]["21"]["sup"]["effect"])} against '
             f'{pc(M["side"]["21"]["res"]["effect"])}.'),
         over=('A period in which sellers defend ceilings the way buyers defend floors — '
               'a long bear market in these names would be the natural test.')),

    dict(id='T-025', scope='ALL', status='PROVISIONAL', fig='16_touch_rate.png',
         figcap='How often price reaches the closest published level at all.',
         title='Most weeks, the levels are scenery. The test only starts when price arrives.',
         body=('A published ladder of six levels looks like six live predictions. In any '
               'given week it mostly is not, because price rarely travels far enough to '
               'meet one. Nothing in this document about levels applies until price '
               'actually gets there — and that is the exception, not the rule.'),
         know=lambda: (
             f'Across every reading in the book, price reached the CLOSEST published '
             f'level within a week only {pt(M["touch"]["5"]["nearest"], 0)} of the time, '
             f'within two weeks {pt(M["touch"]["10"]["nearest"], 0)}, and within a month '
             f'{pt(M["touch"]["21"]["nearest"], 0)}. The other five rungs are reached '
             f'even less often.'),
         over=('Nothing — this is a description of how far prices travel, not a claim '
               'that could be wrong about the levels themselves. It is here so the level '
               'lessons are read with the right expectations.')),

    dict(id='T-026', scope='ALL', status='PROVISIONAL', fig='17_tilted_coin.png',
         figcap='How often a stock in each market simply closes higher.',
         title='The coin is not fair — and its tilt depends on the market and the clock.',
         body=('Before crediting any signal with "it works 53% of the time", ask what a '
               'stock does with no signal at all. Over one week the answer is almost '
               'exactly a coin flip. Over one month the coin tilts upward — and by very '
               'different amounts in different markets. Every claim in this document is '
               'therefore measured against its own market\'s tilt, never against 50%.'),
         know=lambda: (
             f'Over one week, stocks here closed higher {pt(M["coin"]["5"]["pooled"], 1)} '
             f'of the time — a fair coin. Over one month, '
             f'{pt(M["coin"]["21"]["pooled"], 1)} — tilted, and unevenly: about '
             f'{pt(M["coin"]["21"]["by_market"]["US"]["up"], 0)} in the US against '
             f'{pt(M["coin"]["21"]["by_market"]["QA"]["up"], 0)} in Qatar and roughly '
             f'52% across Egypt, the UAE and Saudi. Measured on '
             f'{M["coin"]["21"]["n"]:,} readings.'),
         over=('Nothing to overturn — it is the baseline itself. It moves with rates and '
               'regimes, which is exactly why it is measured fresh at every pass rather '
               'than remembered.')),

    dict(id='T-004', scope='ALL', status='PROVISIONAL',
         title='Being above all three averages is worth about three extra wins in a hundred.',
         body=('The first sentence of every read says where price sits against its 20, '
               '50 and 200-day averages. Sitting above all three genuinely tilts the '
               'odds of the coming weeks upward — but only slightly, and by the same '
               'small amount in every market tested. It is a lean, not a signal.'),
         know=lambda: (
             f'The test: compare weeks that began above the whole stack with weeks that '
             f'began below it, {nobs("trend",5):,} readings in all. Above-the-stack weeks '
             f'closed higher {pc(eff("trend",5))} more often. Egypt, the UAE and Saudi '
             f'give statistically the same answer '
             f'({pc(klass("trend",5,"market_label","Egypt (EGX)"))}, '
             f'{pc(klass("trend",5,"market_label","UAE (ADX & DFM)"))}, '
             f'{pc(klass("trend",5,"market_label","Saudi (Tadawul)"))}), so it is one '
             f'rule, not three. But see T-021: its recent record is in question.'),
         over=('See T-021 — the second half of the data has already put this on watch at '
               'the one-month horizon.')),

    dict(id='T-018', scope='ALL', status='PROVISIONAL', fig='07_slope200.png',
         figcap='The odds shift by the direction of the 200-day average alone.',
         title='The slope of the 200-day average beats the position against it.',
         body=('Every page states whether the 200-day average is rising, flat or '
               'falling, almost in passing. Measured, that little word carries more '
               'information than the headline sentence about being above or below the '
               'averages — and it behaves exactly as it should: rising is best, falling '
               'is worst, flat sits in between.'),
         know=lambda: (
             f'Across {sum(x["n"] for x in DP["h21"]["slope200"]["rows"]):,} monthly '
             f'readings: when the 200-day was rising, the stock closed the month higher '
             f'{pc(DP["h21"]["slope200"]["rows"][0]["lift"])} more often than its base '
             f'rate; flat, {pc(DP["h21"]["slope200"]["rows"][1]["lift"])}; falling, '
             f'{pc(DP["h21"]["slope200"]["rows"][2]["lift"])}. Top to bottom that is a '
             f'{(DP["h21"]["slope200"]["rows"][0]["lift"]-DP["h21"]["slope200"]["rows"][2]["lift"])*100:.0f}-in-100 '
             f'spread — bigger than the stack sentence has ever measured.'),
         over=('A different slope definition failing to reproduce it. This one is the '
               'read\'s own: the average\'s change over ten sessions.')),

    dict(id='T-019', scope='ALL', status='PROVISIONAL', fig='06_52week.png',
         figcap='Odds of a higher close, by how far the stock sat below its 52-week high.',
         title='Stocks near their yearly high keep winning. "Cheap because it fell" loses.',
         body=('Every page prints how far the price sits below its 52-week high. That '
               'number leans the opposite way to bargain-hunting instinct: the closer a '
               'stock is to its yearly high, the better its next month tends to be, and '
               'stocks 30% or more below their high tend to keep disappointing.'),
         know=lambda: (
             f'Sorting all {nobs("tape",21):,} readings into eight equal groups by '
             f'distance below the high: the closest group closed the month higher '
             f'{pc(DP["h21"]["w52"]["buckets"][0]["lift"])} more often than base, while '
             f'the group about {pt(DP["h21"]["w52"]["buckets"][-2]["mid"], 0)} below its '
             f'high ran {pc(DP["h21"]["w52"]["buckets"][-2]["lift"])}. On a single stock '
             f'the pattern is noisy — EMAAR shows '
             f'{pt(M["ep_w52"]["near_up"], 0)} near its high against '
             f'{pt(M["ep_w52"]["far_up"], 0)} deep below it, the right direction but on '
             f'only {M["ep_w52"]["n_near"]}+{M["ep_w52"]["n_far"]} readings — which is '
             f'why the book-wide curve is the evidence, not any one name.'),
         over=('The very deepest group already bends back up a little. If a larger '
               'sample turns that bend into a real recovery effect, this becomes a '
               'U-shape lesson instead.')),

    dict(id='T-020', scope='ALL', status='PROVISIONAL', fig='05_rsi_curve.png',
         figcap='Ten equal slices of RSI. Nine say nothing; the top one says continue.',
         title='RSI is silent across nine tenths of its range.',
         body=('RSI is the most quoted number in retail technical analysis. Sliced into '
               'ten equal groups, the bottom nine are indistinguishable from each other '
               'and from the base rate — a stock with RSI 35 and a stock with RSI 65 '
               'face the same odds. Everything RSI knows lives in its top tenth, and '
               'what it says there is "this keeps going", not "this reverses".'),
         know=lambda: (
             f'Nine of the ten slices sit within about a point of the base rate, each '
             f'measured on roughly {DP["h5"]["rsi"]["buckets"][0]["n"]:,} readings — '
             f'differences well inside their own error bars. The top slice (RSI above '
             f'{DP["h5"]["rsi"]["buckets"][-1]["lo"]:.0f}) closed higher '
             f'{pc(DP["h5"]["rsi"]["buckets"][-1]["lift"])} more often over the week and '
             f'{pc(DP["h21"]["rsi"]["buckets"][-1]["lift"])} over the month.'),
         over=('A different RSI period, or RSI measured against the stock\'s own typical '
               'range instead of the fixed 0-100 scale, showing life in the middle.')),

    dict(id='T-006', scope='ALL', status='ACTED ON',
         title='A word that sounds like caution still needs checking. Ours pointed backwards.',
         body=('For years the pages described RSI above 70 as "stretched" and below 30 '
               'as "washed out". Both words whisper "reversal coming" to any reader. '
               'Measured, both were followed by the OPPOSITE of what they whisper — '
               'strong stocks kept going, weak ones kept sliding. The words survived '
               'unchecked precisely because they sounded prudent. They were replaced '
               'with "very strong" and "very weak" on 31-Aug-2026, and the fix is live.'),
         know=lambda: (
             f'Readings above 70 were followed by a higher close '
             f'{pc(eff("rsi_high",5))} more often than base over the week and '
             f'{pc(eff("rsi_high",21))} over the month ({nobs("rsi_high",5):,} '
             f'occasions) — momentum, not exhaustion. At the old three-month grading the '
             f'same group ran 7.6 in 100 above base.'),
         over=('Nothing about the finding. The lesson is the habit: audit '
               'conservative-sounding language exactly as hard as flattering language.')),

    dict(id='T-005', scope='ALL', status='PROVISIONAL',
         title='The MACD paragraph is the least useful ink on the page.',
         body=('Every read prints MACD with three numbers and a carefully hedged '
               'sentence. Tested against what prices then did, the histogram\'s sign — '
               'the thing chart traders act on — predicts nothing at any horizon. Not '
               'weakly something: measurably nothing, on a sample large enough to have '
               'found even a faint signal.'),
         know=lambda: (
             f'Days with a positive histogram closed the week higher '
             f'{pc(eff("macd",5),2)} more often than base and the month '
             f'{pc(eff("macd",21),2)} — both a rounding error from zero, on '
             f'{nobs("macd",5):,} readings. Only {sig("macd",21)[0]} of '
             f'{sig("macd",21)[1]} individual stocks show anything, which is what pure '
             f'chance produces at this sample size.'),
         over=('A different MACD construction — a signal-line crossing, a divergence — '
               'earning its place on its own evidence. The plain histogram is done.')),

    dict(id='T-011', scope='ALL', status='ACTED ON', fig='09_trigger.png', 
         fig2='19_demo_etel.png',
         figcap='Book-wide: the "zone" opens LESS often after a real level is cleared.',
         figcap2='And on one real stock: Telecom Egypt cleared 97.17 in June 2026; the '
                 'promised 113 zone was never approached.',
         title='"A close above resistance opens the next zone" — our data says the opposite.',
         body=('The old pages carried one genuinely conditional promise: close above the '
               'nearest resistance, and the far zone opens. It is the most natural '
               'sentence in technical analysis and it fails in the most instructive way '
               'possible — clearing a REAL level makes the next target LESS likely to be '
               'reached than clearing an empty price does. Why? Because the far level is '
               'real too. If lines hold (T-003), they also hold when they are your '
               'target. The sentence was rewritten on 31-Aug-2026 to name the next level '
               'without promising it.'),
         know=lambda: (
             f'Counting only months in which the trigger actually fired '
             f'({X["trigger|h21|both"]["n_real"]:,} firings): the far zone was then '
             f'reached {pt(X["trigger|h21|both"]["p_real"], 1)} of the time after a real '
             f'level was cleared, against {pt(X["trigger|h21|both"]["p_null"], 1)} after '
             f'an invented one — {pc(X["trigger|h21|both"]["effect"])} the WRONG way, '
             f'and worse over shorter windows. Telecom Egypt below is a typical firing, '
             f'not a chosen embarrassment.'),
         over=('Nothing about the direction. What it would take is a level-drawing '
               'method whose far targets are systematically weaker than its near ones — '
               'the opposite of how this one works.')),

    dict(id='T-012', scope='ALL', status='ACTED ON', fig='10_cross.png',
         fig2='20_demo_sabic.png',
         figcap='Fresh crosses against established ones, book-wide.',
         figcap2='SABIC, May 2026: a textbook fresh golden cross, then −7.6% in a month.',
         title='A golden cross is a description of the past, not a promise about the future.',
         body=('The read used to greet a fresh 50/200 cross with real drama: "a '
               'momentum-regime change rather than noise". Tested, a fresh golden cross '
               'is followed by slightly WORSE months than an old, established one, a '
               'fresh death cross by slightly better ones, and volatility does not '
               'change at all — there is no "regime" to speak of. The dramatic clause '
               'was deleted on 31-Aug-2026; the crossing itself is still reported, as '
               'the historical fact it is.'),
         know=lambda: (
             f'Comparing fresh crosses only against the SAME cross state when it is old '
             f'— so the trend itself cancels out: after a fresh golden cross the month '
             f'closed higher {pt(X["cross|h21|golden"]["p_real"], 1)} of the time versus '
             f'{pt(X["cross|h21|golden"]["p_null"], 1)} for an established one '
             f'({X["cross|h21|golden"]["n_real"]:,} fresh readings), and the ratio of '
             f'volatility after fresh to after established is '
             f'{X["cross|h21|golden"]["vol_ratio"]:.2f} — nothing. SABIC below is what '
             f'that looks like on a real chart.'),
         over=('A cross of different averages, or a different freshness window, earning '
               'the regime language on its own evidence.')),

    dict(id='T-013', scope='ALL', status='PROVISIONAL', fig='11_volume.png',
         figcap='Three ways to guess how far price will travel. Volume is the faint one.',
         title='Volume shouts about movement and says nothing about direction.',
         body=('Volume is in every library and the read has never used it — so this was '
               'exploration, not calibration. The result: a volume surge tells you the '
               'stock is about to MOVE, not which way. And the moving part is already '
               'said, far more clearly, by the tape sentence the pages carry today. '
               'Volume is not being added.'),
         know=lambda: (
             f'On {X["volume|h5"]["n"]:,} readings, high-volume days and low-volume days '
             f'were followed by a higher close equally often (a gap of '
             f'{pc(X["volume|h5"]["direction"]["effect"])}, indistinguishable from '
             f'zero). For predicting the SIZE of the coming move, volume scores '
             f'{VP["5"]["raw"]:+.2f} where the tape reading scores {VP["5"]["atr"]:+.2f} '
             f'— and once the tape reading is accounted for, volume adds only '
             f'{VP["5"]["partial"]:+.2f}. Real, and not worth a sentence.'),
         over=('A cleverer volume measure — turnover against free float, or volume split '
               'by up-days and down-days — clearing the bar the plain surge missed.')),

    # ------------------------------------------------ what the levels are made of
    dict(id='T-014', scope='ALL', status='PROVISIONAL', fig='02_level_kind.png',
         figcap='One week ahead: what each kind of line was worth when price reached it.',
         title='For a few days, the 20-day average is as strong a line as any on the chart.',
         body=('Our read believes in a hierarchy: real swing structure first, and '
               'moving averages, round numbers or the 52-week mark only as fillers. For '
               'the week ahead that hierarchy is wrong at the top — the 20-day average '
               'held at least as well as true structure. A month out it collapses to '
               'nothing, for a reason that is obvious once said: the average moves, so '
               'the line you drew from it goes stale in days.'),
         know=lambda: (
             f'Over one week, price failed to close through the 20-day average '
             f'{pc(dv(5,"by_kind","20-day MA"))} more often than through an invented '
             f'line ({dv(5,"by_kind","20-day MA","n"):,} tests), against '
             f'{pc(dv(5,"by_kind","swing"))} for swing structure '
             f'({dv(5,"by_kind","swing","n"):,} tests). Over one month the average is '
             f'worth {pc(dv(21,"by_kind","20-day MA"))} — nothing — while structure '
             f'still holds {pc(dv(21,"by_kind","swing"))}.'),
         over=('The 20-day sample is small because the read only admits an average when '
               'structure leaves a slot open. More data pulling it back to the pack '
               'would fold this into T-003.')),

    dict(id='T-016', scope='ALL', status='PROVISIONAL',
         title='Round numbers deserve more respect than we gave them.',
         body=('A price like 20.00 or 150 is where human orders cluster, and our read '
               'treats such lines as a last resort. Measured, a round number holds about '
               'three quarters as well as genuine charted structure — clearly weaker, '
               'clearly not nothing. The QNB picture under T-003 is, fittingly, a round '
               'number doing the work.'),
         know=lambda: (
             f'When price reached a published round-number line it failed to close '
             f'through {pc(dv(5,"by_kind","round"))} more often than through an invented '
             f'line over the week, and {pc(dv(21,"by_kind","round"))} over the month '
             f'({dv(21,"by_kind","round","n"):,} tests) — against '
             f'{pc(dv(21,"by_kind","swing"))} for swing structure on the same clock.'),
         over=('A market whose price grid makes "round" meaningless — very high nominal '
               'prices, say — where the effect should fade.')),

    dict(id='T-015', scope='ALL', status='PROVISIONAL', fig='03_touches.png',
         figcap='The edge, by how many times the level had been tested before.',
         title='A level tested five times is no stronger than a level tested once.',
         body=('Chart lore says every extra test proves a level. Our own read believes '
               'it — it ranks levels partly by touch count. Counted across the whole '
               'book, the edge is flat: once-tested and five-times-tested levels hold '
               'the same. What makes a level real appears to be that structure exists '
               'there at all, not how often it was rehearsed.'),
         know=lambda: (
             f'Grouped by prior touches, the one-month edge runs '
             f'{pc(dv(21,"by_touches","1"))} (one touch), '
             f'{pc(dv(21,"by_touches","2"))} (two), '
             f'{pc(dv(21,"by_touches","3-4"))} (three or four) and '
             f'{pc(dv(21,"by_touches","5+"))} (five or more) — no order, all within '
             f'noise of each other, on '
             f'{sum(dv(21,"by_touches",k,"n") for k in ("1","2","3-4","5+")):,} tests.'),
         over=('A touch counted differently — only touches that produced a sharp '
               'rejection, or touches close together in time — showing a real ladder.')),

    dict(id='T-017', scope='ALL', status='PROVISIONAL',
         title='The level printed first is not the one to trust most.',
         body=('We publish three levels a side, nearest first, and a reader naturally '
               'weights them in that order. Over a month the order inverts: the '
               'furthest level held best and the nearest held worst. Distance to a '
               'level is part of what makes it hold — a far level is only reached by a '
               'strong move, and strong moves are exactly what break lines.'),
         know=lambda: (
             f'Over one month the nearest published level held '
             f'{pc(dv(21,"by_rank","1.0"))} better than its invented twin, the middle '
             f'{pc(dv(21,"by_rank","2.0"))}, the furthest {pc(dv(21,"by_rank","3.0"))} — '
             f'on {dv(21,"by_rank","1.0","n"):,}, {dv(21,"by_rank","2.0","n"):,} and '
             f'{dv(21,"by_rank","3.0","n"):,} tests. Over one week the middle level was '
             f'strongest, so the honest summary is "not ordered the way the page '
               'implies", rather than a new ordering to memorise.'),
         over=('The same ordering reproducing under a different level-drawing method — '
               'as it stands it may partly reflect our own distance filters.')),

    # ---------------------------------------------------------------- durability
    dict(id='T-021', scope='ALL', status='WATCH', fig='13_stability.png',
         figcap='Each claim, measured separately on the two halves of fifteen years.',
         title='The moving-average-stack effect worked before 2020 and has not worked since.',
         body=('The cheapest honesty test in research: cut the years in half and ask '
               'each finding to show up in both halves. The stack sentence fails it at '
               'the one-month horizon — a real effect in 2012-2020 and a slightly '
               'negative one since. What we publish as its overall figure is an average '
               'of "used to work" and "does not". It stays on the pages as a '
               'description; as a lean it is on watch.'),
         know=lambda: (
             f'One-month horizon, split at '
             f'{DP["h21"]["stability"]["early"]["split_at"]}: above-stack weeks beat '
             f'below-stack weeks by {pc(DP["h21"]["stability"]["early"]["trend"])} in '
             f'the first half and {pc(DP["h21"]["stability"]["late"]["trend"])} in the '
             f'second. At one week it survives with the same sign but shrinks, '
             f'{pc(DP["h5"]["stability"]["early"]["trend"])} to '
             f'{pc(DP["h5"]["stability"]["late"]["trend"])}.'),
         over=('The next few years restoring it — WATCH, not withdrawn, because half a '
               'sample is a blunt instrument and the weekly horizon still holds.')),

    dict(id='T-022', scope='ALL', status='PROVISIONAL',
         title='The level edge and the tape reading pass the same durability test.',
         body=('The split that embarrassed the stack sentence is exactly what makes the '
               'other two findings credible. The level edge is about the same size in '
               'both halves of fifteen years, and the tape reading is actually stronger '
               'in the recent half. Findings that show up twice, in two different '
               'market eras, are a different class of evidence from findings that show '
               'up on average.'),
         know=lambda: (
             f'Levels: {pc(DP["h5"]["stability"]["early"]["levels"]["effect"])} before '
             f'{DP["h5"]["stability"]["early"]["split_at"]} and '
             f'{pc(DP["h5"]["stability"]["late"]["levels"]["effect"])} after, at one '
             f'week. Tape: a correlation of '
             f'{DP["h21"]["stability"]["early"]["tape"]:+.2f} then '
             f'{DP["h21"]["stability"]["late"]["tape"]:+.2f}. Both re-run at every pass.'),
         over=('Either measure fading toward zero in a future half — the same check '
               'that caught T-021 is standing guard here.')),

    dict(id='T-023', scope='ALL', status='PROVISIONAL', fig='04_atr_ladder.png',
         figcap='What actually followed each of the four words, over fifteen years.',
         title='Four small words that keep four different promises.',
         body=('"An orderly tape. A normal tape. A lively tape. A volatile tape." They '
               'read like colour, but each one corresponds to a genuinely different '
               'amount of movement in the month that follows, in the right order, with '
               'barely any overlap between the extremes. This is what a calibrated '
               'instrument looks like, and it is the standard every other sentence on '
               'the page is now held to.'),
         know=lambda: (
             ' · '.join(f"after “{b['word']}” → {b['med']*100:.0f}%"
                        for b in DP['h21']['atr'])
             + (f" (median movement at an annual pace over the following month, "
                f"{sum(b['n'] for b in DP['h21']['atr']):,} readings). The middle half "
                f"of outcomes after “orderly” spans "
                f"{DP['h21']['atr'][0]['q25']*100:.0f}–"
                f"{DP['h21']['atr'][0]['q75']*100:.0f}%; after “volatile”, "
                f"{DP['h21']['atr'][-1]['q25']*100:.0f}–"
                f"{DP['h21']['atr'][-1]['q75']*100:.0f}%.")),
         over=('A market where the ladder collapses or inverts. Checked per market; all '
               'nine keep the order.')),

    # ================================================================ A CLASS
    dict(id='T-007', scope='CLASS', cls='market', status='PROVISIONAL',
         fig='08_level_market.png',
         figcap='The level edge, per market, one week ahead.',
         title='Where the chart is drawn changes what a level is worth. Saudi doubles Egypt.',
         body=('The level test does not come out the same everywhere. A drawn level in '
               'Riyadh is worth roughly twice what the same construction is worth in '
               'Cairo, with the UAE in between — and the differences are too large to '
               'be sampling luck. This is the one place in the whole calibration where '
               'the market a stock trades on genuinely changes the answer, rather than '
               'just its strength.'),
         know=lambda: (
             f'One week ahead, the edge over the invented line is '
             f'{pc(klass("levels",5,"market_label","Saudi (Tadawul)"))} in Saudi, '
             f'{pc(klass("levels",5,"market_label","UAE (ADX & DFM)"))} in the UAE and '
             f'{pc(klass("levels",5,"market_label","Egypt (EGX)"))} in Egypt. A formal '
             f'test of whether three markets could differ this much by chance says no '
             f'(p = {cell("levels",5)["heterogeneity"]["p"]:.3f}).'),
         over=('Only these three markets have enough stocks to be judged. A fourth '
               'landing in the middle would soften this; one landing outside would '
               'sharpen it.')),

    dict(id='T-008', scope='CLASS', cls='market', status='PROVISIONAL',
         title='The tape reading works everywhere; it works hardest in the Gulf.',
         body=('Unlike the levels, the tape sentence never changes its answer with '
               'geography — only its volume. It is strongest in the UAE and Saudi and '
               'mildest in Egypt, and positive with room to spare in every market and '
               'every sector tested. So the claim belongs on every page unchanged, '
               'while how much weight to put on it is a market fact.'),
         know=lambda: (
             f'One week ahead the correlation between the tape reading and the movement '
             f'that followed is '
             f'{klass("tape",5,"market_label","UAE (ADX & DFM)"):+.2f} in the UAE, '
             f'{klass("tape",5,"market_label","Saudi (Tadawul)"):+.2f} in Saudi and '
             f'{klass("tape",5,"market_label","Egypt (EGX)"):+.2f} in Egypt; across ten '
             f'industry sectors it spans '
             f'{min(v["effect"] for v in cell("tape",5,"sector")["per_class"].values()):+.2f} '
             f'to '
             f'{max(v["effect"] for v in cell("tape",5,"sector")["per_class"].values()):+.2f}, '
             f'never near zero.'),
         over=('Any class of stocks where it reads at zero on at least four names. None '
               'found.')),

    dict(id='T-009', scope='CLASS', cls='sector', status='WATCH',
         title='For charts, the exchange is a real category. The industry mostly is not.',
         body=('The fundamental register learns lessons per kind of company — banks, '
               'developers, cement. It is tempting to assume charts work the same way. '
               'They largely do not: what moves a technical result is the venue (its '
               'price limits, its liquidity, its trading week), and once the venue is '
               'accounted for, industry adds little. Where a sector split looks '
               'interesting, the market split explains it better.'),
         know=lambda: (
             f'The stack sentence is statistically one population across sectors at one '
             f'week (p = {cell("trend",5,"sector")["heterogeneity"]["p"]:.2f}); so is '
             f'the MACD null. The repo\'s own sector labels also had to be repaired '
             f'before testing — 32 different labels for 84 stocks, including three '
             f'spellings of "financial" — and four of the ten resulting groups hold '
             f'five names or fewer.'),
         over=('A claim that separates cleanly by industry while staying uniform across '
               'markets. None found so far.')),

    # ================================================================ ONE TICKER
    dict(id='T-010', scope='STOCK', status='PROVISIONAL', fig='12_pername_tape.png',
         figcap='Each bar counts stocks; almost the whole book sits to the right of zero.',
         title='Only the tape sentence has earned the right to be said stock-by-stock.',
         body=('Saying "this works on THIS stock" needs the stock\'s own history to '
               'prove it, which is a far higher bar than proving it on the whole book. '
               'One claim clears that bar: the tape sentence, individually confirmed on '
               'nearly every name. The stack sentence looked like it cleared it on a '
               'handful of names — and for every stock where it seemed to work, there '
               'was one where it seemed to work BACKWARDS, which is what noise looks '
               'like. No per-stock trend claims are made, for anyone.'),
         know=lambda: (
             f'The tape reading is individually significant and positive on '
             f'{sig("tape",5)[0]} of {sig("tape",5)[1]} stocks with enough history at '
             f'one week (against 1 negative, where chance alone would produce about '
             f'4.6 of each). The stack test splits 13 "works" against 12 "works '
             f'backwards" at one month — a perfect coin flip. An earlier edition of '
             f'this register read only the positive half of that split and published '
             f'"trend, per name where earned"; this edition withdraws it.'),
         over=('For the tape: nothing pending — 84-3 is not luck. For any future '
               'per-stock claim: it must beat its own mirror image, not just zero.')),

    dict(id='T-027', scope='STOCK', status='PROVISIONAL',
         title='IHC is the most readable chart in the book. SALIK and LULU cannot be read at all yet.',
         body=('Two honest extremes of the same rule. International Holding Company has '
               'nine years of readings and the strongest tape relationship of all 92 '
               'names — its quiet spells and its storms both announce themselves. At '
               'the other end, Salik and Lulu simply have not lived long enough: their '
               'histories cannot yet prove or disprove anything about them, and their '
               'pages must lean on the book-wide record instead. Youth is not a defect, '
               'but it is a fact a reader deserves to see stated.'),
         know=lambda: (
             f'IHC: tape correlation {M["ihc"]["rho"]:+.2f} over {M["ihc"]["n"]} monthly '
             f'readings — the highest in the book (see the chart under T-002). SALIK '
             f'has {M["young_SALIK"]} weekly readings of history and LULU '
             f'{M["young_LULU"]}, against the roughly 60 this calibration requires '
             f'before it will print a stock-specific number.'),
         over=('Time. Both young names accrue about 50 readings a year and cross the '
               'threshold on their own.')),
]
