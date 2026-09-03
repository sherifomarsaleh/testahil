#!/usr/bin/env python3
"""A check nobody has seen fail is not evidence.  [R-GAP-02] negative control.

Reinjects every condition the publication block exists to catch, plus the clean
cases it must NOT fire on, into a throwaway tree. Each case asserts the DIRECTION
of the verdict, so a gate that started passing everything — or blocking
everything — goes red here rather than reading as rigour.
"""
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

DISSENT_OK = """# TK — market dissent

DISSENT_AT_GAP: -42.0%

## MECHANISM
The market capitalises a plant whose bank-approved cost and derived nameplate,
disclosed at note 14, do not earn the capital sunk into them.

## REVERSE READ
The price implies a flat nominal discount rate of 11% against a sovereign at 23.0%.

## WHY NOT CREDIBLE
No leveraged producer funds itself at half its own government's borrowing cost.

## WHAT WE CHECKED
Base year foots; every disclosed period read; bridge on the latest sheet; one
macro path; cash charged once; the claims recomputed.

## FALSIFIER
A disclosed matched pair of nameplate and cost that earns above the cost of capital.
"""


def build(tmp, ticker, central, price, dissent=None, two_sided=None):
    eng = os.path.join(tmp, "engine")
    sd = os.path.join(eng, "%s_study" % ticker.lower())
    os.makedirs(sd, exist_ok=True)
    nums = {"spot": price, "spot_date": "2026-09-03"}
    if two_sided:
        nums["central"] = None
        nums["central_two_sided"] = {"branches": [
            {"label": "a", "value": two_sided[0]}, {"label": "b", "value": two_sided[1]}]}
    else:
        nums["central"] = central
    json.dump(nums, open(os.path.join(sd, "study_numbers.json"), "w"))
    # THE PRICE COMES FROM THE COMMITTED SUPPLIED ARTEFACT, which is what the
    # gate reads. A fixture writing a file the gate does not open would be a
    # negative control proving only that the sandbox was untouched [R-ENF-04].
    os.makedirs(os.path.join(eng, "prices"), exist_ok=True)
    json.dump({"supplied_on": "2026-09-03", "prices": {
        ticker.upper(): {"price": price, "date": "2026-09-03", "ccy": "EGP"}}},
        open(os.path.join(eng, "prices", "SUPPLIED_03-09-2026.json"), "w"))
    if dissent is not None:
        open(os.path.join(sd, "MARKET_DISSENT_03-09-2026.md"), "w").write(dissent)
    return eng


CASES = [
    # (name, central, price, dissent, two_sided, must_publish)
    ("inside the band",                 74.0, 77.0, None, None, True),
    ("just inside the edge",            70.0, 77.0, None, None, True),
    ("just outside the edge",           69.0, 77.0, None, None, False),
    ("far below, no dissent",           53.2, 77.0, None, None, False),
    ("far above, no dissent",          110.0, 77.0, None, None, False),
    ("far below, dissent complete",     44.7, 77.0, DISSENT_OK, None, True),
    ("dissent missing a heading",       44.7, 77.0,
     DISSENT_OK.replace("## FALSIFIER", "## NOTES"), None, False),
    ("dissent with no gap marker",      44.7, 77.0,
     DISSENT_OK.replace("DISSENT_AT_GAP: -42.0%", ""), None, False),
    ("dissent argued at a stale gap",   30.0, 77.0, DISSENT_OK, None, False),
    ("two-sided, both branches far",     0.0, 14.41, None, (1.79, 5.90), False),
    ("two-sided, one branch inside",     0.0, 14.41, None, (1.79, 13.5), True),
]


def main():
    failures = []
    for name, central, price, dissent, two, must in CASES:
        tmp = tempfile.mkdtemp()
        try:
            eng = build(tmp, "TK", central, price, dissent, two)
            for m in ("check_publish_block", "check_valuation_gap"):
                sys.modules.pop(m, None)
            import check_valuation_gap as gap
            gap.ENGINE = eng
            import check_publish_block as blk
            blk.ENGINE = eng
            blk.gap = gap
            got, why, _ = blk.verdict("TK")
            if got != must:
                failures.append("%-32s expected %s, got %s (%s)"
                                % (name, "PUBLISH" if must else "HELD",
                                   "PUBLISH" if got else "HELD", why))
            else:
                print("  ok  %-32s %s" % (name, "PUBLISH" if got else "HELD"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # AND THE POPULATION GUARD: an empty tree must FAIL, not report clean.
    tmp = tempfile.mkdtemp()
    try:
        eng = os.path.join(tmp, "engine")
        os.makedirs(eng)
        for m in ("check_publish_block", "check_valuation_gap"):
            sys.modules.pop(m, None)
        import check_valuation_gap as gap
        gap.ENGINE = eng
        import check_publish_block as blk
        blk.ENGINE = eng
        blk.gap = gap
        if blk.main([]) == 0:
            failures.append("an empty population reported clean [R-ENF-04]")
        else:
            print("  ok  %-32s FAIL" % "empty population")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("\nNEGATIVE CONTROL FAILED:")
        for f in failures:
            print("  " + f)
        return 1
    print("\n%d conditions reinjected, every one behaved" % (len(CASES) + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
