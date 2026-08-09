"""AE panel refit with BOROUGE added — the standing materiality gate.

New coverage places one file in the persistent library; the whole AE market is
then re-fitted against the full library. update_registry=False: the result is
written to the study directory for review, NOT straight into fitted_configs.json,
because a new name arriving already FAILING is an explicit materiality stop.
"""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from panel_refresh import refresh_market

RAW = os.path.join(HERE, '..', 'raw_ohlc', 'AE')
lookup = {os.path.basename(p)[:-4]: p for p in sorted(glob.glob(os.path.join(RAW, '*.csv')))}
assert 'BOROUGE' in lookup, lookup.keys()
print(f"AE library: {len(lookup)} names -> {sorted(lookup)}")

res = refresh_market('AE', {'BOROUGE': lookup['BOROUGE']}, lookup,
                     update_registry=False, tag='3m')
with open(os.path.join(HERE, 'panel_refit_ae.json'), 'w') as f:
    json.dump(res, f, indent=1, default=str)
print(json.dumps({k: v for k, v in res.items() if k != 'per_name'}, indent=1, default=str))
for n, d in sorted(res['per_name'].items()):
    print(f"  {n:<14} skill {d.get('skill'):+.4f}  {d.get('verdict')}")
