"""THE ENTERPRISE-TO-EQUITY BRIDGE, CHECKED FROM OUTSIDE THE STUDY.

[R-BRIDGE-01], enforced per [R-ENF-01]. Four defects, all of which shipped, and
none of which any existing gate could see — every one of them was inside a
study's own arithmetic, which recalculated perfectly:

  A STALE BALANCE SHEET. PHDC's bridge stood on 31-Dec-2025 while a reviewed
  31-Mar-2026 sheet sat on the company's own archive, in the same document set
  the study had already used for its first-quarter income figures.

  THE MINORITY AT BOOK, OR NOT AT ALL. The model capitalises all of the
  subsidiaries' cash flow, so the minority's claim is worth its share of that
  value. CLHO deducted book; PHDC deducted nothing while dividing by parent
  shares.

  THE CASH CHARGED TWICE. AMOC discounted operations at a net-debt-weighted rate
  — which on a net-cash company levers the equity weight above one — and then
  added the same cash back at face.

  A BRIDGE THAT DID NOT FOOT. Nobody was adding the lines up outside the model
  that produced them.

The gate reads each study's own committed numbers file for a `bridge_record` and
runs research_protocol.assert_bridge() over it.

OR FOR A DECLARATION, WHERE THE STUDY OWES NO BRIDGE [R-BRIDGE-01 CLAUSE FIVE,
AMENDED 13-Sep-2026, per instruction]. All four defects above are about a number
that exists only when a study values the WHOLE FIRM and walks down to the
shareholder. ADIB is the book's first bank: all seven of its lenses produce a
figure per share directly off equity, there is no enterprise value anywhere in
the study, and this gate refused it for carrying no bridge record. The remedy is
NOT an exemption by name -- a list of skipped tickers skips whatever is written
into it, silently -- but a DECLARATION on calibration_only.declared()'s pattern:
SILENCE IS NOT A DECLARATION, IN EITHER DIRECTION. A study that values on equity
directly commits `equity_direct_declaration`, names the lenses that do it, and
still carries the balance-sheet date, the register that establishes what the
LATEST disclosed sheet is, and the arithmetic that equity over shares reaches the
published per-share figure. A study that declares it and carries an enterprise
value anywhere in its own committed numbers STILL FAILS. Population anchored per
[R-ENF-04]: every ticker in the ratchet list must resolve to a directory on
disk, and a run that examined zero studies FAILS. Ratcheted per [R-ENF-02]:
studies predating the standard are listed and allowed to fail, and the list may
only ever get SHORTER.

    python3 scripts/check_bridge.py
    python3 scripts/check_bridge.py --prune
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE)

OUTSTANDING_FILE = os.path.join(ENGINE, "build_depth_audit", "bridge_outstanding.json")
RECORD_KEYS = ("bridge_record", "bridge_standard")
DECLARATION_KEYS = ("equity_direct_declaration", "equity_direct")


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


def find_declaration(doc):
    """The no-bridge declaration, or None. Read exactly like the record it replaces,
    so a study cannot be declared by accident or by a gate's own default."""
    for k in DECLARATION_KEYS:
        if isinstance(doc.get(k), dict):
            return doc[k]
    meta = doc.get("meta")
    if isinstance(meta, dict):
        for k in DECLARATION_KEYS:
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
    decl = find_declaration(doc)
    if rec is not None and decl is not None:
        return "fail", ("commits BOTH a bridge record and a declaration that it builds no "
                        "bridge. One of the two is wrong and neither is skippable.")
    if decl is not None:
        try:
            RP.assert_equity_direct(decl, ticker=tk, document=doc)
        except AssertionError as e:
            return "fail", str(e).replace("\n", " ")
        except Exception as e:                               # noqa: BLE001
            return "fail", "%s: %s" % (type(e).__name__, e)
        return "declared", ("no enterprise value at any point: %d lenses reach equity per "
                            "share directly, primary %s; stands on the %s sheet; %s over %s "
                            "shares = %s"
                            % (len(decl.get("lenses") or []), decl.get("primary_lens"),
                               decl.get("balance_sheet_date"), decl.get("equity_value"),
                               decl.get("shares_mn"), decl.get("per_share")))
    if rec is None:
        return "no_record", "carries no bridge record"
    try:
        RP.assert_bridge(rec, ticker=tk)
    except AssertionError as e:
        return "fail", str(e).replace("\n", " ")
    except Exception as e:                                   # noqa: BLE001
        return "fail", "%s: %s" % (type(e).__name__, e)
    return "ok", ("stands on the %s sheet; minority on the %s basis"
                  % (rec.get("balance_sheet_date"), (rec.get("nci") or {}).get("basis")))


def main():
    prune = "--prune" in sys.argv
    if not os.path.exists(OUTSTANDING_FILE):
        print("FAIL — the ratchet list %s does not exist. A gate with no population to "
              "hold itself against reports clean by examining nothing."
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

    ok, fixed, still, hard, declared = [], [], [], [], []
    for d in sdirs:
        tk = ticker_of(d)
        state, detail = audit(d)
        listed = tk in known
        if state in ("ok", "declared"):
            if state == "declared":
                declared.append((tk, detail))
            (fixed if listed else ok).append((tk, detail))
        else:
            (still if listed else hard).append((tk, detail))

    print("studies examined: %d   conforming: %d   of which declared no bridge: %d   "
          "outstanding (allowed): %d"
          % (len(sdirs), len(ok) + len(fixed), len(declared), len(still)))
    # the declared studies get their OWN block below rather than being listed twice:
    # one fact printed in two places is a reader counting it twice
    _decl = {tk for tk, _ in declared}
    for tk, detail in sorted(ok):
        if tk not in _decl:
            print("   %-12s %s" % (tk, detail))
    # PRINTED SEPARATELY AND ALWAYS, whether or not anything fired. A study that owes
    # no bridge is a different fact from one whose bridge passes, and a reader who
    # cannot tell them apart is reading a count with no denominator [R-ENF-04].
    if declared:
        print("\nDECLARED NO BRIDGE [R-BRIDGE-01 CLAUSE FIVE] (%d) — held to the sheet, the "
              "register and the arithmetic, and to carrying no enterprise value anywhere:"
              % len(declared))
        for tk, detail in sorted(declared):
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
