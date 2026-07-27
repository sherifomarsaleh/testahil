"""build_cohorts_pooled.py -- pooled EG+AE+SA panel build for the SIGNED
pre-registered test (Selection_Engine_PreRegistration_v1, signed 27-Jul-2026).

Implements Sign-off Record items (b) and (f): per-market Step 0.0 gate
(data_quality.clean_ohlc with per-market limit threshold), per-market
majority-quorum reference calendar (EG >=15/30, AE >=9/18, SA >=6/11),
ffill limit 3, and the >50x volume-unit screen on every series.

Identical load/clean/screen logic to the EG pass's build_cohorts.py --
verified to reproduce the EG exploratory numbers exactly before this
generalisation was trusted.
"""
import sys
sys.path.insert(0, '/home/claude/repo/engine')
import numpy as np
import pandas as pd
from data_quality import clean_ohlc
from mc_v2 import yz_variance_proxy

RAW_BASE = '/home/claude/repo/engine/raw_ohlc'
OUT = '/home/claude/selection'
HORIZON = 60
FFILL_LIMIT = 3

UNIVERSE = {
    'EG': ['ABUK','ADIB','BTFH','CCAP','CLHO','COMI','DSCW','EFID','EFIH','EGAL','EMFD',
           'ETEL','FWRY','GBCO','HELI','HRHO','ISPH','JUFO','KABO','LCSW','OCDI','OIH',
           'ORAS','ORHD','ORWE','PHDC','PRDC','RAYA','RMDA','TMGH'],
    'AE': ['ADCB','ADIB','ADNOCGAS','AGTHIA','ALDAR','ALPHADHABI','BURJEEL','DEWA','DIB',
           'EAND','EMAAR','EMAARDEV','ENBD','FAB','IHC','LULU','SALIK','TWOPOINTZERO'],
    'SA': ['ACWA','ALINMA','ARAMCO','ELM','EXTRA','MAADEN','RAJHI','RIBL','SABIC','SNB','STC'],
}
QUORUM = {'EG': 15, 'AE': 9, 'SA': 6}   # majority of panel size, per Sign-off Record (b)


def load_clean(market, name):
    df = pd.read_csv(f'{RAW_BASE}/{market}/{name}.csv')
    df.columns = [c.replace('﻿', '').strip() for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.sort_values('Date').reset_index(drop=True)
    for c in ['Price', 'Open', 'High', 'Low']:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', ''), errors='coerce')
    df, log = clean_ohlc(df, ticker=name, verbose=False, market=market)
    return df, log


def parse_vol(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if s in ('', '-', 'nan', 'None'):
        return np.nan
    mult = 1.0
    if s[-1] in ('M', 'K', 'B'):
        mult = {'K': 1e3, 'M': 1e6, 'B': 1e9}[s[-1]]
        s = s[:-1]
    try:
        return float(s.replace(',', '')) * mult
    except ValueError:
        return np.nan


for market, names in UNIVERSE.items():
    series = {}
    vol_screen = []
    n_gate_notes = 0
    for nm in names:
        df, log = load_clean(market, nm)
        v = yz_variance_proxy(df)
        vol = df['Vol.'].apply(parse_vol) if 'Vol.' in df.columns else pd.Series(np.nan, index=df.index)
        s = pd.DataFrame({'Price': df['Price'].values, 'YZvar': v.values, 'Vol': vol.values},
                         index=pd.DatetimeIndex(df['Date']))
        series[nm] = s
        vv = vol.replace(0, np.nan)
        med20 = vv.rolling(20, min_periods=10).median()
        ratio = vv / med20
        n_flag = int(((ratio > 50) | (ratio < 1 / 50)).sum())
        vol_screen.append((nm, n_flag, len(df), float(vv.isna().mean())))
        n_gate_notes += len(log) if log else 0

    print(f'\n=== {market}: volume-unit screen (>50x / <1/50x vs trailing 20d median) ===')
    n_flagged = 0
    for nm, n_flag, n_rows, na_frac in vol_screen:
        flag = '  <-- FLAG' if n_flag > 5 else ''
        n_flagged += 1 if n_flag > 5 else 0
        print(f'  {nm:14s} rows={n_rows:5d}  na_vol={na_frac:5.1%}  jump_days={n_flag}{flag}')
    print(f'  [{market}] Step 0.0 gate notes: {n_gate_notes}; volume-flagged names: '
          f'{n_flagged}/{len(names)}')

    all_dates = sorted(set().union(*[set(s.index) for s in series.values()]))
    counts = pd.Series(0, index=pd.DatetimeIndex(all_dates))
    for s in series.values():
        counts.loc[s.index] += 1
    cal = counts[counts >= QUORUM[market]].index.sort_values()
    print(f'  [{market}] reference calendar (quorum >={QUORUM[market]}/{len(names)}): '
          f'{len(cal)} sessions, {cal[0].date()} .. {cal[-1].date()}')

    R = {}
    for nm, s in series.items():
        r = s.reindex(cal)
        r['Price'] = r['Price'].ffill(limit=FFILL_LIMIT)
        r['Vol'] = r['Vol'].ffill(limit=FFILL_LIMIT)
        R[nm] = r

    pd.DataFrame({nm: R[nm]['Price'] for nm in names}).to_pickle(f'{OUT}/{market}_price.pkl')
    pd.DataFrame({nm: R[nm]['YZvar'] for nm in names}).to_pickle(f'{OUT}/{market}_yzvar.pkl')
    pd.DataFrame({nm: R[nm]['Vol'] for nm in names}).to_pickle(f'{OUT}/{market}_vol.pkl')
    print(f'  [{market}] saved matrices: {len(cal)} x {len(names)}')
