"""Negative control for check_corrections_applied.  [R-ENF-01]

Every mutation asserts that it LANDED before the gate runs, and the case count is
asserted against a declared constant.

THE CLEAN HALF CARRIES THE CASE THIS GATE WAS NEARLY BROKEN BY: a study using the
word "correction" for something else entirely. SCEM records `corrections_applied:
69` in a revision note — a count of EDITORIAL corrections, on a study with no
walk-forward run — and a gate keying on the word rather than on the fields a study
makes its CLAIM in would have opened with a spectacular false positive about a
study that has done nothing wrong.
"""
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(HERE, "check_corrections_applied.py")

spec = importlib.util.spec_from_file_location("cca", TARGET)
cca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cca)


def _sandbox():
    tmp = tempfile.mkdtemp(prefix="ca-nc-")
    eng = os.path.join(tmp, "engine")
    os.makedirs(eng)
    for d in os.listdir(os.path.join(ROOT, "engine")):
        if not (d.endswith("_study") or d.endswith("_walkforward")):
            continue
        src = os.path.join(ROOT, "engine", d)
        for f in ("study_numbers.json", "corrections_log.json"):
            p = os.path.join(src, f)
            if os.path.exists(p):
                os.makedirs(os.path.join(eng, d), exist_ok=True)
                shutil.copy(p, os.path.join(eng, d, f))
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(TARGET, os.path.join(tmp, "scripts", "check_corrections_applied.py"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_corrections_applied.py")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def _nums(tmp, tk):
    return os.path.join(tmp, "engine", "%s_study" % tk, "study_numbers.json")


def _set_factor(o, value):
    """Set ARCC's claimed factor wherever it is stored; returns how many it changed."""
    n = 0

    def walk(x):
        nonlocal n
        if isinstance(x, dict):
            if "driver" in x and "factor" in x:
                x["factor"] = value
                n += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(o)
    return n


def wrong_factor(tmp):
    p = _nums(tmp, "arcc")
    o = json.load(open(p))
    assert _set_factor(o, 1.5), "MUTATION DID NOT LAND: no factor to change"
    json.dump(o, open(p, "w"))
    return "DOES NOT RECONCILE"


def unadopted_driver(tmp):
    p = _nums(tmp, "arcc")
    o = json.load(open(p))
    hit = 0

    def walk(x):
        nonlocal hit
        if isinstance(x, dict):
            if x.get("driver") and "factor" in x:
                x["driver"] = "a_driver_the_run_never_adopted"
                hit += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(o)
    assert hit, "MUTATION DID NOT LAND"
    json.dump(o, open(p, "w"))
    return "NOT ADOPTED BY THE RUN"


def no_run(tmp):
    p = os.path.join(tmp, "engine", "arcc_walkforward", "corrections_log.json")
    assert os.path.exists(p), "MUTATION DID NOT LAND: no log to remove"
    os.unlink(p)
    return "NO RUN"


def silent_while_run_adopted(tmp):
    """A study declaring none while its own run adopted one."""
    p = _nums(tmp, "arcc")
    o = json.load(open(p))
    removed = 0

    def walk(x):
        nonlocal removed
        if isinstance(x, dict):
            for k in list(x):
                if k in ("adopted_correction", "adopted_corrections"):
                    del x[k]
                    removed += 1
                else:
                    walk(x[k])
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(o)
    assert removed, "MUTATION DID NOT LAND: nothing removed"
    o["corrections_adopted"] = 0
    json.dump(o, open(p, "w"))
    return "the study says none"


def unparseable(tmp):
    p = _nums(tmp, "amoc")
    open(p, "w").write("{ this is not json")
    return "will not parse"


def empty_population(tmp):
    eng = os.path.join(tmp, "engine")
    n = 0
    for d in list(os.listdir(eng)):
        if d.endswith("_study"):
            shutil.rmtree(os.path.join(eng, d))
            n += 1
    assert n, "MUTATION DID NOT LAND"
    return "REFUSED"



def silent_with_a_run(tmp):
    """A study with a walk-forward run whose numbers file says nothing either way.

    THE CONDITION THIS FILE'S TARGET PROMISED TO REFUSE AND DID NOT: its opening
    paragraph has said since it was written that silence and "none adopted" are the
    same file to a reader and different facts about the work, while the code skipped
    a silent study with a `continue`. PHDC was in exactly that state when the clause
    was finally implemented."""
    p = _nums(tmp, "egch")
    o = json.load(open(p))
    removed = 0

    def walk(x):
        nonlocal removed
        if isinstance(x, dict):
            for k in list(x):
                if k in ("adopted_correction", "adopted_corrections",
                         "corrections_adopted"):
                    del x[k]
                    removed += 1
                else:
                    walk(x[k])
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(o)
    assert removed, "MUTATION DID NOT LAND: nothing removed"
    json.dump(o, open(p, "w"))
    a, d = cca.claims(json.load(open(p)))
    assert not a and not d, "MUTATION DID NOT LAND: the study still makes a claim"
    return "SILENT"


def unknown_record_shape(tmp):
    """A run this file has no named adapter for. Must be REPORTED, never read as
    having adopted nothing — the [R-ENF-04] shape the adapters were written for."""
    src = os.path.join(tmp, "engine", "arcc_walkforward", "corrections_log.json")
    d = os.path.join(tmp, "engine", "newco_walkforward")
    os.makedirs(d, exist_ok=True)
    shutil.copy(src, os.path.join(d, "corrections_log.json"))
    sd = os.path.join(tmp, "engine", "newco_study")
    os.makedirs(sd, exist_ok=True)
    json.dump({"walkforward": {"adopted_correction": {"driver": "x", "factor": 1.01}}},
              open(os.path.join(sd, "study_numbers.json"), "w"))
    assert "NEWCO" not in cca.ADAPTERS, "MUTATION DID NOT LAND: NEWCO has an adapter"
    return "UNKNOWN RECORD SHAPE"



RED = [
    ("a claimed factor that does not reproduce from the run's bias", wrong_factor),
    ("a correction the run never adopted", unadopted_driver),
    ("a claim with no walk-forward run behind it", no_run),
    ("a study declaring none while its run adopted one", silent_while_run_adopted),
    ("a numbers file that will not parse", unparseable),
    ("an emptied population", empty_population),
    ("a study with a run that says nothing either way", silent_with_a_run),
    ("a run whose record matches no named adapter", unknown_record_shape),
]


def clean_untouched(tmp):
    return None


def clean_editorial_word(tmp):
    """THE CASE THIS GATE WAS NEARLY BROKEN BY, kept as it actually ships.

    SCEM's `corrections_applied: 69` is a count of editorial corrections in a
    revision note, on a study with no walk-forward run. It must not fire.
    """
    p = _nums(tmp, "scem")
    o = json.load(open(p))
    found = json.dumps(o).count('"corrections_applied"')
    assert found, "FIXTURE IS NOT THE REAL CASE: SCEM no longer carries the key"
    return None


def clean_declared_none(tmp):
    """A study declaring none whose run adopted none: the ordinary honest state."""
    p = _nums(tmp, "egch")
    o = json.load(open(p))
    assert any(v == 0 for v in cca._find(o, "corrections_adopted")), \
        "FIXTURE IS NOT THE REAL CASE: EGCH no longer declares none"
    return None



def clean_silent_without_a_run(tmp):
    """A study with NO walk-forward and a numbers file silent on corrections.

    EIGHTEEN OF THE BOOK'S STUDIES ARE IN THIS STATE and every one is correct: a
    study with no run has nothing to declare, and a silence clause that fired on it
    would be a false claim about what this gate checks."""
    tk = "savola"
    p = _nums(tmp, tk)
    assert os.path.exists(p), "FIXTURE: no %s numbers file in the sandbox" % tk
    a, d = cca.claims(json.load(open(p)))
    assert not a and not d, "FIXTURE IS NOT THE REAL CASE: %s makes a claim" % tk
    assert not os.path.isdir(os.path.join(tmp, "engine", "%s_walkforward" % tk)), \
        "FIXTURE IS NOT THE REAL CASE: %s has a run" % tk
    return None


def clean_phdc_conformed(tmp):
    """PHDC declaring both numbers: six shifts APPLIED inside the test, zero
    PROMOTED. Two quantities under two names, which is the point — writing either
    alone under a name that could mean the other is the defect the declaration was
    written to avoid."""
    o = json.load(open(_nums(tmp, "phdc")))
    wf = o.get("walkforward", {})
    assert wf.get("corrections_applied_in_walkforward") == 6, \
        "FIXTURE IS NOT THE REAL CASE: PHDC's applied count moved"
    assert wf.get("corrections_adopted") == 0, \
        "FIXTURE IS NOT THE REAL CASE: PHDC no longer declares zero adopted"
    return None



CLEAN = [
    ("the records exactly as they ship", clean_untouched),
    ("a study using the word for editorial corrections", clean_editorial_word),
    ("a study declaring none whose run adopted none", clean_declared_none),
    ("a study with NO run that says nothing", clean_silent_without_a_run),
    ("PHDC declaring six applied and zero adopted", clean_phdc_conformed),
]

EXPECTED_RED, EXPECTED_CLEAN = 8, 5
assert len(RED) == EXPECTED_RED and len(CLEAN) == EXPECTED_CLEAN, (
    "CASE COUNT CHANGED — update the declared constants deliberately.")

caught = passed = 0
for name, fn in RED:
    tmp = _sandbox()
    try:
        marker = fn(tmp)
        code, out = _run(tmp)
        ok = code != 0 and (marker is None or marker in out)
        caught += ok
        print("  %s %s" % ("CAUGHT " if ok else "MISSED ", name))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

for name, fn in CLEAN:
    tmp = _sandbox()
    try:
        fn(tmp)
        code, out = _run(tmp)
        ok = code == 0
        passed += ok
        print("  %s %s%s" % ("PASSED " if ok else "FALSE+ ", name,
                             "" if ok else "\n           "
                             + out.strip().splitlines()[-1]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print("\n%d/%d defects caught, %d/%d clean cases passed"
      % (caught, EXPECTED_RED, passed, EXPECTED_CLEAN))
if caught != EXPECTED_RED or passed != EXPECTED_CLEAN:
    print("FAIL — the corrections-applied gate does not do what it claims.")
    sys.exit(1)
print("OK — a claim that does not reconcile is refused; the word used for something "
      "else is not.")
