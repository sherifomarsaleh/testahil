/* check_ta_chart_overlay.js — the test that would have caught the 29-Jul defect.
 *
 * injectLevels() recovers price->y by regressing over the chart's own muted axis
 * labels, then draws one line per S/R level. If the chart's y-axis does not span
 * the level ladder, the line is drawn OUTSIDE the 0..320 viewBox — silently.
 * Nothing throws, the page looks fine at a glance, and a level is simply gone.
 *
 * That is exactly what happened when the technical read became computed while
 * the chart stayed frozen at study time: COMI's axis topped out at 148 against a
 * resistance of 160, and a line landed at y = -21.
 *
 * Run:  node scripts/check_ta_chart_overlay.js [baseUrl]
 * Exits non-zero on any page where a level line escapes the plot box.
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'http://localhost:8765';
const ROOT = path.join(__dirname, '..');
const PAD = 2;                       // px tolerance at the plot edges

(async () => {
  const pages = fs.readdirSync(ROOT)
    .filter(f => f.endsWith('.html'))
    .filter(f => fs.readFileSync(path.join(ROOT, f), 'utf8').includes('id="ta-chart-svg"'));

  /* PORTABLE BROWSER RESOLUTION (25-Aug-2026). The path below is where this
   * project's dev sandbox pre-installs Chromium; a GitHub runner installing via
   * `npx playwright install chromium` puts it under ~/.cache/ms-playwright and
   * the hardcoded path does not exist there. Passing a non-existent
   * executablePath fails the launch outright, so the gate would have died in CI
   * on its first run — pass it only when it is actually there and let playwright
   * resolve its own browser otherwise. */
  const PINNED = '/opt/pw-browsers/chromium';
  const browser = await chromium.launch(
    fs.existsSync(PINNED) ? { executablePath: PINNED } : {});
  const ctx = await browser.newContext({ viewport: { width: 1180, height: 1000 } });

  /* HERMETIC BY CONSTRUCTION (25-Aug-2026). Every page links Google Fonts and
   * loads gtag. Neither has anything to do with what this gate measures — the y
   * position of SVG lines that injectLevels() computes from data already inline
   * on the page — but the browser still tries to fetch them, and on any runner
   * that cannot reach those hosts each navigation hangs instead of failing fast.
   * Measured here: >30 minutes without finishing 93 pages, against ~200ms PER
   * PAGE once external requests are aborted. A correctness gate that needs
   * fonts.googleapis.com to be reachable is flaky by construction, and a gate
   * slow enough to be skipped is a gate nobody runs. Only the origin under test
   * is allowed through; everything else is aborted, which is also a stronger
   * check, since a level line's position must not depend on a webfont loading. */
  await ctx.route('**/*', route => {
    const url = route.request().url();
    return url.startsWith(BASE) ? route.continue() : route.abort();
  });
  const bad = [];
  let checked = 0, noLevels = 0;

  for (const f of pages) {
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(`${BASE}/${f}`, { waitUntil: 'domcontentloaded' });
    await p.evaluate(() => document.querySelectorAll('details.rds').forEach(d => (d.open = true)));
    await p.waitForTimeout(250);

    const r = await p.evaluate(() => {
      const svg = document.getElementById('ta-chart-svg');
      if (!svg) return null;
      const vb = (svg.getAttribute('viewBox') || '').split(/\s+/).map(Number);
      const H = vb[3] || 320;
      // gridlines span the full plot width; level lines are the injected ones
      const lines = Array.from(svg.querySelectorAll('line')).map(l => ({
        y: parseFloat(l.getAttribute('y1')),
        x1: parseFloat(l.getAttribute('x1')),
        dash: l.getAttribute('stroke-dasharray') || '',
        stroke: l.getAttribute('stroke') || '',
      })).filter(o => isFinite(o.y));
      const labels = Array.from(svg.querySelectorAll('text'))
        .map(t => parseFloat((t.textContent || '').replace(/,/g, '')))
        .filter(v => isFinite(v));
      return { H, lines, axisMin: Math.min(...labels), axisMax: Math.max(...labels) };
    });

    if (!r) { await p.close(); continue; }
    checked++;
    // an injected level line is any line whose y falls outside the gridline set
    const outside = r.lines.filter(o => o.y < -PAD || o.y > r.H + PAD);
    if (errs.length || outside.length) {
      bad.push({ page: f, outside: outside.map(o => o.y.toFixed(1)), errs });
    }
    await p.close();
  }
  await browser.close();

  console.log(`checked ${checked} page(s) with a technical chart`);
  if (!bad.length) {
    console.log('PASS — every injected level line falls inside its plot box');
    process.exit(0);
  }
  console.log(`FAIL — ${bad.length} page(s):`);
  bad.forEach(b => console.log(`  ${b.page}  lines outside viewBox at y=${b.outside.join(',')}` +
    (b.errs.length ? `  console: ${b.errs.join(' | ')}` : '')));
  process.exit(1);
})();
