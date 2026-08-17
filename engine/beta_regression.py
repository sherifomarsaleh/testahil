"""beta_regression.py — the ONE way a study may produce a regression beta.

[ADDED 10-Aug-2026] Every study in this repo used to carry its own `beta_reg.py`, and
every one of them built an equal-weight composite of the covered names because the CLHO
precedent did and each study copied the last. Measured on FERTIGLB, that understated beta
by ~40% (0.492 against 0.931 on the real index) and overstated fair value by 21.6%.

Writing the rule down did not stop it: `wacc_builder.market_index_path()` raises for an
unregistered index, but nothing forced a study to CALL it. Eight study-local scripts went
on building baskets and passing every gate. This module closes that hole -- it resolves
the regressor itself, so a study cannot regress against anything else without deleting
the call, which a reviewer can see.

WHAT IT GUARANTEES
  - the regressor is the published index of the stock's own EXCHANGE, via wacc_builder
  - both series pass Step 0.0 before a single return is computed
  - the weekly grid matches the exchange's real trading week (Gulf/Egypt Sun-Thu -> W-THU,
    UAE post-2022 and the rest Mon-Fri -> W-FRI); a mismatched grid silently drops
    observations and biases the fit
  - the returned record carries its own provenance: index file, index as-of, the
    interim-substitution note if one applies, and the full usability diagnostics
"""
import os
from typing import Optional

import numpy as np
import pandas as pd

from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt, market_index_path, index_interim_note

# The exchange's real trading week. Egypt and the Gulf ex-UAE run Sunday-Thursday, so a
# Friday grid lands on a non-trading day and resamples badly. The UAE moved to Monday-
# Friday in January 2022 (the same workweek switch the AE calibration break is filtered on).
WEEK_END = {'EG': 'W-THU', 'SA': 'W-THU', 'QA': 'W-THU',
            'AE': 'W-FRI', 'IN': 'W-FRI', 'KR': 'W-FRI', 'US': 'W-FRI'}


def _weekly_logret(px: pd.Series, rule: str) -> pd.Series:
    return np.log(px.resample(rule).last().dropna()).diff().dropna()


def _ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ b
    ssr = float((resid ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    dof = len(y) - X.shape[1]
    cov = np.linalg.inv(X.T @ X) * ssr / dof
    return b, 1 - ssr / sst, cov, dof


def own_stock_beta(ticker: str, market: str, exchange: str,
                   series_path: Optional[str] = None, years: int = 5,
                   dimson: bool = True, root: Optional[str] = None) -> dict:
    """Tier-1 own-stock weekly beta against the exchange's PUBLISHED index.

    Raises rather than falling back if the index is not registered or not present --
    the study must stop and ask, exactly as SIGCM requires for missing primary financials.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    root = root or here
    idx_path = market_index_path(market, exchange)          # raises if unregistered/missing
    interim = index_interim_note(market, exchange)

    stock_path = series_path or os.path.join(root, 'raw_ohlc', market, f'{ticker}.csv')
    if not os.path.exists(stock_path):
        raise FileNotFoundError(f'no price series for {ticker} at {stock_path}')

    s, s_dq = clean_ohlc(load_ohlc(stock_path), ticker, verbose=False, market=market)
    i, i_dq = clean_ohlc(load_ohlc(idx_path), os.path.basename(idx_path)[:-4],
                         verbose=False, market=market)
    s = s.set_index('Date').sort_index()['Price']
    i = i.set_index('Date').sort_index()['Price']

    rule = WEEK_END.get(market, 'W-FRI')
    cut = s.index.max() - pd.DateOffset(years=years)
    sy = _weekly_logret(s[s.index >= cut], rule)
    ix = _weekly_logret(i[i.index >= cut], rule)

    al = pd.concat([sy.rename('y'), ix.rename('m')], axis=1, sort=True).dropna()
    if dimson:
        al = al.assign(lag=al['m'].shift(1), lead=al['m'].shift(-1)).dropna()
        X = np.column_stack([np.ones(len(al)), al['lag'], al['m'], al['lead']])
        b, r2, cov, dof = _ols(al['y'].values, X)
        beta = float(b[1:4].sum())
        se = float(np.sqrt(cov[1:4, 1:4].sum()))
    else:
        X = np.column_stack([np.ones(len(al)), al['m']])
        b, r2, cov, dof = _ols(al['y'].values, X)
        beta, se = float(b[1]), float(np.sqrt(cov[1, 1]))

    att = RegressionBetaAttempt(beta=beta, r_squared=float(r2), n_obs=len(al),
                                se_beta=se, frequency='weekly')
    ok, msg = att.is_usable()
    ci = [beta - 1.645 * se, beta + 1.645 * se]
    return dict(
        ticker=ticker, market=market, exchange=exchange,
        beta=beta, r2=float(r2), se=se, n=len(al), ci90=ci,
        usable=bool(ok), gate_msg=msg, dimson=bool(dimson), frequency='weekly',
        weak=bool(r2 < 0.10 or (ci[1] - ci[0]) > 2 * abs(beta)),
        warnings=att.interim_warnings(),
        window_years=round((al.index.max() - al.index.min()).days / 365.25, 2),
        first_obs=str(al.index.min().date()), last_obs=str(al.index.max().date()),
        blume_crosscheck=2 / 3 * beta + 1 / 3,
        # provenance — a beta is not quotable without it
        index_file=os.path.relpath(idx_path, root), index_asof=str(i.index.max().date()),
        index_dq=i_dq, stock_dq=s_dq, week_rule=rule, interim_note=interim,
        conforming=bool(interim is None),
    )
