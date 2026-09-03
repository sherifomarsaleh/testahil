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
runs research_protocol.assert_bridge() over it. Population anchored per
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
