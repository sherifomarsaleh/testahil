"""AMR — equity beta from the stock's OWN price history against its OWN market's index.

Beta hierarchy (house rule, strict preference order):
  (1) own-stock 2-5yr WEEKLY regression vs its OWN local index, usability gate
      n>=24, R^2>=5%, SE(beta) < |beta|;
  (2) same-country peer beta (median unlevered, re-levered);
  (3) beta = 1.0.

[CHANGED 10-Aug-2026] TIER (1) NOW RUNS AGAINST THE ACTUAL FTSE ADX GENERAL INDEX.
The first edition regressed the company's SAUDI line against the Tadawul All Share
Index, because no daily history for the Abu Dhabi index could be reached from this
environment. That was disclosed rather than hidden, but it priced a UAE-listed
company's systematic risk against a different country's market cycle, and it produced
the highest beta of every estimate available (0.894, against 0.47-0.60 for every
UAE-based one) — which flows straight into a higher discount rate and a lower value.

The index history was then supplied directly, 3,884 daily closes from 2 January 2011
to 24 July 2026, and is committed at engine/market_indices/AE_FADGI.csv. This is the
company's own exchange's own index: same market, same session, same currency, no
proxy and no substitution. It is deliberately NOT placed under engine/raw_ohlc/AE/,
which is the calibration panel of covered STOCKS — an index dropped in there would
silently join a panel it has no business in.

Screened before use, as any series must be: 3,884 sessions over 15.6 years, 250 a
year, no duplicate dates, no non-positive values, largest single-session move 8.8%.
The weekday mix shows the January-2022 trading-week change plainly — Sunday-Thursday
before it, Monday-Friday after — so the weekly sampling below uses the Friday close
that has applied throughout this stock's entire listed life (it floated in December
2022, after the change).

WHY THERE IS NO TIMING CORRECTION HERE. An earlier revision of this file regressed
against a UAE index FUND priced in New York, which closes hours after Abu Dhabi; that
gap biases a plain regression downward and needed a Dimson lead-lag correction. Against
the exchange's own index that problem does not exist — both series are struck at the
same closing auction on the same exchange — so the contemporaneous coefficient is the
estimate, and the Dimson sum is reported only as a diagnostic. It is materially the
same number here, which is itself the evidence that no correction is warranted.

A constructed composite of the covered UAE names is retained as a DIAGNOSTIC and is
never the regressor: it is a selection-biased subset whose sector mix would become the
"market", and the subject is one of its own constituents, so the stock would be partly
regressed against itself.

The index's own behaviour is checked rather than assumed: regressed the same way, two
of the exchange's heavyweights and a large bank should land near or below 1.0, and a
defensive food name well below. Those numbers are reported below.

Every estimate that has ever informed this input stays on the record: the retired
Tadawul regression, the UAE consumer peers, and the composite.
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


def dimson(y, x, label):
    """Dimson (1979) lead-lag sum: the beta a plain regression understates when the
    stock and the index do not close at the same moment.

    y is regressed on the market return LAGGED, CONTEMPORANEOUS and LED, and the three
    coefficients are summed. Under non-synchronous trading the contemporaneous
    coefficient alone captures only the part of the market move the stock had time to
    react to; the neighbours pick up the rest. The standard error of the sum carries the
    full covariance between the three, not just their individual variances — dropping the
    cross terms would understate it badly, since the three regressors are correlated.
    """
    j = pd.concat([y.rename('y'), x.rename('x0'), x.shift(1).rename('xm1'),
                   x.shift(-1).rename('xp1')], axis=1).dropna()
    n = len(j)
    if n < 5:
        return dict(label=label, n=n, usable=False, reason='too few overlapping observations')
    X = np.column_stack([np.ones(n), j['x0'], j['xm1'], j['xp1']])
    coef, *_ = np.linalg.lstsq(X, j['y'].values, rcond=None)
    resid = j['y'].values - X @ coef
    dof = n - 4
    cov = float(resid @ resid / dof) * np.linalg.inv(X.T @ X)
    beta = float(coef[1] + coef[2] + coef[3])
    var = float(sum(cov[i, i] for i in (1, 2, 3))
                + 2 * (cov[1, 2] + cov[1, 3] + cov[2, 3]))
    se_b = float(np.sqrt(var))
    return dict(label=label, n=int(n), beta=beta, se_beta=se_b,
                t_beta=beta / se_b if se_b else float('nan'),
                coef_lag=float(coef[2]), coef_contemporaneous=float(coef[1]),
                coef_lead=float(coef[3]),
                first=str(j.index[0].date()), last=str(j.index[-1].date()))


out = {'note': __doc__.strip()}

# ---- tier (1): own shares (ADX line, AED) vs the FTSE ADX General Index (AED) ----
ANCHOR = pd.Timestamp('2026-08-07')   # no observation past the price anchor enters any window
RAW = os.path.join(HERE, '..', 'raw_ohlc', 'AE')
amr_ae, _ = clean_ohlc(load_ohlc(os.path.join(RAW, 'AMR.csv')), 'AMR', verbose=False, market='AE')
amr_ae = amr_ae[['Date', 'Price']].rename(columns={'Price': 'Close'})
amr_ae = amr_ae[amr_ae['Date'] <= ANCHOR]


def _index_csv(path):
    """The exchange index, from the vendor export committed alongside this study."""
    df = pd.read_csv(path, encoding='utf-8-sig')
    df.columns = [c.strip('"') for c in df.columns]
    out = pd.DataFrame({
        'Date': pd.to_datetime(df['Date'], format='%m/%d/%Y'),
        'Close': pd.to_numeric(df['Price'].astype(str).str.replace(',', ''), errors='coerce'),
    }).dropna().sort_values('Date').reset_index(drop=True)
    assert not out['Date'].duplicated().any(), 'duplicate dates in the index series'
    assert (out['Close'] > 0).all(), 'non-positive index level'
    return out


IDX_LABEL = 'FTSE ADX General Index (AED, the exchange the shares are listed on)'
fadgi = _index_csv(os.path.join(HERE, '..', 'market_indices', 'AE_FADGI.csv'))
fadgi = fadgi[fadgi['Date'] <= ANCHOR]

# The longest window up to five years, per the hierarchy. AMR listed 12-Dec-2022, so the
# usable window is its whole life — stated rather than silently rounded to five years.
cut5 = amr_ae['Date'].iloc[-1] - pd.DateOffset(years=5)
r_amr_ae = _weekly_logret(amr_ae[amr_ae['Date'] >= cut5])
r_uae = _weekly_logret(fadgi[fadgi['Date'] >= cut5])

out['index_series'] = dict(
    label=IDX_LABEL, file='engine/market_indices/AE_FADGI.csv',
    sessions=int(len(fadgi)), first=str(fadgi['Date'].iloc[0].date()),
    last=str(fadgi['Date'].iloc[-1].date()),
    note='Supplied as a primary export. Its last session precedes the 7 August 2026 price '
         'anchor, so the regression window ends there; no observation after the anchor can '
         'enter the sample by construction.')

out['tier1_own_vs_adx_index'] = regress(
    r_amr_ae, r_uae,
    f'AMR (ADX line, AED) weekly vs the {IDX_LABEL}, truncated at the 07-Aug-2026 anchor')
out['tier1_dimson_diagnostic'] = dimson(
    r_amr_ae, r_uae,
    'Same regression, Dimson lead-lag sum — a DIAGNOSTIC only: both series strike at the '
    'same closing auction on the same exchange, so there is no non-synchronous trading to '
    'correct for, and the sum should and does land near the plain coefficient')

# Does the index behave like an index? Three exchange heavyweights and one defensive name
# are regressed the same way. If a heavyweight did NOT come out near 1.0, the series would
# not be measuring the market it claims to and nothing below it would be trustworthy.
out['index_validation_constituents'] = {}
for nm in ('ALDAR', 'EMAAR', 'ADCB', 'AGTHIA'):
    d, _ = clean_ohlc(load_ohlc(os.path.join(RAW, nm + '.csv')), nm, verbose=False, market='AE')
    d = d[['Date', 'Price']].rename(columns={'Price': 'Close'})
    d = d[d['Date'] <= ANCHOR]
    out['index_validation_constituents'][nm] = regress(
        _weekly_logret(d[d['Date'] >= cut5]), r_uae,
        f'{nm} weekly vs the {IDX_LABEL} — index sanity check, not a valuation input')

# ---- cross-check: the retired first-edition regressor (Saudi line vs Tadawul) ----
amr_sr = _yahoo_series('yh_6015.SR.json')
amr_sr = amr_sr[amr_sr['Date'] <= ANCHOR]
tasi = _yahoo_series('yh_TASI.json')
tasi = tasi[tasi['Date'] <= ANCHOR]
cut5_sr = amr_sr['Date'].iloc[-1] - pd.DateOffset(years=5)
out['crosscheck_saudi_line_vs_tasi'] = regress(
    _weekly_logret(amr_sr[amr_sr['Date'] >= cut5_sr]),
    _weekly_logret(tasi[tasi['Date'] >= cut5_sr]),
    'AMR (Saudi line 6015, SAR) weekly vs Tadawul All Share Index — the FIRST EDITION\'s '
    'regressor, retained as a disclosed cross-check: a different country\'s market cycle')

# ---- cross-check A: ADX line (AED) vs equal-weighted covered-UAE composite ----
RAW = os.path.join(HERE, '..', 'raw_ohlc', 'AE')
panel = {}
for f in sorted(os.listdir(RAW)):
    if not f.endswith('.csv'):
        continue
    nm = f[:-4]
    df, _ = clean_ohlc(load_ohlc(os.path.join(RAW, f)), nm, verbose=False, market='AE')
    panel[nm] = df[['Date', 'Price']].rename(columns={'Price': nm})
panel.pop('AMR', None)
wide = None
for nm, df in panel.items():
    wide = df if wide is None else wide.merge(df, on='Date', how='outer')
wide = wide.sort_values('Date').set_index('Date')
comp_ret = np.log(wide / wide.shift(1))
comp = comp_ret.mean(axis=1).dropna()           # equal-weighted daily log return
comp_idx = (comp.cumsum().apply(np.exp)).rename('Close').reset_index()
comp_idx.columns = ['Date', 'Close']
cut5b = cut5
out['crosscheck_adx_line_vs_uae_composite'] = regress(
    _weekly_logret(amr_ae[amr_ae['Date'] >= cut5b]),
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
# The plain contemporaneous coefficient, against the company's own exchange's own index.
# No timing correction is applied because there is no timing gap to correct: the stock and
# the index are struck at the same closing auction. The Dimson sum is computed anyway and
# reported beside it, so the claim "no correction needed" is evidenced, not asserted.
t1 = out['tier1_own_vs_adx_index']
td = out['tier1_dimson_diagnostic']
if not t1['usable']:
    raise SystemExit('tier-1 regression failed its usability gate — do not silently fall '
                     'through to a peer beta; state it and choose deliberately')
out['adopted'] = dict(
    beta=round(t1['beta'], 3),
    tier='(1) own-stock weekly regression against its OWN exchange index',
    basis=t1['label'],
    index=IDX_LABEL,
    n_weeks=t1['n'],
    se=round(t1['se_beta'], 4),
    t_stat=round(t1['t_beta'], 2),
    r2=round(t1['r2'], 4),
    window=f"{t1['first']} .. {t1['last']}",
    dimson_diagnostic=round(td['beta'], 3),
    dimson_se=round(td['se_beta'], 4),
    gate_passed=bool(t1['usable']),
    superseded='first edition used 0.894 — the Saudi line against the Tadawul All Share '
               'Index — because no Abu Dhabi index series could be obtained at the time; '
               'it is retained below as a cross-check',
)
with open(os.path.join(HERE, 'beta_result.json'), 'w') as f:
    json.dump(out, f, indent=1)

for k in ('tier1_own_vs_adx_index', 'crosscheck_saudi_line_vs_tasi',
          'crosscheck_adx_line_vs_uae_composite'):
    d = out[k]
    print(f"{k}: beta {d['beta']:.3f} (SE {d['se_beta']:.3f}, t {d['t_beta']:.2f}) "
          f"R2 {d['r2']:.3f} n={d['n']} {d['first']}..{d['last']} usable={d['usable']}")
td = out['tier1_dimson_diagnostic']
print(f"tier1 DIMSON diagnostic: beta {td['beta']:.3f} (SE {td['se_beta']:.3f}) "
      f"= lag {td['coef_lag']:+.3f} + contemporaneous {td['coef_contemporaneous']:+.3f} "
      f"+ lead {td['coef_lead']:+.3f}")
print('index validation (constituents should land near 1.0):')
for nm, d in out['index_validation_constituents'].items():
    print(f"  {nm}: beta {d['beta']:.3f} R2 {d['r2']:.3f} n={d['n']}")
for nm, d in peers.items():
    print(f"  peer {nm}: beta {d['beta']:.3f} R2 {d['r2']:.3f} n={d['n']} usable={d['usable']}")
print('peer median beta', round(out['peer_median_beta'], 3))
print('ADOPTED', json.dumps(out['adopted'], indent=1))
