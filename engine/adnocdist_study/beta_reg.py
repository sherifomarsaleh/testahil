"""ADNOCDIST beta — tier-1 own-stock weekly regression against its OWN local
market, 5-year window, RegressionBetaAttempt usability gate.

House pattern (CLHO/RMDA/PHAR studies): the engine carries no ADX index series,
so the local market return is an equal-weight composite built from the
engine/raw_ohlc/AE library. ADNOCDIST is ADX-listed, so the PRIMARY composite is
ADX-only — a Dubai Financial Market name is a different exchange and does not
belong in an ADX name's local index. The all-UAE composite (ADX + DFM) is run as
a cross-check, and both are reported.

The subject is inside its own composite, which is how a real published index
behaves, but it biases the coefficient toward one by the subject's own weight —
so the ex-subject regression is run as well and both are reported.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

# Exchange assignment for the AE library. ADNOCDIST lists on ADX, so the ADX-only
# composite is the local index; DFM names are the cross-check leg.
ADX = {'ADCB', 'ADIB', 'ADNOCDIST', 'ADNOCGAS', 'AGTHIA', 'ALDAR', 'ALPHADHABI',
       'BURJEEL', 'EAND', 'FAB', 'IHC', 'LULU', 'TWOPOINTZERO'}
DFM = {'DEWA', 'DIB', 'EMAAR', 'EMAARDEV', 'ENBD', 'SALIK'}

SUBJ = 'ADNOCDIST'


def weekly(px):
    # ADX/DFM trade Monday-Friday since the Jan-2022 workweek switch; W-FRI is the
    # week close for the whole post-break sample.
    return px.resample('W-FRI').last().dropna()


subj, _ = clean_ohlc(load_ohlc(os.path.join(HERE, f'{SUBJ}_Stock_Price_History.csv')),
                     SUBJ, verbose=False, market='AE')
subj = subj.set_index('Date')['Price']

comp = {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='AE')
        comp[tkr] = df.set_index('Date')['Price']
    except Exception as e:
        print('skip', tkr, e)

cut = subj.index.max() - pd.DateOffset(years=5)
wk_subj = weekly(subj[subj.index >= cut])
re_ = np.log(wk_subj / wk_subj.shift(1)).dropna()

rets = {}
for tkr, s in comp.items():
    w = weekly(s[s.index >= cut])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[tkr] = r
R = pd.DataFrame(rets)


def reg(mkt, label):
    al = pd.concat([re_.rename('y'), mkt.rename('x')], axis=1).dropna()
    x, y = al['x'].values, al['y'].values
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
    att = RegressionBetaAttempt(beta=float(b[1]), r_squared=r2, n_obs=n,
                                se_beta=se_b, frequency='weekly')
    ok, msg = att.is_usable()
    out = dict(label=label, beta=float(b[1]), alpha=float(b[0]), r2=float(r2), n=int(n),
               se=float(se_b), ci90=[float(b[1] - 1.645 * se_b), float(b[1] + 1.645 * se_b)],
               usable=bool(ok), gate_msg=msg,
               warnings=att.interim_warnings())
    print(f"[{label}] beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} "
          f"| CI90 [{out['ci90'][0]:.2f},{out['ci90'][1]:.2f}] | usable={ok} ({msg})")
    return out


adx_names = sorted([c for c in R.columns if c in ADX])
adx_ex = [c for c in adx_names if c != SUBJ]
all_names = sorted(R.columns)
all_ex = [c for c in all_names if c != SUBJ]

res = dict(
    primary=reg(R[adx_names].mean(axis=1, skipna=True), 'ADX composite (incl. subject)'),
    primary_ex_subject=reg(R[adx_ex].mean(axis=1, skipna=True), 'ADX composite (ex-subject)'),
    crosscheck_all_uae=reg(R[all_names].mean(axis=1, skipna=True), 'All-UAE composite (incl. subject)'),
    crosscheck_all_uae_ex=reg(R[all_ex].mean(axis=1, skipna=True), 'All-UAE composite (ex-subject)'),
)
res['constituents_adx'] = adx_ex
res['constituents_all'] = all_ex
res['window_years'] = 5
res['frequency'] = 'weekly (W-FRI)'
res['first_week'] = str(re_.index.min().date())
res['last_week'] = str(re_.index.max().date())
res['chosen'] = 'primary_ex_subject'
res['chosen_rationale'] = (
    'ADX-only composite excluding the subject: ADNOCDIST lists on ADX, so the local '
    'index is ADX; excluding the subject removes the mechanical pull of its own weight '
    'toward beta = 1.')
b = res['primary_ex_subject']
res['weak'] = bool(b['r2'] < 0.10 or (b['ci90'][1] - b['ci90'][0]) > 2 * abs(b['beta']))
json.dump(res, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"\nCHOSEN: {res['chosen']} beta {b['beta']:.3f} (R2 {b['r2']:.3f}, n {b['n']}) "
      f"| weak={res['weak']}")
print(f"window {res['first_week']} .. {res['last_week']} | ADX composite {len(adx_ex)} names")
