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
    return sorted(glob.glob(os.path.join(ENGINE, "*_study")))


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

    print("studies examined: %d   conforming: %d   outstanding (allowed): %d"
          % (len(sdirs), len(ok) + len(fixed), len(still)))
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
