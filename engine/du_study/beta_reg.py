"""DU beta — tier-1 own-stock weekly regression vs its OWN local index, the DFM
General Index (DU is DFM-listed), 5-year window, RegressionBetaAttempt usability
gate. Index series: official DFM API (api2.dfm.ae, 2025-01-02..2026-08-07,
complete) spliced with Yahoo DFMGI.AE (2021-07-01..2024-12-31) — the two agree
EXACTLY (max rel diff ~3e-8) on all 307 overlapping sessions. The pre-2025
segment omits the last session of some DFM weeks, so weekly sampling uses the
LAST COMMON trading date per ISO week on an inner join of stock and index —
never a calendar assumption. Cross-check: the house equal-weight AE composite
(engine/raw_ohlc/AE library, CLHO/RMDA/SWDY pattern) is regressed alongside and
published as the alternative construction.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

IDX_CSV = os.path.join(HERE, 'DFMGI_daily.csv')

du, _ = clean_ohlc(load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'AE', 'DU.csv')),
                   'DU', verbose=False, market='AE')
du = du.set_index('Date')['Price']
idx = pd.read_csv(IDX_CSV, parse_dates=['Date']).set_index('Date')['Close']

cut = du.index.max() - pd.DateOffset(years=5)
both = pd.concat([du.rename('du'), idx.rename('idx')], axis=1).dropna()
both = both[both.index >= cut]

# last common session of each ISO week
wk = both.groupby([both.index.isocalendar().year, both.index.isocalendar().week]).tail(1)
r = np.log(wk / wk.shift(1)).dropna()

def reg(x, y):
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = float(((y - yhat) ** 2).sum()); ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
    return float(b[1]), r2, n, se_b

beta, r2, n, se = reg(r['idx'].values, r['du'].values)
att = RegressionBetaAttempt(beta=beta, r_squared=r2, n_obs=n, se_beta=se, frequency='weekly')
ok, msg = att.is_usable()
ci = (beta - 1.645 * se, beta + 1.645 * se)

# ---- cross-check: equal-weight AE composite (house pattern) -----------------
comp = {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    if tkr == 'DU':
        continue
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='AE')
        comp[tkr] = df.set_index('Date')['Price']
    except Exception as e:
        print('skip', tkr, e)
R = pd.DataFrame({t: np.log(s / s.shift(1)) for t, s in comp.items()})
R = R[R.index >= cut]
mkt_d = R.mean(axis=1, skipna=True)
comp_px = (1 + 0).__class__  # noqa - placeholder removed below
# weekly composite return: sum daily log-returns within the same ISO weeks used above
wk_tag = pd.Series(list(zip(both.index.isocalendar().year, both.index.isocalendar().week)),
                   index=both.index)
mkt_wk = mkt_d.reindex(both.index).groupby(wk_tag).sum(min_count=1).dropna()
du_wk = np.log(wk['du'] / wk['du'].shift(1)).dropna()
du_wk.index = pd.Series(list(zip(du_wk.index.isocalendar().year,
                                 du_wk.index.isocalendar().week)), index=du_wk.index).values
al = pd.concat([pd.Series(du_wk, name='du'), pd.Series(mkt_wk, name='mkt')], axis=1).dropna()
beta_c, r2_c, n_c, se_c = reg(al['mkt'].values.astype(float), al['du'].values.astype(float))

out = dict(beta=beta, r2=r2, n=n, se=se, ci90=[float(ci[0]), float(ci[1])],
           usable=bool(ok), gate_msg=msg, window_years=5, frequency='weekly',
           index='DFM General Index (official DFM API + Yahoo splice, cross-validated)',
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(beta)),
           warnings=att.interim_warnings(),
           composite_alt=dict(beta=beta_c, r2=r2_c, n=n_c, se=se_c,
                              names=len(comp), note='equal-weight AE library composite, '
                              'house cross-check construction'))
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"DFMGI beta {beta:.3f} | R2 {r2:.3f} | n {n} | SE {se:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}]"
      f" | usable={ok} ({msg}) | weak={out['weak']}")
print(f"composite alt beta {beta_c:.3f} | R2 {r2_c:.3f} | n {n_c} | SE {se_c:.3f}")
