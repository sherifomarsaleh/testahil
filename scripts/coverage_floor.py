#!/usr/bin/env python3
"""coverage_floor.py — a gate must never report clean having examined nothing.  [R-ENF-04]

WHY THIS EXISTS
---------------
Adopted 25-Aug-2026 after the same failure shape appeared FOUR times in one
session, each time nearly reported as a clean result:

  * a local `origin/main` ref, 24 commits stale, read as current — and produced
    a confident, wrong "this was never merged";
  * an Actions query keyed on a TRUNCATED commit SHA returned `0 runs`, which
    read as "no failures" when it meant "the query matched nothing";
  * a negative control that searched for `"EMFD"` while data.js writes keys
    UNQUOTED — it modified nothing, the gate went green, and that green was
    evidence only that the file was untouched;
  * a `gh` route declared impossible on the strength of `command -v gh` — the
    binary installs from apt in one line, and the route then failed for a
    completely different and more informative reason.

None of these were wrong ANSWERS. They were absent answers wearing the costume
of a clean one, which is strictly worse: a failure announces itself, an empty
result does not. The repository already carries two rules of exactly this
species — COUNT AGAINST A KNOWN TOTAL, never trust a tool's own "0 skipped",
and VERIFY BY IMPORT, NOT BY PARSE — each adopted after its own incident and
neither generalised. [R-ENF-01] says that when a defect of this species is found
again, close the CLASS. This is that.

WHAT IT DOES
------------
Measured on adoption day by emptying `assets/data.js` to a valid, loadable file
with zero entries and running every gate: `check_page_integrity`,
`check_data_freshness` and `check_technical_read` ALL EXITED 0 AND REPORTED
CLEAN. They were not broken — they faithfully checked every one of nothing.

So each gate now declares what it examined and is held against a population
counted from a DIFFERENT PLACE. The anchor is the persistent OHLC library on
disk (`engine/raw_ohlc/{MARKET}/{TICKER}.csv`), chosen because it is
independent of `data.js` — defeating this check would mean emptying the
libraries too, which is a far louder failure than an empty page file.

The rule is EXACT, not a threshold: a threshold would be a free parameter with
no evidence behind it, which this protocol forbids elsewhere for the same
reason. Every library must be covered. A library staged but not yet published
therefore FAILS the gate and says so by name — that is the intended behaviour,
not a false alarm: "counting one side alone is what let 9 names rot unnoticed"
is already written in check_data_freshness's own check 1.
"""
from __future__ import annotations

import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'engine', 'raw_ohlc')


def library_population() -> int:
    """Covered instruments, counted from the persistent library, not from data.js."""
    return len(glob.glob(os.path.join(RAW, '*', '*.csv')))


def assert_examined(n_examined: int, tool: str, unit: str = 'entries') -> int:
    """Fail unless this run examined the whole covered population.

    Returns the population so a caller can print it. Raises SystemExit — it
    never warns, per [R-ENF-01]: a check that warns is one everyone learns to
    ignore.
    """
    expected = library_population()
    if expected == 0:
        raise SystemExit(
            f'{tool}: FAIL — no OHLC libraries under engine/raw_ohlc/. The '
            'population this gate is measured against is itself empty, so a '
            'clean result here would mean nothing. Refusing to report one.')
    if n_examined == 0:
        raise SystemExit(
            f'{tool}: FAIL — examined 0 {unit} while {expected} libraries exist. '
            'A gate that checked nothing must not report clean; that is the '
            'defect [R-ENF-04] exists to close.')
    if n_examined < expected:
        raise SystemExit(
            f'{tool}: FAIL — examined {n_examined} {unit} but {expected} '
            'instruments have a library on disk. Every covered name must be '
            'reached, or the gate is reporting on a subset while looking '
            'complete. Name the missing ones or remove their libraries.')
    return expected
