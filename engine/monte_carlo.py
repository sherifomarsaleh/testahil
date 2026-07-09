"""
Testahil — Monte Carlo engine (one model, ten external factors), seed 42, 50k paths.

Methodology (matches the published TMGH study):
  - Continuous (C) factors contribute a forward DRIFT to price (their price-space 3M drifts).
  - Diffusion volatility = the instrument's realized vol (calibrated from OHLC) — this already
    embeds the historical factor-driven vol, so it is NOT double-counted with C vol.
  - Discrete (M/E) events each occur with their probability on a uniformly-random session inside
    the window, applying a one-day multiplicative impact ~ Normal(mean, spread). Events both
    skew and widen the distribution (so path vol prints a touch above realized).
  - Idiosyncratic diffusion is Gaussian in log-returns (lognormal paths).

Outputs are the canonical study set: percentile table (5/25/50/75/95 at T+20 & T+60),
the forward cone (fan), the T+20/T+60 bell curves, and the level-touch ladder.
"""
from dataclasses import dataclass
from typing import Optional
import numpy as np

TRADING_DAYS = 252


@dataclass
class MCResult:
    anchor: float
    horizon: int
    n_paths: int
    seed: int
    paths: np.ndarray            # (n_paths, horizon+1), paths[:,0] == anchor
    realized_vol: float
    ann_path_vol: float
    net_drift_3m: float

    def percentiles(self, day: int, qs=(5, 25, 50, 75, 95)):
        col = self.paths[:, day]
        return {q: float(np.percentile(col, q)) for q in qs}

    def percentile_table(self, horizons=None):
        if horizons is None:
            horizons = {"T+20": min(20, self.horizon), "T+60": self.horizon}
        return {name: self.percentiles(d) for name, d in horizons.items()}

    def touch_probability(self, level: float, by_day: int) -> float:
        """P(path's running max>=level [up] or running min<=level [down] by `by_day`)."""
        seg = self.paths[:, : by_day + 1]
        if level >= self.anchor:
            return float((seg.max(axis=1) >= level).mean())
        return float((seg.min(axis=1) <= level).mean())

    def prob_between(self, lo, hi, day=None):
        day = self.horizon if day is None else day
        col = self.paths[:, day]
        m = np.ones_like(col, dtype=bool)
        if lo is not None:
            m &= col >= lo
        if hi is not None:
            m &= col < hi
        return float(m.mean())


def run(
    anchor: float,
    realized_vol: float,             # annualized, from OHLC (e.g. 0.36)
    continuous,                      # list[factor_library.Factor] tier 'C'
    events,                          # list[factor_library.Factor] tier 'M'/'E'
    horizon: int = 60,
    n_paths: int = 50_000,
    seed: int = 42,
    vol_floor: float = 0.05,
) -> MCResult:
    rng = np.random.default_rng(seed)
    sigma = max(realized_vol, vol_floor)
    daily_sigma = sigma / np.sqrt(TRADING_DAYS)

    # continuous block -> net daily drift (3M drift assumed over the `horizon` window)
    net_drift_3m = float(sum((f.drift_3m or 0.0) for f in continuous))
    daily_drift = np.log1p(net_drift_3m) / horizon  # log-space, so median lift == exp(net_drift)

    # diffusion: lognormal daily returns
    shocks = rng.normal(daily_drift - 0.5 * daily_sigma**2, daily_sigma, size=(n_paths, horizon))
    log_paths = np.concatenate([np.zeros((n_paths, 1)), np.cumsum(shocks, axis=1)], axis=1)

    # discrete events: per path, Bernoulli(prob); if hit, add impact on a random day (log space)
    for f in events:
        if not f.prob:
            continue
        hit = rng.random(n_paths) < f.prob
        k = int(hit.sum())
        if k == 0:
            continue
        impacts = rng.normal(f.impact_mean or 0.0, f.impact_spread or 0.0, size=k)
        days = rng.integers(1, horizon + 1, size=k)
        log_impacts = np.log1p(np.clip(impacts, -0.95, None))
        idx = np.where(hit)[0]
        # apply from the event day forward (a level shift, not a one-day blip that reverts)
        for j, p_idx in enumerate(idx):
            log_paths[p_idx, days[j]:] += log_impacts[j]

    paths = anchor * np.exp(log_paths)

    # realized annualized vol of the simulated daily log-returns (sanity / reporting)
    dlr = np.diff(np.log(paths), axis=1)
    ann_path_vol = float(dlr.std() * np.sqrt(TRADING_DAYS))

    return MCResult(anchor, horizon, n_paths, seed, paths, sigma, ann_path_vol, net_drift_3m)


def expected_factor_contribution(continuous, events) -> float:
    """Net expected 3M contribution = sum(C drifts) + sum(prob*impact_mean) over events."""
    c = sum((f.drift_3m or 0.0) for f in continuous)
    e = sum((f.prob or 0.0) * (f.impact_mean or 0.0) for f in events)
    return c + e
