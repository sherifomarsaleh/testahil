#!/usr/bin/env python3
"""[R-CAL-02] Rewrite the calibration clause in every coverage.js thesis.

The coverage index carried a one-line skill verdict per name -- "the calibration
is PARITY, not skill", "a ROBUST FAIL", "TIES its calibration back-test" -- in
twenty-odd hand-written forms, each with its own frozen statistics. Those are the
wrong object for a reader (see engine/band_record.py) and they were drifting: the
figures beside them were typed once and never revisited.

This replaces each such sentence with ONE generated sentence carrying the name's
live band record. Where a thesis explained a genuine mechanism -- thin trading,
an explained flat -- that clause is on the ticker page, which has room for it;
the index line is one sentence and the record is the sentence worth having.

Run:  python3 scripts/build_band_theses.py --write
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import band_record as br  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COVERAGE = os.path.join(ROOT, "assets", "coverage.js")

# A sentence in a thesis is a calibration sentence if it carries any of these.
VERDICT = re.compile(
    r"PARITY|CRPS|matches benchmark|failed calibration|ROBUST FAIL|BOUNDARY"
    r"|calibration gate|calibration back-?test|carry-anchored random walk"
    r"|ties,? not beats|TIES its|ILLUSTRATIVE ONLY|illustrative only"
    r"|no skill is claimed|skill-validated|single-name edge|the part that passes"
    r"|classification technicality|over-cover|OVER-COVERED|five-year (?:back-test|requirement)"
    r"|panel-validated|bootstrap|straddles zero|PIT\b", re.I)
# The Arabic thesis carries the same claim in Arabic.
VERDICT_AR = re.compile(r"مونت كارلو|المعايرة|CRPS")
# The clause THIS script emits, so a later run refreshes it instead of appending
# a second one. Without it the theses would migrate once and then freeze — the
# staleness this whole change exists to stop, one file over.
BAND_CLAUSE = re.compile(r"§3 (?:Over \d+ resolved|Only \d+ three-month)")
BAND_CLAUSE_AR = re.compile(r"§3 (?:عبر|لم يُغلق)")

# coverage.js keys the Korean names by exchange code where the ledger uses a
# name. Resolved through the registry's own ticker->market scan, not a second
# hand-written table.
CODE_ALIAS = {"005930": ("KR", "SAMSUNG"), "035720": ("KR", "KAKAO"),
              "373220": ("KR", "LGES")}


def sentence(r, arabic=False):
    """One "§3 ..." clause, rendered by band_record so every surface agrees."""
    return "§3 " + r.record_clause(inner_bands=False, arabic=arabic,
                                    one_sentence=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    src = open(COVERAGE, encoding="utf-8").read()
    records = br.by_key()

    # Operate ONLY on the contents of each thesis string literal. The first cut of
    # this script sliced entries by "next {tk:" and rejoined sentences, which ate
    # the closing '"},' of any entry whose LAST sentence was a calibration one and
    # left the file unparseable. A thesis is a JS string; scan it as one.
    out, skipped = [], []
    for m in re.finditer(r'\{tk:"([A-Za-z0-9]+)"', src):
        tk = m.group(1)
        nxt = src.find('{tk:"', m.end())
        entry_end = nxt if nxt > 0 else len(src)
        # The standard escaped-string-literal pattern, not a character walk: a
        # thesis is a JS double-quoted string and this is the shape of one.
        tm = re.search(r'thesis:"((?:[^"\\]|\\.)*)"', src[m.start():entry_end])
        if not tm:
            continue
        i = m.start() + tm.start(1)
        j = m.start() + tm.end(1)
        body = src[i:j]
        try:
            r = records[CODE_ALIAS[tk]] if tk in CODE_ALIAS else br.resolve(tk, records)
        except KeyError:
            skipped.append(tk)
            continue
        arabic = bool(re.search(r'[؀-ۿ]|\\u06|\\u064', body))
        pat = VERDICT_AR if arabic else VERDICT
        emitted = BAND_CLAUSE_AR if arabic else BAND_CLAUSE
        parts = re.split(r'(?<=[.!?۔])\s+', body)
        hits = [k for k, p in enumerate(parts)
                if pat.search(p) or emitted.search(p)]
        if not hits:
            continue
        keep = []
        for k, p in enumerate(parts):
            if k == hits[0]:
                keep.append(sentence(r, arabic))
            elif k in hits:
                continue
            else:
                keep.append(p)
        new_body = " ".join(keep).strip()
        if '"' in new_body.replace('\\"', ''):
            raise AssertionError(f"{tk}: generated thesis would break the literal")
        if new_body != body:
            out.append((i, j, new_body))
            print(f"  {tk:12s} {r.strength}{', ' + r.flag if r.flag else ''}"
                  f"  ({len(hits)} sentence{'s' if len(hits) != 1 else ''} removed)")

    res = []
    last = 0
    for s0, e0, txt in out:
        res.append(src[last:s0]); res.append(txt); last = e0
    res.append(src[last:])
    new = "".join(res)
    br.assert_no_verdict_tokens(
        "\n".join(re.findall(r'thesis:"[^"]*"', new)), "coverage.js theses")
    print(f"{len(out)} thesis clause(s) rewritten"
          + (f"; no panel for {skipped}" if skipped else ""))
    if a.write:
        open(COVERAGE, "w", encoding="utf-8").write(new)
        print(f"wrote {COVERAGE}")
    else:
        print("(dry run)")


if __name__ == "__main__":
    main()
