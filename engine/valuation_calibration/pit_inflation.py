"""The point-in-time forward inflation ladder, and the factors a projection needs.

[R-MACRO-01] requires that an explicit window run until growth is within 2pp of its
terminal, because a model whose last explicit year still compounds far above its
terminal capitalises a rate it never reached. Measured 18-09-2026 on every cell the
mechanical lens had ever scored, ALL SEVEN breached it and six of the seven carried a
terminal worth more than the whole enterprise value.

THE CAUSE WAS NOT THE TERMINAL. It was the escalator: every walk-forward run escalates
its drivers on the LAST PUBLISHED inflation print compounded FLAT at every horizon,
which is the right point-in-time choice for scoring a DRIVER and the wrong one for
building a VALUE — a flat crisis-level rate never converges to anything, so no window
of any length would have satisfied the bound.

WHAT THIS MODULE SUPPLIES IS NOT A FADE AND NOT A FREE PARAMETER. The point-in-time
archive already holds, at every origin, the IMF World Economic Outlook vintage's own
forward projection for that origin's year and the four after it — published at the
origin, by a named institution, on a named date, and DECLINING on its own:

    origin 2017   16.92 -> 10.91 ->  8.09 ->  7.18 ->  6.96
    origin 2023   32.18 -> 19.88 -> 13.77 -> 11.47 ->  9.50

A forecaster standing at the origin could have used exactly this and nothing else was
knowable. POINT-IN-TIME DISCIPLINE FORBIDS FORESIGHT, NOT A DECLINING FORECAST — and
that distinction is the whole of this module's claim. Nothing here is fitted, chosen,
tuned or smoothed; the ladder is read out of the archive and used as published.

TWO FACTORS AND ONE IDENTITY. `cumulative(h)` is the product of the ladder's first h
rates. `flat_equivalent(h)` is the single rate a run's own flat escalator must carry so
that its cumulative inflation AT horizon h equals the ladder's. The identity that makes
the substitution exact where it matters:

    cumulative(h) / cumulative(h-1) == 1 + ladder_rate(h)

so a projection built at h and one built at h-1 differ, year on year, by the ladder's
OWN rate for that year — even though each was built with a flat equivalent of its own.
The convergence test therefore reads the ladder's true final-year rate, not an average.
WHERE THE FLAT EQUIVALENT IS AN APPROXIMATION IS WITHIN a window (a run with a lagged
base or a year-one carve-out sees a differently-shaped path to the same endpoint), and
a run offering a native year-varying hook is given the ladder itself instead.

REFUSALS, never a guess: an origin with no forward path refuses; a horizon beyond the
ladder's published length refuses rather than extrapolating its last rate, because an
extrapolated ladder is a forecast this desk made and the archive did not.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)

import macro_history as MH       # noqa: E402


def ladder(market: str, origin: int):
    """The archive's own forward inflation path at this origin: {h: rate}, h from 1.

    Returns (None, reason) where the origin carries no forward path at all.
    """
    try:
        v = MH.origin(market, origin)
    except Exception as exc:
        return None, "the archive carries no vintage at this origin (%s)" % str(exc)[:80]
    fwd = (v.extras.get("cpi_annual") or {}).get("forward_path") or {}
    if not fwd:
        return None, "the archive's vintage at this origin publishes no forward path"
    out = {}
    for k, x in fwd.items():
        try:
            y = int(k)
        except (TypeError, ValueError):
            continue
        h = y - origin
        if h >= 1 and isinstance(x, (int, float)):
            out[h] = float(x)
    if not out:
        return None, "the forward path at this origin carries no year after it"
    # A ladder with a hole in it is refused rather than bridged: interpolating a year
    # would be inventing the very figure point-in-time discipline exists to protect.
    for h in range(1, max(out) + 1):
        if h not in out:
            return None, ("the forward path skips year %d and a bridged ladder is an "
                          "invented figure" % (origin + h))
    return out, None


def cumulative(market: str, origin: int, h: int):
    """Compounded inflation from the origin to horizon h, on the archive's own ladder."""
    lad, why = ladder(market, origin)
    if lad is None:
        return None, why
    if h > max(lad):
        return None, ("the forward path reaches %d years and horizon %d would extrapolate "
                      "it — a ladder this desk extended is not a published one"
                      % (max(lad), h))
    f = 1.0
    for j in range(1, h + 1):
        f *= 1.0 + lad[j]
    return f, None


def flat_equivalent(market: str, origin: int, h: int):
    """The single rate a flat escalator needs so its cumulative AT h matches the ladder."""
    f, why = cumulative(market, origin, h)
    if f is None:
        return None, why
    if h <= 0:
        return None, "a horizon of %d has no escalator" % h
    return f ** (1.0 / h) - 1.0, None


def terminal_rate(market: str, origin: int, h_last: int):
    """The ladder's OWN rate in the last explicit year.

    THE TERMINAL IS READ AT THE WINDOW'S END, not at a fixed horizon. A cell whose
    projection stops at three years and whose terminal was read at year five
    capitalises a rate two years further down the ladder than anything it projected,
    which is the same defect as the one this module exists to close, facing the other
    way. So the terminal inflation is whatever the archive published for the last year
    the window actually reached.
    """
    lad, why = ladder(market, origin)
    if lad is None:
        return None, why
    if h_last not in lad:
        return None, ("the forward path reaches %d years and the window ends at %d"
                      % (max(lad), h_last))
    return lad[h_last], None


def report(market: str = "EG"):
    blob = MH.load(market)
    print("THE POINT-IN-TIME FORWARD INFLATION LADDER  —  %s" % market)
    print("   read from the archive, published at each origin, never extended here\n")
    print("  origin   h=1     h=2     h=3     h=4     h=5    | conv h=5   conv h=3")
    print("  " + "-" * 72)
    for rec in blob["origins"]:
        y = rec["year"]
        lad, why = ladder(market, y)
        if lad is None:
            print("  %4d     %s" % (y, why))
            continue
        cells = "".join(("%6.2f%%" % (100 * lad[h])) if h in lad else "      -"
                        for h in range(1, 6))
        bits = []
        for hl in (5, 3):
            t, _ = terminal_rate(market, y, hl)
            bits.append("   %6.2f%%" % (100 * t) if t is not None else "        -")
        print("  %4d  %s |%s" % (y, cells, "".join(bits)))
    print("\n  THE LAST COLUMN IS THE POINT: a window ending at h carries the ladder's")
    print("  own rate for that year, so growth there and the terminal are the SAME")
    print("  number by construction and the convergence bound measures what is left —")
    print("  the run's own REAL growth, which is the thing it should have measured.")


if __name__ == "__main__":
    report(sys.argv[1] if len(sys.argv) > 1 else "EG")
