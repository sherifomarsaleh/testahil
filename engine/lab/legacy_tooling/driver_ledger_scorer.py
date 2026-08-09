"""
driver_ledger_scorer.py
------------------------
Mechanical scorer for the Fundamental Driver Ledger — the counterpart to
ledger_scorer.py (which scores the Calibration Ledger on the Monte Carlo side).

Purpose: bring the fundamental side to parity. Today Fundamental_Driver_Ledger.md
is closed and reviewed manually. This script computes error %, flags bias
direction, and mechanically surfaces the "2 of last 3 missed the same way"
rule that Step 3.5 / Part C already states as a policy but has no code
enforcing.

This does NOT replace analyst judgment (the *rationale* for a driver stays
qualitative) — it only mechanizes the *scoring* of closed rows, the same way
ledger_scorer.py mechanizes CRPS/PIT scoring rather than judging the model.
"""

from dataclasses import dataclass, field
from typing import Optional
from statistics import mean


@dataclass
class DriverRow:
    ticker: str
    driver_class: str          # e.g. "NBFI hyper-growth fade", "opex-ratio fade"
    driver_name: str           # human label, e.g. "2026 revenue growth %"
    assumed: float
    date_opened: str
    rationale: str = ""
    actual: Optional[float] = None
    date_closed: Optional[str] = None

    @property
    def is_closed(self) -> bool:
        return self.actual is not None

    @property
    def error_pct(self) -> Optional[float]:
        """(actual - assumed) / assumed. None if not yet closed or assumed == 0."""
        if not self.is_closed or self.assumed == 0:
            return None
        return (self.actual - self.assumed) / abs(self.assumed)

    @property
    def direction(self) -> Optional[str]:
        """'over' = assumption was too high vs actual; 'under' = too low."""
        e = self.error_pct
        if e is None:
            return None
        if e < 0:
            return "over"     # assumed > actual
        if e > 0:
            return "under"    # assumed < actual
        return "flat"


def score_row(row: DriverRow) -> dict:
    """Score a single closed row. Mirrors the per-cohort grading step in ledger_scorer.py."""
    if not row.is_closed:
        return {"ticker": row.ticker, "driver": row.driver_name, "status": "open"}
    return {
        "ticker": row.ticker,
        "driver": row.driver_name,
        "driver_class": row.driver_class,
        "assumed": row.assumed,
        "actual": row.actual,
        "error_pct": round(row.error_pct * 100, 2),
        "direction": row.direction,
    }


def bias_flag(rows: list[DriverRow], driver_class: str, threshold_pct: float = 10.0) -> dict:
    """
    Implements the ledger's stated rule: if 2 of the last 3 closed rows in a
    driver-class missed in the same direction by more than `threshold_pct`,
    flag the class as biased. This is the mechanical version of the
    "check the ledger before reusing a heuristic" instruction.
    """
    closed = [r for r in rows if r.driver_class == driver_class and r.is_closed]
    closed_sorted = sorted(closed, key=lambda r: r.date_closed or "")
    last_three = closed_sorted[-3:]

    if len(last_three) < 2:
        return {"driver_class": driver_class, "flagged": False, "n": len(last_three),
                "reason": "not enough closed rows yet"}

    material = [r for r in last_three if abs(r.error_pct or 0) * 100 >= threshold_pct]
    directions = [r.direction for r in material]
    same_direction_count = max(directions.count("over"), directions.count("under")) if directions else 0

    flagged = same_direction_count >= 2
    return {
        "driver_class": driver_class,
        "flagged": flagged,
        "n_closed_considered": len(last_three),
        "n_material_misses": len(material),
        "dominant_direction": max(set(directions), key=directions.count) if directions else None,
        "mean_error_pct": round(mean([r.error_pct for r in last_three if r.error_pct is not None]) * 100, 2)
                          if any(r.error_pct is not None for r in last_three) else None,
    }


def aggregate(rows: list[DriverRow]) -> dict:
    """
    Full ledger summary: per-class bias flags + overall closed/open counts.
    Analogous to ledger_scorer.aggregate(cohorts) for the Calibration Ledger.
    """
    classes = sorted({r.driver_class for r in rows})
    return {
        "n_open": sum(1 for r in rows if not r.is_closed),
        "n_closed": sum(1 for r in rows if r.is_closed),
        "by_class": {c: bias_flag(rows, c) for c in classes},
    }


if __name__ == "__main__":
    # Example using the ledger's own real entries (GBCO watchlist items).
    rows = [
        DriverRow("GBCO", "opex-ratio fade", "2026 opex/revenue %", assumed=0.22,
                  date_opened="2026-07-08", rationale="mild operating leverage assumed"),
        DriverRow("GBCO", "NBFI hyper-growth fade", "lender revenue growth %", assumed=0.35,
                  date_opened="2026-07-08", rationale="halved last year's growth"),
    ]
    for r in rows:
        print(score_row(r))
    print(aggregate(rows))
