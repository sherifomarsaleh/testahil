"""TA-signal ablation on the EG panel, h=5/10 — LONO-gated, production-exact.

Question: does adding a technical-analysis drift signal (via the engine's own
signal_alpha hook: alpha = b * sigma_H * clip(z, +/-2), dead zone |z|<0.5,
cap +/-0.5*sigma_H) improve pooled scale-normalized CRPS vs the identical
engine with signal OFF?  Paired design: same seed, same width, same carry —
the on-leg terminal sample is EXACTLY off_sample * exp(alpha), so the test
isolates the signal and nothing else.

Signals (z standardized by trailing-252 z-score of the raw stat, min 60 obs):
  brk20   : ln(close / max(close over prior 20 sessions))       prior sign +
  macd    : MACD(12,26,9) histogram / close                     prior sign +
  rsi     : RSI(14) level                                       prior sign -
  rev_1m  : engine's own 1m reversal z (mc_v3.signal_z)         prior sign -
b (sign+magnitude) is LONO cross-fitted: for name j, OLS slope of u on
clip(z) pooled over the 28 OTHER names' windows, capped |b|<=0.10
(production EG literature prior was IC=0.08).  u = (log y/spot - carry)/sigma_H.

Gate: Delta-skill = 1 - sum(crps_on/spot)/sum(crps_off/spot), house
robust_verdict (block bootstrap, blocks {2,3,4}, 3000 draws, seed 42).
Break filter: origins >= 2022-03-21 (adopted EG cut).  q=0 (gate-neutral).
nu=4, width_cal=0.972, 20k paths, seed 42+origin (production panel settings).
"""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc, yz_variance_proxy, crps_sample, trailing_cc_vol
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, simulate_terminal_v3, signal_z
from mc_v2 import har_features
from data_quality import clean_ohlc
import market_profiles as mp

PROF = mp.PROFILES['EG'] if isinstance(mp.PROFILES, dict) else mp.EGYPT
NU, CAL = PROF.nu, PROF.width_cal
assert NU == 4.0 and abs(CAL - 0.972) < 1e-9 and PROF.signal_active is False
BREAK = pd.Timestamp('2022-03-21')
MIN_HISTORY, NPATHS, SEED = 260, 20000, 42
NAMES = json.load(open('/home/claude/testahil_repo/engine/fitted_configs.json'))['EG']['panel_names']
RAW = '/home/claude/testahil_repo/engine/raw_ohlc/EG/{}.csv'

def trailing_z(x, win=252, minp=60):
    m = x.rolling(win, min_periods=minp).mean()
    s = x.rolling(win, min_periods=minp).std()
    z = (x - m) / s
    return z.replace([np.inf, -np.inf], np.nan).fillna(0.0)

def ta_series(df):
    c = df['Price']
    out = {}
    out['brk20'] = trailing_z(np.log(c / c.rolling(20).max().shift(1)))
    e12, e26 = c.ewm(span=12, adjust=False).mean(), c.ewm(span=26, adjust=False).mean()
    macd = e12 - e26
    hist = (macd - macd.ewm(span=9, adjust=False).mean()) / c
    out['macd'] = trailing_z(hist)
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    rsi = 100 - 100 / (1 + up / dn.replace(0, np.nan))
    out['rsi'] = trailing_z(rsi.fillna(50.0))
    return out

# ---------------- pass 1: records (incremental HAR, verified vs engine) ------
def har_incremental(v, origins, horizon):
    """Exact reimplementation of fit_har_v3 row-building, built once per name."""
    vv = v.ffill()
    X, Y = [], []
    built = 22
    fits = {}
    for o in origins:
        hi = o - horizon           # rows are t in range(22, o - horizon)
        for t in range(built, hi):
            f = har_features(v, t)
            if f is None:
                continue
            fut = vv.iloc[t + 1:t + 1 + horizon]
            m = fut.mean()
            if np.isfinite(m) and m > 0:
                X.append(f); Y.append(np.log(m))
        built = max(built, hi)
        if len(Y) < 60:
            fits[o] = (None, None); continue
        Xd = np.column_stack([np.ones(len(Y)), np.array(X)])
        ya = np.array(Y)
        beta, *_ = np.linalg.lstsq(Xd, ya, rcond=None)
        resid = ya - Xd @ beta
        fits[o] = (beta, float(np.var(resid, ddof=Xd.shape[1])))
    return fits

records = []
verify_har = []
for name in NAMES:
    df = load_ohlc(RAW.format(name))
    df, _ = clean_ohlc(df, name, verbose=False, market='EG')
    v = yz_variance_proxy(df)
    close = df['Price'].values
    dates = df['Date']
    ta = ta_series(df)
    n = len(df)
    for h in (5, 10):
        origins = [o for o in range(MIN_HISTORY, n - h, h) if dates.iloc[o] >= BREAK]
        fits = har_incremental(v, origins, h)
        for k, o in enumerate(origins):
            beta, s2 = fits[o]
            if k == len(origins) // 2 and name in ('ORAS', 'ISPH', 'TMGH'):
                b2, s22 = fit_har_v3(v, o, horizon=h)
                same = (beta is None and b2 is None) or (np.allclose(beta, b2) and np.isclose(s2, s22))
                verify_har.append((name, h, o, bool(same)))
            dv = har_forecast_v3(v, o, beta, s2, horizon=h)
            sig_h = float(np.sqrt(dv * h) * CAL)
            date = dates.iloc[o]
            spot, y = float(close[o]), float(close[o + h])
            carry = float(carry_log_h(PROF, date, 0.0, h))
            u = (np.log(y / spot) - carry) / sig_h
            z = {kk: float(ta[kk].iloc[o]) for kk in ('brk20', 'macd', 'rsi')}
            z['rev_1m'] = float(signal_z(close, o, 'rev_1m'))
            sig_b = float(trailing_cc_vol(close, o) * np.sqrt(h))
            records.append(dict(name=name, h=h, origin=date, oidx=o, spot=spot, y=y,
                                sigma_h=sig_h, carry=carry, u=u, sig_b=sig_b, **z))
r = pd.DataFrame(records).sort_values(['h', 'name', 'origin']).reset_index(drop=True)
assert all(s[3] for s in verify_har), verify_har
print("HAR fast path verified bit-for-bit at", len(verify_har), "sample origins")
print("records:", r.groupby('h').size().to_dict())
r.to_pickle('/tmp/ta/records.pkl')
