#!/usr/bin/env python3
"""Negative control for the mechanical lens's convergence refusal [R-MACRO-01].

A check nobody has seen fail is not evidence. This one reinjects the condition the
refusal exists for and asserts the lens goes red on it, asserts it stays quiet on a
window that HAS converged, and asserts the bound is the house's rather than a copy.

WHY A CONTROL AND NOT A GATE. The refusal lives inside cashflow_lens.cell(), where
the arithmetic it needs already sits. A gate outside would have to rebuild every
cell to re-derive the same growth rates, which is re-implementing another
instrument's job [R-ENF-03]. What an outside check CAN say, and what nothing else
would notice, is that the refusal still fires and still uses the house bound — so
that is what this says.

IT WRITES NOTHING. Every mutation is to an in-memory projector mapping in a process
that then exits; no file in the tree is opened for writing [R-ENF-01 EXTENDED
07-09-2026, no check modifies the tree it checks].

EVERY MUTATION ASSERTS THAT IT LANDED. This project has four times caught a control
passing a fixture that never injected its condition.
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine", "valuation_calibration"))
sys.path.insert(0, os.path.join(ROOT, "engine"))

import cashflow_lens as C          # noqa: E402
import panel as P                  # noqa: E402
import research_protocol as RP     # noqa: E402

CASES = 8
REFUSAL = "explicit window ends growing"


def _live_cell():
    """A real (ticker, origin) that REACHES the convergence check.

    Chosen by ASKING THE LENS rather than by naming one: a fixture keyed on a
    hard-coded name stops testing anything the day that name's block changes.

    REACHING IT IS THE WHOLE REQUIREMENT AND THE FIRST DRAFT MISSED IT. That draft
    asked only whether a cell had a usable projection, and picked one that dies
    several checks earlier on an incomplete valuation-input block. All four RED
    cases then came back quiet -- correctly, since the refusal was never reached --
    and, far worse, ALL THREE CLEAN CASES PASSED for exactly the same reason,
    proving nothing whatever. So the cell is selected by running the real cell()
    and keeping one whose outcome is decided AT the convergence check: it either
    scores, or its refusal IS this one.
    """
    cells, _n, _d, _u = P.build("EG")
    for (tk, y), c in sorted(cells.items()):
        if not c["ready"] or tk not in C.PROJECTORS:
            continue
        try:
            proj = C.PROJECTORS[tk](y)
            r, why = C.cell(tk, y, "EG", c)
        except Exception:
            continue
        if r is None and REFUSAL not in (why or ""):
            continue                      # dies before the check -- useless as a fixture
        hs = [h for h in C.HORIZONS if h in proj]
        if len(hs) < C.MIN_EXPLICIT:
            continue
        return tk, y, c, proj, hs
    return None, None, None, None, None


def _with(tk, proj):
    """Install a fixed projection for one name, restoring afterwards."""
    orig = C.PROJECTORS[tk]
    # **kw, NOT a fixed signature. The lens gained an `esc` argument the evening
    # after this control was written and every case here raised a TypeError rather
    # than testing anything — the control REFUSED, which is the behaviour it exists
    # to have, and a fixture pinned to a signature is the same shape as one pinned
    # to live state [L-403].
    C.PROJECTORS[tk] = lambda origin, _p=proj, **_kw: _p
    return orig


def main() -> int:
    tk, y, ci, proj, hs = _live_cell()
    if tk is None:
        print("FAILED — no live cell reaches a projection, so nothing was tested "
              "[R-ENF-04]: an empty population is not a clean one")
        return 1

    # THE TERMINAL IS READ THE WAY THE LENS READS IT — at the window's own last
    # explicit year — rather than at a horizon this control names. It was pinned at a
    # fixed horizon until the lens stopped reading it that way, and the fixture then
    # measured the bound against a rate no cell was built on.
    infl = C.terminal_inflation("EG", y, max(hs) if hs else None)
    if infl is None:
        print("FAILED — the archive carries no terminal inflation at %s %d, so "
              "the bound has nothing to be measured against" % (tk, y))
        return 1

    ok, bad = 0, []

    def case(n, what, want_refusal, mutate, landed):
        nonlocal ok
        saved = _with(tk, mutate)
        try:
            if not landed(mutate):
                bad.append("%d %s — THE FIXTURE DID NOT LAND" % (n, what))
                return
            r, why = C.cell(tk, y, "EG", ci)
            fired = r is None and REFUSAL in (why or "")
            if fired == want_refusal:
                ok += 1
            else:
                bad.append("%d %s — wanted %s, got %s (%s)"
                           % (n, what, "RED" if want_refusal else "quiet",
                              "RED" if fired else "quiet", (why or "scored")[:70]))
        except Exception as exc:                      # noqa: BLE001
            bad.append("%d %s — raised %s: %s" % (n, what, type(exc).__name__,
                                                  str(exc)[:70]))
        finally:
            C.PROJECTORS[tk] = saved

    def path(growth, base=1.0e9):
        """A projection whose revenue compounds at `growth` and whose margin is fixed."""
        out = {}
        rev = base
        for h in hs:
            rev = base * (1.0 + growth) ** h
            out[h] = {"revenue": rev, "ebit": 0.20 * rev, "dna": 0.05 * rev,
                      "capex": 0.05 * rev}
        return out

    def grows_at(g):
        def landed(p):
            r = [p[h]["revenue"] for h in hs]
            return abs((r[-1] / r[-2] - 1.0) - g) < 1e-9
        return landed

    # ---- RED: windows that end far from the terminal, in both directions
    case(1, "ends 20pp ABOVE terminal", True,
         path(infl + 0.20), grows_at(infl + 0.20))
    case(2, "ends 2.1pp above terminal — just outside the bound", True,
         path(infl + 0.021), grows_at(infl + 0.021))
    case(3, "ends far BELOW terminal (perpetual real decline at the boundary)", True,
         path(0.0), grows_at(0.0))
    case(4, "PHDC's own shape, 21.4% against a 7.0% terminal", True,
         path(0.214), grows_at(0.214))

    # ---- CLEAN: windows that have converged, which must NOT fire
    case(5, "ends exactly AT the terminal", False, path(infl), grows_at(infl))
    case(6, "ends 1.9pp above — just inside the bound", False,
         path(infl + 0.019), grows_at(infl + 0.019))
    case(7, "ends 1.9pp BELOW — just inside, the other side", False,
         path(infl - 0.019), grows_at(infl - 0.019))

    # ---- case 8: the bound is the house's, not a copy [R-ENF-03]
    src = open(C.__file__, encoding="utf-8").read()
    uses_house = "RP.HORIZON_CONVERGENCE" in src
    # a literal 0.02 anywhere in the refusal block would be a second bound
    blk = src.split("[R-MACRO-01]", 1)[-1][:2500] if "[R-MACRO-01]" in src else ""
    literal = re.search(r"\b0\.02\b", blk)
    if uses_house and not literal:
        ok += 1
    else:
        bad.append("8 the bound is imported — uses_house=%s, literal=%s"
                   % (uses_house, bool(literal)))

    print("convergence refusal negative control — %s %d/%d  (fixture %s %d, "
          "terminal %.2f%%)"
          % ("PASS" if not bad else "FAILED", ok, CASES, tk, y, 100 * infl))
    for b in bad:
        print("  - " + b)
    if ok + len(bad) != CASES:
        print("  - CASE COUNT: %d ran against a declared %d" % (ok + len(bad), CASES))
        return 1
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
