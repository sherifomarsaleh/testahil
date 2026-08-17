"""AIRARABIA beta — tier-1 own-stock weekly regression vs the stock's OWN local
index, plus a SECOND-BENCHMARK cross-check.

WHICH INDEX IS "OWN" IS A PRIMARY-SOURCE QUESTION, NOT AN INFERENCE. Air Arabia
is Sharjah-domiciled and its investment portfolio holds both DFM- and ADX-listed
securities (FY2025 note 11), so the listing venue has to be read off the filing
rather than assumed from the head office. Every filing states it identically:
"The Company's ordinary shares are listed on the Dubai Financial Market, United
Arab Emirates" — FY2025 statements note 1, the FY2025 annual report, and the
most recent filing (Q1-2026 interim, note 1). The 2025 annual report's own
share-price chart benchmarks AIRARABIA against DFMGI. So the ADOPTED regressor
is the DFM General Index (engine/raw_indices/AE/DFMGI.csv).

The FTSE ADX General Index (engine/raw_indices/AE/ADXGENERAL.csv) is regressed
too, as an ALTERNATIVE-BENCHMARK cross-check on the same window and the same
usability gate. It is NOT adopted — a UAE name's beta against a different
emirate's exchange composite is a robustness read, not its own local index — but
it answers the fair objection that a single-benchmark regression coheres
internally without being externally verified: a second, independently sourced
market proxy either reproduces the beta or does not. Both are published.

The DFMGI feed lags the stock library by ~3 weeks (last index row 16-Jul-2026);
each regression window is truncated to its own overlap, which costs ~3 of ~260
weekly observations against DFMGI, and is flagged rather than papered over.
"""
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

def regress(index_file, label):
    idx = load_ohlc(os.path.join(HERE, '..', 'raw_indices', 'AE', index_file))
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
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
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
               index=label, index_file=index_file, window_years=5,
               frequency='weekly', window_end=str(last_common.date()),
               weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(b[1])),
               warnings=att.interim_warnings())
    # publish the regression series itself so the fit can be re-run by a reader
    out['series'] = [[str(d.date()), float(a), float(c)]
                     for d, a, c in zip(al.index, al['stk'], al['idx'])]
    print(f"{label}: beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} "
          f"| CI90 [{ci[0]:.2f},{ci[1]:.2f}] | usable={ok} ({msg}) "
          f"| to {last_common.date()} | weak={out['weak']}")
    return out

# ADOPTED — the stock's own local index, per the filing
out = regress('DFMGI.csv', 'DFM General Index (DFMGI)')
# CROSS-CHECK — a second, independently sourced UAE market proxy
alt = regress('ADXGENERAL.csv', 'FTSE ADX General Index')
out['alt_benchmark'] = alt
out['adopted_reason'] = (
    'DFM General Index adopted: every filing states the ordinary shares are listed on the '
    'Dubai Financial Market (FY2025 note 1, FY2025 annual report, Q1-2026 interim note 1), '
    'and the annual report benchmarks the share price against DFMGI. The FTSE ADX General '
    'regression is published as an alternative-benchmark cross-check, not as the adopted beta.')
d = out['beta'] - alt['beta']
overlap = (out['ci90'][0] <= alt['beta'] <= out['ci90'][1])
out['alt_benchmark']['delta_vs_adopted'] = float(d)
out['alt_benchmark']['inside_adopted_ci90'] = bool(overlap)
print(f"cross-check: alternative-benchmark beta differs by {d:+.3f}; "
      f"{'INSIDE' if overlap else 'OUTSIDE'} the adopted 90% interval")

json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
