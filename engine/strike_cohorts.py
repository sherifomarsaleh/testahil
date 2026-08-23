"""strike_cohorts.py — batch roll-forward: re-strike published MC cones.

Runs the EXACT production chain, per the Standing Research Protocol's
roll-forward workflow, for every name in a market's raw_ohlc library:

    clean_ohlc (Step 0.0)            data-quality gate, per-market limits
      -> yz_variance_proxy           gap-aware Yang-Zhang daily variance
      -> fit_har_v3 / har_forecast_v3  mean forward daily variance
      -> carry_log_h(profile.rf_live)  carry drift, exact calendar yearfrac
      -> simulate_paths_v3           live profile nu/width_cal, seed 42, 50k

Horizons come from horizons.cohort_plan() — the calendar 1M/3M convention
adopted 27-Jul-2026 — never a hard-coded 20/60.

No approximations, no shortcuts: this module imports the same functions the
gate and the backtest run on, so a cone struck here is reproducible from the
committed engine.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from data_quality import clean_ohlc                      # noqa: E402
from primitives import load_ohlc, yz_variance_proxy      # noqa: E402
from mc_v3 import (fit_har_v3, har_forecast_v3, carry_log_h,  # noqa: E402
                   signal_alpha, simulate_paths_v3)
import horizons as HZ                                    # noqa: E402
import market_profiles as MP                             # noqa: E402
import adaptive_width as AW                              # noqa: E402

RAW = os.path.join(HERE, 'raw_ohlc')
N_PATHS = 50_000
SEED = 42
PCTS = (5, 25, 50, 75, 95)

_FIT_OVERRIDES_PATH = os.path.join(HERE, 'fit_overrides.json')


def _fit_override(market, ticker):
    """Per-name (nu, width_cal) override -- see engine/per_name_fit.py. A
    market's shared fit is a single number and cannot literally help one
    name while sparing another, so where a proposed re-fit genuinely
    regresses a specific name's own LONO verdict, that name keeps its prior
    config explicitly here rather than inheriting the market average.
    Returns (nu, width_cal) or None."""
    if not os.path.exists(_FIT_OVERRIDES_PATH):
        return None
    with open(_FIT_OVERRIDES_PATH) as f:
        overrides = json.load(f)
    entry = overrides.get(market, {}).get(ticker)
    if entry is None:
        return None
    return float(entry['nu']), float(entry['width_cal'])


def load_clean(market: str, ticker: str):
    """Step 0.0 gate applied. Returns (df, report)."""
    path = os.path.join(RAW, market, f'{ticker}.csv')
    raw = load_ohlc(path)
    df, rep = clean_ohlc(raw, ticker, verbose=False, market=market)
    return df.reset_index(drop=True), {'rows_in': len(raw), 'repairs': list(rep)}


def strike(market: str, ticker: str, q_annual: float = 0.0,
           anchor_idx: int = -1, n_paths: int = N_PATHS, seed: int = SEED):
    """Strike both calendar horizons for one name at the given anchor bar."""
    prof = MP.PROFILES[market]
    df, rep = load_clean(market, ticker)
    dates = pd.to_datetime(df['Date'])
    close = df['Price'].to_numpy(dtype=float)
    i = (len(df) - 1) if anchor_idx < 0 else anchor_idx
    anchor_date = dates.iloc[i]
    spot = float(close[i])

    v = yz_variance_proxy(df)
    plan = HZ.cohort_plan(market, anchor_date)
    width_mult = AW.live_width_mult(df, prof)   # 1.0 unless market flagged AND name past MIN_WINDOWS
    override = _fit_override(market, ticker)
    eff_nu, eff_base_cal = override if override else (prof.nu, prof.width_cal)

    out = {'market': market, 'ticker': ticker, 'anchor_date':
           anchor_date.date().isoformat(), 'spot': spot,
           'rows_in': int(rep['rows_in']), 'repairs': rep['repairs'],
           'rows_out': len(df), 'nu': eff_nu, 'width_cal': eff_base_cal,
           'fit_override_applied': override is not None,
           'width_overlay_mult': width_mult,
           'rf_live': prof.rf_live, 'q_annual': q_annual,
           'signal_active': prof.signal_active, 'horizons': {}}

    for short, hz in plan['horizons'].items():
        h = int(hz['horizon_days'])
        months = 1 if short == '1M' else 3
        beta, s2 = fit_har_v3(v, i, horizon=h)
        dvar = har_forecast_v3(v, i, beta, s2, horizon=h)
        cal_eff = eff_base_cal * width_mult
        sigma_h = float(np.sqrt(dvar * h) * cal_eff)
        # exact calendar year fraction — "3 months" IS 0.25 of a year
        yearfrac = months / 12.0
        drift = carry_log_h(prof, anchor_date, q_annual, h, yearfrac=yearfrac)
        alpha, z = signal_alpha(prof, close, i, sigma_h,
                                ic=(getattr(prof, 'ic_by_h', None) or {}).get(short))
        paths = simulate_paths_v3(spot, dvar, h, drift + alpha,
                                  nu=eff_nu, n_paths=n_paths, seed=seed,
                                  width_cal=cal_eff)
        term = paths[:, -1]
        out['horizons'][short] = {
            'label': hz['horizon_label'], 'h': h,
            'target_date': hz['target_date'], 'grade_date': hz['grade_date'],
            'basis': hz['basis'], 'h_density': hz['h_density'],
            'h_seasonal': hz['h_seasonal'],
            'anchor_vol_ann': float(np.sqrt(dvar * 252)),
            'sigma_h': sigma_h, 'drift_log_h': float(drift),
            'signal_alpha': float(alpha), 'signal_z': float(z),
            'pct': {f'p{p}': float(np.percentile(term, p)) for p in PCTS},
            '_paths': paths,
        }
    return out


def touch_probs(paths: np.ndarray, spot: float, levels) -> dict:
    """P(the path touches `level` at any point before the horizon).

    Direction is taken from the level's position relative to the CURRENT spot,
    which is what makes a ladder still meaningful after the anchor has moved
    past one of its own rungs.
    """
    hi = paths.max(axis=1)
    lo = paths.min(axis=1)
    out = {}
    for lv in levels:
        lv = float(lv)
        p = (hi >= lv).mean() if lv >= spot else (lo <= lv).mean()
        out[lv] = round(float(p) * 100)
    return out


def rel_touch(paths: np.ndarray, spot: float,
              ups=(5, 10, 15, 20), downs=(5, 10)) -> dict:
    hi = paths.max(axis=1)
    lo = paths.min(axis=1)
    out = {}
    for u in ups:
        out[f'+{u}'] = round(float((hi >= spot * (1 + u / 100)).mean()) * 100)
    for d in downs:
        out[f'-{d}'] = round(float((lo <= spot * (1 - d / 100)).mean()) * 100)
    return out


def run_market(market: str, tickers=None, q_map=None, verbose=True):
    q_map = q_map or {}
    if tickers is None:
        tickers = sorted(os.path.splitext(f)[0]
                         for f in os.listdir(os.path.join(RAW, market))
                         if f.endswith('.csv'))
    res = {}
    for t in tickers:
        try:
            r = strike(market, t, q_annual=q_map.get(t, 0.0))
            res[t] = r
            if verbose:
                a = r['horizons']['1M']; b = r['horizons']['3M']
                print(f"  {market}/{t:<13} spot={r['spot']:>12,.2f} "
                      f"1M h={a['h']:>2} [{a['pct']['p5']:>11,.2f} .. "
                      f"{a['pct']['p95']:>11,.2f}]  "
                      f"3M h={b['h']:>2} [{b['pct']['p5']:>11,.2f} .. "
                      f"{b['pct']['p95']:>11,.2f}]")
        except Exception as e:  # noqa: BLE001
            print(f"  {market}/{t:<13} ERROR {type(e).__name__}: {e}")
            res[t] = {'error': f'{type(e).__name__}: {e}'}
    return res


def self_check() -> bool:
    """Import-safe smoke test: one name per in-scope market must strike."""
    ok = True
    for m, t in (('EG', 'PHDC'), ('AE', 'EMAAR'), ('SA', 'ALINMA')):
        try:
            r = strike(m, t, n_paths=5000)
            a = r['horizons']['1M']['pct']
            ok &= a['p5'] < a['p50'] < a['p95'] and a['p5'] > 0
            print(f"{m}/{t}: OK spot={r['spot']:.2f} "
                  f"1M p5/p50/p95 = {a['p5']:.2f}/{a['p50']:.2f}/{a['p95']:.2f}")
        except Exception as e:  # noqa: BLE001
            ok = False
            print(f"{m}/{t}: FAIL {type(e).__name__}: {e}")
    return ok


if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        sys.exit(0 if self_check() else 1)
    market = argv[0]
    out = run_market(market, tickers=argv[1:] or None)
    clean = {k: {kk: vv for kk, vv in v.items() if kk != 'horizons'}
             | {'horizons': {h: {a: b for a, b in d.items() if a != '_paths'}
                             for h, d in v.get('horizons', {}).items()}}
             for k, v in out.items()}
    with open(os.path.join(HERE, f'strike_{market}.json'), 'w') as fh:
        json.dump(clean, fh, indent=1, default=str)
    print(f"wrote strike_{market}.json")
