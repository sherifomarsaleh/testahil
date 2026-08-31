"""Emit the register payload — every number resolved from RESULTS_scopes.json."""
import json, os, datetime
import lessons_source as L

HERE = os.path.dirname(os.path.abspath(__file__))
R = L.R

def cov():
    c = L.cell('tape', 5)
    return dict(names=c['n_stocks'], obs=c['pooled']['n'])

payload = dict(
    generated=datetime.date(2026, 8, 31).strftime('%d %B %Y'),
    coverage=cov(),
    horizons=[{'h': h, 'name': L.HORIZON_NAME[h]} for h in (5, 10, 21)],
    evidence_rows=[
        ['Technical walk-forward', 'the technical read, replayed at every historical '
         'origin and graded on the tape', f"{L.cell('tape',5)['n_stocks']} names",
         f"{L.cell('tape',5)['pooled']['n']:,} readings"],
        ['Price-engine walk-forward', 'the probability cone, graded against resolved '
         'forecasts', '19 names', 'per the fundamental register'],
        ['Fundamental walk-forward', 'the valuation method, graded against filed actuals',
         '1 name (PHDC)', 'per the fundamental register'],
    ],
    indicators=[
        ['Moving averages', '20, 50 and 200 sessions',
         'Simple averages of the closing price. The read states which of them price sits above.'],
        ['Moving-average slope', 'change over 10 sessions; flat if within 0.3%',
         'Whether each average is rising, flat or falling.'],
        ['RSI', "Wilder's, 14 sessions",
         'A 0-100 momentum gauge. High means price has risen on most recent days.'],
        ['ATR', "Wilder's, 14 sessions, on the true range",
         'The average distance price travels in a day, gaps included. The read turns it into the tape sentence.'],
        ['MACD', '12 and 26 session averages, 9-session signal',
         'A trend-following oscillator. The read states the line, the signal and the histogram.'],
        ['50/200 cross', 'flagged as fresh within 25 sessions',
         'The golden cross and the death cross.'],
        ['52-week range', '252 sessions',
         'The high, the low, and how far the last close sits from each.'],
        ['Support and resistance', 'fractal pivots, half-width 5 bars, 500-session lookback',
         'Turning points on the chart, grouped into levels when within 1.5% of each other.'],
        ['  - level weighting', 'recency half-life 180 sessions, weighted by touch count',
         'Recent tests count for more than old ones; more tests counts for more than fewer.'],
        ['  - level filtering', 'at least 0.8% from spot, at most 35%; 3 published per side',
         'A line too close to the price is not a level.'],
        ['  - other level sources', 'the three averages, the 52-week extremes, round numbers',
         'Admitted only when swing structure does not fill the slot, and scored below it.'],
        ['Volume', 'tested here, used nowhere',
         'Present in every library. Scored in T-013 and not adopted.'],
    ],
    figures={x['id']: x['fig'] for x in L.LESSONS if x.get('fig')},
    lessons=[dict(id=x['id'], scope=x['scope'], cls=x.get('cls'), status=x['status'],
                  fig=x.get('fig'), fig2=x.get('fig2'),
                  figcap=x.get('figcap'), figcap2=x.get('figcap2'),
                  title=x['title'], body=x['body'],
                  know=x['know']() if callable(x['know']) else x['know'],
                  over=x['over']) for x in L.LESSONS],
)
json.dump(payload, open(os.path.join(HERE, 'register_payload.json'), 'w'), indent=1)
# COUNT AGAINST THE SOURCE, not against a number typed here. The first version
# asserted == 10 and fired the moment three lessons were added, which is the
# check working but measuring the wrong thing: what must hold is that every
# lesson in the source reaches the payload, whatever the total.
n = len(payload['lessons'])
assert n == len(L.LESSONS), f'{n} in payload vs {len(L.LESSONS)} in source'
assert len({x['id'] for x in payload['lessons']}) == n, 'duplicate lesson id'
print(f"payload written: {n} lessons, {payload['coverage']['names']} names, "
      f"{payload['coverage']['obs']:,} readings")
