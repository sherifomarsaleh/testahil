"""f5_forensics.py -- per-name volume forensic pass for F5 (Amihud).

For every EG name (queue order = worst first), inventory every >50x / <1/50x
jump day vs the trailing 20d median and classify:

  SHIFT  -- sustained level change: trailing-20d median AFTER the day differs
            from BEFORE by >10x (or <1/10) and persists -> unit/scale break.
            Amihud is silently wrong across the break. Fatal unless segmented.
  SPIKE  -- one-off day; level reverts (after/before within [1/3, 3]) -> real
            trading burst (news, block trade). Legitimate data.
  AMBIG  -- neither clean spike nor clean shift.

Also checks the vendor-suffix hypothesis: raw 'Vol.' string on the jump day vs
the modal suffix in the surrounding 40 sessions (a bare number or K in an M
neighbourhood is a suffix drop, i.e. data error, not trading).

Split check: same-day |log price move| > 25% alongside a volume jump suggests
an unadjusted corporate action rather than trading.
"""
import sys
sys.path.insert(0, '/home/claude/repo/engine')
import numpy as np
import pandas as pd

RAW = '/home/claude/fullpower/raw_ohlc/AE'
NAMES = ['ADCB','ADIB','ADNOCGAS','AGTHIA','ALDAR','ALPHADHABI','BURJEEL','DEWA','DIB',
         'EAND','EMAAR','EMAARDEV','ENBD','FAB','IHC','LULU','SALIK','TWOPOINTZERO']


def load(nm):
    df = pd.read_csv(f'{RAW}/{nm}.csv')
    df.columns = [c.replace('﻿', '').strip() for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.sort_values('Date').reset_index(drop=True)
    df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(',', ''), errors='coerce')
    return df


def parse_vol(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if s in ('', '-', 'nan', 'None'):
        return np.nan
    mult = 1.0
    if s and s[-1] in ('M', 'K', 'B'):
        mult = {'K': 1e3, 'M': 1e6, 'B': 1e9}[s[-1]]
        s = s[:-1]
    try:
        return float(s.replace(',', '')) * mult
    except ValueError:
        return np.nan


def suffix_of(s):
    s = str(s).strip()
    return s[-1] if s and s[-1] in ('M', 'K', 'B') else '#'


summary = []
detail = {}
for nm in NAMES:
    df = load(nm)
    vol = df['Vol.'].apply(parse_vol)
    vv = vol.replace(0, np.nan)
    n_zero = int((vol == 0).sum())
    med20 = vv.rolling(20, min_periods=10).median()
    ratio = vv / med20
    jump_idx = np.where((ratio > 50) | (ratio < 1 / 50))[0]
    lr = np.log(df['Price']).diff().abs()

    rows = []
    n_shift = n_spike = n_ambig = n_suffix = n_corp = 0
    for i in jump_idx:
        before = vv.iloc[max(0, i - 20):i].median()
        after = vv.iloc[i + 1:i + 21].median()
        shift_f = after / before if (before and before > 0 and after and after > 0) else np.nan
        if pd.notna(shift_f) and (shift_f > 10 or shift_f < 0.1):
            klass = 'SHIFT'
            n_shift += 1
        elif pd.notna(shift_f) and (1 / 3 <= shift_f <= 3):
            klass = 'SPIKE'
            n_spike += 1
        else:
            klass = 'AMBIG'
            n_ambig += 1
        # suffix anomaly: this day's suffix differs from the modal suffix around it
        lo, hi = max(0, i - 20), min(len(df), i + 21)
        neigh = df['Vol.'].iloc[lo:hi].apply(suffix_of)
        modal = neigh.mode().iloc[0] if len(neigh.mode()) else '?'
        sfx = suffix_of(df['Vol.'].iloc[i])
        sfx_anom = sfx != modal
        n_suffix += int(sfx_anom)
        corp = bool(pd.notna(lr.iloc[i]) and lr.iloc[i] > 0.25)
        n_corp += int(corp)
        rows.append((str(df['Date'].iloc[i].date()), str(df['Vol.'].iloc[i]).strip(),
                     float(ratio.iloc[i]), float(shift_f) if pd.notna(shift_f) else np.nan,
                     klass, sfx, modal, sfx_anom, corp))
    detail[nm] = rows
    # segment view: how much of the series sits at a shifted level?
    verdict = ('CLEAN' if len(jump_idx) == 0 else
               'SPIKES-ONLY' if n_shift == 0 and n_ambig <= max(2, len(jump_idx) // 10) else
               'UNIT-BREAKS' if n_shift > 0 else 'AMBIGUOUS')
    summary.append((nm, len(df), n_zero, float(vv.isna().mean()), len(jump_idx),
                    n_shift, n_spike, n_ambig, n_suffix, n_corp, verdict))

print(f"{'Name':6s} {'rows':>5s} {'zero':>4s} {'naV':>5s} {'jumps':>5s} {'SHIFT':>5s} "
      f"{'SPIKE':>5s} {'AMBIG':>5s} {'sfx?':>4s} {'corp?':>5s}  verdict")
for r in sorted(summary, key=lambda x: -x[4]):
    print(f'{r[0]:6s} {r[1]:5d} {r[2]:4d} {r[3]:5.1%} {r[4]:5d} {r[5]:5d} {r[6]:5d} '
          f'{r[7]:5d} {r[8]:4d} {r[9]:5d}  {r[10]}')

import pickle
with open('/home/claude/selection/f5_forensics_ae.pkl', 'wb') as f:
    pickle.dump(dict(summary=summary, detail=detail), f)
print('\nSaved f5_forensics_ae.pkl')
