"""
Testahil — Step 0 calibration backtest (the pass gate before any study is built).

Runs a rolling backtest of the mc_v2 engine on the target's own OHLC at h = `horizon` trading
days. At each origin, using ONLY data up to that date, it builds the 3-month-ahead forecast
distribution and scores the realized close against it.

The grade is SKILL vs a naive benchmark — a zero-drift random-walk lognormal cone (spot, trailing
realized vol) — measured by CRPS skill (1 - CRPS/CRPS_benchmark; must be > 0) and the Winkler
interval score. A PIT histogram and 50/80/90% interval-coverage table are produced too, but as
DIAGNOSTICS only: band-containment rewards width and is never the pass criterion.

Windows are NON-OVERLAPPING (step = horizon) so the 3-month forecasts do not autocorrelate and
flatter the calibration. Discrete event factors are held OFF in the backtest so the test isolates
the engine's distributional calibration (width / shape / drift) rather than scenario overlays; the
continuous secular/asset-class drift IS included, since that is part of what is being calibrated.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np

import mc_v2
from mc_v2 import TRADING_DAYS


# --------------------------------------------------------------------------- scoring primitives
def crps_ensemble(x: np.ndarray, y: float) -> float:
    """CRPS of an ensemble forecast x against scalar outcome y (sorted O(m log m) estimator)."""
    x = np.sort(np.asarray(x, float))
    m = len(x)
    term1 = np.mean(np.abs(x - y))
    i = np.arange(1, m + 1)
    e_xx = (2.0 / (m * m)) * np.sum((2 * i - m - 1) * x)   # = mean_{i,j}|x_i - x_j|
    return float(term1 - 0.5 * e_xx)


def winkler_score(x: np.ndarray, y: float, alpha: float = 0.20) -> float:
    """Winkler interval score for the central (1-alpha) interval of ensemble x at outcome y."""
    lo = np.percentile(x, 100 * alpha / 2)
    hi = np.percentile(x, 100 * (1 - alpha / 2))
    s = hi - lo
    if y < lo:
        s += (2.0 / alpha) * (lo - y)
    elif y > hi:
        s += (2.0 / alpha) * (y - hi)
    return float(s)


def pit_value(x: np.ndarray, y: float) -> float:
    """Probability-integral transform: fraction of the ensemble at or below the outcome."""
    return float(np.mean(np.asarray(x, float) <= y))


def _benchmark_ensemble(spot, sigma_ann, horizon, n, rng):
    """Zero-drift random-walk lognormal terminal ensemble (the naive benchmark)."""
    dv = (sigma_ann ** 2) / TRADING_DAYS
    z = rng.standard_normal(n)
    return spot * np.exp(-0.5 * dv * horizon + np.sqrt(dv * horizon) * z)


@dataclass
class Step0Result:
    ticker: str
    horizon: int
    n_origins: int
    crps_model: float
    crps_bench: float
    crps_skill: float                 # 1 - crps_model/crps_bench ; PASS if > 0
    winkler_model: float
    winkler_bench: float
    winkler_skill: float
    pit: np.ndarray                   # one PIT value per origin (diagnostic)
    coverage: dict                    # {level: empirical coverage} (diagnostic)
    passed: bool

    def summary(self) -> str:
        cov = "  ".join(f"{k}%: {v:.0%}" for k, v in self.coverage.items())
        return (
            f"Step 0 — {self.ticker}  (h={self.horizon}, {self.n_origins} non-overlapping origins)\n"
            f"  CRPS skill vs RW-lognormal : {self.crps_skill:+.3f}   "
            f"({'PASS' if self.crps_skill > 0 else 'FAIL'})\n"
            f"  Winkler skill              : {self.winkler_skill:+.3f}\n"
            f"  CRPS  model / bench        : {self.crps_model:.3f} / {self.crps_bench:.3f}\n"
            f"  Coverage (target 50/80/90) : {cov}   [diagnostic only]\n"
            f"  PIT mean / std             : {self.pit.mean():.2f} / {self.pit.std():.2f}   "
            f"[uniform ~ 0.50 / 0.29]"
        )


def run_step0(
    ticker: str,
    ohlc: dict,
    continuous,
    *,
    asset_class: Optional[str] = None,
    horizon: int = 60,
    years: int = 5,
    n_paths: int = 4000,
    trail_window: int = 252,
    min_history: int = 130,
    seed: int = 42,
) -> Step0Result:
    close = np.asarray(ohlc["close"], float)
    o, h, l = (np.asarray(ohlc[k], float) for k in ("open", "high", "low"))
    n = len(close)
    lookback = min(years * TRADING_DAYS, n)
    first = max(min_history, n - lookback)
    origins = list(range(first, n - horizon, horizon))   # non-overlapping
    if not origins:
        raise ValueError("Not enough history for a single non-overlapping window.")

    rng = np.random.default_rng(seed)
    crps_m, crps_b, wink_m, wink_b, pit = [], [], [], [], []
    hits = {50: 0, 80: 0, 90: 0}

    for t in origins:
        sub = {"open": o[: t + 1], "high": h[: t + 1], "low": l[: t + 1], "close": close[: t + 1]}
        spot = close[t]
        y = close[t + horizon]

        res = mc_v2.run(
            anchor=spot, realized_vol=0.0, continuous=continuous, events=[],
            horizon=horizon, n_paths=n_paths, seed=int(rng.integers(1, 1_000_000)),
            ohlc=sub, asset_class=asset_class,
        )
        fx = res.paths[:, -1]

        trail_r = np.diff(np.log(close[max(0, t - trail_window): t + 1]))
        sigma_trail = float(trail_r.std() * np.sqrt(TRADING_DAYS))
        bx = _benchmark_ensemble(spot, sigma_trail, horizon, n_paths, rng)

        crps_m.append(crps_ensemble(fx, y)); crps_b.append(crps_ensemble(bx, y))
        wink_m.append(winkler_score(fx, y)); wink_b.append(winkler_score(bx, y))
        pit.append(pit_value(fx, y))
        for lv in hits:
            lo = np.percentile(fx, 50 - lv / 2); hi = np.percentile(fx, 50 + lv / 2)
            hits[lv] += int(lo <= y <= hi)

    cm, cb = float(np.mean(crps_m)), float(np.mean(crps_b))
    wm, wb = float(np.mean(wink_m)), float(np.mean(wink_b))
    n_orig = len(origins)
    return Step0Result(
        ticker=ticker, horizon=horizon, n_origins=n_orig,
        crps_model=cm, crps_bench=cb, crps_skill=1 - cm / cb,
        winkler_model=wm, winkler_bench=wb, winkler_skill=1 - wm / wb,
        pit=np.array(pit),
        coverage={k: hits[k] / n_orig for k in (50, 80, 90)},
        passed=(1 - cm / cb) > 0,
    )
