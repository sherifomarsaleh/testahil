"""Negative control for check_driver_coverage.  [R-ENF-01]

Reinjects every condition the gate claims to refuse, and the clean cases it must
not fire on. EVERY MUTATION ASSERTS THAT IT LANDED before the gate runs — four
negative controls in this repository have been caught passing a fixture that never
injected its condition, so a case that cannot prove it changed anything is evidence
of nothing. The case COUNT is asserted against a declared constant, so a later edit
cannot delete a case and leave the file reporting clean.

THE CLEAN HALF IS THE HALF THAT MATTERS HERE. This gate requires a DISCLOSURE and
never a level, so a driver honestly scored on a fraction of its cells must stay
GREEN — a check that failed on it would push a run to drop the disclosure or to
narrow the denominator, which is the move-the-number-to-satisfy-the-check offence.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(HERE, "check_driver_coverage.py")

spec = importlib.util.spec_from_file_location("cdc", TARGET)
cdc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cdc)

# Mutations are applied to a COPY of the real records, so every fixture starts from
# what actually ships rather than from something invented to be easy.
SRC = os.path.join(ROOT, "engine")


def _sandbox():
    tmp = tempfile.mkdtemp(prefix="cov-nc-")
    eng = os.path.join(tmp, "engine")
    os.makedirs(eng)
    for _, d, _s in cdc.RUNS:
        src = os.path.join(SRC, d)
        if not os.path.isdir(src):
            continue
        os.makedirs(os.path.join(eng, d))
        for f in ("scores.json", "error_cells.json"):
            p = os.path.join(src, f)
            if os.path.exists(p):
                shutil.copy(p, os.path.join(eng, d, f))
    shutil.copy(TARGET, os.path.join(tmp, "check_driver_coverage.py"))
    os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
    shutil.copy(TARGET, os.path.join(tmp, "scripts", "check_driver_coverage.py"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_driver_coverage.py")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def _scores(tmp, d):
    return os.path.join(tmp, "engine", d, "scores.json")


def drop_pair(tmp):
    """A driver publishing n with no n_cells — every record before 07-09-2026."""
    p = _scores(tmp, "egch_walkforward")
    o = json.load(open(p))
    k = sorted(o["by_driver"])[0]
    assert "n_cells" in o["by_driver"][k], "MUTATION DID NOT LAND: no pair to drop"
    del o["by_driver"][k]["n_cells"]
    json.dump(o, open(p, "w"))
    return "n_cells"


def wrong_denominator(tmp):
    """A denominator that does not reproduce from the run's own cells."""
    p = _scores(tmp, "arcc_walkforward")
    o = json.load(open(p))
    k = sorted(o["by_driver"])[0]
    before = o["by_driver"][k]["n_cells"]
    o["by_driver"][k]["n_cells"] = before + 7
    assert o["by_driver"][k]["n_cells"] != before, "MUTATION DID NOT LAND"
    json.dump(o, open(p, "w"))
    return "the committed cells say"


def more_than_exist(tmp):
    """More cells scored than exist — arithmetically impossible."""
    p = _scores(tmp, "tmgh_walkforward")
    o = json.load(open(p))
    k = sorted(o["by_driver"])[0]
    o["by_driver"][k]["n"] = o["by_driver"][k]["n_cells"] + 1
    assert o["by_driver"][k]["n"] > o["by_driver"][k]["n_cells"], "MUTATION DID NOT LAND"
    json.dump(o, open(p, "w"))
    return "more cells taken than exist"


def phantom_driver(tmp):
    """A driver published but absent from the per-cell file: unverifiable."""
    p = _scores(tmp, "phdc_walkforward")
    o = json.load(open(p))
    o["by_driver"]["a_driver_that_is_in_no_cell"] = {"n": 4, "n_cells": 9}
    assert "a_driver_that_is_in_no_cell" in o["by_driver"], "MUTATION DID NOT LAND"
    json.dump(o, open(p, "w"))
    return "absent from the per-cell file"


def no_block(tmp):
    """A run whose by_driver cannot be read — REPORTED, never skipped."""
    p = _scores(tmp, "amoc_walkforward")
    o = json.load(open(p))
    assert "by_driver" in o, "MUTATION DID NOT LAND: no block to remove"
    del o["by_driver"]
    json.dump(o, open(p, "w"))
    return "no readable by_driver block"


def empty_population(tmp):
    """Every run gone: a pass that read nothing must REFUSE [R-ENF-04]."""
    removed = 0
    for _, d, _s in cdc.RUNS:
        p = os.path.join(tmp, "engine", d)
        if os.path.isdir(p):
            shutil.rmtree(p)
            removed += 1
    assert removed, "MUTATION DID NOT LAND: nothing to remove"
    return "REFUSED"


RED = [
    ("a driver publishing n with no n_cells", drop_pair),
    ("a denominator that does not reproduce from the cells", wrong_denominator),
    ("more cells scored than exist", more_than_exist),
    ("a driver published but in no cell", phantom_driver),
    ("a run with no readable by_driver block", no_block),
    ("an emptied population", empty_population),
]


def clean_untouched(tmp):
    return None


def clean_low_coverage(tmp):
    """A driver honestly scored on a small fraction MUST NOT FIRE.

    This gate requires a disclosure and never a level. EGCH already ships one at
    5%; this drives another run to the same shape so the clean case does not rest
    on one study happening to carry it.
    """
    p = _scores(tmp, "tmgh_walkforward")
    cp = os.path.join(tmp, "engine", "tmgh_walkforward", "error_cells.json")
    o = json.load(open(p))
    cells = json.load(open(cp))
    k = sorted(o["by_driver"])[0]
    hit = 0
    for r in cells:
        if r.get("setting") == "asknown" and r.get("driver") == k \
                and r.get("log_error") is not None and hit < 900:
            r["log_error"] = None
            r["dropped"] = "non_positive"
            hit += 1
    assert hit, "MUTATION DID NOT LAND: no cells blanked"
    scored = sum(1 for r in cells if r.get("setting") == "asknown"
                 and r.get("driver") == k and r.get("log_error") is not None)
    total = sum(1 for r in cells if r.get("setting") == "asknown" and r.get("driver") == k)
    assert total and scored / total < 0.5, "MUTATION DID NOT LAND: still at or above half"
    o["by_driver"][k]["n"] = scored
    o["by_driver"][k]["n_cells"] = total
    json.dump(o, open(p, "w"))
    json.dump(cells, open(cp, "w"))
    return None


def clean_zero_coverage(tmp):
    """A driver scored on NONE of its cells is a disclosure, not a failure."""
    p = _scores(tmp, "phdc_walkforward")
    cp = os.path.join(tmp, "engine", "phdc_walkforward", "error_cells.json")
    o = json.load(open(p))
    cells = json.load(open(cp))
    k = sorted(o["by_driver"])[0]
    hit = 0
    for r in cells.get("as_known", []):
        if r.get("field") == k and r.get("e") is not None:
            r["e"] = None
            r["dropped"] = "non_positive"
            hit += 1
    assert hit, "MUTATION DID NOT LAND: no cells blanked"
    total = sum(1 for r in cells.get("as_known", []) if r.get("field") == k)
    o["by_driver"][k]["n"] = 0
    o["by_driver"][k]["n_cells"] = total
    json.dump(o, open(p, "w"))
    json.dump(cells, open(cp, "w"))
    return None


CLEAN = [
    ("the records exactly as they ship", clean_untouched),
    ("a driver honestly scored on under half its cells", clean_low_coverage),
    ("a driver honestly scored on none of its cells", clean_zero_coverage),
]

EXPECTED_RED, EXPECTED_CLEAN = 6, 3
assert len(RED) == EXPECTED_RED and len(CLEAN) == EXPECTED_CLEAN, (
    "CASE COUNT CHANGED — update the declared constants deliberately; a control "
    "that silently shrinks reports clean.")

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
                             "" if ok else "\n           " + out.strip().splitlines()[-1]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

print("\n%d/%d defects caught, %d/%d clean cases passed"
      % (caught, EXPECTED_RED, passed, EXPECTED_CLEAN))
if caught != EXPECTED_RED or passed != EXPECTED_CLEAN:
    print("FAIL — the coverage gate does not do what it claims.")
    sys.exit(1)
print("OK — an unstated or unverifiable coverage is refused; a small one is not.")
