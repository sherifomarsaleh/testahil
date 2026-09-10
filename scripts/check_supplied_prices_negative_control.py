"""THE FALSIFIER FOR check_supplied_prices.py [R-ENF-07].

Plants prices into a throwaway tree and requires the gate to behave as claimed. The cases
are the ones the gate's own design turns on, including the two that its FIRST CUT got
wrong and that only testing found:

  1 a price implying a move far outside the name's own record  -> RED
  2 a large move that IS inside the name's own record          -> GREEN
      the bar is the name's history, so "big" is not the test
  3 a NEWER supplied file carrying an OLDER close              -> the older close must not
      displace a fresher one from an earlier file. This is the GBCO shape of 07-09-2026.
  4 a supplied file with two entries beside one with ninety    -> all ninety are checked
      The first cut read only the newest file, examined TWO names, and reported GREEN.
      That is [R-ENF-04] in its usual costume and it is the case that matters most here.
  5 no supplied file at all                                    -> RED, not a silent pass
  6 a library whose history is dominated by ONE split artefact -> the artefact must not
      raise the bar out of reach. IQCD's extreme one-session move reads 894.7%; a
      max-based bar made the gate unfireable on that name, which is why the bar is a
      percentile.

[R-ENF-01] builds its own tree under a temporary directory and never touches the repo.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, 'scripts', 'check_supplied_prices.py')


def _series(tmp, market, tk, closes, start_day=1):
    """closes: list of floats, oldest first. Dates are consecutive fake sessions."""
    d = os.path.join(tmp, 'engine', 'raw_ohlc', market)
    os.makedirs(d, exist_ok=True)
    lines = ['"Date","Price","Open","High","Low","Vol.","Change %"']
    for i, c in enumerate(closes):
        day = start_day + i
        mm, dd = 1 + (day - 1) // 28, 1 + (day - 1) % 28
        lines.append('"%02d/%02d/2026","%.3f","%.3f","%.3f","%.3f","1M","0%%"'
                     % (mm, dd, c, c, c, c))
    # newest first, as the real libraries are
    body = [lines[0]] + list(reversed(lines[1:]))
    open(os.path.join(d, tk + '.csv'), 'w').write('\n'.join(body) + '\n')


def _supplied(tmp, fname, rows, supplied_date):
    d = os.path.join(tmp, 'engine', 'prices')
    os.makedirs(d, exist_ok=True)
    json.dump({'supplied': supplied_date,
               'prices': {tk: dict(exchange='X', currency='X', company=tk,
                                   price=px, date=dt)
                          for tk, (px, dt) in rows.items()}},
              open(os.path.join(d, fname), 'w'), indent=1)


def _run(tmp):
    gate = os.path.join(tmp, 'scripts', 'check_supplied_prices.py')
    os.makedirs(os.path.dirname(gate), exist_ok=True)
    src = open(GATE, encoding='utf-8').read()
    # the ratchet names real tickers; a fixture tree has none of them, and an entry that
    # cannot fire must not silently excuse a fixture that shares its name
    open(gate, 'w', encoding='utf-8').write(src)
    p = subprocess.run([sys.executable, gate], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def case(label, build, expect_red, must_contain=None):
    tmp = tempfile.mkdtemp(prefix='supx-nc-')
    try:
        build(tmp)
        rc, out = _run(tmp)
        ok = (rc != 0) == expect_red
        if ok and must_contain and must_contain not in out:
            ok = False
            why = 'output lacked %r' % must_contain
        else:
            why = 'expected %s, got exit %d' % ('RED' if expect_red else 'GREEN', rc)
        print('  [%s] %s' % ('PASS' if ok else 'FAIL', label))
        if not ok:
            print('      ' + why)
            print('      ' + out.strip().replace('\n', '\n      ')[:1500])
        return ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


CALM = [10.0 + 0.01 * i for i in range(300)]        # a quiet, well-behaved series


def main():
    ok = True

    ok &= case('1 a supplied price implying a move far outside the name\'s own record',
               lambda t: (_series(t, 'EG', 'AAA', CALM),
                          _supplied(t, 'SUPPLIED_01-01-2026.json',
                                    {'AAA': (99.0, '2026-01-02')}, '2026-01-02')),
               expect_red=True)

    ok &= case('2 a LARGE move that is inside the name\'s own record — the bar is the '
               'history, not the size',
               lambda t: (_series(t, 'EG', 'BBB', [10.0, 20.0] * 150),
                          _supplied(t, 'SUPPLIED_01-01-2026.json',
                                    {'BBB': (20.0, '2026-01-02')}, '2026-01-02')),
               expect_red=False)

    def older_close_in_newer_file(t):
        _series(t, 'EG', 'CCC', CALM)
        _supplied(t, 'SUPPLIED_01-01-2026.json', {'CCC': (12.99, '2026-06-01')}, '2026-06-01')
        # a NEWER file carrying an OLDER, wild close. It must not displace the fresher one.
        _supplied(t, 'SUPPLIED_02-01-2026.json', {'CCC': (99.0, '2026-01-01')}, '2026-01-02')

    ok &= case('3 a newer file carrying an OLDER close does not displace a fresher one '
               '(the GBCO shape)', older_close_in_newer_file, expect_red=False)

    def two_beside_ninety(t):
        for i in range(90):
            _series(t, 'EG', 'N%02d' % i, CALM)
        _supplied(t, 'SUPPLIED_01-01-2026.json',
                  {('N%02d' % i): (99.0 if i == 7 else 13.0, '2026-06-01') for i in range(90)},
                  '2026-06-01')
        _supplied(t, 'SUPPLIED_02-01-2026.json',
                  {'N00': (13.0, '2026-06-02'), 'N01': (13.0, '2026-06-02')}, '2026-06-02')

    ok &= case('4 THE ONE THAT MATTERS — a 2-entry file beside a 90-entry one; all 90 are '
               'checked and the planted bad price in the OLDER file is still caught',
               two_beside_ninety, expect_red=True, must_contain='N07')

    ok &= case('5 no supplied file at all — absent is not clean [R-ENF-04]',
               lambda t: _series(t, 'EG', 'DDD', CALM), expect_red=True)

    def split_artefact(t):
        # one 900% jump, then a calm series: a max-based bar would be unfireable
        _series(t, 'EG', 'EEE', [1.0] * 20 + [10.0] + [10.0 + 0.01 * i for i in range(279)])
        _supplied(t, 'SUPPLIED_01-01-2026.json', {'EEE': (18.0, '2026-06-01')}, '2026-06-01')

    ok &= case('6 a lone split artefact must not raise the bar out of reach (the IQCD '
               'shape, 894.7% extreme)', split_artefact, expect_red=True)

    print('\nNEGATIVE CONTROL %s — check_supplied_prices.py %s'
          % ('OK' if ok else 'FAILED',
             'fires on a price outside the name\'s record, stays green inside it, reads '
             'every supplied file, and is not blinded by a split artefact'
             if ok else 'does NOT behave as claimed'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
