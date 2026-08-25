#!/usr/bin/env python3
"""Coherence gate for the published technical read, read the way a BROWSER reads it.  [R-ENF-03]

WHY THIS EXISTS
---------------
On 25-Aug-2026 a reader asked why gbco.html showed a "Key levels" table
(R 31.70/32.30/33.40, S 29.96/28.20/26.73) that had nothing to do with the
levels its own narrative quoted three lines above (clear 30.12, break 28.64).
The published support sat ABOVE the published close. On clho.html all three
published resistances sat BELOW its close.

Both gates in this workflow passed clean on those pages, that same day. They
read assets/data.js with regexes, and `re.search` returns the FIRST match --
while a JavaScript object literal takes the LAST key. Both entries carried
`levels:` twice. apply_technicals.py rewrote the first one on every pass and
the browser went on rendering the second: valid markup, no console error, a
freshly computed narrative sitting over a superseded ladder, and every
automated check looking at the half the reader never saw.

So the first thing this gate does is REFUSE TO PARSE data.js ITSELF. It hands
the file to node and reads back the object the page actually renders. A checker
that models the parser instead of using it is checking a different file from
the one that ships -- the same species as the unquoted-key regex that dropped
2POINTZERO from three tools at once, and the indentation-keyed `dist` match
that deleted `touch` on nine entries.

The rest are the invariants that were true of every correct page and false of
the two broken ones, each of which would have caught this on its own:

  1. duplicate-key            no entry declares levels/tech/asof twice
  2. ladder-shape             3 resistances ascending, 3 supports descending
  3. ladder-brackets-close    R1 above, S1 below the close the NARRATIVE quotes
  4. narrative-cites-ladder   bull/bear name the levels the table publishes
  5. read-reproduces          published read recomputes from the raw library
  6. stamp-coherent           two-part as-of; tech.data IS the library's last session

Check 3 anchors on the close in the narrative, not on `spot`: those are two
clocks (a mid-cycle library arrival moves the technical read without
re-striking the cone) and conflating them would fire on a legitimate divergence
while missing an impossible ladder struck on the same day.

BOUNDARY: this says the published read is coherent and reproducible. It cannot
say the read is USEFUL, and it does not grade a forecast. A read computed on a
month-old library is coherent and reproducible and still old -- library age is
reported here as an advisory, never as a failure, because only a fresh export
fixes it and a gate nobody can clear is one everybody learns to ignore.

Exit 0 = clean, exit 1 = at least one FAIL.
"""
from __future__ import annotations

import os as _os, sys as _sys                                   # noqa: E402
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # noqa: E402
from coverage_floor import assert_examined                      # noqa: E402  [R-ENF-04]

import argparse
import json
import os
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import apply_technicals as AP                                   # noqa: E402
import technicals as TA                                         # noqa: E402

DEFAULT_JS = os.path.join(ROOT, 'assets', 'data.js')

# Read data.js through a real JS engine. `this.__*` because the file declares
# with const, which never becomes a property of the vm context.
NODE_READ = r'''
const fs = require("fs"), vm = require("vm");
const c = {}; vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[1], "utf8")
  + "\n;this.__T=TICKERS;this.__M=(typeof METALS!=='undefined')?METALS:{};this.__L=LEDGER;", c);
console.log(JSON.stringify({tickers: c.__T, metals: c.__M, ledger: c.__L.length}));
'''

FAILURES: list[tuple[str, str, str]] = []
ADVISORIES: list[str] = []


def fail(key: str, check: str, msg: str) -> None:
    FAILURES.append((key, check, msg))


def as_rendered(path: str) -> tuple[dict, int]:
    """The objects the PAGE sees -- duplicate keys collapsed exactly as JS does."""
    p = subprocess.run(['node', '-e', NODE_READ, path],
                       capture_output=True, text=True)
    if p.returncode != 0:
        print(f'FATAL: node could not load {path}\n{p.stderr.strip()}')
        raise SystemExit(1)
    d = json.loads(p.stdout)
    merged = dict(d['tickers'])
    merged.update(d['metals'])
    return merged, d['ledger']


def fmt(x: float) -> str:
    """How emit_levels renders a level, so a citation test compares like with like."""
    return str(int(x)) if float(x).is_integer() else f'{x:.2f}'


def narrative_close(summary: str):
    """The close the narrative itself states, as printed (it rounds; levels do not)."""
    import re
    m = re.search(r'closed\s+([\d,]+\.?\d*)', summary or '')
    return float(m.group(1).replace(',', '')) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('data_js', nargs='?', default=DEFAULT_JS,
                    help='data.js to check (default: assets/data.js)')
    ap.add_argument('--skip-recompute', action='store_true',
                    help='skip check 5 (the only slow one)')
    args = ap.parse_args()

    rendered, n_ledger = as_rendered(args.data_js)
    src = open(args.data_js, encoding='utf-8').read()
    scope = {k: (mkt, series) for k, _, mkt, series in AP.scope(src, None)}
    print(f'{os.path.relpath(args.data_js, ROOT)}: {len(rendered)} rendered entries, '
          f'{n_ledger} ledger rows, {len(scope)} with an OHLC library')

    # ---- 1. duplicate-key: on the TEXT, because the parsed object cannot show it
    for container in ('const TICKERS = {', 'const METALS = {'):
        try:
            blocks = AP.top_level_blocks(src, container)
        except Exception:                                        # noqa: BLE001
            continue
        for key, (a, b) in blocks.items():
            block = src[a:b]
            for field in ('levels', 'tech', 'asof'):
                n = len(AP.field_spans(block, field))
                if n > 1:
                    fail(key, 'duplicate-key',
                         f'declares `{field}` {n} times — JavaScript renders the LAST, '
                         f'every tool here rewrites the FIRST')

    ages: list[tuple[int, str]] = []
    today = date.today()

    for key, entry in sorted(rendered.items()):
        lv, tech, asof = entry.get('levels'), entry.get('tech'), entry.get('asof')
        if not lv or not tech:
            fail(key, 'ladder-shape', 'no levels/tech block')
            continue
        res, sup = list(lv.get('res') or []), list(lv.get('sup') or [])

        # ---- 2. ladder-shape
        if len(res) != 3 or len(sup) != 3:
            fail(key, 'ladder-shape', f'{len(res)} resistance(s) / {len(sup)} support(s), want 3+3')
        if res != sorted(res):
            fail(key, 'ladder-shape', f'resistances not ascending: {res} — R1 must be NEAREST the close')
        if sup != sorted(sup, reverse=True):
            fail(key, 'ladder-shape', f'supports not descending: {sup} — S1 must be NEAREST the close')
        if any(not (v > 0) for v in res + sup):
            fail(key, 'ladder-shape', f'non-positive level in {res + sup}')

        # ---- 3. ladder-brackets-close
        close = narrative_close(tech.get('summary'))
        if close is None:
            fail(key, 'ladder-brackets-close', 'no close stated in the narrative to anchor on')
        else:
            if res and not res[0] > close:
                fail(key, 'ladder-brackets-close',
                     f'R1 {res[0]} is not above the stated close {close} — a resistance under the price')
            if sup and not sup[0] < close:
                fail(key, 'ladder-brackets-close',
                     f'S1 {sup[0]} is not below the stated close {close} — a support over the price')

        # ---- 4. narrative-cites-ladder
        for field, ladder in (('bull', res), ('bear', sup)):
            txt = tech.get(field) or ''
            for pos, lab in ((0, 'nearest'), (-1, 'far')):
                if ladder and fmt(ladder[pos]) not in txt:
                    fail(key, 'narrative-cites-ladder',
                         f'{field} does not name its own {lab} level {fmt(ladder[pos])}: "{txt}"')

        # ---- 6. stamp-coherent
        if not asof or not asof.get('mc') or not asof.get('tech'):
            fail(key, 'stamp-coherent', 'missing the two-part as-of stamp')
        elif asof['tech']['computed'] < asof['tech']['data']:
            fail(key, 'stamp-coherent',
                 f"computed {asof['tech']['computed']} precedes the data it stands on "
                 f"{asof['tech']['data']}")

        if key in scope:
            mkt, series = scope[key]
            if args.skip_recompute:
                continue
            try:
                st = TA.compute(mkt, series, computed_on=today.isoformat())
            except Exception as e:                               # noqa: BLE001
                fail(key, 'read-reproduces', f'{type(e).__name__}: {e}')
                continue
            # ---- 5. read-reproduces
            if {'res': res, 'sup': sup} != st['levels']:
                fail(key, 'read-reproduces',
                     f'published {res}/{sup} but the library gives '
                     f"{st['levels']['res']}/{st['levels']['sup']}")
            for f in ('trend', 'summary', 'bull', 'bear'):
                if (tech.get(f) or '') != st['tech'][f]:
                    fail(key, 'read-reproduces', f'`{f}` differs from the recomputed read')
            if asof and asof.get('tech') and asof['tech']['data'] != st['data_date']:
                fail(key, 'stamp-coherent',
                     f"tech.data {asof['tech']['data']} but the library ends {st['data_date']}")
            ages.append(((today - date.fromisoformat(st['data_date'])).days, key))

    if ages:
        ages.sort(reverse=True)
        over = [k for d, k in ages if d > 10]
        ADVISORIES.append(
            f'library age: median {sorted(d for d, _ in ages)[len(ages) // 2]}d, '
            f'{sum(1 for d, _ in ages if d <= 3)} of {len(ages)} within 3d, '
            f'{len(over)} older than 10d, {sum(1 for d, _ in ages if d > 25)} older than 25d')
        if over:
            ADVISORIES.append('a fresh export is the ONLY fix for: ' + ', '.join(sorted(over)))

    print()
    for line in ADVISORIES:
        print(f'[advisory] {line}')
    if FAILURES:
        print()
        for key, check, msg in sorted(FAILURES):
            print(f'  FAIL  {key:12} {check:24} {msg}')
    # [R-ENF-04] A gate must never report clean having examined nothing.
    pop = assert_examined(len(rendered), 'check_technical_read')
    print(f'\n{len(rendered)} entries checked against {pop} libraries -- '
          f'{len(FAILURES)} failure(s)')
    return 1 if FAILURES else 0


if __name__ == '__main__':
    raise SystemExit(main())
