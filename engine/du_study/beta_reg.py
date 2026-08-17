"""DU beta — own-stock weekly regression vs the FTSE ADX General Index, adopted
per explicit user instruction (10-Aug-2026 session) as the base market index for
the UAE. DU is DFM-listed, so the house own-local-index default would be the DFM
General; the AE calibration panel itself spans ADX and DFM as one market, which
is the economic basis for a UAE-wide index choice. BOTH constructions are run
and published — ADX as primary (instructed), DFM General and the equal-weight
AE-library composite as the disclosed alternatives — so the choice is priced,
not hidden.

Index sources: FTSE ADX General daily history (user-supplied export,
2011-01-02..2026-07-24); DFM General from the official DFM API spliced with
cross-validated Yahoo history (identical closes on all 307 overlapping
sessions). Weekly sampling uses the LAST COMMON trading date per ISO week on an
inner join of stock and index — never a calendar assumption.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

du, _ = clean_ohlc(load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'AE', 'DU.csv')),
                   'DU', verbose=False, market='AE')
du = du.set_index('Date')['Price']
cut = du.index.max() - pd.DateOffset(years=5)

def reg(x, y):
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = float(((y - yhat) ** 2).sum()); ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
    return float(b[1]), r2, n, se_b

def weekly_beta(idx_csv):
    idx = pd.read_csv(idx_csv, parse_dates=['Date']).set_index('Date')['Close']
    both = pd.concat([du.rename('du'), idx.rename('idx')], axis=1, sort=True).dropna()
    both = both[both.index >= cut]
    wk = both.groupby([both.index.isocalendar().year, both.index.isocalendar().week]).tail(1)
    r = np.log(wk / wk.shift(1)).dropna()
    return reg(r['idx'].values, r['du'].values), both

(beta, r2, n, se), both_adx = weekly_beta(os.path.join(HERE, 'ADXGI_daily.csv'))
att = RegressionBetaAttempt(beta=beta, r_squared=r2, n_obs=n, se_beta=se, frequency='weekly')
ok, msg = att.is_usable()
ci = (beta - 1.645 * se, beta + 1.645 * se)

(beta_d, r2_d, n_d, se_d), _ = weekly_beta(os.path.join(HERE, 'DFMGI_daily.csv'))

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
wk = both_adx.groupby([both_adx.index.isocalendar().year,
                       both_adx.index.isocalendar().week]).tail(1)
wk_tag = pd.Series(list(zip(both_adx.index.isocalendar().year,
                            both_adx.index.isocalendar().week)), index=both_adx.index)
mkt_wk = mkt_d.reindex(both_adx.index).groupby(wk_tag).sum(min_count=1).dropna()
du_wk = np.log(wk['du'] / wk['du'].shift(1)).dropna()
du_wk.index = pd.Series(list(zip(du_wk.index.isocalendar().year,
                                 du_wk.index.isocalendar().week)), index=du_wk.index).values
al = pd.concat([pd.Series(du_wk, name='du'), pd.Series(mkt_wk, name='mkt')], axis=1).dropna()
beta_c, r2_c, n_c, se_c = reg(al['mkt'].values.astype(float), al['du'].values.astype(float))

out = dict(beta=beta, r2=r2, n=n, se=se, ci90=[float(ci[0]), float(ci[1])],
           usable=bool(ok), gate_msg=msg, window_years=5, frequency='weekly',
           index='FTSE ADX General (user-supplied export, adopted per instruction as the '
                 'UAE base market index; series to 24-Jul-2026)',
           weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(beta)),
           warnings=att.interim_warnings(),
           dfm_alt=dict(beta=beta_d, r2=r2_d, n=n_d, se=se_d,
                        note='DFM General Index (DU\'s own listing venue) — the house '
                             'own-local-index default, published as the alternative'),
           composite_alt=dict(beta=beta_c, r2=r2_c, n=n_c, se=se_c,
                              names=len(comp), note='equal-weight AE library composite, '
                              'house cross-check construction'))
json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"ADX beta {beta:.3f} | R2 {r2:.3f} | n {n} | SE {se:.3f} | CI90 [{ci[0]:.2f},{ci[1]:.2f}]"
      f" | usable={ok} ({msg}) | weak={out['weak']}")
print(f"DFMGI alt beta {beta_d:.3f} | R2 {r2_d:.3f} | n {n_d} | SE {se_d:.3f}")
print(f"composite alt beta {beta_c:.3f} | R2 {r2_c:.3f} | n {n_c} | SE {se_c:.3f}")
