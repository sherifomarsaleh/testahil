"""ADNOCDRILL beta — tier-1 own-stock weekly regression against an equal-weight
ADX/DFM composite built from the full engine/raw_ohlc/AE library.

Beta hierarchy (standing rule): tier 1 is a 2-5 year own-stock weekly regression
against the stock's OWN local index, taken whenever that much usable history
exists and it clears the RegressionBetaAttempt gate (n>=24, R^2>=5%,
SE(beta)<|beta|). ADNOC Drilling listed in October 2021, so a full 5-year window
is available as of the August 2026 anchor and tier 1 applies — no peer-beta
fallback is needed.

THE LOCAL INDEX. engine/raw_indices/ carries no AE index file, so the composite
is built the same way the house has built it for every other market that lacks
one: an equal-weight average of weekly log returns across the entire committed
AE price library. That library is the 18-name calibration panel, which spans the
banks, the developers, the utilities and the two large holding companies — the
same names that dominate the published ADX indices. An equal-weight composite is
NOT the FTSE ADX General Index: it under-weights the mega-caps that index is
concentrated in. The consequence is reported rather than hidden — the regression
is re-run against a cap-proxy-weighted composite as a robustness check, and both
betas are carried into the cost-of-capital sensitivity.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt


def weekly(px):
    return px.resample('W-FRI').last().dropna()


def regress(y, x):
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
    return float(b[1]), float(b[0]), r2, se_b, n


tgt, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'ADNOCDRILL_Stock_Price_History.csv')),
                    'ADNOCDRILL', verbose=False, market='AE')
tgt = tgt.set_index('Date')['Price']

comp, turnover = {}, {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    if tkr == 'ADNOCDRILL':
        continue
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='AE')
        comp[tkr] = df.set_index('Date')['Price']
        # traded value proxy for the cap-proxy-weighted robustness composite.
        # "Vol." arrives as a display string ("9.48M", "64.31K") and is parsed here.
        if 'Vol.' in df.columns:
            v = (df['Vol.'].astype(str).str.strip().str.upper()
                 .replace({'': None, 'NAN': None, '-': None}))
            mult = v.str[-1].map({'K': 1e3, 'M': 1e6, 'B': 1e9})
            num = pd.to_numeric(v.str.rstrip('KMB'), errors='coerce') * mult.fillna(1.0)
            tv = (num * df['Price']).tail(260).median()
            if pd.notna(tv) and tv > 0:
                turnover[tkr] = float(tv)
    except Exception as e:
        print('skip', tkr, e)

cut = tgt.index.max() - pd.DateOffset(years=5)
wk_t = weekly(tgt[tgt.index >= cut])
rets = {}
for tkr, s in comp.items():
    w = weekly(s[s.index >= cut])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[tkr] = r
R = pd.DataFrame(rets)
mkt_ew = R.mean(axis=1, skipna=True)

wts = pd.Series({k: turnover.get(k, np.nan) for k in R.columns}).dropna()
mkt_vw = None
if len(wts) >= 8:
    wts = wts / wts.sum()
    sub = R[wts.index]
    mkt_vw = (sub * wts).sum(axis=1, skipna=True) / (sub.notna() * wts).sum(axis=1)

re_t = np.log(wk_t / wk_t.shift(1)).dropna()
al = pd.concat([re_t.rename('tgt'), mkt_ew.rename('mkt')], axis=1).dropna()
beta, alpha, r2, se, n = regress(al['tgt'].values, al['mkt'].values)
att = RegressionBetaAttempt(beta=beta, r_squared=r2, n_obs=n, se_beta=se, frequency='weekly')
ok, msg = att.is_usable()
ci = (beta - 1.645 * se, beta + 1.645 * se)

out = dict(beta=beta, alpha_weekly=alpha, r2=r2, n=n, se=se,
           ci90=[float(ci[0]), float(ci[1])], usable=bool(ok), gate_msg=msg,
           composite_names=len(rets), composite_list=sorted(rets),
           window_years=5, frequency='weekly',
           first_week=str(al.index.min().date()), last_week=str(al.index.max().date()),
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(beta)),
           warnings=att.interim_warnings())

if mkt_vw is not None:
    al2 = pd.concat([re_t.rename('tgt'), mkt_vw.rename('mkt')], axis=1).dropna()
    b2, a2, r22, se2, n2 = regress(al2['tgt'].values, al2['mkt'].values)
    out['robustness_turnover_weighted'] = dict(beta=b2, r2=r22, n=n2, se=se2,
                                               names=int(len(wts)))

# 2-year window, the short end of the tier-1 range, as a stability check
cut2 = tgt.index.max() - pd.DateOffset(years=2)
al3 = al[al.index >= cut2]
if len(al3) >= 24:
    b3, a3, r23, se3, n3 = regress(al3['tgt'].values, al3['mkt'].values)
    out['robustness_2yr_window'] = dict(beta=b3, r2=r23, n=n3, se=se3)

json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"beta {beta:.3f} | R2 {r2:.3f} | n {n} | SE {se:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}] "
      f"| usable={ok} ({msg}) | composite {len(rets)} names | weak={out['weak']}")
for k in ('robustness_turnover_weighted', 'robustness_2yr_window'):
    if k in out:
        d = out[k]
        print(f"  {k}: beta {d['beta']:.3f} R2 {d['r2']:.3f} n {d['n']} SE {d['se']:.3f}")
