"""Block-bootstrap CIs on the state-clause lifts (house bar: blocks {2,3,4})."""
import pandas as pd, numpy as np, json, score
r = pd.read_pickle('claims.pkl')
d = r[r.claim == 'state'].copy()
d['key'] = d.market + '_' + d.ticker
out = {}
for months in (1, 3):
    s = d[d.months == months].copy()
    base = float((s.fwd_ret > 0).mean())
    out[months] = {'base': base, 'cells': {}}
    cells = {
        'stack above': s.trend.str.startswith('Trading above the whole'),
        'stack below': s.trend.str.startswith('Trading below the whole'),
        'RSI stretched (>=70)': s.rsi >= 70,
        'RSI washed out (<30)': s.rsi < 30,
        'RSI soft (30-40)': (s.rsi >= 30) & (s.rsi < 40),
    }
    for label, mask in cells.items():
        sub = s[mask]
        if len(sub) < 100:
            continue
        # lift of this bucket's up-rate over the pooled base rate
        x = (sub.fwd_ret > 0).astype(float).to_numpy() - base
        ci = score.block_boot(x, sub.key.to_numpy())
        out[months]['cells'][label] = dict(
            n=int(len(sub)), up=float((sub.fwd_ret > 0).mean()), lift=float(x.mean()),
            ci={str(k): v for k, v in ci.items()}, verdict=score.robust(ci))
        print(f"{months}M {label:22} n={len(sub):>5} up={float((sub.fwd_ret>0).mean()):.3f} "
              f"lift={x.mean():+.4f} [{score.robust(ci)}] "
              + " ".join(f"b{k}:[{v[0]:+.3f},{v[1]:+.3f}]" for k, v in ci.items()), flush=True)
json.dump(out, open('RESULTS_state_ci.json', 'w'), indent=1, default=float)
