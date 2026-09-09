#!/usr/bin/env python3
"""Run exactly what CI runs, by reading CI's own definition.

WHY THIS EXISTS. On 3 September 2026 I reported "every gate green" after running
the scripts/check_*.py suite by hand, and CI was red — had been red for a day — on
a step that lives inline in the workflow rather than in a check script. The claim
was not a lie and it was not true either: I had run a DIFFERENT POPULATION from
the one CI runs, and my sweep could not see the difference because it was built
from a list I maintained rather than from the workflow.

That is [R-ENF-04] in its usual costume. The fix is the usual one: anchor the
population somewhere else. This script parses the workflow YAML and executes every
`run:` step it finds, so it cannot drift from CI — a step added to the workflow is
a step this runs, without anyone remembering to add it here.

It is a convenience, not a gate: CI remains the authority, and a green run here is
evidence, not a substitute.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")

# WHERE THE EVIDENCE LANDS, so that something OTHER than the acceptance record can
# say whether the gates are green [R-ENF-01].
#
# Part E criterion 1 read `"state": "MET"` as a TYPED CONSTANT in progress.py — a
# claim the acceptance instrument made about itself, which is the exact shape the
# rule forbids everywhere else in this repository. Criterion 3 had the same defect
# and was made a call; 1 and 2 were left behind. This file is what they now read.
#
# IT CARRIES THE COMMIT IT WAS PRODUCED AT [R-ENF-06]. A green run is evidence about
# the tree it ran on and nothing else, so a result from an earlier commit is STALE
# rather than green, and a run on a dirty tree is evidence about a tree nobody else
# can reproduce. Both are refused by the reader rather than being quietly reused.
RESULT = os.path.join(ROOT, "engine", "build_depth_audit", "ci_gate_run.json")


def _head():
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip()
        return sha, [l for l in dirty.splitlines() if l.strip()]
    except (OSError, subprocess.CalledProcessError):
        return None, None


def _record(workflow, green, red, skipped, started, finished):
    """Write the run down. Never a verdict — the numbers, and what they were of."""
    sha, dirty = _head()
    doc = {
        "_": "Written by scripts/run_ci_gates.py. READ BY engine/method_reassessment/"
             "progress.py for Part E criteria 1 and 2, which may not assert their own "
             "state [R-ENF-01]. Never hand-edit: a hand-written green here is the "
             "typed constant this file was created to replace.",
        "workflow": workflow,
        "commit": sha,
        "tree_dirty": dirty if dirty is not None else "unknown",
        "started": started, "finished": finished,
        "green": green,
        "red": [label for label, _tail in red],
        "skipped": [{"step": label, "why": why} for label, why in skipped],
    }
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("\nrecorded to %s at %s%s"
          % (os.path.relpath(RESULT, ROOT), (sha or "unknown")[:9],
             "" if not dirty else "  (TREE DIRTY — %d file(s); this run is evidence "
                                  "about a tree nobody else has)" % len(dirty)))

# Steps that cannot run outside the runner (they need the network, a token, or a
# deploy target). Skipped LOUDLY and counted, because a silent skip is how a
# runner like this starts reporting on less than it claims.
# A step that writes to a runner-provided file handle, or that interpolates a
# ${{ }} expression the runner resolves before bash ever sees it, CANNOT run here
# — not "fails here", cannot run. monthly-backup.yml reported two RED steps on
# `GITHUB_OUTPUT: unbound variable` and a `${{ steps.build.outputs.date }}` that
# bash read as a bad substitution; both are this runner's absence, not a defect
# in the repository, and a red that means "not applicable" is the permanently-red
# check [R-ENF-02] forbids. They are skipped LOUDLY, like every other skip.
CANNOT_RUN_LOCALLY = ("actions/", "deploy", "upload-artifact", "peaceiris",
                      "GITHUB_TOKEN", "gh api", "curl ",
                      "${{", "GITHUB_OUTPUT", "GITHUB_ENV", "GITHUB_STEP_SUMMARY")

# A CI STEP ASSUMES A DISPOSABLE RUNNER, AND THIS ONE IS NOT DISPOSABLE.
#
# The first version of this script had a --all mode that ran every workflow's
# steps against the live working tree. It got as far as a workflow that rebases
# and auto-commits before it was stopped: the checkout was left mid-rebase on a
# detached HEAD, engine/valuation_calibration/ was emptied on disk, and an
# unrelated auto-refresh commit swept an uncommitted file in under a message that
# described something else entirely. Nothing was lost — every commit was already
# on the remote, which is the only reason this is an anecdote rather than an
# incident — but that was luck about push timing, not a property of the design.
#
# So: any step that could mutate the repository is REFUSED rather than run. The
# list is of VERBS, not of workflows, because a new workflow is written without
# anyone thinking of this file. --all is gone with it: a runner that executes
# arbitrary committed shell against a working tree it does not own is a footgun
# whose safe configuration nobody can remember.
MUTATES_THE_REPO = (
    "git commit", "git push", "git rebase", "git merge", "git reset",
    "git checkout", "git switch", "git cherry-pick", "git apply", "git am",
    "git clean", "git stash", "git tag", "git branch", "git rm", "git add",
    "auto_refresh", "publish_site", "rm -rf", "mv ",
)


def _head_sha():
    """The commit this tree is on, or None if git cannot say.

    THE RUN NEEDS THIS BECAUSE IT CANNOT TELL ITS OWN WRITES FROM THE OPERATOR'S.
    _carry/_restore below attribute every content change during a step to that step.
    That is right when the run has the tree to itself and wrong when it does not, and
    on 09-09-2026 it was wrong twice in one hour: an operator committed
    engine/study_population.py while a run was somewhere in the middle of seventy-odd
    steps, and _restore wrote the PRE-COMMIT bytes back over the committed file. No
    step had touched it. The guard built to stop a step clobbering the operator
    clobbered the operator instead, and it did it silently, reporting the step GREEN.

    It happened a second time because the first kill hit the wrapper and not the
    interpreter, so a run nobody could see kept restoring for another half hour. The
    lock is a lock on STARTING, not on running, which is why this check is per-step.
    """
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def _clean_vs_head(rel):
    """True where this path currently matches HEAD.

    A path that matches HEAD was not left dirty by the step that just ran: either the
    step never touched it, or it was COMMITTED while the run was going. Writing carried
    bytes over either one is wrong, and over the second it is the exact failure above.
    """
    r = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT,
                       capture_output=True, text=True)
    return r.returncode == 0 and not r.stdout.strip()


def _dirty_set():
    """The tracked paths that differ from HEAD right now, as a set.

    A SET, not a count: what matters after a step is which files it dirtied that
    were clean before, and a count cannot answer that.
    """
    r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return {l[3:].strip() for l in r.stdout.splitlines() if l.strip()}


#: a file already dirty when a step starts cannot be restored from HEAD -- HEAD is
#: not what the operator had. So its CONTENT is copied first. Bounded, because only
#: dirty files are copied and a working tree with more than this many is not a tree
#: anyone is running a careful local CI sweep against.
_CARRY_LIMIT = 200


def _carry(paths):
    """Copy the current content of these paths so a step cannot clobber them.

    THE HOLE THIS CLOSES, found by testing the guard rather than by reasoning about
    it. Reverting only newly-dirty paths correctly leaves an operator's own edits
    alone -- but a step that OVERWRITES an already-dirty file destroys those edits
    outright, and the guard then has nothing to restore from, because restoring from
    HEAD would throw the edits away just as surely. Measured on the probe: an edit
    appended to assets/data.js was gone after the regenerate step, and the run said
    only that legacy/assets/data.js had been reverted.
    """
    out = {}
    for rel in list(paths)[:_CARRY_LIMIT]:
        full = os.path.join(ROOT, rel)
        try:
            with open(full, "rb") as fh:
                out[rel] = fh.read()
        except OSError:
            out[rel] = None          # deleted or unreadable; nothing to restore
    return out


def _restore(carried):
    """REPORT any carried file whose content changed during the step. WRITES NOTHING.

    THIS USED TO PUT THE CARRIED BYTES BACK AND THAT WAS THE WRONG INSTRUMENT. Restoring
    an ALREADY-DIRTY file means writing over the operator's uncommitted work on a guess
    about who changed it, and inside one working tree a concurrent editor and a mutating
    step are not distinguishable by content. On 09-09-2026 it destroyed the same edit
    three times: engine/study_population.py after it had been COMMITTED, which the
    clean-vs-HEAD guard below now catches, and then engine/swdy_study/build_xlsx_swdy.py
    twice while it was still uncommitted, which no HEAD check can catch because HEAD
    never moved.

    A check does not write to the tree it checks [R-ENF-01], and that binds the guard as
    much as the step. The run now SAYS what a step overwrote and leaves it alone. The
    operator is left with the path named and their editor's undo, which is strictly
    better than having the file silently replaced by whichever of two writers the run
    happened to guess.

    Reverting NEWLY-dirty paths is kept and is a different thing: those were clean when
    the step began, so git checkout restores HEAD rather than overwriting anyone's work.

    Returns the paths a step overwrote, for the caller to print.
    """
    back = []
    for rel, blob in carried.items():
        if blob is None:
            continue
        # A PATH THAT NOW MATCHES HEAD IS NOT THIS STEP'S DOING — see _clean_vs_head.
        if _clean_vs_head(rel):
            continue
        full = os.path.join(ROOT, rel)
        try:
            with open(full, "rb") as fh:
                if fh.read() == blob:
                    continue
        except OSError:
            pass
        back.append(rel)          # REPORTED, NOT REWRITTEN — see the docstring
    return back


def steps(path):
    doc = yaml.safe_load(open(path, encoding="utf-8"))
    for jobname, job in (doc.get("jobs") or {}).items():
        for st in (job.get("steps") or []):
            if "run" in st:
                yield jobname, st.get("name") or "(unnamed)", st["run"], st.get("if")


def _now():
    import datetime
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


#: One run at a time. This became necessary the moment the runner started REVERTING
#: files: two concurrent runs on one working tree will undo each other's steps
#: mid-write, and each will then report a verdict about a tree the other was editing.
#: Before the mutation guard existed, concurrent runs were merely wasteful; now they
#: corrupt. Found by running two at once on 09-09-2026 and noticing both alive.
LOCK = os.path.join(ROOT, ".git", "run_ci_gates.lock")


def _take_lock():
    """Refuse to start if another run holds the lock. Returns True if taken."""
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            with open(LOCK) as fh:
                held = fh.read().strip()
        except OSError:
            held = "unknown"
        # A STALE LOCK IS NOT A RUNNING ONE. A killed run leaves the file behind, and
        # a tool that then refuses for ever is a tool people delete the lock for
        # without reading it -- which is the same as having no lock.
        pid = held.split()[0] if held else ""
        if pid.isdigit():
            try:
                os.kill(int(pid), 0)
            except OSError:
                os.unlink(LOCK)
                return _take_lock()
            print("REFUSED — another run_ci_gates is running (%s). Two runs on one "
                  "working tree revert each other's steps mid-write, and each then "
                  "reports a verdict about a tree the other was editing." % held)
            return False
        os.unlink(LOCK)
        return _take_lock()
    os.write(fd, ("%d started %s" % (os.getpid(), _now())).encode())
    os.close(fd)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow", nargs="?", default="study-provenance.yml",
                    help="one workflow file. There is deliberately no --all: see "
                         "MUTATES_THE_REPO above.")
    a = ap.parse_args()
    if not _take_lock():
        return 1
    try:
        return _run(a)
    finally:
        try:
            os.unlink(LOCK)
        except OSError:
            pass


def _run(a):
    files = [os.path.join(WORKFLOWS, a.workflow)]
    started = _now()

    red, green, skipped, mutating = [], 0, [], []
    for f in files:
        if not os.path.exists(f):
            print("FAIL — no such workflow: %s" % f)
            return 1
        for job, name, script, cond in steps(f):
            label = "%s / %s" % (os.path.basename(f), name)
            # A CONDITIONAL STEP IS NOT UNCONDITIONALLY PART OF THE RUN, and this
            # runner cannot evaluate GitHub's expression language. Running one
            # anyway grades a branch CI would not have taken: testahil-calibration's
            # two failure handlers (`if: ...exit_code != '0'`) both end in `exit 1`,
            # so they reported RED on a repository with no error file to their name,
            # while deploy-pages' retry sleeps reported GREEN and inflated the count.
            # Every gate in these workflows is unconditional; the conditional ones
            # are failure handlers and retry pauses. Skipped LOUDLY, never evaluated.
            if cond is not None:
                skipped.append((label, "conditional (if: %s) — not evaluable outside "
                                       "the runner" % str(cond)[:60]))
                continue
            mut = [t for t in MUTATES_THE_REPO if t in script]
            if mut:
                skipped.append((label, "REFUSED — would mutate this checkout (%s). "
                                       "A CI step assumes a disposable runner; "
                                       "this tree is not one." % ", ".join(mut[:3])))
                continue
            if any(t in script for t in CANNOT_RUN_LOCALLY):
                skipped.append((label, "needs the runner (network, token or deploy)"))
                continue
            # A TIMEOUT IS A RED, NOT A CRASH, AND CERTAINLY NOT A PASS [R-ENF-04].
            # This raised TimeoutExpired straight out of main(), so a single slow step
            # killed the run BEFORE the result was recorded — sixty green steps and a
            # timeout produced NO evidence at all, and the acceptance criteria that read
            # that record saw "no CI run has been recorded". A run that cannot say what
            # it found is worth less than one that says it timed out.
            before_dirty = _dirty_set()
            _head_before = _head_sha()
            head_moved = False
            carried = _carry(before_dirty or ())
            try:
                r = subprocess.run(["bash", "-e", "-c", script], cwd=ROOT,
                                   capture_output=True, text=True, timeout=1800)
            except subprocess.TimeoutExpired:
                red.append((label, ["TIMED OUT after 1800s. Not a pass: nothing was "
                                    "established about this step."]))
                print("  RED    %s   TIMED OUT" % label[:90])
                continue
            # WHAT A STEP ACTUALLY DID TO THE TREE, MEASURED, NOT GUESSED FROM ITS
            # COMMAND NAMES. MUTATES_THE_REPO is a hand-typed list of substrings, so
            # it can only ever refuse what somebody thought of. On 09-09-2026
            # testahil-calibration's "Regenerate the price and funnel blocks onto the
            # current library" walked straight past it -- its commands are
            # build_prices_block.py, build_screen_block.py and a cp -- and rewrote
            # assets/data.js and legacy/assets/data.js, the LIVE SITE's data file,
            # recomputing every screen z-score. It reported GREEN and the operator
            # found the change only because a commit hook noticed the dirty tree.
            #
            # A list guard and a measurement guard fail differently: the list misses
            # what it does not name, and the measurement misses nothing, because it
            # asks the tree instead of the script. The list is kept -- refusing BEFORE
            # a step runs is better than undoing after it -- and this catches the rest.
            #
            # THE REVERT IS DELIBERATE AND IT IS SAFE. Only paths this step made dirty
            # are restored, never anything already dirty when the run began, so a
            # working tree with edits in it survives untouched. Where the tree cannot
            # be read at all the step is reported as UNVERIFIED rather than clean
            # [R-ENF-04]: not knowing whether a step wrote to the tree is not the same
            # as knowing it did not.
            # HEAD MOVED WHILE THE STEP RAN, SO EVERY CARRIED SNAPSHOT IS VOID.
            # A commit during a run means the operator is working in this tree and the
            # run no longer knows which content changes are its own. Restoring on that
            # basis is guessing with a write. It says so out loud and touches nothing.
            _head_after = _head_sha()
            if _head_before is not None and _head_after != _head_before:
                head_moved = True
                print("  NOTE   HEAD moved during this step (%s -> %s). Carried content "
                      "for %d path(s) DISCARDED unrestored: a commit landed while the run "
                      "was going, so this run cannot tell its own writes from the "
                      "operator's and will not guess with a write."
                      % ((_head_before or '?')[:9], (_head_after or '?')[:9],
                         len(carried)))
                carried = {}
            clobbered = _restore(carried)
            if clobbered:
                print("  NOTE   this step OVERWROTE %d file(s) that already carried "
                      "uncommitted changes, and they were NOT put back: %s. A check does "
                      "not write to the tree it checks [R-ENF-01], and that binds this "
                      "guard too — recover from your editor if the change was yours."
                      % (len(clobbered), ", ".join(clobbered[:4])))
            now_dirty = _dirty_set()
            if before_dirty is None or now_dirty is None:
                mutated = None
            else:
                mutated = sorted(now_dirty - before_dirty)
                # SAME REASON, AND MORE DANGEROUS: this one reverts to HEAD. A path the
                # operator created or edited during the step reads as newly dirty and is
                # indistinguishable from a step's own output.
                if mutated and head_moved:
                    print("  NOTE   %d path(s) newly dirty and NOT reverted, because HEAD "
                          "moved during this run: %s"
                          % (len(mutated), ", ".join(mutated[:4])))
                elif mutated:
                    subprocess.run(["git", "checkout", "--"] + mutated, cwd=ROOT,
                                   capture_output=True, text=True)
                    now_dirty = _dirty_set()
                    before_dirty = now_dirty if now_dirty is not None else before_dirty

            if r.returncode == 0:
                green += 1
                _touched = sorted(set(mutated or []) | set(clobbered))
                print("  GREEN  %s%s" % (label[:90],
                      "" if not _touched else
                      "   [TOUCHED: %s]" % ", ".join(_touched[:3])))
            else:
                red.append((label, (r.stdout + r.stderr).strip().splitlines()[-6:]))
                print("  RED    %s   exit %d" % (label[:90], r.returncode))
            if mutated or clobbered:
                mutating.append((label, sorted(set(mutated or []) | set(clobbered))))
            elif mutated is None:
                mutating.append((label, ["UNVERIFIED — the tree could not be read"]))

    _record(a.workflow, green, red, skipped, started, _now())
    print("\nran %d steps from %d workflow(s): %d green, %d red, %d skipped"
          % (green + len(red), len(files), green, len(red), len(skipped)))
    for label, why in skipped:
        print("  skipped  %-60s %s" % (label[:60], why))
    if mutating:
        print("\n%d step(s) WROTE TO THE TREE and were reverted. They ran, so their "
              "verdict stands; what they wrote does not:" % len(mutating))
        for label, paths in mutating:
            print("  %-58s %s" % (label[:58], ", ".join(paths[:4])))
        print("  MUTATES_THE_REPO did not name these. It is a list of command "
              "substrings and cannot refuse what nobody thought of; the tree was "
              "measured instead.")
    for label, tail in red:
        print("\nRED — %s" % label)
        for line in tail:
            print("     " + line[:160])
    if red:
        print("\nCI would be red. This ran CI's OWN step list, so a green sweep of "
              "the check scripts alone is not the same claim.")
        return 1
    if green == 0:
        # [R-ENF-04]: an empty result is not a clean result. A workflow whose every
        # step is runner-only ran NOTHING here, and saying "every step passes" of a
        # population of zero is the absent answer wearing the costume of a clean one.
        print("\nNOTHING RAN — every step is runner-only, so this workflow is "
              "UNCHECKED here, not green.")
        return 0
    print("\nOK — every locally-runnable CI step passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
