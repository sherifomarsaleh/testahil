"""apply_technicals.py — write the computed technical read into assets/data.js.

Surgical by construction, in the same spirit as apply_rollforward.py. For each
in-scope name it rewrites ONLY:

    levels · tech        (recomputed by technicals.py from the OHLC library)
    asof                 (inserted: the two-part data/computed stamp for the
                          Monte Carlo block and the technical block)

Everything else on a ticker entry is left byte-identical — spot, spotDate,
dist, hz, touch, fair{bear,base,full}, the slider's factor-stack constants and
files. The Monte Carlo cone is NOT re-struck here; this module only stamps the
cone that is already published, reading its anchor date off the newest LEDGER
row for that instrument and its run date off that row's own note.

Two formatting conventions live in data.js — the indented TICKERS style and
the compact METALS style. Rather than assume either, every field is located by
a brace-matching scan that respects string literals, and rewritten at whatever
indent it was found on.

Run:  python3 apply_technicals.py                 # plan only, touches nothing
      python3 apply_technicals.py --only COMI     # pilot one name
      python3 apply_technicals.py --write         # apply
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import technicals as TA                                    # noqa: E402

DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
RAW = os.path.join(HERE, 'raw_ohlc')

# exchange prefix on the site's `code` field -> raw_ohlc market folder
EXCHANGE_MARKET = {'EGX': 'EG', 'ADX': 'AE', 'DFM': 'AE', 'TADAWUL': 'SA',
                   'KRX': 'KR', 'NASDAQ': 'US', 'NYSE': 'US',
                   'NSE': 'IN', 'BSE': 'IN', 'QSE': 'QA', 'QE': 'QA'}
# site ticker key -> series name in the library, where they differ
SERIES_OVERRIDE = {'ALRAJHI': 'RAJHI', 'ADIBUAE': 'ADIB',
                   '2POINTZERO': 'TWOPOINTZERO'}
# METALS keys are not exchange-coded
METAL_MARKET = {'GOLD': ('XAU', 'GOLD'), 'SILVER': ('XAU', 'SILVER'),
                'PLATINUM': ('XPT', 'PLATINUM')}
# LEDGER instrument names differ in case from the METALS keys
LEDGER_ALIAS = {'GOLD': 'Gold', 'SILVER': 'Silver', 'PLATINUM': 'Platinum',
                'SAMSUNG': 'Samsung', 'KAKAO': 'Kakao'}


# ------------------------------------------------------------------- scanning
def match_brace(src: str, i: int) -> int:
    """Index just past the '}' matching the '{' at i.

    Aware of string literals AND of comments: data.js carries prose comments
    with apostrophes ("EG's own calendar"), and a naive scanner reads that
    apostrophe as the start of a string and then swallows the rest of the file.
    """
    assert src[i] == '{', f'expected {{ at {i}, found {src[i]!r}'
    depth, j, n = 0, i, len(src)
    while j < n:
        c = src[j]
        if c == '/' and j + 1 < n and src[j + 1] == '/':
            j = src.find('\n', j)
            if j < 0:
                break
            continue
        if c == '/' and j + 1 < n and src[j + 1] == '*':
            k = src.find('*/', j + 2)
            j = (k + 2) if k >= 0 else n
            continue
        if c in '"\'`':
            q, j = c, j + 1
            while j < n and src[j] != q:
                j += 2 if src[j] == '\\' else 1
            j += 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise ValueError('unbalanced braces')


def top_level_blocks(src: str, decl: str):
    """{key: (start, end)} for every entry of a top-level `const NAME = {...}`."""
    d = src.find(decl)
    if d < 0:
        return {}
    o = src.index('{', d)
    end = match_brace(src, o)
    body, out, j = src[o + 1:end - 1], {}, 0
    while True:
        # keys may be quoted — "2POINTZERO" must be, because a JS identifier
        # cannot start with a digit. An unquoted-only pattern silently skipped it.
        m = re.compile(r'\n\s*"?([A-Z0-9_]+)"?\s*:\s*\{').search(body, j)
        if not m:
            break
        a = o + 1 + m.start(0)
        b = o + 1 + match_brace(body, m.end(0) - 1)
        out[m.group(1)] = (a, b)
        j = m.end(0)
    return out


def field_span(block: str, field: str):
    """(start_of_line, end_of_object, indent) for `field: {...}` in a block."""
    m = re.search(r'\n([ \t]*)' + re.escape(field) + r'\s*:\s*\{', block)
    if not m:
        return None
    obj_open = block.index('{', m.end(0) - 1)
    return m.start(0), match_brace(block, obj_open), m.group(1)


def field_spans(block: str, field: str):
    """EVERY TOP-LEVEL `field: {...}` span in an entry, in source order.

    field_span() returns the FIRST, which is silently wrong wherever an entry
    carries the same key TWICE. JavaScript object literals take the LAST key,
    so this module rewrote the first `levels` while the page went on rendering
    a superseded one -- a freshly computed narrative sitting over a level
    ladder from the retired hand-authored era, with valid markup, no console
    error and nothing to see. Found 24-Aug-2026 on CLHO, RMDA and GBCO (RMDA's
    stale ladder put all three of its resistances BELOW its own close).

    Same species as the unquoted-key regex that dropped 2POINTZERO from three
    tools at once, and the indentation-keyed `dist` match that deleted `touch`
    on nine entries: a pattern standing in for a parser is silently correct on
    the entries that happen to be shaped the way its author's were. Closing the
    class rather than the instance ([R-ENF-01]).

    TOP-LEVEL IS ENFORCED BY INDENT, and that is not a nicety: `asof` carries a
    NESTED `tech: {...}` sub-object, so a depth-blind version of this function
    reported a duplicate `tech` on all 93 entries and would have deleted every
    as-of stamp on the site. A candidate is accepted only if its indent matches
    the first match's AND it does not fall inside an already-accepted span.
    """
    pat = re.compile(r'\n([ \t]*)' + re.escape(field) + r'\s*:\s*\{')
    out, pos, ind0 = [], 0, None
    while True:
        m = pat.search(block, pos)
        if not m:
            return out
        obj_open = block.index('{', m.end(0) - 1)
        end = match_brace(block, obj_open)
        if ind0 is None:
            ind0 = m.group(1)
        if m.group(1) == ind0 and not any(s0 <= m.start(0) < s1 for s0, s1, _ in out):
            out.append((m.start(0), end, m.group(1)))
        pos = end


def trailing_len(block: str, i: int) -> int:
    """Chars after a field's closing brace that belong to that field's LINE.

    A replacement span stops at `}`, so the trailing `,` and any `// ...` note
    on the same line SURVIVE a rewrite. That is how CLHO, RMDA and GBCO each
    ended up carrying a machine-recomputed ladder under a hand-written
    `// 19 Jul 2026 - computed from own OHLC` note: the numbers moved on every
    pass, the date never did, and the comment then dated its own line wrongly.
    A comment on a field this module OWNS is consumed with the field; the
    as-of stamp is the date of record. Same class as the duplicate key one line
    to its left ([R-ENF-01]) -- a survivor of a rewrite that nothing renders
    and nothing checks.
    """
    return re.match(r',?[ \t]*(//[^\n]*)?', block[i:]).end()


def drop_superseded(block: str, fields=('levels', 'tech', 'asof')):
    """Delete every duplicate of a field this module owns, keeping the FIRST.

    The first is the one field_span() rewrites, so keeping it is what makes the
    recomputed read the published one. Returns (block, dropped_field_names).
    A block with no duplicates comes back BYTE-IDENTICAL -- verified across all
    90 entries when this landed.
    """
    dropped = []
    for field in fields:
        for s0, s1, _ in reversed(field_spans(block, field)[1:]):
            trail = 1 if block[s1:s1 + 1] == ',' else 0
            block = block[:s0] + block[s1 + trail:]
            dropped.append(field)
    return block, dropped


# ------------------------------------------------------------------ emitting
def js_str(s: str) -> str:
    """A JS double-quoted literal, non-ASCII escaped to match the file."""
    out = ['"']
    for ch in s:
        if ch == '"':
            out.append('\\"')
        elif ch == '\\':
            out.append('\\\\')
        elif ord(ch) < 32:
            out.append(f'\\u{ord(ch):04x}')
        elif ord(ch) > 126:
            out.append(f'\\u{ord(ch):04x}')
        else:
            out.append(ch)
    return ''.join(out) + '"'


def num(x) -> str:
    return str(int(x)) if isinstance(x, int) or float(x).is_integer() else f'{x:.2f}'


def emit_levels(lv: dict, ind: str) -> str:
    return (f'\n{ind}levels: {{ res:[' + ', '.join(num(v) for v in lv['res'])
            + '], sup:[' + ', '.join(num(v) for v in lv['sup']) + '] },')


def emit_tech(t: dict, ind: str) -> str:
    i2 = ind + '  '
    return (f'\n{ind}tech: {{\n'
            + f'{i2}trend: {js_str(t["trend"])},\n'
            + f'{i2}summary: {js_str(t["summary"])},\n'
            + f'{i2}bull: {js_str(t["bull"])},\n'
            + f'{i2}bear: {js_str(t["bear"])}\n'
            + f'{ind}}},')


def emit_asof(a: dict, ind: str) -> str:
    i2 = ind + '  '
    return (f'\n{ind}asof: {{\n'
            + f'{i2}mc:   {{ data:"{a["mc"]["data"]}", '
              f'computed:"{a["mc"]["computed"]}" }},\n'
            + f'{i2}tech: {{ data:"{a["tech"]["data"]}", '
              f'computed:"{a["tech"]["computed"]}" }}\n'
            + f'{ind}}},')


# -------------------------------------------------------------- MC provenance
SPOTDATE_RE = re.compile(r'spotDate\s*:\s*"[^"]*?(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})')
# The strike date is READ FROM A FIELD, never scraped out of the note prose.
# Scraping was the 29-Jul defect: NOTE_RUN_RE took the first dd-Mon-yyyy
# anywhere in the note, so platinum's "origins 05-Jan-2012 -> 13-Feb-2026"
# (the calibration SAMPLE START) was stamped as the day the cone was run.
# Every LEDGER row now carries run_date:"YYYY-MM-DD"; no fallback to prose.
RUN_DATE_RE = re.compile(r'run_date\s*:\s*"(\d{4}-\d{2}-\d{2})"')
MONTHS = {m: i + 1 for i, m in enumerate(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}


def spotdate_iso(block: str):
    m = SPOTDATE_RE.search(block)
    if not m:
        return None
    d, mon, y = int(m.group(1)), MONTHS.get(m.group(2).title()), int(m.group(3))
    return f'{y:04d}-{mon:02d}-{d:02d}' if mon else None


def ledger_index(src: str):
    """Newest (anchor_date, run_date) per instrument, straight from LEDGER."""
    i = src.find('const LEDGER')
    if i < 0:
        return {}
    j = src.find('\n];', i)
    led, out = src[i:j], {}
    for m in re.finditer(r'instrument:"([^"]+)"', led):
        seg = led[m.start():m.start() + 4000]
        ad = re.search(r'anchor_date:"([^"]+)"', seg)
        if not ad:
            continue
        nm = m.group(1)
        rd = RUN_DATE_RE.search(seg[:ad.end() + 40])
        run = rd.group(1) if rd else None
        cur = out.get(nm)
        if cur is None or ad.group(1) > cur[0]:
            out[nm] = (ad.group(1), run)
    return out


# ------------------------------------------------------------------- driving
def scope(src: str, only=None):
    """[(key, container, market, series)] for every name with a library."""
    out = []
    for key, _ in top_level_blocks(src, 'const TICKERS = {').items():
        a, b = top_level_blocks(src, 'const TICKERS = {')[key]
        pre = re.search(r'code:\s*"([A-Z0-9]+):', src[a:b])
        if not pre:
            continue
        mkt = EXCHANGE_MARKET.get(pre.group(1))
        if not mkt:
            continue
        out.append((key, 'TICKERS', mkt, SERIES_OVERRIDE.get(key, key)))
    for key in top_level_blocks(src, 'const METALS = {'):
        if key in METAL_MARKET:
            out.append((key, 'METALS', *METAL_MARKET[key]))
    out = [r for r in out
           if os.path.exists(os.path.join(RAW, r[2], r[3] + '.csv'))]
    if only:
        want = {k.upper() for k in only}
        out = [r for r in out if r[0].upper() in want]
    return sorted(out)


def run(write=False, only=None, computed_on=None):
    src = open(DATA_JS, encoding='utf-8').read()
    computed_on = computed_on or date.today().isoformat()
    led = ledger_index(src)
    todo = scope(src, only)
    print(f'in scope: {len(todo)} name(s) with an OHLC library')

    edits, report, skipped = [], [], []
    for key, container, mkt, series in todo:
        decl = f'const {container} = {{'
        a, b = top_level_blocks(src, decl)[key]
        block = src[a:b]
        # A DUPLICATE KEY IS A SILENT OVERRIDE, NOT A FORMATTING QUIRK.
        block, dropped = drop_superseded(block)
        if dropped:
            print(f'  {key}: dropped superseded duplicate key(s) '
                  f'{sorted(set(dropped))} — JavaScript was rendering the LAST '
                  f'one, so the recomputed read was written and never seen')
        try:
            st = TA.compute(mkt, series, computed_on=computed_on)
        except Exception as e:                                # noqa: BLE001
            skipped.append((key, f'{type(e).__name__}: {e}'))
            continue

        lv_span = field_span(block, 'levels')
        tk_span = field_span(block, 'tech')
        if not lv_span or not tk_span:
            skipped.append((key, 'no levels/tech field to replace'))
            continue

        inst = LEDGER_ALIAS.get(key, key)
        anchor, runday = led.get(inst, (None, None))
        page_anchor = spotdate_iso(block)
        if page_anchor and (not anchor or page_anchor > anchor):
            # MID-CYCLE cone refresh — STEP 0 decision (a). Data arriving
            # between monthly events re-strikes the displayed cone WITHOUT
            # minting a LEDGER row, so the newest ledger anchor is no longer
            # the cone's anchor and stamping from it would publish a fresh
            # cone under a week-old date -- the exact gap the two-part stamp
            # exists to expose. `spot`/`spotDate` and `dist` are always
            # written as one unit by rollforward_one.restrike_entry, so the
            # page's own spotDate IS the anchor the displayed cone was struck
            # on. A genuinely stale cone still warns: there spotDate and the
            # ledger anchor agree and both trail the technical read.
            mc_data = page_anchor
            # A mid-cycle strike mints no LEDGER row, so there is no sourced
            # run_date to read. Keep the recorded compute day when the stamp
            # is not moving (this pass must stay idempotent on an unchanged
            # library); otherwise fall back to the anchor itself, the same
            # convention this module already uses for an unsourced run date.
            # NOT `computed_on` — a technicals pass does not re-strike a cone,
            # so stamping it with today would claim a cone was computed on a
            # day it was not, which is precisely the false-freshness the
            # two-part stamp exists to expose.
            prior = re.search(r'mc:\s*\{\s*data:\s*"([\d-]+)"\s*,\s*'
                              r'computed:\s*"([\d-]+)"', block)
            mc_run = (prior.group(2) if prior and prior.group(1) == mc_data
                      else mc_data)
        else:
            mc_data = anchor or page_anchor or st['data_date']
            mc_run = runday or mc_data
        asof = {'mc': {'data': mc_data, 'computed': mc_run},
                'tech': {'data': st['data_date'], 'computed': computed_on}}

        new = block
        # replace tech first (later in the block than levels on every entry we
        # touch), then levels, so the earlier span's offsets still hold
        for span, text in sorted(
                [(tk_span, emit_tech(st['tech'], tk_span[2])),
                 (lv_span, emit_levels(st['levels'], lv_span[2]))],
                key=lambda p: -p[0][0]):
            s0, s1, _ = span
            new = (new[:s0] + text.rstrip(',') + ','
                   + new[s1 + trailing_len(new, s1):])

        # asof: replace if present, else insert immediately after tech
        ao = field_span(new, 'asof')
        if ao:
            s0, s1, ind = ao
            new = new[:s0] + emit_asof(asof, ind) + new[s1 + trailing_len(new, s1):]
        else:
            tk2 = field_span(new, 'tech')
            ins = tk2[1] + (1 if new[tk2[1]:tk2[1] + 1] == ',' else 0)
            new = new[:ins] + emit_asof(asof, tk2[2]) + new[ins:]

        edits.append((a, b, new))
        report.append({'key': key, 'market': mkt, 'series': series,
                       'close': st['close'], 'sessions': st['sessions'],
                       'ta_data': st['data_date'], 'mc_data': mc_data,
                       'mc_computed': mc_run, 'repairs': st['repairs'],
                       'levels': st['levels'], 'tech': st['tech']})

    for a, b, new in sorted(edits, key=lambda e: -e[0]):
        src = src[:a] + new + src[b:]

    print(f'rewritten: {len(report)}   skipped: {len(skipped)}')
    for k, why in skipped:
        print(f'  SKIP {k}: {why}')

    if write:
        open(DATA_JS, 'w', encoding='utf-8').write(src)
        json.dump(report, open(os.path.join(HERE, 'technicals_report.json'), 'w'),
                  indent=1)
        print(f'wrote {DATA_JS}')
    return src, report, skipped


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--computed-on')
    args = ap.parse_args()
    _, rep, _ = run(write=args.write, only=args.only,
                    computed_on=args.computed_on)
    for r in rep[:6]:
        print(f"\n{r['key']} ({r['market']}/{r['series']}) close {r['close']} "
              f"on {r['ta_data']}")
        print(f"  levels {r['levels']}")
        print(f"  trend  {r['tech']['trend']}")
