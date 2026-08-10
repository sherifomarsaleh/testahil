/* check_ticker_surfaces.js — is a published ticker actually VISIBLE everywhere it belongs?
 *
 * WHY THIS EXISTS
 * ---------------
 * publish_site.py's render check proved two things: the ticker's own page renders, and
 * the ticker appears in ledger.html. Everything else on the site was taken on trust. It
 * should not have been. Three consecutive publishes (SWDY, SCEM, EGCH) shipped green and
 * were silently ABSENT from the Ticker Picker, because that page reads a GENERATED file
 * -- assets/fv_overlay.js -- that nothing in the publish path regenerates. Nobody noticed
 * until a reader asked why a published name was not on the picker.
 *
 * A surface that reads a registry is only as current as the registry. This gate renders
 * each one in a real browser and asserts the ticker is in the DOM the reader sees, which
 * is the only claim that matters: markup can be perfectly correct and still render an
 * empty table, and a grep over the HTML source cannot tell the difference.
 *
 *   node scripts/check_ticker_surfaces.js EGCH
 *
 * Exit 1 on any surface that should carry the ticker and does not, with the reason.
 */
const { chromium } = require('playwright');
const path = require('path');

// Every surface that is supposed to list EVERY covered name. Pages deliberately absent
// from this list, with the reason: index.html (hero + a curated selection, not a
// register), compare.html and calculator.html (both start empty and are driven by user
// input), news.html (dated items), archive.html (a hand-kept record of past states, by
// construction not a live register), method.html / metals.html / other-markets.html
// (prose and non-equity surfaces).
// prose and non-equity surfaces), and egypt.html (a 14-line redirect stub to stocks.html,
// not a market register despite the name).
// Three of these never show their whole register at rest -- stocks.html paginates, and
// Trade and Portfolio start empty behind a search combobox. Reading the resting DOM would
// pass a name that happens to sort onto page one and fail every older name for no reason,
// which is a gate that reports noise. Each is driven the way a reader drives it: type the
// ticker, then read back what the page rendered.
const SURFACES = [
  { file: 'stocks.html',    what: 'coverage index',        search: '#topsearch' },
  { file: 'trade.html',     what: 'Trade name search',     search: '#t-sym' },
  { file: 'portfolio.html', what: 'Portfolio name search', search: '#p-sel' },
  { file: 'ledger.html',    what: 'forecast ledger' },
  // The Ticker Picker used to be EGX-only, because engine/fv_overlay.py could only scope
  // rows for EG and its output file could carry one market's calibration. It now runs
  // --all-markets: every market with a fitted profile, each row priced with its OWN
  // profile and cash hurdle, sectioned per market on the page. So it carries every
  // covered name and is checked for every covered name -- no markets restriction.
  { file: 'picker.html',    what: 'Ticker Picker' },
];

(async () => {
  const TK = (process.argv[2] || '').toUpperCase();
  if (!TK) { console.error('usage: check_ticker_surfaces.js TICKER'); process.exit(2); }
  const ROOT = process.argv[3] || path.resolve(__dirname, '..');
  const base = 'file://' + ROOT + '/';

  // The ticker's market, read from the same data.js the site reads.
  const fs = require('fs'), vm = require('vm'), ctx = {};
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'assets/data.js'), 'utf8')
                  + ';globalThis.__T=TICKERS;', ctx);
  const t = ctx.__T[TK];
  if (!t) { console.error(`${TK} is not in TICKERS — nothing to check`); process.exit(1); }

  const exch = String(t.code || '').split(':')[0];
  const targets = SURFACES.filter(s => !s.markets || s.markets.includes(exch));
  const skipped = SURFACES.filter(s => s.markets && !s.markets.includes(exch));

  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium',
                                    args: ['--no-sandbox'] });
  const p = await b.newPage();
  const bad = [];
  // Word boundary, not substring: "SCEM" must not be satisfied by some longer token, and
  // a three-letter ticker must not match inside a sentence. Case-INSENSITIVE, because
  // three names are spelled one way in TICKERS and another everywhere a reader sees
  // them (SAMSUNG/Samsung, KAKAO/Kakao, XPTUSD/Platinum): a case-sensitive test failed
  // those on pages that were rendering them perfectly well, which is a gate crying wolf.
  const re = new RegExp('\\b' + TK + '\\b', 'i');

  for (const s of targets) {
    const errs = [];
    const onErr = e => errs.push(String(e));
    p.on('pageerror', onErr);
    await p.goto(base + s.file);
    // These pages build their tables from data.js on DOMContentLoaded and some of them
    // simulate paths first; a short wait renders an empty table and reports a false miss.
    await p.waitForTimeout(2000);
    let body = '';
    try {
      if (s.search) {
        await p.click(s.search);
        await p.fill(s.search, TK);
        await p.waitForTimeout(600);
      }
      body = await p.innerText('body');
    } catch (e) { errs.push(String(e)); }
    p.off('pageerror', onErr);
    if (errs.length) bad.push(`${s.file} (${s.what}) — page errors: ${errs.slice(0, 2).join(' | ')}`);
    else if (!re.test(body)) bad.push(`${s.file} (${s.what}) — ${TK} is not in the rendered DOM`);
    else console.log(`  ok  ${s.file.padEnd(16)} ${TK} visible on the ${s.what}`);
  }
  await b.close();

  if (bad.length) {
    console.error(`\nFAIL: ${TK} is missing from ${bad.length} surface(s) that should carry it:`);
    for (const m of bad) console.error('   ! ' + m);
    console.error('\nA generated surface is stale until it is regenerated. The usual causes:');
    console.error('  picker.html   -> python3 engine/fv_overlay.py --all-markets --js assets/fv_overlay.js');
    console.error('  stocks/market -> python3 scripts/build_market_registry.py --write');
    console.error('  ledger.html   -> the LEDGER rows and MARKET_OF in the registry');
    process.exit(1);
  }
  for (const s of skipped)
    console.log(`  --  ${s.file.padEnd(16)} not applicable to ${exch} names`);
  console.log(`\nPASS: ${TK} renders on all ${targets.length} register surfaces`);
})();
