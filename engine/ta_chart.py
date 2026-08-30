"""ta_chart.py — regenerate the static price/MA chart on every ticker page.

WHY THIS EXISTS
---------------
Each ticker page carries a hand-produced `<svg id="ta-chart-svg">` drawn once at
study time and never regenerated. On 29-Jul-2026 the technical read became a
computed, per-price-update object (engine/technicals.py) while the chart under
it stayed frozen — so COMI ended up with a chart whose y-axis topped out at 148,
captioned "last 500 sessions to 29 Jun 2026", carrying a freshly computed
resistance ladder that reached 160. `injectLevels` duly drew a line at y=-21,
outside the 0..320 viewBox. Refreshing the levels onto a stale chart was worse
than leaving both stale.

THE SVG IS A CONTRACT, NOT DECORATION
-------------------------------------
Two runtime features read this SVG back:

  * `injectLevels(svgId, res, sup)` recovers the price->y mapping by LINEAR
    REGRESSION over the axis `<text>` elements whose fill matches `var(--muted`
    and whose content parses as a number. Change the label markup and the
    overlay silently mis-scales — it will not throw.
  * `renderZoomChart(...)` re-reads the same element to build the magnified
    recent-window panel.

So this module reproduces the existing structure exactly: viewBox 0 0 760 320,
plot box x 46..700 / y 14..294, five gridlines with muted right-aligned price
labels at x=40, three polylines in draw order brass (200-day MA) -> teal
(50-day MA) -> ink (price, on top), and seven muted quarter labels at y=312.

THE FIX ITSELF
--------------
The y-range is fitted to the union of the price window, both moving averages,
AND the published S/R ladder — so an overlay can never fall outside the plot.
That is the defect above, closed by construction rather than by eyeballing.

VERIFY BY IMPORT, NOT BY PARSE — per the standing rule.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import numpy as np                                          # noqa: E402
import pandas as pd                                         # noqa: E402

import technicals as TA                                     # noqa: E402
from apply_technicals import scope, top_level_blocks         # noqa: E402

# ---- the contract (do not change without changing app.js in the same commit)
VB_W, VB_H = 760, 320
X0, X1 = 46.0, 700.0
Y0, Y1 = 294.0, 14.0          # bottom, top of the plot box
N_GRID = 5
N_XLAB = 7
WINDOW = 500                  # sessions, matching the published caption
MUTED = 'var(--muted,#6b7c78)'
LINE = 'var(--line,#dce4e2)'
MONO = 'IBM Plex Mono,monospace'
SERIES = [('brass', 'var(--brass,#896F36)', '.9'),      # 200-day MA
          ('teal', 'var(--teal,#12796B)', '.9'),        # 50-day MA
          ('ink', 'var(--ink,#12211e)', '.95')]         # price, drawn last
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def nice_step(rng: float) -> float:
    """A 1/2/5-times-power-of-ten step, so labels read as round numbers."""
    if rng <= 0:
        return 1.0
    raw = rng / (N_GRID - 1)
    mag = 10.0 ** math.floor(math.log10(raw))
    n = raw / mag
    return (1 if n <= 1 else 2 if n <= 2 else 5 if n <= 5 else 10) * mag


def fmt_axis(v: float, ref: float) -> str:
    if ref >= 1000:
        return f'{v:,.0f}'.replace(',', '')
    if ref >= 10:
        return f'{v:.0f}' if abs(v - round(v)) < 1e-9 else f'{v:.1f}'
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def build_svg(market: str, series: str, levels: dict | None = None,
              window: int = WINDOW):
    """Return (svg_text, caption_text, meta) for one name."""
    df, _ = TA.load_clean(market, series)
    df = df.tail(window).reset_index(drop=True)
    dates = pd.to_datetime(df['Date'])
    close = df['Price'].to_numpy(dtype=float)
    n = len(close)
    if n < 60:
        raise ValueError(f'{market}/{series}: {n} sessions — too short to chart')

    ma50 = TA._sma_series(close, 50)
    ma200 = TA._sma_series(close, 200)

    # ---- y-range: price, both MAs, AND the S/R ladder, so no overlay escapes
    pool = [close.min(), close.max()]
    for m in (ma50, ma200):
        if m is not None and len(m):
            pool += [float(np.min(m)), float(np.max(m))]
    if levels:
        pool += [float(v) for v in list(levels.get('res', []))
                 + list(levels.get('sup', []))]
    lo_raw, hi_raw = min(pool), max(pool)
    pad = (hi_raw - lo_raw) * 0.04 or max(abs(hi_raw), 1) * 0.02
    lo_raw, hi_raw = lo_raw - pad, hi_raw + pad

    # The retired hand-drawn charts used a plain even split (COMI's read
    # 60/82/104/126/148 — step 22, not a round number), and that is the right
    # call here: snapping to 1/2/5-times-a-power-of-ten on a 500-session window
    # blows the axis out to 50..250 for a name trading at 142, leaving the data
    # squashed into a third of the plot. Fit the axis to the data, label it
    # honestly.
    lo, hi = lo_raw, hi_raw
    step = (hi - lo) / (N_GRID - 1)

    xpx = lambda i: X0 + (X1 - X0) * (i / max(n - 1, 1))   # noqa: E731
    ypx = lambda p: Y0 + (Y1 - Y0) * (p - lo) / (hi - lo)  # noqa: E731

    parts = []
    for g in range(N_GRID):
        v = lo + step * g
        y = ypx(v)
        parts.append(f'<line x1="{X0:.0f}" y1="{y:.1f}" x2="{X1:.1f}" '
                     f'y2="{y:.1f}" stroke="{LINE}" stroke-width="1" '
                     f'opacity=".6"/>')
        parts.append(f'<text x="40" y="{y + 3:.1f}" text-anchor="end" '
                     f'font-size="10" fill="{MUTED}" font-family="{MONO}">'
                     f'{fmt_axis(v, close[-1])}</text>')

    def poly(vals, colour, op):
        off = n - len(vals)
        pts = ' '.join(f'{xpx(off + k):.1f},{ypx(v):.1f}'
                       for k, v in enumerate(vals))
        return (f'<polyline points="{pts}" fill="none" stroke="{colour}" '
                f'stroke-width="1.6" opacity="{op}"/>')

    for (name, colour, op) in SERIES:
        vals = {'brass': ma200, 'teal': ma50, 'ink': close}[name]
        if vals is None or not len(vals):
            continue
        parts.append(poly(vals, colour, op))

    for k in range(N_XLAB):
        i = round(k * (n - 1) / (N_XLAB - 1))
        d = dates.iloc[i]
        parts.append(f'<text x="{xpx(i):.1f}" y="312" text-anchor="middle" '
                     f'font-size="10" fill="{MUTED}" font-family="{MONO}">'
                     f'Q{(d.month - 1) // 3 + 1} {d.year % 100:02d}</text>')

    svg = (f'<svg id="ta-chart-svg" viewBox="0 0 {VB_W} {VB_H}" width="100%" '
           f'role="img" aria-label="price with 50- and 200-day moving averages" '
           f'style="display:block">' + ''.join(parts) + '</svg>')
    last = dates.iloc[-1]
    caption = (f'Daily close &middot; last {n} sessions to '
               f'{last.day} {MONTHS[last.month - 1]} {last.year}')
    return svg, caption, {'sessions': n, 'lo': lo, 'hi': hi, 'step': step,
                          'last_date': last.date().isoformat(),
                          'close': float(close[-1])}


# ------------------------------------------------------------------- writing
# Both quote styles, because "2POINTZERO" is bracket-indexed rather than
# dot-accessed (a JS identifier cannot start with a digit) and the page happens
# to use SINGLE quotes. This is the third variant of the same one-key trap:
# apply_rollforward and apply_technicals both matched unquoted keys only.
PAGE_KEY = re.compile(r'(?:TICKERS|METALS)\.([A-Z0-9_]+)|'
                      r'''(?:TICKERS|METALS)\[\s*["']([A-Z0-9_]+)["']\s*\]''')


def page_for(key: str, files):
    """The html page whose inline script binds this ticker key."""
    for f in files:
        src = open(f, encoding='utf-8').read()
        for m in PAGE_KEY.finditer(src):
            if (m.group(1) or m.group(2)) == key:
                return f
    return None


def apply(write: bool = False, only=None):
    data = open(os.path.join(ROOT, 'assets', 'data.js'), encoding='utf-8').read()
    todo = scope(data, only)
    blocks = {**top_level_blocks(data, 'const TICKERS = {'),
              **top_level_blocks(data, 'const METALS = {')}
    files = [os.path.join(ROOT, f) for f in sorted(os.listdir(ROOT))
             if f.endswith('.html')]
    # THE CUTOVER MOVED THE CHART-CARRYING PAGES (30-Aug-2026). The new IA put a
    # data-driven template under {TICKER}/ at root and byte-preserved the old
    # site under legacy/, leaving the root slugs as redirect stubs. This scan
    # was flat-root-only, so it went from 93 chart pages to ZERO overnight and
    # reported "0 page(s) carry a chart / no page binds this key" while exiting
    # 0 — a stale technical read shipping under a green run, which is exactly
    # the staleness the 29-Jul rule was written to stop. Same fix and same
    # reason as scripts/check_page_integrity.py and check_band_vocabulary.py
    # took on the same day: legacy/ is SERVED CONTENT, so walk it.
    legacy = os.path.join(ROOT, 'legacy')
    if os.path.isdir(legacy):
        files += [os.path.join(legacy, f) for f in sorted(os.listdir(legacy))
                  if f.endswith('.html')]
    files = [f for f in files if 'id="ta-chart-svg"' in open(f, encoding='utf-8').read()]
    # [R-ENF-04] AN EMPTY POPULATION IS NOT A CLEAN ONE. Finding no chart page at
    # all means the layout moved again, not that there is no work: fail loudly
    # rather than skip every name and report success.
    if not files:
        raise SystemExit('ta_chart: NO page carries id="ta-chart-svg" under '
                         f'{ROOT} or {ROOT}/legacy — the page layout moved. '
                         'Refusing to report clean having examined nothing.')
    print(f'{len(todo)} name(s) in scope, {len(files)} page(s) carry a chart')

    done, skipped = [], []
    for key, _container, market, series in todo:
        page = page_for(key, files)
        if not page:
            skipped.append((key, 'no page binds this key'))
            continue
        a, b = blocks[key]
        blk = data[a:b]
        m = re.search(r'levels:\s*\{\s*res:\[([^\]]*)\],\s*sup:\[([^\]]*)\]',
                      blk)
        levels = None
        if m:
            levels = {'res': [float(x) for x in m.group(1).split(',') if x.strip()],
                      'sup': [float(x) for x in m.group(2).split(',') if x.strip()]}
        try:
            svg, cap, meta = build_svg(market, series, levels)
        except Exception as e:                                # noqa: BLE001
            skipped.append((key, f'{type(e).__name__}: {e}'))
            continue

        src = open(page, encoding='utf-8').read()
        new = re.sub(r'<svg id="ta-chart-svg".*?</svg>', lambda _: svg, src,
                     count=1, flags=re.S)
        # The caption sits in the <figcaption>, OUTSIDE the <svg> block above,
        # so it is a SEPARATE substitution -- and it used to require the HTML
        # entity "&middot;". 8 pages write that separator as a literal U+00B7,
        # so on those the pattern never matched and the caption froze while the
        # chart above it kept being regenerated: phdc.html labelled a 22-Jul
        # chart "last 500 sessions to 17 Jun 2026", 35 days out. Nothing caught
        # it -- check_ta_chart_overlay only tests that level lines land inside
        # the viewBox, and the page reported "chart block not replaced".
        # Accept either separator, and keep whichever the page already uses.
        _c = re.match(r'.*?last (\d+) sessions to (.+)$', cap)
        new, ncap = re.subn(
            r'(Daily close\s*(?:&middot;|\u00b7)\s*last )\d+( sessions to )[^<]*',
            lambda mm: mm.group(1) + _c.group(1) + mm.group(2) + _c.group(2),
            new, count=1)
        if not ncap and 'sessions to' in src:
            # a caption is present but the pattern could not reach it -- that is
            # a defect in this tool, not a page that happens to be current.
            skipped.append((key, 'CAPTION PATTERN DID NOT MATCH -- caption left '
                                 'stale next to a regenerated chart'))
            continue
        if new == src:
            skipped.append((key, 'already current (chart and caption both match)'))
            continue
        if write:
            open(page, 'w', encoding='utf-8').write(new)
        done.append({'key': key, 'page': os.path.basename(page), **meta,
                     'caption_updated': bool(ncap), 'levels': levels})

    print(f'regenerated: {len(done)}   skipped: {len(skipped)}')
    for k, why in skipped:
        print(f'  SKIP {k}: {why}')
    if not write:
        print('DRY RUN — nothing written')
    return done, skipped


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--only', nargs='*')
    args = ap.parse_args()
    d, _ = apply(write=args.write, only=args.only)
    for r in d[:8]:
        print(f"  {r['key']:12s} {r['page']:18s} {r['sessions']:4d} sessions "
              f"to {r['last_date']}  axis {r['lo']:g}..{r['hi']:g}")
