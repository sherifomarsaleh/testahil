#!/usr/bin/env python3
"""Every study states its fundamental walk-forward SCOPE DECISION, and states it truly.

WHY THIS EXISTS
    [R-FCAL-01] has said since 31-Aug-2026 that the fundamental walk-forward is A STANDING
    STEP OF EVERY NEW STUDY AND EVERY UPDATE, on the same footing as the data-quality gate
    and the Step 2A sweep, and that SCOPE IS DECIDED FIRST AND STATED IN THE STUDY — FULL at
    eight or more sourceable fiscal years, LIGHT at five to seven, SKIP below five, with the
    skip recorded in the protocol's own words. Measured 05-Sep-2026, TWENTY-THREE OF
    TWENTY-FOUR STUDIES STATE NO SCOPE DECISION AT ALL. A grep across every study directory
    returns one field, in the study that was being audited when somebody looked.

    The rule was not disputed and was not hard. It was simply not present at the moment it
    bound, which is [R-ENF-01]'s founding observation, and nothing outside a study was
    looking for it.

WHAT A DECISION HAS TO SAY, AND WHY EACH FIELD
    scope                      FULL / LIGHT / SKIP — the decision itself
    sourceable_fiscal_years    the count the decision rests on. NOT the count a study
                               happens to hold: the rule asks what is SOURCEABLE, and a
                               study that fetched three years from an archive carrying
                               sixteen has a deep history and a shallow directory.
    basis                      how that count is known, so it can be checked
    status                     pending / run / not_run
    note                       what a reader is owed. A study whose method has never been
                               tested against the company's own history is in a different
                               position from one whose has, and the difference is not
                               visible from the answer.

THE THREE THINGS IT CHECKS, BEYOND PRESENCE
    1. THE SCOPE MATCHES THE COUNT. FULL needs eight, LIGHT five to seven, SKIP fewer than
       five. A study declaring SKIP on twelve sourceable years has decided something the
       rule does not permit, and a study declaring FULL on three has claimed a test it
       cannot run.
    2. A SKIP CARRIES THE PROTOCOL'S OWN WORDS. The rule specifies them — "walk-forward not
       run - insufficient sourceable history" - because a skip phrased freely is a skip
       nobody can find.
    3. THE DECLARATION MATCHES THE DISK. If a walk-forward run directory exists for the
       ticker, a status of 'pending' or 'not_run' is FALSE, and it is false in the direction
       that matters: it tells a reader the method is untested when it has been tested. This
       is the declared-versus-done check [R-MACRO-01] names — A CHECK THAT READS WHAT A
       PROCESS DECLARES IS NOT CHECKING WHAT THE PROCESS DOES — pointed at the one field
       where the two can be compared.

WHAT IT DELIBERATELY DOES NOT DO
    It does not require the run. [R-FCAL-01] is explicit that a first delivery is NEVER
    DELAYED for one: the run goes alongside, its corrections feed the next edition, and the
    edition carries a pending note. A gate demanding the run would be red on every new
    study by construction, which is the permanently-red check [R-ENF-02] forbids. What it
    requires is that the DECISION exist, be internally consistent, and be true.

THE POPULATION IS ANCHORED ELSEWHERE, BOTH WAYS  [R-ENF-04]
    Every listed ticker must resolve to a study directory; a run examining zero directories
    FAILS; and a run that READ zero numbers files across present directories FAILS, which is
    the distinction an absent answer hides behind.

THE RATCHET  [R-ENF-02]
    Twenty-three studies state no decision on adoption day and are listed. The build breaks
    on a NEW study with no decision either way, on a decision that contradicts itself, or on
    one that contradicts the disk. The list may only ever SHORTEN. --prune rewrites it.

USAGE
    python3 scripts/check_walkforward_scope.py
    python3 scripts/check_walkforward_scope.py --prune
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'walkforward_scope_outstanding.json')

SCOPES = ('FULL', 'LIGHT', 'SKIP')
STATUSES = ('pending', 'run', 'not_run')
#: the bands [R-FCAL-01] sets, as (scope, minimum, maximum-inclusive)
BANDS = {'FULL': (8, 10 ** 6), 'LIGHT': (5, 7), 'SKIP': (0, 4)}
#: the words the rule specifies for a skip, matched loosely on the two that carry it
SKIP_WORDS = ('walk-forward not run', 'insufficient sourceable history')
REQUIRED = ('scope', 'sourceable_fiscal_years', 'basis', 'status', 'note')


def numbers_of(d):
    """A study's committed numbers file, under either name this book has used."""
    for name in ('study_numbers.json',):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    hits = sorted(glob.glob(os.path.join(d, '*numbers*.json')))
    return hits[0] if hits else None


def has_run(tk):
    return os.path.isdir(os.path.join(ROOT, 'engine', '%s_walkforward' % tk.lower()))


def judge(tk, rec):
    """[] if the decision is sound, else the reasons it is not."""
    bad = []
    if not isinstance(rec, dict):
        return ['the walkforward_scope record is not an object']
    for f in REQUIRED:
        if rec.get(f) in (None, ''):
            bad.append('%s is missing or empty' % f)
    if bad:
        return bad
    sc = rec['scope']
    if sc not in SCOPES:
        return ['scope %r is not one of %s' % (sc, ', '.join(SCOPES))]
    if rec['status'] not in STATUSES:
        bad.append('status %r is not one of %s' % (rec['status'], ', '.join(STATUSES)))
    n = rec['sourceable_fiscal_years']
    if not isinstance(n, int) or n < 0:
        bad.append('sourceable_fiscal_years %r is not a count' % (n,))
    else:
        lo, hi = BANDS[sc]
        if not lo <= n <= hi:
            bad.append('scope %s needs %s sourceable fiscal years and the record states %d'
                       % (sc, ('at least %d' % lo) if hi > 100 else
                          ('%d to %d' % (lo, hi)) if lo else ('fewer than %d' % (hi + 1)), n))
    if sc == 'SKIP':
        txt = (str(rec.get('note', '')) + ' ' + str(rec.get('basis', ''))).lower()
        if not all(w in txt for w in SKIP_WORDS):
            bad.append('a SKIP must be recorded in the rule\'s own words — '
                       '"walk-forward not run - insufficient sourceable history (N years)"')
    if has_run(tk) and rec['status'] in ('pending', 'not_run'):
        bad.append('a walk-forward run exists on disk at engine/%s_walkforward/ and the '
                   'record says %r — the declaration contradicts the disk, in the '
                   'direction that tells a reader the method is untested when it is not'
                   % (tk.lower(), rec['status']))
    return bad


def main(argv):
    prune = '--prune' in argv
    rat = (json.load(open(RATCHET)) if os.path.exists(RATCHET)
           else {'entries': {}, 'note': ''})
    entries = rat.get('entries', {})

    dirs = sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study')))
    if not dirs:
        print('FAIL — examined ZERO study directories. The resolver is broken, not the book.')
        return 1
    on_disk = {os.path.basename(d)[:-len('_study')].upper() for d in dirs}
    for tk in entries:
        if tk.upper() not in on_disk:
            print('FAIL — %s is on the ratchet and has no study directory on disk.' % tk)
            return 1

    read, stated, missing, broken = 0, [], [], []
    for d in dirs:
        tk = os.path.basename(d)[:-len('_study')].upper()
        p = numbers_of(d)
        if p is None:
            missing.append((tk, 'no committed numbers file'))
            continue
        try:
            nums = json.load(open(p))
        except Exception as e:                                       # noqa: BLE001
            broken.append((tk, 'the numbers file will not parse: %s' % e))
            continue
        read += 1
        rec = nums.get('walkforward_scope')
        if rec is None:
            missing.append((tk, 'no walkforward_scope record'))
            continue
        why = judge(tk, rec)
        if why:
            broken.append((tk, '; '.join(why)))
        else:
            stated.append((tk, '%s, %d years, %s' % (rec['scope'],
                                                     rec['sourceable_fiscal_years'],
                                                     rec['status'])))

    if read == 0:
        print('FAIL — %d study directories are present and ZERO numbers files were READ. '
              'An empty result is not a clean result.' % len(dirs))
        return 1

    print('WALK-FORWARD SCOPE — the decision [R-FCAL-01] requires every study to state')
    print('examined %d study directories; read %d numbers files' % (len(dirs), read))
    print()
    if stated:
        print('STATED (%d):' % len(stated))
        for tk, s in sorted(stated):
            print('   %-12s %s' % (tk, s))
    if missing:
        print()
        print('NO DECISION (%d): %s' % (len(missing), ', '.join(t for t, _ in sorted(missing))))

    problems = []
    for tk, why in missing:
        if tk not in entries:
            problems.append((tk, why))
    for tk, why in broken:
        # a CONTRADICTORY decision is never excused: the ratchet spares a study that has
        # not written one, not one that has written a false one.
        problems.append((tk, why))

    if broken:
        print()
        print('CONTRADICTS ITSELF OR THE DISK (%d):' % len(broken))
        for tk, why in sorted(broken):
            print('   ! %-12s %s' % (tk, why))

    if prune:
        keep = {t: entries[t] for t, _ in missing if t in entries}
        cut = len(entries) - len(keep)
        json.dump({'entries': keep, 'note': rat.get('note', '')},
                  open(RATCHET, 'w'), indent=1, sort_keys=True)
        print('\npruned %d entr%s; the list may only ever get shorter.'
              % (cut, 'y' if cut == 1 else 'ies'))
        return 0

    if problems:
        print()
        for tk, why in sorted(problems):
            print('  ! %-12s %s' % (tk, why))
        print('\nFAIL — a scope decision is decided first and stated in the study.')
        return 1
    print('\nOK — no new study without a scope decision, and none contradicting itself.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
