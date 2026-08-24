#!/usr/bin/env python3
"""sweep_ledger.py — the executable form of THE LEDGER SWEEP.

`engine/grade_ledger.py` is the grader: it carries the convention, the negative
control and the writer. It had no entry point, so the sweep that
Publish_Protocol.md ("sweep EVERY open row … report the count") and STEP 3 of
Rollforward_and_Grading_Protocol.md both mandate could only be run by hand-rolling
a driver each time — which is how a convention drifts, and the reason
grade_ledger.py exists as a module in the first place. This is that driver, once.

It adds no rule and computes no number of its own: every grade comes from
`grade_ledger.compute()`, every write from `grade_ledger.apply_grade()`, and the
replay negative control inside `grade_ledger.sweep()` gates both.

Run:  python3 scripts/sweep_ledger.py --today YYYY-MM-DD
      python3 scripts/sweep_ledger.py --today YYYY-MM-DD --write
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import grade_ledger as GL  # noqa: E402

DATA_JS = GL.DATA_JS


def lifecycle_report(ledger: list) -> list:
    """Open-row count per instrument. Steady state is 4 (2 -> 3 -> 4 from start).

    Reported, never fixed: a sweep may not reshape another name's cohort structure
    (Publish_Protocol, THE LEDGER SWEEP).
    """
    counts, breaches = {}, []
    for r in ledger:
        if r.get('realized_close') in (None, ''):
            counts.setdefault(r['instrument'], []).append(r)
    for inst, rows in sorted(counts.items()):
        # exactly one open latest-anchor row per (instrument, horizon)
        for hz in sorted({r['horizon_label'] for r in rows}):
            hr = [r for r in rows if r['horizon_label'] == hz]
            newest = max(r['anchor_date'] for r in hr)
            if sum(1 for r in hr if r['anchor_date'] == newest) > 1:
                breaches.append(f'{inst} {hz}: {sum(1 for r in hr if r["anchor_date"] == newest)} '
                                f'open rows share the latest anchor {newest}')
    return counts, breaches


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True, help='ISO date the sweep is run as of')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--allow-early', nargs='*', metavar='INSTRUMENT', default=None,
                    help='grade a matured row whose library stops just short of its stored '
                         'grade date on the last session inside the window, annotated. '
                         f'Bounded: the gap may not exceed {GL.EARLY_MAX_DAYS} calendar days, '
                         'so a library weeks behind stays BLOCKED either way. Name the '
                         'instruments (--allow-early EAND); passing none applies it to every '
                         'matured row inside the bound, which is rarely what you want.')
    args = ap.parse_args()

    early = False if args.allow_early is None else (args.allow_early or True)
    if isinstance(early, set) or isinstance(early, list):
        print(f'  early grading permitted for: {", ".join(sorted(early))} '
              f'(bound {GL.EARLY_MAX_DAYS} calendar days)')
    s = GL.sweep(args.today, allow_early=early)
    ledger, open_rows, matured = s['ledger'], s['open'], s['matured']
    gradable, blocked = s['gradable'], s['blocked']

    print(f'\n=== SWEEP as of {args.today} ===')
    print(f'  {len(ledger)} ledger rows, {len(open_rows)} open, '
          f'{len(matured)} matured, {len(gradable)} gradable, {len(blocked)} blocked')

    for r, got in gradable:
        print(f"  GRADE {r['instrument']:<12} {r['horizon_label']:<9} "
              f"anchor {r['anchor_date']} {r['anchor_price']} -> "
              f"{got['_graded_on']} close {got['realized_close']} "
              f"| in90={got['in_90']} in50={got['in_50']} "
              f"q={got['realized_quantile']} err={got['median_err']:+.4f} "
              f"({got['_sessions']} sessions)"
              + ('  [ROLLED from stored grade_date]' if got['_rolled'] else '')
              + (f"  [EARLY — stored grade_date {r['grade_date']} not yet in the library]"
                 if got.get('_early') else ''))
    for r, why in blocked:
        print(f"  BLOCKED {r['instrument']:<12} {r['horizon_label']:<9} "
              f"grade_date {r['grade_date']} — {why}")

    if args.write and gradable:
        src = open(DATA_JS, encoding='utf-8').read()
        for r, got in gradable:
            src = GL.apply_grade(src, r, got)
        open(DATA_JS, 'w', encoding='utf-8').write(src)
        print(f'  wrote {DATA_JS} ({len(gradable)} rows graded)')

        # VERIFY BY LOAD, NOT BY PARSE — a stitch point is valid-looking text.
        subprocess.run(['node', '--check', DATA_JS], check=True)
        after = GL.read_ledger()
        if len(after) != len(ledger):
            raise SystemExit(f'row count moved {len(ledger)} -> {len(after)}')
        still_open = [r for r in after if r.get('realized_close') in (None, '')]
        if len(still_open) != len(open_rows) - len(gradable):
            raise SystemExit('open-row count does not reconcile after grading')
        print(f'  verified: {len(after)} rows load, {len(still_open)} still open')
    elif args.write:
        print('  nothing to write')

    counts, breaches = lifecycle_report(GL.read_ledger() if args.write else ledger)
    off = {i: len(v) for i, v in counts.items() if len(v) != 4}
    if off:
        print(f'  lifecycle: {len(counts)} names open; off the 4-row steady state: '
              + ', '.join(f'{k}={v}' for k, v in sorted(off.items())))
    else:
        print(f'  lifecycle: all {len(counts)} names at the 4-row steady state')
    for b in breaches:
        print(f'  LIFECYCLE BREACH (reported, not fixed): {b}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
