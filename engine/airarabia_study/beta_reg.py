"""AIRARABIA beta — tier-1 own-stock weekly regression vs the stock's OWN local
index, the DFM General Index (engine/raw_indices/AE/DFMGI.csv, downloaded
09-Aug-2026, daily closes 2015 -> 16-Jul-2026), 5-year window,
RegressionBetaAttempt usability gate. AIRARABIA is DFM-listed, so DFMGI is the
correct regressor — a real capitalisation-weighted local index, preferred to
the equal-weight covered-library composite used where no index file exists.
The index feed lags the stock library by ~3 weeks (last index row 16-Jul-2026);
the regression window is truncated to the overlap, which costs 3 of ~260
weekly observations and is flagged rather than papered over."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

def weekly(px):
    return px.resample('W-THU').last().dropna()

stk, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'AIRARABIA_Stock_Price_History.csv')),
                    'AIRARABIA', verbose=False, market='AE')
stk = stk.set_index('Date')['Price']
idx = load_ohlc(os.path.join(HERE, '..', 'raw_indices', 'AE', 'DFMGI.csv'))
idx = idx.set_index('Date')['Price']

last_common = min(stk.index.max(), idx.index.max())
cut = last_common - pd.DateOffset(years=5)
wk_s = weekly(stk[(stk.index >= cut) & (stk.index <= last_common)])
wk_i = weekly(idx[(idx.index >= cut) & (idx.index <= last_common)])
rs = np.log(wk_s / wk_s.shift(1)).dropna()
ri = np.log(wk_i / wk_i.shift(1)).dropna()
al = pd.concat([rs.rename('stk'), ri.rename('idx')], axis=1).dropna()
x, y = al['idx'].values, al['stk'].values
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
           index='DFM General Index (DFMGI)', window_years=5, frequency='weekly',
           window_end=str(last_common.date()),
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(b[1])),
           warnings=att.interim_warnings())
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}] "
      f"| usable={ok} ({msg}) | vs DFMGI to {last_common.date()} | weak={out['weak']}")
