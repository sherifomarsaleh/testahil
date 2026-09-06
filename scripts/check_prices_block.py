"""The committed PRICES block, held to its own readers — advisory on drift.

PRICES ARE ENTERED BY HAND, ROUGHLY MONTHLY, AND THAT IS THE OPERATING MODEL
until a live terminal feed exists. So a block a few rows behind its readers is
the NORMAL state of this repository, not a defect: a library lands, the supply
does not move for weeks, and the two disagree. Failing on that would be a check
red by design — the one everybody learns to ignore — and it fired twice in one
hour on its first day for exactly that reason.

DRIFT IS THEREFORE REPORTED AND NEVER FAILS. What still fails is a real defect:
no block at all, a malformed row, a covered name the readers price and the block
does not carry, or a run that examined nothing [R-ENF-04]. The page prints the
date of every price, so a reader is never misled about how old one is — which is
what makes reporting sufficient here.

WHAT IT REFUSES [R-ENF-01]:
  · no PRICES block at all
  · a covered name the readers can price that the block does not carry
  · a malformed row (no price, no date, no source)
  · a run that examined ZERO names, an absent answer wearing the costume of a
    clean one [R-ENF-04] — the population is counted off TICKERS in data.js,
    which is not the block being checked

WHAT IT ONLY REPORTS: a row whose price, date or source has moved since the block
was built, and how old the prices are. Both are data-supply facts about a manual
monthly process, and the builders now run inside the same pass as the page
refresh, so ordinary drift heals itself without anybody being told off.
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

    bad, drift = [], []
    for k, w in sorted(want.items()):
        h = have.get(k)
        if not h:
            bad.append("%s: priced by the readers, missing from the block" % k)
            continue
        if abs(float(h.get("px", 0)) - w["px"]) > 1e-6 or h.get("date") != w["date"] \
                or h.get("src") != w["src"]:
            drift.append("%s: block %s@%s (%s) vs readers %s@%s (%s)"
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
    if drift:
        print("  ADVISORY — %d row(s) have moved since the block was built; the "
              "next refresh pass folds them in:" % len(drift))
        for d in drift[:10]:
            print("    " + d)
        if len(drift) > 10:
            print("    ... and %d more" % (len(drift) - 10))
    if bad:
        print("\nFAIL — the block is defective:")
        for b in bad[:40]:
            print("  " + b)
        if len(bad) > 40:
            print("  ... and %d more" % (len(bad) - 40))
        raise SystemExit("Run python3 scripts/build_prices_block.py")
    print("  OK — %d names priced%s" % (len(have),
          ", %d row(s) awaiting the next refresh" % len(drift) if drift else ""))


if __name__ == "__main__":
    main()
