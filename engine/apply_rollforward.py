"""apply_rollforward.py — write re-struck cones into assets/data.js.

Surgical by construction. For each in-scope ticker it rewrites ONLY:

    spot · spotDate · dist · touch      (+ inserts hz, the calendar-convention
                                         marker, when not already present)

and appends one LEDGER row per horizon. Everything else on a ticker entry is
left byte-identical — fair{bear,base,full} (separate clock, needs a real study
refresh), the interactive slider's bespoke factor-stack constants, the
technical S/R `levels` and `tech` narrative (need a fresh chart read), and
`files`. The touch ladder is recomputed at the SAME ABSOLUTE LEVELS already on
the page, never re-picked.

Run:  python3 apply_rollforward.py [--write]
Without --write it reports the plan and touches nothing.
"""
from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                                        # noqa: E402
import pandas as pd                                       # noqa: E402

from strike_cohorts import strike, touch_probs, rel_touch  # noqa: E402
import market_profiles as MP                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')

# ticker key on the site -> (profile code, series name in raw_ohlc)
EXCHANGE_MARKET = {'EGX': 'EG', 'ADX': 'AE', 'DFM': 'AE', 'TADAWUL': 'SA'}
SERIES_OVERRIDE = {'ALRAJHI': 'RAJHI', 'ADIBUAE': 'ADIB'}

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

RF_SRC = {'EG': '19.50% CBE main operation rate',
          'AE': '3.65% CBUAE base rate (AED peg -> Fed path)',
          'SA': '4.25% SAMA repo-anchored estimate',
          # Metals are USD carry-only: rf IS the whole drift, so naming its source
          # matters more here than anywhere else. Without an entry the note fell
          # back to the placeholder "3.63% profile rf_live", which names no source
          # at all -- on a carry-only instrument that is the one number a reader
          # needs to be able to check.
          'XAU': '3.63% Fed funds midpoint schedule (USD cost-of-carry anchor)',
          'XPT': '3.63% Fed funds midpoint schedule (USD cost-of-carry anchor)'}


# ------------------------------------------------------------------ parsing

def _match_brace(src: str, i: int) -> int:
    """Index just past the '}' matching the '{' at i. String- and comment-aware."""
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
            j = src.find('*/', j) + 2
            continue
        if c in '"\'':
            q, j = c, j + 1
            while j < n:
                if src[j] == '\\':
                    j += 2
                    continue
                if src[j] == q:
                    break
                j += 1
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise ValueError('unbalanced braces')

def ticker_blocks(src: str):
    """{key: (start, end)} for every entry of `const TICKERS = {...}`.

    Keys may be QUOTED — "2POINTZERO" must be, since a JS identifier cannot
    start with a digit. The unquoted-only pattern silently dropped it, which is
    why the 28-Jul-2026 market-wide pass re-struck 58 cones instead of 59 and
    left 2POINTZERO's cone anchored 03-Jul against a library already at 24-Jul.

    THE SCAN IS BOUNDED TO THE TICKERS OBJECT (fixed 23-Aug-2026). It used to
    run from `const TICKERS = {` to the FIRST `\n};` after the last key match,
    which is not the same thing: the regex kept matching past the end of the
    object, so the three entries of `const METALS = {...}` — GOLD, SILVER,
    PLATINUM — were returned as if they were ticker entries. It reported 93
    blocks against a TICKERS object holding 90, and nothing counted. Same
    family as the 2POINTZERO defect that this function's own comment records:
    a pattern standing in for a parser. Metals are a DIFFERENT object with a
    different shape (a t252 twelve-month cone, compact one-space indent), so a
    caller handed one as a ticker either crashes or, worse, rewrites it to the
    ticker shape. The end of the object is now found by brace matching.
    """
    st = src.find('const TICKERS = {')
    if st < 0:
        return {}
    o = src.index('{', st)
    stop = _match_brace(src, o)
    idx = [(m.start() + o, m.group(1))
           for m in re.finditer(r'\n  "?([A-Z0-9]+)"?: \{', src[o:stop])]
    out = {}
    for i, (q, k) in enumerate(idx):
        end = idx[i + 1][0] if i + 1 < len(idx) else src.rfind('\n};', q, stop + 3)
        out[k] = (q, end)
    return out


def parse_touch_levels(block: str):
    m = re.search(r'\n    touch: \[(.*?)\n    \]', block, re.S)
    if not m:
        return None, None
    inner = m.group(1)
    lv = [float(x) for x in re.findall(r'\[\s*(-?[\d.]+)\s*,', inner)]
    comment = re.search(r'/\*.*?\*/', inner, re.S)
    return lv, (comment.group(0) if comment else '/* descending high -> low */')


def fmt_price(x: float, ref: float) -> str:
    """Match the decimal convention the page already uses for this name."""
    if ref >= 1000:
        return f'{x:,.0f}'.replace(',', '')
    return f'{x:.2f}'


def in_scope(src: str):
    """Yield (key, market, series) for every published EG/AE/SA cone."""
    out = []
    for k, (a, b) in ticker_blocks(src).items():
        blk = src[a:b]
        m = re.search(r'code:\s*"([A-Z]+):', blk)
        if not m or m.group(1) not in EXCHANGE_MARKET:
            continue
        if '\n    dist: {' not in blk:
            continue
        mk = EXCHANGE_MARKET[m.group(1)]
        out.append((k, mk, SERIES_OVERRIDE.get(k, k)))
    return sorted(out)


# ------------------------------------------------------------------ building
def build(write: bool = False):
    src = open(DATA_JS).read()
    scope = in_scope(src)
    print(f"in scope: {len(scope)} published cones "
          f"({sum(1 for _, m, _ in scope if m == 'EG')} EG / "
          f"{sum(1 for _, m, _ in scope if m == 'AE')} AE / "
          f"{sum(1 for _, m, _ in scope if m == 'SA')} SA)")

    struck, ledger_rows, report = {}, [], []
    for key, mkt, series in scope:
        r = strike(mkt, series)
        struck[key] = r
        report.append((key, mkt, series, r))

    # ---- rewrite each ticker block, from the bottom up so offsets hold
    blocks = ticker_blocks(src)
    edits = []
    for key, mkt, series, r in report:
        a, b = blocks[key]
        blk = src[a:b]
        h1 = r['horizons']['1M']
        h3 = r['horizons']['3M']
        spot = r['spot']
        anchor = pd.Timestamp(r['anchor_date'])
        sd = f"close {anchor.day:02d} {MONTHS[anchor.month - 1]} {anchor.year}"

        new = blk
        # spot
        new = re.sub(r'\n    spot: [\d.,]+,',
                     f'\n    spot: {fmt_price(spot, spot)},', new, count=1)
        # spotDate
        new = re.sub(r'\n    spotDate: "[^"]*",',
                     f'\n    spotDate: "{sd}",', new, count=1)

        # dist
        def row(tag, h, pad):
            p = h['pct']
            f = lambda v: fmt_price(v, spot)  # noqa: E731
            return (f'      {tag}: {{ label:"{h["label"]}",{pad}'
                    f'p5:{f(p["p5"])}, p25:{f(p["p25"])}, p50:{f(p["p50"])}, '
                    f'p75:{f(p["p75"])}, p95:{f(p["p95"])}, '
                    f'resolve:"{h["grade_date"]}" }}')
        dist = ('    dist: {\n'
                + row('t20', h1, '   ') + ',\n'
                + row('t60', h3, '  ') + '\n'
                + '    },\n'
                + f'    hz: {{ h1:{h1["h"]}, h3:{h3["h"]}, '
                  f'l1:"{h1["label"]}", l3:"{h3["label"]}", cal:true }},')
        new = re.sub(r'\n    dist: \{.*?\n    \},(?:\n    hz: \{[^}]*\},)?',
                     '\n' + dist, new, count=1, flags=re.S)

        # touch — SAME absolute levels, probabilities recomputed
        levels, comment = parse_touch_levels(blk)
        if levels:
            t1 = touch_probs(h1['_paths'], spot, levels)
            t3 = touch_probs(h3['_paths'], spot, levels)
            cells = ', '.join(
                f'[{fmt_price(lv, spot)}, {t1[float(lv)]}, {t3[float(lv)]}]'
                for lv in levels)
            new = re.sub(r'\n    touch: \[.*?\n    \]',
                         f'\n    touch: [ {comment}\n      {cells}\n    ]',
                         new, count=1, flags=re.S)
        edits.append((a, b, new))

        # ---- ledger rows
        prof = MP.PROFILES[mkt]
        ccy = (re.search(r'ccy:\s*"([^"]+)"', blk) or [None, '?'])[1]
        prior = prior_anchor(src, key)
        cyc = prior[1] + 1 if prior else 2
        note = (
            f"Cycle {cyc} roll-forward, 28-Jul-2026 — market-wide re-strike of "
            f"EG/AE/SA onto the 15-year calibration libraries and the calendar "
            f"horizon convention. Production chain, no approximation: Step 0.0 "
            f"data-quality gate → YZ variance proxy → fit_har_v3 → "
            f"har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) → "
            f"simulate_paths_v3, 50,000 paths, seed 42, signal OFF. "
            f"q_annual=0 (FLAGGED — house convention; the drift is a "
            f"GROSS-OF-DIVIDEND price carry and overstates the centre by "
            f"roughly the yield). {mkt} live fit nu={prof.nu}, "
            f"width_cal={prof.width_cal}; rf_live {RF_SRC[mkt]}. Horizon "
            f"resolved by horizons.resolve() on {mkt}'s own realized calendar, "
            f"not a session count.")
        if prior and prior[0] == r['anchor_date']:
            note += (
                " RE-ISSUE AT AN UNCHANGED ANCHOR: this name was already re-struck "
                f"at this same {r['anchor_date']} close (cycle {prior[1]}), so "
                "reanchor_from equals this row's own anchor_date. Nothing was "
                "re-anchored — the cycle exists only because the cone itself "
                f"changed: cycle {prior[1]} was struck on the retired "
                "retired session-counted convention under the then-live fit, and "
                "this row re-issues the same anchor on the calendar 1M/3M "
                f"convention under the current fit. Cycle {prior[1]} keeps its "
                "published percentiles and grades exactly as issued.")
        for tag, h in (('1M', h1), ('3M', h3)):
            tp = rel_touch(h['_paths'], spot)
            ledger_rows.append(dict(
                instrument=key, asset_class='equity',
                anchor_date=r['anchor_date'], run_date='2026-07-28',
                anchor_price=round(spot, 4),
                ccy=ccy, horizon_label=h['label'], grade_date=h['grade_date'],
                grade_basis=h['basis'], horizon_days=h['h'],
                cycle_no=cyc, reanchor_from=(prior[0] if prior else None),
                anchor_vol=round(h['anchor_vol_ann'], 4),
                note=note,
                p5=round(h['pct']['p5'], 2), p25=round(h['pct']['p25'], 2),
                p50=round(h['pct']['p50'], 2), p75=round(h['pct']['p75'], 2),
                p95=round(h['pct']['p95'], 2), touch=tp))

    for a, b, new in sorted(edits, key=lambda e: -e[0]):
        src = src[:a] + new + src[b:]

    src = insert_ledger(src, ledger_rows)
    src = bump_site_updated(src, '2026-07-28')

    if write:
        open(DATA_JS, 'w').write(src)
        json.dump(ledger_rows, open(os.path.join(HERE, 'rollforward_ledger.json'), 'w'),
                  indent=1, default=str)
        print(f"wrote {DATA_JS} and {len(ledger_rows)} ledger rows")
    return src, report, ledger_rows


def prior_anchor(src: str, instrument: str):
    """Most recent (anchor_date, cycle_no) already in the ledger for a name."""
    i = src.find('const LEDGER')
    j = src.find('\n];', i)
    led = src[i:j]
    best = None
    for m in re.finditer(r'instrument:"' + re.escape(instrument) + r'"(.{0,600})',
                         led, re.S):
        e = m.group(1)
        ad = re.search(r'anchor_date:"([^"]+)"', e)
        cy = re.search(r'cycle_no:(\d+)', e)
        if ad and cy:
            cand = (ad.group(1), int(cy.group(1)))
            if best is None or cand[1] > best[1]:
                best = cand
    return best


def js_row(d: dict) -> str:
    def v(x):
        if x is None:
            return 'null'
        if isinstance(x, bool):
            return 'true' if x else 'false'
        if isinstance(x, (int, float)):
            return repr(x)
        return json.dumps(x, ensure_ascii=False)
    t = ', '.join(f'"{k}":{n}' for k, n in d['touch'].items())
    # THE DIRECTION CALL IS PART OF THE RECORD [R-DRIFT-01, 23-Aug-2026]. The rule
    # says every strike records signal_z/signal_alpha and every call is graded at its
    # maturity — and a call that is not stored cannot be graded later. strike_cohorts
    # has always computed both; nothing persisted them, so the engine's own lean was
    # invisible the moment the run ended. Emitted only when the caller supplies them,
    # so every pre-tilt caller still produces byte-identical rows.
    sig = ''
    if 'signal_z' in d and 'signal_alpha' in d:
        sig = f'    signal_z:{d["signal_z"]}, signal_alpha:{d["signal_alpha"]},\n'
    # THE NAME-LEVEL CALIBRATION VERDICT IS PART OF THE RECORD. Publish_Protocol.md:
    # "Set the row's `cal` field ONLY for matches / untested / fail -- absent means
    # PASS." Until now only first-publish rows carried it, so a roll-forward struck
    # for a name whose own verdict had since turned FAIL emitted a row that asserted
    # PASS by omission -- the exact silence R-CAL-01 exists to prevent. Emitted only
    # when the caller supplies it, so every PASS name still produces a byte-identical
    # row. Placed after anchor_vol, matching the existing first-publish rows.
    cal = f', cal:{v(d["cal"])}' if d.get('cal') else ''
    # run_date is a FIELD, never prose. scripts/check_data_freshness.py hard-fails a
    # row without one ("the strike date must be a field, never scraped out of the note"),
    # and this emitter silently omitted it — caught on the 05-Aug-2026 QNB strike, the
    # first time a row it produced was run through that gate. anchor_date is the close
    # the cone sits on; run_date is the day it was struck, and they are routinely
    # different (a strike on Tuesday's close published Wednesday).
    return (
        '  {\n'
        f'    instrument:{v(d["instrument"])}, asset_class:{v(d["asset_class"])},\n'
        f'    anchor_date:{v(d["anchor_date"])}, run_date:{v(d["run_date"])}, '
        f'anchor_price:{d["anchor_price"]}, '
        f'ccy:{v(d["ccy"])},\n'
        f'    horizon_label:{v(d["horizon_label"])}, grade_date:{v(d["grade_date"])}, '
        f'grade_basis:{v(d["grade_basis"])}, horizon_days:{d["horizon_days"]},\n'
        f'    cycle_no:{d["cycle_no"]}, reanchor_from:{v(d["reanchor_from"])}, '
        f'anchor_vol:{d["anchor_vol"]}{cal},\n'
        + sig +
        f'    note:{v(d["note"])},\n'
        f'    p5:{d["p5"]}, p25:{d["p25"]}, p50:{d["p50"]}, p75:{d["p75"]}, p95:{d["p95"]},\n'
        f'    touch:{{ {t} }},\n'
        '    realized_close:null, realized_high:null, realized_low:null,\n'
        '    in_90:null, in_50:null, realized_quantile:null, median_err:null,\n'
        '    touch_hit:{ "+5":null, "+10":null, "+15":null, "+20":null, "-5":null, "-10":null }\n'
        '  }')


def insert_ledger(src: str, rows) -> str:
    i = src.find('const LEDGER')
    j = src.find('\n];', i)
    header = ('\n\n  // ---- 28-Jul-2026 MARKET-WIDE RE-STRIKE — EG/AE/SA onto the\n'
              '  //      15-year calibration libraries + the calendar 1M/3M horizon\n'
              '  //      convention. Append-only: every cohort above keeps the\n'
              '  //      horizon and percentiles it was published with.\n')
    body = ',\n'.join(js_row(r) for r in rows)
    return src[:j] + header + body + src[j:]


def bump_site_updated(src: str, date: str) -> str:
    """Move SITE.updated forward to `date` — never backward. [MONOTONIC 05-Aug-2026]

    SITE.updated is the site-wide "last updated" shown on every page; it means
    "the most recent thing that happened here", not "the anchor of whichever
    name I just touched". A single-name refresh stamps it with THAT NAME's
    library close, which is older than the site's last publish whenever the
    name's own data lags. Refreshing ORAS (library to 29-Jul) the same day ELEC
    published (05-Aug) rolled the whole site's date back a week — every page
    quietly claiming to be staler than it was, and the next freshness pass
    would have read that as truth.

    Going forward is always right (something did just happen); going backward
    never is, so it is clamped rather than trusted to the caller.
    """
    m = re.search(r'const SITE = \{ updated: "([^"]*)"', src)
    if m and m.group(1) > date:          # ISO dates: lexicographic == chronological
        return src
    return re.sub(r'(const SITE = \{ updated: ")[^"]*(")', rf'\g<1>{date}\g<2>',
                  src, count=1)




# ---------------------------------------------------------------- replay guard
REPLAY_FLAG = '--i-am-replaying-28-jul-2026'
_REFUSE = f"""apply_rollforward.py is the RECORD of the 28-Jul-2026 market-wide re-strike,
not a live tool, and running it today publishes a cone under a date a month old.

Its per-row note AND its run_date are HARDCODED to that pass — run_date='2026-07-28'.
apply_technicals stamps asof.mc.computed from the newest LEDGER row's run_date, so a
run today writes a fresh cone and then tells every page it was computed on
2026-07-28. It also writes NO `fit` stamp, so check_data_freshness's 2b cannot
catch it: an entry with no stamp is deliberately not failed.

That is the SAME defect closed on 25-Aug-2026 (PR #277), reached by a second route.
[R-ENF-01]: when a defect of this species is found again, close the CLASS, not the
instance — and a warning that lives only in another module's docstring is not a
check, which is exactly why this one had gone unenforced.

Use instead:
  engine/rollforward_one.py   — the monthly metronome strike (writes a LEDGER row)
  engine/refresh_cone_one.py  — the mid-cycle displayed-cone refresh (writes none)
Both stamp the entry with the day the strike actually ran.

If you genuinely mean to replay the historical 28-Jul-2026 pass, pass {REPLAY_FLAG}."""


def _refuse_unless_replaying(argv) -> None:
    """Refuse to re-run the frozen replay tool. Raises; never warns."""
    if REPLAY_FLAG not in argv:
        raise SystemExit(_REFUSE)


if __name__ == '__main__':
    _refuse_unless_replaying(sys.argv)
    build(write='--write' in sys.argv)
