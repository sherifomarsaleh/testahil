#!/usr/bin/env python3
"""[R-ENF-01] THE EXEMPLAR IS HELD TO THE STANDARD THE EXEMPLAR DEFINES.

CLAUDE.md says of the model report: "OPEN IT BESIDE THE STUDY YOU ARE WRITING. Every study
matches its sections list, its sheet list, its content and its depth." That instruction is
the mechanism by which this house's standards propagate — a new study is built by matching
the exemplar, not by reading twenty rules and hoping.

MEASURED ON 04-SEP-2026, THE EXEMPLAR WAS OUTSTANDING ON EIGHT OF THEM AT ONCE: the
study-provenance ratchet, the lens-design ratchet ([R-LENS-03], so it still publishes a
typed four-lens blend), the bridge ratchet ([R-BRIDGE-01]), the cost-of-capital ratchet
([R-COC-01]), the macro-path ratchet ([R-MACRO-01]), the forecast-anchor ratchet
([R-ANCHOR-01]), the output-records ratchet ([R-ENF-05]), and the valuation-gap ratchet —
where it is listed as UNREADABLE, meaning the gate cannot recover a central and a spot from
the document every other study is modelled on.

NONE OF THOSE ENTRIES IS ITSELF WRONG. Every ratchet exists precisely so that work
predating a standard is listed rather than making the build permanently red [R-ENF-02].
What is wrong is that NOTHING WAS COUNTING THEM ON THIS PARTICULAR STUDY, and this study is
not one among twenty-four: A NEW STUDY BUILT BY OPENING IT INHERITS EVERY ONE OF THOSE
CONSTRUCTIONS, and inherits them looking exactly like the house standard, because the
document it is copied from is the house standard.

THIS GATE DOES NOT DEMAND THE DEBT BE ZERO, and saying so is the point. Bringing a
published study to eight standards at once is a re-issue, which is an explicitly-requested
step; a gate red from the day it is written is the check everyone learns to ignore. What it
demands is that THE DEBT MAY NOT GROW: from adoption, a new standard must either be MET by
the exemplar or CONSCIOUSLY ADDED to this list — which is the choice being made either way,
and the only question is whether anybody sees it being made.

Today's two standards were met rather than added, which is the precedent this is written to
set: the exemplar appears on neither the waterfall ratchet nor the sign-convention one.

Population-anchored [R-ENF-04] BOTH WAYS: a run finding zero ratchet files FAILS, and so
does one finding no exemplar on disk as a study — REFERENCE_SET is closed at three names
and at least one of them is a study directory, so an empty population means the resolver
broke, not that the debt is clear.
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import research_protocol as R                                          # noqa: E402

AUDIT = os.path.join(ROOT, 'engine', 'build_depth_audit')
RATCHET = os.path.join(AUDIT, 'exemplar_outstanding.json')


def survey():
    """(entries, ratchet files read, exemplars on disk).

    An entry is "EXEMPLAR:ratchet.json:list", so a name moving between two lists of the
    same ratchet — outstanding to unreadable, say — reads as a change rather than as
    nothing. That distinction is the one [R-TERM-01]'s negative control had to learn: an
    allowance for reading badly does not excuse a study that cannot be read.
    """
    on_disk = [t for t in R.REFERENCE_SET
               if os.path.isdir(os.path.join(ROOT, 'engine', '%s_study' % t.lower()))]
    entries, files = [], 0
    for f in sorted(glob.glob(os.path.join(AUDIT, '*_outstanding.json'))
                    + glob.glob(os.path.join(AUDIT, 'outstanding.json'))):
        if os.path.abspath(f) == os.path.abspath(RATCHET):
            continue                                  # this gate's own list is not a debt
        try:
            d = json.load(open(f))
        except (ValueError, OSError):
            continue
        files += 1
        if not isinstance(d, dict):
            continue
        # A RATCHET STORES ITS ENTRIES IN FOUR SHAPES AND THIS GATE READ ONE OF THEM
        # [WIDENED 05-Sep-2026]. The first draft matched only a list item equal to a
        # ticker, so it was blind to: a group stored as a DICT keyed by ticker (which is
        # how terminal_outstanding and lens_vocabulary_outstanding store theirs), a list
        # of FILE PATHS (band_outstanding.documents), and a dict keyed by path
        # (edition_outstanding). Measured on the exemplar the night this was found:
        # ADNOCLS sits in FIVE ratchets and the gate reported ONE — and the rule's own
        # adoption note records it as outstanding on EIGHT when it was written, so this
        # has been under-reporting since the day it shipped.
        #
        # THE GATE WHOSE WHOLE PURPOSE IS TO NOTICE THE EXEMPLAR ACQUIRING DEBT COULD NOT
        # SEE FOUR FIFTHS OF IT. That is [R-ENF-04] in the place it costs most, because
        # the exemplar is how this house's standards propagate: a debt on it is a debt
        # every study written afterwards inherits without anybody deciding to take it on.
        for key, val in d.items():
            if isinstance(val, list):
                names = [str(x) for x in val if not isinstance(x, (list, dict))]
            elif isinstance(val, dict):
                names = [str(k) for k in val]
            else:
                continue
            if not names:
                continue
            for tk in R.REFERENCE_SET:
                # the bare ticker, or a path naming that study's own directory, or a
                # document whose filename starts with it — a path is how three ratchets
                # record a document rather than a name
                needle = '%s_study/' % tk.lower()
                if any(x.upper() == tk
                       or needle in x.replace(os.sep, '/').lower()
                       or os.path.basename(x).upper().startswith(tk + '_')
                       for x in names):
                    entries.append('%s:%s:%s' % (tk, os.path.basename(f), key))
    return sorted(set(entries)), files, on_disk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true',
                    help='rewrite the list with what is outstanding now; it may only '
                         'ever SHORTEN')
    a = ap.parse_args()

    entries, files, on_disk = survey()
    allowed = (set(json.load(open(RATCHET))['outstanding'])
               if os.path.exists(RATCHET) else set())

    if files == 0:
        print('FAIL — read zero ratchet files under engine/build_depth_audit/. An absent '
              'answer is not a clean one; the debt is not clear, the resolver is broken.')
        return 1
    if not on_disk:
        print('FAIL — no member of REFERENCE_SET %s resolves to a study directory. The '
              'reference set is closed at three names and the exemplar is one of them, so '
              'an empty population means the resolver broke.' % (R.REFERENCE_SET,))
        return 1

    print('reference set %s; %s on disk as a stud%s; %d ratchet file(s) read; %d '
          'outstanding entr%s'
          % (', '.join(R.REFERENCE_SET), ', '.join(on_disk),
             'y' if len(on_disk) == 1 else 'ies', files, len(entries),
             'y' if len(entries) == 1 else 'ies'))
    for e in entries:
        print('%s%s' % ('   ' if e in allowed else '>> ', e))

    new = sorted(set(entries) - allowed)

    if a.prune:
        if allowed and new:
            print('REFUSED — --prune may only ever SHORTEN; %s would be added'
                  % ', '.join(new))
            return 1
        json.dump({'rule': 'R-ENF-01 / the exemplar is held to the standard it defines',
                   'note': 'Standards the model report is outstanding on. It may only ever '
                           'SHORTEN: a new standard is either MET by the exemplar or the '
                           'entry is added here deliberately, in the commit that adopts it.',
                   'outstanding': sorted(entries)}, open(RATCHET, 'w'), indent=1)
        print('list rewritten with %d entr%s'
              % (len(entries), 'y' if len(entries) == 1 else 'ies'))
        return 0

    if new:
        print('\nFAIL — the exemplar has fallen onto %d standard(s) it was not outstanding '
              'on:' % len(new))
        for e in new:
            print('   %s' % e)
        print('\nA study is built by opening the exemplar beside it, so a construction the '
              'exemplar carries propagates to every study written after it, looking exactly '
              'like the house standard. Either bring the exemplar to the new standard, or '
              'add the entry here in the same commit that adopts it — the choice is being '
              'made either way and this is where it is visible.')
        return 1
    print('\nOK — the exemplar has fallen onto no new standard. %d entr%s outstanding, '
          'which may only SHORTEN.'
          % (len(allowed), 'y' if len(allowed) == 1 else 'ies'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
