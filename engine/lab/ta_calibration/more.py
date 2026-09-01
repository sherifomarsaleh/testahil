"""more.py — the cuts added for the third edition, plus the named episodes.

Same discipline as every other results file: the register resolves its numbers
from HERE at build time, so nothing in the document is typed. The episodes are
real rows selected by stated criteria — a level that held on a flagship name, a
trigger that fired and fizzled, a fresh golden cross that dropped — with their
dates and prices carried verbatim so the demonstration charts and the lesson
text cannot drift apart.
"""
import json, os
import numpy as np, pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
r = pd.read_pickle(os.path.join(HERE, 'claims_short.pkl'))
lv = r[(r.claim == 'level') & (r.n_sides == 2)]
st = r[r.claim == 'state']

out = {}

# --- support vs resistance ----------------------------------------------------
side = {}
for h in (5, 10, 21):
    side[h] = {}
    for sd in ('res', 'sup'):
        d = lv[(lv.h == h) & (lv.side == sd)]
        b = d[d.touched & d.p_touched].dropna(subset=['p_broke'])
        x = (b.p_broke - b.broke.astype(float))
        side[h][sd] = dict(effect=float(x.mean()), n=int(len(b)),
                           z=float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))))
out['side'] = side

# --- how often a level is even reached ---------------------------------------
touch = {}
for h in (5, 10, 21):
    d = lv[lv.h == h]
    touch[h] = dict(nearest=float(d[d['rank'] == 1].touched.mean()),
                    any_rung=float(d.groupby(['market', 'ticker', 'origin', 'h'])
                                   .touched.max().mean()),
                    n=int(len(d)))
out['touch'] = touch

# --- the tilted coin ----------------------------------------------------------
coin = {}
for h in (5, 21):
    d = st[st.h == h]
    coin[h] = dict(pooled=float((d.fwd_ret > 0).mean()),
                   n=int(len(d)),
                   by_market={m: dict(up=float((g.fwd_ret > 0).mean()), n=int(len(g)))
                              for m, g in d.groupby('market') if len(g) > 1000})
out['coin'] = coin

# --- IHC, the most readable single stock -------------------------------------
ihc = st[(st.h == 21) & (st.ticker == 'IHC')].dropna(subset=['atr_pct', 'rlz_vol'])
out['ihc'] = dict(n=int(len(ihc)),
                  rho=float(stats.spearmanr(ihc.atr_pct, ihc.rlz_vol)[0]))
for t in ('SALIK', 'LULU'):
    d = st[(st.h == 5) & (st.ticker == t)]
    out[f'young_{t}'] = int(d.origin.nunique())

# --- the named episodes, selected by stated criteria --------------------------
def row(d):
    x = d.iloc[0]
    return dict(market=x.market, ticker=x.ticker, origin=x.origin,
                origin_idx=int(x.origin_idx), spot=float(x.spot),
                level=float(x.level), fwd_ret=float(x.fwd_ret),
                far=(float(x.spot * (1 + x.p_touch_dist))
                     if x.claim == 'trigger' else None),
                cross_ago=(int(x.cross_ago) if pd.notna(x.cross_ago) else None))

# the most recent nearest-resistance on a flagship name that was reached and
# held. NOTE the astype(bool): broke is object dtype here, and a bare ~ on an
# object True/False column returns -2/-1 — both truthy — so it filters NOTHING.
# The first scan for this episode made exactly that mistake and confidently
# offered a row where the level had in fact been broken.
FLAGSHIP = ['COMI', 'EMAAR', 'FAB', 'ALRAJHI', 'RAJHI', 'SABIC', 'ETEL', 'ADCB',
            'QNB', 'EAND', 'ARAMCO', 'TMGH', 'SWDY', 'MAADEN', 'DIB', 'SNB']
c = lv[(lv.h == 21) & (lv['rank'] == 1) & (lv.side == 'res') & lv.touched
       & (~lv.broke.astype(bool)) & lv.ticker.isin(FLAGSHIP)].sort_values('origin')
# The first pick (ADCB, Mar-2026) was correct but told a muddled story: price had
# crashed THROUGH the level from above days before the read, so on the chart the
# 'resistance' reads as debris from the fall. A demonstration should look like
# what it demonstrates, so one more condition: the level must have been OVERHEAD
# for the whole month before the read — every close in the prior 21 sessions
# below it. Approach from below, touch, rejection.
import sys as _s, os as _o
_s.path.insert(0, _o.path.abspath(_o.path.join(HERE, '..', '..')))
from strike_cohorts import load_clean
def _clean_approach(x):
    df, _ = load_clean(x.market, x.ticker)
    i = int(x.origin_idx)
    prior = df['Price'].astype(float).iloc[max(0, i - 21):i + 1]
    return bool((prior < x.level).all())
picked = None
for _, x in c.iloc[::-1].iterrows():
    if _clean_approach(x):
        picked = x
        break
out['ep_level'] = row(pd.DataFrame([picked]))

# a trigger on ETEL that fired and whose far zone never opened, most recent
t = r[(r.claim == 'trigger') & (r.h == 21) & (r.side == 'res') & r.touched
      & (r.broke == False) & (r.ticker == 'ETEL')].sort_values('origin')
out['ep_trigger'] = row(t.tail(1))

# a fresh golden cross on SABIC followed by a clearly lower close
g = st[(st.h == 21) & (st.cross_kind == 'golden') & (st.cross_ago <= 25)
       & (st.fwd_ret < -0.05) & (st.ticker == 'SABIC')].sort_values('origin')
x = g.tail(1).iloc[0]
out['ep_cross'] = dict(market=x.market, ticker=x.ticker, origin=x.origin,
                       origin_idx=int(x.origin_idx), cross_ago=int(x.cross_ago),
                       fwd_ret=float(x.fwd_ret))

# EMAAR's own 52-week pattern, quoted with its noise
d = st[(st.h == 21) & (st.ticker == 'EMAAR')].dropna(subset=['off_high'])
near, far = d[d.off_high <= 0.05], d[d.off_high >= 0.30]
out['ep_w52'] = dict(ticker='EMAAR', near_up=float((near.fwd_ret > 0).mean()),
                     n_near=int(len(near)), far_up=float((far.fwd_ret > 0).mean()),
                     n_far=int(len(far)))

json.dump(out, open(os.path.join(HERE, 'RESULTS_more.json'), 'w'), indent=1)
print('episodes chosen:')
for k in ('ep_level', 'ep_trigger', 'ep_cross'):
    print(' ', k, {kk: vv for kk, vv in out[k].items() if kk != 'origin_idx'})
print('touch nearest h5/h21:', f"{out['touch'][5]['nearest']*100:.1f}% /",
      f"{out['touch'][21]['nearest']*100:.1f}%",
      '| any rung h5:', f"{out['touch'][5]['any_rung']*100:.1f}%")
