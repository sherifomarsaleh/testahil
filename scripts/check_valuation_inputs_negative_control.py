#!/usr/bin/env python3
"""Negative control for check_valuation_inputs.py.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. Each case below builds a temporary
engine tree, injects one defect the amendment forbids, and asserts the checker
goes RED; the clean cases assert it stays GREEN, because a gate that fires on
correct work is the permanently-red check [R-ENF-02] forbids.

The defects are not invented. Every one is a shape the five pre-amendment runs
could have shipped, and two of them — an item simply absent from the block, and a
share count carried without the par value it foots against — are exactly what the
census found in the repository on the day the rule was written.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_valuation_inputs as G  # noqa: E402


def full_block():
    def v(x, src="FS2021 p.31", route="text layer"):
        return {"value": x, "source": src, "route": route}
    b = {i: v(1.0) for i in ("cash", "debt", "ppe", "dep", "wc")}
    b["capex"] = dict(v(2.0), derived=True, identity="capex = dPPE + D&A")
    b["shares"] = dict(v(2063562286.0), issued_capital=20635622860.0, par_value=10.0)
    return {"origins": {"2021": b, "2022": json.loads(json.dumps(b))}}


def tree(record=None, ratchet=None, names=("TMGH",)):
    d = tempfile.mkdtemp()
    eng = os.path.join(d, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    for n in names:
        rd = os.path.join(eng, "%s_walkforward" % n.lower())
        os.makedirs(rd)
        if record is not None:
            json.dump(record, open(os.path.join(rd, G.RECORD), "w",
                                   encoding="utf-8"), indent=1)
    json.dump({"runs": ratchet or {}},
              open(os.path.join(eng, "build_depth_audit",
                                "valuation_inputs_outstanding.json"),
                   "w", encoding="utf-8"), indent=1)
    return d, eng


def run(eng):
    old = G.OUTSTANDING
    G.OUTSTANDING = os.path.join(eng, "build_depth_audit",
                                 "valuation_inputs_outstanding.json")
    try:
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = G.main(["--engine=%s" % eng])
        return rc, buf.getvalue()
    finally:
        G.OUTSTANDING = old


CASES = []


def case(name, expect_red, build):
    CASES.append((name, expect_red, build))


# ---- defects, each of which must go RED ------------------------------------
def _no_record():
    return tree(record=None)                      # not on the ratchet
case("a new run with no valuation-input block at all", True, _no_record)


def _unparseable():
    d, eng = tree(record=full_block())
    p = os.path.join(eng, "tmgh_walkforward", G.RECORD)
    open(p, "w").write("{ not json")
    return d, eng
case("a record that will not parse", True, _unparseable)


def _no_origins():
    return tree(record={"origins": {}})
case("a record naming no origins", True, _no_origins)


def _item_omitted():
    r = full_block()
    del r["origins"]["2022"]["cash"]
    return tree(record=r)
case("an item simply absent from one origin's block", True, _item_omitted)


def _missing_without_reason():
    r = full_block()
    r["origins"]["2022"]["wc"] = {"missing": "   "}
    return tree(record=r)
case("an item marked missing with no reason given", True, _missing_without_reason)


def _no_source():
    r = full_block()
    r["origins"]["2021"]["debt"] = {"value": 5.0, "route": "text layer"}
    return tree(record=r)
case("a value carried with no source", True, _no_source)


def _no_route():
    r = full_block()
    r["origins"]["2021"]["ppe"] = {"value": 5.0, "source": "FS2021"}
    return tree(record=r)
case("a value carried with no route", True, _no_route)


def _shares_no_par():
    r = full_block()
    r["origins"]["2021"]["shares"] = {"value": 2063562286.0, "source": "FS2021",
                                      "route": "text layer"}
    return tree(record=r)
case("a share count with no par value to foot against", True, _shares_no_par)


def _shares_do_not_foot():
    r = full_block()
    r["origins"]["2021"]["shares"] = {"value": 2063562286.0, "source": "FS2021",
                                      "route": "text layer",
                                      "issued_capital": 20635622860.0,
                                      "par_value": 5.0}
    return tree(record=r)
case("a share count that does not foot against its own capital and par",
     True, _shares_do_not_foot)


def _derived_capex_unnamed():
    r = full_block()
    r["origins"]["2021"]["capex"] = {"value": 2.0, "source": "FS2021",
                                     "route": "text layer", "derived": True}
    return tree(record=r)
case("a derived capex that does not name the identity", True, _derived_capex_unnamed)


def _waived_but_malformed():
    r = full_block()
    del r["origins"]["2021"]["dep"]
    return tree(record=r, ratchet={"TMGH": "predates"})
case("a run ON the ratchet whose record exists and is malformed", True,
     _waived_but_malformed)


def _stale_ratchet():
    return tree(record=full_block(), ratchet={"GHOST": "not on disk"})
case("a ratchet naming a run that does not resolve on disk", True, _stale_ratchet)


def _empty_population():
    d, eng = tree(record=full_block(), names=())
    return d, eng
case("a population of zero runs — an empty result is not a clean result", True,
     _empty_population)


# ---- clean cases, each of which must stay GREEN -----------------------------
case("a complete block on every origin", False, lambda: tree(record=full_block()))


def _legit_missing():
    r = full_block()
    r["origins"]["2022"]["capex"] = {
        "missing": "the cash-flow statement for this year was not filed in English "
                   "and PPE is disclosed net only, so the identity cannot be run"}
    return tree(record=r)
case("an item legitimately missing, recorded with its reason", False, _legit_missing)


def _waived_no_record():
    return tree(record=None, ratchet={"TMGH": "predates the amendment"})
case("a pre-amendment run with no record, listed on the ratchet", False,
     _waived_no_record)


def _capex_not_derived():
    r = full_block()
    r["origins"]["2021"]["capex"] = {"value": 2.0, "source": "FS2021 cash flow",
                                     "route": "text layer", "derived": False}
    return tree(record=r)
case("a capex read straight off the cash-flow statement, not derived", False,
     _capex_not_derived)


def main():
    caught = passed = 0
    red = sum(1 for _, e, _ in CASES if e)
    green = len(CASES) - red
    for name, expect_red, build in CASES:
        d, eng = build()
        try:
            rc, out = run(eng)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        got_red = rc != 0
        ok = got_red == expect_red
        if ok:
            caught += 1 if expect_red else 0
            passed += 0 if expect_red else 1
        print("  %-6s %s" % ("CAUGHT" if (ok and expect_red) else
                             "PASSED" if ok else "MISSED", name))
        if not ok:
            print(out)
    print("\ndefects caught %d/%d | clean cases passed %d/%d"
          % (caught, red, passed, green))
    return 0 if (caught == red and passed == green) else 1


if __name__ == "__main__":
    raise SystemExit(main())
