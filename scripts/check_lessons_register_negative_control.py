#!/usr/bin/env python3
"""Prove the lessons-register check can actually fail.

A check nobody has seen go red is not evidence that it works. This injects each
defect the checker claims to catch, one at a time, and fails if the checker
reports clean on any of them. Everything is restored afterwards, and the restore
is verified rather than assumed.

The defects injected are the real ones this project has already lived through in
other forms: a document that drifted from its source, a rule scoped to something
that does not exist, and a register that quietly stopped being fed.
"""
import os, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
MD = os.path.join(ENGINE, "Lessons_Register.md")
PY = os.path.join(ENGINE, "lessons_register.py")
CHECK = os.path.join(ROOT, "scripts", "check_lessons_register.py")


def run():
    r = subprocess.run([sys.executable, CHECK], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def _unresolve_a_draft():
    """Take one resolved draft back to open, as if nobody had ruled on it."""
    import json
    for d in sorted(os.listdir(ENGINE)):
        if not d.endswith("_walkforward"):
            continue
        p = os.path.join(ENGINE, d, "lessons_draft.json")
        if not os.path.exists(p):
            continue
        doc = json.load(open(p))
        for x in doc.get("drafts", []):
            if x.get("registered") or x.get("declined"):
                DRAFTS_TOUCHED.append((p, json.dumps(doc)))
                x.pop("registered", None)
                x.pop("declined", None)
                json.dump(doc, open(p, "w"), indent=1)
                return
    raise RuntimeError("no resolved draft to un-resolve — this control cannot "
                       "test the case it claims to")


DRAFTS_TOUCHED = []


def main():
    rc, _ = run()
    if rc != 0:
        print("PRECONDITION FAILED — the register is already red, so this "
              "control cannot prove anything. Fix the register first.")
        return 1
    print("  precondition: the check is green before any injection")

    backup = tempfile.mkdtemp(prefix="lessons-nc-")
    shutil.copy2(MD, backup)
    shutil.copy2(PY, backup)
    failures = []

    cases = [
        ("the document drifts from its generator",
         lambda: open(MD, "a").write("\n\nAn edit nobody generated.\n")),

        ("a lesson is scoped to a company that does not exist",
         lambda: open(PY, "a").write(
             '\nLESSONS.append(L("L-999", "STOCK", "NOTAREALTICKER",'
             ' "x.", "x.", "x", "build", "x", "x"))\n')),

        ("a lesson id is invented in the document with nothing behind it",
         lambda: open(MD, "a").write("\n\nSee L-888 for details.\n")),

        ("a class is registered with no lesson under it",
         lambda: open(PY, "a").write(
             '\nCLASSES = CLASSES + ("a class nobody wrote a lesson for",)\n')),

        ("a lesson exists that the Word file does not carry",
         lambda: open(PY, "a").write(
             '\nLESSONS.append(L("L-097", "ALL", None, "x.", "x.", "x",'
             ' "build", "x", "x"))\n')),

        ("a harvested finding is left neither registered nor declined",
         _unresolve_a_draft),
    ]

    for name, inject in cases:
        shutil.copy2(os.path.join(backup, os.path.basename(MD)), MD)
        shutil.copy2(os.path.join(backup, os.path.basename(PY)), PY)
        for path, original in DRAFTS_TOUCHED:
            open(path, "w").write(original)
        DRAFTS_TOUCHED.clear()
        inject()
        rc, out = run()
        if rc == 0:
            failures.append(name)
            print("  [MISSED] %s — the check still reported clean" % name)
        else:
            print("  [caught] %s" % name)

    shutil.copy2(os.path.join(backup, os.path.basename(MD)), MD)
    shutil.copy2(os.path.join(backup, os.path.basename(PY)), PY)
    for path, original in DRAFTS_TOUCHED:
        open(path, "w").write(original)
    shutil.rmtree(backup, ignore_errors=True)

    rc, out = run()
    if rc != 0:
        print("\nRESTORE FAILED — the register did not come back clean:\n" + out)
        return 1
    print("  restored: the check is green again")

    if failures:
        print("\nFAILED — %d defect(s) the checker does not catch:" % len(failures))
        for f in failures:
            print("  - %s" % f)
        return 1
    print("\nnegative control passed — every injected defect was caught")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
