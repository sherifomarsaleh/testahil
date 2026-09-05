#!/usr/bin/env python3
"""Negative control for the delivered-PDF currency gate.

Each case copies the repository into a sandbox, injects ONE condition, asserts the mutation
LANDED, and asserts the gate behaves as specified. A fixture that quietly changes nothing
produces a green proving only that the file was untouched, which is how controls in this
repository have failed before.

THE CASE THAT MATTERS is a study whose committed central moves while its delivered PDF does
not — because that is exactly what happened, unnoticed, for four hours on 03-Sep-2026 with
every other gate green.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_CASES = 8


def sandbox(tmp):
    dst = os.path.join(tmp, 'repo')
    os.makedirs(dst)
    for p in ('engine', 'scripts'):
        shutil.copytree(os.path.join(REPO, p), os.path.join(dst, p),
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.docx',
                                                      '*.xlsx', '*.png', '*.jpg', '*.csv'))
    return dst


def run(root):
    r = subprocess.run([sys.executable,
                        os.path.join(root, 'scripts', 'check_delivered_pdf_currency.py')],
                       capture_output=True, text=True, cwd=root)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def numbers(root, tk):
    return os.path.join(root, 'engine', f'{tk.lower()}_study', 'study_numbers.json')


def ratchet(root):
    return os.path.join(root, 'engine', 'build_depth_audit', 'pdf_outstanding.json')


# --------------------------------------------------------------------------------------
def _central_moved(root):
    """THE ONE THAT MATTERS — the study's answer moves and the PDF does not."""
    f = numbers(root, 'ARCC')
    d = json.load(open(f))
    before = d['central']
    d['central'] = before * 1.37          # a value no rendered edition carries at any rounding
    json.dump(d, open(f, 'w'), indent=1)
    assert json.load(open(f))['central'] != before, 'mutation did not land'
    return 'ARCC central moved %.2f -> %.2f with the PDF untouched' % (before, d['central'])


def _pdf_removed(root):
    """The delivered PDF disappears. No PDF is not a current PDF."""
    d = os.path.join(root, 'engine', 'arcc_study')
    n = 0
    for f in os.listdir(d):
        if f.endswith('.pdf') and 'Valuation_Study' in f:
            os.remove(os.path.join(d, f)); n += 1
    assert n > 0, 'mutation did not land'
    return 'removed %d ARCC study PDF(s)' % n


def _pdf_emptied(root):
    """A PDF whose opening pages yield no text is not a readable deliverable."""
    import glob
    hits = [f for f in glob.glob(os.path.join(root, 'engine', 'arcc_study', '*.pdf'))
            if 'Valuation_Study' in os.path.basename(f)]
    assert hits, 'fixture found no ARCC study PDF'
    for f in hits:
        open(f, 'wb').write(b'%PDF-1.4\n%%EOF\n')
    return 'emptied %d ARCC study PDF(s)' % len(hits)


def _off_ratchet(root):
    """A real outstanding entry with its allowance removed.

    THE ENTRY IS READ FROM THE RATCHET, NEVER NAMED. This fixture named SCEM, and when
    SCEM was brought onto the standard and pruned off the list the case stopped being
    constructible — the mutation did not land, the control went red, and it went red for
    a reason that has nothing to do with the gate it exists to test. A ratchet may only
    ever SHORTEN, so a control that names one of its entries is a control with an expiry
    date on it. Whichever entry is first is as good a fixture as any, and there is always
    one while the list is non-empty; when the list finally empties this raises with a
    message saying so, which is the honest state and not a failure to work around.
    """
    f = ratchet(root)
    d = json.load(open(f))
    names = sorted(d['entries'])
    assert names, ('the ratchet is empty, so no real outstanding entry exists to remove. '
                   'That is the list having done its job, not a broken fixture — retire '
                   'this case when it happens.')
    # AN ENTRY ON THE RATCHET IS NOT THE SAME AS AN ENTRY STILL BREACHING [fixed
    # 05-Sep-2026]. Taking names[0] assumed every listed name still fails, and a ratchet
    # legitimately carries names that have since been fixed and not yet pruned. On
    # 5 September five entries cleared at once — four studies exposed answers the gate had
    # never been able to read — and the first name alphabetically was one of them, so this
    # fixture removed an allowance nothing needed, the gate stayed correctly GREEN, and the
    # control went red for a reason with nothing to do with the gate it tests. THAT IS THE
    # MUTATION-DID-NOT-LAND FAILURE this file already guards everywhere else: assert the
    # CONDITION, not the edit. So the gate is run first and the fixture picks a name it
    # actually reports as outstanding.
    rc0, out0 = run(root)
    listed = [tk for tk in names
              if re.search(r'^\s+%s\s' % re.escape(tk), out0, re.M)]
    assert listed, ('every name on the ratchet is now passing the gate, so removing an '
                    'allowance cannot make it fail. Prune the list — that is what --prune '
                    'is for — and this case becomes constructible again.')
    tk = listed[0]
    d['entries'].pop(tk)
    json.dump(d, open(f, 'w'), indent=1)
    assert tk not in json.load(open(f))['entries'], 'mutation did not land'
    return '%s removed from the ratchet' % tk


def _empty_population(root):
    """No study directories. An empty result is not a clean result [R-ENF-04]."""
    n = 0
    for d in os.listdir(os.path.join(root, 'engine')):
        if d.endswith('_study'):
            shutil.rmtree(os.path.join(root, 'engine', d)); n += 1
    assert n > 0, 'mutation did not land'
    return 'removed all %d study directories' % n


def _clean_untouched(root):
    return 'nothing changed'


def _clean_superseded_edition(root):
    """A SUPERSEDED edition's PDF left stale beside a current one must NOT fire.

    Only the latest delivered edition is the deliverable. An older one is a dated record and
    is never rewritten — the same append-only discipline the ledgers and gap reviews obey.
    """
    import glob
    olds = [f for f in glob.glob(os.path.join(root, 'engine', 'arcc_study', '*.pdf'))
            if 'Valuation_Study' in os.path.basename(f)
            and '03-09-2026' not in os.path.basename(f)]
    assert olds, 'fixture found no superseded ARCC edition'
    for f in olds:
        open(f, 'wb').write(b'%PDF-1.4\n%%EOF\n')
    return 'emptied %d SUPERSEDED ARCC edition(s); the current one is untouched' % len(olds)



def _one_branch_of_two(root):
    """A TWO-SIDED STUDY WHOSE DOCUMENT SHOWS ONE BRANCH. Half current is not current.

    The condition this reproduces is the one the gate missed on the day it was written:
    PHAR publishes two named branches, its rebuilt model moved both, and its stale
    document happened to carry one of the new figures in its opening pages while the
    headline still read the old one. `any` over the branches passed it. Here only the
    SECOND branch is moved, so the document still shows the first — which is exactly
    the shape that used to pass and must now go red.
    """
    f = numbers(root, 'PHAR')
    d = json.load(open(f))
    br = (d.get('central_two_sided') or {}).get('branches') or []
    assert len(br) >= 2, 'PHAR does not publish two branches; this case tests nothing'
    before = br[1]['value']
    br[1]['value'] = before * 1.41        # a value no rendered edition carries
    json.dump(d, open(f, 'w'), indent=1)
    got = json.load(open(f))['central_two_sided']['branches'][1]['value']
    assert got != before, 'mutation did not land'
    return ('PHAR second branch moved %.2f -> %.2f; the first is untouched, so the '
            'document still shows one of the two' % (before, got))


CASES = [
    ('THE ONE THAT MATTERS — the central moves and the PDF does not', _central_moved, 'red'),
    ('the delivered PDF is removed', _pdf_removed, 'red'),
    ('the delivered PDF yields no text [R-ENF-04]', _pdf_emptied, 'red'),
    ('a real outstanding entry with its allowance removed', _off_ratchet, 'red'),
    ('no study directories at all [R-ENF-04]', _empty_population, 'red'),
    ('a two-sided study whose document shows ONE of its two branches',
     _one_branch_of_two, 'red'),
    ('CLEAN — the repository as it stands', _clean_untouched, 'green'),
    ('CLEAN — a SUPERSEDED edition left stale beside a current one',
     _clean_superseded_edition, 'green'),
]


def main():
    assert len(CASES) == EXPECTED_CASES, (
        'this control declares %d cases and carries %d' % (EXPECTED_CASES, len(CASES)))
    bad = 0
    for i, (name, mutate, want) in enumerate(CASES, 1):
        with tempfile.TemporaryDirectory() as tmp:
            root = sandbox(tmp)
            try:
                what = mutate(root)
            except AssertionError as e:
                print('FAIL %2d. %s\n        the MUTATION did not land: %s' % (i, name, e))
                bad += 1
                continue
            rc, out = run(root)
            got = 'red' if rc != 0 else 'green'
            ok = got == want
            bad += 0 if ok else 1
            print('%s %2d. %-58s %s (%s)' % ('PASS' if ok else 'FAIL', i, name, got, what))
            if not ok:
                for line in out.strip().splitlines()[-6:]:
                    print('        | %s' % line)
    print('\n%d/%d cases behaved as specified' % (len(CASES) - bad, len(CASES)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
