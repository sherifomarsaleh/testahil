#!/usr/bin/env python3
"""Negative control for [R-ASSET-01] — a check nobody has seen fail is not evidence.

EVERY MUTATION ASSERTS THAT IT LANDED before the gate is asked about it. This project has
four times caught a negative control passing a fixture that never injected its condition,
reporting green and proving only that nothing had changed; so each case here states the
condition it injects and verifies the injection is present.

THE CASE COUNT IS ASSERTED AGAINST A DECLARED CONSTANT, because a later edit that deletes
cases would otherwise report fewer-of-fewer and read as clean.

IT NEVER WRITES INTO THE REAL TREE [R-ENF-01, adopted on a committed loss]: the unit cases
call the module directly with fixtures held in memory, and the gate-level cases build a
throwaway directory. Nothing points at engine/ for writing, so there is no undo to fail to
run.

THE CLEAN HALF IS THE HALF THAT MATTERS HERE. A gate that refused every asset-based study
would look strict and be useless: the equality edge must pass, a genuine
not-restated declaration must pass, a class the registry knows but that is NOT asset-based
must stay out of scope entirely, and TMGH's em-dash class must RESOLVE rather than being
reported unresolvable — that last one is the whole reason the normalisation exists.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")
for p in (ENGINE, ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

import asset_base as ab                      # noqa: E402
import research_protocol as rp               # noqa: E402

DECLARED_CASES = 15

OK = "\033[0m"
def red(s):  return s
def line(tag, name, detail=""):
    print("  %-6s %-46s %s" % (tag, name, detail))


# --------------------------------------------------------------- fixtures

def rec(**kw):
    base = {"quantity": "land bank", "unit": "mn sqm", "value": 33.0,
            "as_at": "2026-03-31", "disclosure": "1Q2026 interim statements"}
    base.update(kw)
    for k, v in list(base.items()):
        if v is None:
            base.pop(k)
    return base


CASES = []

def case(name, kind, build, expect_fail, injected):
    """kind: 'unit' (module) or 'gate' (subprocess). injected: assertion the fixture landed."""
    CASES.append((name, kind, build, expect_fail, injected))


# ---- RED, unit level ----------------------------------------------------

case("PHDC's defect exactly as it stands", "unit",
     lambda: (rec(as_at="2024-12-31",
                  disclosure="PHD FY2024 earnings release"), "1Q2026"),
     True,
     lambda f: f[0]["as_at"] == "2024-12-31" and f[1] == "1Q2026")

case("as_at missing", "unit",
     lambda: (rec(as_at=None), "1Q2026"), True,
     lambda f: "as_at" not in f[0])

case("disclosure missing", "unit",
     lambda: (rec(disclosure=None), "1Q2026"), True,
     lambda f: "disclosure" not in f[0])

case("unit missing", "unit",
     lambda: (rec(unit=None), "1Q2026"), True,
     lambda f: "unit" not in f[0])

case("no record at all", "unit",
     lambda: (None, "1Q2026"), True,
     lambda f: f[0] is None)

case("stale, released with an EMPTY reason", "unit",
     lambda: (rec(as_at="2024-12-31",
                  not_restated_since={"reason": "   ",
                                      "disclosures_checked": ["1Q2026"]}), "1Q2026"),
     True,
     lambda f: not f[0]["not_restated_since"]["reason"].strip())

case("stale, released naming NO disclosure checked", "unit",
     lambda: (rec(as_at="2024-12-31",
                  not_restated_since={"reason": "the company does not restate it quarterly",
                                      "disclosures_checked": []}), "1Q2026"),
     True,
     lambda f: f[0]["not_restated_since"]["disclosures_checked"] == [])

case("an unparseable as_at", "unit",
     lambda: (rec(as_at="sometime in 2024"), "1Q2026"), True,
     lambda f: f[0]["as_at"] == "sometime in 2024")

case("an unparseable information set", "unit",
     lambda: (rec(), "recently"), True,
     lambda f: f[1] == "recently")

# ---- CLEAN, unit level --------------------------------------------------

case("as_at EQUALS the information set end", "unit",
     lambda: (rec(as_at="2026-03-31"), "1Q2026"), False,
     lambda f: ab.period_end(f[0]["as_at"]) == ab.period_end(f[1]))

case("as_at LATER than the information set end", "unit",
     lambda: (rec(as_at="2026-06-30"), "1Q2026"), False,
     lambda f: ab.period_end(f[0]["as_at"]) > ab.period_end(f[1]))

case("stale, released COMPLETELY", "unit",
     lambda: (rec(as_at="2024-12-31",
                  not_restated_since={
                      "reason": "the land bank is disclosed annually; the FY2025 release "
                                "and the 1Q2026 interim both restate the balance sheet "
                                "and neither restates the area",
                      "disclosures_checked": ["FY2025 earnings release",
                                              "1Q2026 interim statements"]}), "1Q2026"),
     False,
     lambda f: bool(f[0]["not_restated_since"]["reason"].strip())
               and len(f[0]["not_restated_since"]["disclosures_checked"]) == 2)


# ---- scope, which is where a silent skip would hide ---------------------

def _scope_check(cls):
    scope = ab.in_scope_classes(rp.LENS_REGISTRY)
    return ab.normalise_class(cls) in scope

case("TMGH's em-dash class RESOLVES into scope", "scope",
     lambda: "real-estate developer, off-plan — point-in-time on handover",
     False,                       # False == must be IN scope / must not be a miss
     lambda f: "—" in f)

case("a registry class that is NOT asset-based stays OUT of scope", "scope",
     lambda: "bank", True,        # True == must be OUT of scope
     lambda f: f in rp.LENS_REGISTRY)

# ---- gate level ---------------------------------------------------------

case("a ratchet naming a study not on disk", "gate", None, True, None)


# --------------------------------------------------------------- runners

def run_unit(build, expect_fail, injected):
    fixture = build()
    assert injected(fixture), "MUTATION DID NOT LAND"
    record, infoset = fixture
    fails = ab.check(record, infoset)
    return (len(fails) > 0), ("; ".join(fails)[:88] if fails else "no failures")


def run_scope(build, expect_out, injected):
    cls = build()
    assert injected(cls), "MUTATION DID NOT LAND"
    inside = _scope_check(cls)
    # expect_out True  -> must be OUT of scope
    # expect_out False -> must be IN scope
    got_out = not inside
    return got_out, ("out of scope" if got_out else "in scope")


def run_gate_ghost():
    tmp = tempfile.mkdtemp(prefix="assetbase_nc_")
    try:
        repo = os.path.join(tmp, "repo")
        os.makedirs(os.path.join(repo, "scripts"))
        os.makedirs(os.path.join(repo, "engine", "build_depth_audit"))
        shutil.copy(os.path.join(HERE, "check_asset_base.py"),
                    os.path.join(repo, "scripts", "check_asset_base.py"))
        # EVERY module the gate imports, or it crashes on the absence and exits 1 for the
        # WRONG reason — which reads exactly like exiting 1 for the right one. The gauntlet
        # learned this the same way and it cost a case there too.
        for m in ("asset_base.py", "research_protocol.py", "lessons_register.py",
                  "ratchet_shape.py"):
            src = os.path.join(ENGINE, m)
            if os.path.exists(src):
                shutil.copy(src, os.path.join(repo, "engine", m))
        # one real in-scope study so the population is not empty for the WRONG reason
        sd = os.path.join(repo, "engine", "phdc_study")
        os.makedirs(sd)
        json.dump({"meta": {"class": "real-estate developer, off-plan, "
                                     "percentage-of-completion",
                            "information_set_ends": "1Q2026"}},
                  open(os.path.join(sd, "study_numbers.json"), "w"))
        ghost = {"why": "control", "outstanding": {"PHDC": "listed",
                                                   "NOSUCHNAME": "a study that is not here"},
                 "pruned_on": []}
        json.dump(ghost, open(os.path.join(repo, "engine", "build_depth_audit",
                                           "asset_base_outstanding.json"), "w"))
        assert "NOSUCHNAME" in json.load(open(os.path.join(
            repo, "engine", "build_depth_audit",
            "asset_base_outstanding.json")))["outstanding"], "MUTATION DID NOT LAND"
        r = subprocess.run([sys.executable, "scripts/check_asset_base.py"],
                           cwd=repo, capture_output=True, text=True, timeout=300)
        out = (r.stdout or "") + (r.stderr or "")
        named = "NOSUCHNAME" in out
        return (r.returncode != 0 and named), \
               ("exit %d, names the ghost: %s" % (r.returncode, named))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("[R-ASSET-01] negative control — every mutation asserts it landed\n")
    assert len(CASES) == DECLARED_CASES, (
        "case count moved: %d present, %d declared. A control that quietly loses cases "
        "reports fewer-of-fewer and reads as clean." % (len(CASES), DECLARED_CASES))

    bad = 0
    for name, kind, build, expect, injected in CASES:
        try:
            if kind == "unit":
                got, detail = run_unit(build, expect, injected)
            elif kind == "scope":
                got, detail = run_scope(build, expect, injected)
            else:
                got, detail = run_gate_ghost()
        except AssertionError as e:
            print("  FIXTURE  %-46s %s" % (name, e))
            bad += 1
            continue
        ok = (got == expect)
        want = "RED" if expect else "CLEAN"
        line("ok" if ok else "WRONG", "[%s] %s" % (want, name), detail)
        if not ok:
            bad += 1

    print("\n%d case(s): %d red-expected, %d clean-expected"
          % (len(CASES), sum(1 for c in CASES if c[3]), sum(1 for c in CASES if not c[3])))
    if bad:
        print("FAIL — %d case(s) did not behave as declared." % bad)
        return 1
    print("OK — the gate fires on every injected defect and on none of the clean cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
