#!/usr/bin/env python3
"""[R-ENF-01] A FIGURE MAY NOT DRAW SOMETHING OUTSIDE ITS OWN AXIS AND SAY NOTHING.

A study figure hardcoded its x-axis at 0 to 10.4 while the values it drew ran 10.86 to
12.74 against a traded price of 13.50. Every bar was clipped at the axis edge and they ALL
RENDERED THE SAME LENGTH — 11.40 indistinguishable from 12.74 — and the price line the
caption's whole argument rested on ("not all of them together reaches the price") was drawn
outside the axis and thrown away, leaving a red label floating over no line. A second figure
in the same study hardcoded 2 to 11 against the same price and lost its line the same way.

NOTHING RAISED IN EITHER CASE, and no gate could have seen them: every instrument in this
repository reads a document, a workbook or a committed number, and this defect lives in a
PNG. It is the same failure the ticker-page overlay gate exists for — a level line drawn at
y=-21, outside the viewBox, silently — arriving where nothing was watching.

THE GATE RUNS THE INSTRUMENT, IT DOES NOT COUNT THE FILE. engine/figure_guard.py wraps
Figure.savefig and inspects what each figure actually drew against the limits it actually
set, so this executes each study's figure script and reads the findings back. It runs in
DRY RUN: savefig checks and returns without writing, so the gate cannot rewrite the work it
is checking.

WHAT IS NOT A DEFECT, AND THE DETECTOR HAD TO LEARN IT TWICE. A hardcoded limit is not
itself wrong — a percentage axis pinned to 0-100 is right, and a histogram cropped at its
99.7th percentile is an honest choice. What is wrong is cropping something the figure DREW.
The first draft compared both extents of every rectangle against both axes, which fired on
ten scripts of twenty-six, most of them the detector rather than the figure: a vertical
bar's x is a category index. The second read the container's DATAVALUES, which is a
magnitude measured from the bar's base rather than a position, so every football-field span
bar drawn as barh(y, hi - lo, left=lo) was compared as though its width were a coordinate —
sixteen of twenty-six. The third reads the container for ORIENTATION and the patches for
the EDGES, and lands on two. A check that cries wolf is one everybody learns to ignore.

Ratcheted [R-ENF-02], population-anchored [R-ENF-04] both ways: a run that found no figure
scripts fails, and so does one where every script it ran refused to execute.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'figaxes_outstanding.json')

RUNNER = r'''
import os, sys, runpy, json
os.environ['FIGURE_GUARD_DRY_RUN'] = '1'
sys.path.insert(0, sys.argv[2])
import figure_guard
p = sys.argv[1]
d = os.path.dirname(os.path.abspath(p))
sys.path.insert(0, d)
os.chdir(d)
try:
    runpy.run_path(os.path.basename(p), run_name='__main__')
except SystemExit:
    pass
sys.stderr.write('@@FINDINGS@@' + json.dumps(figure_guard.FINDINGS) + '\n')
'''


def figure_scripts():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study', '*.py'))):
        try:
            s = open(f, encoding='utf-8', errors='ignore').read()
        except Exception:                                            # noqa: BLE001
            continue
        if 'matplotlib' in s and 'savefig' in s:
            out.append(f)
    return out


def audit():
    """(ran, unrunnable, findings) over every study figure script."""
    runner = os.path.join(ROOT, 'engine', 'build_depth_audit', '_figure_guard_runner.py')
    os.makedirs(os.path.dirname(runner), exist_ok=True)
    open(runner, 'w').write(RUNNER)
    ran, unrunnable, bad = 0, [], {}
    for f in figure_scripts():
        rel = os.path.relpath(f, ROOT)
        try:
            r = subprocess.run([sys.executable, runner, f,
                                os.path.join(ROOT, 'engine')],
                               capture_output=True, text=True, timeout=600)
        except Exception as e:                                       # noqa: BLE001
            unrunnable.append('%s (%s)' % (rel, e))
            continue
        err = r.stderr or ''
        if '@@FINDINGS@@' not in err:
            # THE SCRIPT WOULD NOT RUN. That is reported, never counted as clean: a
            # figure script that cannot execute has not been checked, and an unchecked
            # figure is exactly what this gate exists to stop passing quietly.
            unrunnable.append(rel)
            continue
        ran += 1
        found = json.loads(err.split('@@FINDINGS@@', 1)[1].splitlines()[0])
        if found:
            bad[rel] = found
    try:
        os.remove(runner)
    except OSError:
        pass
    return ran, unrunnable, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true')
    a = ap.parse_args()
    rat = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    allowed = set(rat.get('outstanding', {}))
    known_unrunnable = set(rat.get('unrunnable', []))

    scripts = figure_scripts()
    if not scripts:
        print('FAIL — found zero figure scripts; an empty result is not a clean result '
              '[R-ENF-04]')
        return 1
    ran, unrunnable, bad = audit()
    if not ran:
        print('FAIL — %d figure script(s) found and NONE of them ran; the guard did not '
              'execute [R-ENF-04]' % len(scripts))
        return 1

    print('figure scripts: %d;  ran under the guard: %d;  would not run: %d;  '
          'drawing outside their own axis: %d'
          % (len(scripts), ran, len(unrunnable), len(bad)))
    for k in sorted(bad):
        print('  [%s] %s' % ('ratcheted' if k in allowed else 'NEW', k))
        for line in bad[k][:4]:
            print('        %s' % line)
    new_unrunnable = sorted(set(unrunnable) - known_unrunnable)
    for u in sorted(unrunnable):
        print('  [%s] %s — would not run, so its figures are UNCHECKED'
              % ('known' if u in known_unrunnable else 'NEW', u))
    fixed = sorted(allowed - set(bad))
    if fixed:
        print('\nNOW INSIDE THEIR AXES — remove from the list (%d): %s'
              % (len(fixed), ', '.join(fixed)))

    if a.prune:
        grown = sorted(set(bad) - allowed)
        if grown:
            print('\nREFUSING TO PRUNE — the list would GROW by %s [R-ENF-02].' % grown)
            return 1
        rat['outstanding'] = {k: bad[k] for k in sorted(set(bad) & allowed)}
        rat['unrunnable'] = sorted(set(unrunnable) & known_unrunnable)
        json.dump(rat, open(RATCHET, 'w'), indent=1)
        print('\npruned: %d -> %d' % (len(allowed), len(rat['outstanding'])))
        return 0

    new = sorted(set(bad) - allowed)
    if new or new_unrunnable:
        if new:
            print('\nFAIL — figure(s) drawing outside their own axis: %s\n'
                  'Derive the limits from what is drawn, or declare the crop with '
                  'figure_guard.allow(ax, why).' % new)
        if new_unrunnable:
            print('\nFAIL — figure script(s) that will not run, so nothing checked them: '
                  '%s' % new_unrunnable)
        return 1
    print('\nOK — no new violations. %d script(s) on the ratchet and %d that will not run, '
          'both of which may only SHORTEN.' % (len(allowed), len(known_unrunnable)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
