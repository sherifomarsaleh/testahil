"""What criterion 3's GATING clauses would read if they were put on series (b).

THIS MEASURES AN OPTION. IT ADOPTS NOTHING. No clause moves, no verdict changes, no
fair value is touched: criterion3.py still gates Phase 1 on series (a), and this prints
what the same four clauses WOULD say against the delivered cross-section instead, so the
choice between them is made on figures rather than on an expectation.

WHY THE QUESTION EXISTS. [R-ENF-01 EXTENDED 18-09-2026] added the convergence refusal to
the mechanical lens and the declared run went to ZERO admissible cells, so clauses A, B,
C and F are UNMEASURED — not failed, which is a different and worse thing to act on. The
three ways out are (a) capitalise the growth each window ends at, (b) declare a fade to
terminal, (c) put the gating clauses on the fair values this house actually published.
(a) and (b) each need a number nobody has tested, which the PROMOTION RULE forbids; (c)
needs no new number and its cost is that the sample changes shape — ONE OBSERVATION PER
NAME RATHER THAN ONE PER ORIGIN.

THE CLAUSES ARE IMPORTED, NEVER RE-IMPLEMENTED [R-ENF-03]: the same _covers_zero and the
same sign tests criterion3.py applies, fed a different series. What differs is only what
the series IS, which is the whole subject of the comparison.

READ THE VERDICTS THE SAME WAY criterion3 does: an UNMEASURED clause is UNMEASURED and
never met [R-ENF-04], and a clause whose object does not exist says so rather than
returning a number about something else.
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "engine", "valuation_calibration"))
sys.path.insert(0, HERE)

import delivered as D          # noqa: E402
import criterion3 as C3        # noqa: E402

# THE ERA BOUNDARY IS THIS BOOK'S OWN AND IS NOT CHOSEN HERE: every era label in this
# repository is the year the market's currency moved, which for Egypt is 2022. Picking a
# different cut for this series would be the selection [R-FCAL-01 AMENDED] forbids in
# terms — the one that makes a bias look stable, or the one that makes it look unstable.
ERA_BOUNDARY = 2022


def series():
    """The delivered cross-section: one log(FV/P) per name, with its strike date."""
    rows, nonpositive, unreadable, two_sided = D.read_book()
    return rows, nonpositive, unreadable, two_sided


def clause_a(rows):
    """Pooled contemporaneous bias, interval covering zero."""
    xs = [r["log_gap"] for r in rows]
    if len(xs) < 2:
        return None, ["fewer than two observations: no interval to place"]
    mean = sum(xs) / len(xs)
    by_name = D.boot(xs)
    by_mkt = D.boot_clustered(rows)
    lines = ["mean log(FV/P) %+.4f on %d names  (%.1f%% in price terms)"
             % (mean, len(xs), (math.exp(mean) - 1.0) * 100.0)]
    out = []
    # delivered.boot returns a (lo, hi) TUPLE and criterion3._covers_zero reads a DICT.
    # Adapted here rather than either side changed: two modules that already work are not
    # rewritten to suit a third that only reads them.
    for label, b in (("resampling NAMES", by_name), ("resampling MARKETS", by_mkt)):
        lo, hi = (b if isinstance(b, (tuple, list)) else (b.get("lo"), b.get("hi")))
        if lo is None or hi is None or lo != lo or hi != hi:
            lines.append("%-20s no interval" % label)
            out.append(None)
            continue
        cov = C3._covers_zero({"lo": lo, "hi": hi})
        lines.append("%-20s %+.4f to %+.4f   %s zero"
                     % (label, lo, hi, "COVERS" if cov else "EXCLUDES"))
        out.append(cov)
    if any(o is None for o in out):
        return None, lines
    return all(out), lines


def clause_b(rows):
    """Leave one NAME out: does the pooled mean keep its sign?

    The criterion says LONO, and on series (a) that means leaving out a name with several
    origins behind it. Here a name IS one observation, so this is the same test on a
    thinner sample and it says so rather than pretending otherwise.
    """
    xs = [r["log_gap"] for r in rows]
    if len(xs) < 3:
        return None, ["fewer than three observations: leaving one out leaves no pool"]
    means = {}
    for i, r in enumerate(rows):
        rest = xs[:i] + xs[i + 1:]
        means[r["ticker"]] = sum(rest) / len(rest)
    signs = {(m > 0) for m in means.values()}
    worst = sorted(means.items(), key=lambda kv: kv[1])
    lines = ["%d leave-one-out means, %+.4f to %+.4f"
             % (len(means), worst[0][1], worst[-1][1]),
             "most negative without %s  %+.4f" % (worst[0][0], worst[0][1]),
             "least negative without %s  %+.4f" % (worst[-1][0], worst[-1][1])]
    return len(signs) == 1, lines


def clause_c(rows):
    """Does it hold in BOTH eras?

    THE ANSWER IS STRUCTURAL RATHER THAN EMPIRICAL AND THAT IS THE POINT OF RUNNING IT:
    every delivered fair value in this book was struck in 2026, so the cross-section sits
    entirely on one side of this market's own era boundary. There is no second side for a
    sign to hold in, and no amount of further work on these sixteen names creates one —
    a second era needs vintages struck before the currency moved, which this house did not
    publish and cannot now go back and publish.
    """
    eras = {}
    for r in rows:
        y = None
        for key in ("spot_date", "date", "struck"):
            v = r.get(key)
            if isinstance(v, str) and len(v) >= 4 and v[:4].isdigit():
                y = int(v[:4])
                break
        label = "unknown" if y is None else ("pre-%d" % ERA_BOUNDARY if y < ERA_BOUNDARY
                                             else "%d+" % ERA_BOUNDARY)
        eras.setdefault(label, []).append(r["log_gap"])
    lines = ["%-10s %3d name(s)  mean %+.4f" % (k, len(v), sum(v) / len(v))
             for k, v in sorted(eras.items())]
    if len(eras) < 2:
        return None, lines + [
            "ONLY ONE ERA IS POPULATED, and it is not a sampling accident: every "
            "delivered fair value in this book was struck in 2026. 'Both eras' has no "
            "second side here and cannot acquire one — the vintages that would carry it "
            "were never published.",
            "SO ADOPTING SERIES (b) MEANS AMENDING THIS CLAUSE IN TERMS, not reading it "
            "as satisfied. An unmeasured clause is UNMEASURED [R-ENF-04]."]
    signs = {(sum(v) / len(v) > 0) for v in eras.values()}
    return len(signs) == 1, lines


def main():
    rows, nonpositive, unreadable, two_sided = series()
    print("CRITERION 3's GATING CLAUSES, PUT ON SERIES (b) — A MEASUREMENT, NOT AN ADOPTION")
    print("=" * 78)
    print("  series (b): the fair values this house published, each against the spot it")
    print("  was struck at. %d scoreable, %d non-positive, %d two-sided, %d unreadable."
          % (len(rows), len(nonpositive), len(two_sided), len(unreadable)))
    print()
    verdicts = {}
    for name, fn in (("A  pooled bias covers zero", clause_a),
                     ("B  LONO-stable in sign", clause_b),
                     ("C  holds in both eras", clause_c)):
        met, lines = fn(rows)
        verdicts[name[0]] = met
        tag = "MET" if met else ("UNMEASURED" if met is None else "NOT MET")
        print("  %-28s %s" % (name, tag))
        for l in lines:
            print("        " + l)
        print()
    met_f, lines_f = C3.clause_f(verdicts.get("A"))
    verdicts["F"] = met_f
    print("  %-28s %s" % ("F  residual bias named",
                          "MET" if met_f else ("UNMEASURED" if met_f is None
                                               else "NOT MET")))
    for l in lines_f:
        print("        " + l)
    print()
    print("=" * 78)
    blocking = [k for k, v in sorted(verdicts.items()) if v is not True]
    if not blocking:
        print("  ALL FOUR GATING CLAUSES WOULD READ MET on series (b).")
    else:
        print("  WOULD NOT CLOSE PHASE 1 ON ITS OWN. Clause(s) %s do not read MET."
              % ", ".join(blocking))
        print("  Adopting series (b) therefore means amending those clauses IN TERMS and")
        print("  stating the cost, which is the principal's call and not a reading of the")
        print("  existing text. NOTHING HERE IS ADOPTED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
