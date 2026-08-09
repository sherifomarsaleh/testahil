"""EGCH — the computed technical read, from the same cleaned series the rest of the
study uses. Nothing here is fitted; every clause of the narrative is selected by a
computed number."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import technicals as T
res = T.compute('EG', 'EGCH')
json.dump(res, open(os.path.join(HERE, 'technicals.json'), 'w'), indent=1, default=float)
print({k: (round(v, 2) if isinstance(v, float) else v)
       for k, v in res.items() if not isinstance(v, (list, dict))})
print('levels:', res.get('levels'))
