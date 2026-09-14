#!/usr/bin/env python3
"""[R-LENS-03] read off the PAGE A READER OPENS, not off the document or the record.

WHY THIS EXISTS, AND IT IS [R-GAP-03]'s LESSON ARRIVING ONE ARTEFACT OVER.
[R-LENS-03] retired the typed multi-lens blend on 02-09-2026: one class primary IS the
central, every other lens is a cross-check published beside it, never averaged into the
answer. Three instruments enforce that today and all three take a STUDY as their subject:
check_lens_design.py reads each study's committed lens_record, check_lens_independence.py
reads its builders, and check_lens_vocabulary.py reads its delivered PDF and workbook.

A READER OPENS NONE OF THOSE. A reader opens a page on the site.

MEASURED 07-09-2026 by running check_lens_vocabulary's OWN pattern over the pages:

    93 study pages published          93 assert the retired blend        299 assertions

EVERY PAGE IN THE BOOK, five days after the architecture was retired. Not a straggler and
not a naming slip: the fan caption on all 93 renders `", weighted central "+fmtPx(f.base)`
from one shared template line, 43 pages tell the reader the site publishes "a weighted
central fair value", 38 say in terms that the lenses are "blended into one weighted central
fair value", and individual pages carry a bold table row reading "Weighted central fair
value" above the number itself.

WHY EVERY EXISTING GATE WAS BLIND is a property of those gates rather than an oversight in
them. check_lens_vocabulary globs `engine/*_study` — the right subject for the question it
asks, and 22 of the 90 published names have such a directory, so it is silent about the
other 68 by construction rather than passing them. check_page_integrity reads these very
pages and tolerates the row, because what it tests is that the FIGURE agrees with data.js,
which it does. THE NUMBER WAS CHECKED AND THE CLAIM ABOUT WHERE IT CAME FROM WAS NOT.

WHAT IT DOES NOT DO, AND THIS IS THE HALF THAT KEEPS IT HONEST. It does not assert that any
published figure IS a blend. Most of these pages have no committed lens record at all, so
what the arithmetic behind them was cannot be read from here and this gate does not pretend
to — that is check_lens_design's question and it needs a record. What is wrong on the page
is narrower and certain: the page NAMES a construction this house retired, and it names it
to the only person the whole apparatus exists for. A page that says nothing about how the
central was reached is not flagged; a page that describes the retirement is not flagged
either, on the same sentence-window discount the document gate uses.

THE INSTRUMENT IS IMPORTED, NEVER RE-IMPLEMENTED [R-ENF-03]. BLEND, RETIRED, SENT, WINDOW
and scan_text come from check_lens_vocabulary. That pattern has been re-pointed twice on
real documents — once for a table row whose layout splits the label around its own figures,
once because it knew only the American spelling of the noun — and two readers of one rule
drift into two notions of what the rule says the moment a third copy exists.

RATCHET [R-ENF-02], AND ITS ENTRIES CARRY A COUNT [R-ENF-08]. A page listed here is excused
for the assertions it was measured carrying; a page that acquires MORE goes red, because
the failure message of this gate never changes shape and a fingerprint alone would excuse
any amount of new text. The list may only ever SHORTEN.

POPULATION ANCHORED [R-ENF-04] BOTH WAYS: a run finding zero pages FAILS, and so does a run
that READ zero of them — a matcher that stopped matching reads exactly like a clean book.

EXCLUDED from the new-study gauntlet with its reason: its subject is the SITE, and a study
directory planted in a sandbox publishes no page. The same disposition as the other
site-subject gates.

USAGE
    python3 scripts/check_published_lens_vocabulary.py            # gate
    python3 scripts/check_published_lens_vocabulary.py --prune    # rewrite the ratchet SHORTER
"""
from __future__ import annotations

import glob
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTSTANDING = os.path.join(ROOT, "engine", "build_depth_audit",
                           "published_lens_outstanding.json")


def _instrument():
    """check_lens_vocabulary's own patterns and window logic — imported, not copied."""
    path = os.path.join(ROOT, "scripts", "check_lens_vocabulary.py")
    spec = importlib.util.spec_from_file_location("_clv", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pages(root=ROOT):
    """The reader-facing surfaces that carry a fair value.

    The ticker study pages, which is what a reader actually opens, plus the coverage
    file behind the stocks grid. `legacy/` is excluded BY DIRECTORY NAME rather than by
    substring — the exclusion that dropped .github by matching '/.git' was the same
    mistake, and an absent answer reads exactly like a clean one [R-ENF-04].
    """
    out = []
    for p in sorted(glob.glob(os.path.join(root, "*", "study", "index.html"))):
        rel = os.path.relpath(p, root)
        if rel.split(os.sep)[0] in ("legacy", "engine", "node_modules"):
            continue
        out.append(rel)
    cov = os.path.join(root, "assets", "coverage.js")
    if os.path.exists(cov):
        out.append(os.path.relpath(cov, root))
    return out


def load_outstanding():
    if not os.path.exists(OUTSTANDING):
        return {}
    try:
        return json.load(open(OUTSTANDING, encoding="utf-8")).get("outstanding", {})
    except Exception:
        return {}


def measure(root=ROOT):
    """{page: (asserting_hits, explained)} over every reader-facing surface."""
    clv = _instrument()
    found = {}
    for rel in pages(root):
        try:
            t = open(os.path.join(root, rel), encoding="utf-8", errors="replace").read()
        except OSError as exc:
            found[rel] = ([f"UNREADABLE: {exc}"], 0)
            continue
        found[rel] = clv.scan_text(t)
    return found


def main(argv):
    prune = "--prune" in argv
    surfaces = pages()
    if not surfaces:
        print("FAIL — examined ZERO reader-facing pages. A run that read nothing is not a "
              "run that found nothing [R-ENF-04].")
        return 1

    found = measure()
    if not found:
        print("FAIL — %d surfaces on disk and ZERO read." % len(surfaces))
        return 1

    outstanding = load_outstanding()
    breaches, worse, clean = [], [], []
    for rel in surfaces:
        asserting, _explained = found.get(rel, ([], 0))
        n = len(asserting)
        if n == 0:
            clean.append(rel)
            continue
        entry = outstanding.get(rel)
        if entry is None:
            breaches.append((rel, n, asserting[0]))
            continue
        rec = entry.get("assertions")
        if isinstance(rec, int) and n > rec:
            worse.append((rel, rec, n, asserting[0]))

    if prune:
        keep = {}
        for rel in surfaces:
            asserting, _ = found.get(rel, ([], 0))
            if not asserting:
                continue
            old = outstanding.get(rel, {})
            keep[rel] = {
                "assertions": len(asserting),
                "reason": old.get("reason",
                                  "publishes the retired weighted blend as the account of "
                                  "its own central [R-LENS-03]"),
                "example": asserting[0][:180],
            }
        dropped = sorted(set(outstanding) - set(keep))
        json.dump({"rule": "R-LENS-03 on the published page",
                   "note": "May only ever SHORTEN. An entry excuses the assertions it "
                           "records; more is a NEW breach [R-ENF-08].",
                   "outstanding": keep},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print("pruned: %d listed (was %d); %d came off%s"
              % (len(keep), len(outstanding), len(dropped),
                 (": " + ", ".join(dropped[:8])) if dropped else ""))
        return 0

    print("reader-facing surfaces examined: %d   clean: %d   listed: %d"
          % (len(surfaces), len(clean), len(outstanding)))

    if breaches or worse:
        for rel, n, ex in breaches:
            print("  NEW   %-46s %d assertion(s)  %s" % (rel, n, ex[:90]))
        for rel, rec, n, ex in worse:
            print("  WORSE %-46s excused %d, now %d  %s" % (rel, rec, n, ex[:80]))
        print("\nFAIL — a page tells its reader the central is a weighted blend of lenses, "
              "which [R-LENS-03] retired. The fix is the page's own wording, never the "
              "number behind it.")
        return 1

    print("\nOK — no reader-facing surface newly publishes the retired blend.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
