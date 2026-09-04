#!/usr/bin/env python3
"""Negative control for [R-ENF-01]'s exemplar-debt gate.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. Every mutation is asserted to have LANDED
before the gate runs, because a fixture that silently fails to inject its condition
produces a green run proving only that the file was untouched — the [R-ENF-04] species,
and how this repository's earlier controls have failed.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = 'scripts/check_exemplar_debt.py'


def sandbox():
    d = tempfile.mkdtemp(prefix='xd-nc-')
    dst = os.path.join(d, 'repo')
    os.makedirs(dst)
    for item in ('scripts', 'engine'):
        shutil.copytree(os.path.join(ROOT, item), os.path.join(dst, item),
                        ignore=shutil.ignore_patterns('*.pdf', '*.png', '*.xlsx', '*.docx',
                                                      '__pycache__', 'raw_ohlc',
                                                      'raw_indices', 'lab', 'panels'))
    return d, dst


def run(cwd):
    p = subprocess.run([sys.executable, GATE], cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def a_new_standard_the_exemplar_misses(dst):
    """A standard adopted tomorrow whose ratchet names the exemplar."""
    p = os.path.join(dst, 'engine', 'build_depth_audit', 'newthing_outstanding.json')
    json.dump({'rule': 'a standard adopted tomorrow',
               'outstanding': ['ADNOCLS', 'PHDC']}, open(p, 'w'), indent=1)
    assert 'ADNOCLS' in json.load(open(p))['outstanding']
    return 'newthing'


def the_exemplar_moves_between_lists(dst):
    """UNREADABLE to BREACHING on the same ratchet is a change, not nothing.

    THE FIXTURE PLANTS ITS OWN STARTING STATE RATHER THAN ASSUMING ONE. This case read
    the live ratchet and required ADNOCLS to be sitting on the unreadable list, which it
    was on the day the case was written and is not any more — the exemplar's answer was
    made readable on 4 September 2026 and every entry it held was cleared. The case then
    failed for a reason that has nothing to do with the property it tests, which reads
    exactly like failing for the right one. A ratchet may only ever SHORTEN, so any
    control that names one of its entries has an expiry date on it; this one plants the
    entry, moves it, and asserts BOTH steps landed.
    """
    p = os.path.join(dst, 'engine', 'build_depth_audit', 'gap_outstanding.json')
    d = json.load(open(p))
    d.setdefault('unreadable', [])
    if not any(str(x).upper() == 'ADNOCLS' for x in d['unreadable']):
        d['unreadable'].append('ADNOCLS')
    json.dump(d, open(p, 'w'), indent=1)
    d = json.load(open(p))
    assert any(str(x).upper() == 'ADNOCLS' for x in d['unreadable']), \
        'fixture never injected: ADNOCLS is not on the unreadable list to move from'
    d['unreadable'] = [x for x in d['unreadable'] if str(x).upper() != 'ADNOCLS']
    d.setdefault('outstanding', []).append('ADNOCLS')
    json.dump(d, open(p, 'w'), indent=1)
    d = json.load(open(p))
    assert 'ADNOCLS' in d['outstanding'] and not any(
        str(x).upper() == 'ADNOCLS' for x in d.get('unreadable', [])), \
        'the move did not land: the exemplar must leave one list and join the other'
    return 'gap_outstanding.json:outstanding'


def no_ratchets_at_all(dst):
    n = 0
    for f in os.listdir(os.path.join(dst, 'engine', 'build_depth_audit')):
        if f.endswith('.json'):
            os.remove(os.path.join(dst, 'engine', 'build_depth_audit', f))
            n += 1
    assert n, 'fixture never injected: no ratchet files were removed'
    return 'zero ratchet files'


def the_exemplar_is_not_a_study(dst):
    p = os.path.join(dst, 'engine', 'adnocls_study')
    assert os.path.isdir(p), 'fixture never injected: the exemplar was not on disk'
    shutil.rmtree(p)
    return 'no exemplar on disk'


def a_debt_that_shortens(dst):
    """Removing the exemplar from a ratchet must stay GREEN — the list may SHORTEN.

    PLANTS ITS OWN STARTING STATE, for the reason the move-between-lists case above
    does: naming a live ratchet entry gives a control an expiry date, and this one
    expired the day the exemplar came off the macro ratchet.
    """
    p = os.path.join(dst, 'engine', 'build_depth_audit', 'macro_outstanding.json')
    d = json.load(open(p))
    if not any(str(x).upper() == 'ADNOCLS' for x in d['outstanding']):
        d['outstanding'].append('ADNOCLS')
        json.dump(d, open(p, 'w'), indent=1)
        d = json.load(open(p))
    assert any(str(x).upper() == 'ADNOCLS' for x in d['outstanding']), \
        'fixture never injected: ADNOCLS is not on the macro ratchet to remove'
    d['outstanding'] = [x for x in d['outstanding'] if str(x).upper() != 'ADNOCLS']
    json.dump(d, open(p, 'w'), indent=1)
    assert not any(str(x).upper() == 'ADNOCLS'
                   for x in json.load(open(p))['outstanding']), 'the removal did not land'
    return 'one fewer'


def a_non_exemplar_joining_a_ratchet(dst):
    """Another study joining a ratchet is ordinary and must NOT fire here."""
    p = os.path.join(dst, 'engine', 'build_depth_audit', 'macro_outstanding.json')
    d = json.load(open(p))
    before = len(d['outstanding'])
    d['outstanding'].append('SCEM')
    json.dump(d, open(p, 'w'), indent=1)
    assert len(json.load(open(p))['outstanding']) == before + 1
    return 'SCEM added'


def clean(dst):
    return ''


CASES = [
    ('1 a standard adopted tomorrow whose ratchet names the exemplar',
     a_new_standard_the_exemplar_misses, True, 'newthing'),
    ('2 the exemplar moving between two lists of one ratchet is a change',
     the_exemplar_moves_between_lists, True, 'gap_outstanding'),
    ('3 zero ratchet files must FAIL, not report clean', no_ratchets_at_all, True, 'zero'),
    ('4 no exemplar on disk must FAIL, not report clean', the_exemplar_is_not_a_study,
     True, 'resolver'),
    ('5 a debt that SHORTENS must stay GREEN', a_debt_that_shortens, False, ''),
    ('6 another study joining a ratchet must NOT fire here',
     a_non_exemplar_joining_a_ratchet, False, ''),
    ('7 the repository as it stands must stay GREEN', clean, False, ''),
]


def main():
    fails = []
    for name, mutate, expect_red, must_name in CASES:
        d, dst = sandbox()
        try:
            marker = mutate(dst)
            rc, out = run(dst)
            ok = ((rc != 0) == expect_red)
            if ok and expect_red and must_name:
                ok = must_name.lower() in out.lower()
            print('  %-4s %s' % ('ok' if ok else 'FAIL', name))
            if not ok:
                fails.append(name)
                print('       rc=%d marker=%r' % (rc, marker))
                print('       ' + '\n       '.join(out.strip().splitlines()[-5:]))
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print('\n%d/%d conditions behaved as required' % (len(CASES) - len(fails), len(CASES)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
