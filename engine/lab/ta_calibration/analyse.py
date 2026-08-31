"""analyse.py — the scored result table. Every cell reported, none selected."""
import pandas as pd, numpy as np, json, sys
import score

r = pd.read_pickle('claims.pkl')
lv = r[(r.claim == 'level') & (r.n_sides == 2)].copy()
lv['key'] = lv.market + '_' + lv.ticker
out = {'meta': {}, 'levels': [], 'trend': {}, 'tape': {}, 'rsi': {}}
out['meta'] = dict(
    claim_rows=int(len(r)), names=int(len(r.groupby(['market', 'ticker']))),
    origin_first=r.origin.min(), origin_last=r.origin.max(),
    level_rows=int((r.claim == 'level').sum()), two_sided=int(len(lv)),
    dist_real=float(lv.dist.mean()), dist_null=float(lv.placebo_dist.mean()))
print(json.dumps(out['meta'], indent=1), flush=True)


def cell(d, months, side, rank):
    both = d[d.touched & d.p_touched].dropna(subset=['p_broke'])
    if len(both) < 30:
        return dict(months=months, side=side, rank=rank, n=int(len(both)), note='too few')
    diff = (both.p_broke - both.broke.astype(float)).to_numpy()
    ci = score.block_boot(diff, both.key.to_numpy())
    # LONO, vectorised: leave-one-name-out mean from per-name sums.
    g = pd.DataFrame({'k': both.key.to_numpy(), 'd': diff}).groupby('k').agg(['sum', 'count'])
    tot_s, tot_n = diff.sum(), len(diff)
    lono = (tot_s - g[('d', 'sum')]) / (tot_n - g[('d', 'count')])
    o = pd.to_datetime(both.origin); med = o.median()
    e, l = diff[(o <= med).to_numpy()].mean(), diff[(o > med).to_numpy()].mean()
    return dict(
        months=months, side=side, rank=rank, n=int(len(both)),
        names=int(len(both.groupby(['market', 'ticker']))),
        dist_real=float(both.dist.mean()), dist_null=float(both.p_touch_dist.mean()),
        broke_real=float(both.broke.mean()), broke_null=float(both.p_broke.mean()),
        delta=float(diff.mean()), ci={str(k): v for k, v in ci.items()},
        verdict=score.robust(ci),
        lono_min=float(lono.min()), lono_max=float(lono.max()),
        lono_same_sign=bool((lono > 0).all() or (lono < 0).all()),
        split_early=float(e), split_late=float(l),
        split_same_sign=bool(np.sign(e) == np.sign(l) and e != 0))


for months in (1, 3):
    for side in ('res', 'sup'):
        for rank in (1, 2, 3, None):
            d = lv[(lv.months == months) & (lv.side == side)]
            if rank:
                d = d[d['rank'] == rank]
            c = cell(d, months, side, rank or 'all')
            out['levels'].append(c)
            if 'note' in c:
                print(f"{months}M {side.upper()}{rank or ' all'}: {c['note']} (n={c['n']})", flush=True)
            else:
                print(f"{months}M {side.upper()}{rank or ' all'} | n={c['n']:>5} names={c['names']:>2} | "
                      f"dist {c['dist_real']:.4f}/{c['dist_null']:.4f} | "
                      f"broke real {c['broke_real']:.3f} null {c['broke_null']:.3f} | "
                      f"delta {c['delta']:+.4f} [{c['verdict']}] "
                      f"LONO{'=' if c['lono_same_sign'] else '!'} split{'=' if c['split_same_sign'] else '!'}",
                      flush=True)

for months in (1, 3):
    out['trend'][months] = score.score_trend(r, months)
    out['tape'][months] = score.score_tape(r, months)
    out['rsi'][months] = score.score_rsi(r, months)

json.dump(out, open('RESULTS.json', 'w'), indent=1, default=float)
print('\nwrote RESULTS.json', flush=True)
