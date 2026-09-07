"""Negative control for check_correction_boundary.  [R-ENF-01]

Every mutation ASSERTS THAT IT LANDED before the gate runs, and the case count is
asserted against a declared constant — four negative controls in this repository
have been caught passing a fixture that never injected its condition.

THE CLEAN HALF IS THE ONE THAT MATTERS. This gate must not fire on a driver too
thin to cut, on a run that adopts nothing, or on a correction whose sign genuinely
survives — a check that did would push a run to stop declaring its corrections,
which is the opposite of what it is for.
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
TARGET = os.path.join(HERE, "check_correction_boundary.py")

spec = importlib.util.spec_from_file_location("ccb", TARGET)
ccb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ccb)


def _sandbox():
    tmp = tempfile.mkdtemp(prefix="cb-nc-")
    eng = os.path.join(tmp, "engine")
    os.makedirs(os.path.join(eng, "valuation_calibration"))
    shutil.copy(os.path.join(ROOT, "engine", "valuation_calibration",
                             "boundary_sensitivity.py"),
                os.path.join(eng, "valuation_calibration"))
    for _n, d, _a in ccb.RUNS:
        src = os.path.join(ROOT, "engine", d)
        if not os.path.isdir(src):
            continue
        os.makedirs(os.path.join(eng, d))
        for f in ("corrections_log.json", "error_cells.json"):
            p = os.path.join(src, f)
            if os.path.exists(p):
                shutil.copy(p, os.path.join(eng, d, f))
    os.makedirs(os.path.join(tmp, "scripts"))
    shutil.copy(TARGET, os.path.join(tmp, "scripts", "check_correction_boundary.py"))
    return tmp


def _run(tmp):
    r = subprocess.run([sys.executable,
                        os.path.join(tmp, "scripts", "check_correction_boundary.py")],
                       capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def _log(tmp, d):
    return os.path.join(tmp, "engine", d, "corrections_log.json")


def _bs(tmp):
    import importlib.util as iu
    s = iu.spec_from_file_location(
        "bs", os.path.join(tmp, "engine", "valuation_calibration",
                           "boundary_sensitivity.py"))
    m = iu.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _arcc_candidate(tmp, want):
    """A real ARCC candidate whose sign FLIPS ("flip") or SURVIVES ("stable").

    Chosen from the data rather than hardcoded: a fixture naming a driver by hand
    breaks silently the day the panel moves, and a control that cannot build its
    own condition proves nothing. The first draft named `cogs`, which is not a
    candidate at all, and the landing assertion said so.
    """
    bs = _bs(tmp)
    cells = bs.load("ARCC")
    o = json.load(open(_log(tmp, "arcc_walkforward")))
    for c in o["candidates"]:
        got = cells.get(c["driver"])
        if not got:
            continue
        cuts, flipped = bs.cuts_for(got)
        if not cuts:
            continue
        if (want == "flip") == bool(flipped):
            return c["driver"]
    raise AssertionError("NO FIXTURE AVAILABLE: no ARCC candidate is %s" % want)


def adopt_a_flipper(tmp):
    """ARCC adopts a driver whose sign flips — the condition the gate exists for."""
    drv = _arcc_candidate(tmp, "flip")
    p = _log(tmp, "arcc_walkforward")
    o = json.load(open(p))
    for c in o["candidates"]:
        if c["driver"] == drv:
            c["disposition"] = "ADOPTED"
    json.dump(o, open(p, "w"))
    assert any(c.get("disposition") == "ADOPTED" and c["driver"] == drv
               for c in json.load(open(p))["candidates"]), "MUTATION DID NOT LAND"
    return drv


def adopt_a_phantom(tmp):
    """A driver adopted that appears in no cell: untestable, never clean."""
    p = _log(tmp, "arcc_walkforward")
    o = json.load(open(p))
    o["candidates"].append({"driver": "a_driver_in_no_cell", "disposition": "ADOPTED"})
    json.dump(o, open(p, "w"))
    assert any(c["driver"] == "a_driver_in_no_cell"
               for c in json.load(open(p))["candidates"]), "MUTATION DID NOT LAND"
    return "absent from the per-cell file"


def stale_ratchet(tmp):
    """A listed entry that stops flipping must go RED, not quietly pass."""
    p = _log(tmp, "phdc_walkforward")
    o = json.load(open(p))
    removed = 0
    for e in o["log"]:
        for drv, v in (e.get("corrections") or {}).items():
            if drv == "asp" and v.get("applied"):
                v["applied"] = 0.0
                removed += 1
    assert removed, "MUTATION DID NOT LAND: asp carried no applied correction"
    json.dump(o, open(p, "w"))
    return "may only SHORTEN"


def no_record(tmp):
    """A run with no corrections record is REPORTED, never skipped."""
    p = _log(tmp, "tmgh_walkforward")
    assert os.path.exists(p), "MUTATION DID NOT LAND: no record to remove"
    os.unlink(p)
    return "no corrections record"


def empty_population(tmp):
    n = 0
    for _x, d, _a in ccb.RUNS:
        p = os.path.join(tmp, "engine", d)
        if os.path.isdir(p):
            shutil.rmtree(p)
            n += 1
    assert n, "MUTATION DID NOT LAND: nothing to remove"
    return "REFUSED"


RED = [
    ("a correction adopted on a sign that flips", adopt_a_flipper),
    ("a correction adopted on a driver in no cell", adopt_a_phantom),
    ("a ratchet entry that stopped flipping", stale_ratchet),
    ("a run with no corrections record", no_record),
    ("an emptied population", empty_population),
]


def clean_untouched(tmp):
    return None


def clean_adopt_a_survivor(tmp):
    """Adopting a driver whose sign genuinely survives must stay GREEN."""
    drv = _arcc_candidate(tmp, "stable")
    p = _log(tmp, "arcc_walkforward")
    o = json.load(open(p))
    for c in o["candidates"]:
        if c["driver"] == drv:
            c["disposition"] = "ADOPTED"
    json.dump(o, open(p, "w"))
    return None


def clean_adopt_a_thin_driver(tmp):
    """A driver too thin to cut is untestable, and untestable is not a failure.

    THE CONDITION IS CREATED RATHER THAN FOUND, because no ARCC driver is currently
    thin enough and the only run that has thin drivers adopts nothing — so a fixture
    hunting for one would report "no case available" and prove nothing. Cells are
    removed from a real candidate until no boundary leaves MIN_SIDE either side,
    and the fixture asserts that it actually reached that state.
    """
    drv = _arcc_candidate(tmp, "stable")
    cp = os.path.join(tmp, "engine", "arcc_walkforward", "error_cells.json")
    cells = json.load(open(cp))
    dropped = 0
    # Blank every cell of this driver outside a single year, so only one year has
    # any error at all and no cut can leave MIN_SIDE cells on both sides.
    years = sorted({r.get("year") for r in cells
                    if r.get("setting") == "asknown" and r.get("driver") == drv
                    and r.get("log_error") is not None})
    assert years, "MUTATION DID NOT LAND: driver has no scored cells"
    survivor = years[0]
    for r in cells:
        if (r.get("setting") == "asknown" and r.get("driver") == drv
                and r.get("year") != survivor):
            r["log_error"] = None
            r["dropped"] = "non_positive"
            dropped += 1
    assert dropped, "MUTATION DID NOT LAND: nothing blanked"
    json.dump(cells, open(cp, "w"))
    bs = _bs(tmp)
    cuts, _ = bs.cuts_for(bs.load("ARCC")[drv])
    assert not cuts, ("MUTATION DID NOT LAND: driver still admits %d cut(s)"
                      % len(cuts))
    p = _log(tmp, "arcc_walkforward")
    o = json.load(open(p))
    for c in o["candidates"]:
        if c["driver"] == drv:
            c["disposition"] = "ADOPTED"
    json.dump(o, open(p, "w"))
    return None


CLEAN = [
    ("the records exactly as they ship", clean_untouched),
    ("adopting a driver whose sign survives every cut", clean_adopt_a_survivor),
    ("adopting a driver too thin to cut", clean_adopt_a_thin_driver),
]

EXPECTED_RED, EXPECTED_CLEAN = 5, 3
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
    print("FAIL — the boundary gate does not do what it claims.")
    sys.exit(1)
print("OK — a correction adopted on an unstable sign is refused; a stable or "
      "untestable one is not.")
