#!/usr/bin/env python3
"""[R-ENF-06] — A COMMITTED RECORD THAT A REBUILD REMOVES IS NOT A RECORD, IT IS A MEMORY.

WHY THIS EXISTS, AND IT IS THE SECOND TIME THIS DEFECT HAS BEEN FOUND. On 06-09-2026 a
rebuild of SWDY deleted that study's entire [R-ANCHOR-01] forecast_anchor block — sixteen
carefully evidenced lines — because compute.py writes the numbers file WHOLE and a second
script appends the record afterwards. It was caught by a person reading a diffstat, and
check_numbers_generators was built for it: it requires a study with more than one writer to
DECLARE their run order in the main generator's docstring. The declaration was what was
missing and the declaration is what it closed.

ON 07-09-2026 IT HAPPENED AGAIN, TO TWO STUDIES, WITH THAT GATE GREEN. Conforming the
terminal record shape meant re-running twelve generators, and SAVOLA and SWDY both came out
missing forecast_anchor. SWDY sits on the anchor gate's ratchet so it stayed green; SAVOLA
does not, so check_forecast_anchor went red and named it. A DECLARED RUN ORDER IS NOT A
SURVIVING RECORD, and the only reason two broke that day is that somebody happened to
rebuild those two.

THE EXPOSURE IS THE WHOLE BOOK. Asked of every top-level key in every study_numbers.json
whether any .py in that study's own directory so much as mentions it, 20 of 21 studies
carry at least one key no generator writes: forecast_anchor in fifteen, lens_record in the
exemplar and PHAR, bridge_record in FERTIGLOBE, macro_record in three, eps_reconciliation in
SWDY. EVERY ONE OF THOSE IS A RECORD A GATE READS. So the records this house checks its
studies against are, in most studies, hand-placed fields that a rebuild silently removes.

That mention test is a FLAG rather than a verdict — a generator can build keys
programmatically — so THIS gate does the exact thing: it copies the study into a sandbox,
runs its generator there, and diffs the top-level keys.

THE COST ARGUMENT IS THE ONE ALREADY DISPROVED ONCE TODAY. check_numbers_generators says in
its own docstring that it does not run the models because that "would take minutes and
would fail for reasons that have nothing to do with this defect". The second half was
measured on 07-09-2026 and is FALSE: five of twenty-four failed and every one of the five
was a real defect. Minutes is the true half, so this gate is slow by construction and says
so rather than trading exactness for speed.

NOTHING IS WRITTEN INTO THE REAL TREE [R-ENF-01]. The study is copied into a temporary
directory and the generator runs THERE, so a generator that rewrites its own numbers file
rewrites the copy. A check that mutates production state and undoes it afterwards is
correct exactly as often as it completes.

A GENERATOR THAT CANNOT RUN IS UNREADABLE, NEVER CLEAN [R-ENF-04], and is ratcheted in its
own group: one excuses a record that does not survive, the other a rebuild that cannot be
attempted, and they are not interchangeable [R-TERM-01].

USAGE
    python3 scripts/check_record_survives_rebuild.py [--only TK] [--timeout N]
    python3 scripts/check_record_survives_rebuild.py --prune
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit", "record_survives_outstanding.json")
DEFAULT_TIMEOUT = 400

sys.path.insert(0, ENGINE)


def generator_chain(study_dir):
    """The scripts a rebuild would run, IN THE ORDER THE STUDY DECLARES.

    THE FIRST DRAFT RAN ONLY THE MAIN GENERATOR AND WAS WRONG ABOUT TWO STUDIES —
    correctly red on what it measured and measuring the wrong thing. SAVOLA and SWDY each
    write their numbers file with compute.py and then APPEND the forecast_anchor record
    with a second script, and both compute.py files say so in capitals in their own first
    line: "RUN ORDER: compute.py THEN forecast_anchor.py. RUNNING THIS FILE ALONE DELETES
    A COMMITTED RECORD." That declaration is what [R-ENF-01]'s numbers-generators gate
    exists to require, and it was there, and this gate ignored it.

    So the rebuild under test is the DECLARED one. A study that declares no order and has
    one writer runs that; a study that declares no order and has SEVERAL is a different
    defect, owned by check_numbers_generators, and is reported here as unreadable rather
    than guessed at. Per [R-COC-01]: when a check fires on work that is right, re-point it.
    """
    import numbers_generators as ng
    w = ng.writers(study_dir)
    if not w:
        return None, "no script in this directory writes its numbers file"
    main, named = _declared_order(study_dir, w)
    if named:
        # the declaration names them in order; keep the declared sequence
        head = open(os.path.join(study_dir, main), encoding="utf-8").read(4000)
        return sorted(named, key=lambda f: head.find(f)), None
    if len(w) > 1:
        return None, ("%d scripts write this numbers file and none declares a RUN ORDER, "
                      "so which rebuild is the rebuild cannot be read [R-ENF-04]" % len(w))
    return [w[0]], None


def _declared_order(study_dir, generators):
    """(main generator, the scripts it names) — the same reading check_numbers_generators
    does, so the two gates cannot disagree about what a study declared [R-ENF-03]."""
    for g in generators:
        try:
            head = open(os.path.join(study_dir, g), encoding="utf-8").read(4000)
        except OSError:
            continue
        if "RUN ORDER" in head.upper():
            return g, [x for x in generators if x in head]
    return None, []


def rebuild_keys(tk, study_dir, chain, timeout):
    """(keys after a sandbox rebuild of the DECLARED chain, error). The real tree is
    never written."""
    tmp = tempfile.mkdtemp(prefix="rsr_")
    try:
        # The whole engine is copied because a study's generator imports its siblings.
        dst = os.path.join(tmp, "engine")
        shutil.copytree(ENGINE, dst, ignore=shutil.ignore_patterns(
            "*.xlsx", "*.docx", "*.pdf", "*.png", "raw_ohlc", "raw_indices",
            "__pycache__", "lab"))
        sd = os.path.join(dst, os.path.basename(study_dir))
        for gen in chain:
            p = subprocess.run([sys.executable, gen], cwd=sd,
                               capture_output=True, text=True, timeout=timeout)
        nf = os.path.join(sd, "study_numbers.json")
        if not os.path.exists(nf):
            return None, "the rebuild wrote no numbers file (exit %d): %s" % (
                p.returncode, (p.stderr or p.stdout).strip().splitlines()[-1:][0][:120]
                if (p.stderr or p.stdout).strip() else "no output")
        try:
            return set(json.load(open(nf, encoding="utf-8")).keys()), None
        except Exception as exc:
            return None, "the rebuilt numbers file will not parse: %s" % exc
    except subprocess.TimeoutExpired:
        return None, "the generator did not finish in %ds" % timeout
    except Exception as exc:
        return None, "the sandbox rebuild could not run: %s" % exc
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def load():
    if not os.path.exists(OUTSTANDING):
        return {}, {}
    try:
        d = json.load(open(OUTSTANDING, encoding="utf-8"))
    except Exception:
        return {}, {}
    return d.get("outstanding", {}), d.get("unreadable", {})


def main(argv):
    prune = "--prune" in argv
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1].upper()
    timeout = DEFAULT_TIMEOUT
    if "--timeout" in argv:
        timeout = int(argv[argv.index("--timeout") + 1])

    dirs = sorted(glob.glob(os.path.join(ENGINE, "*_study")))
    if not dirs:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    lost, unread, read = {}, {}, 0
    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        if only and tk != only:
            continue
        nf = os.path.join(d, "study_numbers.json")
        if not os.path.exists(nf):
            continue
        chain, why = generator_chain(d)
        if not chain:
            unread[tk] = why
            continue
        try:
            before = set(json.load(open(nf, encoding="utf-8")).keys())
        except Exception as exc:
            unread[tk] = "the committed numbers file will not parse: %s" % exc
            continue
        after, err = rebuild_keys(tk, d, chain, timeout)
        if after is None:
            unread[tk] = err
            continue
        read += 1
        gone = sorted(before - after)
        if gone:
            lost[tk] = {"gen": " -> ".join(chain), "keys": gone,
                        "why": "rebuilding with %s removes %d committed record(s): %s"
                               % (" -> ".join(chain), len(gone), ", ".join(gone))}
        print("  %-13s %-34s %s" % (tk, " -> ".join(chain),
                                    ("LOSES " + ", ".join(gone)) if gone else "survives"))

    if read == 0 and not only:
        print("FAIL — %d study directories and ZERO rebuilds completed. A run that "
              "attempted nothing is not a run that found nothing [R-ENF-04]." % len(dirs))
        return 1

    known_lost, known_unread = load()

    if prune:
        json.dump({"rule": "R-ENF-06 — a record a rebuild removes",
                   "note": "Two groups, NOT interchangeable: one excuses a record that "
                           "does not survive a rebuild, the other a rebuild that cannot "
                           "be attempted. Both may only SHORTEN.",
                   "outstanding": lost, "unreadable": unread},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print("\npruned: not-surviving %d -> %d, unreadable %d -> %d"
              % (len(known_lost), len(lost), len(known_unread), len(unread)))
        return 0

    print("\n[R-ENF-06] rebuilds attempted: %d   records lost: %d   unreadable: %d"
          % (read, len(lost), len(unread)))

    new = sorted(set(lost) - set(known_lost))
    new_un = sorted(set(unread) - set(known_unread))
    grown = [tk for tk in lost if tk in known_lost
             and set(lost[tk]["keys"]) - set(known_lost[tk].get("keys", []))]

    rc = 0
    for tk in new:
        print("  NEW   %-13s %s" % (tk, lost[tk]["why"]))
    for tk in grown:
        print("  WORSE %-13s now also loses: %s"
              % (tk, ", ".join(sorted(set(lost[tk]["keys"])
                                      - set(known_lost[tk].get("keys", []))))))
    for tk in new_un:
        print("  NEW   %-13s %s" % (tk, unread[tk]))
    if new or grown:
        print("\nFAIL — a committed record does not survive its own rebuild. Write it in "
              "the generator; a repair that does not survive a rebuild is not a repair "
              "[R-REPAIR-01].")
        rc = 1
    if new_un:
        print("\nFAIL — a rebuild could not be attempted. An absent answer is not a clean "
              "one [R-ENF-04].")
        rc = 1
    if rc:
        return rc
    print("\nOK — every committed record survives its own study's rebuild, except where "
          "the ratchet records otherwise.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
