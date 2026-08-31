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
import json
import os
import shutil
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

    backup = tempfile.mkdtemp(prefix="tcal-nc-")
    originals = {}
    for p in (RECORDS, PAYLOAD, DOCX):
        dst = os.path.join(backup, os.path.basename(p))
        shutil.copy2(p, dst)
        originals[p] = dst

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
