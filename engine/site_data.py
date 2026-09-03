"""The one way to read assets/data.js — through a real JavaScript parse.

WHY THIS EXISTS. [R-ENF-03] says the published data must be read through a real parse and
never by regular expression, and the reason is exact: re.search returns the FIRST match
where a JavaScript object literal takes the LAST, so a duplicated key means every tool
inspects the half the reader never sees. That rule was adopted after a READER — not a check
— found a ticker page publishing a support above its own close while both existing gates
reported it clean.

Measured on 03-Sep-2026: eleven files across the book read assets/data.js, and NINE of them
did it with a regular expression. Two did it correctly. The rule was right, was written
down, was implemented well where it existed, and bound in two places — which is the same
finding as the prose-figure gate, the sweep register and the external-reader scrub, all in
the same week. A SHARED INSTRUMENT BEATS A GOOD LOCAL ONE, and making it shared ONCE is the
only way it binds everywhere.

WHAT IT REFUSES. A missing node binary, a file that will not evaluate, an absent top-level
object and an absent key all RAISE with the reason. An empty result is not a clean result
[R-ENF-04]: a reader that returned {} on a broken file would be worse than one that fails,
because a study would then publish nothing where it meant to publish a record.
"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')

_JS = ("const fs=require('fs');const vm=require('vm');"
       "const src=fs.readFileSync({path},'utf8');const ctx=vm.createContext({{}});"
       "vm.runInContext(src+';globalThis.__O=typeof {obj}!==\"undefined\"?{obj}:null;',ctx);"
       "const o=ctx.__O;"
       "if(o===null)throw new Error('no top-level object {obj} in data.js');"
       "console.log(JSON.stringify(o));")


def read_object(obj, path=None):
    """A whole top-level object from data.js — TICKERS, LEDGER, BANDS, CALIB — as a dict."""
    p = path or DATA_JS
    if not os.path.exists(p):
        raise RuntimeError('assets/data.js not found at %s' % p)
    js = _JS.format(path=json.dumps(p), obj=obj)
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError('could not read %s from data.js through a real parse: %s'
                           % (obj, (r.stderr or '').strip()[:400]))
    out = json.loads(r.stdout)
    if not isinstance(out, dict) or not out:
        raise RuntimeError('%s parsed to an empty object; an empty result is not a clean '
                           'result [R-ENF-04]' % obj)
    return out


def read(obj, key, path=None):
    """One entry, refusing loudly rather than returning None for an absent key."""
    o = read_object(obj, path)
    if key not in o:
        raise RuntimeError('no %s entry for %r in data.js. It carries %d entries; a study '
                           'that needs this one cannot proceed without it.'
                           % (obj, key, len(o)))
    return o[key]


def band_record(ticker, path=None):
    """The published band record [R-CAL-02] — the one calibration figure a reader is shown."""
    b = read('BANDS', ticker, path)
    for f in ('n', 'c50', 'c80', 'c90', 'width', 'strength'):
        if b.get(f) is None:
            raise RuntimeError('band record for %s carries no %s' % (ticker, f))
    return b
