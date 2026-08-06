"""SWDY beta — tier-1 own-stock weekly regression vs an equal-weight EGX
composite built from the full engine/raw_ohlc/EG library (house pattern:
CLHO/RMDA studies), 5-year window, RegressionBetaAttempt usability gate."""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

def weekly(px):
    return px.resample('W-THU').last().dropna()

swdy, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'SWDY_Stock_Price_History.csv')),
                     'SWDY', verbose=False, market='EG')
swdy = swdy.set_index('Date')['Price']

comp = {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'EG', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='EG')
        comp[tkr] = df.set_index('Date')['Price']
    except Exception as e:
        print('skip', tkr, e)

cut = swdy.index.max() - pd.DateOffset(years=5)
wk_swdy = weekly(swdy[swdy.index >= cut])
rets = {}
for tkr, s in comp.items():
    w = weekly(s[s.index >= cut])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[tkr] = r
R = pd.DataFrame(rets)
mkt = R.mean(axis=1, skipna=True)          # equal-weight composite weekly log-return
re = np.log(wk_swdy / wk_swdy.shift(1)).dropna()
al = pd.concat([re.rename('swdy'), mkt.rename('mkt')], axis=1).dropna()
x, y = al['mkt'].values, al['swdy'].values
n = len(x)
X = np.column_stack([np.ones(n), x])
b, res, *_ = np.linalg.lstsq(X, y, rcond=None)
yhat = X @ b
ss_res = float(((y - yhat) ** 2).sum()); ss_tot = float(((y - y.mean()) ** 2).sum())
r2 = 1 - ss_res / ss_tot
se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
att = RegressionBetaAttempt(beta=float(b[1]), r_squared=r2, n_obs=n,
                            se_beta=se_b, frequency='weekly')
ok, msg = att.is_usable()
ci = (b[1] - 1.645 * se_b, b[1] + 1.645 * se_b)
out = dict(beta=float(b[1]), r2=float(r2), n=n, se=float(se_b),
           ci90=[float(ci[0]), float(ci[1])], usable=bool(ok), gate_msg=msg,
           composite_names=len(rets), window_years=5, frequency='weekly',
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(b[1])),
           warnings=att.interim_warnings())
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}] "
      f"| usable={ok} ({msg}) | composite {len(rets)} names | weak={out['weak']}")
