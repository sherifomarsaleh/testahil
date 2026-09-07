"""Negative control for check_terminal_record_shape.  [R-ENF-01]

Reinjects every condition the gate claims to refuse, and the clean cases it must
NOT fire on. EVERY MUTATION ASSERTS THAT IT LANDED before the gate runs — five
negative controls in this repository have been caught passing a fixture that never
injected its condition, so a case that cannot prove it changed anything is evidence
about nothing. The case COUNT is asserted against a declared constant so a later
edit cannot delete a case and leave the file reporting clean.

TWO OF THE RED CASES ARE THE DEFECT EXACTLY AS IT SHIPPED — the three top-level
fields FERTIGLOBE's four records were missing, and the two input fields PHAR's two
were missing, both removed from the real committed records rather than from
something invented to be easy.

THE CLEAN HALF IS THE HALF THAT DECIDES WHETHER THIS GATE IS HONEST. A record
carrying EXTRA keys must stay green, because a study may hold its own context beside
the module's and a gate refusing that would push studies to strip context; and a
study with NO terminal record must stay green, because eleven of twenty-four carry
none and demanding one would be a false claim about what this gate checks.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGET = os.path.join(HERE, "check_terminal_record_shape.py")
SRC_ENGINE = os.path.join(ROOT, "engine")

CASES_EXPECTED = 10          # 7 red + 3 clean
RED_EXPECTED = 7
CLEAN_EXPECTED = 3


def _sandbox():
    """A copy carrying only what the gate reads, built from what actually ships."""
    tmp = tempfile.mkdtemp(prefix="trs-nc-")
    eng = os.path.join(tmp, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    shutil.copy(os.path.join(SRC_ENGINE, "terminal_value.py"), eng)
    rat = os.path.join(SRC_ENGINE, "build_depth_audit",
                       "terminal_record_outstanding.json")
    if os.path.exists(rat):
        shutil.copy(rat, os.path.join(eng, "build_depth_audit"))
    for d in sorted(glob.glob(os.path.join(SRC_ENGINE, "*_study"))):
        dst = os.path.join(eng, os.path.basename(d))
        os.makedirs(dst)
        for f in glob.glob(os.path.join(d, "*numbers*.json")):
            shutil.copy(f, dst)
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(TARGET, os.path.join(tmp, "scripts",
                                     "check_terminal_record_shape.py"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts",
                                     "check_terminal_record_shape.py")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def _numbers(tmp, study):
    c = [p for p in sorted(glob.glob(os.path.join(tmp, "engine", study,
                                                  "*numbers*.json")))
         if "_v1" not in os.path.basename(p)
         and "gap_review" not in os.path.basename(p)]
    assert len(c) == 1, f"fixture: {study} has {len(c)} numbers files"
    return c[0]


def _each_record(node):
    if isinstance(node, dict):
        if node.get("rule") == "R-TERM-01":
            yield node
        for v in node.values():
            yield from _each_record(v)
    elif isinstance(node, list):
        for v in node:
            yield from _each_record(v)


# ---------------------------------------------------------------- red cases

def missing_top_level(tmp):
    """FERTIGLOBE's four records exactly as they stood before 07-09-2026."""
    p = _numbers(tmp, "fertiglobe_study")
    o = json.load(open(p))
    gone = ["maintenance_age_basis", "maintenance_age_years",
            "maintenance_escalator"]
    hit = 0
    for rec in _each_record(o):
        for k in gone:
            if k in rec:
                del rec[k]
                hit += 1
    assert hit == 12, f"MUTATION DID NOT LAND: removed {hit} keys, expected 12"
    json.dump(o, open(p, "w"))
    return "short of the field set"


def missing_input_field(tmp):
    """PHAR's two records exactly as they stood — the inputs half of the same defect."""
    p = _numbers(tmp, "phar_study")
    o = json.load(open(p))
    hit = 0
    for rec in _each_record(o):
        for k in ("average_age_years", "average_age_source"):
            if k in rec.get("inputs", {}):
                del rec["inputs"][k]
                hit += 1
    assert hit == 4, f"MUTATION DID NOT LAND: removed {hit} input fields, expected 4"
    json.dump(o, open(p, "w"))
    return "short of the field set"


def no_records_anywhere(tmp):
    """The record marker moves and every record becomes invisible [R-ENF-04].

    This is the state the gate would silently enter if terminal_value ever renamed
    its rule field: nothing to check, nothing wrong, green — which is exactly the
    absent answer wearing a clean one's clothes.
    """
    hit = 0
    for p in glob.glob(os.path.join(tmp, "engine", "*_study", "*numbers*.json")):
        o = json.load(open(p))
        for rec in _each_record(o):
            rec["rule"] = "R-TERM-01-RENAMED"
            hit += 1
        json.dump(o, open(p, "w"))
    assert hit == 37, f"MUTATION DID NOT LAND: renamed {hit} markers, expected 37"
    return "ZERO terminal records"


def no_study_dirs(tmp):
    """An emptied population [R-ENF-04]."""
    dirs = glob.glob(os.path.join(tmp, "engine", "*_study"))
    assert dirs, "MUTATION DID NOT LAND: no study directories to remove"
    for d in dirs:
        shutil.rmtree(d)
    assert not glob.glob(os.path.join(tmp, "engine", "*_study")), \
        "MUTATION DID NOT LAND: directories survived"
    return "ZERO study directories"


def unparseable_numbers(tmp):
    """A numbers file that will not parse is RED, never skipped [R-ENF-04]."""
    p = _numbers(tmp, "scem_study")
    before = open(p).read()
    open(p, "w").write(before[: len(before) // 2])
    try:
        json.load(open(p))
        raise AssertionError("MUTATION DID NOT LAND: the file still parses")
    except ValueError:
        pass
    return "will not parse"


def phantom_ratchet(tmp):
    """A ratchet naming a study that does not exist is anchored on nothing."""
    p = os.path.join(tmp, "engine", "build_depth_audit",
                     "terminal_record_outstanding.json")
    o = json.load(open(p)) if os.path.exists(p) else {"outstanding": []}
    o["outstanding"] = ["NOSUCHNAME"]
    json.dump(o, open(p, "w"))
    assert json.load(open(p))["outstanding"] == ["NOSUCHNAME"], "MUTATION DID NOT LAND"
    return "anchored on nothing"


def build_refuses(tmp):
    """The gate cannot learn the standard and must say so rather than pass.

    A gate whose reference shape comes back empty has checked nothing, and an empty
    reference makes EVERY record conform by construction — the failure that would
    read most convincingly as a clean run.
    """
    p = os.path.join(tmp, "engine", "terminal_value.py")
    src = open(p).read()
    old = "def build("
    assert old in src, "MUTATION DID NOT LAND: build() not found"
    src = src.replace(old, "def build(*_a, **_k):\n    raise RuntimeError('fixture')\n\n\ndef _shadowed_build(", 1)
    open(p, "w").write(src)
    return "could not learn the standard"


# -------------------------------------------------------------- clean cases

def as_it_stands(tmp):
    """The repository unmutated. If this is not green nothing below means anything."""
    return None


def extra_keys(tmp):
    """A record carrying MORE than the module emits. Extra context is not a defect."""
    p = _numbers(tmp, "arcc_study")
    o = json.load(open(p))
    hit = 0
    for rec in _each_record(o):
        rec["study_local_context"] = "a note this study keeps beside the module's record"
        hit += 1
    assert hit >= 1, "MUTATION DID NOT LAND: no record to extend"
    json.dump(o, open(p, "w"))
    return None


def study_without_record(tmp):
    """A study directory whose numbers carry no terminal record at all.

    Eleven of twenty-four are in this state and every one of them is legitimate.
    """
    d = os.path.join(tmp, "engine", "newname_study")
    os.makedirs(d)
    json.dump({"meta": {"ticker": "NEWNAME"}, "dcf": {"central": 1.0}},
              open(os.path.join(d, "study_numbers.json"), "w"))
    assert os.path.exists(os.path.join(d, "study_numbers.json")), "MUTATION DID NOT LAND"
    return None


RED = [
    ("missing top-level fields (FERTIGLOBE as it stood)", missing_top_level),
    ("missing input fields (PHAR as it stood)", missing_input_field),
    ("the record marker moves — zero records read", no_records_anywhere),
    ("an emptied population", no_study_dirs),
    ("a numbers file that will not parse", unparseable_numbers),
    ("a ratchet naming a study not on disk", phantom_ratchet),
    ("build() refuses — the standard cannot be learned", build_refuses),
]
CLEAN = [
    ("the repository as it stands", as_it_stands),
    ("a record carrying EXTRA keys", extra_keys),
    ("a study with no terminal record at all", study_without_record),
]


def main():
    assert len(RED) == RED_EXPECTED, "a red case was deleted"
    assert len(CLEAN) == CLEAN_EXPECTED, "a clean case was deleted"
    assert len(RED) + len(CLEAN) == CASES_EXPECTED, "the case count moved"

    print("NEGATIVE CONTROL — check_terminal_record_shape  [R-ENF-01]")
    print("   %d conditions: %d that must go RED, %d that must stay GREEN"
          % (CASES_EXPECTED, RED_EXPECTED, CLEAN_EXPECTED))
    bad = []

    for name, fn in RED:
        tmp = _sandbox()
        try:
            want = fn(tmp)
            rc, out = _run(tmp)
            ok = rc != 0 and (want is None or want in out)
            print("   %-52s %s" % (name, "RED" if ok else "*** STAYED GREEN ***"))
            if not ok:
                bad.append("%s: rc=%d, expected %r in output" % (name, rc, want))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    for name, fn in CLEAN:
        tmp = _sandbox()
        try:
            fn(tmp)
            rc, out = _run(tmp)
            print("   %-52s %s" % (name, "green" if rc == 0 else "*** WENT RED ***"))
            if rc != 0:
                bad.append("%s: went red\n%s" % (name, out[-900:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    if bad:
        print("\nFAIL")
        for b in bad:
            print("  - " + b)
        return 1
    print("\nOK — %d of %d conditions behaved as the gate claims." % (CASES_EXPECTED,
                                                                     CASES_EXPECTED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
