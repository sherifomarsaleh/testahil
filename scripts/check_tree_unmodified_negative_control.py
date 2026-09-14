"""Negative control for check_tree_unmodified.  [R-ENF-01]

Reinjects every condition the gate claims to refuse, and the clean cases it must NOT
fire on. EVERY MUTATION ASSERTS THAT IT LANDED before the gate runs — negative
controls in this repository have been caught passing fixtures that never injected
their condition, so a case that cannot prove it changed anything is evidence about
nothing. The case COUNT is asserted against a declared constant.

THE FIRST RED CASE IS THE DEFECT EXACTLY AS IT HAPPENED: a register file rewritten in
place while the checks were running, which is what destroyed thirteen escalations on
07-09-2026 and reached a commit.

THE CLEAN HALF IS WHAT KEEPS THIS FROM BECOMING A TIDINESS RULE. An untracked file
must NOT fire. Gates here render documents, write panels and leave build output, and
none of that changes anything that was committed; a gate refusing it would be making
a claim about housekeeping rather than about the record, and would be red often
enough to be ignored — the permanently-red check [R-ENF-02] forbids.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(HERE, "check_tree_unmodified.py")

CASES_EXPECTED = 10
RED_EXPECTED = 6
CLEAN_EXPECTED = 4


def _git(d, *a):
    return subprocess.run(("git",) + a, cwd=d, capture_output=True, text=True)


def _sandbox(with_git=True):
    """A small real repository, so the gate is exercised the way it runs."""
    tmp = tempfile.mkdtemp(prefix="tree-nc-")
    os.makedirs(os.path.join(tmp, "scripts"))
    os.makedirs(os.path.join(tmp, "engine"))
    shutil.copy(TARGET, os.path.join(tmp, "scripts", "check_tree_unmodified.py"))
    open(os.path.join(tmp, "engine", "escalations.json"), "w").write(
        '{"entries": [{"key": "a-real-question"}]}\n')
    open(os.path.join(tmp, "engine", "keep.txt"), "w").write("committed\n")
    if with_git:
        _git(tmp, "init", "-q")
        _git(tmp, "config", "user.email", "t@t")
        _git(tmp, "config", "user.name", "t")
        _git(tmp, "add", "-A")
        _git(tmp, "commit", "-qm", "root")
        st = _git(tmp, "status", "--porcelain", "-uno").stdout
        assert st.strip() == "", "fixture: the sandbox did not start clean"
    return tmp


def _baseline(tmp):
    return os.path.join(tmp, "baseline.txt")


def _record(tmp, env=None):
    """The --record half, run BEFORE each case's mutation, as the workflow runs it."""
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_tree_unmodified.py"),
                        "--record", "--baseline", _baseline(tmp)],
                       capture_output=True, text=True, timeout=120, env=env)
    return r.returncode, r.stdout + r.stderr


def _run(tmp, env=None):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_tree_unmodified.py"),
                        "--baseline", _baseline(tmp)],
                       capture_output=True, text=True, timeout=120, env=env)
    return r.returncode, r.stdout + r.stderr


# ------------------------------------------------------------------ red cases

def register_rewritten(tmp):
    """The 07-09-2026 defect: a committed register replaced while checks ran."""
    p = os.path.join(tmp, "engine", "escalations.json")
    before = open(p).read()
    open(p, "w").write('{"_": "negative control", "entries": [{"key": "NC-example"}]}\n')
    assert open(p).read() != before, "MUTATION DID NOT LAND: the file is unchanged"
    assert _git(tmp, "status", "--porcelain", "-uno").stdout.strip(), \
        "MUTATION DID NOT LAND: git does not see the change"
    return "changed WHILE the checks ran"


def tracked_file_deleted(tmp):
    p = os.path.join(tmp, "engine", "keep.txt")
    assert os.path.exists(p), "MUTATION DID NOT LAND: nothing to delete"
    os.remove(p)
    assert _git(tmp, "status", "--porcelain", "-uno").stdout.strip(), \
        "MUTATION DID NOT LAND: git does not see the deletion"
    return "changed WHILE the checks ran"


def not_a_work_tree(tmp):
    """An unanswerable check is not a clean one [R-ENF-04]."""
    g = os.path.join(tmp, ".git")
    assert os.path.isdir(g), "MUTATION DID NOT LAND: no .git to remove"
    shutil.rmtree(g)
    assert not os.path.exists(g), "MUTATION DID NOT LAND: .git survived"
    return "not a git work tree"


def git_status_refuses(tmp):
    """git runs and REFUSES. The probe did not run, so it found nothing [R-ENF-04]."""
    binn = os.path.join(tmp, "fakebin")
    os.makedirs(binn)
    fake = os.path.join(binn, "git")
    open(fake, "w").write("#!/bin/sh\n"
                          "case \"$1\" in rev-parse) exit 0;; esac\n"
                          "echo 'fatal: fixture' >&2; exit 128\n")
    os.chmod(fake, 0o755)
    r = subprocess.run(["git", "status"], cwd=tmp, capture_output=True, text=True,
                       env=dict(os.environ, PATH=binn + os.pathsep + os.environ["PATH"]))
    assert r.returncode == 128, "MUTATION DID NOT LAND: the fake git was not used"
    return "git status did not run"


# ---------------------------------------------------------------- clean cases

def pristine(tmp):
    """A checkout nothing has written to. If this is not green nothing else means anything."""
    return None


def untracked_file(tmp):
    """A gate that leaves a build artefact has changed nothing that was committed."""
    p = os.path.join(tmp, "engine", "rendered_output.pdf")
    open(p, "w").write("build output\n")
    st = _git(tmp, "status", "--porcelain").stdout
    assert "rendered_output.pdf" in st, "MUTATION DID NOT LAND: git does not see the file"
    assert not _git(tmp, "status", "--porcelain", "-uno").stdout.strip(), \
        "fixture: an untracked file must not show under -uno"
    return None


def untracked_directory(tmp):
    p = os.path.join(tmp, "engine", "scratch_panels")
    os.makedirs(p)
    open(os.path.join(p, "panel.json"), "w").write("{}\n")
    assert "scratch_panels" in _git(tmp, "status", "--porcelain").stdout, \
        "MUTATION DID NOT LAND"
    return None


def no_baseline(tmp):
    """The --record step dropped from the run. Nothing to compare against [R-ENF-04]."""
    p = _baseline(tmp)
    assert os.path.exists(p), "MUTATION DID NOT LAND: there was no baseline to remove"
    os.remove(p)
    assert not os.path.exists(p), "MUTATION DID NOT LAND: the baseline survived"
    return "no baseline"


def already_dirty_and_unchanged(tmp):
    """A LOCAL pre-commit run: edits present before the checks, none made by them.

    This is the case that decides whether the gate asks the right question. Keyed on
    dirtiness it would be red on every run anybody makes by hand, which is the
    permanently-red check [R-ENF-02] forbids and the surest way to hide a real leak.
    """
    p = os.path.join(tmp, "engine", "keep.txt")
    open(p, "w").write("an edit the operator made before running the checks\n")
    assert _git(tmp, "status", "--porcelain", "-uno").stdout.strip(), \
        "MUTATION DID NOT LAND: git does not see the edit"
    return None


def stale_baseline(tmp):
    """A baseline left behind by an ABORTED earlier run, at a different commit.

    The baseline lives at a fixed path, so this is not hypothetical — it happened
    within an hour of the gate being written. A MISSING baseline already failed
    loudly; a STALE one compared against a different tree and reported staged files
    as "reverted", which is a confident wrong answer rather than an absent one.
    """
    p = _baseline(tmp)
    assert os.path.exists(p), "MUTATION DID NOT LAND: there is no baseline to stale"
    body = open(p).read()
    assert body.startswith("# head "), "MUTATION DID NOT LAND: baseline declares no head"
    open(p, "w").write("# head 0000000000000000000000000000000000000000\n"
                       + body.split("\n", 1)[1])
    assert open(p).read().startswith("# head 0000"), "MUTATION DID NOT LAND"
    return "describes a different tree"


RED = [
    ("a committed register rewritten while checks ran", register_rewritten, {}),
    ("a baseline left behind by an aborted run", stale_baseline, {}),
    ("the --record step is missing from the run", no_baseline, {"skip_record": True}),
    ("a tracked file deleted", tracked_file_deleted, {}),
    ("not a git work tree", not_a_work_tree, {}),
    ("git status refuses", git_status_refuses, {"env_path": True}),
]
CLEAN = [
    ("a pristine checkout", pristine, {}),
    ("edits made BEFORE the run, none made by it", already_dirty_and_unchanged,
     {"mutate_first": True}),
    ("an untracked build artefact", untracked_file, {}),
    ("an untracked directory of scratch output", untracked_directory, {}),
]


def _env(tmp, opts):
    if opts.get("env_path"):
        return dict(os.environ,
                    PATH=os.path.join(tmp, "fakebin") + os.pathsep + os.environ["PATH"])
    return None


def _case(tmp, fn, opts):
    """Record the baseline, then mutate, then compare — the order the workflow uses.

    `mutate_first` inverts it deliberately: that case is about an edit that existed
    BEFORE the checks ran, which is the whole point of a baseline.
    """
    if opts.get("mutate_first"):
        want = fn(tmp)
        if not opts.get("skip_record"):
            _record(tmp)
        return want
    if not opts.get("skip_record"):
        _record(tmp)
    else:
        _record(tmp)          # recorded, then removed by the case itself
    return fn(tmp)


def main():
    assert len(RED) == RED_EXPECTED, "a red case was deleted"
    assert len(CLEAN) == CLEAN_EXPECTED, "a clean case was deleted"
    assert len(RED) + len(CLEAN) == CASES_EXPECTED, "the case count moved"

    print("NEGATIVE CONTROL — check_tree_unmodified  [R-ENF-01]")
    print("   %d conditions: %d that must go RED, %d that must stay GREEN"
          % (CASES_EXPECTED, RED_EXPECTED, CLEAN_EXPECTED))
    bad = []

    for name, fn, opts in RED:
        tmp = _sandbox()
        try:
            want = _case(tmp, fn, opts)
            rc, out = _run(tmp, _env(tmp, opts))
            ok = rc != 0 and (want is None or want in out)
            print("   %-50s %s" % (name, "RED" if ok else "*** STAYED GREEN ***"))
            if not ok:
                bad.append("%s: rc=%d, expected %r\n%s" % (name, rc, want, out[-500:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    for name, fn, opts in CLEAN:
        tmp = _sandbox()
        try:
            _case(tmp, fn, opts)
            rc, out = _run(tmp, _env(tmp, opts))
            print("   %-50s %s" % (name, "green" if rc == 0 else "*** WENT RED ***"))
            if rc != 0:
                bad.append("%s: went red\n%s" % (name, out[-600:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    if bad:
        print("\nFAIL")
        for b in bad:
            print("  - " + b)
        return 1
    print("\nOK — %d of %d conditions behaved as the gate claims."
          % (CASES_EXPECTED, CASES_EXPECTED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
