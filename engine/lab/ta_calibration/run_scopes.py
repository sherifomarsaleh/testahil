import json, pandas as pd, numpy as np
import scopes, scope_analysis as SA

r = scopes.annotate(pd.read_pickle('claims_short.pkl'))
print(f"{len(r):,} rows | {r.key.nunique()} names | horizons {sorted(r.h.unique())}")
print(f"markets {r.market_label.nunique()} | coarse sectors {r.sector.nunique()}\n")

out = {}
FAM = ['trend', 'tape', 'rsi_high', 'rsi_low', 'macd', 'levels']
for cls_col in ('market_label', 'sector'):
    for fam in FAM:
        for h in sorted(r.h.unique()):
            k = f'{fam}|h{h}|{cls_col}'
            try:
                out[k] = SA.run(r, fam, int(h), cls_col)
            except Exception as e:
                out[k] = {'error': f'{type(e).__name__}: {e}'}
json.dump(out, open('RESULTS_scopes.json','w'), indent=1, default=float)

print('='*92)
print('POOLED (ALL TICKERS) — the same numbers whichever class dimension is used')
print('='*92)
print(f"{'claim':10} {'h':>4} {'n':>8} {'effect':>9} {'z':>7}  {'verdict':11} {'names sig':>10} / {'tested':>6}")
for fam in FAM:
    for h in (5,10,21):
        v=out.get(f'{fam}|h{h}|market_label')
        if not v or not v.get('pooled'): continue
        p=v['pooled']; z=p['effect']/p['se'] if p['se'] else 0
        verdict = 'HOLDS' if abs(z)>1.96 else 'not proven'
        print(f"{fam:10} {h:>4} {p['n']:>8,} {p['effect']:>+9.4f} {z:>7.1f}  {verdict:11} "
              f"{v['n_stocks_sig']:>10} / {v['n_stocks']:>6}")
