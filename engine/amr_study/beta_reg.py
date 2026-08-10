"""AMR — equity beta from the stock's OWN price history against a local index.

Beta hierarchy (house rule, strict preference order):
  (1) own-stock 2-5yr WEEKLY regression vs its OWN local index, usability gate
      n>=24, R^2>=5%, SE(beta) < |beta|;
  (2) same-country peer beta (median unlevered, re-levered);
  (3) beta = 1.0.

SOURCING NOTE (recorded, not hidden). Americana is CONCURRENTLY DUAL-LISTED:
ADX (AMR, AED) and the Saudi Exchange (6015, SAR), same shares, both home
markets, both currencies hard-pegged to the US dollar. A daily history for the
FTSE ADX General Index could not be obtained from any machine-readable source
reachable this session (Yahoo carries the FADGI.FGI quote but returns a single
observation with no timeseries; stooq and investing.com's data endpoints are
JavaScript-walled or return 403; adx.ae returns 403 and its data service
rejected every route probed). The Saudi Exchange line and the Tadawul All Share
Index ARE both available as full daily series, so the tier-(1) regression is run
there: the company's own shares against the index of a market in which those
same shares are listed. Two independent cross-checks are computed and reported
alongside — a UAE-listed consumer-peer beta from the local price library, and
the ADX line regressed on an equal-weighted composite of the covered UAE panel
(a CONSTRUCTED proxy, never presented as the index).
"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc

WEEKLY_RULE = 'W-THU'   # Gulf trading week ends Thursday historically; W-FRI post-2022


def _yahoo_series(path):
    d = json.load(open(os.path.join(HERE, path)))
    r = d['chart']['result'][0]
    ts = r['timestamp']
    close = r['indicators']['quote'][0]['close']
    df = pd.DataFrame({'Date': [pd.Timestamp(time.strftime('%Y-%m-%d', time.gmtime(t))) for t in ts],
                       'Close': close}).dropna()
    return df.sort_values('Date').reset_index(drop=True)


def _weekly_logret(df, col='Close'):
    s = df.set_index('Date')[col].resample('W-FRI').last().dropna()
    return np.log(s / s.shift(1)).dropna()


def regress(y, x, label):
    j = pd.concat([y.rename('y'), x.rename('x')], axis=1).dropna()
    n = len(j)
    if n < 3:
        return dict(label=label, n=n, usable=False, reason='too few overlapping observations')
    X = np.column_stack([np.ones(n), j['x'].values])
    coef, *_ = np.linalg.lstsq(X, j['y'].values, rcond=None)
    resid = j['y'].values - X @ coef
    dof = n - 2
    s2 = float(resid @ resid / dof)
    xtx_inv = np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(xtx_inv) * s2)
    ss_tot = float(((j['y'].values - j['y'].values.mean()) ** 2).sum())
    r2 = 1 - float(resid @ resid) / ss_tot if ss_tot > 0 else float('nan')
    beta, se_b = float(coef[1]), float(se[1])
    gate = dict(n_ge_24=bool(n >= 24), r2_ge_5pct=bool(r2 >= 0.05), se_lt_abs_beta=bool(se_b < abs(beta)))
    return dict(label=label, n=int(n), alpha=float(coef[0]), beta=beta, se_beta=se_b,
                t_beta=float(beta / se_b) if se_b else float('nan'), r2=float(r2),
                first=str(j.index[0].date()), last=str(j.index[-1].date()),
                gate=gate, usable=bool(all(gate.values())))


out = {'note': __doc__.strip()}

# ---- tier (1): own shares (Saudi line, SAR) vs Tadawul All Share Index (SAR) ----
ANCHOR = pd.Timestamp('2026-08-07')   # no observation past the price anchor enters any window
amr_sr = _yahoo_series('yh_6015.SR.json')
amr_sr = amr_sr[amr_sr['Date'] <= ANCHOR]
tasi = _yahoo_series('yh_TASI.json')
tasi = tasi[tasi['Date'] <= ANCHOR]
cut5 = amr_sr['Date'].iloc[-1] - pd.DateOffset(years=5)
r_amr = _weekly_logret(amr_sr[amr_sr['Date'] >= cut5])
r_tasi = _weekly_logret(tasi[tasi['Date'] >= cut5])
out['tier1_own_vs_tasi'] = regress(r_amr, r_tasi,
                                  'AMR (Saudi line 6015, SAR) weekly vs Tadawul All Share Index, truncated at the 07-Aug-2026 anchor')

# ---- cross-check A: ADX line (AED) vs equal-weighted covered-UAE composite ----
RAW = os.path.join(HERE, '..', 'raw_ohlc', 'AE')
panel = {}
for f in sorted(os.listdir(RAW)):
    if not f.endswith('.csv'):
        continue
    nm = f[:-4]
    df, _ = clean_ohlc(load_ohlc(os.path.join(RAW, f)), nm, verbose=False, market='AE')
    panel[nm] = df[['Date', 'Price']].rename(columns={'Price': nm})
amr_ae = panel.pop('AMR')
wide = None
for nm, df in panel.items():
    wide = df if wide is None else wide.merge(df, on='Date', how='outer')
wide = wide.sort_values('Date').set_index('Date')
comp_ret = np.log(wide / wide.shift(1))
comp = comp_ret.mean(axis=1).dropna()           # equal-weighted daily log return
comp_idx = (comp.cumsum().apply(np.exp)).rename('Close').reset_index()
comp_idx.columns = ['Date', 'Close']
cut5b = amr_ae['Date'].iloc[-1] - pd.DateOffset(years=5)
out['crosscheck_adx_line_vs_uae_composite'] = regress(
    _weekly_logret(amr_ae[amr_ae['Date'] >= cut5b].rename(columns={'AMR': 'Close'})),
    _weekly_logret(comp_idx[comp_idx['Date'] >= cut5b]),
    'AMR (ADX line, AED) weekly vs equal-weighted composite of the 18 covered UAE names '
    '(CONSTRUCTED PROXY, not the exchange index)')

# ---- cross-check B: UAE-listed consumer peers vs the same composite -------------
peers = {}
for nm in ('AGTHIA', 'LULU'):
    d, _ = clean_ohlc(load_ohlc(os.path.join(RAW, nm + '.csv')), nm, verbose=False, market='AE')
    d = d[['Date', 'Price']].rename(columns={'Price': 'Close'})
    peers[nm] = regress(_weekly_logret(d[d['Date'] >= cut5b]),
                        _weekly_logret(comp_idx[comp_idx['Date'] >= cut5b]),
                        f'{nm} (UAE-listed consumer) weekly vs the same constructed composite')
out['crosscheck_uae_consumer_peers'] = peers
out['peer_median_beta'] = float(np.median([p['beta'] for p in peers.values()]))

# ---- adopted beta --------------------------------------------------------------
t1 = out['tier1_own_vs_tasi']
out['adopted'] = dict(
    beta=round(t1['beta'], 3),
    tier='(1) own-stock weekly regression against a local index of a market in which the '
         'shares are listed',
    basis=t1['label'], n_weeks=t1['n'], r2=round(t1['r2'], 4),
    se=round(t1['se_beta'], 4), window=f"{t1['first']} .. {t1['last']}",
    gate_passed=t1['usable'],
)
with open(os.path.join(HERE, 'beta_result.json'), 'w') as f:
    json.dump(out, f, indent=1)

for k in ('tier1_own_vs_tasi', 'crosscheck_adx_line_vs_uae_composite'):
    d = out[k]
    print(f"{k}: beta {d['beta']:.3f} (SE {d['se_beta']:.3f}, t {d['t_beta']:.2f}) "
          f"R2 {d['r2']:.3f} n={d['n']} {d['first']}..{d['last']} usable={d['usable']}")
for nm, d in peers.items():
    print(f"  peer {nm}: beta {d['beta']:.3f} R2 {d['r2']:.3f} n={d['n']} usable={d['usable']}")
print('peer median beta', round(out['peer_median_beta'], 3))
print('ADOPTED', out['adopted'])
