"""AIRARABIA beta — regressed against the index the BINDING beta rule resolves for this
stock's exchange, plus the other UAE market proxy as a published cross-check.

WHICH INDEX IS THE REGRESSOR IS NOT THIS STUDY'S CHOICE. It is resolved by
wacc_builder.market_index_path(market, exchange), the hard gate adopted 10-Aug-2026 and
re-keyed on EXCHANGE the same day. Air Arabia is DFM-listed — stated identically in Note 1
of the FY2025 audited statements, the FY2025 annual report and the Q1-2026 interim, and the
annual report's own share-price chart benchmarks the stock against the DFM general index —
so the exchange passed to the resolver is DFM, never the market code alone ("AE" spans ADX
and DFM, and the resolver REFUSES to resolve an unqualified "AE" for exactly that reason).

For ("AE", "DFM") the resolver returns FTSE ADX General (FADGI) under a registered INTERIM
substitution: no DFM General series is registered in this repo, and the substitution is
empirically the better-supported half — over five years of weekly returns FADGI explains
the six covered DFM names BETTER than it explains the ADX names it actually covers. Any
beta built on an interim substitute MUST quote the note, so the study carries it verbatim.

An earlier edition of this study adopted a Yahoo-sourced DFM General series (DFMGI) as the
regressor on the reasoning that a DFM-listed share should be measured against the DFM
index. That reasoning is right in principle and is what the interim note anticipates
("Replace with a DFM index when one is supplied") — but registering a new regressor is an
amendment to the beta rule, which travels on its own branch with both protocol files in
sync, not something a study silently does to itself. So DFMGI stays in the repo and stays
PUBLISHED here as the cross-check, and the conforming FADGI regression is what the
valuation adopts.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt, market_index_path, index_interim_note

MARKET, EXCHANGE = 'AE', 'DFM'
ADOPTED_PATH = market_index_path(MARKET, EXCHANGE)
INTERIM_NOTE = index_interim_note(MARKET, EXCHANGE)
print(f"resolver -> {os.path.basename(ADOPTED_PATH)} for ({MARKET}, {EXCHANGE})")

def weekly(px):
    return px.resample('W-THU').last().dropna()

stk, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'AIRARABIA_Stock_Price_History.csv')),
                    'AIRARABIA', verbose=False, market='AE')
stk = stk.set_index('Date')['Price']

def regress(index_path, label):
    idx = load_ohlc(index_path).set_index('Date')['Price']
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
               index=label, index_file=os.path.basename(index_path), window_years=5,
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

# ADOPTED — whatever the binding rule resolves for this stock's exchange
out = regress(ADOPTED_PATH, 'FTSE ADX General Index (FADGI)')
assert out['usable'], 'the resolved regressor must clear the usability gate'
out['exchange'] = EXCHANGE
out['interim_note'] = INTERIM_NOTE
out['adopted_reason'] = (
    'Resolved by the binding beta rule: wacc_builder.market_index_path("AE", "DFM") -> '
    'FADGI, an INTERIM substitution registered because no DFM General series is registered '
    'in the repo. The exchange is DFM on primary evidence (FY2025 statements Note 1, FY2025 '
    'annual report, Q1-2026 interim Note 1); the market code alone does not resolve.')

# CROSS-CHECK — the DFM General series held in the repo but not registered as a regressor
alt = regress(os.path.join(HERE, '..', 'raw_indices', 'AE', 'DFMGI.csv'),
              'DFM General Index (DFMGI)')
alt['status'] = ('held in the repo, NOT the registered regressor. Registering it is an '
                 'amendment to the beta rule, which the interim note anticipates; until '
                 'that amendment lands this is a published cross-check, not the basis.')
out['alt_benchmark'] = alt
d = out['beta'] - alt['beta']
out['alt_benchmark']['delta_vs_adopted'] = float(d)
out['alt_benchmark']['inside_adopted_ci90'] = bool(out['ci90'][0] <= alt['beta'] <= out['ci90'][1])
print(f"cross-check: DFMGI beta differs by {d:+.3f}; "
      f"{'INSIDE' if out['alt_benchmark']['inside_adopted_ci90'] else 'OUTSIDE'} "
      f"the adopted 90% interval")

json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
