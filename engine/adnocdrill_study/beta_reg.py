"""ADNOCDRILL beta — own-stock weekly regression against the FTSE ADX General Index.

Beta hierarchy (standing rule): the first tier is a 2-5 year own-stock weekly
regression against the stock's OWN local index, taken whenever that much usable
history exists and it clears the usability gate (n>=24, R^2>=5%, SE(beta)<|beta|).
ADNOC Drilling listed in October 2021, so a full five-year window is available at
the August 2026 anchor and the first tier applies — no peer beta is needed.

THE LOCAL INDEX. engine/raw_indices/AE/ADXGENERAL.csv is the FTSE ADX General
Index, the headline index of the exchange the stock actually trades on. It is the
correct regressor for an Abu Dhabi name, exactly as the EGX30 is for an Egyptian
one, and it supersedes the equal-weight library composite this study previously
used as its primary. The composite is retained below as a robustness check
rather than discarded, because the difference between the two is itself
information: an equal-weight average of eighteen names under-weights the
mega-caps the published index is concentrated in, so if the two betas disagree,
the disagreement is about index construction and the reader should see it.

AS-OF GAP, FLAGGED. The index series ends 2026-07-24 and the price series ends
2026-08-07, so the regression's overlap ends at the index's last full week. That
is two weeks short of the valuation anchor. It is immaterial for a five-year
weekly regression — it drops two of roughly 250 observations — but it is stated
here and in the study rather than passed over, per the standing rule that a beta
quoted from this library carries its as-of date.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

INDEX_PATH = os.path.join(HERE, '..', 'raw_indices', 'AE', 'ADXGENERAL.csv')
INDEX_NAME = 'FTSE ADX General Index'


def weekly(px):
    return px.resample('W-FRI').last().dropna()


def monthly(px):
    return px.resample('ME').last().dropna()


def regress(y, x):
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
    return float(b[1]), float(b[0]), r2, se_b, n


def run(stock_px, index_px, resample, years, last):
    cut = last - pd.DateOffset(years=years)
    a = resample(stock_px[stock_px.index >= cut])
    b = resample(index_px[index_px.index >= cut])
    ra = np.log(a / a.shift(1)).dropna()
    rb = np.log(b / b.shift(1)).dropna()
    al = pd.concat([ra.rename('y'), rb.rename('x')], axis=1).dropna()
    beta, alpha, r2, se, n = regress(al['y'].values, al['x'].values)
    return dict(beta=beta, alpha=alpha, r2=r2, se=se, n=n,
                first=str(al.index.min().date()), last=str(al.index.max().date()))


# ---- the stock ---------------------------------------------------------------
tgt, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'ADNOCDRILL_Stock_Price_History.csv')),
                    'ADNOCDRILL', verbose=False, market='AE')
tgt = tgt.set_index('Date')['Price']

# ---- the index ---------------------------------------------------------------
# Screened before use exactly as a price series is: no blank prices, no duplicate
# dates, no single-session move beyond what the exchange's daily limit allows,
# and a trading-day density consistent with the real Abu Dhabi calendar.
idx_raw = load_ohlc(INDEX_PATH)
assert idx_raw['Price'].isna().sum() == 0, 'the index series carries blank prices'
assert idx_raw['Date'].duplicated().sum() == 0, 'the index series carries duplicate dates'
idx_lr = np.diff(np.log(idx_raw['Price'].values))
assert np.abs(idx_lr).max() < 0.2114, 'a single-session index move exceeds the exchange limit'
density = {int(y): int(n) for y, n in idx_raw['Date'].dt.year.value_counts().sort_index().items()
           if 2021 <= y <= 2025}
assert all(230 <= n <= 260 for n in density.values()), ('index trading-day density is not '
                                                        f'consistent with the ADX calendar: '
                                                        f'{density}')
idx = idx_raw.set_index('Date')['Price']

last_common = min(tgt.index.max(), idx.index.max())
gap_days = int((tgt.index.max() - idx.index.max()).days)

# ---- PRIMARY: five-year weekly against the published index -------------------
P = run(tgt, idx, weekly, 5, last_common)
att = RegressionBetaAttempt(beta=P['beta'], r_squared=P['r2'], n_obs=P['n'],
                            se_beta=P['se'], frequency='weekly')
ok, msg = att.is_usable()
ci = (P['beta'] - 1.645 * P['se'], P['beta'] + 1.645 * P['se'])

out = dict(
    beta=P['beta'], alpha_weekly=P['alpha'], r2=P['r2'], n=P['n'], se=P['se'],
    ci90=[float(ci[0]), float(ci[1])], usable=bool(ok), gate_msg=msg,
    regressor=INDEX_NAME, regressor_file='engine/raw_indices/AE/ADXGENERAL.csv',
    regressor_span=[str(idx.index.min().date()), str(idx.index.max().date())],
    regressor_rows=int(len(idx_raw)), regressor_density=density,
    window_years=5, frequency='weekly',
    first_week=P['first'], last_week=P['last'],
    index_asof=str(idx.index.max().date()), price_asof=str(tgt.index.max().date()),
    asof_gap_days=gap_days,
    weak=bool(P['r2'] < 0.10 or (ci[1] - ci[0]) > 2 * abs(P['beta'])),
    warnings=att.interim_warnings(), robustness={})

# ---- ROBUSTNESS 1: shorter and longer windows, same regressor ----------------
for yrs in (2, 3, 4):
    r = run(tgt, idx, weekly, yrs, last_common)
    out['robustness'][f'weekly_{yrs}yr_vs_index'] = r

# ---- ROBUSTNESS 2: monthly frequency, same regressor -------------------------
out['robustness']['monthly_5yr_vs_index'] = run(tgt, idx, monthly, 5, last_common)

# ---- ROBUSTNESS 3: the equal-weight library composite (the previous primary) --
comp, turnover = {}, {}
for f in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    tkr = os.path.basename(f)[:-4]
    if tkr == 'ADNOCDRILL':
        continue
    try:
        df, _ = clean_ohlc(load_ohlc(f), tkr, verbose=False, market='AE')
        comp[tkr] = df.set_index('Date')['Price']
        if 'Vol.' in df.columns:
            v = (df['Vol.'].astype(str).str.strip().str.upper()
                 .replace({'': None, 'NAN': None, '-': None}))
            mult = v.str[-1].map({'K': 1e3, 'M': 1e6, 'B': 1e9})
            num = pd.to_numeric(v.str.rstrip('KMB'), errors='coerce') * mult.fillna(1.0)
            tv = (num * df['Price']).tail(260).median()
            if pd.notna(tv) and tv > 0:
                turnover[tkr] = float(tv)
    except Exception as e:
        print('skip', tkr, e)

cut = last_common - pd.DateOffset(years=5)
wk_t = weekly(tgt[tgt.index >= cut])
re_t = np.log(wk_t / wk_t.shift(1)).dropna()
rets = {}
for tkr, s in comp.items():
    w = weekly(s[s.index >= cut])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[tkr] = r
R = pd.DataFrame(rets)
for label, series in (('equal_weight_composite', R.mean(axis=1, skipna=True)),):
    al = pd.concat([re_t.rename('y'), series.rename('x')], axis=1).dropna()
    b_, a_, r2_, se_, n_ = regress(al['y'].values, al['x'].values)
    out['robustness'][f'weekly_5yr_vs_{label}'] = dict(beta=b_, r2=r2_, se=se_, n=n_,
                                                       names=len(rets))
wts = pd.Series({k: turnover.get(k, np.nan) for k in R.columns}).dropna()
if len(wts) >= 8:
    wts = wts / wts.sum()
    sub = R[wts.index]
    vw = (sub * wts).sum(axis=1, skipna=True) / (sub.notna() * wts).sum(axis=1)
    al = pd.concat([re_t.rename('y'), vw.rename('x')], axis=1).dropna()
    b_, a_, r2_, se_, n_ = regress(al['y'].values, al['x'].values)
    out['robustness']['weekly_5yr_vs_turnover_weighted_composite'] = dict(
        beta=b_, r2=r2_, se=se_, n=n_, names=int(len(wts)))

# ---- how well the composite tracked the published index ----------------------
al = pd.concat([R.mean(axis=1, skipna=True).rename('comp'),
                np.log(weekly(idx[idx.index >= cut]) /
                       weekly(idx[idx.index >= cut]).shift(1)).dropna().rename('idx')],
               axis=1).dropna()
out['composite_vs_index_correlation'] = float(al['comp'].corr(al['idx']))

json.dump(out, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"PRIMARY — {INDEX_NAME}, 5yr weekly")
print(f"  beta {P['beta']:.3f} | R2 {P['r2']:.3f} | n {P['n']} | SE {P['se']:.3f} "
      f"| CI90 [{ci[0]:.2f},{ci[1]:.2f}] | usable={ok} ({msg}) | weak={out['weak']}")
print(f"  overlap {P['first']} .. {P['last']} | index as of {out['index_asof']}, "
      f"prices as of {out['price_asof']} ({gap_days}-day gap, flagged)")
print('ROBUSTNESS')
for k, v in out['robustness'].items():
    print(f"  {k:44s} beta {v['beta']:.3f}  R2 {v['r2']:.3f}  n {v['n']}  SE {v['se']:.3f}")
print(f"  composite-to-index weekly correlation {out['composite_vs_index_correlation']:.3f}")
