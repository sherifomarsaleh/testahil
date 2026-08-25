#!/usr/bin/env python3
"""[R-CAL-02] Refresh every ticker page's band-record clause from the panels.

THE SELECTOR IS THE SPAN, not a page list. The first cut of this script carried a
hardcoded PAGES dict and matched the paragraph by its opening word ("Honestly:"),
while the runtime refresher in assets/app.js selected by `[data-band-record]` —
so the two disagreed on day one: platinum.html was listed but had no such
paragraph and was silently skipped (its verdict clause had to be removed by
hand), and agthia/egch/scem carried spans no generator maintained. One selector
now, shared with app.js and with the gate that validates it.

A coverage figure moves the moment a forecast is graded, which is why this is a
generator: riyadhcable.html once claimed "13 non-overlapping three-month windows
have resolved" with "coverage 85% / 92%" against a panel holding 10 at 70% / 90%.

Run:  python3 scripts/build_band_prose.py --write [--only TK]
"""
import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import band_record as br  # noqa: E402

SPAN = re.compile(r'(<span data-band-record="([^"]+)">)(.*?)(</span>)', re.S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    records = br.by_key()
    changed, spans = [], 0

    for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
        src = open(path, encoding="utf-8").read()
        if "data-band-record" not in src:
            continue
        rel = os.path.relpath(path, ROOT)

        def repl(m):
            nonlocal spans
            tk = m.group(2)
            if a.only and a.only != tk:
                return m.group(0)
            spans += 1
            r = br.resolve(tk, records)      # raises on an unknown name
            return m.group(1) + r.record_clause() + m.group(4)

        out = SPAN.sub(repl, src)
        # The span holds ONE self-contained sentence, so the surrounding prose
        # reads the same before and after JS runs. agthia.html briefly held a
        # lowercase mid-sentence fragment that app.js replaced with a capitalised
        # full sentence, rendering "...bands have held: Over 58 ... — see the".
        for m in SPAN.finditer(out):
            body = m.group(3).strip()
            if body and (body[0].islower() or not body.endswith(".")):
                raise AssertionError(
                    f'{rel}: span "{m.group(2)}" must be a standalone sentence — '
                    f'got {body[:60]!r}')
        br.assert_no_verdict_tokens(out, rel)
        if out != src:
            changed.append(rel)
            if a.write:
                open(path, "w", encoding="utf-8").write(out)

    print(f"{spans} span(s) across {len(changed)} changed page(s)"
          f"{': ' + ', '.join(changed) if changed else ''}")
    if not a.write:
        print("(dry run — pass --write)")


if __name__ == "__main__":
    main()
