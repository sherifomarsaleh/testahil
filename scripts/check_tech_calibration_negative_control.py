#!/usr/bin/env python3
"""Prove the technical-calibration check can actually fail.  [R-TCAL-01]

A check nobody has seen go red is not evidence that it works [R-ENF-04]. This
injects each defect the checker claims to catch, one at a time, and fails if
the checker reports clean on any of them. Everything is restored afterwards,
and the restore is verified byte for byte rather than assumed.

The injections are the real failure shapes this project has already lived
through: a record certifying a module that has moved on (the frozen-chart
species), a population that quietly lost a member (the "0 skipped" species),
a generated file hand-drifted from its generator (the digest species), and an
id in a delivered document that resolves to nothing (the T-013 defect the
checker's orphan test caught on the day it was written).
"""
import glob
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
LAB = os.path.join(ENGINE, "lab", "ta_calibration")
RECORDS = os.path.join(ENGINE, "tech_records.json")
PAYLOAD = os.path.join(LAB, "register_payload.json")
DOCX = os.path.join(LAB, "Technical_Lessons_Register.docx")
CHECK = os.path.join(ROOT, "scripts", "check_tech_calibration.py")


def run():
    r = subprocess.run([sys.executable, CHECK], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    rc, _ = run()
    if rc != 0:
        print("PRECONDITION FAILED — the calibration check is already red, so "
              "this control cannot prove anything. Fix that first.")
        return 1
    print("  precondition: the check is green before any injection")

    # A STALE BACKUP MEANS A PREVIOUS RUN DID NOT FINISH RESTORING, AND THE TREE MAY
    # STILL CARRY AN INJECTED DEFECT. Refusing here is the difference between a defect
    # that announces itself and one that gets committed: on 09-09-2026 a run of this
    # control was killed between injecting "(edited by hand)" into register_payload.json
    # and restoring it, `git add -A` swept the injected fixture into a commit, and CI
    # went red on a hand-edit nobody had made. The tell was there -- the backup
    # directory was still on disk -- and nothing read it.
    # ONE INSTANCE AT A TIME. This control INJECTS DEFECTS INTO REAL TRACKED FILES and
    # restores them, so two instances interleave catastrophically: A backs up the clean
    # file, B injects, A restores its backup, B restores ITS backup -- which is A's
    # injected state -- and the tree keeps a defect nobody wrote. It is not a
    # hypothetical: on 09-09-2026 register_payload.json came back carrying
    # "(edited by hand)" twice, once from a killed run and once while a subagent was
    # running gates in parallel, and the second time the control had already reported
    # "green again after every restore" on its own postcondition. A postcondition can
    # only speak for the instant it ran.
    lock = os.path.join(ROOT, ".git", "tcal_nc.lock")
    try:
        _fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(_fd, str(os.getpid()).encode())
        os.close(_fd)
    except FileExistsError:
        try:
            _held = open(lock).read().strip()
        except OSError:
            _held = ""
        _alive = False
        if _held.isdigit():
            try:
                os.kill(int(_held), 0)
                _alive = True
            except OSError:
                pass
        if _alive:
            print("REFUSED — another run of this control is live (pid %s). It injects "
                  "defects into real tracked files; two runs interleave and leave a "
                  "defect in the tree that neither one wrote." % _held)
            return 1
        os.unlink(lock)          # stale: the holder is gone
        _fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(_fd, str(os.getpid()).encode())
        os.close(_fd)

    stale = sorted(glob.glob(os.path.join(tempfile.gettempdir(), "tcal-nc-*")))
    if stale:
        print("REFUSED — %d backup directory/ies from an earlier run are still on "
              "disk:" % len(stale))
        for d in stale:
            print("    %s   holding: %s" % (d, ", ".join(sorted(os.listdir(d))) or "(empty)"))
        print("  A run that did not finish may have left an INJECTED DEFECT in the "
              "tree. Check `git status`, restore from the directory above or "
              "regenerate (engine/lab/ta_calibration/build_register.py), then delete "
              "it and re-run. An injected fixture that reaches a commit reads as a "
              "real defect and costs a CI cycle to diagnose.")
        try:
            os.unlink(lock)
        except OSError:
            pass
        return 1

    backup = tempfile.mkdtemp(prefix="tcal-nc-")
    originals = {}
    for p in (RECORDS, PAYLOAD, DOCX):
        dst = os.path.join(backup, os.path.basename(p))
        shutil.copy2(p, dst)
        originals[p] = dst

    # EVERY INJECTION IS UNDONE EVEN IF THE RUN DIES. The body below mutates real
    # files in the working tree and restores them line by line, so any exception --
    # or a SIGTERM, or a Ctrl-C -- between an injection and its restore used to leave
    # the defect behind. It is wrapped now, and the signals are caught so the same
    # unwind runs. SIGKILL still cannot be caught by anything; for that case the
    # stale-backup refusal above is the backstop.
    def _unwind(*_a):
        for src in originals:
            try:
                shutil.copy2(originals[src], src)
            except OSError:
                pass
        raise SystemExit("interrupted — every injected defect was restored")

    for _sig in (signal.SIGINT, signal.SIGTERM):
        try:
            signal.signal(_sig, _unwind)
        except (ValueError, OSError):
            pass          # not the main thread, or the platform will not take it

    try:
        return _body(backup, originals)
    except BaseException:
        for src in originals:
            try:
                shutil.copy2(originals[src], src)
            except OSError:
                pass
        raise
    finally:
        try:
            os.unlink(lock)
        except OSError:
            pass


def _body(backup, originals):
    misses = []

    def restore(p):
        shutil.copy2(originals[p], p)
        if open(p, "rb").read() != open(originals[p], "rb").read():
            raise RuntimeError("restore of %s did not restore it" % p)

    def inject(name, expect_fragment):
        rc, out = run()
        if rc == 0:
            misses.append("%s: checker reported CLEAN" % name)
            print("  [MISS] %s — checker stayed green" % name)
        elif expect_fragment not in out:
            misses.append("%s: red, but not for the injected reason" % name)
            print("  [MISS] %s — red for the wrong reason" % name)
        else:
            print("  [ok]   %s — caught" % name)

    # A — the read moved without its record
    doc = json.load(open(RECORDS))
    doc["read_sha256"] = "0" * 64
    json.dump(doc, open(RECORDS, "w"), indent=1)
    inject("read moved, record did not", "the read moved without its record")
    restore(RECORDS)

    # B — a library quietly dropped from the record
    doc = json.load(open(RECORDS))
    victim = sorted(doc["records"])[0]
    del doc["records"][victim]
    json.dump(doc, open(RECORDS, "w"), indent=1)
    inject("population lost a member", "missing a horizon")
    restore(RECORDS)

    # C — the payload hand-drifted from its generator
    p = json.load(open(PAYLOAD))
    p["lessons"][0]["title"] = p["lessons"][0]["title"] + " (edited by hand)"
    json.dump(p, open(PAYLOAD, "w"), indent=1)
    inject("payload drifted from generator", "not the generated form")
    restore(PAYLOAD)

    # D — the delivered document cites an id that resolves to nothing:
    # the T-013 defect, reinjected in its exact shape
    try:
        from docx import Document
        d = Document(DOCX)
        d.add_paragraph("Scored in T-013 and not adopted.")
        d.save(DOCX)
        inject("orphan id in the document", "resolve to no lesson")
        restore(DOCX)
    except ImportError:
        print("  [--]   python-docx not installed; orphan injection skipped "
              "(the checker skips the same ground without it)")

    rc, _ = run()
    if rc != 0:
        print("POSTCONDITION FAILED — the tree did not come back clean after "
              "restore; inspect %s" % backup)
        return 1
    print("  postcondition: green again after every restore")
    shutil.rmtree(backup)

    if misses:
        print("\nNEGATIVE CONTROL FAILED — %d injected defect(s) not caught:"
              % len(misses))
        for m in misses:
            print("  - %s" % m)
        return 1
    print("\nnegative control OK — every injected defect went red")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
