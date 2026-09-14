#!/usr/bin/env python3
"""[R-GAP-02 CLAUSE SIX] A filed dissent must be REACHABLE FROM THE TICKER PAGE.

WHY THIS EXISTS, measured rather than imagined. SWDY published on 14-09-2026 at a
fair value 35.4% below the market price. [R-GAP-02] had done its work: the study was
held until MARKET_DISSENT_14-09-2026.md was written, and the principal authorised the
publication on the strength of it. Then the page went live carrying the number and
NOTHING pointing at the case for it. A reader on testahil.com saw 87.94 against a
market at 136.20 and no argument. The document was public in the repository and
unreachable from the one page anybody opens.

THE RULE THE DESK STATES IS "where we disagree with the market, we must PUBLISH a
written case for the difference". Writing it and filing it is not publishing it. A
case the reader cannot reach is a case made to ourselves, and the gate that made us
write it was satisfied either way — which is exactly how a control comes to certify
something it never checked.

WHAT THIS CHECKS. For every study directory carrying a MARKET_DISSENT_*.md:

  1. the ticker's data.js entry carries a `dissent` key,
  2. that key points at a file that EXISTS on disk,
  3. the stamp in that filename matches the LATEST dissent filed, so a re-argued
     case at a new gap cannot leave last week's PDF on the page.

It says nothing about names with no dissent, which is most of them: a study inside
the publication limit owes no case and is not held to one.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data.js")


def entries() -> dict:
    """{TICKER: files-dict} read out of data.js without executing it.

    A TICKER APPEARS AT THIS INDENT IN MORE THAN ONE SECTION of data.js — the
    TICKERS map carries the files block, and the ledger and band-record sections
    carry the same name with no files at all. A plain assignment lets the later,
    empty match overwrite the real one, and the gate then reports every published
    dissent as missing. It did exactly that on the first run. A populated entry is
    never replaced by an empty one.
    """
    raw = open(DATA, encoding="utf-8").read()
    out: dict[str, dict] = {}
    for m in re.finditer(r"\n  ([A-Z0-9_]+)\s*:\s*\{", raw):
        tk = m.group(1)
        seg = raw[m.end():m.end() + 12000]
        f = re.search(r"files\s*:\s*\{(.*?)\}", seg, re.S)
        files = dict(re.findall(r"(\w+)\s*:\s*\"([^\"]+)\"", f.group(1))) if f else {}
        if files or tk not in out:
            out[tk] = files if files else out.get(tk, {})
    return out


def main() -> int:
    found = entries()
    bad, checked = [], 0

    for sdir in sorted(glob.glob(os.path.join(ROOT, "engine", "*_study"))):
        hits = sorted(glob.glob(os.path.join(sdir, "MARKET_DISSENT_*.md")))
        if not hits:
            continue
        tk = os.path.basename(sdir)[:-len("_study")].upper()
        checked += 1
        latest = os.path.basename(hits[-1])
        stamp = re.search(r"(\d{2}-\d{2}-\d{4})", latest)

        files = found.get(tk)
        if files is None:
            bad.append(f"{tk}: filed {latest} but the name is not in data.js at all")
            continue
        ref = files.get("dissent")
        if not ref:
            bad.append(f"{tk}: filed {latest} and its page carries NO dissent link — "
                       f"the case was written and never published [R-GAP-02 CLAUSE SIX]")
            continue
        path = os.path.join(ROOT, ref.split("?")[0])
        if not os.path.exists(path):
            bad.append(f"{tk}: page points at {ref.split('?')[0]}, which is not on disk")
            continue
        if stamp and stamp.group(1) not in ref:
            bad.append(f"{tk}: page carries {os.path.basename(ref.split('?')[0])} but the "
                       f"latest filed case is {latest} — a re-argued case left the old "
                       f"one facing the reader")

    print("[R-GAP-02 CLAUSE SIX] a filed dissent is reachable from its ticker page")
    print(f"  studies carrying a dissent : {checked}")
    print(f"  published to the reader    : {checked - len(bad)}")

    if not checked:
        # Not a pass. Nothing was examined, and an empty examination reads exactly
        # like a clean one unless it says so [R-ENF-04].
        print("\n  no study carries a MARKET_DISSENT — nothing to check, nothing proven")
        return 0
    if bad:
        print(f"\nFAIL — {len(bad)} filed case(s) the reader cannot reach:")
        for b in bad:
            print(f"  {b}")
        print("\n  Build it with scripts/build_dissent_docx.py TICKER and give the "
              "ticker's files block a dissent key.")
        return 1
    print("\nOK — every filed case is on the page that carries the number it argues for.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
