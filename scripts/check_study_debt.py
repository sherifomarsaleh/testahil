#!/usr/bin/env python3
"""[R-ENF-01] THE BOOK'S RECORDED DEBT IS COUNTED, AND AN UNRECOGNISED RATCHET IS RED.

[R-ENF-02] is right that a ratchet is the way to carry a known debt. [R-REPAIR-01] is
right that a system which only detects accumulates debt at the rate it detects, and
that every individual entry is legitimate, which is what makes the TOTAL invisible.

NOBODY HAD COUNTED THE TOTAL. [R-REPAIR-01] was adopted on "47 ratchet entries
accumulated on five studies", read off the lists somebody happened to open. Measured
18-09-2026 across all 67 ratchets: 386 entries across 94 names -- 274 on the 24 studies
that exist on disk and 112 on 70 names the site publishes with no study directory at
all. The gap between 47 and 386 is the whole argument for counting.

THIS GATE SETS NO CEILING, DELIBERATELY. A new standard legitimately adds entries on
the day it is adopted -- that is what [R-ENF-02] exists for -- so a bar on the total
would fire on a rule being written, which is the permanently-red check that rule
forbids. What it refuses is the three ways a count stops being a count:

    an UNRECOGNISED KEY, which a reader would otherwise skip silently [L-355];
    a TICKER ON A DEBT LIST THAT IS NOT ON DISK and is not a published name either;
    ZERO ratchets read, or zero entries found across them [R-ENF-04].

The count itself is REPORTED, dated, and committed so movement is visible -- which is
the one thing a pile of individually-correct lists cannot show.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import study_debt as SD                                            # noqa: E402

SNAPSHOT = os.path.join(ROOT, 'engine', 'build_depth_audit', 'debt_snapshot.json')


def published_names():
    """Every name the site carries, through a real JavaScript parse [R-ENF-03]."""
    p = os.path.join(ROOT, 'assets', 'data.js')
    if not os.path.exists(p):
        return set()
    t = open(p, encoding='utf-8', errors='ignore').read()
    return set(re.findall(r'^\s*"?([A-Z0-9][A-Z0-9_]{1,13})"?\s*:\s*\{', t, re.M))


def main() -> int:
    try:
        lines, by_tk, files, unknown = SD.report()
    except SD.UnknownShape as exc:
        print('FAIL — %s' % exc)
        return 1

    if files == 0:
        print('FAIL — read zero ratchet files. An absent answer is not a clean one.')
        return 1
    total = sum(len(v) for v in by_tk.values())
    if total == 0:
        print('FAIL — %d ratchet file(s) read and NOT ONE entry found. A reader that '
              'stopped reading looks exactly like a book with no debt [R-ENF-04].' % files)
        return 1
    if unknown:
        print('FAIL — %d ratchet key(s) this reader cannot classify. An unrecognised '
              'shape is RED, never skipped: a reader that guesses silently finds '
              'nothing and reports it as a result [L-355].' % len(unknown))
        for f, k in unknown[:12]:
            print('    %-44s %s' % (f, k))
        print('  Each needs a decision in study_debt.DEBT or study_debt.NOT_DEBT, by '
              'name. There is no pattern that can make it for you.')
        return 1

    on_disk = {os.path.basename(d).replace('_study', '').upper()
               for d in glob.glob(os.path.join(ROOT, 'engine', '*_study'))}
    pub = published_names()
    # NOT EVERY RATCHETED NAME IS A STUDY, and the gate found that out by refusing two
    # it could not place. [R-IDX-01]'s held_unregistered list names INDEX SERIES --
    # ADXGENERAL and DFMGI -- which are a real debt about a different subject. They are
    # resolved against engine/raw_indices/ rather than against the study directories,
    # because a name checked against the wrong population is worse than one unchecked.
    idx = {os.path.splitext(os.path.basename(f))[0].upper()
           for f in glob.glob(os.path.join(ROOT, 'engine', 'raw_indices', '*', '*.csv'))}
    ghosts = sorted(tk for tk in by_tk
                    if tk not in on_disk and tk not in pub and tk not in idx)
    if ghosts:
        print('FAIL — %d name(s) carry a recorded debt and are neither a study on disk '
              'nor a name the site publishes: %s' % (len(ghosts), ', '.join(ghosts)))
        return 1

    with_study = {k: v for k, v in by_tk.items() if k in on_disk}
    without = {k: v for k, v in by_tk.items() if k not in on_disk}
    n_w = sum(len(v) for v in with_study.values())
    n_o = sum(len(v) for v in without.values())

    for l in lines[:1]:
        print(l)
    print('  %3d entries on %2d stud%s that exist on disk'
          % (n_w, len(with_study), 'y' if len(with_study) == 1 else 'ies'))
    print('  %3d entries on %2d name(s) the site publishes with NO study directory'
          % (n_o, len(without)))
    print()
    for tk, v in sorted(with_study.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print('  %-13s %2d  %s' % (tk, len(v),
                                   ', '.join(sorted(set(x.split(':')[0] for x in v)))[:96]))

    prev = json.load(open(SNAPSHOT)) if os.path.exists(SNAPSHOT) else None
    if prev:
        d = total - prev.get('total', total)
        print('\n  against the snapshot of %s: %+d entr%s'
              % (prev.get('as_of', '?'), d, 'y' if abs(d) == 1 else 'ies'))
    if '--write' in sys.argv:
        import datetime as dt
        json.dump({'as_of': dt.date.today().isoformat(), 'total': total,
                   'with_study': n_w, 'without_study': n_o,
                   'ratchets': files,
                   'by_ticker': {k: len(v) for k, v in sorted(by_tk.items())},
                   'note': 'GENERATED by scripts/check_study_debt.py --write. Never '
                           'hand-edited. It sets no ceiling: a new standard adds '
                           'entries legitimately on the day it is adopted, and a bar '
                           'on the total would fire on a rule being written.'},
                  open(SNAPSHOT, 'w'), indent=1)
        open(SNAPSHOT, 'a').write('\n')
        print('  snapshot written')

    print('\nOK — %d ratchet(s) read, every key classified by name, every name resolves.'
          % files)
    return 0


if __name__ == '__main__':
    sys.exit(main())
