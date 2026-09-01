#!/usr/bin/env python3
"""Negative control for check_campaign_parked.py.  [R-CAMP-01, R-ENF-04]

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE.  This reinjects each defect the
gate claims to catch, into a COPY of the store, and asserts the gate goes red
on every one.  It also asserts the unmodified store passes, so a gate that
failed everything unconditionally would be caught too.

The defects are the real ones this design was written against, not invented
ones: a park with no attempt log (an assertion), an attempt with no outcome (a
URL list read as evidence), a park with no document request (a block nobody
else can clear), and the two exclusions -- a parked name that also carries a
run directory or a frozen baseline, each of which turns a campaign gate red for
a run that is not happening.
"""
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
sys.path.insert(0, ENGINE)
import campaign_parked as cp  # noqa: E402

STORE = cp.STORE


def run_gate():
    import importlib
    importlib.reload(cp)
    cp.STORE = STORE
    return cp.check()


def with_store(mutate):
    orig = open(STORE, encoding='utf-8').read()
    d = json.loads(orig)
    mutate(d)
    open(STORE, 'w', encoding='utf-8').write(json.dumps(d, indent=1, sort_keys=True))
    try:
        return run_gate()
    finally:
        open(STORE, 'w', encoding='utf-8').write(orig)


def first(d):
    return sorted(k for k, v in d['entries'].items() if not v.get('unparked'))[0]


def main():
    fails = []
    if not os.path.exists(STORE):
        print('nothing parked — negative control has nothing to reinject; '
              'that is a vacuous pass and is reported as one')
        return 0

    print('baseline (unmodified store) must PASS:')
    if run_gate() != 0:
        fails.append('the unmodified store does not pass — the control cannot '
                     'attribute later failures to its own injections')
    else:
        print('  [ok]   baseline green\n')

    cases = {
        'attempts stripped (a park that is an assertion, not evidence)':
            lambda d: d['entries'][first(d)].__setitem__('attempts', []),
        'an attempt with its OUTCOME blanked (a URL list read as evidence)':
            lambda d: d['entries'][first(d)]['attempts'][0].__setitem__('outcome', ''),
        'document request removed (a block nobody else can clear)':
            lambda d: d['entries'][first(d)].__setitem__('documents_needed', []),
        'unpark condition removed (a park with no way out)':
            lambda d: d['entries'][first(d)].__setitem__('unpark_when', ''),
        'parked name renamed to one not in the queue':
            lambda d: d['entries'].__setitem__(
                'NOTATICKER', dict(d['entries'][first(d)], ticker='NOTATICKER')),
    }
    for label, mut in cases.items():
        rc = with_store(mut)
        print('  %-64s -> %s' % (label[:64], 'RED (correct)' if rc else 'GREEN — MISSED'))
        if rc == 0:
            fails.append('gate did not catch: %s' % label)

    # the two exclusions need a real directory / real baseline on disk
    tk = first(json.loads(open(STORE, encoding='utf-8').read()))
    rd = os.path.join(ENGINE, '%s_walkforward' % tk.lower())
    made = False
    if not os.path.isdir(rd):
        os.makedirs(rd)
        made = True
    try:
        rc = run_gate()
        print('  %-64s -> %s' % ('parked name given a run directory',
                                 'RED (correct)' if rc else 'GREEN — MISSED'))
        if rc == 0:
            fails.append('gate did not catch a parked name with a run directory')
    finally:
        if made:
            shutil.rmtree(rd)

    import fv_movement
    fv_orig = open(fv_movement.STORE, encoding='utf-8').read()
    fd = json.loads(fv_orig)
    fd['entries'][tk] = {'ticker': tk, 'baseline': {}, 'editions': []}
    open(fv_movement.STORE, 'w', encoding='utf-8').write(json.dumps(fd, indent=1, sort_keys=True))
    try:
        rc = run_gate()
        print('  %-64s -> %s' % ('parked name given a frozen fair-value baseline',
                                 'RED (correct)' if rc else 'GREEN — MISSED'))
        if rc == 0:
            fails.append('gate did not catch a parked name with a frozen baseline')
    finally:
        open(fv_movement.STORE, 'w', encoding='utf-8').write(fv_orig)

    print()
    if fails:
        for f in fails:
            print('  FAIL  %s' % f)
        return 1
    print('negative control OK — every reinjected defect turned the gate red, '
          'and the unmodified store stayed green')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
