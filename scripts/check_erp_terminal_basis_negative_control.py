#!/usr/bin/env python3
"""Negative control for the erp_terminal basis requirement [R-MACRO-01].

Every level in a house macro path is published by a named institution on a named
date, or DERIVED by an identity from numbers that are. The inflation ladder has
carried a per-step `basis` since the rule was adopted and NOTHING ASKED THE SAME OF
THE TERMINAL EQUITY RISK PREMIUM -- measured 18-09-2026, five of seven paths cite
Damodaran's country risk file with its publication date, AE states a held-flat
convention with its reason, and Egypt's cites a rationale that names no institution,
no date and no identity while reading on the page exactly like the five that do.

IT WRITES NOTHING INTO THE TREE [R-ENF-01 EXTENDED 07-09-2026]. Every fixture is a
dict built in memory and handed straight to _validate(); the real path files are read
once, for the clean cases, and never opened for writing.

EVERY MUTATION ASSERTS THAT IT LANDED, and the clean half is the half that matters:
a control proving only that a rationale fails would not show that the six paths which
were already right stay right.
"""
from __future__ import annotations

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))

import macro_path as MP   # noqa: E402

CASES = 12
PATHS = os.path.join(ROOT, "engine", "macro_paths")


def _raw(m):
    with open(os.path.join(PATHS, "%s.json" % m), encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ok, bad = 0, []

    def case(n, what, want_red, d, landed):
        nonlocal ok
        if not landed(d):
            bad.append("%d %s — THE FIXTURE DID NOT LAND" % (n, what))
            return
        try:
            MP._validate(d, "FIXTURE")
            red = False
            msg = ""
        except MP.MacroPathError as exc:
            red, msg = True, str(exc)
        except Exception as exc:                       # noqa: BLE001
            bad.append("%d %s — raised %s, not MacroPathError: %s"
                       % (n, what, type(exc).__name__, str(exc)[:70]))
            return
        # a red for some OTHER reason is not this check firing
        if red and want_red and "erp_terminal" not in msg:
            bad.append("%d %s — red, but on %r rather than on erp_terminal"
                       % (n, what, msg[:60]))
            return
        if red == want_red:
            ok += 1
        else:
            bad.append("%d %s — wanted %s, got %s%s"
                       % (n, what, "RED" if want_red else "clean",
                          "RED" if red else "clean",
                          (": " + msg[:80]) if red else ""))

    eg = _raw("EG")
    if not eg.get("erp_terminal", {}).get("basis"):
        print("FAILED — the live EG path carries no erp_terminal basis, so the "
              "clean cases would prove nothing [R-ENF-04]")
        return 1

    def mut(market, **kw):
        d = copy.deepcopy(_raw(market))
        d["erp_terminal"].update(kw)
        for k, v in list(kw.items()):
            if v is None:
                d["erp_terminal"].pop(k, None)
        return d

    has = lambda k, v: (lambda d: d["erp_terminal"].get(k) == v)          # noqa: E731
    lacks = lambda k: (lambda d: k not in d["erp_terminal"])              # noqa: E731

    # ---- RED: the shapes that must not pass
    case(1, "EG's rationale exactly as it shipped, with no basis at all", True,
         mut("EG", basis=None), lacks("basis"))
    case(2, "a basis invented outside the closed list ('normalised')", True,
         mut("EG", basis="normalised"), has("basis", "normalised"))
    case(3, "'sourced', which sounds like one and is not", True,
         mut("EG", basis="sourced"), has("basis", "sourced"))
    case(4, "an empty basis string", True,
         mut("EG", basis=""), has("basis", ""))
    case(5, "a house judgement that does not say what would source it", True,
         mut("EG", basis="house_judgement", what_would_source_it=None),
         lambda d: d["erp_terminal"]["basis"] == "house_judgement"
         and "what_would_source_it" not in d["erp_terminal"])
    case(6, "a house judgement whose route to evidence is EMPTY — declared off "
            "rather than declared", True,
         mut("EG", basis="house_judgement", what_would_source_it=""),
         has("what_would_source_it", ""))
    case(7, "a PUBLISHED path stripped of its basis (US)", True,
         mut("US", basis=None), lacks("basis"))
    case(8, "basis carried as a number rather than a name", True,
         mut("EG", basis=1), has("basis", 1))

    # ---- CLEAN: everything the book actually ships, which must stay green
    case(9, "EG exactly as it now stands — a declared house judgement", False,
         copy.deepcopy(eg),
         lambda d: d["erp_terminal"]["basis"] == "house_judgement"
         and bool(d["erp_terminal"].get("what_would_source_it")))
    case(10, "US exactly as it stands — published, Damodaran with its date", False,
         copy.deepcopy(_raw("US")), has("basis", "published"))
    case(11, "AE exactly as it stands — a held-flat convention, published basis", False,
         copy.deepcopy(_raw("AE")), has("basis", "published"))
    case(12, "a DERIVED basis, the third member of the closed list", False,
         mut("SA", basis="derived"), has("basis", "derived"))

    print("erp_terminal basis negative control — %s %d/%d"
          % ("PASS" if not bad else "FAILED", ok, CASES))
    for b in bad:
        print("  - " + b)
    if ok + len(bad) != CASES:
        print("  - CASE COUNT: %d ran against a declared %d" % (ok + len(bad), CASES))
        return 1
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
