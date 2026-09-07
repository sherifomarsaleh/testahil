#!/usr/bin/env python3
"""[R-BRIDGE-01] — THE BRIDGE MUST REACH THE ANSWER THE STUDY PUBLISHES.

WHY THIS EXISTS. [R-BRIDGE-01] records the enterprise-to-equity bridge as a set of CHOICES
— which balance sheet, the minority at what basis, the cash charged how often — and
check_bridge.py holds each of them, including that the lines sum to the stated equity value
and that the equity divides to the stated per share. THE BRIDGE IS THEREFORE INTERNALLY
PERFECT AND JOINED TO NOTHING. Nobody had asked whether the per-share figure it arrives at
is the figure the study actually publishes.

The chain is: bridge_record.per_share --[nothing]--> the published central --[the document
and workbook gates]--> the reader. Only the second link was instrumented, so every defect
[R-BRIDGE-01] was founded on — minority at book instead of value share, the cash charged
twice, a stale sheet — can be corrected inside a bridge that then feeds nothing, and the
gate reports the correction while the published answer never moved.

MEASURED 07-09-2026. Five studies agree to the cent — AMOC, ARCC, PHDC, SCEM, STC — which
is what a joined bridge looks like. TWO DISAGREE, and one of them is the exemplar:

    ADNOCLS   bridge 1.5263 against a published central of 5.6054   -72.8%
    TMGH      bridge 65.1633 against 91.8306                        -29.0%

WHICH OF THE TWO IS WRONG IS NOT THIS GATE'S QUESTION AND IT DOES NOT GUESS. On ADNOCLS the
bridge divides an equity value of 11,292,414 by a field named `shares_mn` holding
7,398,498.76 — a count that is plainly not in millions — which is the SAME unit confusion
found the same morning in that study's circularity block, where net debt sits in thousands
against a market capitalisation in millions. Whether the bridge is mis-scaled or the
central comes from somewhere else is a question about the study, answerable by opening the
filings, and a gate that picked one would be asserting something it cannot support.

THE RELEASE IS A DECLARATION, NOT A TOLERANCE. A study whose central legitimately comes
from a lens the bridge does not serve — a sum-of-the-parts where the bridge covers one leg,
a two-sided answer with no single central — declares `bridge_serves` naming what the bridge
produces and why the published answer differs. AN EMPTY DECLARATION HAS SWITCHED THE CHECK
OFF RATHER THAN DECLARED IT.

TOLERANCE IS DERIVED FROM THE PRINTED ROUNDING, NEVER CHOSEN: half a unit in the last
decimal each figure is committed to, propagated through the division — arithmetic about the
record, the table-footing precedent. Five studies clear it by being exactly equal.

RATCHET [R-ENF-02] with each entry carrying its MEASURED disagreement, so a bridge drifting
further from the answer is a NEW breach [R-ENF-08]. POPULATION-ANCHORED [R-ENF-04] BOTH
WAYS: zero directories fails, and so does zero studies committing BOTH figures.

USAGE
    python3 scripts/check_bridge_reaches_answer.py [--prune]
"""
from __future__ import annotations

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit", "bridge_answer_outstanding.json")

PER_SHARE_KEYS = ("per_share", "value_per_share", "equity_per_share")
DECLARE_KEY = "bridge_serves"


def _half_unit(x):
    s = repr(float(x))
    if "e" in s or "E" in s:
        return 0.0
    d = len(s.split(".")[1]) if "." in s else 0
    return 0.5 * 10 ** -d


def _dig(o, keys):
    if isinstance(o, dict):
        for k in keys:
            v = o.get(k)
            if isinstance(v, (int, float)):
                return float(v)
        for v in o.values():
            r = _dig(v, keys)
            if r is not None:
                return r
    elif isinstance(o, list):
        for x in o:
            r = _dig(x, keys)
            if r is not None:
                return r
    return None


def central_of(doc):
    lr = doc.get("lens_record") or {}
    c = lr.get("central")
    if isinstance(c, dict):
        c = c.get("value")
    if isinstance(c, (int, float)):
        return float(c)
    p = (lr.get("primary") or {}).get("value")
    if isinstance(p, (int, float)):
        return float(p)
    c = doc.get("central")
    return float(c) if isinstance(c, (int, float)) else None


def studies(engine=ENGINE):
    out = {}
    for d in sorted(glob.glob(os.path.join(engine, "*_study"))):
        tk = os.path.basename(d)[:-6].upper()
        for n in ("study_numbers.json", "numbers.json"):
            p = os.path.join(d, n)
            if os.path.exists(p):
                out.setdefault(tk, p)
                break
    return out


def load():
    if not os.path.exists(OUTSTANDING):
        return {}
    try:
        return json.load(open(OUTSTANDING, encoding="utf-8")).get("outstanding", {})
    except Exception:
        return {}


def measure():
    bad, read = {}, 0
    for tk, path in sorted(studies().items()):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        br = doc.get("bridge_record") or {}
        ps = _dig(br, PER_SHARE_KEYS)
        cen = central_of(doc)
        if ps is None or cen is None:
            continue                      # a study committing one of the two is out of scope
        read += 1
        if (doc.get(DECLARE_KEY) or "").strip():
            continue
        tol = max(_half_unit(ps), _half_unit(cen))
        if abs(ps - cen) <= tol:
            continue
        bad[tk] = {"per_share": ps, "central": cen,
                   "gap": (ps / cen - 1.0) if cen else None,
                   "why": ("the equity bridge arrives at %.4f a share and the study "
                           "publishes %.4f (%+.1f%%), with no %s declaring what the bridge "
                           "serves. A bridge joined to nothing can be corrected without the "
                           "answer moving" % (ps, cen, 100 * (ps / cen - 1.0) if cen else 0,
                                              DECLARE_KEY))}
    return bad, read


def main(argv):
    prune = "--prune" in argv
    all_st = studies()
    if not all_st:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1
    bad, read = measure()
    if read == 0:
        print("FAIL — %d study directories and NOT ONE commits both a bridge per-share and "
              "a published central. A reader that stopped matching reads exactly like a "
              "book of joined bridges [R-ENF-04]." % len(all_st))
        return 1

    known = load()
    if prune:
        json.dump({"rule": "R-BRIDGE-01 — the bridge reaches the published answer",
                   "note": "May only SHORTEN. An entry excuses the DISAGREEMENT it records; "
                           "a bridge drifting further from the answer is a NEW breach "
                           "[R-ENF-08].",
                   "outstanding": bad},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print("pruned: %d listed (was %d)" % (len(bad), len(known)))
        return 0

    print("[R-BRIDGE-01] the bridge against the answer the study publishes")
    print("  study directories examined : %d" % len(all_st))
    print("  committing both figures    : %d" % read)
    print("  reaching the answer        : %d" % (read - len(bad)))

    new, worse = [], []
    for tk, det in sorted(bad.items()):
        e = known.get(tk)
        if e is None:
            new.append(tk)
        elif isinstance(e.get("gap"), (int, float)) and det["gap"] is not None \
                and abs(det["gap"]) > abs(e["gap"]) + 1e-9:
            worse.append((tk, e["gap"], det["gap"]))
        print("  %-6s %-13s %s" % ("NEW" if e is None else "known", tk, det["why"]))

    rc = 0
    if new:
        print("\nFAIL — %d bridge(s) do not reach the answer their study publishes: %s"
              % (len(new), ", ".join(new)))
        print("   Which of the two is wrong is a question about the study. Declare what "
              "the bridge serves, or join it to the answer. Never move either figure to "
              "close the gap.")
        rc = 1
    for tk, was, now in worse:
        print("\nFAIL — %s has drifted further: %+.1f%% excused, %+.1f%% now [R-ENF-08]."
              % (tk, 100 * was, 100 * now))
        rc = 1
    if rc:
        return rc
    print("\nOK — every committed bridge reaches the answer its study publishes, or says "
          "what it serves instead.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
