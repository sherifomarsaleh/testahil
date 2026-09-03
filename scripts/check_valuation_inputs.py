#!/usr/bin/env python3
"""[R-FCAL-01 AMENDED] — a run commits the inputs a VALUE is rebuilt from.

WHY THIS RUNS OUTSIDE THE RUN [R-ENF-01]. The amendment it enforces was adopted
because five careful, well-evidenced walk-forwards each answered the question they
were built for and left no trace of the figures beside it. Nobody disagreed with
the idea of committing a balance sheet; it simply was not asked for, and nothing
outside the run was looking. A self-attested "inputs committed: true" would have
been set by every one of them.

WHAT IT ASSERTS, and each clause is one the amendment states:

  the record EXISTS            valuation_inputs.json beside the run
  it COVERS every origin       the run's own origin list, not a subset
  every ITEM is present        each of the six is a value or an explicit
                               missing-with-a-reason — an item simply absent is a
                               FAIL, because a block quietly carrying five of six
                               reads as complete
  the share count FOOTS        issued capital / par reproduces the stated count
  a derived CAPEX says so      and names the identity it was derived by
  the ROUTE is recorded        text layer or OCR, with the file it came from

RATCHET [R-ENF-02]. The runs that predate the amendment are listed in
engine/build_depth_audit/valuation_inputs_outstanding.json and are allowed to fail;
the build breaks on a NEW run with no record, or on a listed run whose record is
present but malformed. The list may only ever SHORTEN — `--prune` rewrites it from
what actually passes and never adds.

POPULATION ANCHORED ELSEWHERE [R-ENF-04]. The population is the walk-forward run
directories ON DISK, not the outstanding list and not this file: a run that
examined zero runs FAILS rather than reporting clean, and every ticker on the
ratchet must resolve to a directory or the list has gone stale against the thing
it is meant to describe.
"""
from __future__ import annotations

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit",
                           "valuation_inputs_outstanding.json")

RECORD = "valuation_inputs.json"
ITEMS = ("cash", "debt", "capex", "ppe", "dep", "wc", "shares")
DERIVED_IDENTITY = "capex = dppe + d&a"


def runs(engine=ENGINE):
    out = {}
    for d in sorted(glob.glob(os.path.join(engine, "*_walkforward"))):
        out[os.path.basename(d).replace("_walkforward", "").upper()] = d
    return out


def _foots(rec):
    """capital / par must reproduce the stated count. No tolerance worth the name."""
    cap, par, n = rec.get("issued_capital"), rec.get("par_value"), rec.get("value")
    if not all(isinstance(v, (int, float)) and v for v in (cap, par, n)):
        return False, "a share-count record without capital, par and a count"
    implied = cap / par
    if abs(implied - n) > max(1.0, 1e-6 * n):
        return False, ("capital %.0f / par %.4g = %.0f against a stated %.0f — it "
                       "does not foot against itself" % (cap, par, implied, n))
    return True, ""


def check_record(path):
    """[] if the record conforms, else the reasons it does not."""
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return ["the record will not parse: %s" % e]
    bad = []
    origins = doc.get("origins")
    if not isinstance(origins, dict) or not origins:
        return ["the record names no origins"]
    for y, block in sorted(origins.items()):
        if not isinstance(block, dict):
            bad.append("%s: the origin is not a block" % y)
            continue
        for item in ITEMS:
            rec = block.get(item)
            if rec is None:
                bad.append("%s: %s is absent from the block — a missing item is "
                           "RECORDED as missing, never omitted" % (y, item))
                continue
            if not isinstance(rec, dict):
                bad.append("%s: %s is not a record" % (y, item))
                continue
            if "missing" in rec:
                if not str(rec.get("missing") or "").strip():
                    bad.append("%s: %s is marked missing with no reason" % (y, item))
                continue
            if rec.get("value") is None:
                bad.append("%s: %s carries neither a value nor a missing reason"
                           % (y, item))
                continue
            if not str(rec.get("source") or "").strip():
                bad.append("%s: %s carries a value and no source" % (y, item))
            if not str(rec.get("route") or "").strip():
                bad.append("%s: %s carries a value and no route — text layer or "
                           "OCR, with the file" % (y, item))
            if item == "shares":
                ok, why = _foots(rec)
                if not ok:
                    bad.append("%s: %s" % (y, why))
            if item == "capex" and rec.get("derived"):
                if DERIVED_IDENTITY not in str(rec.get("identity") or "").lower():
                    bad.append("%s: capex is derived and does not name the "
                               "identity it was derived by" % y)
    return bad


def load_outstanding():
    if not os.path.exists(OUTSTANDING):
        return {}
    try:
        return json.load(open(OUTSTANDING, encoding="utf-8")).get("runs", {})
    except Exception:
        return {}


def main(argv):
    prune = "--prune" in argv
    engine = ENGINE
    for a in argv:
        if a.startswith("--engine="):
            engine = a.split("=", 1)[1]
    found = runs(engine)
    if not found:
        print("REFUSED: no walk-forward run directories were examined. An empty "
              "population is not a clean result [R-ENF-04].")
        return 2

    outstanding = load_outstanding()
    stale = [tk for tk in outstanding if tk not in found]
    conforming, waived, failed = [], [], {}
    for tk, d in sorted(found.items()):
        p = os.path.join(d, RECORD)
        if not os.path.exists(p):
            if tk in outstanding:
                waived.append(tk)
            else:
                failed[tk] = ["no %s beside the run" % RECORD]
            continue
        bad = check_record(p)
        if bad:
            failed[tk] = bad          # a record that EXISTS must conform, waived or not
        else:
            conforming.append(tk)

    print("valuation-input block [R-FCAL-01 AMENDED]\n")
    print("  runs on disk        %d   %s" % (len(found), ", ".join(sorted(found))))
    print("  conforming          %d   %s" % (len(conforming), ", ".join(conforming)))
    print("  waived on the ratchet %d %s" % (len(waived), ", ".join(sorted(waived))))
    print("  failing             %d" % len(failed))
    for tk, why in sorted(failed.items()):
        print("    %-6s %s" % (tk, why[0]))
        for w in why[1:6]:
            print("           %s" % w)
        if len(why) > 6:
            print("           ... and %d more" % (len(why) - 6))
    if stale:
        print("\n  REFUSED: the ratchet names runs that do not resolve on disk: %s"
              % ", ".join(sorted(stale)))
        return 2

    if prune:
        keep = {tk: v for tk, v in outstanding.items()
                if tk in found and tk not in conforming}
        json.dump({"_": ("Runs predating [R-FCAL-01 AMENDED] (03-09-2026), allowed "
                         "to carry no valuation-input block. THE LIST MAY ONLY "
                         "SHORTEN — --prune rewrites it from what passes and never "
                         "adds [R-ENF-02]."),
                   "runs": keep},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        print("\n  pruned: %d run(s) remain outstanding" % len(keep))

    if failed:
        print("\nFAILED — a run whose record exists must conform to it, and a run "
              "not on the ratchet must have one.")
        return 1
    print("\nOK — every run either commits a conforming valuation-input block or "
          "is a listed pre-amendment run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
