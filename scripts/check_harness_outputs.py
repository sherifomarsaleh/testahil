#!/usr/bin/env python3
"""A COMMITTED NUMBERS FILE THAT IS ACTUALLY A PRICING-HARNESS RUN [L-293].

    python3 scripts/check_harness_outputs.py [--prune]

WHY THIS EXISTS. Three studies carry an override harness so that an audit finding can
be PRICED on the real chain rather than on a re-implementation -- which is right, and is
the [R-ENF-03] discipline applied to pricing a critique. One of them wrote its overridden
run STRAIGHT OVER the committed study_numbers.json, and the file it left behind LOOKED
PERFECTLY CLEAN.

WHAT MAKES IT INVISIBLE, AND IT IS NOT CARELESSNESS. Every other block in that file was
internally coherent, because it was a complete and correct run of the model -- of a model
answering a different question. Worse, the BETA RECORD still reported the registered
0.488, because a record is written from the input's own metadata rather than from the
value the model actually used: the file asserted a beta the run had not used. No gate in
this repository could see it. The four-field register was complete, the workbook
reconciled every formula cell against the file, the document builders read the file and
rendered it faithfully, and the answer was a solved-for number that happened to equal
the market price to seven decimal places.

It was found because a figure printed for an unrelated purpose was one somebody
recognised. That is not a control.

WHAT THIS CHECKS. Two mechanical conditions, neither needing judgement:

  (1) A committed study_numbers.json carrying an `override` block is a harness run and
      is REFUSED. The block is what an honest harness writes about itself.
  (2) A study whose compute.py reads an override environment variable must not write the
      committed file on that path -- the output name has to depend on whether the
      override was set. A harness that CAN overwrite the study eventually does, and
      making the safe path the DEFAULT is the only version of this that survives
      somebody being in a hurry.

WHAT IT DELIBERATELY DOES NOT CHECK. Whether the numbers in a clean file are right --
that is what every other gate is for. This one asks only whether the file is the run the
study claims it is.

The population is the study directories on disk [R-ENF-04]: a run that examined zero
numbers files, or found zero harnesses to test condition (2) against, reports the counts
and FAILS on an empty population rather than reporting clean.
"""
import ast
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'harness_outputs_outstanding.json')

# An environment variable whose name ends this way is an override switch. Matching by
# SHAPE rather than by a list of known names, for the reason the delivered-vocabulary
# gate gives: a list of names cannot be complete, and a study inventing a fourth
# harness would be invisible to one.
OVERRIDE_ENV = re.compile(r'^[A-Z][A-Z0-9_]*_OVERRIDE$')


def _env_reads(tree):
    """Override environment variables this module reads, by name."""
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if getattr(fn, 'attr', None) not in ('get', 'getenv'):
            continue
        for a in node.args:
            if isinstance(a, ast.Constant) and isinstance(a.value, str) \
                    and OVERRIDE_ENV.match(a.value):
                found.add(a.value)
    return found


def _writes_committed_unconditionally(tree, src):
    """True if the module can write study_numbers.json on the override path.

    The safe shape makes the OUTPUT NAME depend on whether the override was set. So
    the test is whether any string mentioning study_numbers.json that reaches a write
    is a bare constant with no alternative beside it -- i.e. whether the file name is
    a decision the code makes, or one it has already made.
    """
    if 'study_numbers.json' not in src:
        return True
    # a conditional expression, an if-statement or a dict/......get default that selects
    # between two output names is the safe shape.
    for node in ast.walk(tree):
        if isinstance(node, ast.IfExp) and 'study_numbers' in ast.dump(node):
            return False
        if isinstance(node, ast.If) and 'study_numbers' in ast.dump(node):
            return False
        if isinstance(node, ast.Call):
            fn = node.func
            if getattr(fn, 'attr', None) in ('get', 'getenv') and \
                    'study_numbers' in ast.dump(node):
                return False
    return True


def main(argv):
    prune = '--prune' in argv
    d, known = {}, set()
    if os.path.exists(OUTSTANDING):
        d = json.load(open(OUTSTANDING, encoding='utf-8'))
        known = set(d.get('outstanding', []))

    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    if not dirs:
        print('FAIL - the population is empty: no engine/*_study directories were '
              'found. An empty result is not a clean result [R-ENF-04].')
        return 1

    numbers_read, harnesses, bad, clean = 0, 0, {}, []
    for dd in dirs:
        tk = os.path.basename(dd)[:-6].upper()
        nf = os.path.join(dd, 'study_numbers.json')
        if os.path.exists(nf):
            numbers_read += 1
            try:
                D = json.load(open(nf, encoding='utf-8'))
            except Exception as e:
                bad.setdefault(tk, []).append('study_numbers.json will not parse: %s' % e)
                D = None
            if isinstance(D, dict) and 'override' in D:
                ov = D.get('override') or {}
                bad.setdefault(tk, []).append(
                    'the COMMITTED study_numbers.json is a pricing-harness run: it carries '
                    'an override block over %s. Re-run the model with no override set.'
                    % ', '.join(sorted((ov.get('inputs') or {}))) or 'unnamed inputs')

        cf = os.path.join(dd, 'compute.py')
        if os.path.exists(cf):
            src = open(cf, encoding='utf-8').read()
            try:
                tree = ast.parse(src, filename=cf)
            except SyntaxError as e:
                bad.setdefault(tk, []).append('compute.py does not parse: %s' % e)
                continue
            envs = _env_reads(tree)
            if envs:
                harnesses += 1
                if _writes_committed_unconditionally(tree, src):
                    bad.setdefault(tk, []).append(
                        'compute.py reads %s and writes study_numbers.json on the same '
                        'path: an overridden run replaces the committed study and the '
                        'file it leaves behind is internally coherent, so nothing '
                        'downstream can tell. Select the output name from whether the '
                        'override is set.' % ', '.join(sorted(envs)))
                else:
                    clean.append('%-12s harness %s writes beside the committed file'
                                 % (tk, ', '.join(sorted(envs))))

    if numbers_read == 0:
        print('FAIL - %d study directories and not one committed study_numbers.json was '
              'read. An absent answer is not a clean one [R-ENF-04].' % len(dirs))
        return 1
    if harnesses == 0:
        print('FAIL - not one pricing harness was found across %d studies. This gate '
              'exists to hold them; finding none means the detector stopped matching, '
              'not that the risk went away [R-ENF-04].' % len(dirs))
        return 1

    print('study directories: %d   committed numbers files read: %d   pricing harnesses: %d'
          % (len(dirs), numbers_read, harnesses))
    for line in clean:
        print('   ok   ' + line)

    if prune:
        still = sorted(t for t in known if t in bad)
        json.dump({'outstanding': still, 'note': d.get('note', '')},
                  open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
        print('pruned: %d -> %d' % (len(known), len(still)))
        return 0

    new = {t: v for t, v in bad.items() if t not in known}
    for t in sorted(bad):
        for line in bad[t]:
            print('   %-12s %s   %s' % (t, line, '[outstanding]' if t in known else '[NEW]'))
    if new:
        print('\nFAIL - %d study/studies newly in breach: %s'
              % (len(new), ', '.join(sorted(new))))
        return 1
    print('\nOK - no new violations. %d on the ratchet, which may only SHORTEN.' % len(known))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
