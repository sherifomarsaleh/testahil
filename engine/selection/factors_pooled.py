"""factors_pooled.py -- pooled EG+AE+SA cohorts and estimators per the Sign-off
Record (items a, c, d) of the SIGNED pre-registration, 27-Jul-2026.

- Anchors: EG reference-calendar grid (identical walkback to the EG pass: 58
  anchors for 252d factors, 41 for F3). Each other market's anchor = its own
  last session at or before the EG anchor date; horizon = the 3-month calendar window on its
  own calendar; resolved-outcome and trailing-history inclusion per name.
- A market joins a cohort only with >=6 admissible names (min-6 per market).
- Pooled cohort IC = Spearman of within-market percentile ranks (rank/(n-1),
  average-rank ties), pooled in market order EG,AE,SA.
- Pooled tercile spread = mean z(top third) - mean z(bottom third), returns
  z-scored within market-cohort, terciles cut on pooled factor percentiles
  (stable sort).
For an EG-only cohort both estimators reduce exactly to the EG pass's.
"""
import numpy as np
import pandas as pd
import pickle
from scipy.stats import spearmanr, rankdata

OUT = '/home/claude/selection'
MARKETS = ['EG', 'AE', 'SA']          # fixed pooling order (Sign-off Record d)
HORIZON = 60
MIN_NAMES = 6
EXPECTED_SIGN = {'F1': 1, 'F2': -1, 'F3': -1, 'F4': 1, 'F5': 1, 'F6': 1}
FACTORS = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']

price, yzvar, vol, logp, cal = {}, {}, {}, {}, {}
for m in MARKETS:
    price[m] = pd.read_pickle(f'{OUT}/{m}_price.pkl')
    yzvar[m] = pd.read_pickle(f'{OUT}/{m}_yzvar.pkl')
    vol[m] = pd.read_pickle(f'{OUT}/{m}_vol.pkl')
    logp[m] = np.log(price[m])
    cal[m] = price[m].index

# --- EG master anchor grids (identical to the EG pass) ---
last = len(cal['EG']) - 1
anchors_f3, anchors_short = [], []
t = last - HORIZON
while t - 1260 >= 0:
    anchors_f3.append(t)
    t -= HORIZON
t = last - HORIZON
while t - 252 >= 0:
    anchors_short.append(t)
    t -= HORIZON
anchors_f3, anchors_short = sorted(anchors_f3), sorted(anchors_short)
print(f'EG master grid: {len(anchors_short)} anchors (252d), {len(anchors_f3)} (F3), '
      f'{cal["EG"][anchors_short[0]].date()} .. {cal["EG"][anchors_short[-1]].date()}')

# --- map each EG anchor date to the other markets' own calendars ---
def map_anchor(m, d):
    """Index of market m's last session at or before date d; None if none or
    if the forward 60-session outcome is unresolved on m's calendar."""
    i = cal[m].searchsorted(d, side='right') - 1
    if i < 0 or i + HORIZON > len(cal[m]) - 1:
        return None
    return int(i)

mapped = {m: {t: (t if m == 'EG' else map_anchor(m, cal['EG'][t]))
              for t in anchors_short} for m in MARKETS}
for m in ['AE', 'SA']:
    ok = [t for t in anchors_short if mapped[m][t] is not None]
    if ok:
        idx = [mapped[m][t] for t in ok]
        steps = np.diff(sorted(idx))
        print(f'{m}: anchor mappable+resolvable at {len(ok)} of {len(anchors_short)} EG anchors '
              f'({cal["EG"][ok[0]].date()} .. {cal["EG"][ok[-1]].date()}); '
              f'own-calendar anchor steps min/max = {steps.min()}/{steps.max()} sessions')

def flat_hl_frac(m, nm, t, window=252):
    w = yzvar[m][nm].iloc[max(0, t - window):t + 1]
    if len(w) == 0:
        return 1.0
    return float(w.isna().mean())

def compute_factor_row(m, fac, t):
    """Per-market factor row at market-local anchor index t. Identical factor
    logic to the EG pass; RAYA exclusion is EG's recorded F4 decision; the
    >20% degenerate-bars guard applies to every name in every market."""
    out = {}
    for nm in price[m].columns:
        p = logp[m][nm]
        if fac == 'F1':
            if t - 252 < 0 or pd.isna(p.iloc[t - 21]) or pd.isna(p.iloc[t - 252]):
                continue
            out[nm] = p.iloc[t - 21] - p.iloc[t - 252]
        elif fac == 'F2':
            if t - 21 < 0 or pd.isna(p.iloc[t]) or pd.isna(p.iloc[t - 21]):
                continue
            out[nm] = p.iloc[t] - p.iloc[t - 21]
        elif fac == 'F3':
            if t - 1260 < 0 or pd.isna(p.iloc[t - 252]) or pd.isna(p.iloc[t - 1260]):
                continue
            out[nm] = p.iloc[t - 252] - p.iloc[t - 1260]
        elif fac == 'F4':
            if m == 'EG' and nm == 'RAYA':
                continue
            if t - 252 < 0:
                continue
            if flat_hl_frac(m, nm, t) > 0.20:
                continue
            w = yzvar[m][nm].iloc[max(0, t - 252):t + 1]
            if w.notna().sum() < 200:
                continue
            out[nm] = -1.0 * w.mean()
        elif fac == 'F5':
            if t - 252 < 0:
                continue
            r = logp[m][nm].diff()
            pv = (price[m][nm] * vol[m][nm])
            w_r = r.iloc[max(0, t - 251):t + 1]
            w_pv = pv.iloc[max(0, t - 251):t + 1]
            amihud_daily = (w_r.abs() / w_pv).replace([np.inf, -np.inf], np.nan)
            if amihud_daily.notna().sum() < 200:
                continue
            out[nm] = amihud_daily.mean()
        elif fac == 'F6':
            if t - 252 < 0:
                continue
            w = price[m][nm].iloc[max(0, t - 252):t + 1]
            if pd.isna(price[m][nm].iloc[t]) or w.notna().sum() < 200:
                continue
            out[nm] = price[m][nm].iloc[t] / w.max()
    return out

def forward_return(m, t):
    fwd = t + HORIZON
    out = {}
    for nm in price[m].columns:
        p0, p1 = price[m][nm].iloc[t], price[m][nm].iloc[fwd]
        if pd.notna(p0) and pd.notna(p1) and p0 > 0 and p1 > 0:
            out[nm] = np.log(p1 / p0)
    return out

def pct_rank(v):
    """Percentile rank in [0,1]: (average rank - 1)/(n-1)."""
    return (rankdata(v, method='average') - 1.0) / (len(v) - 1.0)

def pooled_stats(blocks):
    """blocks: list of (market, names, fac_arr, fwd_arr) in MARKETS order.
    Returns pooled Spearman IC, pooled tercile spread (z-units), per-market IC."""
    fac_pct, ret_pct, ret_z = [], [], []
    per_mkt_ic = {}
    for m, names, fv, rv in blocks:
        fac_pct.append(pct_rank(fv))
        ret_pct.append(pct_rank(rv))
        ret_z.append((rv - rv.mean()) / rv.std(ddof=1))
        per_mkt_ic[m] = float(spearmanr(fv, rv)[0])
    fp = np.concatenate(fac_pct)
    rp = np.concatenate(ret_pct)
    rz = np.concatenate(ret_z)
    ic = float(spearmanr(fp, rp)[0])
    k = len(fp) // 3
    order = np.argsort(fp, kind='stable')
    spread = float(rz[order[-k:]].mean() - rz[order[:k]].mean()) if k >= 1 else np.nan
    return ic, spread, per_mkt_ic

results = {}
for fac in FACTORS:
    grid = anchors_f3 if fac == 'F3' else anchors_short
    rows = []
    for t_eg in grid:
        d = cal['EG'][t_eg]
        blocks, block_store = [], {}
        for m in MARKETS:
            t_m = t_eg if m == 'EG' else map_anchor(m, d)
            if t_m is None:
                continue
            fv = compute_factor_row(m, fac, t_m)
            rv = forward_return(m, t_m)
            names = sorted(set(fv) & set(rv))
            if len(names) < MIN_NAMES:
                continue
            fa = np.array([fv[n] for n in names])
            ra = np.array([rv[n] for n in names])
            blocks.append((m, names, fa, ra))
            block_store[m] = dict(t=t_m, names=names, fac=fa.tolist(), fwd=ra.tolist())
        n_pool = sum(len(b[1]) for b in blocks)
        if n_pool < MIN_NAMES or not blocks:
            continue
        ic, spread, per_mkt = pooled_stats(blocks)
        rows.append(dict(t_eg=t_eg, date=str(d.date()), n_pool=n_pool,
                         markets=[b[0] for b in blocks], blocks=block_store,
                         ic=ic, spread=spread, per_mkt_ic=per_mkt))
    results[fac] = rows
    ics = np.array([r['ic'] for r in rows])
    sps = np.array([r['spread'] for r in rows])
    n_ae = sum(1 for r in rows if 'AE' in r['markets'])
    n_sa = sum(1 for r in rows if 'SA' in r['markets'])
    print(f'{fac}: {len(rows)} pooled cohorts (AE in {n_ae}, SA in {n_sa}); '
          f'mean pooled IC={ics.mean():+.4f}  mean spread={np.nanmean(sps):+.4f} z-units  '
          f'expected sign={EXPECTED_SIGN[fac]:+d}')
    for m in MARKETS:
        mic = [r['per_mkt_ic'][m] for r in rows if m in r['per_mkt_ic']]
        if mic:
            print(f'     {m}: {len(mic)} cohorts, mean within-market IC={np.mean(mic):+.4f}')

with open(f'{OUT}/pooled_results.pkl', 'wb') as f:
    pickle.dump(results, f)
print('\nSaved pooled_results.pkl')
