#!/usr/bin/env python3
"""Negative control for scripts/check_new_study_gauntlet.py.  [R-ENF-07]

The gauntlet asserts a property of the whole system — that a new study directory is refused
everywhere — so its own falsifier is a WEAKENED GATE. This weakens one gate at a time, in a
sandbox, and asserts the gauntlet notices. A gauntlet that stays green while a gate has been
told to ignore unknown studies would be the most comfortable check in the repository and the
least informative.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAUNTLET = os.path.join('scripts', 'check_new_study_gauntlet.py')


def sandbox():
    tmp = tempfile.mkdtemp(prefix='gauntlet_nc_')
    def ignore(d, names):
        return [n for n in names
                if n in ('.git', '__pycache__', 'raw_ohlc', 'panels', 'node_modules',
                         'filings')]
    shutil.copytree(ROOT, os.path.join(tmp, 'repo'), ignore=ignore, symlinks=True)
    return tmp, os.path.join(tmp, 'repo')


def run(repo):
    r = subprocess.run([sys.executable, GAUNTLET], cwd=repo,
                       capture_output=True, text=True, timeout=2400)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


CASES = []


def case(name, must_fail, mutate, expect=None):
    CASES.append((name, must_fail, mutate, expect))


def _over_ratchet(*ratchets):
    """Seed the unknown ticker into a gate's own outstanding list.

    THIS REPLACED A MUTATION THAT NEVER LANDED. The first draft tried to blind a gate by
    inserting an early `continue` into its loop with a regex, the regex matched nothing, and
    all three cases reported the gauntlet green — proving only that the gates were
    unchanged. That is the third time in this session a negative control has been caught
    passing a fixture that never injected its condition, and it is the reason every one of
    them now asserts the mutation landed.

    It is also the more faithful test. A gate does not go blind by someone editing its loop;
    it goes blind when a RATCHET is seeded one entry too generously, which is a one-line
    edit anybody could make in good faith and which the ratchet's own --prune would then
    preserve. That is the hole this whole design is exposed to, so that is the hole to test.
    """
    def go(repo):
        import json as _j
        for r in ratchets:
            p = os.path.join(repo, 'engine', 'build_depth_audit', r)
            d = _j.load(open(p, encoding='utf-8'))
            before = _j.dumps(d)
            if 'entries' in d:
                d['entries']['ZZTEST'] = 'seeded by the negative control'
            elif 'outstanding' in d:
                d['outstanding'] = sorted(set(d['outstanding']) | {'ZZTEST'})
            elif 'unreadable' in d:
                d['unreadable'] = sorted(set(d.get('unreadable', [])) | {'ZZTEST'})
            else:
                raise AssertionError('unknown ratchet shape in %s: %s' % (r, list(d)))
            _j.dump(d, open(p, 'w', encoding='utf-8'), indent=1)
            assert _j.dumps(d) != before, 'the mutation did not land in %s' % r
    return go


case("1. the gap ratchet seeded one entry too generously — the gate then passes an "
     "unknown study", True, _over_ratchet('gap_outstanding.json'), 'check_valuation_gap.py')
case('2. the document ratchet seeded with the unknown study', True,
     _over_ratchet('document_outstanding.json'), 'check_document_structure.py')
case('3. the prose ratchet seeded with the unknown study', True,
     _over_ratchet('prose_outstanding.json'), 'check_prose_figures.py')
case('4. EVERY ratchet seeded — the whole design defeated in one edit per list', True,
     _over_ratchet('gap_outstanding.json', 'document_outstanding.json',
                   'prose_outstanding.json', 'bridge_outstanding.json',
                   'sweep_outstanding.json', 'vocabulary_outstanding.json',
                   'workbook_outstanding.json', 'macro_outstanding.json',
                   'lens_outstanding.json', 'coc_outstanding.json',
                   'output_outstanding.json', 'anchor_outstanding.json',
                   'artefact_outstanding.json', 'outstanding.json'),
     'refuse a new study')


def _delete(gate):
    def go(repo):
        os.remove(os.path.join(repo, 'scripts', gate))
    return go


case('5. a gate named in the list is deleted [R-ENF-04]', True,
     _delete('check_bridge.py'), 'do not exist')
case('6. an EXCLUDED gate is deleted — the exclusions are claims too [R-ENF-04]', True,
     _delete('check_lens_vocabulary.py'), 'do not exist')
case('7. CLEAN — nothing weakened', False, lambda repo: None)


EXPECTED_CASES = 7          # a dropped case is a green that proves nothing


def main():
    assert len(CASES) == EXPECTED_CASES, (
        'this file declares %d cases and %d are registered — a case lost to an edit is '
        'a green that proves nothing, which has now happened three times in this '
        'repository' % (EXPECTED_CASES, len(CASES)))
    bad = 0
    for name, must_fail, mutate, expect in CASES:
        tmp, repo = sandbox()
        try:
            mutate(repo)
            rc, out = run(repo)
            red = rc != 0
            ok = (red == must_fail) and (expect is None or expect in out)
            print('%-4s %s' % ('PASS' if ok else 'FAIL', name))
            if not ok:
                bad += 1
                print('      rc=%d wanted %s%s' % (
                    rc, 'RED' if must_fail else 'GREEN',
                    (' containing %r' % expect) if expect else ''))
                print('      ' + '\n      '.join(out.strip().splitlines()[-8:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print('\n%d/%d cases behaved as specified' % (len(CASES) - bad, len(CASES)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
