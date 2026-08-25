#!/usr/bin/env python3
"""Re-measure fit drift against current main, WITHOUT trusting the ledger note.

Method (the task's own suggested route, and [R-WIDTH-01]-compliant):
  re-strike every covered name through the production chain at anchor_idx=-1
  (which IS the published anchor, because every page currently stands on its
  library), then compare the resulting 90% cone half-width in LOG space against
  the PUBLISHED dist. Log half-width is drift-invariant, so q_annual and the
  carry anchor cannot contaminate the width comparison.

  Because the library and anchor are identical, the ONLY thing that can move the
  half-width is the fit itself: (nu, width_cal) and the per-name overlay
  multiplier. The overlay is read by RECOMPUTING live_width_mult() inside
  strike(), never inferred from a note.

Materiality is the engine's own metric, imported not reimplemented:
  auto_refresh.BAND_TOL on the relative move of the published 90% cone.
"""
import json, os, subprocess, sys, math, warnings
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(ROOT, 'engine')
sys.path.insert(0, ENGINE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

from apply_technicals import EXCHANGE_MARKET, SERIES_OVERRIDE, METAL_MARKET
from strike_cohorts import strike
from market_profiles import PROFILES
from auto_refresh import BAND_TOL, band_halfwidth

NODE = ("const fs=require('fs'),vm=require('vm');const s={};vm.createContext(s);"
        "vm.runInContext(fs.readFileSync(process.argv[1],'utf8')"
        "+';globalThis.__T=TICKERS;globalThis.__L=LEDGER;',s);"
        "process.stdout.write(JSON.stringify({t:s.__T,l:s.__L}));")
data = json.loads(subprocess.run(['node','-e',NODE, os.path.join(ROOT,'assets','data.js')],
                                 capture_output=True, text=True, check=True).stdout)

def half(p5, p95):
    return (math.log(p95) - math.log(p5)) / 2.0

rows, skipped = [], []
items = sorted(data['t'].items())
for n, (key, e) in enumerate(items, 1):
    code = str(e.get('code') or '')
    mkt = EXCHANGE_MARKET.get(code.split(':')[0])
    if not mkt:
        skipped.append((key, 'no market from code prefix')); continue
    series = SERIES_OVERRIDE.get(key, key)
    dist = e.get('dist') or {}
    if not dist.get('t60') or not dist.get('t20'):
        skipped.append((key, 'no published t20/t60 dist')); continue
    try:
        r = strike(mkt, series)
    except Exception as exc:
        skipped.append((key, f'{type(exc).__name__}: {exc}')); continue

    pub_anchor = (((e.get('asof') or {}).get('mc') or {}).get('data')) or ''
    rec = {'key': key, 'market': mkt, 'code': code,
           'pub_anchor': pub_anchor, 'strike_anchor': r['anchor_date'],
           'anchor_match': pub_anchor == r['anchor_date'],
           'nu_live': r['nu'], 'cal_live': r['width_cal'],
           'overlay_mult': r['width_overlay_mult'],
           'override': r['fit_override_applied']}
    for tag, hz in (('t20','1M'), ('t60','3M')):
        pub = dist[tag]
        h_pub = half(float(pub['p5']), float(pub['p95']))
        h_new = half(r['horizons'][hz]['pct']['p5'], r['horizons'][hz]['pct']['p95'])
        rec[f'{hz}_pub'] = h_pub
        rec[f'{hz}_new'] = h_new
        rec[f'{hz}_rel'] = (h_new - h_pub) / h_pub
    rows.append(rec)
    print(f"  [{n:3d}/{len(items)}] {key:12s} {mkt}  3M {rec['3M_rel']:+7.2%}  "
          f"1M {rec['1M_rel']:+7.2%}  mult={rec['overlay_mult']:.4f}"
          f"{'  ANCHOR-MISMATCH' if not rec['anchor_match'] else ''}", flush=True)

json.dump({'rows': rows, 'skipped': skipped, 'band_tol': BAND_TOL},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RESULTS_25-08-2026.json'),'w'), indent=1)
print(f"\nmeasured {len(rows)}, skipped {len(skipped)}")
for k, why in skipped:
    print(f"  SKIP {k}: {why}")
