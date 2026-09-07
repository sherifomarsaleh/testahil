"""Negative control for check_four_field.  [R-ENF-01]

Reinjects every condition the gate claims to refuse, and the clean cases it must NOT
fire on. EVERY MUTATION ASSERTS THAT IT LANDED before the gate runs, and the case COUNT
is asserted against a declared constant.

THE CLEAN HALF IS WHAT THIS GATE TURNS ON. The fourth field is spelled `layer` in five
studies and `ring` in thirteen, and BOTH must stay green: a control testing only one
spelling would prove the gate works on a third of the book and say nothing about the
rest — which is precisely the reading that made the author's own first measurement
report 58% of inputs missing a field that was there all along.

The absent-register case is here TWICE on purpose, once deferred and once not, because
the whole design decision is that this gate defers to `source_outstanding.json` instead
of opening a second list. A fixture proving only the deferral would leave the refusal
untested, and a gate that never refuses an absent register is a gate that lets a new
study skip the standard entirely.
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
TARGET = os.path.join(HERE, "check_four_field.py")
SRC_ENGINE = os.path.join(ROOT, "engine")

CASES_EXPECTED = 12
RED_EXPECTED = 7
CLEAN_EXPECTED = 5


def _sandbox():
    """Only what the gate reads, copied from what actually ships."""
    tmp = tempfile.mkdtemp(prefix="4f-nc-")
    eng = os.path.join(tmp, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    src = os.path.join(SRC_ENGINE, "build_depth_audit", "source_outstanding.json")
    if os.path.exists(src):
        shutil.copy(src, os.path.join(eng, "build_depth_audit"))
    for d in sorted(glob.glob(os.path.join(SRC_ENGINE, "*_study"))):
        dst = os.path.join(eng, os.path.basename(d))
        os.makedirs(dst)
        for f in glob.glob(os.path.join(d, "*numbers*.json")):
            shutil.copy(f, dst)
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(TARGET, os.path.join(tmp, "scripts", "check_four_field.py"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_four_field.py")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def _nums(tmp, study):
    c = [p for p in sorted(glob.glob(os.path.join(tmp, "engine", study,
                                                  "*numbers*.json")))
         if "_v1" not in os.path.basename(p)
         and "gap_review" not in os.path.basename(p)]
    assert len(c) == 1, f"fixture: {study} has {len(c)} numbers files"
    return c[0]


def _an_input(doc):
    for k, v in (doc.get("inputs") or {}).items():
        if isinstance(v, dict) and "value" in v:
            return k, v
    raise AssertionError("fixture: no input carrying a value")


def _deferred(tmp):
    p = os.path.join(tmp, "engine", "build_depth_audit", "source_outstanding.json")
    return p, (json.load(open(p)) if os.path.exists(p) else {"unreadable": []})


# ------------------------------------------------------------------ red cases

def drop_source(tmp):
    p = _nums(tmp, "arcc_study")
    o = json.load(open(p))
    k, v = _an_input(o)
    assert str(v.get("source") or "").strip(), "MUTATION DID NOT LAND: no source to drop"
    v["source"] = ""
    json.dump(o, open(p, "w"))
    return "four-field complete"


def drop_date(tmp):
    p = _nums(tmp, "adnocls_study")
    o = json.load(open(p))
    k, v = _an_input(o)
    assert str(v.get("date") or "").strip(), "MUTATION DID NOT LAND: no date to drop"
    del v["date"]
    json.dump(o, open(p, "w"))
    return "four-field complete"


def drop_fourth_ring(tmp):
    """A `ring`-spelled register losing its fourth field."""
    p = _nums(tmp, "arcc_study")
    o = json.load(open(p))
    k, v = _an_input(o)
    assert "ring" in v, "MUTATION DID NOT LAND: this register is not ring-spelled"
    del v["ring"]
    assert not any(f in v for f in ("layer", "ring")), "MUTATION DID NOT LAND"
    json.dump(o, open(p, "w"))
    return "four-field complete"


def drop_fourth_layer(tmp):
    """The SAME defect in the OTHER spelling — a gate blind to one is blind to a third
    of the book."""
    p = _nums(tmp, "adnocls_study")
    o = json.load(open(p))
    k, v = _an_input(o)
    assert "layer" in v, "MUTATION DID NOT LAND: this register is not layer-spelled"
    del v["layer"]
    json.dump(o, open(p, "w"))
    return "four-field complete"


def register_absent_not_deferred(tmp):
    """A study with no register that no other list excuses."""
    p = _nums(tmp, "arcc_study")
    o = json.load(open(p))
    assert (o.get("inputs") or {}), "MUTATION DID NOT LAND: there was no register"
    o["inputs"] = {}
    json.dump(o, open(p, "w"))
    dp, dd = _deferred(tmp)
    assert "ARCC" not in dd.get("unreadable", []), "fixture: ARCC is already deferred"
    return "no inputs register"


def unparseable(tmp):
    p = _nums(tmp, "scem_study")
    before = open(p).read()
    open(p, "w").write(before[: len(before) // 3])
    try:
        json.load(open(p))
        raise AssertionError("MUTATION DID NOT LAND: it still parses")
    except ValueError:
        pass
    return "will not parse"


def emptied_population(tmp):
    dirs = glob.glob(os.path.join(tmp, "engine", "*_study"))
    assert dirs, "MUTATION DID NOT LAND: nothing to remove"
    for d in dirs:
        shutil.rmtree(d)
    return "ZERO study directories"


# ---------------------------------------------------------------- clean cases

def as_it_stands(tmp):
    return None


def ring_spelling_intact(tmp):
    """Thirteen studies spell it `ring`; that must not read as a missing field."""
    p = _nums(tmp, "arcc_study")
    o = json.load(open(p))
    k, v = _an_input(o)
    assert "ring" in v and "layer" not in v, "fixture: not a ring-only register"
    return None


def layer_spelling_intact(tmp):
    p = _nums(tmp, "adnocls_study")
    o = json.load(open(p))
    k, v = _an_input(o)
    assert "layer" in v and "ring" not in v, "fixture: not a layer-only register"
    return None


def absent_register_deferred(tmp):
    """A study with no register that source_outstanding ALREADY records as unreadable."""
    dp, dd = _deferred(tmp)
    tks = [t for t in dd.get("unreadable", [])
           if os.path.isdir(os.path.join(tmp, "engine", t.lower() + "_study"))]
    assert tks, "fixture: the deferred list names no study present in the sandbox"
    p = _nums(tmp, tks[0].lower() + "_study")
    assert not (json.load(open(p)).get("inputs") or {}), \
        "fixture: the deferred study unexpectedly carries a register"
    return None


def a_block_is_not_an_input(tmp):
    """A dict with no `value` is a record, not an input, and owes no four fields."""
    p = _nums(tmp, "arcc_study")
    o = json.load(open(p))
    o.setdefault("inputs", {})["a_note_block"] = {"basis": "prose", "why": "context"}
    json.dump(o, open(p, "w"))
    assert "a_note_block" in json.load(open(p))["inputs"], "MUTATION DID NOT LAND"
    return None


RED = [
    ("an input with no source", drop_source),
    ("an input with no date", drop_date),
    ("the fourth field dropped from a ring register", drop_fourth_ring),
    ("the fourth field dropped from a layer register", drop_fourth_layer),
    ("an absent register no other list excuses", register_absent_not_deferred),
    ("a numbers file that will not parse", unparseable),
    ("an emptied population", emptied_population),
]
CLEAN = [
    ("the repository as it stands", as_it_stands),
    ("a ring-spelled register", ring_spelling_intact),
    ("a layer-spelled register", layer_spelling_intact),
    ("an absent register already deferred elsewhere", absent_register_deferred),
    ("a block carrying no value is not an input", a_block_is_not_an_input),
]


def main():
    assert len(RED) == RED_EXPECTED, "a red case was deleted"
    assert len(CLEAN) == CLEAN_EXPECTED, "a clean case was deleted"
    assert len(RED) + len(CLEAN) == CASES_EXPECTED, "the case count moved"

    print("NEGATIVE CONTROL — check_four_field  [R-ENF-01]")
    print("   %d conditions: %d that must go RED, %d that must stay GREEN"
          % (CASES_EXPECTED, RED_EXPECTED, CLEAN_EXPECTED))
    bad = []
    for name, fn in RED:
        tmp = _sandbox()
        try:
            want = fn(tmp)
            rc, out = _run(tmp)
            ok = rc != 0 and (want is None or want in out)
            print("   %-50s %s" % (name, "RED" if ok else "*** STAYED GREEN ***"))
            if not ok:
                bad.append("%s: rc=%d, expected %r\n%s" % (name, rc, want, out[-400:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    for name, fn in CLEAN:
        tmp = _sandbox()
        try:
            fn(tmp)
            rc, out = _run(tmp)
            print("   %-50s %s" % (name, "green" if rc == 0 else "*** WENT RED ***"))
            if rc != 0:
                bad.append("%s: went red\n%s" % (name, out[-500:]))
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
