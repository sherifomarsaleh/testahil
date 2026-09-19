"""THE FALSIFIER FOR check_terminal_module_use.py [R-ENF-07].

Builds throwaway study trees and requires the gate to behave as claimed:

  1 a study with a terminal and no terminal_value import anywhere  -> RED
  2 the same study, importing the module                           -> GREEN
      the test is the CONSTRUCTION, not the presence of a record
  3 a study with no terminal at all owes nothing                   -> GREEN
  4 a ratcheted name stays green, and a NEW hand-rolled one is red beside it
  5 an unreadable study_numbers.json                               -> RED, not skipped
  6 no studies at all                                              -> RED, not a pass

[R-ENF-01] builds its own tree under a temporary directory and never touches the repo.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, 'scripts', 'check_terminal_module_use.py')

TERMINAL_NUMBERS = {'dcf': {'tv': 1000.0, 'terminal_growth': 0.05}}
NO_TERMINAL = {'lenses': {'book': {'base': 1.0}}}


def _study(tmp, ticker, numbers, source):
    d = os.path.join(tmp, 'engine', '%s_study' % ticker.lower())
    os.makedirs(d, exist_ok=True)
    if numbers is None:
        open(os.path.join(d, 'study_numbers.json'), 'w').write('{not json')
    else:
        json.dump(numbers, open(os.path.join(d, 'study_numbers.json'), 'w'))
    open(os.path.join(d, 'compute.py'), 'w').write(source)


def _run(tmp):
    gate = os.path.join(tmp, 'scripts', 'check_terminal_module_use.py')
    os.makedirs(os.path.dirname(gate), exist_ok=True)
    shutil.copy(GATE, gate)
    p = subprocess.run([sys.executable, gate], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def case(label, build, expect_red, must_contain=None):
    tmp = tempfile.mkdtemp(prefix='tmu-nc-')
    try:
        build(tmp)
        rc, out = _run(tmp)
        ok = (rc != 0) == expect_red
        if ok and must_contain and must_contain not in out:
            ok = False
        print('  [%s] %s' % ('PASS' if ok else 'FAIL', label))
        if not ok:
            print('      exit %d\n      %s' % (rc, out.strip().replace('\n', '\n      ')[:1200]))
        return ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


HAND = "x = 1  # a terminal built by hand\ntv = nopat * (1 + g) / (w - g)\n"
MODULE = "import terminal_value as TV\nrec = TV.build(TV.TerminalInputs())\n"


def main():
    ok = True

    ok &= case('1 a terminal built by hand, module imported nowhere',
               lambda t: _study(t, 'HANDA', TERMINAL_NUMBERS, HAND), expect_red=True)

    ok &= case('2 the same study through the module — the test is the CONSTRUCTION',
               lambda t: _study(t, 'HANDA', TERMINAL_NUMBERS, MODULE), expect_red=False)

    ok &= case('3 a study with no terminal owes nothing',
               lambda t: _study(t, 'NOTERM', NO_TERMINAL, HAND), expect_red=False)

    def ratcheted_plus_new(t):
        _study(t, 'AMOC', TERMINAL_NUMBERS, HAND)      # on the ratchet
        _study(t, 'NEWCO', TERMINAL_NUMBERS, HAND)     # not on it

    ok &= case('4 a ratcheted name stays green and a NEW hand-rolled one is red beside it',
               ratcheted_plus_new, expect_red=True, must_contain='NEWCO')

    ok &= case('5 an unreadable study_numbers.json — unreadable is not clean [R-ENF-04]',
               lambda t: _study(t, 'BROKEN', None, MODULE), expect_red=True)

    ok &= case('6 no studies at all — an empty population is not a pass [R-ENF-04]',
               lambda t: os.makedirs(os.path.join(t, 'engine'), exist_ok=True),
               expect_red=True)

    print('\nNEGATIVE CONTROL %s — check_terminal_module_use.py %s'
          % ('OK' if ok else 'FAILED',
             'fires on a hand-rolled terminal, clears when the module is used, and is not '
             'blinded by an absent or unreadable study' if ok else
             'does NOT behave as claimed'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
