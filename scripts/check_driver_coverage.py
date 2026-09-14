"""Every published driver bias states the coverage behind it.  [R-ENF-01]

A DRIVER SCORED ON HALF ITS HISTORY PUBLISHES A BIAS THAT LOOKS EXACTLY LIKE ONE
SCORED ON ALL OF IT. The log score cannot take a cell where either side is
non-positive, so it drops them -- correctly, and silently -- and every run's record
then printed `n`, the count of cells the score TOOK, with the count that EXIST
nowhere. The two are the same number on revenue and cost, which are always
positive, and they come apart on precisely the bottom-line drivers a valuation
depends on.

MEASURED BEFORE THE FIELD EXISTED, by a census that had to be run by hand: across
the five runs, six of EGCH's fourteen drivers are scored on under HALF their cells,
including `net` and `pbt`, and one driver in the book carries a bias computed on
NONE of its fifty cells. Nothing in any record said so.

WHAT THIS GATE REQUIRES IS THE DISCLOSURE, NEVER A LEVEL. There is no threshold
here and there is deliberately not going to be one: a driver genuinely scored on
few cells is a fact about that company's history, not a defect, and a cutoff would
be the free parameter the PROMOTION RULE forbids. What a record may not do is go
QUIET about it -- which is [R-SIGCM-02]'s own shape, where a coarser level is
permitted and going quiet about it never is.

THE PAIR GOES WHERE THE READER LOOKS. The first cut put it on the internal
`drivers` block while every census reads `by_driver` — the disclosure in the
working papers and not on the page, which is the defect the field exists to close,
committed while closing it.

Population-anchored BOTH ways [R-ENF-04]: a run with no scores file is REPORTED,
a run examined with zero drivers read FAILS, and a pass having read no run at all
FAILS. `n_cells` is verified against the run's OWN committed per-cell file rather
than taken on trust, because a self-declared denominator is the self-attested
boolean this repository has closed everywhere else.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENG = os.path.join(ROOT, "engine")

# (ticker, directory, the per-cell setting the published bias is computed on)
RUNS = [
    ("AMOC", "amoc_walkforward", "asknown"),
    ("ARCC", "arcc_walkforward", "asknown"),
    ("EGCH", "egch_walkforward", "asknown"),
    ("TMGH", "tmgh_walkforward", "asknown"),
    ("PHDC", "phdc_walkforward", "as_known"),
]


def cell_counts(d, setting):
    """{driver: (scored, existing)} from the run's own committed per-cell file.

    Two shapes read as they are: a flat list carrying `setting`, and a dict keyed
    by setting whose rows name their fields differently.
    """
    path = os.path.join(ENG, d, "error_cells.json")
    if not os.path.exists(path):
        return None
    raw = json.load(open(path, encoding="utf-8"))
    scored, exists = {}, {}
    if isinstance(raw, list):
        rows = [r for r in raw if r.get("setting") == setting]
        dk, ek = "driver", "log_error"
    else:
        rows = raw.get(setting, [])
        dk, ek = "field", "e"
    for r in rows:
        d_ = r[dk]
        exists[d_] = exists.get(d_, 0) + 1
        if r.get(ek) is not None:
            scored[d_] = scored.get(d_, 0) + 1
    return {k: (scored.get(k, 0), v) for k, v in exists.items()}


def published(d):
    """{driver: record} from the block a reader and every census actually read."""
    path = os.path.join(ENG, d, "scores.json")
    if not os.path.exists(path):
        return None
    sc = json.load(open(path, encoding="utf-8"))
    blk = sc.get("by_driver")
    if not isinstance(blk, dict):
        return None
    return {k: v for k, v in blk.items() if isinstance(v, dict)}


def main():
    print("does every published driver bias state the coverage behind it?\n")
    runs_read = drivers_read = 0
    failures = []
    for name, d, setting in RUNS:
        pub = published(d)
        if pub is None:
            print("  %-6s no readable by_driver block — REPORTED, never skipped "
                  "[R-ENF-04]" % name)
            failures.append("%s: no readable by_driver block" % name)
            continue
        counts = cell_counts(d, setting)
        if counts is None:
            print("  %-6s no per-cell file to verify the denominator against" % name)
            failures.append("%s: no per-cell file" % name)
            continue
        runs_read += 1
        bad, under = [], []
        for drv, rec in sorted(pub.items()):
            drivers_read += 1
            n, nc = rec.get("n"), rec.get("n_cells")
            if not isinstance(n, int) or not isinstance(nc, int):
                bad.append("%s: n=%r n_cells=%r — the pair is the disclosure and "
                           "both halves are required" % (drv, n, nc))
                continue
            if n > nc:
                bad.append("%s: scored %d of %d — more cells taken than exist"
                           % (drv, n, nc))
                continue
            actual = counts.get(drv)
            if actual is None:
                bad.append("%s: published but absent from the per-cell file, so the "
                           "denominator cannot be verified" % drv)
                continue
            if (n, nc) != actual:
                bad.append("%s: record says %d of %d, the committed cells say %d of %d"
                           % (drv, n, nc, actual[0], actual[1]))
                continue
            if nc and n / nc < 0.5:
                under.append("%s %d/%d (%.0f%%)" % (drv, n, nc, 100 * n / nc))
        print("  %-6s %2d drivers, all carrying a verified pair" % (name, len(pub))
              if not bad else "  %-6s %2d drivers, %d PROBLEM(S)" % (name, len(pub), len(bad)))
        for b in bad:
            print("           %s" % b)
        if under:
            print("           DISCLOSED, not failed — scored on under half their "
                  "cells: %s" % ", ".join(under))
        failures.extend("%s %s" % (name, b) for b in bad)

    print("\n  %d run(s) read, %d driver(s) examined" % (runs_read, drivers_read))
    if not runs_read or not drivers_read:
        print("\nREFUSED — a run that examined nothing is not a run that found "
              "nothing [R-ENF-04].")
        return 1
    if failures:
        print("\nFAIL — a published bias whose coverage is unstated or unverifiable "
              "is not the evidence it is read as.")
        return 1
    print("\nOK — every published driver bias states the cells it was scored on and "
          "the cells that exist, and both reproduce from the run's own record.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
