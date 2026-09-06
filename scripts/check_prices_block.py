"""The committed PRICES block must be what its own readers produce NOW.

WHY A GATE AND NOT A REMINDER. Prices arrive by hand, so the block goes stale by
the calendar the moment a file is added and nobody re-runs the builder — the same
shape as the technical read the 29-July rule closed, and as tech_records.json,
which stores the hash of the technicals.py it graded so a moved read with an
unmoved record goes RED rather than staying a remembered obligation.

WHAT IT REFUSES, all four rather than warns [R-ENF-01]:
  · a block that disagrees with the readers on any name's price, date or source
  · a covered name carrying no priced row where the readers can resolve one
  · a row that is malformed (no price, no date, no source)
  · a run that examined ZERO names, which is an absent answer wearing the costume
    of a clean one [R-ENF-04] — the population is counted off TICKERS in data.js,
    which is not the block being checked

IT DOES NOT CHECK FRESHNESS, DELIBERATELY. How old a price is is a data-supply
fact, disclosed beside every number and never a blocker; a gate nobody in the room
can clear is one everybody learns to ignore. It prints the age distribution as an
ADVISORY, the same posture as the library-staleness sweep.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build_prices_block as B                                    # noqa: E402


def committed():
    out = subprocess.run(
        ["node", "-e",
         "const fs=require('fs'),vm=require('vm');"
         "let s=fs.readFileSync(process.argv[1],'utf8');"
         "s+='\\n;globalThis.__P=(typeof PRICES!==\"undefined\")?PRICES:null;"
         "globalThis.__T=TICKERS;';const c={window:{}};"
         "vm.createContext(c);vm.runInContext(s,c);"
         "console.log(JSON.stringify({p:c.__P,n:Object.keys(c.__T).length}));",
         B.DATA_JS],
        capture_output=True, text=True, check=True)
    d = json.loads(out.stdout)
    return d["p"], d["n"]


def main():
    have, total = committed()
    if have is None:
        raise SystemExit("FAIL: assets/data.js carries no PRICES block. Run "
                         "python3 scripts/build_prices_block.py")
    want, unresolved = B.build()
    if not want:
        raise SystemExit("FAIL: the readers resolved zero prices — an empty "
                         "result is not a clean result [R-ENF-04].")

    bad = []
    for k, w in sorted(want.items()):
        h = have.get(k)
        if not h:
            bad.append("%s: priced by the readers, missing from the block" % k)
            continue
        if abs(float(h.get("px", 0)) - w["px"]) > 1e-6 or h.get("date") != w["date"] \
                or h.get("src") != w["src"]:
            bad.append("%s: block %s@%s (%s) vs readers %s@%s (%s)"
                       % (k, h.get("px"), h.get("date"), h.get("src"),
                          w["px"], w["date"], w["src"]))
    for k, h in sorted(have.items()):
        if k not in want:
            bad.append("%s: in the block, the readers resolve no price for it" % k)
        elif not (h.get("px") and h.get("date") and h.get("src")):
            bad.append("%s: malformed row %r" % (k, h))

    print("PRICES gate — examined %d covered names against %d committed rows"
          % (total, len(have)))
    if unresolved:
        print("  no price resolvable (named, not dropped): %s" % ", ".join(sorted(unresolved)))
    dates = sorted({r["date"] for r in have.values() if r.get("date")})
    if dates:
        print("  ADVISORY — price dates span %s .. %s (age is disclosed, never gated)"
              % (dates[0], dates[-1]))
    if bad:
        print("\nFAIL — the block is not what its readers produce now:")
        for b in bad[:40]:
            print("  " + b)
        if len(bad) > 40:
            print("  ... and %d more" % (len(bad) - 40))
        raise SystemExit("Run python3 scripts/build_prices_block.py in the same "
                         "pass as the price supply that moved them.")
    print("  OK — every row matches, %d names priced" % len(have))


if __name__ == "__main__":
    main()
