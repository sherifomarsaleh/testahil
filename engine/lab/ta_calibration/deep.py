"""deep.py — the cuts the first calibration never made.

Beyond "does the claim hold", these ask the questions a technical analyst would
actually ask, and several of them test assumptions technicals.py makes about
ITSELF — the ranking of level kinds, the weight given to touch count, the
distance cut-off. Those were chosen by convention and have never been measured.
"""
from __future__ import annotations
import numpy as np, pandas as pd, json
from scipy import stats

MIN = 60


def _paired(d):
    b = d[(d.n_sides == 2) & d.touched & d.p_touched].dropna(subset=['p_broke'])
    if len(b) < MIN:
        return None
    x = (b.p_broke - b.broke.astype(float)).to_numpy()
    se = x.std(ddof=1) / np.sqrt(len(x))
    return dict(effect=float(x.mean()), se=float(se), n=int(len(x)),
                z=float(x.mean() / se) if se else 0.0,
                real=float(b.broke.mean()), null=float(b.p_broke.mean()))


def by(d, col, h, buckets=None):
    out = {}
    s = d[(d.claim == 'level') & (d.h == h)]
    for k, g in s.groupby(col if buckets is None else buckets):
        v = _paired(g)
        if v:
            out[str(k)] = v
    return out


def rsi_curve(r, h, nb=10):
    d = r[(r.claim == 'state') & (r.h == h)].dropna(subset=['rsi']).copy()
    d['b'] = pd.qcut(d.rsi, nb, duplicates='drop')
    base = float((d.fwd_ret > 0).mean())
    rows = []
    for b, g in d.groupby('b', observed=True):
        p = float((g.fwd_ret > 0).mean())
        rows.append(dict(lo=float(b.left), hi=float(b.right), mid=float(g.rsi.mean()),
                         n=int(len(g)), up=p, lift=p - base,
                         se=float(np.sqrt(p * (1 - p) / len(g)))))
    return dict(base=base, buckets=rows)


def atr_curve(r, h):
    d = r[(r.claim == 'state') & (r.h == h)].dropna(subset=['atr_pct', 'rlz_vol'])
    edges = [(0, .015, 'an orderly tape'), (.015, .030, 'a normal tape'),
             (.030, .050, 'a lively tape'), (.050, 9, 'a volatile tape')]
    rows = []
    for lo, hi, name in edges:
        g = d[(d.atr_pct >= lo) & (d.atr_pct < hi)]
        if len(g) >= 50:
            rows.append(dict(word=name, n=int(len(g)),
                             med=float(g.rlz_vol.median()),
                             q25=float(g.rlz_vol.quantile(.25)),
                             q75=float(g.rlz_vol.quantile(.75))))
    return rows


def state_lift(r, h, col, order):
    d = r[(r.claim == 'state') & (r.h == h)].dropna(subset=[col])
    base = float((d.fwd_ret > 0).mean())
    rows = []
    for k in order:
        g = d[d[col] == k]
        if len(g) < MIN:
            continue
        p = float((g.fwd_ret > 0).mean())
        rows.append(dict(state=k, n=int(len(g)), up=p, lift=p - base,
                         se=float(np.sqrt(p * (1 - p) / len(g)))))
    return dict(base=base, rows=rows)


def w52_curve(r, h, nb=8):
    d = r[(r.claim == 'state') & (r.h == h)].dropna(subset=['off_high']).copy()
    d['b'] = pd.qcut(d.off_high, nb, duplicates='drop')
    base = float((d.fwd_ret > 0).mean())
    rows = []
    for b, g in d.groupby('b', observed=True):
        p = float((g.fwd_ret > 0).mean())
        rows.append(dict(mid=float(g.off_high.mean()), n=int(len(g)), up=p,
                         lift=p - base, se=float(np.sqrt(p * (1 - p) / len(g)))))
    return dict(base=base, buckets=rows)


def stability(r, h):
    """Does each family hold in BOTH halves of the fifteen years?"""
    out = {}
    d = r[r.h == h].copy()
    d['o'] = pd.to_datetime(d.origin)
    med = d.o.median()
    for tag, g in (('early', d[d.o <= med]), ('late', d[d.o > med])):
        lv = _paired(g[g.claim == 'level'])
        st = g[g.claim == 'state']
        a = st[st.trend.str.startswith('Trading above the whole')]
        b = st[st.trend.str.startswith('Trading below the whole')]
        v = st.dropna(subset=['atr_pct', 'rlz_vol'])
        out[tag] = dict(
            split_at=str(med.date()),
            levels=lv,
            trend=(float((a.fwd_ret > 0).mean() - (b.fwd_ret > 0).mean())
                   if len(a) > MIN and len(b) > MIN else None),
            tape=float(stats.spearmanr(v.atr_pct, v.rlz_vol)[0]) if len(v) > MIN else None)
    return out


def per_name_tape(r, h):
    d = r[(r.claim == 'state') & (r.h == h)].dropna(subset=['atr_pct', 'rlz_vol'])
    vals = []
    for k, g in d.groupby(['market', 'ticker']):
        if len(g) >= 60:
            vals.append(float(stats.spearmanr(g.atr_pct, g.rlz_vol)[0]))
    return vals


if __name__ == '__main__':
    r = pd.read_pickle('claims_short.pkl')
    lv = r[r.claim == 'level']
    out = dict(meta=dict(rows=int(len(r)), names=int(len(r.groupby(['market', 'ticker']))),
                         origins=int(len(r[(r.claim == 'state') & (r.h == 5)])),
                         first=str(r.origin.min()), last=str(r.origin.max())))
    for h in (5, 10, 21):
        out[f'h{h}'] = dict(
            by_kind=by(lv, 'kind', h),
            by_rank=by(lv, 'rank', h),
            by_touches=by(lv, None, h, buckets=pd.cut(
                lv[(lv.claim == 'level') & (lv.h == h)].touches.fillna(0),
                [-1, 0, 1, 2, 4, 99], labels=['none (MA/round/52w)', '1', '2', '3-4', '5+'])
                if len(lv[(lv.claim == 'level') & (lv.h == h)]) else None),
            by_dist=by(lv, None, h, buckets=pd.cut(
                lv[(lv.claim == 'level') & (lv.h == h)].dist,
                [0, .03, .06, .10, .15, 1], labels=['<3%', '3-6%', '6-10%', '10-15%', '>15%'])),
            rsi=rsi_curve(r, h), atr=atr_curve(r, h), w52=w52_curve(r, h),
            slope200=state_lift(r, h, 'slope200', ['rising', 'flat', 'falling']),
            stability=stability(r, h),
            tape_per_name=per_name_tape(r, h),
        )
    json.dump(out, open('RESULTS_deep.json', 'w'), indent=1, default=float)
    print(f"{out['meta']['rows']:,} rows | {out['meta']['names']} names | "
          f"{out['meta']['origins']:,} origins")
    k = out['h5']['by_kind']
    print('\nLEVEL EDGE BY KIND (h=5) — the module ranks swing above the rest:')
    for kk, v in sorted(k.items(), key=lambda x: -x[1]['effect']):
        print(f"   {kk:14} {v['effect']:+.4f}  n={v['n']:>6,}  z={v['z']:>5.1f}")
