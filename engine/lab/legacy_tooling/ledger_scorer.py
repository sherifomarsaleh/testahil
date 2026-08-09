"""
Testahil — Calibration Ledger scorer (the moat's scoreboard).

Two questions, the established forecasting-science way:
  1. Band coverage / PIT  -> did the realized close land where the distribution said it would?
  2. Touch calibration     -> did stated touch probabilities match realized touches (Brier)?

A single cohort gives a few data points; the real signal is the AGGREGATE across cohorts as
horizons mature. `score_cohort` handles one logged distribution; `aggregate` rolls many up into
coverage rates, a PIT histogram, and a Brier score / reliability table.

Built for the first live grade: PHDC's T+60 cohort, 2 September 2026.
"""
from dataclasses import dataclass, field
from typing import Optional
import numpy as np


@dataclass
class Cohort:
    """A logged distribution at anchor + the realized outcome once the horizon matures."""
    name: str
    anchor_date: str
    horizon: str                       # 'T+20' | 'T+60'
    anchor_price: float
    percentiles: dict                  # {5:.., 25:.., 50:.., 75:.., 95:..}
    realized_close: Optional[float] = None     # close at horizon
    realized_path_high: Optional[float] = None # max over the window (for upside touches)
    realized_path_low: Optional[float] = None  # min over the window (for downside touches)
    touch_quotes: list = field(default_factory=list)  # [(level, stated_prob), ...]


def _pit(percentiles: dict, realized: float) -> float:
    """Approximate PIT: interpolate the realized close onto the predicted CDF (0..1)."""
    qs = sorted(percentiles)
    xs = [percentiles[q] for q in qs]
    ps = [q / 100.0 for q in qs]
    if realized <= xs[0]:
        return max(0.0, ps[0] * realized / xs[0]) if xs[0] else 0.0
    if realized >= xs[-1]:
        return min(1.0, ps[-1] + (1 - ps[-1]) * (realized - xs[-1]) / max(xs[-1], 1e-9))
    return float(np.interp(realized, xs, ps))


def score_cohort(c: Cohort) -> dict:
    out = {"name": c.name, "horizon": c.horizon, "anchor_date": c.anchor_date,
           "anchor_price": c.anchor_price, "realized_close": c.realized_close}
    if c.realized_close is not None:
        p = c.percentiles
        out["in_50_band"] = bool(p[25] <= c.realized_close <= p[75])
        out["in_90_band"] = bool(p[5] <= c.realized_close <= p[95])
        out["pit"] = round(_pit(p, c.realized_close), 4)
        out["median_error_pct"] = round(100 * (c.realized_close - p[50]) / p[50], 2)
    # touch events scored against realized high/low
    touch_rows = []
    for level, stated in c.touch_quotes:
        realized_touch = None
        if level >= c.anchor_price and c.realized_path_high is not None:
            realized_touch = int(c.realized_path_high >= level)
        elif level < c.anchor_price and c.realized_path_low is not None:
            realized_touch = int(c.realized_path_low <= level)
        if realized_touch is not None:
            touch_rows.append({"level": level, "stated_prob": stated,
                               "touched": realized_touch,
                               "brier": round((stated - realized_touch) ** 2, 4)})
    out["touches"] = touch_rows
    return out


def aggregate(cohorts) -> dict:
    """Roll matured cohorts into coverage rates, a PIT histogram, and a Brier score."""
    scored = [score_cohort(c) for c in cohorts if c.realized_close is not None]
    if not scored:
        return {"n": 0, "note": "no matured cohorts yet"}
    in50 = np.mean([s["in_50_band"] for s in scored])
    in90 = np.mean([s["in_90_band"] for s in scored])
    pits = [s["pit"] for s in scored]
    hist, edges = np.histogram(pits, bins=[0, .1, .25, .5, .75, .9, 1.0])
    briers = [t["brier"] for s in scored for t in s["touches"]]
    return {
        "n": len(scored),
        "coverage_50_band": round(float(in50), 3),   # target ~0.50
        "coverage_90_band": round(float(in90), 3),    # target ~0.90
        "pit_hist": dict(zip([f"{edges[i]:.2f}-{edges[i+1]:.2f}" for i in range(len(hist))], hist.tolist())),
        "pit_mean": round(float(np.mean(pits)), 3),    # target ~0.50 (centred = unbiased)
        "touch_brier": round(float(np.mean(briers)), 4) if briers else None,  # lower = better
        "n_touch_events": len(briers),
        "read": _read(in50, in90, float(np.mean(pits))),
    }


def _read(in50, in90, pit_mean) -> str:
    """Plain-language diagnostic -> which tier to move (per the self-tuning loop, §2.3)."""
    msgs = []
    if in90 < 0.80:
        msgs.append("bands too NARROW (90% coverage low) -> widen C volatility")
    elif in90 > 0.98:
        msgs.append("bands too WIDE -> tighten C volatility")
    if pit_mean > 0.60:
        msgs.append("centre biased LOW (realized above median) -> raise C drift / event impacts")
    elif pit_mean < 0.40:
        msgs.append("centre biased HIGH (realized below median) -> lower C drift / event impacts")
    return "; ".join(msgs) if msgs else "well-calibrated on the sample so far"
