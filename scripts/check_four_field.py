#!/usr/bin/env python3
"""[R-ENF-01] DEPTH-BAR STANDARD 2 IS CHECKED FROM OUTSIDE, AND THE FOURTH FIELD HAS
TWO SPELLINGS.

Standard 2 has required since the bar was written that EVERY input be four-field
complete — value, source, date, and the research layer it came from — "validated by
assertion". What validated it outside the study was research_protocol's
`provenance_four_field`, A BOOLEAN EACH STUDY SETS ON ITSELF: the composite-beta shape
[R-ENF-01] closes everywhere else, and the shape [R-ENF-02 AMENDED] already had to
close once on `structure_matches_model` in the same checklist.

MEASURED 07-09-2026 THE BOOLEAN WAS HONEST, and saying so is part of the finding rather
than a reason not to check: 3,862 inputs across eighteen registers, ZERO incomplete.
A gate is not worth less for finding a book in good order — what it is worth is that
the nineteenth register cannot quietly skip the field, which is what a ratcheted check
is for and what the new-study gauntlet [R-ENF-07] tests.

THE FOURTH FIELD IS SPELLED TWO WAYS AND THAT IS THE REAL FRAGILITY. Five studies
write `layer` (1,622 inputs) and thirteen write `ring` (2,240); none writes both, none
writes neither, and NOTHING OUTSIDE A STUDY READS THE FIELD AT ALL — every occurrence
in scripts/ is a fixture inside a negative control. So a check written naively against
one spelling would have silently passed five studies and condemned thirteen, or the
reverse, and either reading would have looked authoritative. THIS IS THE
CORRECTION-BOUNDARY LESSON IN ANOTHER COSTUME: five records, five shapes, a reader that
guesses finds nothing. Both spellings are accepted HERE rather than renamed across the
book, because renaming 2,240 committed inputs in thirteen delivered studies is a
re-issue and is not done in passing.

MY OWN FIRST MEASUREMENT REPORTED 58% OF THE BOOK MISSING THE FIELD. It read `layer`
only. The register was complete and the reader was ignorant — an absent answer wearing
a clean one's clothes [R-ENF-04], which is why the two spellings are named in code here
instead of remembered.

AN ABSENT REGISTER DEFERS RATHER THAN DUPLICATING [R-ENF-07]. Six studies commit no
inputs register at all, and `source_outstanding.json` already lists exactly those six
as unreadable. This gate reads THAT list rather than opening a second one: two records
of one fact diverge the moment somebody prunes one. It therefore carries NO RATCHET OF
ITS OWN, deliberately — there is nothing outstanding that another list does not
already hold, and an allowance created for nothing is an allowance nobody maintains.

POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: a run examining zero study directories FAILS,
and so does one that read zero INPUTS across present directories.
"""

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
DEFERRED = os.path.join(ENGINE, 'build_depth_audit', 'source_outstanding.json')

# The fourth field, both spellings. NAMED, never guessed — see the docstring.
FOURTH = ('layer', 'ring')
REQUIRED = ('source', 'date')


def deferred_unreadable():
    """Studies another list already records as having no readable register."""
    try:
        return set(json.load(open(DEFERRED, encoding='utf-8')).get('unreadable', []))
    except Exception:
        return set()


def numbers_file(study_dir):
    cands = [c for c in sorted(glob.glob(os.path.join(study_dir, '*numbers*.json')))
             if '_v1' not in os.path.basename(c)
             and 'gap_review' not in os.path.basename(c)]
    return cands[0] if len(cands) == 1 else None


def audit(inputs):
    """Every input carrying a value, and what it is missing. Never a threshold."""
    n, bad = 0, []
    for key, v in inputs.items():
        if not isinstance(v, dict) or 'value' not in v:
            continue          # a note or a block, not an input
        n += 1
        missing = [f for f in REQUIRED if not str(v.get(f) or '').strip()]
        if not any(str(v.get(f) or '').strip() for f in FOURTH):
            missing.append('/'.join(FOURTH))
        if missing:
            bad.append((key, missing))
    return n, bad


def main(argv):
    deferred = deferred_unreadable()
    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    rows, fail = [], []
    total_inputs = 0

    for d in dirs:
        tk = os.path.basename(d)[:-len('_study')].upper()
        nf = numbers_file(d)
        if nf is None:
            rows.append((tk, 'no unambiguous numbers file', 0, []))
            continue
        try:
            doc = json.load(open(nf, encoding='utf-8'))
        except Exception as exc:
            rows.append((tk, 'will not parse: %s' % str(exc)[:70], 0, []))
            continue
        inputs = doc.get('inputs') or {}
        n, bad = audit(inputs)
        total_inputs += n
        rows.append((tk, 'read', n, bad))

    print('FOUR-FIELD PROVENANCE GATE  [R-ENF-01]')
    print('   every input carries value, source, date and its research layer —')
    print('   the fourth field spelled %s, both accepted, neither guessed'
          % ' or '.join(FOURTH))
    readable = [r for r in rows if r[1] == 'read' and r[2]]
    print('   %d study directories · %d with a readable register · %d inputs'
          % (len(dirs), len(readable), total_inputs))

    # ---- population anchoring, both ways [R-ENF-04] ---------------------------------
    if not dirs:
        print('\nFAIL — the gate examined ZERO study directories. An empty result is '
              'not a clean result.')
        return 1
    if not total_inputs:
        print('\nFAIL — the gate read ZERO inputs across %d study directories. That is '
              'an absent answer wearing the costume of a clean one: either every '
              'register moved or the reader is looking in the wrong place.' % len(dirs))
        return 1

    on_disk = {os.path.basename(d)[:-len('_study')].upper() for d in dirs}
    for tk in sorted(deferred):
        if tk not in on_disk:
            fail.append('the deferred unreadable list names %s and no such study '
                        'directory exists — this gate is anchored on nothing' % tk)

    for tk, state, n, bad in rows:
        if state != 'read':
            if tk in deferred:
                continue                      # already owned by source_outstanding
            fail.append('%s: %s. An unreadable study is not a clean study [R-ENF-04], '
                        'and it is not on the deferred unreadable list.' % (tk, state))
            continue
        if n == 0:
            if tk in deferred:
                continue
            fail.append('%s commits no inputs register and is not on the deferred '
                        'unreadable list. Standard 2 cannot be met by a register that '
                        'does not exist.' % tk)
            continue
        if bad:
            fail.append('%s: %d of %d inputs are not four-field complete, e.g. %s '
                        'missing %s' % (tk, len(bad), n, bad[0][0],
                                        ', '.join(bad[0][1])))
            print('    %-12s %d of %d INCOMPLETE' % (tk, len(bad), n))
            for key, miss in bad[:4]:
                print('        %s missing %s' % (key, ', '.join(miss)))

    absent = [r[0] for r in rows if (r[1] != 'read' or r[2] == 0)]
    if absent:
        print('\n  NO READABLE REGISTER: %s' % ', '.join(sorted(absent)))
        print('  deferred to build_depth_audit/source_outstanding.json (unreadable), '
              'which already holds this fact — a second list would diverge from it')

    if fail:
        print('\nFAIL')
        for f in fail:
            print('  - ' + f)
        return 1
    print('\nOK — every committed input carries all four fields.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
