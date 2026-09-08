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


AUTH_OK = """# TK — publication authorisation

AUTHORISED_BY: the principal
AUTHORISED_AT_GAP: -42.0%
AUTHORISED_CENTRAL: 44.70
DATE: 2026-09-08

The case in MARKET_DISSENT_03-09-2026.md was put to the principal and approved
for publication at this gap.
"""

AUTH_NO_NAME = AUTH_OK.replace("AUTHORISED_BY: the principal\n", "")
AUTH_NO_GAP = AUTH_OK.replace("AUTHORISED_AT_GAP: -42.0%\n", "")
AUTH_STALE = AUTH_OK.replace("-42.0%", "-12.0%")


def build(tmp, ticker, central, price, dissent=None, two_sided=None, auth=None):
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
    if auth is not None:
        open(os.path.join(sd, "PUBLISH_AUTHORISATION_08-09-2026.md"), "w").write(auth)
    return eng


CASES = [
    # (name, central, price, dissent, two_sided, must_publish[, auth])
    ("inside the band",                 74.0, 77.0, None, None, True),
    ("just inside the edge",            70.0, 77.0, None, None, True),
    ("just below the edge",             69.0, 77.0, None, None, False),
    ("just above the edge",             86.0, 77.0, None, None, True),
    ("far below, no dissent",           53.2, 77.0, None, None, False),
    ("far above, no dissent — OK now", 110.0, 77.0, None, None, True),
    # [R-GAP-02 CLAUSE FOUR] INVERTED RATHER THAN DELETED. This construction was
    # correct evidence that a complete dissent RELEASED the block, and from
    # 08-Sep-2026 it must go the other way: the dissent is the case, and the
    # principal is the decision. Keeping the fixture and flipping its expectation
    # is the only way the change is tested where it matters — the same precedent
    # [R-GAP-01] set when its trigger went two-sided.
    ("far below, dissent but no authorisation", 44.7, 77.0, DISSENT_OK, None, False),
    ("dissent missing a heading",       44.7, 77.0,
     DISSENT_OK.replace("## FALSIFIER", "## NOTES"), None, False),
    ("dissent with no gap marker",      44.7, 77.0,
     DISSENT_OK.replace("DISSENT_AT_GAP: -42.0%", ""), None, False),
    ("dissent argued at a stale gap",   30.0, 77.0, DISSENT_OK, None, False),
    ("two-sided, both branches far",     0.0, 14.41, None, (1.79, 5.90), False),
    ("two-sided, one branch inside",     0.0, 14.41, None, (1.79, 13.5), True),
    ("two-sided, one branch above",      0.0, 14.41, None, (1.79, 20.0), True),
    # [R-GAP-02 CLAUSE FOUR] the authorisation half. AN EXEMPTION IS ONLY AS NARROW
    # AS THE CASES THAT PROVE IT CANNOT BE WIDENED, so every way of arriving at a
    # release without a real decision is held: no case behind the approval, nobody
    # named as approving, no gap stated, and an approval of a different gap.
    ("dissent + authorisation",         44.7, 77.0, DISSENT_OK, None, True, AUTH_OK),
    ("authorisation with no dissent",   44.7, 77.0, None,       None, False, AUTH_OK),
    ("authorisation naming nobody",     44.7, 77.0, DISSENT_OK, None, False, AUTH_NO_NAME),
    ("authorisation with no gap",       44.7, 77.0, DISSENT_OK, None, False, AUTH_NO_GAP),
    ("authorisation of a stale gap",    44.7, 77.0, DISSENT_OK, None, False, AUTH_STALE),
]


def main():
    failures = []
    # COUNT AGAINST WHAT ACTUALLY RAN, NEVER A TYPED OFFSET (08-Sep-2026). The
    # tally read `len(CASES) + 16`, so three conditions added below it would have
    # been reported as 34 — a control silently understating its own coverage,
    # which is the shape [R-ENF-04] names: the number looks authoritative and
    # moves only when somebody remembers. Every condition now records itself.
    ran = []
    for case in CASES:
        name, central, price, dissent, two, must = case[:6]
        auth = case[6] if len(case) > 6 else None
        tmp = tempfile.mkdtemp()
        try:
            eng = build(tmp, "TK", central, price, dissent, two, auth)
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
                ran.append(name); print("  ok  %-32s %s" % (name, "PUBLISH" if got else "HELD"))
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
                ran.append(name); print("  ok  %-32s %s" % (name, "PUBLISH" if got else "HELD"))
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
                ran.append(name); print("  ok  %-32s %s" % (name, "PUBLISH" if got else "HELD"))
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
            # [R-GAP-02 AMENDED 06-Sep-2026, SECOND] THIS CASE IS INVERTED RATHER
            # THAN DELETED, on the precedent [R-GAP-01] set when its own trigger went
            # two-sided: it asserted that a price-only publish breaching the gap must
            # stay HELD, which was correct evidence for the FIRST amendment and must
            # now go the other way. Keeping the construction and flipping its
            # expectation is the sharpest available evidence the second amendment took
            # effect; deleting it would have left the change untested exactly where it
            # matters.
            ("price-only, breaches the gap - released", dict(LIVE, spot=98.52), LIVE,
             53.2, 77.0, None, True),
            ("price-only, breaches, dissent filed", dict(LIVE, spot=98.52), LIVE,
             44.7, 77.0, DISSENT_OK, True),
            # AND THE FOUR WAYS THE WIDENED EXEMPTION COULD BE ABUSED, each of which
            # must still be HELD while breaching the gap - because what releases is the
            # ARITHMETIC condition and nothing else. If any of these publishes, the
            # exemption has stopped being about whether a valuation moves.
            ("breaches + fair value moves - held", moved_fair, LIVE,
             53.2, 77.0, None, False),
            ("breaches + deliverables move - held", moved_files, LIVE,
             53.2, 77.0, None, False),
            ("breaches + nothing pending - held", dict(LIVE), LIVE,
             53.2, 77.0, None, False),
            ("breaches + first publish - held", dict(LIVE, spot=98.52), None,
             53.2, 77.0, None, False)):
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
                ran.append(name); print("  ok  %-36s %s" % (name, "PUBLISH" if got else "HELD"))
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
            ran.append("unreadable comparison")
            print("  ok  %-36s %s" % ("unreadable comparison", "HELD"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # AND THE NAME THE EXEMPTION IS ASKED ABOUT (added 08-Sep-2026, on a real miss).
    #
    # A STUDY DIRECTORY STEM IS NOT ALWAYS ITS TICKERS KEY. campaign_queue.STUDY_ALIAS
    # has carried FERTIGLOBE -> FERTIGLB since the campaign was written, and
    # check_valuation_gap._resolve_ticker imports it — which is why the PRICE resolved
    # correctly. price_only_publish() keyed on the raw stem instead, missed BOTH sides
    # of the comparison, and reported the miss as "not on origin/main — a first publish
    # is never price-only": a plausible sentence naming a real refusal, about a
    # condition that was never tested [R-ENF-04]. It HELD a roll-forward that moved no
    # fair value at all, which is exactly what the exemption exists to release.
    #
    # RUN IN BOTH DIRECTIONS, because a fix that simply stopped missing would be
    # indistinguishable from one that stopped checking: an aliased study whose entry
    # sits under its REAL key must PUBLISH, and a study that genuinely resolves to
    # nothing on origin/main must still be HELD. The alias is injected into the
    # resolver's own cache rather than over the function, so the production code path
    # runs [R-ENF-03].
    for name, alias, there_key, must in (
            ("aliased study, entry under real key", {"TKLONG": "TK"}, "TK", True),
            ("aliased study, genuinely absent on main", {"TKLONG": "TK"}, None, False),
            ("no alias, stem is the key", {}, "TKLONG", True)):
        tmp = tempfile.mkdtemp()
        try:
            eng = build(tmp, "TKLONG", 74.0, 77.0, None, None)
            # the price must resolve under the RESOLVED name, not the stem
            json.dump({"supplied_on": "2026-09-03", "prices": {
                (alias.get("TKLONG") or "TKLONG"): {
                    "price": 77.0, "date": "2026-09-03", "ccy": "EGP"}}},
                open(os.path.join(eng, "prices", "SUPPLIED_03-09-2026.json"), "w"))
            for m in ("check_publish_block", "check_valuation_gap"):
                sys.modules.pop(m, None)
            import check_valuation_gap as gap
            gap.ENGINE = eng
            gap._ALIAS_CACHE = (alias, {})
            import check_publish_block as blk
            blk.ENGINE = eng
            blk.gap = gap
            here_key = alias.get("TKLONG", "TKLONG")
            blk._published_pair = lambda: (
                {here_key: dict(LIVE, spot=98.52)},
                ({there_key: LIVE} if there_key else {}))
            blk.phase1_proven = lambda: (False, "Phase 1 is not proven — stubbed")
            # THE MUTATION MUST HAVE LANDED: the stem must not resolve to itself
            # where an alias is set, or this case tests nothing.
            resolved, _ = gap._resolve_ticker("TKLONG")
            assert resolved == (alias.get("TKLONG") or "TKLONG"), \
                "alias did not land for %r" % name
            got, why, _ = blk.verdict("TKLONG")
            if got != must:
                failures.append("%-36s expected %s, got %s (%s)"
                                % (name, "PUBLISH" if must else "HELD",
                                   "PUBLISH" if got else "HELD", why))
            else:
                ran.append(name); print("  ok  %-36s %s" % (name, "PUBLISH" if got else "HELD"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # AND THE SAME NAME FROM THE CALLER'S SIDE (added 08-Sep-2026, same real miss).
    #
    # main() globs engine/*_study and passes the STEM; publish_site.py passes the
    # TICKERS KEY. verdict() built its path from whichever it was handed, so
    # `--ticker FERTIGLB` looked for engine/fertiglb_study, found nothing, and
    # answered "no study directory on disk" about a study sitting on disk under
    # engine/fertiglobe_study. Both directions must resolve to the SAME directory,
    # and a name with genuinely no study must still be refused — otherwise the fix
    # would have turned "unreadable is not clean" into "unfound is fine" [R-ENF-04].
    tmp = tempfile.mkdtemp()
    try:
        eng = build(tmp, "TKLONG", 74.0, 77.0, None, None)
        json.dump({"supplied_on": "2026-09-03", "prices": {
            "TK": {"price": 77.0, "date": "2026-09-03", "ccy": "EGP"}}},
            open(os.path.join(eng, "prices", "SUPPLIED_03-09-2026.json"), "w"))
        for m in ("check_publish_block", "check_valuation_gap"):
            sys.modules.pop(m, None)
        import check_valuation_gap as gap
        gap.ENGINE = eng
        gap._ALIAS_CACHE = ({"TKLONG": "TK"}, {})
        import check_publish_block as blk
        blk.ENGINE = eng
        blk.gap = gap
        blk._published_pair = pair(dict(LIVE, spot=98.52), LIVE)
        blk.phase1_proven = lambda: (False, "Phase 1 is not proven — stubbed")
        # the two spellings must land on ONE directory
        assert blk._study_dir("TKLONG") == blk._study_dir("TK") is not None, \
            "the stem and the ticker did not resolve to one study directory"
        # ...and a name with no study must still resolve to nothing
        assert blk._study_dir("NOTHINGHERE") is None, \
            "a name with no study resolved to a directory — the resolver invented one"
        for spelling in ("TKLONG", "TK"):
            got, why, _ = blk.verdict(spelling)
            if not got:
                failures.append("caller spelling %-8s expected PUBLISH, got HELD (%s)"
                                % (spelling, why))
            else:
                ran.append("caller spelling %s" % spelling)
                print("  ok  %-36s %s" % ("caller spelling " + spelling, "PUBLISH"))
        got, why, _ = blk.verdict("NOTHINGHERE")
        if got or "no study directory" not in why:
            failures.append("a name with no study was not refused (%s)" % why)
        else:
            ran.append("no study on disk")
            print("  ok  %-36s %s" % ("no study on disk", "HELD"))
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
            ran.append("empty population")
            print("  ok  %-32s FAIL" % "empty population")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if failures:
        print("\nNEGATIVE CONTROL FAILED:")
        for f in failures:
            print("  " + f)
        return 1
    assert len(ran) >= len(CASES), (
        "the control reported fewer conditions than CASES holds — it did not run "
        "what it claims [R-ENF-04]")
    print("\n%d conditions reinjected, every one behaved" % len(ran))
    return 0


if __name__ == "__main__":
    sys.exit(main())
