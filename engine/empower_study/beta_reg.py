"""EMPOWER beta — tier-1 own-stock weekly regression vs the DFM General Index
(DFMGI), the stock's own local index. Window = full listing history
(16-Nov-2022 IPO -> latest common date, ~3.7y, inside the 2-5y band).
Index series: DFMGI.AE daily closes (Yahoo Finance chart API pull,
scratchpad/dfmgi_daily.csv committed alongside as dfmgi_daily.csv) — the index
is market data, not company historicals, so SIGCM clause 1 is not implicated;
the series' ~20% missing-session sparsity is flagged in the bibliography and
absorbed by the weekly resample (last observation in each Mon-Fri week).
RegressionBetaAttempt usability gate applied as everywhere else."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

def weekly(px):
    # DFM trades Mon-Fri (since Jan-2022): week closes Friday
    return px.resample('W-FRI').last().dropna()

emp, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'EMPOWER_Stock_Price_History.csv')),
                    'EMPOWER', verbose=False, market='AE')
emp = emp.set_index('Date')['Price']

idx = pd.read_csv(os.path.join(HERE, 'dfmgi_daily.csv'), parse_dates=['Date'])
idx = idx.set_index('Date')['Close'].astype(float).dropna()

wk_e, wk_m = weekly(emp), weekly(idx)
re = np.log(wk_e / wk_e.shift(1)).dropna()
rm = np.log(wk_m / wk_m.shift(1)).dropna()
al = pd.concat([re.rename('emp'), rm.rename('mkt')], axis=1).dropna()
x, y = al['mkt'].values, al['emp'].values
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
           index='DFMGI (DFM General Index)',
           window=[str(al.index.min().date()), str(al.index.max().date())],
           window_years=round((al.index.max() - al.index.min()).days / 365.25, 2),
           frequency='weekly',
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(b[1])),
           warnings=att.interim_warnings())
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}] "
      f"| usable={ok} ({msg}) | window {out['window']} ({out['window_years']}y) | weak={out['weak']}")
