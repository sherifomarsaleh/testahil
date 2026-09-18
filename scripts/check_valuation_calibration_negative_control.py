"""Negative control for the pre-registration order gate.

Each case is built as a REAL git repository, because the thing under test is
commit order and a fixture that fakes it would be testing the fixture.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "check_valuation_calibration.py")
PREG = "PRE_REGISTRATION_03-09-2026.md"
BODY = "the design, fixed before any data existed\n"


def git(d, *a):
    return subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)


PREG2 = "PRE_REGISTRATION_18-09-2026.md"
BODY2 = "the second design, superseding the first and saying so\n"


def build(tmp, order="preg_first", seal=True, seal_ok=True, commit_preg=True,
          add_score=True, shallow=False, supersede=False, seal2_ok=True,
          edit_old_after=False):
    calib = os.path.join(tmp, "engine", "valuation_calibration")
    os.makedirs(calib)
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(GATE, os.path.join(tmp, "scripts",
                                   "check_valuation_calibration.py"))
    git(tmp, "init", "-q")
    git(tmp, "config", "user.email", "t@t"); git(tmp, "config", "user.name", "t")
    open(os.path.join(tmp, "README"), "w").write("x")
    git(tmp, "add", "-A"); git(tmp, "commit", "-qm", "root")

    def write_preg():
        open(os.path.join(calib, PREG), "w").write(BODY)
        if seal:
            h = hashlib.sha256(BODY.encode()).hexdigest()
            if not seal_ok:
                h = "0" * 64
            json.dump({"sha256": h},
                      open(os.path.join(calib, "PRE_REGISTRATION_HASH.json"), "w"))
        if commit_preg:
            git(tmp, "add", os.path.join("engine", "valuation_calibration", PREG))
            git(tmp, "add", os.path.join("engine", "valuation_calibration",
                                         "PRE_REGISTRATION_HASH.json"))
            git(tmp, "commit", "-qm", "prereg")

    def write_score():
        # Only the score path, so a case that deliberately leaves the
        # pre-registration uncommitted does not have it swept in by `add -A`.
        # The first version of this control did exactly that and its
        # "never committed" case passed a gate that should have failed it.
        open(os.path.join(calib, "SCORES_2026.json"), "w").write("{}")
        git(tmp, "add", os.path.join("engine", "valuation_calibration",
                                     "SCORES_2026.json"))
        git(tmp, "commit", "-qm", "scores")

    def write_preg2():
        """A SECOND dated pre-registration, committed AFTER the first score.

        This is the shape the sealed document itself prescribes for a correction, and
        the first version of this gate made it impossible — it held every score against
        the LATEST document, so the moment a second existed, a score correctly produced
        under the first became "a score that predates its design". The clean case below
        is that exact history and it must PASS.
        """
        open(os.path.join(calib, PREG2), "w").write(BODY2)
        rec = {"file": PREG2,
               "sha256": ("0" * 64 if not seal2_ok
                          else hashlib.sha256(BODY2.encode()).hexdigest()),
               "superseded": [{"file": PREG,
                               "sha256": hashlib.sha256(BODY.encode()).hexdigest()}]}
        json.dump(rec, open(os.path.join(calib, "PRE_REGISTRATION_HASH.json"), "w"))
        if edit_old_after:
            # THE SUPERSEDED DOCUMENT IS WHERE A RATIONALISATION WOULD GO: it is the
            # design the earlier scores claim to follow, and nobody looks at it again.
            open(os.path.join(calib, PREG), "w").write(
                BODY + "and a sentence added later\n")
        git(tmp, "add", os.path.join("engine", "valuation_calibration"))
        git(tmp, "commit", "-qm", "prereg2")

    if order == "preg_first":
        write_preg()
        if add_score:
            write_score()
        if supersede:
            write_preg2()
    else:
        if add_score:
            write_score()
        write_preg()
        if supersede:
            write_preg2()
    if shallow:
        open(os.path.join(tmp, ".git", "shallow"), "w").write("")


def run_case(name, kwargs, must_fail, results):
    tmp = tempfile.mkdtemp(prefix="vcal-")
    try:
        build(tmp, **kwargs)
        r = subprocess.run([sys.executable, os.path.join(
            tmp, "scripts", "check_valuation_calibration.py")],
            capture_output=True, text=True, timeout=300)
        red = r.returncode != 0
        ok = (red == must_fail)
        results.append(ok)
        print("  %-56s %s   exit %d   %s"
              % (name[:56], "ok  " if ok else "MISS", r.returncode,
                 (r.stdout.strip().splitlines() or [""])[-1][:56]))
        if not ok:
            for line in (r.stdout + r.stderr).strip().splitlines()[-6:]:
                print("        " + line[:150])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("pre-registration order gate — negative control")
    res = []
    run_case("a score committed BEFORE the pre-registration",
             {"order": "score_first"}, True, res)
    run_case("the pre-registration edited after it was sealed",
             {"seal_ok": False}, True, res)
    run_case("no seal at all — an edit would leave no trace",
             {"seal": False}, True, res)
    run_case("the pre-registration exists but was never committed",
             {"commit_preg": False}, True, res)
    run_case("a SHALLOW clone, where order cannot be read",
             {"shallow": True}, True, res)

    run_case("CLEAN — pre-registration first, then a score, must PASS",
             {}, False, res)
    run_case("CLEAN — sealed and committed, no scores yet, must PASS",
             {"add_score": False}, False, res)

    # ---- the supersession clauses, added 18-09-2026 with the gate change -------
    run_case("CLEAN — score under design 1, design 2 committed LATER, must PASS",
             {"supersede": True}, False, res)
    run_case("a SUPERSEDED pre-registration edited after its seal",
             {"supersede": True, "edit_old_after": True}, True, res)
    run_case("the SUPERSEDING document's own seal does not match",
             {"supersede": True, "seal2_ok": False}, True, res)
    run_case("a score before BOTH designs, with a supersession present",
             {"order": "score_first", "supersede": True}, True, res)

    tmp = tempfile.mkdtemp(prefix="vcal-")
    try:
        os.makedirs(os.path.join(tmp, "scripts"))
        shutil.copy(GATE, os.path.join(tmp, "scripts",
                                       "check_valuation_calibration.py"))
        r = subprocess.run([sys.executable, os.path.join(
            tmp, "scripts", "check_valuation_calibration.py")],
            capture_output=True, text=True, timeout=120)
        ok = r.returncode != 0
        res.append(ok)
        print("  %-56s %s   exit %d" % ("no calibration directory at all",
                                        "ok  " if ok else "MISS", r.returncode))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if all(res):
        print("negative control OK — the gate goes red on every injected defect "
              "and stays green on every clean case")
        return 0
    print("NEGATIVE CONTROL FAILED — %d of %d cases came back wrong."
          % (sum(1 for r in res if not r), len(res)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
