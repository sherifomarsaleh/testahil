#!/usr/bin/env node
/* qc_charts.js — QC gate for every cohort chart on ledger.html.
 *
 * Run before any publish that touches assets/data.js, ledger.html, or
 * engine/raw_ohlc/. Exits non-zero on a FAIL.
 *
 *   node qc_charts.js
 *
 * WHY THIS EXISTS. The "predicted vs actual" chart is supposed to draw the
 * COMPLETE realized daily close path from anchor to grade date inside the
 * published cone — never just the two endpoints (standing instruction,
 * 28-Jul-2026). Three separate ways that silently failed, all found live:
 *
 *   1. A covered name had no COHORT_OHLC entry, so the chart fell back to
 *      endpoints only. COMI, Kakao and LGES all shipped this way.
 *   2. The chart's CSV parser only extracted quoted ("...") fields. All 11
 *      Saudi exports are UNQUOTED, so the parser returned zero rows and
 *      drawActualLine bailed on `if(!series.length) return` — every Tadawul
 *      chart drew nothing at all, with no error anywhere.
 *   3. A cohort's published anchor_price disagreed with the actual close on
 *      its anchor date, so the cone apex and the start of the price path sat
 *      at different heights and the chart looked broken. (It was not broken —
 *      it was correctly reporting a data defect.)
 *
 * Every one of these is invisible from the rendered page unless you already
 * know to look. Hence a gate.
 */
const fs = require('fs');

let FAIL = 0, WARN = 0;
const fail = m => { console.log('  FAIL  ' + m); FAIL++; };
const warn = m => { console.log('  warn  ' + m); WARN++; };

(0, eval)(fs.readFileSync('assets/data.js', 'utf8') + ';globalThis.__L=LEDGER;globalThis.__T=TICKERS;');
const L = globalThis.__L;
const html = fs.readFileSync('ledger.html', 'utf8');

const PATH_BLOCK = /const OHLC_BASE[\s\S]*?OHLC_BASE \+ v\]\)\);/.exec(html);
if (!PATH_BLOCK) { console.log('FAIL: could not find the COHORT_OHLC block in ledger.html'); process.exit(1); }
const COHORT_OHLC_PATH = new Function(PATH_BLOCK[0] + '; return COHORT_OHLC_PATH;')();

const ROW_BLOCK = /const splitRow = l => \{[\s\S]*?\n  \};/.exec(html);
if (!ROW_BLOCK) { console.log('FAIL: could not find splitRow in ledger.html'); process.exit(1); }
const splitRow = new Function('return ' + ROW_BLOCK[0].replace('const splitRow = ', '').replace(/;$/, ''))();

const toISO = d => { const m = /(\d{1,2})\/(\d{1,2})\/(\d{4})/.exec(d);
  return m ? `${m[3]}-${m[1].padStart(2, '0')}-${m[2].padStart(2, '0')}` : null; };

const CCY_OF_MARKET = { EG:'EGP', AE:'AED', SA:'SAR', KR:'KRW', IN:'INR', QA:'QAR',
                        US:'USD', XAU:'USD', XPT:'USD', GB:'GBP', BR:'BRL' };

const cache = {};
function series(inst) {
  if (inst in cache) return cache[inst];
  const rel = COHORT_OHLC_PATH[inst];
  if (!rel) return cache[inst] = null;
  const p = 'engine/raw_ohlc/' + rel;
  if (!fs.existsSync(p)) return cache[inst] = undefined;
  const map = {};
  fs.readFileSync(p, 'utf8').split(/\r?\n/).slice(1).map(splitRow)
    .filter(c => c[0] && c[1]).forEach(c => {
      const iso = toISO(c[0]); const px = parseFloat(String(c[1]).replace(/,/g, ''));
      if (iso && isFinite(px)) map[iso] = px;
    });
  return cache[inst] = map;
}

const instruments = [...new Set(L.map(r => r.instrument))].sort();

console.log('\n[1] every ledger instrument has a COHORT_OHLC entry');
instruments.forEach(i => { if (!COHORT_OHLC_PATH[i]) fail(`${i}: no COHORT_OHLC entry -> its chart draws endpoints only`); });

console.log('\n[2] every mapped file exists and parses to a non-empty series');
instruments.forEach(i => {
  const s = series(i);
  if (s === undefined) fail(`${i}: mapped file engine/raw_ohlc/${COHORT_OHLC_PATH[i]} does not exist`);
  else if (s && Object.keys(s).length === 0) fail(`${i}: ${COHORT_OHLC_PATH[i]} parsed to ZERO rows -> chart silently blank`);
});

console.log('\n[3] mapped market directory agrees with the ledger currency (catches ADIB/EGX vs ADIBUAE/ADX)');
instruments.forEach(i => {
  const rel = COHORT_OHLC_PATH[i]; if (!rel) return;
  const mkt = rel.split('/')[0];
  const row = L.find(r => r.instrument === i && r.ccy);
  if (!row) return;
  if (CCY_OF_MARKET[mkt] && CCY_OF_MARKET[mkt] !== row.ccy)
    fail(`${i}: mapped to ${rel} (${mkt} = ${CCY_OF_MARKET[mkt]}) but its ledger rows are ${row.ccy}`);
});

console.log('\n[4] each cohort anchor is a real trading session in its own library');
const seen = new Set();
L.forEach(r => {
  const k = r.instrument + '|' + r.anchor_date;
  if (seen.has(k) || !r.anchor_date) return; seen.add(k);
  const s = series(r.instrument); if (!s || !Object.keys(s).length) return;
  if (s[r.anchor_date] === undefined)
    fail(`${r.instrument} anchored ${r.anchor_date}, which is not a trading session in ${COHORT_OHLC_PATH[r.instrument]}`);
});

console.log('\n[5] published anchor_price agrees with the close on that date (cone apex vs start of path)');
const seen2 = new Set();
L.forEach(r => {
  const k = r.instrument + '|' + r.anchor_date;
  if (seen2.has(k) || !r.anchor_price || !r.anchor_date) return; seen2.add(k);
  const s = series(r.instrument); if (!s) return;
  const lib = s[r.anchor_date]; if (lib === undefined) return;
  const rel = lib / r.anchor_price - 1;
  if (Math.abs(rel) > 0.01)
    fail(`${r.instrument} ${r.anchor_date}: published anchor ${r.anchor_price} vs tape ${lib} (${(rel*100).toFixed(2)}%) — cone apex will not meet the price path`);
  else if (Math.abs(rel) > 0.001)
    warn(`${r.instrument} ${r.anchor_date}: published anchor ${r.anchor_price} vs tape ${lib} (${(rel*100).toFixed(2)}%)`);
});

console.log('\n[6] every graded cohort has a full path available, not just endpoints');
L.filter(r => r.realized_close != null && r.anchor_date && r.grade_date).forEach(r => {
  const s = series(r.instrument); if (!s || !Object.keys(s).length) return;
  const n = Object.keys(s).filter(d => d >= r.anchor_date && d <= r.grade_date).length;
  if (n < 3) fail(`${r.instrument} ${r.horizon_label} ${r.anchor_date}->${r.grade_date}: only ${n} session(s) in window — chart would be endpoints only`);
});

console.log(`\n${'='.repeat(64)}`);
console.log(`RESULT: ${FAIL} fail, ${WARN} warn`);
if (FAIL) { console.log('QC GATE FAILED — do not publish until these are resolved or explicitly accepted.'); process.exit(1); }
console.log('QC GATE PASSED.');
