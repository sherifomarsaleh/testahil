#!/usr/bin/env python3
"""Negative control for the terminal-floor gate — a check nobody has seen fail is not
evidence.

Each case copies the repository into a sandbox, injects ONE condition, and asserts the gate
behaves as specified. Every mutation is ASSERTED TO HAVE LANDED before the gate runs: a
fixture that quietly changes nothing produces a green that proves only that the file was
untouched, which is how this repository's own negative controls have failed twice before
[R-ENF-04].

The clean cases matter as much as the red ones. A gate that fires where no rule exists is
the permanently-red check [R-ENF-02] forbids, so a terminal comfortably ABOVE its floor and
a breach that is knowingly on the ratchet must both stay GREEN.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_CASES = 10


def sandbox(tmp):
    dst = os.path.join(tmp, 'repo')
    os.makedirs(dst)
    for p in ('engine', 'scripts'):
        shutil.copytree(os.path.join(REPO, p), os.path.join(dst, p),
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pdf',
                                                      '*.docx', '*.xlsx', '*.jpg', '*.png'))
    return dst


def run(root):
    r = subprocess.run([sys.executable, os.path.join(root, 'scripts',
                                                     'check_terminal_floor.py')],
                       capture_output=True, text=True, cwd=root)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def numbers(root, tk):
    return os.path.join(root, 'engine', f'{tk.lower()}_study', 'study_numbers.json')


def ratchet(root):
    return os.path.join(root, 'engine', 'build_depth_audit', 'terminal_outstanding.json')


# --------------------------------------------------------------------------------------
# The mutations. Each returns a short description of what it did, and RAISES if it did
# not actually land.
# --------------------------------------------------------------------------------------
def _new_signature(root):
    """A study OFF the ratchet is made to carry the 1/g construction. The one that matters.

    ARCC is the only readable study whose terminal is not built on the identity, so it is
    the only name that can newly acquire it. Its charge is put back onto g x IC by setting
    its terminal value to what that construction yields.
    """
    f = numbers(root, 'ARCC')
    d = json.load(open(f))
    dcf = d['dcf']
    N = d['forecast']['nopat'][-1] * (1 + d['macro_record']['growth_at_horizon_end'])
    g = d['macro_record']['growth_at_horizon_end']
    W = d['forecast']['fwd_wacc'][-1]
    before = dcf['tv']
    dcf['tv'] = (N - g * dcf['ic_repl']) / (W - g)      # the retired construction, exactly
    json.dump(d, open(f, 'w'), indent=1)
    assert abs(json.load(open(f))['dcf']['tv'] - before) > 1.0, 'mutation did not land'
    return 'ARCC terminal put back on g x IC (%.1f -> %.1f)' % (before, dcf['tv'])


def _signature_off_ratchet(root):
    """A real 1/g construction with its allowance removed. The live condition."""
    f = ratchet(root)
    d = json.load(open(f))
    assert 'AMOC' in d['signature'], 'fixture assumed AMOC was on the signature ratchet'
    d['signature'].pop('AMOC')
    json.dump(d, open(f, 'w'), indent=1)
    assert 'AMOC' not in json.load(open(f))['signature'], 'mutation did not land'
    return 'AMOC removed from the signature ratchet'


def _newly_unreadable(root):
    """A readable terminal becomes unreadable. Unreadable is not clean."""
    f = numbers(root, 'SAVOLA')
    d = json.load(open(f))
    assert 'dcf' in d and 'tv' in d['dcf'], 'fixture assumed SAVOLA exposed a terminal'
    d['dcf'].pop('tv')
    json.dump(d, open(f, 'w'), indent=1)
    assert 'tv' not in json.load(open(f))['dcf'], 'mutation did not land'
    return 'SAVOLA terminal value removed from its committed numbers'


def _ratchet_grew(root):
    """A name on the ratchet that is not on disk — the list anchored on nothing."""
    f = ratchet(root)
    d = json.load(open(f))
    d['breaching']['NOSUCHNAME'] = 'invented'
    json.dump(d, open(f, 'w'), indent=1)
    assert 'NOSUCHNAME' in json.load(open(f))['breaching'], 'mutation did not land'
    return 'a ticker with no study directory added to the ratchet'


def _empty_population(root):
    """No study directories at all. An empty result is not a clean result."""
    n = 0
    for d in os.listdir(os.path.join(root, 'engine')):
        if d.endswith('_study'):
            shutil.rmtree(os.path.join(root, 'engine', d)); n += 1
    assert n > 0, 'mutation did not land — nothing to remove'
    return 'all %d study directories removed' % n


def _all_terminals_dark(root):
    """Directories present, terminals all unreadable: zero READ, not zero examined."""
    n = 0
    for d in os.listdir(os.path.join(root, 'engine')):
        if not d.endswith('_study'):
            continue
        f = os.path.join(root, 'engine', d, 'study_numbers.json')
        if os.path.exists(f):
            open(f, 'w').write('{}'); n += 1
    assert n > 0, 'mutation did not land'
    return 'every one of %d numbers files emptied' % n


def _growth_above_rate(root):
    """Terminal growth at or above the terminal rate: the perpetuity does not converge."""
    f = numbers(root, 'DU')
    d = json.load(open(f))
    d['dcf']['g'] = 0.99
    json.dump(d, open(f, 'w'), indent=1)
    assert json.load(open(f))['dcf']['g'] == 0.99, 'mutation did not land'
    return 'DU terminal growth set to 99%%, above its terminal rate'


# --- clean cases: these must stay GREEN -----------------------------------------------
def _clean_untouched(root):
    return 'nothing changed'


def _clean_below_floor(root):
    """A terminal pushed BELOW the NOPAT/W figure must NOT fire — the floor is a diagnostic.

    This case is the INVERSE of the one it replaced, and keeping it inverted rather than
    deleting it is the sharpest available evidence the re-pointing took effect. The floor was
    the failing test and is now printed as a diagnostic: it assumes a maintenance charge the
    company does not face, so it is not an available policy, and measured across the book it
    does not separate the class — four studies carrying the construction sit above it.
    """
    f = numbers(root, 'ARCC')
    d = json.load(open(f))
    before = d['dcf']['tv']
    d['dcf']['tv'] = before * 0.55          # well under NOPAT/W, and not a 1/g cycle
    json.dump(d, open(f, 'w'), indent=1)
    assert json.load(open(f))['dcf']['tv'] < before, 'mutation did not land'
    return 'ARCC terminal cut to 55%% — below the NOPAT/W diagnostic, must stay green'


def _clean_at_the_floor(root):
    """A terminal sitting EXACTLY on its floor must NOT fire.

    This case replaced one that asserted a name re-filed from `unreadable` to `breaching`
    should stay green. The gate refused it and THE GATE WAS RIGHT: the two groups excuse
    two different conditions, so an entry filed under the wrong one is not an allowance —
    a study that cannot be read is not excused by an allowance for reading badly. The
    fixture's premise was wrong and the fixture was changed, not the gate.

    What is worth testing at that spot is the boundary itself, which is where a `<` and a
    `<=` diverge and where a dominance argument has to be exact: at TV == floor the
    company is indifferent between investing and not, and nothing is dominated.
    """
    f = numbers(root, 'DU')
    d = json.load(open(f))
    dcf = d['dcf']
    # solve the terminal that sits exactly on NOPAT_last / W
    import sys as _s
    _s.path.insert(0, root)
    for m in [k for k in list(_s.modules) if 'terminal_census' in k or 'valuation_calib' in k]:
        _s.modules.pop(m, None)
    from engine.valuation_calibration.terminal_census import read_study
    r = read_study(os.path.join(root, 'engine', 'du_study'))
    assert 'floor' in r, 'fixture could not read DU\'s floor'
    dcf['tv'] = r['floor']
    json.dump(d, open(f, 'w'), indent=1)
    assert abs(json.load(open(f))['dcf']['tv'] - r['floor']) < 1e-6, 'mutation did not land'
    return 'DU terminal set EXACTLY to its floor of %.1f' % r['floor']


CASES = [
    ('THE ONE THAT MATTERS — a study newly carrying the 1/g construction',
     _new_signature, 'red'),
    ('a real 1/g construction with its allowance removed', _signature_off_ratchet, 'red'),
    ('a terminal that stopped being readable [R-ENF-04]', _newly_unreadable, 'red'),
    ('the ratchet lists a ticker with no study on disk [R-ENF-04]', _ratchet_grew, 'red'),
    ('no study directories at all [R-ENF-04]', _empty_population, 'red'),
    ('directories present, every terminal dark [R-ENF-04]', _all_terminals_dark, 'red'),
    ('terminal growth at or above the terminal rate', _growth_above_rate, 'red'),
    ('CLEAN — the repository as it stands', _clean_untouched, 'green'),
    ('CLEAN — a terminal BELOW the NOPAT/W diagnostic (inverted on purpose)',
     _clean_below_floor, 'green'),
    ('CLEAN — a terminal sitting EXACTLY on its floor', _clean_at_the_floor, 'green'),
]


def main():
    assert len(CASES) == EXPECTED_CASES, (
        'this control declares %d cases and carries %d. A control that loses a case '
        'reports a smaller clean run as a clean run.' % (EXPECTED_CASES, len(CASES)))
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
                print('        wanted %s. Gate said:' % want)
                for line in out.strip().splitlines()[-8:]:
                    print('        | %s' % line)
    print('\n%d/%d cases behaved as specified' % (len(CASES) - bad, len(CASES)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
