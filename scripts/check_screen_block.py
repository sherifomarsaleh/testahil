"""The committed SCREEN block must be what its own readers produce NOW.

Same posture as the PRICES gate beside it. The funnel reads prices, libraries,
band records and study state, all of which move on their own, and prices move by
hand roughly monthly — so a block a few rows behind its readers is the ordinary
state here, not a defect, and failing on it would be a check red by design.

DRIFT IS REPORTED. What FAILS is a defect: no block, a covered name the readers
classify that the block does not carry, or a run that examined nothing
[R-ENF-04]. The population is counted off TICKERS, not off the block.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_screen_block as B                                    # noqa: E402


def committed():
    out = subprocess.run(
        ["node", "-e",
         "const fs=require('fs'),vm=require('vm');"
         "let s=fs.readFileSync(process.argv[1],'utf8');"
         "s+='\\n;globalThis.__S=(typeof SCREEN!==\"undefined\")?SCREEN:null;"
         "globalThis.__T=TICKERS;';const c={window:{}};"
         "vm.createContext(c);vm.runInContext(s,c);"
         "console.log(JSON.stringify({s:c.__S,n:Object.keys(c.__T).length}));",
         B.DATA_JS], capture_output=True, text=True, check=True)
    d = json.loads(out.stdout)
    return d["s"], d["n"]


def main():
    have, total = committed()
    if have is None:
        raise SystemExit("FAIL: assets/data.js carries no SCREEN block. Run "
                         "python3 scripts/build_screen_block.py")
    want = B.build()
    if not want:
        raise SystemExit("FAIL: the readers classified zero names [R-ENF-04].")

    bad, drift = [], []
    for k, w in sorted(want.items()):
        h = have.get(k)
        if not h:
            bad.append("%s: classified by the readers, missing from the block" % k)
            continue
        for f in ("stop", "pxDate", "lib", "trend", "rebuilt"):
            if (h.get(f) if h.get(f) is not None else None) != (w.get(f) if w.get(f) is not None else None):
                drift.append("%s.%s: block %r vs readers %r" % (k, f, h.get(f), w.get(f)))
        for f in ("gap", "z", "px"):
            a, b2 = h.get(f), w.get(f)
            if (a is None) != (b2 is None) or (a is not None and abs(a - b2) > 1e-6):
                drift.append("%s.%s: block %r vs readers %r" % (k, f, a, b2))
    for k in have:
        if k not in want:
            bad.append("%s: in the block, the readers do not classify it" % k)

    print("SCREEN gate — examined %d covered names against %d committed rows"
          % (total, len(have)))
    tally = {}
    for r in have.values():
        s = r.get("stop") or "clears"
        tally[s] = tally.get(s, 0) + 1
    print("  " + " · ".join("%s %d" % (k, v) for k, v in sorted(tally.items())))
    if drift:
        print("  ADVISORY — %d field(s) have moved since the block was built; the "
              "next refresh pass folds them in" % len(drift))
        for d in drift[:8]:
            print("    " + d)
        if len(drift) > 8:
            print("    ... and %d more" % (len(drift) - 8))
    if bad:
        print("\nFAIL — the block is defective:")
        for b3 in bad[:40]:
            print("  " + b3)
        if len(bad) > 40:
            print("  ... and %d more" % (len(bad) - 40))
        raise SystemExit("Run python3 scripts/build_screen_block.py")
    print("  OK — %d names classified" % len(have))


if __name__ == "__main__":
    main()
