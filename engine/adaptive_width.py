"""adaptive_width.py — Testahil per-stock ONLINE width overlay.

ADOPTED 23-Jul-2026, EG ONLY, GOING FORWARD. Holds a MECHANISM (and a small set of
fixed a-priori constants); it holds no per-market fit and never goes stale.

WHAT IT DOES
    A per-name multiplier on the market cone width, learned ONLINE from that name's OWN
    resolved 60-day residuals. It corrects the single thing the pooled (nu, width_cal)
    structurally cannot: a name whose OWN volatility sits below (or above) the panel
    average is given a market-level cone that is too WIDE (or too narrow) for it. The
    dominant failure this fixes is OVER-COVERAGE — the system's robust FAILs (LGES, Korea;
    ALPHADHABI, ADX) are OVER-covered (cov90 ~= 1.00) with well-CENTRED PITs (~0.47): not
    mis-centred, simply too wide, because their own vol is below the panel average.

OVERLAY, NOT A REFIT
    The pooled (nu, width_cal) are UNCHANGED and keep driving the Step-0 calibration gate.
    This layer multiplies width_cal for the LIVE forecast ONLY, per name. It NEVER touches
    drift (pure carry) and NEVER touches the tail nu. Turn the flag off and the engine is
    bit-for-bit the previous production engine.

SPEC (all constants fixed a-priori; only the shrink s was ever fitted — on an 11-name DEV
split — and it has been out-of-sample on every name added since):
    m_raw = clip( sqrt( EWMA_lambda( u^2 over the resolved past ) ), 0.7, 1.5 )
    mult  = 1 + s * sign(m_raw - 1) * max(0, |m_raw - 1| - dz)
  with lambda = 0.85 (EWMA on resolved windows, most-recent weighted 1), s = 0.5 (gentle),
  dz = 0.10 (dead zone: leave a name untouched when its implied mis-calibration is within
  +/-10% of correct). std_u = 1 is perfectly width-calibrated; <1 => cone too wide (tighten),
  >1 => too narrow (widen).
    u = (log(close[o+H]/close[o]) - carry) / (sqrt(HAR_var * H) * width_cal),  q = 0 in carry
        (drift is common to every s and cancels in the paired promotion delta; q=0 keeps the
         residual a pure WIDTH object).
  WALK-FORWARD SAFE: a 60d window opened at origin o' only enters the estimate once it has
  RESOLVED, i.e. o'+H <= today. Nothing uses an outcome it could not have known.

PROMOTION EVIDENCE (30-name EG panel; strict LONO / held-out FINAL; block bootstrap {2,3,4}Q):
    proper score : log-CRPS skill 0.0154 (baseline) -> 0.0152 (overlay) = PARITY, robust
                   across block sizes -> ZERO proper-score cost (this is NOT a CRPS gain).
    calibration  : pooled |std_u - 1| 0.096 -> 0.069 ; cov90 0.903 -> 0.893 (both in-band);
                   24 / 30 names moved CLOSER to std_u = 1.
    Replicated as the panel grew: 11/11, 13/16, 17/21, 24/30. The win is per-name width
    HONESTY at no cost to the proper score — that, and only that, is the claim.
  Same OOS gate that KILLED the CRPS-selection idea and the Amihud/dynamic-DoF arm. It passed.

HISTORY GATE (safety — read this before activating a new market)
    The overlay OVER-CORRECTS on short (~5yr) history and only behaves on long (~10-15yr)
    history. Below MIN_WINDOWS resolved 60d windows the multiplier is FORCED to 1.0 (exact
    baseline — always safe, since baseline is the currently adopted, validated engine).
    OPERATIONAL REALITY as of adoption: engine/raw_ohlc/EG currently carries mostly ~5-year
    histories (~17 resolved windows per name) — squarely in the over-correction regime — so
    with this gate the overlay is DORMANT (mult == 1.0) on the live library and merging it
    changes nothing. It begins to act, per name, ONLY once that name's LONG history is loaded
    into raw_ohlc/EG (bringing it to >= MIN_WINDOWS). MIN_WINDOWS is a CONSERVATIVE floor,
    not an OOS-tuned knob: it sits above the ~16-17-window 5yr failure regime and below the
    ~30-window ISPH long history; making it larger only keeps the overlay at baseline longer,
    which cannot hurt.

SCOPE / PROMOTION RULE
    EG ONLY. Every other market runs mult == 1.0 (flag off) until it clears the SAME 30-name-
    style LONO gate on its OWN panel. Activation is the per-profile flag width_overlay_active.

GOING-FORWARD ONLY
    Applies to cohorts anchored on/after adoption. Published / graded cohorts are NEVER
    retro-fitted (append-only ledger). Turning the overlay live for a market is a reviewed-PR
    / materiality step, because it moves some published 90% cones by >5%.
"""
import numpy as np

from mc_v2 import yz_variance_proxy
from mc_v3 import (fit_har_v3, har_forecast_v3, carry_log_h,
                   signal_alpha, simulate_paths_v3)

# ---- fixed a-priori constants (RULES, not a fit) ------------------------------------------
EWMA_LAM = 0.85            # EWMA decay on resolved windows (most-recent weight 1.0)
CLIP = (0.7, 1.5)          # clip on the raw sqrt-EWMA multiplier
SHRINK = 0.5               # gentle shrink s toward 1.0
DEAD_ZONE = 0.10           # leave a name untouched within +/-10% of correct
H = 60                     # forecast/residual horizon (trading days)
MIN_HIST = 260             # burn-in before the first residual window
MIN_WINDOWS = 28           # history gate: below this many resolved windows -> baseline (mult=1.0)


def gentle(m_raw: float) -> float:
    """Gentle + dead-zoned shrink of a raw multiplier toward 1.0 (the validated map)."""
    dev = float(m_raw) - 1.0
    sign = 1.0 if dev > 0 else (-1.0 if dev < 0 else 0.0)
    return 1.0 + SHRINK * sign * max(0.0, abs(dev) - DEAD_ZONE)


def resolved_u2(df, profile, horizon: int = H, min_hist: int = MIN_HIST):
    """Standardized-residual u^2 for every RESOLVED non-overlapping `horizon`-day window,
    using the profile's OWN base (nu, width_cal) config and pure-carry drift (q=0).
    Walk-forward safe by construction: the loop only reaches windows whose outcome exists."""
    v = yz_variance_proxy(df)
    close = df['Price'].values
    cal = float(getattr(profile, 'width_cal', 1.0) or 1.0)
    out = []
    o = min_hist
    n = len(df)
    while o + horizon < n:
        beta, s2 = fit_har_v3(v, o, horizon=horizon)
        dv = har_forecast_v3(v, o, beta, s2, horizon=horizon)
        sig = float(np.sqrt(dv * horizon) * cal)
        if sig > 0:
            drift = float(carry_log_h(profile, df['Date'].iloc[o], 0.0, horizon))
            u = (np.log(close[o + horizon] / close[o]) - drift) / sig
            out.append(u * u)
        o += horizon
    return out


def live_width_mult(df, profile, horizon: int = H, min_hist: int = MIN_HIST,
                    return_detail: bool = False):
    """The per-name LIVE width multiplier at today's origin.

    Returns 1.0 (exact baseline) when the overlay is inactive for this market OR the name has
    fewer than MIN_WINDOWS resolved windows (short history -> over-correction risk). Otherwise
    returns the validated gentle+dead-zoned online multiplier.
    """
    active = bool(getattr(profile, 'width_overlay_active', False))
    if not active:
        return (1.0, dict(active=False, reason='flag_off', n_windows=0, m_raw=1.0)) if return_detail else 1.0
    u2 = resolved_u2(df, profile, horizon, min_hist)
    if len(u2) < MIN_WINDOWS:
        d = dict(active=True, reason='insufficient_history', n_windows=len(u2), m_raw=1.0)
        return (1.0, d) if return_detail else 1.0
    w = np.array([EWMA_LAM ** k for k in range(len(u2))][::-1])
    m_raw = float(np.clip(np.sqrt(np.sum(w * np.array(u2)) / np.sum(w)), *CLIP))
    mult = float(gentle(m_raw))
    if return_detail:
        return mult, dict(active=True, reason='applied', n_windows=len(u2), m_raw=m_raw)
    return mult


def live_paths(df, profile, spot, date, q_annual, horizon: int = H,
               n_paths: int = 50000, seed: int = 42):
    """Canonical LIVE forecast path set for a covered name, WITH the per-market width overlay
    applied per profile.width_overlay_active. The base engine (mc_v3) is untouched — this only
    scales width_cal by the per-name multiplier and then calls simulate_paths_v3 exactly as the
    standing roll-forward chain does (drift = carry + signal-if-active; nu from the profile;
    seed 42). Returns (paths[n_paths, horizon+1], meta)."""
    v = yz_variance_proxy(df)
    close = df['Price'].values
    o = len(df) - 1
    beta, s2 = fit_har_v3(v, o, horizon=horizon)
    dv = har_forecast_v3(v, o, beta, s2, horizon=horizon)
    mult = live_width_mult(df, profile, horizon)
    cal_eff = float(getattr(profile, 'width_cal', 1.0) or 1.0) * mult
    sigma_h = float(np.sqrt(dv * horizon) * cal_eff)
    carry = float(carry_log_h(profile, date, q_annual, horizon))
    alpha, _ = signal_alpha(profile, close, o, sigma_h)   # 0.0 when signal inactive (all markets today)
    drift = carry + alpha
    nu = float(profile.nu) if getattr(profile, 'nu', None) else 8.0
    paths = simulate_paths_v3(spot, dv, horizon, drift, nu=nu,
                              n_paths=n_paths, seed=seed, width_cal=cal_eff)
    meta = dict(mult=mult, width_cal_base=float(getattr(profile, 'width_cal', 1.0) or 1.0),
                width_cal_eff=cal_eff, sigma_h=sigma_h, drift=drift, nu=nu)
    return paths, meta


if __name__ == "__main__":
    # Data-free self-check of the validated map and the safety fallbacks (VERIFY BY IMPORT).
    assert abs(gentle(1.00) - 1.00) < 1e-12          # centred -> untouched
    assert abs(gentle(1.05) - 1.00) < 1e-12          # inside dead zone -> untouched
    assert abs(gentle(1.40) - 1.15) < 1e-12          # 1 + 0.5*(0.40-0.10)
    assert abs(gentle(0.70) - 0.90) < 1e-12          # 1 - 0.5*(0.30-0.10)

    class _P:  # flag OFF -> exact baseline regardless of data
        width_overlay_active = False
        width_cal = 0.972
        nu = 4.0
    assert live_width_mult(None, _P()) == 1.0
    print("adaptive_width self-check OK — gentle map + inactive fallback verified; "
          f"MIN_WINDOWS={MIN_WINDOWS}, lambda={EWMA_LAM}, s={SHRINK}, dz={DEAD_ZONE}")
