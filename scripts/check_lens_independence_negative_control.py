#!/usr/bin/env python3
"""Negative control for [R-LENS-01]. The property is TRUE today, so this is the evidence.

The gate is green on the book as it stands: no valuation builder consumes another lens,
neither the engine nor the read reads a fair value, and every registered signal is
momentum-family. A gate that has only ever been seen green is indistinguishable from one
that cannot go red, and this rule is the claim an outside reader probes hardest — three
lenses agreeing is one lens counted three times if they are not independent.

FOUR OF THE CASES ARE THE GATE'S OWN FIRST-DRAFT MISTAKES, kept because each was a real
misreading and the fixture is what stops it coming back: a metal skipped correctly, a
TWO-SIDED study that must NOT be skipped, a declared presentational use that must stay
green, and a builder population too small to believe.

Everything runs in a sandbox built from scratch; the real tree is never written to.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")

DECLARED_CASES = 13

GEN = ("import json, os\nHERE = os.path.dirname(__file__)\n%s\n"
       "json.dump({'central': 1.0}, open(os.path.join(HERE, 'study_numbers.json'), 'w'))\n")


def sandbox(builders, engine_edits=None, profile_signal=None, tech_body=None,
            orphan_numbers=0):
    tmp = tempfile.mkdtemp(prefix="lensind_nc_")
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"))
    os.makedirs(os.path.join(repo, "engine"))
    shutil.copy(os.path.join(HERE, "check_lens_independence.py"),
                os.path.join(repo, "scripts", "check_lens_independence.py"))
    # the three modules the gate reads
    open(os.path.join(repo, "engine", "technicals.py"), "w").write(
        tech_body if tech_body is not None else
        "def _sma(x,n): pass\ndef _rsi(x): pass\natr=1\nmacd=1\n"
        "# 52-week range, cross recency, support and resistance\n")
    open(os.path.join(repo, "engine", "mc_v3.py"), "w").write(
        (engine_edits or {}).get("mc_v3", "def simulate(): pass\n"))
    open(os.path.join(repo, "engine", "market_profiles.py"), "w").write(
        "class P:\n    def __init__(s,t): s.signal_type=t\n"
        + "\n".join("%s = P(%r)" % (m, profile_signal or "mom_combo")
                    for m in ("EGYPT", "UAE", "SAUDI")) + "\n")
    for tk, (body, has_central) in builders.items():
        d = os.path.join(repo, "engine", "%s_study" % tk.lower())
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "compute.py"), "w").write(GEN % body)
        json.dump(has_central, open(os.path.join(d, "study_numbers.json"), "w"))
    for i in range(orphan_numbers):
        d = os.path.join(repo, "engine", "orphan%02d_study" % i)
        os.makedirs(d, exist_ok=True)
        json.dump(CENTRAL, open(os.path.join(d, "study_numbers.json"), "w"))
    return tmp, repo


def run(repo):
    r = subprocess.run([sys.executable, "scripts/check_lens_independence.py"],
                       cwd=repo, capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


CENTRAL = {"central": 1.0}
TWO_SIDED = {"branches": [{"label": "A", "value": 1.0}, {"label": "B", "value": 2.0}]}
METAL = {"price": 1.0, "path": [1, 2]}

# enough clean builders that the population anchor is satisfied in every case
def bulk(n, body="pass"):
    return {"CLEAN%02d" % i: (body, CENTRAL) for i in range(n)}


CASES = []
def case(name, builders, expect_fail, must_say=None, **kw):
    CASES.append((name, builders, expect_fail, must_say, kw))


# ---- RED ---------------------------------------------------------------
case("a valuation builder importing the technical read, undeclared",
     dict(bulk(6), BAD=("import technicals", CENTRAL)), True, "BAD")
case("a valuation builder importing the MC engine, undeclared",
     dict(bulk(6), BAD=("import mc_v3", CENTRAL)), True, "BAD")
case("an EMPTY presentational declaration is not a declaration",
     dict(bulk(6), BAD=("import mc_v3\n# [R-LENS-01] presentational:", CENTRAL)),
     True, "BAD")
case("the MC engine reading a fair value",
     bulk(6), True, "mc_v3", engine_edits={"mc_v3": "fv = d['central']\n"})
case("the technical read reading a fair value",
     bulk(6), True, "technicals",
     tech_body="def _sma(x,n): pass\ndef _rsi(x): pass\natr=1\nmacd=1\n"
               "# 52-week, cross, support resistance\nfair_value = 1.0\n")
case("a profile running an RSI signal",
     bulk(6), True, "rsi", profile_signal="rsi_reversal")
case("a profile running a moving-average-distance signal",
     bulk(6), True, "sma", profile_signal="sma_distance")
case("technicals.py yielding no constructions — the derivation broke",
     bulk(6), True, "zero constructions", tech_body="# nothing here\n")
# THIS FIXTURE HAD TO BE REBUILT: the first version planted one builder and one numbers
# file, so on-disk was 1 and the anchor never tripped — a case that never injected its
# condition and reported green, which is the failure this project has now been bitten by
# five times. It now plants numbers files with NO builder beside them, which is the state
# a matcher that stopped matching would actually produce.
case("too few builders matched against the numbers files on disk",
     {"ONE": ("pass", CENTRAL)}, True, "reads exactly like", orphan_numbers=12)

# ---- CLEAN -------------------------------------------------------------
case("STC's shape — an import WITH a presentational declaration",
     dict(bulk(6), STC=("import strike_cohorts as SC\n"
                        "# [R-LENS-01] presentational: renders the committed cone in §3",
                        CENTRAL)), False)
case("a metal with no fundamental central is skipped, not failed",
     dict(bulk(6), XPT=("import mc_v3", METAL)), False)
case("a TWO-SIDED study is IN scope and clean",
     dict(bulk(6), EGCH=("pass", TWO_SIDED)), False)
case("momentum signals are the eligible pool",
     bulk(6), False, profile_signal="mom_12_1")


def main():
    print("[R-LENS-01] negative control — the property holds today, so this is the "
          "evidence\n")
    assert len(CASES) == DECLARED_CASES, (
        "case count moved: %d present, %d declared" % (len(CASES), DECLARED_CASES))
    bad = 0
    for name, builders, expect, must_say, kw in CASES:
        tmp, repo = sandbox(builders, **kw)
        try:
            # ASSERT THE FIXTURE LANDED
            for tk, (body, _) in builders.items():
                src = open(os.path.join(repo, "engine", "%s_study" % tk.lower(),
                                        "compute.py")).read()
                assert body.splitlines()[0] in src, "MUTATION DID NOT LAND for %s" % tk
            if kw.get("orphan_numbers"):
                import glob as _g
                n = len(_g.glob(os.path.join(repo, "engine", "*_study",
                                             "*numbers*.json")))
                assert n > 2 * len(builders), (
                    "CONDITION NOT INJECTED: %d numbers files against %d builders is not "
                    "a population a matcher has stopped matching" % (n, len(builders)))
            rc, out = run(repo)
            got = (rc != 0)
            said = (must_say.lower() in out.lower()) if must_say else True
            ok = (got == expect) and said
            print("  %-6s [%s] %s" % ("ok" if ok else "WRONG",
                                      "RED" if expect else "CLEAN", name[:70]))
            if not ok:
                bad += 1
                print("         exit %d  says %r: %s" % (rc, must_say, said))
        except AssertionError as e:
            print("  FIXTURE %s -- %s" % (name[:56], e))
            bad += 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d case(s): %d red-expected, %d clean-expected"
          % (len(CASES), sum(1 for c in CASES if c[2]),
             sum(1 for c in CASES if not c[2])))
    if bad:
        print("FAIL — %d case(s) did not behave as declared." % bad)
        return 1
    print("OK — fires on every way a lens could feed another, and on none of the ways "
          "they are legitimately shown side by side.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
