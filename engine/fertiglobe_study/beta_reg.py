"""FERTIGLB beta — own-stock weekly regression against an ADX/DFM market composite.

THREE CHANGES OVER THE FIRST CUT (09-Aug-2026), all aimed at accuracy:

1. TURNOVER WEIGHTING. The first cut equal-weighted 17 constituents, which gave
   TWOPOINTZERO the same weight as FAB. A published index is capitalisation-weighted;
   we hold no share counts, but every series carries volume, so traded value
   (price x volume) is available and is far closer to economic weight than 1/N.
   Both weightings are computed and reported.

2. DIMSON (1979) LEAD-LAG CORRECTION. Fertiglobe's free float is ~13% -- the rest is
   held by ADNOC and the former parent. A thinly-floated share does not fully
   incorporate market news within the measurement interval, which biases a naive beta
   DOWNWARD. The Dimson beta sums the coefficients on the market at t-1, t and t+1 and
   is the standard correction. Reporting the naive beta alone would present a
   liquidity artifact as low systematic risk.

3. THE FULL LIBRARY AND THE FULL WINDOW. Every AE name is used, over the longest
   window the listing supports (FERTIGLB listed 27-Oct-2021, so ~4.8 years -- inside
   the 2-5yr tier-1 band).

RESOLVED 10-Aug-2026 -- THE REAL INDEX IS NOW THE REGRESSOR. engine/raw_indices/AE/
FADGI.csv (FTSE ADX General, 2011-01-02 -> 2026-07-24) was supplied and is now the
primary regressor, which is what SIGCM clause 6 actually asks for. The constituent
composite is retained ONLY as a cross-check and is no longer the headline.

Why the composite was worse than "an approximation of the index":
  - It mixed TWO EXCHANGES. The engine's AE library holds ADX names (ADCB, FAB,
    ALDAR, ADNOCGAS) alongside DFM names (EMAAR, DIB, ENBD, SALIK). FERTIGLB is
    ADX-listed, so the correct regressor is an ADX index, not an ADX/DFM mongrel.
  - It covered only the 17 names this engine happens to cover, not the exchange.
  - Equal weighting gave TWOPOINTZERO the same weight as FAB; turnover weighting
    was a proxy for a float-cap scheme the real index applies properly.
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from primitives import load_ohlc                      # noqa: E402
from data_quality import clean_ohlc                   # noqa: E402
from wacc_builder import RegressionBetaAttempt        # noqa: E402

AE = os.path.join(HERE, '..', 'raw_ohlc', 'AE')
MULT = {'K': 1e3, 'M': 1e6, 'B': 1e9}


def to_num(v):
    """'22.72M' -> 22_720_000. Blank/'-' -> nan."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(',', '')
    if not s or s in ('-', 'nan'):
        return np.nan
    return float(s[:-1]) * MULT[s[-1]] if s[-1] in MULT else float(s)


def weekly_last(s):
    return s.resample('W-FRI').last().dropna()


def load(tkr):
    df, _ = clean_ohlc(load_ohlc(os.path.join(AE, f'{tkr}.csv')), tkr,
                       verbose=False, market='AE')
    df = df.set_index('Date')
    df['turnover'] = df['Price'] * df['Vol.'].map(to_num)
    return df


names = sorted(os.path.basename(f)[:-4] for f in glob.glob(os.path.join(AE, '*.csv')))
fg = load('FERTIGLB')
cut = fg.index.max() - pd.DateOffset(years=5)

px, tno = {}, {}
for t in names:
    if t == 'FERTIGLB':
        continue
    d = load(t)
    d = d[d.index >= cut]
    w = weekly_last(d['Price'])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) < 100:                      # too short to carry a weight (LULU)
        continue
    px[t] = r
    tno[t] = d['turnover'].resample('W-FRI').sum().reindex(r.index)

R = pd.DataFrame(px)
T = pd.DataFrame(tno).reindex(R.index)
# weight by the PRIOR week's traded value so the index is not built with hindsight
Wt = T.shift(1)
Wt = Wt.where(R.notna()).div(Wt.where(R.notna()).sum(axis=1), axis=0)

mkt_eq = R.mean(axis=1, skipna=True)
mkt_to = (R * Wt).sum(axis=1, skipna=True).where(Wt.sum(axis=1) > 0)

wk = weekly_last(fg['Price'])
y_all = np.log(wk / wk.shift(1)).dropna()


def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ b
    ssr = float((resid ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    dof = len(y) - X.shape[1]
    XtXi = np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(XtXi) * ssr / dof)
    return b, 1 - ssr / sst, se, dof


def fit(mkt, label, dimson):
    al = pd.concat([y_all.rename('y'), mkt.rename('m')], axis=1).dropna()
    if dimson:
        al['lag'] = al['m'].shift(1)
        al['lead'] = al['m'].shift(-1)
        al = al.dropna()
        X = np.column_stack([np.ones(len(al)), al['lag'], al['m'], al['lead']])
        b, r2, se, dof = ols(al['y'].values, X)
        beta = float(b[1] + b[2] + b[3])
        # var(sum) = sum of the 3x3 covariance block of the slope coefficients
        ssr = float(((al['y'].values - X @ b) ** 2).sum())
        cov = np.linalg.inv(X.T @ X) * ssr / dof
        se_b = float(np.sqrt(cov[1:4, 1:4].sum()))
    else:
        X = np.column_stack([np.ones(len(al)), al['m']])
        b, r2, se, dof = ols(al['y'].values, X)
        beta, se_b = float(b[1]), float(se[1])
    att = RegressionBetaAttempt(beta=beta, r_squared=float(r2), n_obs=len(al),
                                se_beta=se_b, frequency='weekly')
    ok, msg = att.is_usable()
    return dict(label=label, dimson=dimson, beta=beta, r2=float(r2), n=len(al),
                se=se_b, ci90=[beta - 1.645 * se_b, beta + 1.645 * se_b],
                usable=bool(ok), gate_msg=msg,
                window_years=round((al.index.max() - al.index.min()).days / 365.25, 2),
                first_obs=str(al.index.min().date()), last_obs=str(al.index.max().date()))


# THE PUBLISHED LOCAL INDEX -- the SIGCM clause 6 regressor.
IDX = os.path.join(HERE, '..', 'raw_indices', 'AE', 'FADGI.csv')
idx, idx_dq = clean_ohlc(load_ohlc(IDX), 'FADGI', verbose=False, market='AE')
idx = idx.set_index('Date').sort_index()['Price']
idx_wk = weekly_last(idx[idx.index >= cut])
mkt_ix = np.log(idx_wk / idx_wk.shift(1)).dropna()

fits = [fit(mkt_ix, 'FTSE ADX General (published index)', False),
        fit(mkt_ix, 'FTSE ADX General (published index)', True),
        fit(mkt_eq, 'equal-weight composite [cross-check]', False),
        fit(mkt_to, 'turnover-weighted composite [cross-check]', False),
        fit(mkt_eq, 'equal-weight composite [cross-check]', True),
        fit(mkt_to, 'turnover-weighted composite [cross-check]', True)]

# DAILY CROSS-CHECK ONLY. The tier-1 rule is a 2-5yr WEEKLY/monthly regression; a daily
# regression is explicitly NOT one of the tiers. It is run here purely to see whether a
# five-fold increase in observations corroborates the weekly answer, with Dimson +/-5
# lags because daily data is where non-synchronous trading bites hardest. It never feeds
# the WACC.
def daily_fit(weight):
    d_fg = np.log(fg['Price'] / fg['Price'].shift(1)).dropna()
    d = {}
    for t in px:
        s = load(t)['Price']
        s = s[s.index >= cut]
        d[t] = np.log(s / s.shift(1)).dropna()
    Rd = pd.DataFrame(d)
    m = Rd.mean(axis=1, skipna=True) if weight == 'equal' else None
    if m is None:
        Td = pd.DataFrame({t: load(t)['turnover'].reindex(Rd.index) for t in px}).shift(1)
        Td = Td.where(Rd.notna()).div(Td.where(Rd.notna()).sum(axis=1), axis=0)
        m = (Rd * Td).sum(axis=1, skipna=True).where(Td.sum(axis=1) > 0)
    al = pd.concat([d_fg.rename('y'), m.rename('m')], axis=1).dropna()
    cols = [al['m'].shift(k) for k in range(-5, 6)]
    al = pd.concat([al['y']] + cols, axis=1).dropna()
    X = np.column_stack([np.ones(len(al))] + [al.iloc[:, i].values for i in range(1, 12)])
    b, r2, se, dof = ols(al.iloc[:, 0].values, X)
    ssr = float(((al.iloc[:, 0].values - X @ b) ** 2).sum())
    cov = np.linalg.inv(X.T @ X) * ssr / dof
    return dict(label=f'DAILY cross-check ({weight}-weight, Dimson +/-5)',
                beta=float(b[1:].sum()), r2=float(r2), n=len(al),
                se=float(np.sqrt(cov[1:, 1:].sum())), tier='cross-check only, not a tier')


daily = [daily_fit('equal'), daily_fit('turnover')]

# SELECTION under the WACC beta hierarchy. Tier 1 is an own-stock 2-5yr weekly
# regression THAT PASSES the usability gate. The turnover-weighted fits -- the better
# index proxy -- FAIL it (R2 below 5%), so the gate outcome depends on how the composite
# is built. That fragility is reported rather than resolved by picking the construction
# that passes. Among the fits that DO pass, the Dimson form is preferred: it corrects a
# documented downward bias from the ~13% float, and it is also the more conservative
# (higher beta, lower value), so the choice does not flatter the valuation.
# SELECTION. SIGCM clause 6 names the stock's own LOCAL INDEX, so the choice is between
# the two published-index fits only; the composites are cross-checks and cannot be
# selected. Between naive and Dimson, the Dimson form is taken when it is usable: the
# ~13% float means a naive beta understates systematic risk.
idx_fits = [f for f in fits if 'published index' in f['label']]
usable_idx = [f for f in idx_fits if f['usable']]
chosen = (max(usable_idx, key=lambda f: f['beta']) if usable_idx
          else dict(idx_fits[0], tier_fallback=True))
chosen = dict(chosen, selection_note=(
    'tier-1 own-stock weekly regression against the PUBLISHED FTSE ADX General index '
    '(engine/raw_indices/AE/FADGI.csv). The constituent composites are reported as '
    'cross-checks only -- they mixed ADX and DFM names and covered only the 17 names '
    'this engine holds, so they were never the right regressor for an ADX-listed share.'))
out = dict(chosen=chosen, all_fits=fits, daily_crosscheck=daily, constituents=sorted(px),
           constituent_count=len(px), weighting='turnover (price x volume, lagged one week)',
           correction='Dimson (1979) lead-lag, +/-1 week',
           blume_crosscheck=2 / 3 * chosen['beta'] + 1 / 3,
           naive_equal_weight_beta=[f for f in fits if f['label'].startswith('equal') and not f['dimson']][0]['beta'],
           index_file='engine/raw_indices/AE/FADGI.csv (FTSE ADX General)', index_dq=idx_dq,
           index_note='published FTSE ADX General index supplied 10-Aug-2026 and now the regressor',
           free_float_note='~13% free float — a naive beta is biased low by thin trading')
# Mirror the CHOSEN fit's scalars at the top level. compute.py and any other consumer
# reads _beta['beta'] / ['r2'] / ['se'] / ['n'] / ['ci90'] / ['window_years'] directly, and
# nesting them under 'chosen' silently broke that contract -- compute.py died on KeyError.
# The nested detail stays for the ladder; the top level stays the stable interface.
out.update({k: chosen[k] for k in ('beta', 'r2', 'se', 'n', 'ci90', 'window_years',
                                   'usable', 'gate_msg', 'first_obs', 'last_obs')})
out['weak'] = bool(chosen['r2'] < 0.10
                   or (chosen['ci90'][1] - chosen['ci90'][0]) > 2 * abs(chosen['beta']))
out['frequency'] = 'weekly'
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)

print(f'constituents: {len(px)}  ({", ".join(sorted(px))})')
for f in fits:
    tag = 'Dimson' if f['dimson'] else 'naive '
    print(f"  {tag} {f['label']:30s} beta {f['beta']:6.3f}  R2 {f['r2']:.3f}  "
          f"n {f['n']:3d}  SE {f['se']:.3f}  CI90 [{f['ci90'][0]:.2f},{f['ci90'][1]:.2f}]  "
          f"usable={f['usable']}")
print(f"\nCHOSEN: {chosen['label']}, Dimson-corrected -> beta {chosen['beta']:.3f} "
      f"(was {fits[0]['beta']:.3f} equal-weight naive)")
