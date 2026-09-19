#!/usr/bin/env python3
"""Negative control for the campaign queue and fair-value register gate.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.  This reinjects each condition
the gate claims to catch and fails if any of them is reported clean, plus a
clean control that must PASS -- because a control that only ever proves things
go red would also pass if the gate had become unconditionally red.

The conditions are the ones that actually cost something in this campaign:

  1. a walk-forward run on disk with NO frozen baseline -- the case where the
     old fair value may already be unrecoverable, which is the single failure
     this record exists to prevent and the only one with no repair
  2. a run with a baseline but no recorded fair value -- a name left in flight
  3. a record with no run directory behind it -- a fabricated entry
  4. an EMPTIED population -- the [R-ENF-04] case: zero runs examined must FAIL,
     never read as zero problems found

Nothing here touches the real record: every case runs against a temporary
ENGINE directory and a temporary store.
"""

import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import fv_movement as fv  # noqa: E402

REAL_ENGINE = fv.ENGINE
REAL_STORE = fv.STORE


def run_case(name, runs, entries, expect_fail):
    """Point the gate at a synthetic population and check its verdict."""
    tmp = tempfile.mkdtemp()
    try:
        for tk in runs:
            os.makedirs(os.path.join(tmp, '%s_walkforward' % tk.lower()))
        fv.ENGINE = tmp
        fv.STORE = os.path.join(tmp, 'fv_movement.json')
        fv._save({'entries': entries})

        # check() re-imports campaign_queue from the real engine directory --
        # the queue is a fact about the register, not about this fixture.
        sys.path.insert(0, REAL_ENGINE)
        buf, real_stdout = [], sys.stdout

        class Tee:
            def write(self, s):
                buf.append(s)

            def flush(self):
                pass

        sys.stdout = Tee()
        try:
            rc = fv.check()
        finally:
            sys.stdout = real_stdout

        failed = rc != 0
        ok = failed == expect_fail
        print('  %-4s %-58s %s'
              % ('[ok]' if ok else 'MISS', name,
                 'went red' if failed else 'reported clean'))
        if not ok:
            print('        ---- what the gate printed ----')
            for line in ''.join(buf).splitlines():
                print('        %s' % line)
        return ok
    finally:
        fv.ENGINE, fv.STORE = REAL_ENGINE, REAL_STORE
        shutil.rmtree(tmp, ignore_errors=True)


def entry(ticker, with_baseline=True, with_edition=True):
    return {
        'ticker': ticker, 'market': 'EG', 'exchange': 'EGX',
        'tier': 'reissue', 'ccy': 'EGP',
        'baseline': ({'fair': {'bear': 1.0, 'base': 2.0, 'full': 3.0},
                      'unrecoverable': None, 'built_to': 'x',
                      'captured': '2026-09-01', 'spot': None,
                      'spot_date': None, 'note': ''}
                     if with_baseline else
                     {'fair': None, 'unrecoverable': 'declared',
                      'built_to': 'x', 'captured': '2026-09-01',
                      'spot': None, 'spot_date': None, 'note': ''}),
        'editions': ([{'edition': 1, 'delivered': '2026-09-01', 'scope': 'full',
                       'origins': '', 'fair': {'bear': 1.0, 'base': 2.0, 'full': 3.0},
                       'vs_baseline_pct': None, 'vs_previous_pct': None,
                       'lessons': []}] if with_edition else []),
    }


def main():
    print('campaign register gate — negative control')
    results = [
        run_case('run on disk with no frozen baseline',
                 runs=['PHDC'], entries={}, expect_fail=True),
        run_case('run and baseline but no recorded fair value',
                 runs=['PHDC'], entries={'PHDC': entry('PHDC', with_edition=False)},
                 expect_fail=True),
        run_case('record with no walk-forward run behind it',
                 runs=['PHDC'], entries={'PHDC': entry('PHDC'),
                                         'ARCC': entry('ARCC')},
                 expect_fail=True),
        run_case('emptied population — zero runs is not zero problems',
                 runs=[], entries={}, expect_fail=True),
        run_case('CLEAN control — one complete run, must PASS',
                 runs=['PHDC'], entries={'PHDC': entry('PHDC')},
                 expect_fail=False),
    ]
    print()
    if all(results):
        print('negative control OK — the gate goes red on every injected '
              'defect and stays green on the clean case')
        return 0
    print('NEGATIVE CONTROL FAILED — %d of %d cases came back wrong. A gate '
          'that cannot be shown to fail is not evidence.'
          % (sum(1 for r in results if not r), len(results)))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
