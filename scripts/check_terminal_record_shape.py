#!/usr/bin/env python3
"""[R-ENF-01] A COMMITTED RECORD CARRIES THE SHAPE THE MODULE THAT WRITES IT EMITS TODAY.

FOUND BY ASKING WHETHER EACH STUDY'S COMMITTED NUMBERS FILE STILL REPRODUCES FROM
ITS OWN GENERATORS, which nothing in this repository had ever asked. Nineteen of
twenty-four reproduce byte for byte; THREE DIFFER AND ALL THREE DIFFER THE SAME WAY
— engine/terminal_value.py grew five fields after those studies last built, so their
committed terminal records carry the old shape (FERTIGLOBE 4 records, PHAR 2, SCEM
1; the missing fields are maintenance_age_basis, maintenance_age_years,
maintenance_escalator and the two average_age inputs).

NOTHING VALUED HAD MOVED AND SAYING SO IS PART OF THE FINDING, not a mitigation of
it: the escalator is APPLIED inside build() and always was, so every terminal in
those studies was struck at current cost exactly as [R-TERM-01] requires. What was
missing is the record OF it — which is [R-ENF-06] one level up, and the reason it
matters is the same: a record that does not name the quantity a value was built
from cannot be checked, rebuilt or graded afterwards, and it looks complete while
it cannot.

WHY EVERY EXISTING GATE WAS BLIND IS A PROPERTY OF THOSE GATES RATHER THAN AN
OVERSIGHT IN THEM. check_terminal_floor reads the census and tests the 1/g
SIGNATURE — a relationship between figures, which these records carry correctly.
check_artefact_currency [R-ENF-06] asks whether an artefact declares the ANSWER it
was built against, and these declare it. check_numbers_generators says in its own
docstring that it deliberately does NOT test reproduction, because running every
study's model takes minutes. So the shape of a committed record was governed by
nothing at all — and THE CHEAP TEST TURNS OUT TO FIND EXACTLY WHAT THE EXPENSIVE ONE
DOES: this gate names the same three studies as re-running all twenty-four models,
in under a second, because the only thing that had drifted was a field set.

WHAT IT CHECKS: no key the module emits TODAY is ABSENT from a committed record.
EXTRA keys are not a defect and must not fire — a study may carry its own context
beside the module's, and a gate refusing that would push studies to strip context to
stay green. The standard is LEARNED BY RUNNING build() on a canonical input rather
than by parsing the dict literal or carrying a copy of the key list: a check holding
its own copy of a standard stops testing the standard the moment one of them moves
([R-ENF-02]'s own lesson), and a check that PARSES the emission path is checking a
different file from the one that runs ([R-ENF-03]).

A STUDY WITH NO TERMINAL RECORD IS NOT A FAILING STUDY. Eleven of twenty-four carry
none — banks, holdcos and studies whose terminal predates the module — and demanding
one here would be a FALSE CLAIM about what this gate checks. That is why it is
ARTEFACT-conditional in the new-study gauntlet [R-ENF-07].

RATCHET [R-ENF-02]: the list starts EMPTY because all three were conformed rather
than listed — regenerating adds the fields and deletes nothing, and no valued figure
in any of the three moved. One of them needed its generator fixed first and that is
the more useful half: FERTIGLOBE stamped meta.asof with date.today(), which
docx_fertiglobe.py prints as "Study date", so REBUILDING IT RESTAMPED A DELIVERED
DOCUMENT'S ACCOUNT OF WHEN THE WORK WAS DONE. Frozen to the date the delivered
document already carries, which commits a fact rather than inventing one.

POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: a run that examined zero study directories
FAILS, and so does one that read zero terminal records across present directories —
that second is the absent answer wearing a clean one's clothes, and it is the state
this gate would silently enter if the record key ever changed name.
"""

import glob
import json
import os
import sys
from dataclasses import fields

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
sys.path.insert(0, ENGINE)
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'terminal_record_outstanding.json')

RULE = 'R-TERM-01'


def reference_shape():
    """The key set the module emits TODAY, learned by RUNNING it.

    Not by parsing the dict literal and not from a copy kept here: [R-ENF-03] — a
    checker that models the emission path is checking a different file from the one
    that runs. If build() cannot produce a record the gate cannot learn the standard
    and says so rather than passing.
    """
    import terminal_value as tv
    t = tv.build(tv.TerminalInputs(
        nopat=100.0, wacc=0.12, inflation=0.05, real_growth=0.0, dna_book=20.0,
        ic_replacement=500.0, useful_life_years=20.0,
        useful_life_source='canonical fixture — accounting-policies note'))
    top = set(t.record)
    inp = {f.name for f in fields(tv.TerminalInputs)}
    if not top or not inp:
        raise RuntimeError('the reference record is empty')
    return top, inp


def numbers_file(study_dir):
    """The study's committed numbers file, or None where it is not unambiguous.

    Ambiguity is REPORTED, never resolved by picking one: a gate that guesses which
    of two numbers files a study publishes is guessing at the subject.
    """
    cands = [c for c in sorted(glob.glob(os.path.join(study_dir, '*numbers*.json')))
             if '_v1' not in os.path.basename(c) and 'gap_review' not in os.path.basename(c)]
    return cands[0] if len(cands) == 1 else None


def walk_records(node, path=''):
    """Every dict the module stamped, found by its own rule marker."""
    if isinstance(node, dict):
        if node.get('rule') == RULE:
            yield path or '<root>', node
        for k, v in node.items():
            yield from walk_records(v, f'{path}.{k}' if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_records(v, f'{path}[{i}]')


def load_ratchet():
    if not os.path.exists(OUTSTANDING):
        return []
    return json.load(open(OUTSTANDING, encoding='utf-8')).get('outstanding', [])


def census(top, inp):
    rows = []
    for d in sorted(glob.glob(os.path.join(ENGINE, '*_study'))):
        tk = os.path.basename(d)[:-len('_study')].upper()
        nf = numbers_file(d)
        if nf is None:
            rows.append(dict(ticker=tk, state='unreadable',
                             why='no unambiguous numbers file'))
            continue
        try:
            doc = json.load(open(nf, encoding='utf-8'))
        except Exception as exc:
            rows.append(dict(ticker=tk, state='unreadable',
                             why='numbers file will not parse: %s' % str(exc)[:90]))
            continue
        recs = list(walk_records(doc))
        stale = []
        for path, rec in recs:
            miss_top = sorted(top - set(rec))
            miss_inp = sorted(inp - set(rec.get('inputs', {}) or {}))
            if miss_top or miss_inp:
                stale.append((path, miss_top, miss_inp))
        rows.append(dict(ticker=tk, state='read', n=len(recs), stale=stale))
    return rows


def main(argv):
    prune = '--prune' in argv
    try:
        top, inp = reference_shape()
    except Exception as exc:
        print('TERMINAL RECORD SHAPE GATE  [R-ENF-01]')
        print('\nFAIL — the gate could not learn the standard: terminal_value.build() '
              'did not produce a reference record (%s). A gate that cannot read the '
              'standard has not checked anything.' % str(exc)[:160])
        return 1

    rat = load_ratchet()
    rows = census(top, inp)
    read = [r for r in rows if r['state'] == 'read']
    dark = [r for r in rows if r['state'] == 'unreadable']
    total_recs = sum(r['n'] for r in read)
    carrying = [r for r in read if r['n']]

    print('TERMINAL RECORD SHAPE GATE  [R-ENF-01]')
    print('   a committed record carries the field set engine/terminal_value.py emits')
    print('   TODAY — learned by running build(), never from a copy kept here')
    print('   %d study directories · %d readable · %d carrying a terminal record · '
          '%d records · %d fields (%d top-level, %d inputs)'
          % (len(rows), len(read), len(carrying), total_recs,
             len(top) + len(inp), len(top), len(inp)))

    fail = []

    # ---- population anchoring, both ways [R-ENF-04] ----------------------------------
    if not rows:
        print('\nFAIL — the gate examined ZERO study directories. An empty result is not '
              'a clean result.')
        return 1
    if not total_recs:
        print('\nFAIL — the gate read ZERO terminal records across %d study directories. '
              'That is an absent answer wearing the costume of a clean one: either the '
              'record marker %r has moved or the numbers files are not being read.'
              % (len(rows), RULE))
        return 1

    on_disk = {r['ticker'] for r in rows}
    for tk in sorted(rat):
        if tk not in on_disk:
            fail.append('the ratchet lists %s and no such study directory exists — the '
                        'list is anchored on nothing' % tk)

    for r in dark:
        fail.append('%s: %s. An unreadable study is not a clean study [R-ENF-04].'
                    % (r['ticker'], r['why']))

    stale_rows = [r for r in read if r['stale']]
    print('\n  RECORDS SHORT OF THE CURRENT SHAPE: %d studies'
          % len(stale_rows))
    cleared = []
    for r in sorted(stale_rows, key=lambda r: r['ticker']):
        tk = r['ticker']
        mark = 'ratcheted' if tk in rat else 'NEW'
        print('    %-12s %d of %d records  [%s]' % (tk, len(r['stale']), r['n'], mark))
        for path, mt, mi in r['stale'][:3]:
            print('        %s  missing top=%s inputs=%s' % (path, mt, mi))
        if tk not in rat:
            fail.append('%s commits %d terminal record(s) short of the field set '
                        'terminal_value.build() emits today. Rebuild the study\'s '
                        'numbers from its own generator; the module writes the record.'
                        % (tk, len(r['stale'])))
    for tk in sorted(rat):
        if tk in on_disk and tk not in {r['ticker'] for r in stale_rows}:
            cleared.append(tk)

    if cleared:
        print('\n  RATCHET ENTRIES NOW CLEAN: %s' % ', '.join(cleared))
        if prune:
            keep = [t for t in rat if t not in cleared]
            json.dump({'rule': 'R-ENF-01/R-TERM-01', 'outstanding': keep},
                      open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
            print('  --prune: list shortened to %d' % len(keep))
        else:
            print('  run with --prune to shorten the list (it may only ever SHORTEN)')

    if fail:
        print('\nFAIL')
        for f in fail:
            print('  - ' + f)
        return 1
    print('\nOK — every committed terminal record carries the current field set.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
