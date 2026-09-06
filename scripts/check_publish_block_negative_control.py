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
    ("just below the edge",             69.0, 77.0, None, None, False),
    ("just above the edge",             86.0, 77.0, None, None, True),
    ("far below, no dissent",           53.2, 77.0, None, None, False),
    ("far above, no dissent — OK now", 110.0, 77.0, None, None, True),
    ("far below, dissent complete",     44.7, 77.0, DISSENT_OK, None, True),
    ("dissent missing a heading",       44.7, 77.0,
     DISSENT_OK.replace("## FALSIFIER", "## NOTES"), None, False),
    ("dissent with no gap marker",      44.7, 77.0,
     DISSENT_OK.replace("DISSENT_AT_GAP: -42.0%", ""), None, False),
    ("dissent argued at a stale gap",   30.0, 77.0, DISSENT_OK, None, False),
    ("two-sided, both branches far",     0.0, 14.41, None, (1.79, 5.90), False),
    ("two-sided, one branch inside",     0.0, 14.41, None, (1.79, 13.5), True),
    ("two-sided, one branch above",      0.0, 14.41, None, (1.79, 20.0), True),
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
            blk.phase1_proven = lambda: (True, "stubbed proven for the gap cases")
            got, why, _ = blk.verdict("TK")
            if got != must:
                failures.append("%-32s expected %s, got %s (%s)"
                                % (name, "PUBLISH" if must else "HELD",
                                   "PUBLISH" if got else "HELD", why))
            else:
                print("  ok  %-32s %s" % (name, "PUBLISH" if got else "HELD"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # THE METHOD HOLD IS TESTED SEPARATELY, and in BOTH directions. The gap cases
    # above stub it proven so they measure the gap; these measure the method, so a
    # future change that quietly drops one condition cannot pass by satisfying the
    # other — which is exactly how a two-condition rule normally decays into one.
    for name, proven, must in (("method proven, inside band", True, True),
                               ("method NOT proven, inside band", False, False),
                               ("method NOT proven, dissent filed", False, False)):
        tmp = tempfile.mkdtemp()
        try:
            eng = build(tmp, "TK", 74.0, 77.0,
                        DISSENT_OK if "dissent" in name else None, None)
            for m in ("check_publish_block", "check_valuation_gap"):
                sys.modules.pop(m, None)
            import check_valuation_gap as gap
            gap.ENGINE = eng
            import check_publish_block as blk
            blk.ENGINE = eng
            blk.gap = gap
            blk.phase1_proven = lambda p=proven: (
                p, "stubbed" if p else "Phase 1 is not proven — stubbed")
            got, why, _ = blk.verdict("TK")
            if got != must:
                failures.append("%-32s expected %s, got %s (%s)"
                                % (name, "PUBLISH" if must else "HELD",
                                   "PUBLISH" if got else "HELD", why))
            else:
                print("  ok  %-32s %s" % (name, "PUBLISH" if got else "HELD"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # THE METALS EXCLUSION, IN BOTH DIRECTIONS AND WITH THE ROSTER MUTATED.
    #
    # A name outside this rule's population must be reported as OUTSIDE IT, and a name
    # inside it must not escape by resembling one. The three conditions are the whole
    # claim: a registered metal with no study PUBLISHES; an equity with no study is
    # still UNREADABLE and HELD, which is what stops "delete the directory" becoming
    # the cheapest route past this gate; and a metal that is NOT on the roster is HELD
    # too, so the exclusion tracks the site's own registration rather than a hunch
    # about what a name looks like. All three are run with the method stubbed NOT
    # proven — the state the book is actually in — because an exclusion that only holds
    # while the method hold is off is not an exclusion from the rule, and reading the
    # roster as a stub of _metal_keys asserts the mutation LANDED rather than trusting
    # that it did.
    for name, tk, roster, must in (
            ("metal, no study, on roster",      "SILVER", {"GOLD", "SILVER"}, True),
            ("equity, no study, not a metal",   "TK",     {"GOLD", "SILVER"}, False),
            ("metal-shaped, NOT on roster",     "SILVER", {"GOLD"},           False),
            ("roster unreadable, excludes none", "SILVER", set(),             False)):
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
            blk._metal_keys = lambda r=roster: r
            blk.phase1_proven = lambda: (False, "Phase 1 is not proven — stubbed")
            assert not os.path.isdir(os.path.join(eng, "%s_study" % tk.lower())), \
                "fixture did not land: %s_study exists" % tk.lower()
            got, why, _ = blk.verdict(tk)
            if got != must:
                failures.append("%-32s expected %s, got %s (%s)"
                                % (name, "PUBLISH" if must else "HELD",
                                   "PUBLISH" if got else "HELD", why))
            else:
                print("  ok  %-32s %s" % (name, "PUBLISH" if got else "HELD"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # THE PRICE-ONLY EXEMPTION [R-GAP-02 AMENDED 06-Sep-2026], IN BOTH DIRECTIONS.
    #
    # An exemption is the most dangerous thing in a gate, because it is the one place
    # the gate is designed to stop looking. Every condition below is run with the
    # method stubbed NOT proven — the state the book is actually in — since an
    # exemption that only matters while the hold is off is not an exemption at all.
    # The pair of published entries is injected through _published_pair, and each
    # fixture ASSERTS the injection changed what it meant to change rather than
    # trusting that it did: a control that mutates nothing goes green for the wrong
    # reason, which is the failure [R-ENF-04] is named for.
    #
    # CASE "nothing pending" IS THE ONE THAT MATTERS MOST. Run ON main the tree and
    # origin/main are identical by construction, so a comparison that only asked
    # "does fair{} differ?" would answer no for every study in the book and exempt
    # all of them while reporting itself green. It must stay HELD.
    LIVE = {"fair": {"bear": 46.84, "base": 53.12, "full": 59.1},
            "files": {"pdf": "files/TK_06-08-2026.pdf"}, "spot": 79.0}

    def pair(here, there):
        return lambda: (({"TK": here} if here is not None else {}),
                        ({"TK": there} if there is not None else {}))

    moved_fair = dict(LIVE, spot=98.52, fair={"bear": 60.0, "base": 70.0, "full": 80.0})
    moved_files = dict(LIVE, spot=98.52, files={"pdf": "files/TK_04-09-2026.pdf"})
    for name, here, there, central, price, dissent, must in (
            ("price-only, method unproven", dict(LIVE, spot=98.52), LIVE,
             74.0, 77.0, None, True),
            ("nothing pending — not a publish", dict(LIVE), LIVE,
             74.0, 77.0, None, False),
            ("fair value moves — a study publish", moved_fair, LIVE,
             74.0, 77.0, None, False),
            ("deliverables move — a study publish", moved_files, LIVE,
             74.0, 77.0, None, False),
            ("absent on main — a first publish", dict(LIVE, spot=98.52), None,
             74.0, 77.0, None, False),
            ("price-only, but breaches the gap", dict(LIVE, spot=98.52), LIVE,
             53.2, 77.0, None, False),
            ("price-only, breaches, dissent filed", dict(LIVE, spot=98.52), LIVE,
             44.7, 77.0, DISSENT_OK, True)):
        tmp = tempfile.mkdtemp()
        try:
            eng = build(tmp, "TK", central, price, dissent, None)
            for m in ("check_publish_block", "check_valuation_gap"):
                sys.modules.pop(m, None)
            import check_valuation_gap as gap
            gap.ENGINE = eng
            import check_publish_block as blk
            blk.ENGINE = eng
            blk.gap = gap
            blk._published_pair = pair(here, there)
            blk.phase1_proven = lambda: (False, "Phase 1 is not proven — stubbed")
            # the mutation must have LANDED: the two sides must stand in the
            # relationship this case is about, before the gate is asked anything.
            a, b = blk._published_pair()
            assert a.get("TK") == here and b.get("TK") == there, \
                "fixture did not land for %r" % name
            got, why, _ = blk.verdict("TK")
            if got != must:
                failures.append("%-36s expected %s, got %s (%s)"
                                % (name, "PUBLISH" if must else "HELD",
                                   "PUBLISH" if got else "HELD", why))
            else:
                print("  ok  %-36s %s" % (name, "PUBLISH" if got else "HELD"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # AND THE EXEMPTION'S OWN FAILURE MODE: an unreadable comparison releases NOTHING.
    tmp = tempfile.mkdtemp()
    try:
        eng = build(tmp, "TK", 74.0, 77.0, None, None)
        for m in ("check_publish_block", "check_valuation_gap"):
            sys.modules.pop(m, None)
        import check_valuation_gap as gap
        gap.ENGINE = eng
        import check_publish_block as blk
        blk.ENGINE = eng
        blk.gap = gap

        def _boom():
            raise RuntimeError("node is not available")
        blk._published_pair = _boom
        blk.phase1_proven = lambda: (False, "Phase 1 is not proven — stubbed")
        ok_po, why_po = blk.price_only_publish("TK")
        assert not ok_po and "not an exemption" in why_po, \
            "an unreadable comparison did not fall to the strict side: %s" % why_po
        got, why, _ = blk.verdict("TK")
        if got:
            failures.append("unreadable comparison released the method hold (%s)" % why)
        else:
            print("  ok  %-36s %s" % ("unreadable comparison", "HELD"))
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
    print("\n%d conditions reinjected, every one behaved" % (len(CASES) + 16))
    return 0


if __name__ == "__main__":
    sys.exit(main())
