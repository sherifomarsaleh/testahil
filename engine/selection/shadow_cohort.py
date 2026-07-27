"""shadow_cohort.py -- Shadow Selection Cohort #1: rankings for the five live
factors at the latest possible anchor per market, from the staged full-power
libraries. UNPUBLISHED -- forward evidence only. F5 excluded (retired UNTESTABLE).

Anchor per market = last session of its reference calendar. Factor logic and
admissibility identical to factors_pooled_full.py (RAYA excluded from F4;
>20% degenerate-bars guard everywhere).
"""
import numpy as np
import pandas as pd
from scipy.stats import rankdata

OUT = '/home/claude/fullpower'
MARKETS = ['EG', 'AE', 'SA']
FACTORS = ['F1', 'F2', 'F3', 'F4', 'F6']
EXPECTED_SIGN = {'F1': 1, 'F2': -1, 'F3': -1, 'F4': 1, 'F6': 1}

price, yzvar = {}, {}
for m in MARKETS:
    price[m] = pd.read_pickle(f'{OUT}/{m}_price.pkl')
    yzvar[m] = pd.read_pickle(f'{OUT}/{m}_yzvar.pkl')

def flat_hl_frac(m, nm, t, window=252):
    w = yzvar[m][nm].iloc[max(0, t - window):t + 1]
    return float(w.isna().mean()) if len(w) else 1.0

def factor_row(m, fac, t):
    out = {}
    logp = np.log(price[m])
    for nm in price[m].columns:
        p = logp[nm]
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
            if t - 252 < 0 or flat_hl_frac(m, nm, t) > 0.20:
                continue
            w = yzvar[m][nm].iloc[max(0, t - 252):t + 1]
            if w.notna().sum() < 200:
                continue
            out[nm] = -1.0 * w.mean()
        elif fac == 'F6':
            if t - 252 < 0:
                continue
            w = price[m][nm].iloc[max(0, t - 252):t + 1]
            if pd.isna(price[m][nm].iloc[t]) or w.notna().sum() < 200:
                continue
            out[nm] = price[m][nm].iloc[t] / w.max()
    return out

def pct(v):
    return (rankdata(v, method='average') - 1.0) / (len(v) - 1.0)

for m in MARKETS:
    t = len(price[m]) - 1
    anchor = price[m].index[t].date()
    print(f'### {m} — anchor {anchor} (last session, index {t})')
    tables = {}
    for fac in FACTORS:
        fv = factor_row(m, fac, t)
        if len(fv) < 6:
            print(f'  {fac}: only {len(fv)} admissible names — not scored')
            continue
        names = sorted(fv)
        vals = np.array([fv[n] for n in names])
        pr = pct(vals)
        order = np.argsort(-pr)  # best (highest percentile) first
        tables[fac] = [(names[i], vals[i], pr[i]) for i in order]
    # F6 primary table, full; others compact
    if 'F6' in tables:
        print(f'  F6 (PRIMARY — 52w-high proximity, higher=better), {len(tables["F6"])} names:')
        for nm, v, p_ in tables['F6']:
            print(f'    {nm:14s} F6={v:.4f}  pct={p_:.3f}')
    for fac in ['F1', 'F2', 'F3', 'F4']:
        if fac in tables:
            row = tables[fac]
            top = ', '.join(f'{nm}({p_:.2f})' for nm, v, p_ in row[:5])
            bot = ', '.join(f'{nm}({p_:.2f})' for nm, v, p_ in row[-5:])
            print(f'  {fac}: {len(row)} names | top-5 by factor pct: {top} | bottom-5: {bot}')
    print()
