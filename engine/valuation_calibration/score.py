"""Scoring for the valuation calibration — and its refusal to score too early.

[R-VCAL-01]'s pre-registration fixes TWO series and this module implements both.
It also implements the thing a scorer most needs and least often has: the
condition under which it declines to produce a number.

  (i)  CONTEMPORANEOUS AGREEMENT — log(FV_t / P_t) at every origin. Measurable the
       moment a vintage exists, and `delivered.py` already reports it across the
       published book.

  (ii) GAP CLOSURE — whether log(FV_t / P_t) predicts the subsequent one-, two-
       and three-year total return net of carry. This is the measure of whether
       the lean is INFORMATION rather than merely a lean, and it is the one the
       whole reassessment turns on.

WHY THIS REFUSES TODAY, AND WHY THE REFUSAL IS THE POINT. The vintage archive
begins on 11-Jun-2026. Under [R-LENS-02] the fundamental lens speaks to horizons
of up to ONE YEAR, so the first vintage cannot be graded on its own clock before
11-Jun-2027, and the three-year reading not before 2029.

The temptation is obvious and this module exists partly to refuse it: three months
of subsequent prices ARE available, and a one-to-three-month score could be
computed today and would look like evidence. It would be evidence about the wrong
question. A fair value makes no claim over three months — that horizon belongs to
the price cone, which has its own calibration and its own record — and scoring the
fundamental lens on the cone's clock is the [R-TCAL-01] mistake exactly, whose
first edition graded a sub-monthly read at three months and produced one wrong
conclusion before it was caught. A LENS IS GRADED OVER THE HORIZON IT IS USED FOR.

So the honest output today is a DATE, not a number: this is when the instrument
starts working, and the instrument had to exist before the clock could start.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
ARCHIVE = os.path.join(ENGINE, "fv_vintages.json")

# The fundamental lens's own clock [R-LENS-02]. Not a tunable: it is the horizon
# the published claim is made over, so it is the horizon the claim is graded over.
HORIZONS_YEARS = (1, 2, 3)


def _load():
    return json.load(open(ARCHIVE, encoding="utf-8"))


def maturity_table(today: Optional[dt.date] = None) -> dict:
    """When each pre-registered horizon becomes scoreable, per vintage and pooled."""
    today = today or dt.date.today()
    arch = _load()
    rows = []
    for name, entries in sorted(arch.get("series", {}).items()):
        for e in entries:
            when = e.get("struck") or e.get("first_seen")
            if not when:
                continue
            d = dt.date.fromisoformat(when)
            rows.append({"ticker": name, "struck": d,
                         "spot": e.get("spot"),
                         "fair": (e.get("fair") or {}).get("base")})
    out = {"today": today.isoformat(), "vintages": len(rows), "by_horizon": {}}
    for h in HORIZONS_YEARS:
        mature = [r for r in rows
                  if _add_years(r["struck"], h) <= today
                  and r["spot"] and r["fair"] and r["fair"] > 0]
        first = min((_add_years(r["struck"], h) for r in rows), default=None)
        out["by_horizon"][h] = {
            "mature_now": len(mature),
            "first_scoreable": first.isoformat() if first else None,
            "days_away": (first - today).days if first and first > today else 0,
        }
    return out


def _add_years(d: dt.date, n: int) -> dt.date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:                       # 29 February
        return d.replace(year=d.year + n, day=28)


def gap_closure(today: Optional[dt.date] = None) -> dict:
    """Score (ii), or REFUSE with the date on which it becomes possible.

    Never returns a number computed over a horizon the lens does not claim. A
    score produced early is not a weak score, it is a score of a different
    question, and it would be read as the answer to this one.
    """
    t = maturity_table(today)
    scoreable = {h: v for h, v in t["by_horizon"].items() if v["mature_now"] > 0}
    if not scoreable:
        h1 = t["by_horizon"][1]
        return {
            "scored": False,
            "reason": (
                "REFUSED — the vintage archive holds %d fair values and NOT ONE has "
                "reached the one-year horizon the fundamental lens claims "
                "[R-LENS-02]. The first becomes scoreable on %s, %d days from %s.\n\n"
                "Three months of subsequent prices exist and a one-to-three-month "
                "score could be printed today. It would be a score of the PRICE "
                "CONE's question, which has its own calibration and its own "
                "published record, and reading it as this one's answer is the "
                "mistake [R-TCAL-01] caught in its own first edition: a lens graded "
                "over a horizon it does not speak to reports the weakest available "
                "reading of every claim it makes.\n\n"
                "The archive is the instrument. It had to exist before the clock "
                "could start, and now it does."
                % (t["vintages"], h1["first_scoreable"], h1["days_away"], t["today"])),
            "maturity": t,
        }
    return {"scored": False,
            "reason": ("some vintages have matured (%s) — the scorer's estimation "
                       "half is not written yet, deliberately: it is written when "
                       "there is something to score, so that its choices are made "
                       "against real data rather than imagined data."
                       % ", ".join("%dy: %d" % (h, v["mature_now"])
                                   for h, v in sorted(scoreable.items()))),
            "maturity": t}


def report(today: Optional[dt.date] = None):
    r = gap_closure(today)
    print("valuation calibration — gap closure [R-VCAL-01] score (ii)\n")
    print(r["reason"])
    print("\n  horizon   mature now   first scoreable")
    for h, v in sorted(r["maturity"]["by_horizon"].items()):
        print("  %d year%s  %6d       %s%s"
              % (h, " " if h == 1 else "s", v["mature_now"],
                 v["first_scoreable"],
                 ("   (%d days away)" % v["days_away"]) if v["days_away"] else ""))
    return r


if __name__ == "__main__":
    report()
