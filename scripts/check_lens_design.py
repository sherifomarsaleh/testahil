"""THE LENS ARCHITECTURE, CHECKED FROM OUTSIDE THE STUDY.

[R-LENS-03], enforced per [R-ENF-01].

The defect. PHDC published a central that was a weighted blend of four lenses at
typed weights — 45% discounted cash flow, 15% book value, 20% an earnings
multiple, 20% normalised earnings power. Three of the four value a developer on
its reported accounting earnings and its historical-cost book. For a company
whose value sits in an undelivered order book carried at historical cost in a
currency that has lost most of its value since 2022, those three measure a floor
rather than a value. The cash-flow lens landed within 2.2% of the market price;
the blend landed 28% below it. Nothing in the study was wrong except its
architecture, and the weights had never cleared any out-of-sample test — they
were chosen, written down, and inherited by the next study.

What this gate holds studies to: one class primary is the central, the other
lenses are cross-checks published beside it, the envelope is the RANGE of the
present-value reads on one clock, book value is a disclosed floor and never
weighted, a relative multiple never takes its multiple from the current price,
and normalised earnings is Fisher-consistent or absent.

Population-anchored [R-ENF-04], ratcheted [R-ENF-02].

    python3 scripts/check_lens_design.py
    python3 scripts/check_lens_design.py --prune
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE)

OUTSTANDING_FILE = os.path.join(ENGINE, "build_depth_audit", "lens_outstanding.json")
RECORD_KEYS = ("lens_record", "lens_design")


def studies():
    """The record directories a record-reading gate can inspect, resolved through
    engine/study_population.py rather than by globbing engine/*_study.

    THE GLOB WAS THE WRONG POPULATION. All 90 covered names carry a delivered
    valuation study; 23 commit a record. This gate globbed the directories and
    printed a count with NO DENOMINATOR, which is why 24 looked like the book.
    The names with no record are DEFERRED to the shared no-record ratchet, which
    the valuation-gap gate reports on — they are not re-listed here, because ten
    gates reporting one fact is the duplication this refactor exists to avoid.

    The import is LAZY so a sandbox that copies this script without engine/
    beside it does not die on an import it never needed.
    """
    global _DEFERRED, _POP_LINE
    # A SANDBOXED FIXTURE SUPPLIES ITS OWN POPULATION, AND SAYS SO OUT LOUD.
    # Several negative controls copy this script into a temp tree holding a fake
    # ENGINE and run it as a subprocess, so the resolver is not importable there —
    # and it should not be, because the whole point of those fixtures is a
    # population they control. The escape is an explicit environment variable that
    # CI never sets, and taking it PRINTS that it was taken: a switch that quietly
    # restored the directory glob would reinstate the defect this replaced.
    if os.environ.get('TESTAHIL_FIXTURE_POPULATION'):
        dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
        _DEFERRED, _POP_LINE = [], ('population: FIXTURE — %d study directories under a '
                                    'sandboxed ENGINE, not the book' % len(dirs))
        print(_POP_LINE)
        return dirs
    if ENGINE not in sys.path:
        sys.path.insert(0, ENGINE)
    import study_population
    dirs, _DEFERRED, _POP_LINE = study_population.examinable()
    # printed HERE so the ten gates have exactly ONE edit site each and the line
    # cannot be forgotten in one of them: a denominator that appears in nine gates
    # and not the tenth is the drift this refactor exists to stop
    print(_POP_LINE)
    return dirs


_DEFERRED, _POP_LINE = [], ""


def ticker_of(sdir):
    return os.path.basename(sdir)[: -len("_study")].upper()


def numbers_file(sdir):
    for name in ("study_numbers.json", "numbers.json"):
        p = os.path.join(sdir, name)
        if os.path.exists(p):
            return p
    cands = [p for p in glob.glob(os.path.join(sdir, "*.json"))
             if "numbers" in os.path.basename(p).lower()]
    return cands[0] if cands else None


def find_record(doc):
    for k in RECORD_KEYS:
        if isinstance(doc.get(k), dict):
            return doc[k]
    meta = doc.get("meta")
    if isinstance(meta, dict):
        for k in RECORD_KEYS:
            if isinstance(meta.get(k), dict):
                return meta[k]
    return None


def audit(sdir):
    import research_protocol as RP

    tk = ticker_of(sdir)
    nf = numbers_file(sdir)
    if not nf:
        return "unreadable", "no committed numbers file in the study directory"
    try:
        doc = json.load(open(nf, encoding="utf-8"))
    except Exception as e:                                   # noqa: BLE001
        return "unreadable", "%s will not parse: %s" % (os.path.basename(nf), e)
    rec = find_record(doc)
    if rec is None:
        return "no_record", "carries no lens record"
    try:
        out = RP.assert_lens_design(rec, ticker=tk)
    except AssertionError as e:
        return "fail", str(e).replace("\n", " ")
    except Exception as e:                                   # noqa: BLE001
        return "fail", "%s: %s" % (type(e).__name__, e)
    # THE IDENTITY CLAUSE IS THE STRONGEST THING THIS RULE SAYS AND IT DOES NOT ALWAYS RUN.
    # assert_lens_design() tests "the primary IS the central" only where the record EXPOSES a
    # central or a containing range; where it exposes neither, the clause is skipped and the
    # study returns ok. That skip is correct in the assertion — `central` is optional in this
    # record's shape and an assertion may not invent a field requirement — and it is NOT
    # correct to then count the study as conforming, because the clause that would have
    # caught a blend never ran.
    #
    # MEASURED 06-09-2026, and the correlation is the finding rather than the count: NINE
    # studies carry a record exposing no central, SEVEN carry no record at all, and only
    # SEVEN of twenty-three were held to the identity test — while a book-wide census found
    # NINE studies still publishing a weighted central, EVERY ONE of them in the unheld
    # group. A study with nothing to be tested on is not a study that passed [R-ENF-04].
    # THE CONDITION MUST MATCH THE ONE THAT ACTUALLY GATES THE CLAUSE. A first draft of this
    # check asked for a missing central AND a missing primary value, and caught two studies
    # where the real number is nine — because assert_lens_design() wraps the WHOLE identity
    # test in `if central is not None`, so a record carrying a primary value and no central
    # skips it just as completely. A check whose condition is narrower than the skip it is
    # detecting reports most of the hole as clean, which is the failure it exists to close.
    # ---- A TWO-SIDED ANSWER IS HELD BRANCH-WISE [added 06-09-2026]. The clause
    # above was firing on work that was right: a study whose answer turns on a
    # contested judgement publishes BOTH framings and is forbidden to average
    # them, so it has no scalar central and demanding one demands the midpoint
    # the dual-framing rule prohibits. Re-pointed per [R-COC-01], and the test
    # is harder than the one it replaces rather than looser.
    #
    # THE SPLIT IS FORCED BY WHAT EACH INSTRUMENT CAN SEE. assert_lens_design()
    # receives the RECORD and so tests the record's own shape — two_sided implies
    # branches, distinct, labelled, no scalar beside them. Only this gate holds
    # the DOCUMENT, so only this gate can ask the question that matters: are the
    # branches the record declares the branches the study actually publishes?
    _pub_ts = (doc.get("central_two_sided") or {}).get("branches")
    _pub_vals = sorted(round(float(b["value"]), 9) for b in (_pub_ts or [])
                       if isinstance((b or {}).get("value"), (int, float)))
    if out.get("two_sided"):
        _rec_vals = sorted(round(v, 9) for v in out.get("branches") or [])
        if not _pub_vals:
            return ("fail", "the record declares a two-sided primary and the study "
                            "publishes no two-sided answer for it to describe")
        if _rec_vals != _pub_vals:
            return ("fail", "the record's branches %s are not the branches the study "
                            "publishes %s. THE IDENTITY CLAUSE, BRANCH-WISE: each answer a "
                            "reader is given is a lens read, and a branch nothing produced "
                            "is the blend arriving one framing at a time."
                            % (_rec_vals, _pub_vals))
        return "ok", "two-sided primary %s, branches %s, %d cross-checks" % (
            out["primary"], _rec_vals, len(out["cross_checks"]))
    if _pub_vals:
        return ("fail", "the study publishes a TWO-SIDED answer (%s) and its lens record "
                        "declares a single-sided primary. The record understates the answer "
                        "the study gives, and everything downstream reads the one branch it "
                        "names." % _pub_vals)
    _c = rec.get("central")
    if _c is None:
        return ("no_central",
                "record present and everything testable passes, but it exposes NO CENTRAL, "
                "so THE IDENTITY CLAUSE NEVER RAN — the one clause that catches a weighted "
                "blend")
    return "ok", "primary %s, %d cross-checks" % (out["primary"], len(out["cross_checks"]))


def main():
    prune = "--prune" in sys.argv
    if not os.path.exists(OUTSTANDING_FILE):
        print("FAIL — the ratchet list %s does not exist."
              % os.path.relpath(OUTSTANDING_FILE, ROOT))
        return 1
    out = json.load(open(OUTSTANDING_FILE, encoding="utf-8"))
    known = set(out["outstanding"])

    sdirs = studies()
    if not sdirs:
        print("FAIL — examined zero studies. An empty result is not a clean result "
              "[R-ENF-04].")
        return 1
    on_disk = {ticker_of(d) for d in sdirs}
    missing = sorted(known - on_disk)
    if missing:
        print("FAIL — the outstanding list names studies that do not exist on disk: %s"
              % ", ".join(missing))
        return 1

    # the registry itself must still agree with the lessons register's classes
    try:
        import research_protocol as RP   # noqa: F401  (the import runs the check)
    except AssertionError as e:
        print("FAIL — %s" % e)
        return 1

    ok, fixed, still, hard = [], [], [], []
    for d in sdirs:
        tk = ticker_of(d)
        state, detail = audit(d)
        listed = tk in known
        if state == "ok":
            (fixed if listed else ok).append((tk, detail))
        else:
            (still if listed else hard).append((tk, detail))

    _untested = [t for t, d in still + hard if d.startswith("record present and")]
    print("studies examined: %d   conforming AND held to the identity clause: %d   "
          "outstanding (allowed): %d" % (len(sdirs), len(ok) + len(fixed), len(still)))
    if _untested:
        print("   of the outstanding, %d carry a record whose identity clause could not "
              "run: %s" % (len(_untested), ", ".join(sorted(_untested))))
    for tk, detail in sorted(ok):
        print("   %-12s %s" % (tk, detail))
    if fixed:
        print("\nNOW PASSING — remove from the outstanding list (%d):" % len(fixed))
        for tk, detail in fixed:
            print("   %-12s %s" % (tk, detail))
    if still:
        print("\nstill outstanding, allowed for now (%d):" % len(still))
        for tk, detail in still[:40]:
            print("   %-12s %s" % (tk, detail[:150]))
    if hard:
        print("\nFAIL — not on the outstanding list and not conforming (%d):" % len(hard))
        for tk, detail in hard:
            print("   %-12s %s" % (tk, detail[:400]))

    if prune:
        out["outstanding"] = sorted(known - {tk for tk, _ in fixed})
        json.dump(out, open(OUTSTANDING_FILE, "w", encoding="utf-8"), indent=1)
        print("\npruned — now %d entries" % len(out["outstanding"]))
        return 0
    if hard:
        return 1
    print("\nOK — no new violations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
