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


def read_list(obj, path=None):
    """A whole top-level ARRAY from data.js — LEDGER — as a list of dicts.

    read_object() refuses a non-dict deliberately, so the array needs its own door rather
    than a loosened one: an object that came back as a list where a dict was wanted is a
    real failure everywhere else, and widening the check to accept both would delete it.
    """
    p = path or DATA_JS
    if not os.path.exists(p):
        raise RuntimeError('assets/data.js not found at %s' % p)
    js = _JS.format(path=json.dumps(p), obj=obj)
    r = subprocess.run(['node', '-e', js], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError('could not read %s from data.js through a real parse: %s'
                           % (obj, (r.stderr or '').strip()[:400]))
    out = json.loads(r.stdout)
    if not isinstance(out, list) or not out:
        raise RuntimeError('%s parsed to an empty array; an empty result is not a clean '
                           'result [R-ENF-04]' % obj)
    return out


def _same(a, b):
    """Equality that compares NUMBERS as numbers and everything else exactly.

    RE-POINTED, NOT LOOSENED [R-COC-01]. The first draft compared JSON encodings, and its
    first live run went red on 102.0 against 102 and 300.0 against 300 — a Python float
    beside a JSON integer, the same number written two ways. The check was firing on work
    that was right. Widening it to a tolerance would have been a free parameter with
    nothing behind it, and rounding the writer's output to satisfy it would have corrupted
    the thing being verified; what was wrong was the COMPARISON, so the comparison is what
    changed. A string "102" against a number 102 still differs, which is the case this
    exists to catch: a value that reached the file as text when it was meant as a number.
    """
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return float(a) == float(b)
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return type(a) is type(b) and a == b


def assert_written(obj, key, expected, path=None):
    """After writing data.js by hand, assert the PARSER agrees with what you meant to write.

    WHY A SYNTAX CHECK IS NOT ENOUGH, AND THIS IS MEASURED RATHER THAN ASSERTED. Every tool
    that writes this file does assert-guarded string surgery — correctly, because a JSON
    round-trip would destroy the file's formatting and its prose comments — and each one
    verifies with `node --check`. A DUPLICATED KEY IS VALID JAVASCRIPT AND `node --check`
    PASSES IT. Demonstrated on a two-line fixture: an entry declaring `levels` twice checks
    clean, the parser returns the SECOND, and a regular expression returns the FIRST.

    That is not a hypothetical shape. It is the exact defect [R-ENF-03] was adopted on: a
    ticker page published a support ABOVE its own close because its entry declared levels
    twice, and BOTH gates reported the page clean because both read the half the reader
    never saw. The write path could produce that file again today and nothing would say so.

    So a writer's verification is not "does it parse" but "does the PARSER return what I
    meant" — which is the same distinction as [R-ENF-01]'s, one layer down: a self-attested
    syntax check is not a check on the object that ships.
    """
    got = read(obj, key, path)
    bad = []
    for f, want in expected.items():
        have = got.get(f)
        if not _same(want, have):
            bad.append('  %s.%s: wrote %r, the parser returns %r' % (key, f, want, have))
    if bad:
        raise RuntimeError(
            'assets/data.js does not parse to what was just written to it. The commonest '
            'cause is a DUPLICATED KEY, which is valid JavaScript, passes `node --check`, '
            'and leaves the parser taking the other one [R-ENF-03]:\n' + '\n'.join(bad))
    return got


def assert_ledger_lifecycle(path=None):
    """Exactly one OPEN row at the latest anchor, per (instrument, horizon).

    THE FORECAST LIFECYCLE RULE HAS BEEN STANDING SINCE 29-Jul-2026 — "after ANY ledger
    write, assert the lifecycle invariant" — and it executed nowhere. Neither writer that
    appends ledger rows checked it; it lived in the protocol and in whatever the operator
    remembered, which is the same shape as every other finding this week.

    WHAT IT IS NOT: it does not say a name may carry one open row. Steady state is FOUR
    open rows per name, because a fresh 3-month strike DEMOTES the prior 3-month cone to an
    aging calibration tail that stays open and grades at its own maturity. Measured across
    the live ledger: 114 pairs carry one open row and 73 carry two, and every one of those
    is correct. What may never happen is TWO OPEN ROWS SHARING THE LATEST ANCHOR for one
    (instrument, horizon) — that is a duplicate strike, and it is what a re-run of a write
    that half-succeeded would produce.

    Measured before it was asserted, per [R-ENF-02]: 0 violations across 187 pairs, so this
    is a check that passes today rather than a permanently-red one.
    """
    rows = read_list('LEDGER', path)
    by = {}
    for r in rows:
        if r.get('realized_close') not in (None, ''):
            continue
        by.setdefault((r.get('instrument'), r.get('horizon_label')), []).append(r)
    if not by:
        raise RuntimeError('the ledger carries no OPEN rows at all; an empty result is not '
                           'a clean result [R-ENF-04]')
    bad = []
    for k, rs in sorted(by.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        latest = max((r.get('anchor_date') or '') for r in rs)
        n = sum(1 for r in rs if (r.get('anchor_date') or '') == latest)
        if n != 1:
            bad.append('  %s / %s: %d open rows share the latest anchor %s'
                       % (k[0], k[1], n, latest))
    if bad:
        raise RuntimeError('LIFECYCLE INVARIANT BROKEN — at most one current forecast per '
                           'name per horizon:\n' + '\n'.join(bad))
    return len(by)
