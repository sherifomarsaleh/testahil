"""How far each walk-forward's projection drifts over horizons its own score cannot see.

WHY THIS EXISTS. [R-FCAL-01]'s walk-forwards score a cell only where an ACTUAL exists,
which is right — a forecast is graded against what happened. The consequence is
structural and nobody had measured it: at a recent origin the far horizons are years
that have not happened, so THE ERROR RECORD IS BLIND TO THEM. A discounted cash flow
leans on those years hardest — the terminal is struck off the last explicit year, and
the explicit years compound into it — so the part of the projection carrying the most
value is the part with the least evidence behind it.

FOUND BY BUILDING SOMETHING ELSE ON IT. [R-VCAL-01]'s cash-flow lens read ARCC's origin
2023 at EGP 105.78 against a close of 10.00, and the cause was in that run's own forward
model: a projected EBIT margin compounding from 30.6% at horizon 1 to 60.1% at horizon
5, against filed gross margins of 21.2% and 40.6%. NO GATE LOOKS AT IT AND THE REASON IS
STRUCTURAL — [R-ANCHOR-01] tests a forecast opening BELOW the filed record and a rate
DECLINING from its own opening year, and says in terms that it does not fire above.

WHAT THIS MODULE DOES, AND WHAT IT DELIBERATELY DOES NOT. It measures, per run and per
origin: how far the projected operating margin travels from horizon 1 to the run's last
horizon, and how many of those horizon cells the run's own score could grade. It sets no
threshold and it fails nothing. A margin that rises is not a defect — a company
genuinely recovering operating leverage does exactly that — and a cutoff invented here
would be the free parameter the PROMOTION RULE forbids. WHAT IT ESTABLISHES IS WHETHER
THE PROBLEM IS GENERAL OR WHETHER ARCC IS ALONE, which is the question a rule would have
to answer first.

Read it live. Nothing quotes a figure from it.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, HERE)

import cashflow_lens as CL   # noqa: E402
import panel as P            # noqa: E402


def last_actual(tk):
    """The last fiscal year the run holds an ACTUAL for — the edge of what it can grade."""
    d = os.path.join(ENGINE, "%s_walkforward" % tk.lower())
    for fn in ("bottom_up.json",):
        p = os.path.join(d, fn)
        if os.path.exists(p):
            try:
                j = json.load(open(p, encoding="utf-8"))
                if isinstance(j.get("last_actual"), int):
                    return j["last_actual"], fn
            except Exception:
                pass
    pan, src = P._panel(d)
    return (max(pan) if pan else None), src


def rows(market="EG"):
    cells, names, declared, usable = P.build(market)
    out = []
    for tk in sorted(CL.PROJECTORS):
        la, la_src = last_actual(tk)
        for y in declared:
            c = cells.get((tk, y))
            if not c or not c["ready"]:
                continue
            try:
                proj = CL.PROJECTORS[tk](y)
            except Exception as exc:
                out.append({"ticker": tk, "origin": y, "error":
                            "%s: %s" % (type(exc).__name__, str(exc)[:70])})
                continue
            hs = [h for h in sorted(proj)
                  if proj[h].get("revenue") and proj[h].get("ebit") is not None]
            if len(hs) < 2:
                continue
            m1 = proj[hs[0]]["ebit"] / proj[hs[0]]["revenue"]
            mN = proj[hs[-1]]["ebit"] / proj[hs[-1]]["revenue"]
            gradeable = sum(1 for h in hs if la is not None and y + h <= la)
            out.append({"ticker": tk, "origin": y, "h_first": hs[0], "h_last": hs[-1],
                        "margin_first": m1, "margin_last": mN,
                        "drift_pp": (mN - m1) * 100,
                        "relative": (mN / m1 - 1) if m1 else None,
                        "gradeable": gradeable, "horizons": len(hs),
                        "last_actual": la, "last_actual_src": la_src})
    return out


def report(market="EG"):
    rs = rows(market)
    if not rs:
        raise SystemExit("REFUSED: no origin produced a projection. An empty census is "
                         "not a clean census [R-ENF-04].")
    print("how far a projection travels over horizons its own score cannot grade\n")
    print("  A RISING MARGIN IS NOT A DEFECT and nothing here is a threshold. What is")
    print("  measured is the DRIFT and the GRADEABLE FRACTION side by side, because a")
    print("  large drift on horizons that were all graded is evidence, and the same")
    print("  drift on horizons that could not be is an assertion.\n")
    print("  %-6s %-6s %8s %8s %9s %9s  %s"
          % ("name", "origin", "m(h1)", "m(hN)", "drift pp", "relative", "graded"))
    ungraded_drift, graded_drift = [], []
    for r in sorted(rs, key=lambda r: (r["ticker"], r["origin"])):
        if "error" in r:
            print("  %-6s %-6d  %s" % (r["ticker"], r["origin"], r["error"]))
            continue
        print("  %-6s %-6d %7.1f%% %7.1f%% %+8.1f %+8.1f%%  %d of %d"
              % (r["ticker"], r["origin"], 100 * r["margin_first"],
                 100 * r["margin_last"], r["drift_pp"],
                 100 * (r["relative"] or 0), r["gradeable"], r["horizons"]))
        (graded_drift if r["gradeable"] == r["horizons"] else ungraded_drift).append(
            abs(r["drift_pp"]))

    def _m(xs):
        return sum(xs) / len(xs) if xs else None
    print("\n  origins whose every horizon could be graded: %d, mean |drift| %s"
          % (len(graded_drift),
             "—" if not graded_drift else "%.1f pp" % _m(graded_drift)))
    print("  origins carrying at least one ungradeable horizon: %d, mean |drift| %s"
          % (len(ungraded_drift),
             "—" if not ungraded_drift else "%.1f pp" % _m(ungraded_drift)))
    biggest = max((r for r in rs if "error" not in r),
                  key=lambda r: abs(r["drift_pp"]))
    print("\n  largest drift: %s %d, %.1f%% to %.1f%% (%+.1f pp), %d of %d horizons "
          "gradeable against a last actual of %s"
          % (biggest["ticker"], biggest["origin"], 100 * biggest["margin_first"],
             100 * biggest["margin_last"], biggest["drift_pp"], biggest["gradeable"],
             biggest["horizons"], biggest["last_actual"]))
    return rs


if __name__ == "__main__":
    report()
