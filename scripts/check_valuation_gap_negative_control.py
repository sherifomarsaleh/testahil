#!/usr/bin/env python3
"""Negative control for the valuation-gap gate.  [R-GAP-01]

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. This reinjects every condition the gate
claims to catch and fails if any of them is reported clean, plus a clean control that
must PASS — because a control proving only that things go red would also pass if the
gate had become unconditionally red.

The conditions are the ones that actually cost something:

  1. a central fair value far below the traded price with NO review — the AMOC case of
     1-Sep-2026, where six independent modelling defects sat behind a 39% discount and
     every existing gate passed the study
  2. a review that EXISTS but skips a required heading — the rubber stamp, which is the
     way a review requirement normally dies
  3. a study whose committed numbers do not resolve to a central/spot pair — an answer
     nobody can read is not an answer that passed  [R-ENF-04]
  4. an EMPTIED population — zero studies examined must FAIL, never read as zero
     problems found  [R-ENF-04]
  5. a study on the outstanding list that no longer resolves on disk — the gate's own
     glob having silently stopped matching
  6. [AMENDED 02-Sep-2026] a gap on the other side (central far ABOVE spot) MUST now fire:
     the rule is two-sided, and the case that used to prove the one-sidedness is inverted
     here rather than deleted, because the same construction going from green to red is the
     sharpest evidence the extension took effect. What used to read: the rule is
     one-sided by instruction, and a check that fires where no rule exists is the
     permanently-red check [R-ENF-02] forbids

Nothing here touches the real studies: every case runs against a temporary ENGINE
directory built from scratch.
"""
import io
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import check_valuation_gap as gate  # noqa: E402

REAL_ENGINE, REAL_OUTSTANDING = gate.ENGINE, gate.OUTSTANDING

FULL_REVIEW = '\n'.join('## %s\ncovered.\n' % k for k in gate.REQUIRED_SECTIONS)


def make_study(engine, tk, central=None, spot=None, review=None, numbers=True):
    d = os.path.join(engine, '%s_study' % tk.lower())
    os.makedirs(d, exist_ok=True)
    if numbers:
        j = {}
        if central is not None:
            j['central'] = central
        if spot is not None:
            j['spot'] = spot
        json.dump(j, io.open(os.path.join(d, 'study_numbers.json'), 'w', encoding='utf-8'))
    if review is not None:
        io.open(os.path.join(d, 'GAP_REVIEW_01-09-2026.md'), 'w',
                encoding='utf-8').write(review)
    return d


def run_case(name, build, outstanding, expect_fail):
    tmp = tempfile.mkdtemp()
    try:
        build(tmp)
        os.makedirs(os.path.join(tmp, 'build_depth_audit'), exist_ok=True)
        op = os.path.join(tmp, 'build_depth_audit', 'gap_outstanding.json')
        json.dump(outstanding, io.open(op, 'w', encoding='utf-8'))
        gate.ENGINE, gate.OUTSTANDING = tmp, op

        buf, real = [], sys.stdout

        class Tee:
            def write(self, s):
                buf.append(s)

            def flush(self):
                pass

        sys.stdout = Tee()
        try:
            rc = gate.main([])
        finally:
            sys.stdout = real

        failed = rc != 0
        ok = failed == expect_fail
        print('  %-4s %-62s %s' % ('[ok]' if ok else 'MISS', name,
                                   'went red' if failed else 'reported clean'))
        if not ok:
            print('        ---- what the gate printed ----')
            for line in ''.join(buf).splitlines():
                print('        %s' % line)
        return ok
    finally:
        gate.ENGINE, gate.OUTSTANDING = REAL_ENGINE, REAL_OUTSTANDING
        shutil.rmtree(tmp, ignore_errors=True)


EMPTY = {'breach_no_review': [], 'unreadable': [], 'exempt': {}}


def main():
    print('valuation-gap gate — negative control')
    cases = [
        ('central 39% below spot, no gap review',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10), EMPTY, True),
        ('review exists but skips a required heading',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10,
                              review=FULL_REVIEW.replace('## DISCOUNT RATE', '## SOMETHING ELSE')),
         EMPTY, True),
        ('committed numbers carry no central/spot pair',
         lambda e: make_study(e, 'AMOC'), EMPTY, True),
        ('emptied population — zero studies is not zero problems',
         lambda e: None, EMPTY, True),
        ('listed study no longer resolves on disk',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10),
         {'breach_no_review': ['SWDY'], 'unreadable': [], 'exempt': {}}, True),
        ('CLEAN — central 1% below spot, must PASS',
         lambda e: make_study(e, 'AMOC', 9.00, 9.10), EMPTY, False),
        # [R-GAP-01 amended, 02-Sep-2026] the gate is TWO-SIDED. This case tested the
        # one-sidedness and is INVERTED here rather than deleted: the same construction
        # that had to stay green under the old rule must go red under the new one, which
        # is the sharpest possible evidence that the extension actually took effect.
        ('central far ABOVE spot, unreviewed — the two-sided extension',
         lambda e: make_study(e, 'AMOC', 18.00, 9.10), EMPTY, True),
        ('central 13% above spot, unreviewed — the DU case the one-sided rule could not see',
         lambda e: make_study(e, 'AMOC', 10.28, 9.10), EMPTY, True),
        ('CLEAN — central above spot WITH a complete review, must PASS',
         lambda e: make_study(e, 'AMOC', 18.00, 9.10, review=FULL_REVIEW), EMPTY, False),
        ('CLEAN — central 8% above spot, inside the band, must PASS',
         lambda e: make_study(e, 'AMOC', 9.83, 9.10), EMPTY, False),
        ('CLEAN — breach WITH a complete review, must PASS',
         lambda e: make_study(e, 'AMOC', 5.53, 9.10, review=FULL_REVIEW), EMPTY, False),
    ]
    results = [run_case(n, b, o, f) for n, b, o, f in cases]
    print()
    if all(results):
        print('negative control OK — the gate goes red on every injected defect, on both '
              'sides of the price, and stays green on every clean case')
        return 0
    print('NEGATIVE CONTROL FAILED — %d of %d cases came back wrong. A gate that cannot be '
          'shown to fail is not evidence.' % (sum(1 for r in results if not r), len(results)))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
