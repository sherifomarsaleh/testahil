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

  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await browser.newContext({ viewport: { width: 1180, height: 1000 } });
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
