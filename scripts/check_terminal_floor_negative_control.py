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
EXPECTED_CASES = 15


def sandbox(tmp):
    dst = os.path.join(tmp, 'repo')
    os.makedirs(dst)
    for p in ('engine', 'scripts'):
        shutil.copytree(os.path.join(REPO, p), os.path.join(dst, p),
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pdf',
                                                      '*.docx', '*.xlsx', '*.jpg', '*.png'))
    return dst


# THIS FIXTURE SUPPLIES ITS OWN POPULATION [06-09-2026]. The gate resolves the
# book through engine/study_population.py; this control runs it against a
# sandboxed tree holding studies it planted, which is the point of the control.
# The escape is explicit and the gate PRINTS that it took it, so a fixture
# population can never be mistaken for the real one.
_FIXTURE_ENV = dict(os.environ, TESTAHIL_FIXTURE_POPULATION='1')


def run(root):
    r = subprocess.run([sys.executable, os.path.join(root, 'scripts',
                                                     'check_terminal_floor.py')],
                       capture_output=True, text=True, cwd=root, env=_FIXTURE_ENV)
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


def _moves_unreadable_to_signature(root):
    """A study on `unreadable` that BECOMES READABLE and carries 1/g must stay GREEN.

    THE ALLOWANCE TRAVELS ONE WAY AND THE DIRECTION IS THE WHOLE ARGUMENT. When the census
    learned to derive g from a reinvestment rate and a return a study already publishes,
    SCEM and BOROUGE stopped being unreadable and turned out to carry the 1/g construction
    they had carried all along — SCEM's terminal 34% below its own floor, the worst in the
    book and invisible until then. Failing that as a NEW violation would punish the census
    for learning to read and make widening a reader more expensive than leaving studies
    dark, which is the exact incentive [R-ENF-04] exists to remove.

    The fixture re-files a name currently on `signature` back onto `unreadable` WITHOUT
    touching the study, so the gate meets a breaching study whose only allowance is an
    unreadable one — the shape the move produces.
    """
    f = os.path.join(root, 'engine', 'build_depth_audit', 'terminal_outstanding.json')
    d = json.load(open(f))
    tk = sorted(d['signature'])[0]
    d['unreadable'][tk] = d['signature'].pop(tk)
    json.dump(d, open(f, 'w'), indent=1)
    after = json.load(open(f))
    assert tk in after['unreadable'] and tk not in after['signature'], 'mutation did not land'
    return '%s re-filed onto `unreadable` while still breaching — must stay GREEN' % tk


def _breaching_hidden_as_unreadable(root):
    """...AND THE REVERSE MOVE STAYS REFUSED, which is what makes the first one safe.

    A study whose terminal is genuinely unreadable, listed ONLY under `signature`, must
    still fail: an entry able to travel that way lets a name escape a real breach by being
    re-filed as merely unreadable, which is the cheapest route past any gate [R-ENF-04].
    The fixture breaks a study's terminal so it cannot be read AND files its allowance in
    the wrong group.
    """
    f = numbers(root, 'AMOC')
    d = json.load(open(f))
    for k in ('tv', 'terminal_value', 'tv_value'):
        d['dcf'].pop(k, None)
    json.dump(d, open(f, 'w'), indent=1)
    r = os.path.join(root, 'engine', 'build_depth_audit', 'terminal_outstanding.json')
    rat = json.load(open(r))
    rat['unreadable'].pop('AMOC', None)
    rat['signature']['AMOC'] = 'filed in the WRONG group on purpose'
    json.dump(rat, open(r, 'w'), indent=1)
    # ASSERT THE CONDITION, NOT THE EDIT. The first draft removed the terminal RATE and
    # asserted only that the key was gone from the file — and the census resolved a rate
    # from another route, so the study stayed readable and the case passed for a reason
    # that had nothing to do with what it tests. An empty result is not a clean result
    # [R-ENF-04] and neither is a mutation that did not produce the state it names.
    import sys as _s
    _s.path.insert(0, root)
    for m in [k for k in list(_s.modules) if 'terminal_census' in k or 'valuation_calib' in k]:
        _s.modules.pop(m, None)
    from engine.valuation_calibration.terminal_census import read_study
    rr = read_study(os.path.join(root, 'engine', 'amoc_study'))
    assert 'unreadable' in rr, 'mutation did not land: AMOC still reads (%s)' % sorted(rr)[:6]
    return 'AMOC made unreadable with its allowance filed under `signature` — must go RED'


def _newly_unscoreable(root):
    """A terminal that still RESOLVES but whose charge can no longer be derived.

    THE THIRD BUCKET [ADDED 05-Sep-2026]. Between `unreadable` (no terminal at all) and
    `scored` (the charge is derivable) sits a state the gate did not name: the terminal
    reads, the charge does not, and the 1/g test never runs. Four studies were in it and
    the gate printed OK — one of them, ELEC, carrying the retired construction in plain
    sight in its own compute.py. An UNTESTED terminal is not a clean terminal.
    """
    f = numbers(root, 'SAVOLA')
    d = json.load(open(f))
    assert 'nopat' in d.get('fcst', {}), 'fixture assumed SAVOLA exposed a forecast NOPAT'
    d['fcst'].pop('nopat')
    json.dump(d, open(f, 'w'), indent=1)
    import sys as _s
    _s.path.insert(0, root)
    for m in [k for k in list(_s.modules) if 'terminal_census' in k or 'valuation_calib' in k]:
        _s.modules.pop(m, None)
    from engine.valuation_calibration.terminal_census import read_study
    rr = read_study(os.path.join(root, 'engine', 'savola_study'))
    assert 'unreadable' not in rr and 'floor' not in rr, (
        'mutation did not land: SAVOLA is %s'
        % ('unreadable' if 'unreadable' in rr else 'still scoreable'))
    return 'SAVOLA terminal still reads and its charge no longer derives — must go RED'


def _unscoreable_hidden_as_signature(root):
    """A study whose charge cannot be derived, with its allowance filed under `signature`.

    The mirror of the unreadable escape hatch and refused for the same reason: an entry
    able to travel INTO an ignorance group lets a name escape the group that actually
    describes it. GBCO is genuinely unscoreable; filing it under `signature` must not
    satisfy the unscoreable check.
    """
    r = os.path.join(root, 'engine', 'build_depth_audit', 'terminal_outstanding.json')
    rat = json.load(open(r))
    assert 'GBCO' in rat.get('unscored', {}), 'fixture assumed GBCO was on the unscored list'
    rat['unscored'].pop('GBCO')
    rat['signature']['GBCO'] = 'filed in the WRONG group on purpose'
    json.dump(rat, open(r, 'w'), indent=1)
    assert 'GBCO' not in json.load(open(r))['unscored'], 'mutation did not land'
    return 'GBCO unscoreable with its allowance filed under `signature` — must go RED'


def _clean_scenario_knob_ignored(root):
    """CLEAN — a bear-case knob is set absurd and the base answer must not move.

    ELEC's terminal growth WAS being read from `scenarios.bear.knobs.g`, so its whole
    terminal was scored on the bear case: 1/g read 25.0 years against the study's own
    committed 20.0. A resolver that guesses is the defect [R-ENF-04] closes, and a
    sensitivity grid, a bear case and a scenario knob all carry the same field names as
    the base answer and are numerically plausible — so the wrong one reads as clean. The
    knob below would give 1/g of 1000 years if it were read.
    """
    f = numbers(root, 'ELEC')
    d = json.load(open(f))
    assert d['scenarios']['bear']['knobs']['g'], 'fixture assumed ELEC had a bear g knob'
    d['scenarios']['bear']['knobs']['g'] = 0.001
    json.dump(d, open(f, 'w'), indent=1)
    assert json.load(open(f))['scenarios']['bear']['knobs']['g'] == 0.001, 'did not land'
    return "ELEC's bear-case growth knob set to 0.1% — the base answer must ignore it"


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
    ('CLEAN — the allowance travels `unreadable` -> `signature` when a study becomes '
     'readable', _moves_unreadable_to_signature, 'green'),
    ('...and NOT the other way: a breach hidden behind an unreadable allowance',
     _breaching_hidden_as_unreadable, 'red'),
    ('a terminal that reads and can no longer be SCORED [R-ENF-04]',
     _newly_unscoreable, 'red'),
    ('an unscoreable terminal filed under `signature` — the mirror escape hatch',
     _unscoreable_hidden_as_signature, 'red'),
    ('CLEAN — a bear-case knob set absurd; the base answer must ignore it',
     _clean_scenario_knob_ignored, 'green'),
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
