"""EVERY STUDY THAT HAS A TERMINAL BUILDS IT THROUGH THE SANCTIONED MODULE.

WHAT THIS CLOSES, AND IT IS A HOLE IN AN EXISTING RULE RATHER THAN A NEW ONE.
[R-TERM-01] requires a terminal's maintenance capital to rest on a DISCLOSED useful life,
and engine/terminal_value.py refuses one without a source. Four gates already police the
terminal: check_terminal_record_shape.py, _basis, _floor, _spread.

Every one of them reads a COMMITTED TERMINAL RECORD. A study that builds its terminal by
hand and commits no record is examined by none of them and passes all four -- the
[R-ENF-04] costume, absence reading as cleanliness. Measured 09-09-2026: 24 study
directories, 24 readable, and only 12 carrying a terminal record.

Four of those studies have a terminal in their committed numbers and do not import
terminal_value ANYWHERE -- not in compute.py, not in any module beside it. Their terminals
are hand-rolled, which is what every terminal in this book was before the module existed
and before the defect that produced it was found: a construction that reinvested a share of
profit at an assumed return, which read as a capital programme rebuilding the whole asset
base every 1/g years -- a fact about the pound rather than about the plant. That defect
REVERSES SIGN in a pegged currency, which is why it matters that the module is used rather
than that its answer is copied.

THE RATCHET [R-ENF-02] carries the four standing at adoption so this binds forward without
being red on the day it lands. It may only ever SHORTEN. A study joining the book with a
hand-rolled terminal is a NEW breach and fails.

WHAT THIS DOES NOT CHECK: whether a terminal is CORRECT. The four gates above do that on
the record. This one asks only whether the record exists to be checked.

[R-ENF-01] runs from outside every study it governs and modifies nothing.
[R-ENF-07] falsifier: scripts/check_terminal_module_use_negative_control.py.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')

#: measured 09-09-2026. Each carries a terminal in its committed numbers and imports
#: terminal_value nowhere. May only SHORTEN.
RATCHET = {
    'ADNOCDIST': 'hand-rolled terminal, no terminal_record committed',
    'AMOC': 'hand-rolled terminal; carries terminal_recon only, and the sanctioned build '
            'on its own measured asset age was priced at -0.247 a share by an outside '
            'challenge on 09-09-2026 and never carried in',
    'AMR': 'hand-rolled terminal, no terminal_record committed',
    'ELEC': 'hand-rolled terminal; the study is HELD on SIGCM and is not deliverable on '
            'its own sources regardless',
}


def _study_dirs():
    return sorted(d for d in glob.glob(os.path.join(ENGINE, '*_study'))
                  if os.path.isdir(d))


def _has_terminal(numbers):
    """Does this study's committed record describe a terminal at all?

    Deliberately broad: 'terminal' anywhere in the committed keys or a top-level tv. A
    study with no terminal owes no record, and a broad test errs toward ASKING rather
    than toward silence.
    """
    txt = json.dumps(numbers).lower()
    return '"tv"' in txt or 'terminal' in txt


def main():
    rows, missing, unreadable = [], [], []
    for d in _study_dirs():
        tk = os.path.basename(d)[:-len('_study')].upper()
        sn = os.path.join(d, 'study_numbers.json')
        if not os.path.exists(sn):
            continue
        try:
            j = json.load(open(sn, encoding='utf-8'))
        except Exception as e:
            unreadable.append((tk, str(e)[:60]))
            continue
        if not _has_terminal(j):
            rows.append((tk, 'no terminal', ''))
            continue
        src = ''
        for f in glob.glob(os.path.join(d, '*.py')):
            try:
                src += open(f, encoding='utf-8', errors='ignore').read()
            except OSError:
                pass
        uses = 'terminal_value' in src
        has_record = bool(j.get('terminal_record'))
        if uses:
            rows.append((tk, 'module', 'record' if has_record else 'no record committed'))
        else:
            missing.append(tk)

    print('TERMINAL CONSTRUCTION — does the study build it through terminal_value.py?')
    print('  %-13s %-12s %s' % ('study', 'built by', 'record'))
    for tk, how, note in rows:
        print('  %-13s %-12s %s' % (tk, how, note))
    print('\n  %d study/ies examined · %d through the module · %d hand-rolled · %d with '
          'no terminal' % (len(rows) + len(missing),
                           sum(1 for _, h, _ in rows if h == 'module'),
                           len(missing),
                           sum(1 for _, h, _ in rows if h == 'no terminal')))

    if unreadable:
        print('\nRED — %d study/ies could not be read. Unreadable is not clean '
              '[R-ENF-04]:' % len(unreadable))
        for tk, why in unreadable:
            print('   %-13s %s' % (tk, why))
        return 1

    if not rows and not missing:
        print('\nRED — zero studies examined. An empty population is not a clean result '
              '[R-ENF-04]: this globs engine/*_study and that returning nothing means the '
              'layout moved, not that every terminal is sanctioned.')
        return 1

    covered = [tk for tk in missing if tk in RATCHET]
    new = [tk for tk in missing if tk not in RATCHET]

    if covered:
        print('\nON THE RATCHET (%d) — recorded, may only shorten:' % len(covered))
        for tk in sorted(covered):
            print('   %-13s %s' % (tk, RATCHET[tk]))

    cleared = [tk for tk in RATCHET if tk not in missing]
    if cleared:
        print('\nCLEARED since the ratchet was written (%d) — remove from RATCHET: %s'
              % (len(cleared), ', '.join(sorted(cleared))))

    if new:
        print('\nRED — %d study/ies build a terminal outside the sanctioned module:' % len(new))
        for tk in sorted(new):
            print('   %-13s carries a terminal and imports terminal_value nowhere' % tk)
        print('\nFour gates police the terminal and every one of them reads a committed '
              'terminal record, so a hand-rolled terminal is examined by none of them and '
              'passes all four. Build it through terminal_value.build() and commit the '
              'record it returns.')
        return 1

    print('\nOK — every study with a terminal builds it through the sanctioned module, or '
          'is on the ratchet.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
