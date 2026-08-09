"""FERTIGLB beta — tier-1 own-stock weekly regression against an equal-weight ADX/DFM
composite built from the full engine/raw_ohlc/AE library (house pattern: CLHO / RMDA /
SWDY studies), longest window up to 5 years, RegressionBetaAttempt usability gate.

FERTIGLB listed 27-Oct-2021, so the available window is 4.8 years -- inside the 2-5yr
tier-1 band, so this is a tier-1 beta, not a stopgap."""
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


fg, _ = clean_ohlc(load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'AE', 'FERTIGLB.csv')),
                   'FERTIGLB', verbose=False, market='AE')
fg = fg.set_index('Date')['Price']

comp = {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    if tkr == 'FERTIGLB':
        continue
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='AE')
        comp[tkr] = df.set_index('Date')['Price']
    except Exception as e:
        print('skip', tkr, e)

cut = fg.index.max() - pd.DateOffset(years=5)
wk_fg = weekly(fg[fg.index >= cut])
rets = {}
for tkr, s in comp.items():
    w = weekly(s[s.index >= cut])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[tkr] = r
R = pd.DataFrame(rets)
mkt = R.mean(axis=1, skipna=True)
re_ = np.log(wk_fg / wk_fg.shift(1)).dropna()
al = pd.concat([re_.rename('fg'), mkt.rename('mkt')], axis=1).dropna()
x, y = al['mkt'].values, al['fg'].values
n = len(x)
X = np.column_stack([np.ones(n), x])
b, *_ = np.linalg.lstsq(X, y, rcond=None)
yhat = X @ b
ss_res = float(((y - yhat) ** 2).sum())
ss_tot = float(((y - y.mean()) ** 2).sum())
r2 = 1 - ss_res / ss_tot
se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
att = RegressionBetaAttempt(beta=float(b[1]), r_squared=r2, n_obs=n, se_beta=se_b,
                            frequency='weekly')
ok, msg = att.is_usable()
ci = (b[1] - 1.645 * se_b, b[1] + 1.645 * se_b)
# Blume adjustment shown as a cross-check only; the raw regression beta is what the
# WACC uses (house rule: tier-1 own-stock regression, no smoothing toward 1.0).
blume = 2.0 / 3.0 * float(b[1]) + 1.0 / 3.0
out = dict(beta=float(b[1]), r2=float(r2), n=n, se=float(se_b),
           ci90=[float(ci[0]), float(ci[1])], usable=bool(ok), gate_msg=msg,
           composite_names=len(rets), composite_list=sorted(rets),
           window_years=round(float((al.index.max() - al.index.min()).days / 365.25), 2),
           frequency='weekly', blume_crosscheck=float(blume),
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(b[1])),
           warnings=att.interim_warnings(),
           first_obs=str(al.index.min().date()), last_obs=str(al.index.max().date()))
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}] "
      f"| usable={ok} ({msg}) | composite {len(rets)} names | window {out['window_years']}yr "
      f"| weak={out['weak']} | Blume x-check {blume:.3f}")
