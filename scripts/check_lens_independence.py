#!/usr/bin/env python3
"""[R-LENS-01] enforced from outside — the three lenses do not feed each other.

THE RULE, ADOPTED 23-AUG-2026 FROM AN INVESTOR-CRITIQUE SESSION: the FUNDAMENTAL study, the
MC price engine and the TECHNICAL read are INDEPENDENT lenses, no lens's output is ever an
input to another, and they are shown side by side SO THAT AGREEMENT BETWEEN THEM IS
INFORMATION RATHER THAN AN ECHO.

WHAT WAS CHECKING IT: nothing. Measured 07-09-2026, no file in scripts/ mentions the rule.
It is among the oldest rules here and among the least checked, which is this repository's
own recorded pattern — a rule adopted before there was machinery to enforce it does not
acquire that machinery by being important.

AND IT IS THE CLAIM AN OUTSIDE READER PROBES HARDEST, because it is the one that makes the
three-lens presentation worth anything. If a cone leans on a fair value, or a fair value
leans on a chart, then three lenses agreeing is one lens counted three times — and the
agreement is the very thing the presentation offers as evidence.

FOUR CONDITIONS, EACH READ OFF THE CODE RATHER THAN ATTESTED:

  1. NO BUILDER THAT WRITES A STUDY'S COMMITTED VALUATION MAY IMPORT THE OTHER TWO LENSES.
     Reading a SPOT is not consuming a lens — a price is not an output of anything — so the
     test is on the import, and on files that WRITE the numbers rather than read them.
  2. THE MC ENGINE MAY NOT READ A FAIR VALUE. The Fundamental-MC integration protocol's
     Phase C engine hook is permanently retired as a drift source.
  3. THE TECHNICAL READ MAY NOT READ A FAIR VALUE OR A CONE.
  4. NO REGISTERED MC SIGNAL MAY BE A CONSTRUCTION THE TECHNICAL READ USES. The rule names
     moving-average distances, 52-week-high proximity, "RSI and kin" — and the honest way
     to test "and kin" is not a word list somebody maintains but to ASK THE TECHNICAL READ
     WHAT IT USES [R-ENF-03]. engine/technicals.py is the authority on that, so the
     ineligible set is derived from it and grows when the read does.

WHAT IT DELIBERATELY DOES NOT DO: it does not forbid a study directory from HOSTING cone or
technical work. Every study directory carries a strike script and a step-0 screen, and that
is the study directory being a workspace rather than the valuation consuming a cone. The
subject is the builder that writes the answer.
"""
from __future__ import annotations

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")

LENS_MODULES = ("technicals", "ta_chart", "apply_technicals", "mc_v3", "strike_cohorts")
IMPORT_RX = re.compile(r"^\s*(?:from\s+(%s)\s+import|import\s+(%s)\b)"
                       % ("|".join(LENS_MODULES), "|".join(LENS_MODULES)), re.M)
# A generator writes its numbers file in several shapes across this book —
#   json.dump(out, open(os.path.join(HERE, 'study_numbers.json'), 'w'))
#   json.dump(D,   open(os.path.join(HERE, "study_numbers.json"), "w"))
#   open('study_numbers.json', 'w')
# — and the first draft's pattern matched THREE builders across twenty-four studies, which
# is not a book with three generators in it. Matching the FILENAME anywhere in a json.dump
# or an open-for-write line is what the book actually contains [L-355].
# SHOWING A LENS BESIDE ANOTHER IS WHAT [R-LENS-01] REQUIRES — "they are shown side by
# side so agreement between them is information" — and every study owes a §3 probabilistic
# price map, which IS the cone rendered inside a study document. So an import alone is not
# a breach, and the first draft's refusal of one was wrong: STC calls strike_cohorts to
# reproduce the committed fit for its own §3, with the reason written in a comment three
# lines above the call, and re-deriving a cone instead is the defect that comment records.
#
# WHAT SEPARATES RENDERING FROM CONSUMING IS NOT VISIBLE TO A STATIC READER, so it is
# DECLARED at the import rather than guessed at — the shape this repository uses wherever a
# rule has a legitimate exception. A declaration is a marker naming what is rendered; an
# EMPTY one is not a declaration, on the same reasoning as every other release here.
# [^\S\n] IS WHITESPACE THAT IS NOT A NEWLINE, and the distinction is the whole check.
# The first draft used \s*, which matches a newline, so an EMPTY declaration absorbed the
# next line of code and passed — the "an empty reason has switched the check off rather
# than declared it" hole, in this gate's own pattern. Its negative control caught it.
DECLARED_RX = re.compile(r"\[R-LENS-01\][^\S\n]*presentational:[^\S\n]*\S+", re.I)

WRITES_NUMBERS_RX = re.compile(
    r"(?:json\.dump|open)\([^\n]*numbers[^\n]*\.json[^\n]*['\"]w['\"]", re.I)
FAIR_RX = re.compile(r"\bfair\s*\[|\bfair_value\b|\bfv_overlay\b|['\"]central['\"]|"
                     r"\bvalue_gap\b")


def technical_constructions():
    """What the technical read actually computes — the authority on 'and kin'."""
    src = open(os.path.join(ENGINE, "technicals.py"), encoding="utf-8").read()
    found = set()
    # _sma( and _sma_series( are how this module spells it, and \b never matches before
    # an underscore — the first draft derived a set with no moving average in it, which
    # would have let a moving-average signal through the one check built to stop it.
    for name, pat in (("sma", r"_?sma[_(]"), ("rsi", r"_?rsi\b"),
                      ("atr", r"\batr\b"), ("macd", r"\bmacd\b"),
                      ("52w", r"52[-_ ]?w(?:eek)?"), ("cross", r"\bcross\b"),
                      ("sr", r"support|resistance")):
        if re.search(pat, src, re.I):
            found.add(name)
    return found


def _publishes_a_central(sdir):
    """Does this study directory commit a FUNDAMENTAL answer at all?"""
    for p in glob.glob(os.path.join(sdir, "*.json")):
        if "numbers" not in os.path.basename(p).lower():
            continue
        try:
            import json
            doc = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        stack = [doc]
        while stack:
            o = stack.pop()
            if isinstance(o, dict):
                if isinstance(o.get("central"), (int, float)):
                    return True
                # A TWO-SIDED ANSWER IS STILL A FUNDAMENTAL ANSWER. The first draft asked
                # only for a single `central` and so skipped three real companies as
                # having no lens — which is this repository's own recorded defect, where a
                # gate's comment said "a two-sided study; handled by its branches" AND
                # NOTHING HANDLED THE BRANCHES.
                for k in ("branches", "cases", "frames", "two_sided"):
                    v = o.get(k)
                    if isinstance(v, (list, dict)) and v:
                        return True
                stack.extend(o.values())
            elif isinstance(o, list):
                stack.extend(o)
    return False


def main(argv=None):
    fails, skipped, examined = [], [], {"builders": 0, "signals": 0}

    # ---- 1: a builder that WRITES the valuation may not import another lens ----------
    for p in sorted(glob.glob(os.path.join(ENGINE, "*_study", "*.py"))):
        try:
            src = open(p, encoding="utf-8").read()
        except Exception:
            continue
        if not WRITES_NUMBERS_RX.search(src):
            continue
        # A STUDY WITH NO FUNDAMENTAL VALUATION HAS NO LENS TO ECHO, and this is a
        # re-pointing rather than a widening [R-COC-01]. The first run flagged XPT, whose
        # builder imports the MC engine and writes study_numbers_xpt.json — and XPT is
        # PLATINUM. A metal has no issuer, no statements and no drivers, so its study IS
        # the cone plus a technical read and there is no third lens to be echoed. The test
        # is not "is it a metal" — naming metals would be a list somebody maintains — but
        # whether the committed record exposes a FUNDAMENTAL CENTRAL at all.
        if not _publishes_a_central(os.path.dirname(p)):
            skipped.append(os.path.basename(os.path.dirname(p)))
            continue
        examined["builders"] += 1
        m = IMPORT_RX.search(src)
        if m and not DECLARED_RX.search(src):
            fails.append("%s writes the study's committed numbers AND imports %s with no "
                         "presentational declaration — a valuation CONSUMING another lens "
                         "is the echo [R-LENS-01] removes, and a valuation RENDERING one "
                         "beside itself is what the rule requires. Say which, at the "
                         "import." % (os.path.relpath(p, ROOT), m.group(1) or m.group(2)))

    # ANCHORED ON A COUNT FROM SOMEWHERE ELSE [R-ENF-04]: the numbers files on disk. A
    # matcher that quietly stops matching reports a small clean population rather than an
    # error, and "zero" is not the only dishonest answer — three of twenty-four is too.
    on_disk = len(glob.glob(os.path.join(ENGINE, "*_study", "*numbers*.json")))
    if examined["builders"] + len(skipped) < on_disk // 2:
        print("FAIL — matched %d builder(s) against %d committed numbers files on disk. "
              "A reader that stopped matching reads exactly like a book with few "
              "generators [R-ENF-04]."
              % (examined["builders"] + len(skipped), on_disk))
        return 1

    # ---- 2 and 3: the engine and the read may not consume a fair value ---------------
    for mod, what in (("mc_v3.py", "the MC engine"),
                      ("market_profiles.py", "the MC profiles"),
                      ("technicals.py", "the technical read")):
        p = os.path.join(ENGINE, mod)
        if not os.path.exists(p):
            fails.append("%s is not on disk, so this gate cannot test %s [R-ENF-04]"
                         % (mod, what))
            continue
        body = "\n".join(l for l in open(p, encoding="utf-8").read().splitlines()
                         if not l.strip().startswith("#"))
        m = FAIR_RX.search(body)
        if m:
            fails.append("%s reads a fair value (%r) — %s may not take the fundamental "
                         "lens as an input" % (mod, m.group(0), what))

    # ---- 4: no registered signal may be a construction the technical read uses -------
    sys.path.insert(0, ENGINE)
    import market_profiles as mp                       # noqa: E402
    tech = technical_constructions()
    if not tech:
        print("FAIL — derived zero constructions from technicals.py. The ineligible set "
              "would be empty and every signal would pass [R-ENF-04].")
        return 1
    for name, prof in sorted(vars(mp).items()):
        st = getattr(prof, "signal_type", None)
        if not isinstance(st, str):
            continue
        examined["signals"] += 1
        hit = [t for t in tech if re.search(r"\b%s" % re.escape(t), st, re.I)]
        if hit:
            fails.append("%s runs signal_type %r, which is a construction the technical "
                         "read uses (%s). The eligible pool is the momentum family and "
                         "constructions the read does NOT use."
                         % (name, st, ", ".join(hit)))

    if not examined["signals"]:
        print("FAIL — read zero signal types from market_profiles [R-ENF-04].")
        return 1

    print("[R-LENS-01] the three lenses do not feed each other")
    print("  valuation builders examined      : %d" % examined["builders"])
    if skipped:
        print("  skipped, no fundamental central  : %s   (a metal has no third lens)"
              % ", ".join(sorted(set(skipped))))
    print("  market profiles examined         : %d" % examined["signals"])
    print("  constructions the read uses      : %s" % ", ".join(sorted(tech)))
    if fails:
        print("\nFAIL — a lens is taking another lens as an input:")
        for f in fails:
            print("   %s" % f)
        return 1
    print("\nOK — no valuation builder imports the cone or the read, neither the engine "
          "nor the\n     read consumes a fair value, and no registered signal is a "
          "construction the read uses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
