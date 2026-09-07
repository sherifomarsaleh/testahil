#!/usr/bin/env python3
"""[R-BRIDGE-01] / [R-ANCHOR-01] — THE PROFIT ANCHOR IS NOT OLDER THAN THE SAME STUDY'S
OWN BALANCE SHEET.

WHY THIS EXISTS. [R-BRIDGE-01] requires the bridge to stand on the LATEST DISCLOSED balance
sheet and check_bridge.py enforces it. [R-ANCHOR-01] requires the forecast to be anchored
on the LATEST REVIEWED period and check_forecast_anchor.py enforces that. Each gate reads
its own field, neither reads the other's, AND NOTHING ASKED WHETHER THE TWO AGREE.

They come out of the same filing. A reviewed interim carries a balance sheet and an income
statement between the same covers, so a study standing its bridge on 30 June while
anchoring its margins on the previous 31 December has OPENED THAT FILING AND TAKEN ONLY
HALF OF IT. Nothing about either figure is wrong on its own, which is why both gates pass:
the defect lives in the relationship, and it is the shape [R-MACRO-01 AMENDED 06-09-2026]
names — two rules governing one quantity from different directions, with the JOINT
condition owned by neither.

MEASURED 07-09-2026, four studies anchor their profit behind their own balance sheet:

    ADNOCLS    bridge 2026-03-31   anchor 2025-12-31   one quarter behind (the EXEMPLAR)
    ARCC       bridge 2026-06-30   anchor 2025-12-31   two quarters
    EGCH       bridge 2026-03-31   anchor 2025-06-30   three quarters
    SCEM       bridge 2026-03-31   anchor 2025-12-31   one quarter

THE TEST IS AN ORDERING, NOT A THRESHOLD, for [R-ASSET-01]'s reason: there is no number of
days to argue about, and a study whose two dates are equal — which is most of the book —
passes trivially. What it asks is only that the profit anchor is not BEHIND the sheet.

THE RELEASE IS REAL AND IT IS NOT A FORMALITY. A later balance sheet can legitimately exist
without a comparable income statement — a company filing a balance-sheet-only interim, a
fiscal-year boundary where the P&L for the stub is not on the same basis, an acquisition
restating the sheet mid-period. A study in that position declares
`anchor_ordering_reason` naming the mechanism from the filings. AN EMPTY REASON HAS
SWITCHED THE CHECK OFF RATHER THAN DECLARED IT.

WHAT IT DELIBERATELY DOES NOT DO. It does not ask whether either date is the LATEST the
company has published — nothing in this repository can answer that, since every gate here
compares two fields that both originate inside the study, and an analyst who does not know
a later filing exists writes both dates consistently and wrong. That gap is real, is named
in the census, and needs a filings index rather than a comparison; this gate closes the
half that IS answerable from what a study commits.

RATCHET [R-ENF-02], entries carrying the MEASURED lag so a study falling further behind is
a NEW breach [R-ENF-08]; may only SHORTEN. POPULATION-ANCHORED [R-ENF-04] BOTH WAYS.

USAGE
    python3 scripts/check_anchor_ordering.py            # gate
    python3 scripts/check_anchor_ordering.py --prune    # rewrite the ratchet SHORTER
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit", "anchor_ordering_outstanding.json")

SHEET_KEYS = ("balance_sheet_date", "as_at", "sheet_date", "balance_sheet_as_at")
ANCHOR_KEYS = ("latest_reviewed_date", "latest_reviewed_period", "anchor_date")
DECLARE_KEY = "anchor_ordering_reason"


def _date(s):
    if not isinstance(s, str):
        return None
    try:
        return dt.date.fromisoformat(s.strip()[:10])
    except ValueError:
        return None


def _pick(doc, keys):
    for k in keys:
        d = _date(doc.get(k))
        if d:
            return d, k
    return None, None


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
    """{ticker: (lag_days, why)} for every study whose profit anchor sits behind its sheet."""
    bad, read = {}, 0
    for tk, path in sorted(studies().items()):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        sheet, sk = _pick(doc.get("bridge_record") or {}, SHEET_KEYS)
        anchor, ak = _pick(doc.get("forecast_anchor") or {}, ANCHOR_KEYS)
        if not (sheet and anchor):
            continue                      # a study committing only one is not in scope
        read += 1
        if anchor >= sheet:
            continue
        if (doc.get(DECLARE_KEY) or "").strip():
            continue
        bad[tk] = ((sheet - anchor).days,
                   "the bridge stands on %s %s while the forecast is anchored on %s %s — "
                   "%d days BEHIND its own balance sheet. Both come out of the same "
                   "reviewed filing, so the study opened it and took half of it, and no %s "
                   "declares why" % (sk, sheet, ak, anchor, (sheet - anchor).days,
                                     DECLARE_KEY))
    return bad, read


def main(argv):
    prune = "--prune" in argv
    all_st = studies()
    if not all_st:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1
    bad, read = measure()
    if read == 0:
        print("FAIL — %d study directories on disk and ZERO carry BOTH a balance-sheet "
              "date and a profit anchor. A reader that stopped matching reads exactly like "
              "a book with none [R-ENF-04]." % len(all_st))
        return 1

    known = load()

    if prune:
        keep = {tk: {"lag_days": lag, "why": why,
                     "reason": (known.get(tk) or {}).get(
                         "reason", "measured on adoption day; the fix is to read the income "
                                   "statement out of the filing the bridge already stands on")}
                for tk, (lag, why) in bad.items()}
        dropped = sorted(set(known) - set(keep))
        json.dump({"rule": "R-BRIDGE-01 / R-ANCHOR-01 — the joint condition",
                   "note": "May only SHORTEN. An entry excuses the LAG it records; a study "
                           "falling further behind is a NEW breach [R-ENF-08].",
                   "outstanding": keep},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print("pruned: %d listed (was %d); %d came off%s"
              % (len(keep), len(known), len(dropped),
                 (": " + ", ".join(dropped)) if dropped else ""))
        return 0

    print("[R-BRIDGE-01]/[R-ANCHOR-01] the profit anchor against the study's own sheet")
    print("  study directories examined : %d" % len(all_st))
    print("  carrying both dates        : %d" % read)
    print("  anchored on or after       : %d" % (read - len(bad)))

    new, worse = [], []
    for tk, (lag, why) in sorted(bad.items()):
        e = known.get(tk)
        if e is None:
            new.append((tk, why))
        elif isinstance(e.get("lag_days"), int) and lag > e["lag_days"]:
            worse.append((tk, e["lag_days"], lag))
        print("  %-6s %-12s %s" % ("NEW" if e is None else "known", tk, why))

    rc = 0
    if new:
        print("\nFAIL — %d study/studies anchor profit behind their own balance sheet with "
              "nothing declaring it: %s" % (len(new), ", ".join(t for t, _ in new)))
        rc = 1
    for tk, was, now in worse:
        print("\nFAIL — %s has fallen further behind: %d days excused, %d now [R-ENF-08]."
              % (tk, was, now))
        rc = 1
    if rc:
        return rc
    print("\nOK — no study anchors its profit behind the balance sheet it built its bridge "
          "on, except where the ratchet records it.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
