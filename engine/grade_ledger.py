"""grade_ledger.py — the ledger sweep of STEP 3 (Rollforward_and_Grading_Protocol).

Grades every OPEN LEDGER row (`realized_close: null`) whose stored calendar
`grade_date` has arrived AND whose persisted library covers it. Everything else is
reported and left alone — a matured row whose library stops short is BLOCKED, not
skipped silently.

WHY THIS EXISTS AS A MODULE [R-ENF-01]. Until now grading was done by hand at each
roll-forward, so the convention lived in whoever's head was doing it that day. The
convention is not obvious and two of its three choices are invisible in the output:

  * the window is the sessions STRICTLY AFTER the anchor date through the grade date
    (the anchor's own bar is the strike, not part of the outcome);
  * realized_high/low come from the HIGH and LOW columns, not from closes;
  * realized_close is the close ON the stored grade_date.

Six of the fourteen grades on record cannot tell the first choice apart (their anchor
bar is not the window extreme either way). Eight can, and all eight say
after-the-anchor. A hand-grader who happened to start on one of the six ambiguous
names would have learned the wrong rule and never found out.

So the module is NEGATIVE-CONTROLLED: `replay()` regrades every ALREADY-GRADED row
from its own library and asserts the published fields come back identical. A grader
that cannot reproduce the grades already on the site does not get to write a new one.
Run it as `--replay-only` any time; the sweep runs it first and refuses to write if it
fails.

The control tests the CONVENTION, and it is deliberately split from a second thing it
kept getting confused with — whether the library still holds the same close the row was
graded on. EMFD's 2026-07-19 grade records realized_close 11.70 (its median_err of
-0.0824 is internally consistent with 11.6994) while the library now reads 11.69 for
that session. That is a one-cent provenance gap in an already-graded row, and graded
rows are permanent: it is REPORTED, never repaired. So the derived fields are checked
against the close the ROW ITSELF records — which is what tests the formula — and
close-vs-library disagreement is raised separately as a data observation. Widening a
tolerance until the mismatch disappears would have hidden both the gap and any real
convention error behind the same slack.

WHAT IT MAY NOT DO (Publish_Protocol, THE LEDGER SWEEP):
  * never edit a graded row or any frozen percentile — grading APPENDS outcome fields;
  * never strike a new cycle (that is the metronome's job, STEP 4);
  * never quietly fix a lifecycle breach — report and leave it.

If the stored grade_date is not a real session in the library (closure/suspension), the
next actual session is graded, `grade_date` is set to the session actually graded, and
`grade_date_projected` + a one-line `grade_note` are added. Annotate, never overwrite.
"""
from __future__ import annotations

import argparse, csv, io, json, os, re, subprocess, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
LEDGER_HTML = os.path.join(ROOT, 'ledger.html')
RAW = os.path.join(ROOT, 'engine', 'raw_ohlc')

PCTS = [('p5', 0.05), ('p25', 0.25), ('p50', 0.50), ('p75', 0.75), ('p95', 0.95)]
# Below this, a difference between the frozen anchor_price and the library's close on
# the same session is vendor noise, not a corporate action. See ca_factor().
#
# Set at 2%, not at rounding width, and the negative control is why: at 0.5% the
# detector fired on Platinum, whose row froze 1608.37 against a library close 0.65%
# away — a vendor revision of one print, not a share-count change — and the replay
# refused to reproduce a published grade. The smallest corporate action anyone
# actually issues is a 5% stock dividend, so 2% separates the two classes with room
# on both sides. A false NEGATIVE here only reverts to the old behaviour; a false
# POSITIVE silently rewrites a grade, so the threshold leans to the safe side.
CA_TOL = 0.02
REL = [('+5', 0.05), ('+10', 0.10), ('+15', 0.15), ('+20', 0.20), ('-5', -0.05), ('-10', -0.10)]


# ---------------------------------------------------------------- library access

def raw_csv_map() -> dict:
    """instrument -> 'MKT/TICKER.csv', read from ledger.html's own map.

    Read from the page rather than re-derived, so the sweep and the ledger's realized
    price overlay can never disagree about which series a name is.
    """
    src = open(LEDGER_HTML, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'"?([A-Za-z0-9]+)"?\s*:\s*"([A-Z]{2,3}/[A-Za-z0-9]+\.csv)"', src):
        out[m.group(1)] = m.group(2)
    return out


def load_library(rel_path: str):
    """date -> {c,h,l} from the persistent library, vendor format, newest-first."""
    p = os.path.join(RAW, rel_path)
    if not os.path.exists(p):
        return None
    rows = list(csv.DictReader(io.StringIO(open(p, encoding='utf-8-sig').read())))
    out = {}
    for r in rows:
        d = datetime.strptime(r['Date'], '%m/%d/%Y').strftime('%Y-%m-%d')
        f = lambda k: float(r[k].replace(',', ''))
        out[d] = {'c': f('Price'), 'h': f('High'), 'l': f('Low')}
    return out


def read_ledger() -> list:
    js = r'''
const fs=require("fs"),vm=require("vm");const s={};vm.createContext(s);
vm.runInContext(fs.readFileSync(process.argv[1],"utf8")+";globalThis.__L=LEDGER;",s);
process.stdout.write(JSON.stringify(s.__L));
'''
    r = subprocess.run(['node', '-e', js, DATA_JS], capture_output=True)
    if r.returncode:
        raise SystemExit('could not load LEDGER from data.js:\n' + r.stderr.decode())
    return json.loads(r.stdout)


# ---------------------------------------------------------------- the grade itself

def grade_session(lib: dict, stored_grade_date: str):
    """The session actually graded: the stored date, or the next real one after it."""
    if stored_grade_date in lib:
        return stored_grade_date, False
    later = [d for d in sorted(lib) if d > stored_grade_date]
    return (later[0], True) if later else (None, False)


def ca_factor(row: dict, lib: dict) -> float:
    """The cumulative corporate-action factor between the strike and today's library.

    A ledger row freezes `anchor_price` on the basis that traded the day it was
    struck. When a bonus issue or split goes ex inside the window, the vendor
    restates the WHOLE series onto the new share basis — so the library's close for
    that same anchor_date is no longer the number the cone was built on, and the
    frozen percentiles are denominated in the old basis while the realized close is
    denominated in the new one. Grading one against the other is a unit error.

    Their RATIO is the adjustment, and it needs no new field anyone has to remember
    to set: anchor_price / library-close-on-anchor_date IS the cumulative factor,
    self-checking and correct for any future split or bonus.

    Found 24-Aug-2026 on Juhayna, which went ex a second 25% bonus (1,176.8m ->
    1,470.9m shares) inside its 1-month window. Its row froze anchor 28.90; the
    restated library holds 23.12 for that same 22-Jul-2026 session. 28.90/23.12 =
    1.25 exactly. Graded raw, the 23-Aug close of 26.88 scores median_err -8.4%
    against a cone centred at 29.33; restated to the anchor's basis it is 33.60 and
    scores +14.6%. THE ERROR FLIPS SIGN — the grade would have recorded the engine
    missing low when it actually missed high.

    Inert where nothing happened: with no corporate action the ratio is 1.0 to
    within vendor rounding, so every other row grades exactly as before. The
    replay negative control over the already-graded rows is what proves that.
    """
    # Equities only. A spot metal has no share count, so nothing can rescale its
    # series and any gap is a vendor revision by construction — which is exactly
    # what the Platinum row turned out to be.
    if row.get('asset_class') != 'equity':
        return 1.0
    base = lib.get(row['anchor_date'])
    if not base or not base['c']:
        return 1.0
    ratio = row['anchor_price'] / base['c']
    return ratio if abs(ratio - 1.0) > CA_TOL else 1.0


def compute(row: dict, lib: dict) -> dict | None:
    """Outcome fields for one open row, or None if its library cannot cover it."""
    gd, rolled = grade_session(lib, row['grade_date'])
    if gd is None:
        return None
    window = [d for d in sorted(lib) if row['anchor_date'] < d <= gd]
    if not window:
        return None

    # Restate the realized window onto the basis the cone was struck on, so the
    # frozen percentiles are never compared across a share-count change.
    ca = ca_factor(row, lib)
    rc = lib[gd]['c'] * ca
    hi = max(lib[d]['h'] for d in window) * ca
    lo = min(lib[d]['l'] for d in window) * ca
    if ca != 1.0:
        rc, hi, lo = round(rc, 2), round(hi, 2), round(lo, 2)
    p = {k: row[k] for k, _ in PCTS}

    out = {
        'realized_close': rc,
        'realized_high': hi,
        'realized_low': lo,
        'in_90': p['p5'] <= rc <= p['p95'],
        'in_50': p['p25'] <= rc <= p['p75'],
        'realized_quantile': quantile(rc, p),
        'median_err': round(rc / p['p50'] - 1, 4),
        'touch_hit': {k: (hi >= row['anchor_price'] * (1 + f) if f > 0
                          else lo <= row['anchor_price'] * (1 + f)) for k, f in REL},
        '_sessions': len(window),
        '_graded_on': gd,
        '_rolled': rolled,
        '_ca': ca,
    }
    return out


def quantile(rc: float, p: dict):
    """Linear interpolation on the frozen percentile grid; None outside [p5, p95].

    Outside the grid there is no interpolant and extrapolating one would invent a
    precision the cone never claimed — Samsung's -26.6% miss is stored with a null
    quantile for exactly this reason.
    """
    xs = [p[k] for k, _ in PCTS]
    ys = [q for _, q in PCTS]
    if rc < xs[0] or rc > xs[-1]:
        return None
    for i in range(len(xs) - 1):
        if xs[i] <= rc <= xs[i + 1]:
            if xs[i + 1] == xs[i]:
                return round(ys[i], 3)
            t = (rc - xs[i]) / (xs[i + 1] - xs[i])
            return round(ys[i] + t * (ys[i + 1] - ys[i]), 3)
    return None


# ---------------------------------------------------------------- negative control

def replay(ledger: list, rawmap: dict, verbose: bool = True) -> tuple:
    """Regrade every already-graded row and assert the published fields come back.

    This is the gate on the grader, not on the data: a mismatch means the convention
    encoded here is not the convention the site was graded under, and nothing may be
    written until that is resolved.
    """
    checked = failed = skipped = 0
    drift = []
    for row in ledger:
        if row.get('realized_close') in (None, ''):
            continue
        lib = load_library(rawmap.get(row['instrument'], ''))
        if not lib or row['grade_date'] not in lib:
            skipped += 1
            continue
        got = compute(row, lib)
        checked += 1
        bad = []

        # (1) Does the library still hold the close this row was graded on? A
        #     disagreement is a provenance observation about a permanent row, not a
        #     convention failure — collected separately and never repaired here.
        if abs(got['realized_close'] - row['realized_close']) > 0.0001:
            drift.append((row, got['realized_close'], row['realized_close']))

        # (2) Does the CONVENTION reproduce? Window extremes come from the library;
        #     the close-derived fields are re-derived from the row's OWN recorded
        #     close, so a stale close cannot masquerade as a formula error.
        for f in ('realized_high', 'realized_low'):
            if abs(got[f] - row[f]) > 0.011:
                bad.append(f'{f}: got {got[f]} published {row[f]}')
        rc = row['realized_close']
        p = {k: row[k] for k, _ in PCTS}
        exp = {
            'in_90': p['p5'] <= rc <= p['p95'],
            'in_50': p['p25'] <= rc <= p['p75'],
            'realized_quantile': quantile(rc, p),
            'median_err': round(rc / p['p50'] - 1, 4),
        }
        for f in ('in_90', 'in_50'):
            if exp[f] != row[f]:
                bad.append(f'{f}: got {exp[f]} published {row[f]}')
        if (exp['realized_quantile'] is None) != (row['realized_quantile'] is None):
            bad.append(f"realized_quantile null-ness: got {exp['realized_quantile']} published {row['realized_quantile']}")
        elif exp['realized_quantile'] is not None and abs(exp['realized_quantile'] - row['realized_quantile']) > 0.0011:
            bad.append(f"realized_quantile: got {exp['realized_quantile']} published {row['realized_quantile']}")
        if abs(exp['median_err'] - row['median_err']) > 0.0002:
            bad.append(f"median_err: got {exp['median_err']} published {row['median_err']}")
        for k, _ in REL:
            if got['touch_hit'][k] != row['touch_hit'][k]:
                bad.append(f"touch_hit[{k}]: got {got['touch_hit'][k]} published {row['touch_hit'][k]}")
        if bad:
            failed += 1
            print(f"  REPLAY FAIL {row['instrument']} {row['horizon_label']} {row['anchor_date']}")
            for b in bad:
                print('      ' + b)
        elif verbose:
            print(f"  replay ok   {row['instrument']:10} {row['horizon_label']:9} "
                  f"{row['anchor_date']} -> {row['grade_date']} ({got['_sessions']} sessions)")
    return checked, failed, skipped, drift


# ---------------------------------------------------------------- the sweep

def sweep(today: str, verbose: bool = True) -> dict:
    ledger = read_ledger()
    rawmap = raw_csv_map()

    print('=== NEGATIVE CONTROL: replay of already-graded rows ===')
    checked, failed, skipped, drift = replay(ledger, rawmap, verbose)
    print(f'  {checked} replayed, {failed} convention mismatches, {skipped} not replayable (library no longer covers)')
    for row, libc, pubc in drift:
        print(f"  NOTE {row['instrument']} {row['horizon_label']} graded {row['grade_date']}: "
              f"library close {libc} vs recorded realized_close {pubc} "
              f"— permanent row, reported not repaired")
    if failed:
        raise SystemExit('REPLAY FAILED — the grader does not reproduce grades already published. '
                         'Nothing written.')

    open_rows = [r for r in ledger if r.get('realized_close') in (None, '')]
    matured = [r for r in open_rows if r['grade_date'] <= today]
    gradable, blocked = [], []
    for r in matured:
        lib = load_library(rawmap.get(r['instrument'], ''))
        if not lib:
            blocked.append((r, 'no library file'))
            continue
        got = compute(r, lib)
        if got is None:
            blocked.append((r, f"library ends {max(lib)}, grade date {r['grade_date']} not covered"))
        else:
            gradable.append((r, got))
    return {'ledger': ledger, 'open': open_rows, 'matured': matured,
            'gradable': gradable, 'blocked': blocked}


# ---------------------------------------------------------------- writing a grade

def _ledger_span(src: str) -> tuple:
    i = src.find('const LEDGER')
    if i < 0:
        raise SystemExit('const LEDGER not found in data.js')
    j = src.find('[', i)
    depth, k = 0, j
    while k < len(src):
        if src[k] == '[':
            depth += 1
        elif src[k] == ']':
            depth -= 1
            if depth == 0:
                return j, k + 1
        k += 1
    raise SystemExit('unterminated LEDGER array')


def ledger_row_spans(src: str) -> list:
    """(start, end) of every top-level `{...}` inside LEDGER, by brace matching.

    Brace-matched rather than pattern-matched on purpose. The rows are not written
    in one style — 276 use `instrument:"X"` and six (the three most recent publishes)
    use `instrument: "X"` — and every regex in this repo that stood in for a parser
    eventually met the entries formatted differently and silently skipped them.
    A depth counter cannot care about whitespace.

    It must, however, care about COMMENTS. The LEDGER carries dated calibration
    headers, and those quote bootstrap block sizes as "{2,3,4}" — seven of them.
    A brace counter that reads comments finds 212 rows where node finds 205, which
    is how this was caught: by counting against a known total rather than trusting
    the scan's own silence.
    """
    a, b = _ledger_span(src)
    spans, k, depth, start = [], a, 0, None
    in_str, esc = False, False
    while k < b:
        ch = src[k]
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == '/' and k + 1 < b and src[k + 1] == '/':
            k = src.find('\n', k)
            if k < 0:
                break
            continue
        elif ch == '/' and k + 1 < b and src[k + 1] == '*':
            k = src.find('*/', k)
            if k < 0:
                break
            k += 2
            continue
        elif ch == '{':
            if depth == 0:
                start = k
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                spans.append((start, k + 1))
        k += 1
    return spans


def _field(text: str, key: str):
    m = re.search(r'\b' + re.escape(key) + r'\s*:\s*("(?:[^"\\]|\\.)*"|[-\w.]+)', text)
    if not m:
        return None
    v = m.group(1)
    return v[1:-1] if v.startswith('"') else v


def apply_grade(src: str, row: dict, got: dict) -> str:
    """Rewrite exactly the outcome fields of the one row this grade belongs to.

    Identity is the (instrument, horizon_label, anchor_date, cycle_no) tuple, matched
    on the parsed row text — never on position — and it must match exactly one row.
    """
    def num(x):
        s = f'{x:.4f}'.rstrip('0').rstrip('.')
        return s if s else '0'

    hits = []
    for a, b in ledger_row_spans(src):
        t = src[a:b]
        if (_field(t, 'instrument') == row['instrument']
                and _field(t, 'horizon_label') == row['horizon_label']
                and _field(t, 'anchor_date') == row['anchor_date']
                and _field(t, 'cycle_no') == str(row['cycle_no'])):
            hits.append((a, b))
    if len(hits) != 1:
        raise SystemExit(f"expected exactly 1 row for {row['instrument']} "
                         f"{row['horizon_label']} {row['anchor_date']} cycle {row['cycle_no']}, "
                         f"found {len(hits)}")
    a, b = hits[0]
    t = src[a:b]
    if _field(t, 'realized_close') != 'null':
        raise SystemExit('refusing to regrade an already-graded row — graded rows are permanent')

    jb = lambda v: 'true' if v else 'false'
    rq = 'null' if got['realized_quantile'] is None else f"{got['realized_quantile']:.3f}"
    new_outcome = (
        f"realized_close:{num(got['realized_close'])}, "
        f"realized_high:{num(got['realized_high'])}, "
        f"realized_low:{num(got['realized_low'])},")
    old_outcome = re.search(r'realized_close:null, realized_high:null, realized_low:null,', t)
    if not old_outcome:
        raise SystemExit('outcome block not in the expected shape')
    t2 = t.replace(old_outcome.group(0), new_outcome)

    old_stats = re.search(r'in_90:null, in_50:null, realized_quantile:null, median_err:null,', t2)
    if not old_stats:
        raise SystemExit('stats block not in the expected shape')
    t2 = t2.replace(old_stats.group(0),
                    f"in_90:{jb(got['in_90'])}, in_50:{jb(got['in_50'])}, "
                    f"realized_quantile:{rq}, median_err:{got['median_err']:.4f},")

    old_th = re.search(r'touch_hit:\{[^}]*\}', t2)
    if not old_th:
        raise SystemExit('touch_hit block not found')
    th = ', '.join(f'"{k}":{jb(got["touch_hit"][k])}' for k, _ in REL)
    t2 = t2.replace(old_th.group(0), 'touch_hit:{ ' + th + ' }')

    # A closure/suspension that pushed the graded session past the stored date is
    # ANNOTATED, never overwritten (STEP 3.3).
    if got['_rolled']:
        t2 = t2.replace(f"grade_date:\"{row['grade_date']}\"",
                        f"grade_date:\"{got['_graded_on']}\", "
                        f"grade_date_projected:\"{row['grade_date']}\", "
                        f"grade_note:\"Stored grade date {row['grade_date']} was not a traded "
                        f"session in the library; graded on the next actual session "
                        f"{got['_graded_on']}.\"")

    # A corporate action inside the window is likewise ANNOTATED, never silent: the
    # frozen percentiles stay exactly as published and the realized window is the
    # thing restated onto their basis. Recording the factor is what lets a reader
    # recompute the grade from the library without knowing the action happened.
    if got.get('_ca', 1.0) != 1.0:
        ca = got['_ca']
        t2 = t2.replace(f"anchor_price:{_field(t2, 'anchor_price')},",
                        f"anchor_price:{_field(t2, 'anchor_price')}, "
                        f"ca_factor:{ca:.6f},", 1)
        note = (f"A corporate action went ex inside this window: the library has since "
                f"been restated onto a new share basis, so its close for the anchor "
                f"session {row['anchor_date']} is {row['anchor_price'] / ca:.2f} against "
                f"the {row['anchor_price']} this cone was struck on. The realized close, "
                f"high and low are restated by x{ca:.6f} onto the anchor's basis; the "
                f"published percentiles are untouched.")
        if 'grade_note:' in t2:
            t2 = re.sub(r'grade_note:"([^"]*)"', lambda m: f'grade_note:"{m.group(1)} {note}"', t2, count=1)
        else:
            t2 = t2.replace(f"grade_date:\"{row['grade_date']}\"",
                            f"grade_date:\"{row['grade_date']}\", grade_note:\"{note}\"", 1)
    return src[:a] + t2 + src[b:]
