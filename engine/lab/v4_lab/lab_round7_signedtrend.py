"""
lab_round7_signedtrend.py -- Equation Lab, Round 7 (23-Jul-2026).

Direct response to two corrections from Sherif (ORWE/PHDC chart screenshots):
  1. "I never asked for the return to be higher for all stocks across the board.
     Some stocks are on a downward trend so surely their return should be
     downward i.e. negative. Some stocks like ORWE are sideways, so definitely
     will not have a premium return. Some are on an upward trend like PHDC.
     So treat each one individually." -> beta (Round 6) only scales the
     MAGNITUDE of a common positive premium; it never flips sign. This round
     builds a candidate whose sign is genuinely per-name.
  2. "Go for the slower bullet proof" -> build a DATED Egypt ERP/rf* schedule
     (not the Round 6 static Jul-2026 snapshot) before spending the FINAL shot.

PART A -- dated Egypt ERP/spread schedule (Task 27)
  Sourced, dated anchor points (NOT Damodaran's raw xls -- those are binary
  and unreachable by this session's web tools; web.archive.org is proxy-
  blocked; blog narratives don't embed per-country tables. Best available:
  independently-sourced reproductions/mirrors of his numbers, each dated and
  cited below). Held flat between knowns (step function) -- IDENTICAL
  convention to EGYPT.carry_schedule's own carry_rate() lookup.

    2013-01-01  rating B2   spread 5.00%  ERP(total) 13.30%  (studylib.net
                mirror of Damodaran's ctryprem table, "last updated Jan 2013")
    2022-01-01  ERP(total) 9.68%   (gurufocus.com, "Egypt Total Equity Risk
                Premium", explicitly sourced "Damodaran Online")
    2023-01-01  ERP(total) 15.43%  (gurufocus.com, same series/source)
    2026-01-01  rating Caa1  spread 6.37%  ERP(total) 13.94% CRP 9.71%
                (tools.theinvestlog.com "Egypt as of 2026-01-01" -- this
                EXACTLY matches Cost_of_Capital_Reference.md's already-vetted
                rating-basis figure, cross-validating both sources)

  IMPORTANT, checked directly: the actual EG panel's raw_ohlc history is
  NOT 2016-2026 -- 21/30 names start exactly 2021-01-03, a few start later,
  only CLHO (2016) and DSCW (2012) go deeper. So the panel MIN_HISTORY=260
  backtest population lives almost entirely in 2021-2026, which this
  schedule covers well (three anchors inside that exact window, capturing
  the 2022-2023 devaluation spike). The sparse 2013->2022 segment (flat 9yr)
  only touches early origins of the two long-history names -- flagged, not
  hidden, and does not miss any structural break inside the backtest data
  (the profile's 2016-11-03 break predates the panel entirely).

PART B -- signed, individual trend drift (Task 28) -- THE NEW CANDIDATE
  Distinct in construction from all six prior dead drift families:
    - NOT expanding-window (Round 5's own_mean) -> bounded lookback (6mo/12mo),
      i.e. the actual chart trend a person would read.
    - NOT shrunk toward a noisy cross-sectional grand mean (Round 5) ->
      shrunk toward ZERO (== toward carry, the one anchor already proven low-
      noise) with a per-name weight.
    - NOT cross-sectionally demeaned / zero-net (Round 4b) -> raw signed
      individual trend, no ranking, no panel-average subtraction.
    - NOT a trailing realized-ERP substitute (Round 4a) -> a plain trend
      statistic, no risk-premium interpretation attached.
    - NOT beta (Round 6) -> a first-moment (mean/direction) statistic, not a
      second-moment (co-movement) one -- beta cannot carry sign information
      about a name's own trend; this can.
  Shrinkage weight uses the SAME statistical-usability-gate PHILOSOPHY the
  codebase already trusts for beta (wacc_builder.py's n>=24/R^2>=5%/
  SE<|beta| gate, "not distinguishable from noise" -> fallback): here, a
  James-Stein-style t-stat gate, continuous rather than a hard cutoff --
       w_i = t_i^2 / (t_i^2 + k)
  so a flat/choppy name (ORWE-like, small |t|) gets weight ~0 (drift stays
  at carry) and a strongly trending name (PHDC-like, large |t|) gets weight
  ~1 (drift moves toward its own trailing trend). k controls how much
  evidence is required; swept.

Walk-forward precompute reuses fit_har_v3/har_forecast_v3/carry_log_h/
simulate_terminal_v3/crps_sample/winkler/pooled_scores exactly as Rounds
5-6. Benchmark (carry-anchored lognormal RW) and shape (nu, width_cal)
unchanged throughout -- center-only candidate. DEV only; FINAL untouched.
Seeding: zlib.crc32-based (deterministic), per the lesson learned earlier
this session (hash() is salted/non-deterministic across process runs).
"""
import sys, os, time, zlib
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc, crps_sample, winkler, trailing_cc_vol, yz_variance_proxy
from mc_v3 import fit_har_v3, har_forecast_v3, simulate_terminal_v3, carry_log_h, pooled_scores, block_bootstrap_ci, verdict
from data_quality import clean_ohlc
from market_profiles import EGYPT

PROFILE = EGYPT
HORIZON = 60
MIN_HISTORY = 260
N_PATHS = 20000
SEED = 42
Q_ANNUAL = 0.0
DEV_CUTOFF = pd.Timestamp('2025-07-01')
NU = PROFILE.nu
WIDTH_CAL = PROFILE.width_cal


def stable_seed(ticker, oi):
    return SEED + int(oi) + zlib.crc32(ticker.encode()) % 1000


# ============================================================ PART A: dated ERP/spread schedule
ERP_SCHEDULE = [
    ("2013-01-01", 0.1330),
    ("2022-01-01", 0.0968),
    ("2023-01-01", 0.1543),
    ("2026-01-01", 0.1394),
]
SPREAD_SCHEDULE = [
    ("2013-01-01", 0.0500),
    ("2026-01-01", 0.0637),
]
# static Round-6 snapshot, kept for a direct before/after comparison
RF_STAR_STATIC, ERP_STATIC = 0.1594, 0.1394


def schedule_lookup(schedule, date):
    d = pd.Timestamp(date)
    v = schedule[0][1]
    for eff, val in schedule:
        if d >= pd.Timestamp(eff):
            v = val
    return v


def rf_star_dated(date):
    return PROFILE.carry_rate(date) - schedule_lookup(SPREAD_SCHEDULE, date)


def erp_dated(date):
    return schedule_lookup(ERP_SCHEDULE, date)


print("=== dated Egypt ERP/spread schedule (Part A) ===")
for chk in ['2021-06-01', '2022-06-01', '2023-06-01', '2024-06-01', '2025-06-01', '2026-06-01']:
    print(f"  {chk}: rf*={rf_star_dated(chk)*100:.2f}%  ERP={erp_dated(chk)*100:.2f}%  "
          f"(carry_rate={PROFILE.carry_rate(chk)*100:.2f}%)")

d = '/home/claude/testahil_repo/engine/raw_ohlc/EG'
names = sorted(f[:-4] for f in os.listdir(d) if f.endswith('.csv'))

# ---------------------------------------------------------------- real EGX30 index -> weekly log returns (for beta)
idx = pd.read_csv('/home/claude/labwork/EGX30_index.csv')
idx['Date'] = pd.to_datetime(idx['Date'], format='%m/%d/%Y')
idx['Price'] = idx['Price'].astype(str).str.replace(',', '', regex=False).astype(float)
idx = idx.sort_values('Date').reset_index(drop=True)
idx_s = pd.Series(idx['Price'].values, index=pd.DatetimeIndex(idx['Date'].values))
idx_wk = idx_s.resample('W-THU').last().dropna()
market_wk = np.log(idx_wk / idx_wk.shift(1)).dropna()
print(f"\nreal EGX30 index: {len(market_wk)} weekly obs, {market_wk.index.min().date()} .. {market_wk.index.max().date()}")

# ---------------------------------------------------------------- load & prep panel (unfiltered history, matches Round 0/5/6)
panels = {}
for t in names:
    df = load_ohlc(os.path.join(d, f'{t}.csv'))
    df, _ = clean_ohlc(df, t, verbose=False, market='EG')
    df = df.sort_values('Date').reset_index(drop=True)
    if len(df) < MIN_HISTORY + HORIZON + 1:
        continue
    v = yz_variance_proxy(df)
    close = df['Price'].values
    dates = pd.DatetimeIndex(df['Date'].values)
    s = pd.Series(close, index=dates)
    wk = s.resample('W-THU').last().dropna()
    wk_lr = np.log(wk / wk.shift(1)).dropna()
    panels[t] = dict(df=df, v=v, close=close, dates=dates, wk_lr=wk_lr,
                      first_date=dates[0], last_date=dates[-1])

print(f"{len(panels)}/{len(names)} names loaded")
print(f"first_date range: {min(p['first_date'] for p in panels.values()).date()} .. "
      f"{max(p['first_date'] for p in panels.values()).date()}")


def beta_at(ticker, origin_date, max_weeks=260, min_n=24, min_r2=0.05):
    own = panels[ticker]['wk_lr']
    own = own[own.index < origin_date].tail(max_weeks)
    mkt = market_wk[market_wk.index < origin_date].tail(max_weeks)
    both = pd.concat([own.rename('own'), mkt.rename('mkt')], axis=1).dropna()
    n = len(both)
    if n < min_n:
        return 1.0, n, np.nan, 'fallback_n'
    x = both['mkt'].values; y = both['own'].values
    xm, ym = x.mean(), y.mean()
    sxx = np.sum((x - xm) ** 2)
    if sxx <= 0:
        return 1.0, n, np.nan, 'fallback_degenerate'
    beta = np.sum((x - xm) * (y - ym)) / sxx
    resid = y - (ym + beta * (x - xm))
    sse = np.sum(resid ** 2); sst = np.sum((y - ym) ** 2)
    r2 = 1 - sse / sst if sst > 0 else 0.0
    dof = n - 2
    se_beta = np.sqrt(sse / dof / sxx) if dof > 0 and sxx > 0 else np.inf
    if r2 < min_r2 or se_beta >= abs(beta):
        return 1.0, n, r2, 'fallback_gate'
    return float(beta), n, float(r2), 'own_regression'


# ============================================================ PART B: signed trend statistic
TREND_WINDOWS = [126, 252]


def trend_at(close, origin, window):
    """Walk-forward-safe trailing trend statistic ending at `origin`
    (uses close[origin-window .. origin], i.e. strictly known-by-origin data).
    Returns (daily_mean, t_stat) or (0.0, 0.0) if insufficient history."""
    lo = origin - window
    if lo < 0:
        return 0.0, 0.0
    seg = close[lo:origin + 1]
    if len(seg) < window + 1:
        return 0.0, 0.0
    lr = np.diff(np.log(seg))
    daily_mean = lr.mean()
    daily_std = lr.std(ddof=1)
    if daily_std <= 0:
        return 0.0, 0.0
    se_mean = daily_std / np.sqrt(window)
    t_stat = daily_mean / se_mean
    return float(daily_mean), float(t_stat)


# ---------------------------------------------------------------- Phase 1: per-(name,origin) precompute
t0 = time.time()
precomp = []
for t, p in panels.items():
    df, v, close = p['df'], p['v'], p['close']
    n = len(df)
    origin = MIN_HISTORY
    while origin + HORIZON < n:
        date = df['Date'].iloc[origin]
        spot = close[origin]
        y = close[origin + HORIZON]
        beta_fit, s2 = fit_har_v3(v, origin, horizon=HORIZON)
        dv = har_forecast_v3(v, origin, beta_fit, s2, horizon=HORIZON)
        sigma_h = np.sqrt(dv * HORIZON) * WIDTH_CAL
        carry_b = carry_log_h(PROFILE, date, Q_ANNUAL, HORIZON)
        sig_b = trailing_cc_vol(close, origin) * np.sqrt(HORIZON)
        b, nb, r2b, bsrc = beta_at(t, date)
        row = dict(ticker=t, origin_idx=origin, date=date, spot=spot, realized=y,
                   sigma_h=sigma_h, carry_b=carry_b, sig_b=sig_b,
                   beta=b, beta_n=nb, beta_r2=r2b, beta_src=bsrc,
                   rf_star_dated=rf_star_dated(date), erp_dated=erp_dated(date))
        for w in TREND_WINDOWS:
            dm, ts = trend_at(close, origin, w)
            row[f'dmean_{w}'] = dm
            row[f'tstat_{w}'] = ts
        precomp.append(row)
        origin += HORIZON

pre = pd.DataFrame(precomp)
print(f"\nPhase 1 done: {len(pre)} windows in {time.time()-t0:.1f}s")
n_dev = (pre['date'] < DEV_CUTOFF).sum(); n_final = (pre['date'] >= DEV_CUTOFF).sum()
print(f"DEV: {n_dev}  FINAL: {n_final}")
pre.to_csv('/tmp/lab_round7_precomp.csv', index=False)

for w in TREND_WINDOWS:
    ts = pre[f'tstat_{w}']
    print(f"  window={w}: |t| mean={ts.abs().mean():.2f} median={ts.abs().median():.2f} "
          f"p90={ts.abs().quantile(0.9):.2f} max={ts.abs().max():.2f}  "
          f"frac|t|>2: {(ts.abs()>2).mean():.2%}")


# ============================================================ Phase 2: sweep & score
def run_variant(rows_df, drift_fn):
    out = []
    for _, r in rows_df.iterrows():
        drift = drift_fn(r)
        seed = stable_seed(r['ticker'], r['origin_idx'])
        samp = simulate_terminal_v3(r['spot'], r['sigma_h'], drift, nu=NU, n_paths=N_PATHS, seed=seed)
        rngb = np.random.default_rng(seed + 1)
        bench = r['spot'] * np.exp(r['carry_b'] + r['sig_b'] * rngb.standard_normal(N_PATHS))
        q_e = np.percentile(samp, [5, 25, 50, 75, 95]); q_b = np.percentile(bench, [5, 25, 50, 75, 95]); y = r['realized']
        out.append(dict(origin=r['date'], ticker=r['ticker'], spot=r['spot'], realized=y, drift=drift,
            crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
            pin50=0.5*abs(y-q_e[2]), pin50_b=0.5*abs(y-q_b[2]),
            wink=winkler(q_e[0], q_e[4], y), wink_b=winkler(q_b[0], q_b[4], y),
            pit=float(np.mean(samp <= y)),
            in50=q_e[1] <= y <= q_e[3], in80=np.percentile(samp,10) <= y <= np.percentile(samp,90), in90=q_e[0] <= y <= q_e[4],
            w90=(q_e[4]-q_e[0])/r['spot'], w90_b=(q_b[4]-q_b[0])/r['spot'], med_disp=(q_e[2]/r['spot']-1)))
    return pd.DataFrame(out)


def cov_flag(cov90):
    return "OK" if 0.88 <= cov90 <= 0.92 else "OUT-OF-RANGE"


dev_rows = pre[pre['date'] < DEV_CUTOFF].reset_index(drop=True)
results = []
t0 = time.time()

# --- B1: trend-only, sweep window x k x s ---------------------------------
print("\n=== B1: signed trend-only sweep (carry + s*tilt, tilt = t^2/(t^2+k) * dmean * H) ===")
for w in TREND_WINDOWS:
    for k in [1, 4, 9]:
        for s in [0.0, 0.5, 1.0]:
            def drift_fn(r, w=w, k=k, s=s):
                t2 = r[f'tstat_{w}'] ** 2
                wgt = t2 / (t2 + k)
                tilt = wgt * r[f'dmean_{w}'] * HORIZON
                return r['carry_b'] + s * tilt
            res = run_variant(dev_rows, drift_fn)
            sc, _ = pooled_scores([res])
            results.append(dict(family='trend_only', window=w, k=k, s=s, **sc))
            print(f"  [w={w:3d} k={k} s={s:.2f}]  crps_skill={sc['crps_skill']:+.4f}  "
                  f"cov90={sc['cov90']:.3f} [{cov_flag(sc['cov90'])}]  pit={sc['pit_mean']:.3f}  "
                  f"w90_ratio={sc['w90_ratio']:.3f}  ({time.time()-t0:.0f}s)")

res_df = pd.DataFrame(results)
res_df.to_csv('/tmp/lab_round7_dev_sweep.csv', index=False)
print(f"\nB1 total runtime: {time.time()-t0:.0f}s")
print(res_df.to_string(index=False, float_format=lambda x: f'{x:8.4f}'))
