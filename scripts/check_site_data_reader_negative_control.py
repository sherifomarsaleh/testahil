#!/usr/bin/env python3
"""The site-data gate must go RED on a regex reader and GREEN on a real parse.

Every failing case is a construction that actually exists or existed in this repository.
Every clean case is a construction that must NOT fire, including the two studies that had
been reading data.js correctly for weeks while nine others did not.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join('scripts', 'check_site_data_reader.py')

REGEX_READER = '''
import re, os
src = open(os.path.join('..', '..', 'assets', 'data.js')).read()
m = re.search(r'ARCC\\s*:\\s*\\{([^}]*)\\}', src)
'''
FINDALL_READER = '''
import re
src = open('assets/data.js').read()
rows = re.findall(r'(\\w+)\\s*:\\s*"([^"]*)"', src)
'''
SHARED_READER = '''
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import site_data
b = site_data.band_record('ARCC')
'''
NODE_READER = '''
import subprocess, os
JS = "const vm=require('vm');const src=require('fs').readFileSync('assets/data.js','utf8');"
JS += "const ctx=vm.createContext({});vm.runInContext(src+';globalThis.__B=BANDS;',ctx);"
out = subprocess.run(['node', '-e', JS], capture_output=True, text=True)
'''
NO_DATA_JS = '''
import re
src = open('something_else.json').read()
m = re.search(r'x', src)
'''

# ---------------------------------------------------------------------------------------
# THE RE-POINTED POPULATION [03-Sep-2026]. The first predicate keyed on the STRING
# "data.js" appearing anywhere in a file, and ratcheted three files that never open it:
# two carry the word inside an external-reader SCRUB LIST — the internal vocabulary a
# delivered document may not contain — and one names the path in a prose comment. All
# three separately use a regular expression for something else. These are the two
# constructions verbatim, and they must not merely pass, they must not be COUNTED, which
# is a different state and the one that matters: a ratchet entry standing over innocent
# work would silently excuse that file the day it did start parsing data.js by hand.
SCRUB_LIST = '''
import re
FORBIDDEN = ["walk-forward", "ring", "cohort", "raw_ohlc", "data.js", "pre-registration"]
def scrub(paragraphs):
    for low in paragraphs:
        for w in FORBIDDEN:
            if re.search(r"\\b%s\\b" % re.escape(w), low):
                yield w
'''
PROSE_MENTION = '''
import os, re
# Until then `assets/data.js` carries the PRE-CALIBRATION range and the calibrated
# figure lives in the study. This script never opens it.
def edition(p):
    return re.search(r\'(\\d{2})[-_]?(\\d{2})[-_]?(\\d{4})\', os.path.basename(p))
'''
# and the shape the re-pointing must NOT have blinded: a pathlib construction, which is how
# scripts/check_page_integrity.py resolves the file.
PATHLIB_READER = '''
import re
from pathlib import Path
src = (Path(\'.\') / "assets" / "data.js").read_text()
m = re.search(r\'fair:\\s*\\{([^}]*)\\}\', src)
'''

CASES = [
    ('a study reading data.js with re.search', {'zzz': REGEX_READER}, True),
    ('a script reading data.js with re.findall', {'zzz': FINDALL_READER}, True),
    ('a study using the SHARED reader', {'zzz': SHARED_READER}, False),
    ('a study evaluating data.js in node itself', {'zzz': NODE_READER}, False),
    ('a file with a regex that does not touch data.js', {'zzz': NO_DATA_JS}, False),
    ('a SCRUB LIST carrying "data.js" as a forbidden word — fired against the first '
     'predicate', {'zzz': SCRUB_LIST}, False),
    ('a prose comment naming assets/data.js beside a filename-date regex — fired against '
     'the first predicate', {'zzz': PROSE_MENTION}, False),
    ('a PATHLIB path construction with a regex — the re-pointing must not blind the gate',
     {'zzz': PATHLIB_READER}, True),
]


def build(tmp, extra, ratchet):
    for d in ('scripts', os.path.join('engine', 'build_depth_audit'), 'assets'):
        os.makedirs(os.path.join(tmp, d), exist_ok=True)
    shutil.copy(os.path.join(ROOT, GATE), os.path.join(tmp, GATE))
    shutil.copy(os.path.join(ROOT, 'engine', 'site_data.py'),
                os.path.join(tmp, 'engine', 'site_data.py'))
    open(os.path.join(tmp, 'assets', 'data.js'), 'w').write('const BANDS={};\n')
    # one always-present correct reader so the population is never empty for the wrong reason
    open(os.path.join(tmp, 'engine', 'good_reader.py'), 'w').write(SHARED_READER)
    for tk, src in extra.items():
        sd = os.path.join(tmp, 'engine', '%s_study' % tk)
        os.makedirs(sd, exist_ok=True)
        open(os.path.join(sd, 'reader.py'), 'w').write(src)
    json.dump({'outstanding': ratchet},
              open(os.path.join(tmp, 'engine', 'build_depth_audit',
                                'sitedata_outstanding.json'), 'w'), indent=1)


def run_gate(tmp):
    r = subprocess.run([sys.executable, GATE], cwd=tmp, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def main():
    bad = 0
    for name, extra, must_fail in CASES:
        tmp = tempfile.mkdtemp(prefix='ncsite')
        try:
            build(tmp, extra, [])
            rc, out = run_gate(tmp)
            ok = (rc != 0) if must_fail else (rc == 0)
            print('%s %s' % ('PASS' if ok else 'FAIL', name))
            if not ok:
                bad += 1
                print('      rc=%d wanted %s' % (rc, 'RED' if must_fail else 'GREEN'))
                print('      ' + '\n      '.join(out.strip().splitlines()[-6:]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # GREEN-BECAUSE-EXCLUDED IS NOT GREEN-BECAUSE-COMPLIANT, and only the first is right
    # for a file that never opens data.js. rc alone cannot tell them apart — a scrub list
    # carries no site_data call, so were it counted it would be counted as an OFFENDER —
    # so the population COUNT is compared with and without it.
    import re as _re

    def _population(extra):
        t = tempfile.mkdtemp(prefix='ncsite')
        try:
            build(t, extra, [])
            _, o = run_gate(t)
            m = _re.search(r'files reading assets/data\.js: (\d+)', o)
            return int(m.group(1)) if m else -1
        finally:
            shutil.rmtree(t, ignore_errors=True)

    base = _population({})
    for nm, src in (('a scrub list', SCRUB_LIST), ('a prose mention', PROSE_MENTION)):
        n = _population({'zzz': src})
        ok = n == base
        print('%s %s is EXCLUDED from the population, not merely passed (%d vs %d)'
              % ('PASS' if ok else 'FAIL', nm, n, base))
        bad += 0 if ok else 1
    n = _population({'zzz': PATHLIB_READER})
    ok = n == base + 1
    print('%s a pathlib reader IS counted (%d vs %d)' % ('PASS' if ok else 'FAIL', n, base))
    bad += 0 if ok else 1

    # the ratchet actually excuses, and only what it names
    tmp = tempfile.mkdtemp(prefix='ncsite')
    try:
        build(tmp, {'zzz': REGEX_READER}, ['engine/zzz_study/reader.py'])
        rc, out = run_gate(tmp)
        ok = rc == 0 and 'ratcheted' in out
        print('%s a ratcheted regex reader stays GREEN' % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # a run examining nothing must FAIL, not report clean
    tmp = tempfile.mkdtemp(prefix='ncsite')
    try:
        build(tmp, {}, [])
        os.remove(os.path.join(tmp, 'engine', 'good_reader.py'))
        rc, out = run_gate(tmp)
        ok = rc != 0 and 'zero files' in out
        print('%s a run examining ZERO readers FAILS [R-ENF-04]' % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # a ratchet naming a file that is gone must FAIL
    tmp = tempfile.mkdtemp(prefix='ncsite')
    try:
        build(tmp, {}, ['engine/vanished_study/reader.py'])
        rc, out = run_gate(tmp)
        ok = rc != 0 and 'no longer exist' in out
        print('%s a ratchet naming a vanished file FAILS [R-ENF-04]'
              % ('PASS' if ok else 'FAIL'))
        bad += 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # the shared reader itself refuses an absent key rather than returning nothing
    sys.path.insert(0, os.path.join(ROOT, 'engine'))
    import site_data
    try:
        site_data.read('BANDS', 'NO_SUCH_TICKER_AT_ALL')
        print('FAIL the shared reader returns silently on an absent key')
        bad += 1
    except RuntimeError:
        print('PASS the shared reader REFUSES an absent key rather than returning nothing')

    total = len(CASES) + 7
    print('\nNEGATIVE CONTROL %s — %d/%d conditions'
          % ('OK' if not bad else 'FAILED', total - bad, total))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
