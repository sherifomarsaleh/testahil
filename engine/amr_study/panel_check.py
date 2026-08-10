"""AMR — UAE panel refit + materiality assessment with AMR added.

Runs the same machinery the unattended loop runs, but with update_registry=False:
this study does not publish, so neither fitted_configs.json nor market_profiles.py
is touched. The output is the evidence: whether adding AMR to the 18-name UAE panel
is material under the standing gate (band move > 5%, any verdict change, a new name
arriving already failing, market-verdict change).
"""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from panel_refresh import refresh_market
from auto_refresh import assess_materiality
from market_profiles import PROFILES

RAW = os.path.join(HERE, '..', 'raw_ohlc', 'AE')
lookup = {os.path.basename(p)[:-4]: p for p in sorted(glob.glob(os.path.join(RAW, '*.csv')))}
assert 'AMR' in lookup, lookup.keys()
print(f"AE panel with AMR: {len(lookup)} names")

res = refresh_market('AE', {'AMR': lookup['AMR']}, lookup, update_registry=False, tag='3m')
with open(os.path.join(HERE, '..', 'fitted_configs.json')) as f:
    incumbent = json.load(f)['AE']
material, reasons, added = assess_materiality('AE', res, PROFILES['AE'], incumbent)

out = dict(
    incumbent=dict(nu=incumbent['nu'], width_cal=incumbent['width_cal'],
                   market_verdict=incumbent['market_verdict'],
                   market_skill=incumbent['market_skill'], market_ci90=incumbent['market_ci90'],
                   panel_names=incumbent['panel_names'], windows=incumbent['windows']),
    refit=dict(nu=res['nu'], width_cal=res['width_cal'],
               market_verdict=res['market_verdict'], market_skill=res['market_skill'],
               market_ci90=res['market_ci90'], windows=res['windows'],
               panel_names=res['panel_names']),
    amr=res['per_name'].get('AMR', {}),
    per_name=res['per_name'],
    material=bool(material), reasons=reasons, added=added,
    registry_written=False,
)
with open(os.path.join(HERE, 'panel_check.json'), 'w') as f:
    json.dump(out, f, indent=1, default=str)
print(f"\nincumbent : nu={incumbent['nu']} cal={incumbent['width_cal']} "
      f"{incumbent['market_verdict']} {incumbent['market_skill']:+.4f} "
      f"({len(incumbent['panel_names'])} names, {incumbent['windows']} windows)")
print(f"with AMR  : nu={res['nu']} cal={res['width_cal']} "
      f"{res['market_verdict']} {res['market_skill']:+.4f} "
      f"({len(res['panel_names'])} names, {res['windows']} windows)")
print(f"AMR       : {out['amr']}")
print(f"MATERIAL  : {material}")
for r in reasons:
    print('  -', r)
