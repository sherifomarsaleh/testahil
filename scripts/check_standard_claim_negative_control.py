#!/usr/bin/env python3
"""Negative control for [R-STD-02]. The defect it guards is LATENT, so this is the only
evidence the gate works at all.

Every study in the book reads 2026.09.01 against a live 2026.09.07, so the gate is green
and will stay green until somebody rebuilds one. A gate that has never been seen to fire,
on a condition that does not currently exist, is indistinguishable from a gate that cannot
fire — which is why the first case here is the EXACT rebuild the repair loop reverted this
morning, reconstructed rather than described.

NOTHING IS WRITTEN INTO THE REAL TREE: the whole check runs against a sandbox built from
scratch, so there is no undo that has to run [R-ENF-01].
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

DECLARED_CASES = 10


def sandbox(studies, ratchets):
    """A minimal repository: the gate, the studies it reads, the ratchets it names."""
    tmp = tempfile.mkdtemp(prefix="stdclaim_nc_")
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"))
    os.makedirs(os.path.join(repo, "engine", "build_depth_audit"))
    shutil.copy(os.path.join(HERE, "check_standard_claim.py"),
                os.path.join(repo, "scripts", "check_standard_claim.py"))
    for tk, doc in studies.items():
        d = os.path.join(repo, "engine", "%s_study" % tk.lower())
        os.makedirs(d, exist_ok=True)
        if doc is not None:
            json.dump(doc, open(os.path.join(d, "study_numbers.json"), "w"))
    for f, payload in ratchets.items():
        if payload is None:
            continue
        json.dump(payload, open(os.path.join(repo, "engine", "build_depth_audit", f), "w"))
    return tmp, repo


def run(repo):
    r = subprocess.run([sys.executable, "scripts/check_standard_claim.py"],
                       cwd=repo, capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


FULL = {"gap_outstanding.json": {"breach_no_review": [], "unreadable": []},
        "asset_base_outstanding.json": {"outstanding": {"PHDC": "no record"}},
        "ke_outstanding.json": {"outstanding": {"ARCC": "undeclared"}}}


def study(v):
    return None if v is None else {"meta": {"standard_version": v}}


CASES = []
def case(name, studies, ratchets, expect_fail, must_name=None):
    CASES.append((name, studies, ratchets, expect_fail, must_name))


# ---- RED ---------------------------------------------------------------
case("THE LATENT DEFECT — PHDC rebuilt, stamping 2026.09.07 while ratcheted on the "
     "asset base",
     {"PHDC": study("2026.09.07")}, FULL, True, "PHDC")

case("ARCC rebuilt, stamping 2026.09.07 while ratcheted on the terminal construction",
     {"ARCC": study("2026.09.07")}, FULL, True, "ARCC")

case("a study claiming a version LATER than the ones mapped",
     {"PHDC": study("2027.01.01")}, FULL, True, "PHDC")

case("a named ratchet file that is not on disk",
     {"PHDC": study("2026.09.01")},
     dict(FULL, asset_base_outstanding=None, **{"asset_base_outstanding.json": None}),
     True, "asset_base_outstanding.json")

case("zero study directories",
     {}, FULL, True, None)

case("study directories present but not one carries a claim",
     {"PHDC": study(None), "ARCC": study(None)}, FULL, True, None)

# ---- CLEAN -------------------------------------------------------------
case("TODAY'S BOOK — every study at 2026.09.01 against a live 2026.09.07",
     {"PHDC": study("2026.09.01"), "ARCC": study("2026.09.01"),
      "TMGH": study("2026.09.01")}, FULL, False)

case("a study at 2026.09.07 that meets both requirements",
     {"TMGH": study("2026.09.07")}, FULL, False)

case("a study far behind the current version — being behind is ordinary",
     {"TMGH": study("2026.06.01")}, FULL, False)

case("a study with a claim beside one with none",
     {"TMGH": study("2026.09.01"), "SCEM": study(None)}, FULL, False)


def main():
    print("[R-STD-02] negative control — the defect it guards is LATENT, so this is the "
          "only evidence\n")
    assert len(CASES) == DECLARED_CASES, (
        "case count moved: %d present, %d declared" % (len(CASES), DECLARED_CASES))
    bad = 0
    for name, studies, ratchets, expect, must_name in CASES:
        tmp, repo = sandbox(studies, ratchets)
        try:
            # ASSERT THE FIXTURE LANDED before asking the gate anything.
            for tk, doc in studies.items():
                p = os.path.join(repo, "engine", "%s_study" % tk.lower(),
                                 "study_numbers.json")
                if doc is None:
                    assert not os.path.exists(p), "fixture wrote a file it should not have"
                else:
                    assert json.load(open(p))["meta"]["standard_version"] == \
                        doc["meta"]["standard_version"], "MUTATION DID NOT LAND"
            rc, out = run(repo)
            got = (rc != 0)
            named = (must_name in out) if must_name else True
            ok = (got == expect) and named
            print("  %-6s [%s] %-72s" % ("ok" if ok else "WRONG",
                                         "RED" if expect else "CLEAN", name[:72]))
            if not ok:
                bad += 1
                print("         exit %d, names %r: %s"
                      % (rc, must_name, named))
        except AssertionError as e:
            print("  FIXTURE %s -- %s" % (name[:60], e))
            bad += 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    print("\n%d case(s): %d red-expected, %d clean-expected"
          % (len(CASES), sum(1 for c in CASES if c[3]),
             sum(1 for c in CASES if not c[3])))
    if bad:
        print("FAIL — %d case(s) did not behave as declared." % bad)
        return 1
    print("OK — fires on the rebuild that would over-claim, and on nothing the book does "
          "today.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
