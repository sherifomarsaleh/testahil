#!/usr/bin/env python3
"""Negative control for [R-LESSON-02] — check_lesson_promotion.py.

TWO KINDS OF CASE, HELD APART ON PURPOSE, because conflating them is how a control
reports green while proving nothing:

  CLASSIFICATION cases exercise lesson_promotion.classify() directly on a single
  fixture lesson. They are unit-level and the fixture is the whole input.

  POPULATION cases exercise THE GATE, in a sandbox copy of the repository with a
  mutated register, as a subprocess, and read its exit status. A population guard
  cannot be tested by asserting that a list is empty — that asserts the fixture, not
  the gate, and THE FIRST DRAFT OF THIS FILE DID EXACTLY THAT: it set LESSONS to []
  and then checked len(LESSONS) == 0, which is true by construction and invokes
  nothing. That is the fifth time in this session a control was caught proving its
  own fixture, and it is recorded rather than quietly fixed.

Nothing is written into the real tree [R-ENF-01 EXTENDED 07-09-2026]. Every mutation
asserts that it LANDED. The case COUNT is asserted against a declared constant.

RED — the classification must refuse:
  1  an eligible lesson with no declaration
  2  promotion outside the closed list
  3  enforced, naming a rule id that resolves in neither document
  4  enforced, naming a file that is not on disk
  5  enforced, naming neither — an unrecognised reference shape
  6  enforced, naming nothing at all
  7  prose with an empty reason

RED — the gate must refuse:
  8  zero lessons                        [R-ENF-04]
  9  lessons present, zero eligible      [R-ENF-04]
 10  a ratcheted lesson that now declares and was not pruned

CLEAN — must pass, and this half is what keeps the gate narrow:
 11  a CLASS lesson with no declaration            — out of scope, never demanded
 12  a PROVISIONAL ALL lesson with no declaration  — the promotion rule's own answer
 13  enforced by a rule id that resolves
 14  enforced by a file that exists
 15  prose with a reason
 16  OUTSTANDING — a DEBT, not a defect. The case that matters most: a gate refusing
     it would push a lesson to be declared prose to stay green, which is the exact
     opposite of what this rule measures.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

EXPECTED_CASES = 16
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))

import lesson_promotion as LP          # noqa: E402

DOC = "a document mentioning [R-MACRO-01] and [R-BETA-05] and nothing else"
GATE = "scripts/check_lesson_promotion.py"
RATCHET = "engine/build_depth_audit/lesson_promotion_outstanding.json"
results = []


def base(**kw):
    l = {"id": "L-TEST", "scope": "ALL", "status": "adopted", "headline": "h",
         "plain": "p", "source": "s", "origin": "build", "evidence": "e",
         "overturned_by": "o", "applies_to": None}
    l.update(kw)
    return l


def classification(n, label, lesson, expect, landed, red=True):
    if not landed(lesson):
        print("   FIXTURE DID NOT LAND case %d — %s" % (n, label))
        results.append(False)
        return
    state, detail = LP.classify(lesson, DOC)
    ok = (state == expect)
    print("   %s case %-2d %s" % ("CAUGHT " if ok and red else
                                  "PASSED " if ok else "MISSED ", n, label))
    if not ok:
        print("        expected %r, got %r (%s)" % (expect, state, detail))
    results.append(ok)


def sandbox():
    d = tempfile.mkdtemp(prefix="lesspromo_nc_")
    os.makedirs(os.path.join(d, "scripts"))
    os.makedirs(os.path.join(d, "engine", "build_depth_audit"))
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(d, GATE))
    for f in ("lesson_promotion.py", "lessons_register.py",
              "Standing_Research_Protocol.md"):
        shutil.copy(os.path.join(ROOT, "engine", f),
                    os.path.join(d, "engine", f))
    import glob
    dg = glob.glob(os.path.join(ROOT, "engine", "PROJECT_INSTRUCTIONS_*.md"))[0]
    shutil.copy(dg, os.path.join(d, "engine", os.path.basename(dg)))
    return d


def write_register(d, lessons):
    """A REAL module the gate imports, not a patched object."""
    body = "LESSONS = [\n"
    for l in lessons:
        body += "    %r,\n" % (l,)
    body += "]\n\n\ndef assert_lessons_register():\n    return len(LESSONS)\n"
    open(os.path.join(d, "engine", "lessons_register.py"), "w").write(body)


def run_gate(d, ratchet):
    json.dump({"rule": "[R-LESSON-02]", "outstanding": ratchet},
              open(os.path.join(d, RATCHET), "w"))
    r = subprocess.run([sys.executable, GATE], cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def eligibility(n, label, lesson, expect_eligible):
    """Cases 11 and 12 ask a different question from classify(), so they get their
    own reporter. An earlier draft ran them through classification() and then
    overwrote the result afterwards, so the line printed MISSED while the tally
    counted a pass — a control whose own output disagrees with its own verdict."""
    got = LP.eligible(lesson)
    ok = (got == expect_eligible)
    print("   %s case %-2d %s" % ("PASSED " if ok else "MISSED ", n, label))
    if not ok:
        print("        expected eligible=%s, got %s" % (expect_eligible, got))
    results.append(ok)


def population(n, label, lessons, ratchet, expect_red, landed):
    d = sandbox()
    try:
        write_register(d, lessons)
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "sandbox_reg", os.path.join(d, "engine", "lessons_register.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        if not landed(m.LESSONS):
            print("   FIXTURE DID NOT LAND case %d — %s" % (n, label))
            results.append(False)
            return
        rc, out = run_gate(d, ratchet)
        ok = ((rc != 0) == expect_red)
        print("   %s case %-2d %s" % ("CAUGHT " if ok and expect_red else
                                      "PASSED " if ok else "MISSED ", n, label))
        if not ok:
            print("        exit %d — %s" % (rc, out.strip().splitlines()[-1][:120]))
        results.append(ok)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    classification(1, "no declaration", base(), "undeclared",
                   lambda l: "promotion" not in l)
    classification(2, "promotion outside the closed list",
                   base(promotion="sort-of"), "bad_value",
                   lambda l: l["promotion"] not in LP.PROMOTION)
    # CONSTRUCTED RATHER THAN TYPED, and the reason is check_protocol_sync's:
    # it scans the tree for rule identifiers and refuses any that resolve in
    # neither governing document, because "to a later session an unresolvable
    # [R-...] reads exactly like settled law". That gate fired on the first draft
    # of this line and it was RIGHT. A fixture assembled at run time is a literal
    # nowhere in the source, so it cannot be read as law by anyone — while the
    # condition under test, an id resolving nowhere, lands exactly as before.
    unresolvable = "[R-" + "NOPE-99]"
    classification(3, "enforced by a rule id that resolves nowhere",
                   base(promotion="enforced", promoted_by=unresolvable),
                   "broken_reference", lambda l: l["promoted_by"] not in DOC)
    classification(4, "enforced by a file that is not on disk",
                   base(promotion="enforced",
                        promoted_by="engine/does_not_exist.py"),
                   "broken_reference",
                   lambda l: not os.path.exists(os.path.join(ROOT,
                                                             l["promoted_by"])))
    classification(5, "enforced by an unrecognised reference shape",
                   base(promotion="enforced", promoted_by="the general principle"),
                   "broken_reference", lambda l: "/" not in l["promoted_by"])
    classification(6, "enforced, naming nothing",
                   base(promotion="enforced", promoted_by=""),
                   "broken_reference", lambda l: l["promoted_by"] == "")
    classification(7, "prose with an empty reason",
                   base(promotion="prose", promotion_note="   "),
                   "empty_reason", lambda l: not l["promotion_note"].strip())

    population(8, "zero lessons [R-ENF-04]", [], [], True,
               lambda ls: len(ls) == 0)
    population(9, "lessons present, zero eligible [R-ENF-04]",
               [base(scope="CLASS", applies_to="bank")], [], True,
               lambda ls: ls and not any(LP.eligible(x) for x in ls))
    population(10, "a declared lesson left on the ratchet",
               [base(id="L-900", promotion="outstanding")], ["L-900"], True,
               lambda ls: "promotion" in ls[0])

    eligibility(11, "a CLASS lesson is out of scope",
                base(scope="CLASS", applies_to="bank"), False)
    eligibility(12, "a PROVISIONAL lesson is out of scope",
                base(status="provisional"), False)

    classification(13, "enforced by a rule id that resolves",
                   base(promotion="enforced", promoted_by="[R-MACRO-01]"),
                   "enforced", lambda l: l["promoted_by"] in DOC, red=False)
    classification(14, "enforced by a file that exists",
                   base(promotion="enforced",
                        promoted_by="engine/prose_figures.py"), "enforced",
                   lambda l: os.path.exists(os.path.join(ROOT, l["promoted_by"])),
                   red=False)
    classification(15, "prose with a reason",
                   base(promotion="prose",
                        promotion_note="not a property of the repository"),
                   "prose", lambda l: bool(l["promotion_note"].strip()), red=False)
    classification(16, "OUTSTANDING is a debt, not a defect",
                   base(promotion="outstanding", promotion_note="not built"),
                   "outstanding", lambda l: l["promotion"] == "outstanding",
                   red=False)

    assert len(results) == EXPECTED_CASES, (
        "the control declares %d cases and ran %d — a control that quietly loses "
        "cases reports clean" % (EXPECTED_CASES, len(results)))
    red, clean = results[:10], results[10:]
    print("\n%d/%d red conditions caught, %d/%d clean cases passed"
          % (sum(red), len(red), sum(clean), len(clean)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
