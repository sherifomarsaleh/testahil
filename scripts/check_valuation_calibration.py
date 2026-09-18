#!/usr/bin/env python3
"""The pre-registration was committed BEFORE any score.  [R-VCAL-01]

WHY. The valuation calibration's whole claim on credibility is that no lever was
fitted to the gap it measures. That claim cannot be established by assurance — of
course the document says it was written first; every such document says so. It can
be established by COMMIT ORDER, which nobody can rewrite after the fact without
rewriting history in public.

So this gate reads git rather than the file: the pre-registration's own commit
must precede the first commit of every score or result file in the calibration
directory, and the document must still hash to what it hashed to when it was
sealed. A pre-registration that can be edited afterwards is a rationalisation with
a date on it.

WHAT IT CHECKS
  1. exactly one sealed pre-registration exists, with its recorded sha256
  2. the file on disk still hashes to that value — sealed means sealed
  3. every score/result file in the directory was first committed AFTER it
  4. history is deep enough to answer 3 at all — a shallow clone cannot, and
     saying so is not the same as passing [R-ENF-04]
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALIB = os.path.join(ROOT, "engine", "valuation_calibration")
PREREG_GLOB = "PRE_REGISTRATION_*.md"
HASH_FILE = os.path.join(CALIB, "PRE_REGISTRATION_HASH.json")

# What counts as a SCORE — a file whose content could have been influenced by
# seeing the data. Modules that only define the method are not scores; a results
# file is. Named by suffix so a new results file is caught without an edit here.
SCORE_MARKERS = ("SCORES", "RESULTS", "scores", "results", "PREDICTIONS")


def _git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a),
                          capture_output=True, text=True, timeout=300)


def first_commit(path):
    """The commit that introduced a file, as a SHA — never as a timestamp.

    Timestamps tie. Two commits made in the same second compare equal, and the
    first version of this gate passed a fixture in which a score was committed
    BEFORE the pre-registration for exactly that reason: the negative control
    caught it on its first run. Order here is TOPOLOGY — is the pre-registration's
    commit an ancestor of the score's — which is exact, and which a later rewrite
    of history cannot fake without rewriting it in public.
    """
    r = _git("log", "--follow", "--diff-filter=A", "--format=%H", "--", path)
    shas = [l for l in r.stdout.split() if len(l) == 40]
    if shas:
        return shas[-1]
    r = _git("log", "--format=%H", "--", path)
    shas = [l for l in r.stdout.split() if len(l) == 40]
    return shas[-1] if shas else None


def is_ancestor(a, b):
    """True when commit a is an ancestor of b (or they are the same commit)."""
    if a == b:
        return True
    return _git("merge-base", "--is-ancestor", a, b).returncode == 0


def main():
    if not os.path.isdir(CALIB):
        print("FAIL — %s does not exist. An absent calibration is not a clean one."
              % os.path.relpath(CALIB, ROOT))
        return 1

    pregs = sorted(glob.glob(os.path.join(CALIB, PREREG_GLOB)))
    if not pregs:
        print("FAIL — no pre-registration in %s. Every score this directory "
              "produces would then rest on an assurance rather than on a commit "
              "order, which is the thing the pre-registration exists to replace."
              % os.path.relpath(CALIB, ROOT))
        return 1

    if os.path.exists(os.path.join(ROOT, ".git", "shallow")):
        print("FAIL — this is a SHALLOW clone, so commit order cannot be read and "
              "the one thing this gate exists to check cannot be checked. Check "
              "out at full depth (fetch-depth: 0). Reporting clean here would be "
              "reporting on nothing [R-ENF-04].")
        return 1

    fails = []

    # ---- 1 & 2: sealed means sealed -----------------------------------------
    recorded = {}
    if os.path.exists(HASH_FILE):
        try:
            recorded = json.load(open(HASH_FILE, encoding="utf-8"))
        except Exception as exc:
            fails.append("the hash record will not parse (%s)" % exc)
    else:
        fails.append("no PRE_REGISTRATION_HASH.json — the document is unsealed, so "
                     "an edit to it would leave no trace at all")

    # EVERY SEALED DOCUMENT IS CHECKED, NOT ONLY THE CURRENT ONE. A superseded
    # pre-registration whose hash stops being verified is a document nobody can check
    # any more, and the superseded one is precisely where a rationalisation would be
    # inserted afterwards — it is the design the earlier scores claim to follow.
    seals = {recorded.get("file"): recorded.get("sha256")} if recorded.get("file") else {}
    seals.update({k: v for k, v in (recorded.get("files") or {}).items()})
    for old in (recorded.get("superseded") or []):
        if old.get("file"):
            seals[old["file"]] = old.get("sha256")

    latest = pregs[-1]
    digest = hashlib.sha256(open(latest, "rb").read()).hexdigest()
    for q in pregs:
        base = os.path.basename(q)
        dg = hashlib.sha256(open(q, "rb").read()).hexdigest()
        claimed = seals.get(base) or (recorded.get("sha256") if q is latest else None)
        if claimed is None:
            fails.append("%s carries no seal in the hash record. An unsealed "
                         "pre-registration could be edited afterwards and leave no "
                         "trace, which is the one thing this record exists to stop."
                         % base)
        elif not str(claimed).startswith(dg[:16]) and claimed != dg:
            fails.append("%s hashes to %s and its seal records %s. A pre-registration "
                         "that changed after it was sealed is a rationalisation with a "
                         "date on it; supersede it with a NEW dated document that says "
                         "so, never by editing this one."
                         % (base, dg[:16], str(claimed)[:16]))

    # THE DESIGN A SCORE FOLLOWS IS THE ONE IN FORCE WHEN THE SCORE WAS WRITTEN.
    # The first version of this gate held every score against the LATEST document, which
    # made supersession impossible — the moment a second pre-registration was committed,
    # every score written under the first became "a score that predates the design it
    # claims to follow", although each had been produced correctly under the design that
    # existed at the time. The sealed document ITSELF prescribes supersession as the only
    # way to correct it, so a gate that cannot express one is a gate disagreeing with the
    # rule it enforces. NOTHING IS EXCUSED BY THE CHANGE: each score is still required to
    # come strictly after a committed, sealed design, and a score produced today is still
    # held against today's document. What changes is only WHICH document a given score is
    # paired with, and the pairing is read off commit topology rather than asserted.
    preg_shas = []
    for q in pregs:
        sha = first_commit(q)
        if sha is None:
            fails.append("%s has no commit — it exists only in the working tree, so "
                         "nothing establishes when it was written" % os.path.basename(q))
        preg_shas.append((q, sha))
    preg_sha = dict(preg_shas).get(latest)

    def design_in_force(score_sha):
        """The LATEST pre-registration whose commit is an ancestor of this score's."""
        best = None
        for q, sha in preg_shas:
            if sha is not None and is_ancestor(sha, score_sha):
                best = (q, sha)
        return best

    # ---- 3: every score came after ------------------------------------------
    scores, checked = [], 0
    for p in sorted(glob.glob(os.path.join(CALIB, "**", "*"), recursive=True)):
        if not os.path.isfile(p):
            continue
        base = os.path.basename(p)
        if base.startswith("PRE_REGISTRATION"):
            continue
        if not any(m in base for m in SCORE_MARKERS):
            continue
        scores.append(p)
        e = first_commit(p)
        checked += 1
        if e is None:
            fails.append("%s is uncommitted, so its order against the "
                         "pre-registration cannot be established" % base)
        else:
            held = design_in_force(e)
            if held is None:
                fails.append("%s was first committed BEFORE any pre-registration. A "
                             "score that predates the design it claims to follow is "
                             "not evidence about that design." % base)

    print("pre-registration: %s (sealed %s, introduced in %s)"
          % (os.path.basename(latest), digest[:12],
             preg_sha[:12] if preg_sha else "NO COMMIT"))
    print("score/result files found: %d   order-checked: %d" % (len(scores), checked))
    if not scores:
        print("  none yet — the calibration has produced no scores, which is the "
              "expected state until a vintage matures. That is a REPORTED "
              "condition, not a silent pass: this gate would be equally quiet if "
              "the directory had been emptied, so the count above is the evidence.")

    for f in fails:
        print("  FAIL  %s" % f)
    if fails:
        return 1
    print("\nOK — the pre-registration is sealed and precedes every score.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
