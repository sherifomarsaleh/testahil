#!/usr/bin/env python3
"""check_grade_writer_layout.py — the grade writer reaches every open ledger row,
whatever line-wrapping that row happens to carry, and changes nothing on the rows
it already reached.

WHY THIS EXISTS
---------------
`grade_ledger.apply_grade()` rewrites a matured row's outcome fields by matching
two literal patterns. Both hard-coded ONE line-wrapping. Measured on the shipped
ledger 06-Sep-2026: 234 open rows carry the stats block on one line and 12 wrap it
between `in_50:null,` and `realized_quantile:null,`. On those 12 the grader raised
'stats block not in the expected shape' and the matured row DID NOT GRADE — PHAR's
1-month cone resolved inside its own 50% band and could not be recorded, because of
where a line happened to break.

This is the family the roll-forward protocol already names — "A LAYOUT MUST NEVER
DECIDE WHETHER A FIELD GETS REFRESHED" — and the same shape as the `dist` span that
closed on the first 4-space `},` and the `touch` ladder matched only in its
multi-line form. Per [R-ENF-01] the fix is checked from OUTSIDE the module.

WHAT IT ASSERTS, BOTH WAYS
--------------------------
1. REACH — every open row is writable by apply_grade(), or is NAMED with the field
   set it is actually missing. A row that cannot be graded is reported, never
   silently skipped: an ungradable row looks exactly like a row nobody graded.
2. BYTE-IDENTITY — on every row the OLD one-line patterns matched, the new
   whitespace-tolerant patterns must produce a byte-identical rewrite. This is the
   half that matters: a widened pattern that also changes existing output has not
   fixed the gate, it has moved it.
3. POPULATION [R-ENF-04] — a run that examined ZERO open rows FAILS. An empty
   result is not a clean result.
"""
from __future__ import annotations
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import grade_ledger as GL  # noqa: E402

# The patterns EXACTLY as apply_grade carried them before the fix.
OLD_OUTCOME = r'realized_close:null, realized_high:null, realized_low:null,'
OLD_STATS = r'in_90:null, in_50:null, realized_quantile:null, median_err:null,'

# A representative grade payload. The VALUES are irrelevant — what is under test is
# which rows the writer can reach and whether its output moves, not any number.
GOT = dict(realized_close=128.0, realized_high=160.18, realized_low=124.5,
           in_90=True, in_50=True, realized_quantile=0.417, median_err=-0.0280,
           touch_hit={k: False for k, _ in GL.REL},
           _rolled=False, _graded_on='2026-09-06', _early=False)


def main() -> int:
    src = open(GL.DATA_JS, encoding='utf-8').read()
    spans = list(GL.ledger_row_spans(src))
    if not spans:
        print('FAIL: examined zero ledger rows — the reader broke, the ledger did not empty')
        return 1

    reached = old_reachable = identical = 0
    unreachable, drifted = [], []
    for a, b in spans:
        t = src[a:b]
        if GL._field(t, 'realized_close') != 'null':
            continue                                   # graded rows are permanent
        row = dict(instrument=GL._field(t, 'instrument'),
                   horizon_label=GL._field(t, 'horizon_label'),
                   anchor_date=GL._field(t, 'anchor_date'),
                   grade_date=GL._field(t, 'grade_date'),
                   cycle_no=int(GL._field(t, 'cycle_no')))
        label = f"{row['instrument']} {row['horizon_label']} {row['anchor_date']}"
        try:
            new_src = GL.apply_grade(src, row, GOT)
        except SystemExit as e:
            missing = [f for f in ('realized_high', 'realized_low', 'in_90', 'in_50')
                       if GL._field(t, f) is None]
            unreachable.append((label, str(e), missing))
            continue
        reached += 1
        # Byte-identity against the OLD patterns, on the rows the old code reached.
        if re.search(OLD_OUTCOME, t) and re.search(OLD_STATS, t):
            old_reachable += 1
            legacy = _legacy_rewrite(src, a, b, t)
            if legacy == new_src:
                identical += 1
            else:
                drifted.append(label)

    print(f'examined {len(spans)} ledger rows; {reached + len(unreachable)} open')
    print(f'  writer reaches            : {reached}')
    print(f'  old one-line patterns hit : {old_reachable}')
    print(f'  byte-identical to legacy  : {identical} of {old_reachable}')
    if unreachable:
        print(f'  UNREACHABLE ({len(unreachable)}) — rows whose field set the writer cannot fill:')
        for label, why, missing in unreachable:
            print(f'    {label}: {why} | fields absent from the row: {missing or "none"}')

    bad = False
    if drifted:
        print(f'FAIL: the widened pattern CHANGED output on {len(drifted)} rows '
              f'the old one already handled: {drifted[:8]}')
        bad = True
    if old_reachable and identical != old_reachable:
        bad = True
    if reached == 0:
        print('FAIL: the writer reached zero open rows')
        bad = True
    if unreachable:
        # Reported, not fatal: these rows are short a FIELD, not a line break, and
        # inventing the missing fields would edit a published forecast's structure.
        # They are named here so the gap is visible rather than absent.
        print('NOTE: the rows above are missing outcome FIELDS, not merely wrapped — '
              'a schema gap, recorded rather than silently patched.')
    print('OK' if not bad else 'FAILED')
    return 1 if bad else 0


def _legacy_rewrite(src: str, a: int, b: int, t: str) -> str:
    """apply_grade's rewrite exactly as it stood before the whitespace fix."""
    def num(x):
        s = f'{x:.4f}'.rstrip('0').rstrip('.')
        return s if s else '0'
    jb = lambda v: 'true' if v else 'false'
    rq = f"{GOT['realized_quantile']:.3f}"
    t2 = t.replace(OLD_OUTCOME,
                   f"realized_close:{num(GOT['realized_close'])}, "
                   f"realized_high:{num(GOT['realized_high'])}, "
                   f"realized_low:{num(GOT['realized_low'])},")
    t2 = t2.replace(OLD_STATS,
                    f"in_90:{jb(GOT['in_90'])}, in_50:{jb(GOT['in_50'])}, "
                    f"realized_quantile:{rq}, median_err:{GOT['median_err']:.4f},")
    old_th = re.search(r'touch_hit:\{[^}]*\}', t2)
    if old_th:
        th = ', '.join(f'"{k}":{jb(GOT["touch_hit"][k])}' for k, _ in GL.REL)
        t2 = t2.replace(old_th.group(0), 'touch_hit:{ ' + th + ' }')
    return src[:a] + t2 + src[b:]


if __name__ == '__main__':
    raise SystemExit(main())
