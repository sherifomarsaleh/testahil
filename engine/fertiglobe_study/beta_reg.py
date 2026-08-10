"""FERTIGLB beta — thin wrapper over the shared, enforced module.

This file used to build its own equal-weight ADX/DFM composite, like every other study in
the repo. It no longer computes anything: the regressor is resolved by
engine/beta_regression.py through wacc_builder.market_index_path(), so this study cannot
point at a basket without deleting that call.

FERTIGLB is ADX-listed, so the regressor is FTSE ADX General (raw_indices/AE/FADGI.csv).
The composite it replaced gave beta 0.492 / R2 6.2%; the real index gives 0.931 / R2 10.0%.

The composite ladder is retained purely as a CROSS-CHECK in the JSON, so a reader can see
the size of the substitution that was corrected — it is not the regressor and never again
feeds the WACC.
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from primitives import load_ohlc                     # noqa: E402
from data_quality import clean_ohlc                  # noqa: E402
import beta_regression as br                         # noqa: E402
from research_protocol import assert_beta_provenance  # noqa: E402

MULT = {'K': 1e3, 'M': 1e6, 'B': 1e9}


def to_num(v):
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(',', '')
    if not s or s in ('-', 'nan'):
        return np.nan
    return float(s[:-1]) * MULT[s[-1]] if s[-1] in MULT else float(s)


def composite_crosscheck():
    """The retired equal-weight composite, kept only to show what was corrected."""
    AE = os.path.join(HERE, '..', 'raw_ohlc', 'AE')
    fg, _ = clean_ohlc(load_ohlc(os.path.join(AE, 'FERTIGLB.csv')), 'FERTIGLB',
                       verbose=False, market='AE')
    fg = fg.set_index('Date').sort_index()['Price']
    cut = fg.index.max() - pd.DateOffset(years=5)
    rets = {}
    for f in sorted(glob.glob(os.path.join(AE, '*.csv'))):
        t = os.path.basename(f)[:-4]
        if t == 'FERTIGLB':
            continue
        d, _ = clean_ohlc(load_ohlc(f), t, verbose=False, market='AE')
        s = d.set_index('Date').sort_index()['Price']
        r = np.log(s[s.index >= cut].resample('W-FRI').last().dropna()).diff().dropna()
        if len(r) >= 100:
            rets[t] = r
    mkt = pd.DataFrame(rets).mean(axis=1, skipna=True)
    y = np.log(fg[fg.index >= cut].resample('W-FRI').last().dropna()).diff().dropna()
    al = pd.concat([y.rename('y'), mkt.rename('m')], axis=1, sort=True).dropna()
    X = np.column_stack([np.ones(len(al)), al['m'].values])
    b, *_ = np.linalg.lstsq(X, al['y'].values, rcond=None)
    resid = al['y'].values - X @ b
    r2 = 1 - float((resid ** 2).sum()) / float(((al['y'].values - al['y'].values.mean()) ** 2).sum())
    return dict(beta=float(b[1]), r2=float(r2), n=len(al), names=len(rets),
                note='RETIRED equal-weight composite — shown only to size the correction')


out = br.own_stock_beta('FERTIGLB', 'AE', 'ADX', dimson=True)
assert_beta_provenance(out)
out['composite_crosscheck_RETIRED'] = composite_crosscheck()
out['naive_index_beta'] = br.own_stock_beta('FERTIGLB', 'AE', 'ADX', dimson=False)['beta']

json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1, default=str)
c = out['composite_crosscheck_RETIRED']
print(f"beta {out['beta']:.3f} | R2 {out['r2']:.3f} | n {out['n']} | SE {out['se']:.3f} | "
      f"CI90 [{out['ci90'][0]:.2f},{out['ci90'][1]:.2f}] | usable={out['usable']}")
print(f"regressor {out['index_file']} as-of {out['index_asof']} | conforming={out['conforming']}")
print(f"retired composite cross-check: beta {c['beta']:.3f} R2 {c['r2']:.3f} "
      f"({c['names']} names) -> the substitution corrected here")
