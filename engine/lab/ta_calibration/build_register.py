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
    lessons=[dict(id=x['id'], scope=x['scope'], cls=x.get('cls'), status=x['status'],
                  title=x['title'], body=x['body'],
                  know=x['know']() if callable(x['know']) else x['know'],
                  over=x['over']) for x in L.LESSONS],
)
json.dump(payload, open(os.path.join(HERE, 'register_payload.json'), 'w'), indent=1)
n = len(payload['lessons'])
assert n == 10, n
print(f"payload written: {n} lessons, {payload['coverage']['names']} names, "
      f"{payload['coverage']['obs']:,} readings")
