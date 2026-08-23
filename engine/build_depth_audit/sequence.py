# -*- coding: utf-8 -*-
"""Order the 83 studies owed an update into a work sequence.

Ordering principle, in priority order:
  1. Studies that already have a working model come first - they are re-runs, not
     rebuilds, and they lock the standard cheaply before the expensive work starts.
  2. Then batch by EXCHANGE. The cost-of-capital inputs (sovereign yield, equity risk
     premium, index, tax) are per-country, so doing a whole exchange together sources
     each input once instead of once per name.
  3. Within an exchange, batch by BUSINESS CLASS, so same-class names reuse one lens
     and one peer set.
  4. Within a class, alphabetical - no hidden ranking.
"""
import json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = json.load(open(os.path.join(HERE, 'queue_raw.json')))

EXCH_ORDER = ['EGX', 'ADX', 'DFM', 'TADAWUL', 'QSE', 'KRX', 'NSE', 'NASDAQ']
import importlib.util as _i
_s=_i.spec_from_file_location('cl', os.path.join(os.path.dirname(os.path.abspath(__file__)),'classes.py'))
_CL=_i.module_from_spec(_s); _s.loader.exec_module(_CL)
CLASS_ORDER = _CL.ORDER

# Wave 1 is every study that already has a working model, whatever its exchange.
w1 = [r for r in ROWS if r['code']]
rest = [r for r in ROWS if not r['code']]

def keyed(rs):
    return sorted(rs, key=lambda r: (EXCH_ORDER.index(r['x']), CLASS_ORDER.index(r['cls']), r['tk']))

WAVES = [('Wave 1', 'Studies that already have a working model',
          'Re-runs, not rebuilds. Cheapest work in the book and it locks the standard before '
          'the expensive reconstruction starts.', keyed(w1))]

by_x = collections.defaultdict(list)
for r in rest: by_x[r['x']].append(r)

GROUPS = [('Wave 2', ['EGX'],  'Egypt', 'The largest single block, and it holds every one of the seven studies whose beta is known wrong. One Egyptian cost-of-capital sourcing serves all of them.'),
          ('Wave 3', ['ADX', 'DFM'], 'United Arab Emirates', 'Run only after the Dubai index is registered - eight of these are Dubai-listed and are standing on an Abu Dhabi index today.'),
          ('Wave 4', ['TADAWUL'], 'Saudi Arabia', 'One sovereign, one index, one tax regime across the whole batch.'),
          ('Wave 5', ['QSE', 'KRX', 'NSE', 'NASDAQ'], 'The international tail', 'Four small country batches. Each needs its own sovereign row, so they are cheapest done last, together.')]

for name, xs, label, why in GROUPS:
    rs = keyed([r for x in xs for r in by_x[x]])
    if rs: WAVES.append((name, label, why, rs))

n = 0
out = []
for wname, wlabel, wwhy, rs in WAVES:
    grouped = collections.OrderedDict()
    for r in rs:
        grouped.setdefault((r['x'], r['cls']), []).append(r)
    batch = []
    for (x, cls), items in grouped.items():
        for r in items:
            n += 1
            r['seq'] = n
        batch.append(dict(exchange=x, cls=cls, items=items))
    out.append(dict(wave=wname, label=wlabel, why=wwhy, batches=batch,
                    count=sum(len(b['items']) for b in batch)))

json.dump(out, open(os.path.join(HERE, 'queue.json'), 'w'), indent=1)
print('sequenced', n, 'studies across', len(out), 'waves')
for w in out:
    print(f"  {w['wave']:8s} {w['label']:44s} {w['count']:3d}")
    for b in w['batches']:
        print(f"      {b['exchange']:8s} {b['cls']:22s} {len(b['items']):2d}  "
              f"{', '.join(i['tk'] for i in b['items'])}")
