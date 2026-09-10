"""THE RE-ISSUE WORK ORDER — what each study owes, read from the ratchets themselves.

WHY THIS EXISTS. Every ratchet in this repository records a debt one gate is willing to
carry, and each is read by that gate alone. Nobody had ever asked the question a re-issue
actually asks: WHAT DOES THIS ONE STUDY OWE, ACROSS ALL OF THEM. A list per gate is the
right shape for a build; a list per study is the right shape for the work.

It is GENERATED from the ratchet files at run time and never typed [R-DOC-02]. A ratchet
may only ever shorten, so this report can only get shorter too — which makes it a measure
of the re-issue rather than a description of it.

THE ENTRY SHAPES DIFFER AND THEY ARE READ, NOT GUESSED. Across the ratchets a debt is
recorded as a bare list of tickers, a dict keyed by ticker, a dict with named groups
(outstanding / unreadable / no_check / failing), a list of file paths, and a dict keyed by
path. A reader that knew one shape would find a fraction and report it as a result —
[L-355], which this repository met four times in one day. Every shape below was read off
the files that exist rather than assumed.

USAGE
    python3 engine/method_reassessment/reissue_work_order.py            # per study
    python3 engine/method_reassessment/reissue_work_order.py --by-gate  # per ratchet
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
AUDIT = os.path.join(ENGINE, "build_depth_audit")

# A path entry names a study by the directory it sits in; a ticker entry names it outright.
PATH_TICKER = re.compile(r"(?:^|/)([A-Za-z0-9]+)_study(?:/|$)")
GROUPS = ("outstanding", "unreadable", "no_check", "failing", "held", "entries",
          "documents", "signature")


def _ticker(x):
    """The study a ratchet entry is about, from whichever shape it is written in."""
    if not isinstance(x, str):
        return None
    m = PATH_TICKER.search(x)
    if m:
        return m.group(1).upper()
    if "/" in x or x.endswith(".html") or x.endswith(".js"):
        return None                        # a site surface, not a study
    return x.upper() if re.fullmatch(r"[A-Za-z0-9]{2,20}", x) else None


def _walk(obj, group, out):
    if isinstance(obj, list):
        for x in obj:
            tk = _ticker(x)
            if tk:
                out.append((tk, group, ""))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            tk = _ticker(k)
            if tk:
                why = ""
                if isinstance(v, str):
                    why = v
                elif isinstance(v, dict):
                    why = str(v.get("reason") or v.get("why") or
                              v.get("detail") or "")
                out.append((tk, group, why))


def read_ratchets(audit=AUDIT):
    """{gate: [(ticker, group, why)]} — every debt on disk, in whatever shape it is kept."""
    found = {}
    for p in sorted(glob.glob(os.path.join(audit, "*outstanding*.json"))):
        name = os.path.basename(p)
        try:
            doc = json.load(open(p, encoding="utf-8"))
        except Exception:
            found[name] = [("(unreadable)", "-", "the ratchet file will not parse")]
            continue
        rows = []
        if isinstance(doc, list):
            _walk(doc, "outstanding", rows)
        elif isinstance(doc, dict):
            hit = False
            for g in GROUPS:
                if g in doc:
                    _walk(doc[g], g, rows)
                    hit = True
            if not hit:
                _walk(doc, "outstanding", rows)
        if rows:
            found[name] = rows
    return found


def by_study(found):
    out = defaultdict(list)
    for gate, rows in found.items():
        for tk, group, why in rows:
            out[tk].append((gate.replace("_outstanding.json", "")
                                .replace(".json", ""), group, why))
    return out


def main(argv):
    found = read_ratchets()
    if not found:
        print("FAIL — read zero ratchets. A reader that stopped matching reads exactly "
              "like a book with no debt [R-ENF-04].")
        return 1

    if "--by-gate" in argv:
        print("THE RE-ISSUE WORK ORDER, by gate")
        for gate in sorted(found):
            print("\n%s  (%d)" % (gate, len(found[gate])))
            for tk, group, _ in sorted(found[gate]):
                print("    %-14s %s" % (tk, group))
        return 0

    studies = by_study(found)
    total = sum(len(v) for v in studies.values())
    print("THE RE-ISSUE WORK ORDER — what each study owes, across every ratchet")
    print("  ratchets read     : %d" % len(found))
    print("  studies with debt : %d" % len(studies))
    print("  entries           : %d" % total)
    print("\n  A ratchet may only ever SHORTEN, so this list can only get shorter. It is")
    print("  the measure of the re-issue, not a description of it.\n")
    for tk in sorted(studies, key=lambda t: (-len(studies[t]), t)):
        rows = studies[tk]
        print("  %-14s %2d  %s" % (tk, len(rows),
                                   ", ".join(sorted({g for g, _, _ in rows}))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
