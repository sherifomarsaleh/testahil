#!/usr/bin/env python3
"""The fair-value vintage archive is CURRENT with what the site actually carries.

WHY. `assets/data.js` holds one undated `fair{}` per name. The archive exists so
that "what did we say this was worth in March, and against what price?" has an
answer that does not require excavating git history. An archive that stops being
fed answers that question with a stale number and says nothing about it — and
this session has now found the same failure shape three times in three different
places: a gap review green-lighted against a superseded answer, a study's own
gates opening a superseded workbook, and the fair-value register reporting [ok]
while it sat two editions behind. Every one of them checked that an artefact
EXISTED. None checked that it was CURRENT.

WHAT IT CHECKS
  1. every name in the site's own TICKERS that carries a fair value has a vintage
  2. that name's LATEST vintage equals what data.js publishes today
  3. the archive was rebuilt from a real history, not an empty walk [R-ENF-04]

THE POPULATION IS COUNTED SOMEWHERE ELSE. The names come from data.js loaded
through node — the object the page actually renders, not a regex over it
[R-ENF-03] — so an archive that quietly lost half its names fails rather than
reporting on the half it kept.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine", "valuation_calibration"))

import fv_vintages as V  # noqa: E402


def main(argv):
    rebuild = "--rebuild" in argv
    if rebuild:
        # REFUSE to rebuild from a shallow clone. A rebuild REPLACES the
        # reconstructed half, and a one-commit checkout would replace three months
        # of recovered vintages with one — silently, and with a file that looks
        # exactly as authoritative afterwards. CI checks out at depth 1, so this
        # is not a hypothetical.
        if os.path.exists(os.path.join(ROOT, ".git", "shallow")):
            print("REFUSED — this is a shallow clone, and rebuilding would replace "
                  "the archive with whatever short history it can see. Deepen the "
                  "clone (git fetch --unshallow) or run the gate without "
                  "--rebuild; the check itself needs no history.")
            return 1
        V.build()

    data_js = os.path.join(ROOT, V.DATA_JS)
    if not os.path.exists(data_js):
        print("FAIL — %s does not exist. An absent file is not a clean file."
              % V.DATA_JS)
        return 1
    live = V.parse_data_js(open(data_js, encoding="utf-8").read())
    if live.get("error"):
        print("FAIL — could not load %s: %s" % (V.DATA_JS, live["error"]))
        return 1
    published = live.get("tickers") or {}
    if not published:
        print("FAIL — loaded %d names from %s and NONE carried a fair value. An "
              "empty result is not a clean result [R-ENF-04]."
              % (live.get("total", 0), V.DATA_JS))
        return 1

    if not os.path.exists(V.ARCHIVE):
        print("FAIL — %s does not exist. Run "
              "`python3 engine/valuation_calibration/fv_vintages.py build`."
              % os.path.relpath(V.ARCHIVE, ROOT))
        return 1
    arch = V.load()
    recon = arch.get("reconstruction") or {}
    if not recon.get("revisions_walked"):
        print("FAIL — the archive records no reconstruction. It was either never "
              "built or built from an empty walk, and the two are indistinguishable "
              "from the file alone, which is why the count is stored.")
        return 1

    missing, stale = [], []
    for name, rec in sorted(published.items()):
        entries = arch.get("series", {}).get(name) or []
        if not entries:
            missing.append(name)
            continue
        latest = entries[-1]["fair"]
        now = rec["fair"]
        if any(round(float(latest.get(k, 0)), 4) != round(float(now.get(k, 0)), 4)
               for k in ("bear", "base", "full")):
            stale.append((name, latest, now))

    print("names published with a fair value: %d   vintages held: %d   "
          "reconstruction: %d revisions of %s on %s, %s to %s"
          % (len(published), sum(len(v) for v in arch.get("series", {}).values()),
             recon.get("revisions_walked"), V.DATA_JS, recon.get("ref"),
             recon.get("earliest"), recon.get("latest")))
    if recon.get("shallow_clone"):
        print("  NOTE — built from a SHALLOW clone, so the archive reaches back "
              "only as far as the clone did. Not a failure; a stated limit.")

    if missing:
        print("\nFAIL — published with a fair value and no vintage recorded (%d):"
              % len(missing))
        for n in missing[:20]:
            print("   %s" % n)
    if stale:
        print("\nFAIL — the archive's latest vintage disagrees with what the site "
              "publishes today (%d):" % len(stale))
        for n, was, now in stale[:20]:
            print("   %-12s archive %s / %s / %s   site %s / %s / %s"
                  % (n, was.get("bear"), was.get("base"), was.get("full"),
                     now.get("bear"), now.get("base"), now.get("full")))
        print("\nThe archive is BEHIND the site. Rebuild it in the same pass as any "
              "change to data.js — a record that states a fact which moves must not "
              "be the thing that remembers it.")
    if missing or stale:
        return 1
    print("\nOK — every published fair value has a vintage and the latest one "
          "matches what the site carries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
