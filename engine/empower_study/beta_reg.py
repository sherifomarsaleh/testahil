"""EMPOWER beta — own-stock weekly regression vs the FTSE ADX General Index
(FADGI), used as the UAE base market index PER EXPLICIT INSTRUCTION (10-Aug-2026)
in place of the listing exchange's own DFM General Index. The DFMGI regression
is retained as beta_result_dfmgi.json for comparison. Window = full listing
history (16-Nov-2022 IPO -> latest common week, ~3.7y, inside the 2-5y band).
The index is market data, not company historicals; the user-supplied export is
the build source and its 24-Jul-2026 endpoint (two weeks before the study
anchor) is flagged. RegressionBetaAttempt usability gate applied as always."""
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

# FTSE ADX General: user-supplied investing.com export (comma-grouped prices),
# 03-Jan-2011..24-Jul-2026 — ends two weeks before the study anchor; the
# regression window clips to the last common week (flagged in the register).
idx = pd.read_csv(os.path.join(HERE, 'FTSE_ADX_General_Historical_Data.csv'))
idx['Date'] = pd.to_datetime(idx['Date'], format='%m/%d/%Y')
idx['Close'] = idx['Price'].astype(str).str.replace(',', '').astype(float)
idx = idx.sort_values('Date').set_index('Date')['Close'].dropna()

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
           index='FADGI (FTSE ADX General Index), per instruction',
           window=[str(al.index.min().date()), str(al.index.max().date())],
           window_years=round((al.index.max() - al.index.min()).days / 365.25, 2),
           frequency='weekly',
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(b[1])),
           warnings=att.interim_warnings())
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}] "
      f"| usable={ok} ({msg}) | window {out['window']} ({out['window_years']}y) | weak={out['weak']}")
