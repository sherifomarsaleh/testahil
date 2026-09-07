#!/usr/bin/env python3
"""Negative control for check_record_survives_rebuild.py.

EIGHT CONDITIONS, FIVE RED AND THREE CLEAN, and the clean half is what this gate got wrong
twice before it was right. A study that appends a record with a SECOND declared script must
NOT fire — the first draft ran only the main generator and reported SAVOLA and SWDY losing
forecast_anchor, against a docstring saying in capitals that running compute.py alone
deletes it. And a study whose second writer is a RESTORE GUARD must not read as having an
undeclared run order — the first draft reported FERTIGLOBE unreadable on exactly that.

The fixtures are small real generators rather than copies of the book, because what is
under test is the RULE — does a rebuild of the declared chain keep what was committed — and
copying a study in would only add ways for the test to fail for reasons that are not the
rule's. Every mutation asserts it landed. Nothing is written into the real tree.
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
CASES = 8

# THE TALLY IS A SHARED INSTRUMENT, NOT A LINE EACH CONTROL PRINTS FOR ITSELF.
# Six controls here printed the DECLARED CONSTANT twice — "cases run: N
# (declared N)" — which is true whatever ran, and beside it a hand-typed red/clean
# split that had stopped matching. engine/control_tally.py counts what actually
# ran and refuses a count that moved [R-ENF-04].
sys.path.insert(0, ROOT)
from engine.control_tally import Tally          # noqa: E402

T = Tally(CASES, subject="check_record_survives_rebuild.py")

MAIN = '''"""%s"""
import json, os
D = {"central": 1.23, "wacc": 0.11}
json.dump(D, open(os.path.join(os.path.dirname(__file__), "study_numbers.json"), "w"),
          indent=1)
'''
APPEND = '''import json, os
p = os.path.join(os.path.dirname(__file__), "study_numbers.json")
D = json.load(open(p))
D["forecast_anchor"] = {"latest_reviewed_date": "2026-06-30"}
json.dump(D, open(p, "w"), indent=1)
'''
GUARD = '''import json, os
import numbers_generators as ng
p = os.path.join(os.path.dirname(__file__), "study_numbers.json")
_B = ng.guard(p)
ng.guard(p, _B)
'''


def build(tmp, files, committed, ratchet):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
    eng = os.path.join(repo, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "check_record_survives_rebuild.py"),
                os.path.join(repo, "scripts", "check_record_survives_rebuild.py"))
    shutil.copy(os.path.join(ENGINE, "numbers_generators.py"),
                os.path.join(eng, "numbers_generators.py"))
    sd = os.path.join(eng, "aaa_study")
    os.makedirs(sd, exist_ok=True)
    for n, body in files.items():
        open(os.path.join(sd, n), "w", encoding="utf-8").write(body)
    json.dump(committed, open(os.path.join(sd, "study_numbers.json"), "w",
                              encoding="utf-8"), indent=1)
    json.dump(ratchet, open(os.path.join(eng, "build_depth_audit",
                                         "record_survives_outstanding.json"), "w",
                            encoding="utf-8"), indent=1)
    return repo, sd


def run(repo):
    p = subprocess.run([sys.executable, os.path.join(
        repo, "scripts", "check_record_survives_rebuild.py"), "--timeout", "120"],
        capture_output=True, text=True, cwd=repo, timeout=600)
    return p.returncode != 0, (p.stdout + p.stderr)


def case(name, files, committed, ratchet, expect_red, landed, results):
    T.case(name, expect_red)
    tmp = tempfile.mkdtemp(prefix="rsr_nc_")
    try:
        repo, sd = build(tmp, files, committed, ratchet)
        ok, why = landed(sd)
        if not ok:
            results.append((name, "MUTATION DID NOT LAND: " + why))
            return
        red, out = run(repo)
        if red != expect_red:
            results.append((name, "expected %s, got %s\n%s"
                            % ("RED" if expect_red else "GREEN",
                               "RED" if red else "GREEN", out[-600:])))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    r = []
    NODECL = MAIN % "writes the numbers file whole"
    DECL = MAIN % "RUN ORDER: compute.py THEN anchor.py. Running this file alone deletes it."
    KEEP = {"central": 1.23, "wacc": 0.11}
    PLUS = dict(KEEP, forecast_anchor={"latest_reviewed_date": "2026-06-30"})

    # ---------- RED ----------
    case("1 a committed record the sole generator does not write",
         {"compute.py": NODECL}, PLUS, {}, True,
         lambda sd: ("forecast_anchor" not in open(os.path.join(sd, "compute.py")).read(),
                     "the generator writes the record after all"), r)

    case("2 two writers, no declared run order — which rebuild is the rebuild?",
         {"compute.py": NODECL, "anchor.py": APPEND}, PLUS, {}, True,
         lambda sd: ("RUN ORDER" not in open(os.path.join(sd, "compute.py")).read()
                     and os.path.exists(os.path.join(sd, "anchor.py")),
                     "an order was declared, or the second writer is absent"), r)

    case("3 a generator that will not run",
         {"compute.py": "raise SystemExit('deliberately broken')\n"}, KEEP, {}, True,
         lambda sd: ("deliberately broken" in open(os.path.join(sd, "compute.py")).read(),
                     "the generator was not broken"), r)

    case("4 no script writes the numbers file at all",
         {"notes.py": "X = 1\n"}, KEEP, {}, True,
         lambda sd: (not os.path.exists(os.path.join(sd, "compute.py")),
                     "a generator survived"), r)

    case("5 a LISTED study that now loses MORE than the ratchet records",
         {"compute.py": NODECL}, dict(PLUS, lens_record={"class": "x"}),
         {"outstanding": {"AAA": {"gen": "compute.py", "keys": ["forecast_anchor"],
                                  "why": "seeded"}}}, True,
         lambda sd: ("lens_record" in open(os.path.join(sd,
                                                        "study_numbers.json")).read(),
                     "the second record was not committed"), r)

    # ---------- CLEAN ----------
    case("6 a DECLARED two-step build keeps what the second step appends",
         {"compute.py": DECL, "anchor.py": APPEND}, PLUS, {}, False,
         lambda sd: ("RUN ORDER" in open(os.path.join(sd, "compute.py")).read()
                     and "anchor.py" in open(os.path.join(sd, "compute.py")).read(),
                     "the run order was not declared"), r)

    case("7 a second writer that is a RESTORE GUARD is not a second generator",
         {"compute.py": NODECL, "diagnostics.py": GUARD}, KEEP, {}, False,
         lambda sd: (os.path.exists(os.path.join(sd, "diagnostics.py"))
                     and "guard(" in open(os.path.join(sd, "diagnostics.py")).read(),
                     "the guard fixture is not a guard"), r)

    case("8 a single generator that writes everything it committed",
         {"compute.py": NODECL}, KEEP, {}, False,
         lambda sd: (json.load(open(os.path.join(sd, "study_numbers.json"))) == KEEP,
                     "the committed file is not the plain one"), r)

    return T.report(r)


if __name__ == "__main__":
    sys.exit(main())
