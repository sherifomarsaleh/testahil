"""ADNOCDIST beta — tier-1 own-stock weekly regression against its OWN local index.

CHANGED 09-Aug-2026: the local index is now the REAL published one. Earlier editions of
this study regressed against an equal-weight composite built from the AE price library,
because the engine carried no ADX index series — the house pattern when a market's index
is missing. The FTSE ADX General Index has since been added at
engine/raw_indices/AE/ADXGENERAL.csv, so the composite is demoted to a cross-check and the
published index becomes the primary regressor. That is what the beta rule actually asks
for: a stock's beta comes from its own price history against its own local index, the way
EGX30 is the regressor for an EGX name.

The published index INCLUDES the subject, which is what a real index does, and that biases
the coefficient toward one by the subject's own weight. That bias is not removable from a
published index — you cannot un-include a constituent from a number someone else computed —
so it is reported rather than corrected, and the ex-subject composite is run alongside it as
the check on how much it matters.

Both the index and the composite are resampled to Friday week-ends. The Sunday-to-Thursday
workweek that ADX ran until January 2022 is handled by that resampling rather than assumed
away: a week bucket ending Friday contains whatever days actually traded, so the pre-switch
weeks take their Thursday close and the post-switch weeks their Friday one, consistently on
both sides of the regression.
"""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from wacc_builder import RegressionBetaAttempt

ADX = {'ADCB', 'ADIB', 'ADNOCDIST', 'ADNOCGAS', 'AGTHIA', 'ALDAR', 'ALPHADHABI',
       'BURJEEL', 'EAND', 'FAB', 'IHC', 'LULU', 'TWOPOINTZERO'}
SUBJ = 'ADNOCDIST'
INDEX_CSV = os.path.join(HERE, '..', 'raw_indices', 'AE', 'ADXGENERAL.csv')
INDEX_NAME = 'FTSE ADX General Index'


def weekly(px):
    return px.resample('W-FRI').last().dropna()


subj, _ = clean_ohlc(load_ohlc(os.path.join(HERE, f'{SUBJ}_Stock_Price_History.csv')),
                     SUBJ, verbose=False, market='AE')
subj = subj.set_index('Date')['Price']

# The index is NOT run through clean_ohlc. That gate repairs a series by asking whether a
# move is larger than one session can physically produce under the exchange's own daily
# price limit — a test about corporate actions in a single stock. An index has no daily
# limit and no corporate actions, so the gate has nothing to say about it. It is screened
# on its own terms instead: continuity, duplication, and whether the trading-day pattern
# matches the exchange calendar either side of the workweek change.
idx_raw = load_ohlc(INDEX_CSV)
assert idx_raw['Date'].duplicated().sum() == 0, 'duplicate dates in the index series'
assert idx_raw['Date'].is_monotonic_increasing, 'index series is not in date order'
assert (idx_raw['Price'] > 0).all(), 'non-positive index level'
idx = idx_raw.set_index('Date')['Price']
_ir = np.log(idx).diff().dropna()
assert _ir.abs().max() < 0.15, 'implausible single-session index move'

# The index series ends before the price series. Anchor the window on the LAST DATE BOTH
# CARRY so the regression is not quietly extended with weeks only one side has.
last_common = min(subj.index.max(), idx.index.max())
cut = last_common - pd.DateOffset(years=5)
print(f'price series to {subj.index.max().date()}, index series to {idx.index.max().date()}'
      f' -> regression window {cut.date()} .. {last_common.date()}')

wk_subj = weekly(subj[(subj.index >= cut) & (subj.index <= last_common)])
re_ = np.log(wk_subj / wk_subj.shift(1)).dropna()
wk_idx = weekly(idx[(idx.index >= cut) & (idx.index <= last_common)])
ri_ = np.log(wk_idx / wk_idx.shift(1)).dropna()

comp = {}
for fpath in sorted(glob.glob(os.path.join(HERE, '..', 'raw_ohlc', 'AE', '*.csv'))):
    tkr = os.path.basename(fpath)[:-4]
    try:
        df, _ = clean_ohlc(load_ohlc(fpath), tkr, verbose=False, market='AE')
        comp[tkr] = df.set_index('Date')['Price']
    except Exception as e:
        print('skip', tkr, e)

rets = {}
for tkr, s in comp.items():
    w = weekly(s[(s.index >= cut) & (s.index <= last_common)])
    r = np.log(w / w.shift(1)).dropna()
    if len(r) >= 100:
        rets[tkr] = r
R = pd.DataFrame(rets)


def reg(mkt, label):
    al = pd.concat([re_.rename('y'), mkt.rename('x')], axis=1).dropna()
    x, y = al['x'].values, al['y'].values
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot
    se_b = float(np.sqrt(ss_res / (n - 2) / ((x - x.mean()) ** 2).sum()))
    att = RegressionBetaAttempt(beta=float(b[1]), r_squared=r2, n_obs=n,
                                se_beta=se_b, frequency='weekly')
    ok, msg = att.is_usable()
    out = dict(label=label, beta=float(b[1]), alpha=float(b[0]), r2=float(r2), n=int(n),
               se=float(se_b), ci90=[float(b[1] - 1.645 * se_b), float(b[1] + 1.645 * se_b)],
               usable=bool(ok), gate_msg=msg, warnings=att.interim_warnings())
    print(f"[{label}] beta {b[1]:.3f} | R2 {r2:.3f} | n {n} | SE {se_b:.3f} "
          f"| CI90 [{out['ci90'][0]:.2f},{out['ci90'][1]:.2f}] | usable={ok} ({msg})")
    return out


adx_names = sorted([c for c in R.columns if c in ADX])
adx_ex = [c for c in adx_names if c != SUBJ]
all_ex = [c for c in sorted(R.columns) if c != SUBJ]

res = dict(
    primary=reg(ri_, f'{INDEX_NAME} (published, includes the subject)'),
    crosscheck_adx_composite_ex=reg(R[adx_ex].mean(axis=1, skipna=True),
                                    'Equal-weight ADX composite (ex-subject)'),
    crosscheck_adx_composite=reg(R[adx_names].mean(axis=1, skipna=True),
                                 'Equal-weight ADX composite (incl. subject)'),
    crosscheck_all_uae_ex=reg(R[all_ex].mean(axis=1, skipna=True),
                              'Equal-weight all-UAE composite (ex-subject)'),
)
res['index_file'] = 'engine/raw_indices/AE/ADXGENERAL.csv'
res['index_name'] = INDEX_NAME
res['index_span'] = [str(idx.index.min().date()), str(idx.index.max().date())]
res['index_rows'] = int(len(idx))
res['constituents_adx'] = adx_ex
res['constituents_all'] = all_ex
res['window_years'] = 5
res['frequency'] = 'weekly (W-FRI)'
res['first_week'] = str(re_.index.min().date())
res['last_week'] = str(re_.index.max().date())
res['price_series_end'] = str(subj.index.max().date())
res['index_series_end'] = str(idx.index.max().date())
res['chosen'] = 'primary'
res['chosen_rationale'] = (
    f'The published {INDEX_NAME} is the local index for an ADX-listed share, and the beta '
    'rule takes a stock\'s own history against its own local index ahead of any '
    'constructed proxy. It includes the subject, as a published index must; the '
    'equal-weight composite excluding the subject is reported alongside it to show how '
    'much that inclusion moves the coefficient.')
b = res['primary']
res['weak'] = bool(b['r2'] < 0.10 or (b['ci90'][1] - b['ci90'][0]) > 2 * abs(b['beta']))
res['index_vs_composite_delta'] = float(b['beta'] - res['crosscheck_adx_composite_ex']['beta'])
json.dump(res, open(os.path.join(HERE, 'beta_result.json'), 'w'), indent=1)
print(f"\nCHOSEN: {res['chosen']} beta {b['beta']:.4f} (R2 {b['r2']:.3f}, n {b['n']}) "
      f"| weak={res['weak']}")
print(f"window {res['first_week']} .. {res['last_week']}")
print(f"vs the equal-weight composite this study used before: "
      f"{res['index_vs_composite_delta']:+.4f}")
