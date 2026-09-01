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
  // `keyedBy: 'coverage'` — this register renders assets/coverage.js, so the symbol a
  // reader searches and sees is that file's `tk`, which is NOT always the TICKERS key.
  // See THE REGISTER'S OWN SYMBOL below.
  { file: 'stocks.html',    what: 'coverage index',        search: '#topsearch',
    keyedBy: 'coverage' },
  { file: 'trade.html',     what: 'Trade name search',     search: '#t-sym' },
  { file: 'portfolio.html', what: 'Portfolio name search', search: '#p-sel' },
  { file: 'ledger.html',    what: 'forecast ledger',    marker: 'HAS_BACKTEST' },
  // [CHANGED 10-Aug-2026] The picker now carries EVERY covered name, each row computed
  // under its own market's committed fit and cash hurdle (fv_overlay.py resolves markets
  // per row from assets/markets.js). The old EGX-only carve-out let the first non-EG
  // publish ship an overlay that silently recomputed every EGX row under the AE config
  // -- this gate skipped the one page that would have shown it.
  { file: 'picker.html',    what: 'Ticker Picker',      marker: 'fv_overlay.js' },
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
  // Hermetic render: the registers are built by LOCAL scripts off file://, and
  // that DOM is all this gate asserts on. A hanging third-party font/analytics
  // fetch on a sandboxed runner stalls the default 'load' wait until the gate
  // times out, so external requests are blocked and navigation waits on the DOM.
  await p.route('**/*', r =>
    r.request().url().startsWith('file://') ? r.continue() : r.abort());
  const bad = [];
  // Word boundary, not substring: "SCEM" must not be satisfied by some longer token, and
  // a three-letter ticker must not match inside a sentence.
  // Case-INSENSITIVE: three names are spelled one way in TICKERS and another
  // everywhere a reader sees them (SAMSUNG/Samsung, KAKAO/Kakao), so a
  // case-sensitive test failed them on pages rendering them perfectly well.
  // [CHANGED 19-Aug-2026] Match the ticker OR the name a reader actually sees.
  // These surfaces are registers: most render the DISPLAY NAME, not the symbol. A
  // ticker-only test therefore FAILS any name whose display form is not the symbol as
  // one word -- RIYADHCABLE renders as "Riyadh Cables", so this gate reported it
  // missing from the Ticker Picker while all 97 rows, including its own, were on the
  // page. A gate that cries wolf is worse than no gate: the next real miss gets waved
  // through as "that one always fails". Case-insensitive as before (SAMSUNG/Samsung).
  const esc = x => String(x).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const alts = [TK, t.name, t.nameAr].filter(Boolean);
  let covRows = null;
  try {
    const cov = {}; vm.createContext(cov);
    vm.runInContext(fs.readFileSync(path.join(ROOT, 'assets/coverage.js'), 'utf8')
                    + ';globalThis.__S=SHORT;'
                    + ';globalThis.__EN=typeof COVERAGE_EN!=="undefined"?COVERAGE_EN:null;',
                    cov);
    if (cov.__S && cov.__S[TK]) alts.push(cov.__S[TK]);
    covRows = cov.__EN;
  } catch (e) { /* SHORT is a convenience, not a requirement */ }
  const re = new RegExp('\\b' + esc(TK) + '\\b|' +
                        alts.slice(1).map(a => esc(a)).join('|'), 'i');

  /* THE REGISTER'S OWN SYMBOL IS NOT ALWAYS THE SITE KEY (01-Sep-2026).
   *
   * This gate typed the TICKERS key into every register's search box and then looked
   * for it in the DOM. That is an assumption about the DATA, not a fact about it, and
   * it held for 87 of the 90 covered names only because their site key and their
   * published symbol happen to be the same string. The three KRX names are keyed by
   * their NUMERIC EXCHANGE TICKER in assets/coverage.js — LGES is listed as 373220,
   * SAMSUNG as 005930, KAKAO as 035720 — which is how a Korean symbol is written
   * everywhere a reader looks. So typing "LGES" filtered the coverage index to nothing
   * and the gate reported the name missing from a page that carries it correctly. Same
   * species as the RIYADHCABLE/"Riyadh Cables" miss the display-name alternative fixed
   * above, one field further out: the identity a register uses is the register's to
   * declare, not this script's to assume.
   *
   * So resolve it from the register's OWN authority. Match the coverage row on `code`
   * (KRX:373220) — carried by both files, unique per exchange, and never a display
   * string — then search and assert on the symbol and name that row publishes.
   *
   * WHERE THE TWO AGREE THIS IS A NO-OP BY CONSTRUCTION: `covAlias` is null unless the
   * coverage symbol DIFFERS from the site key, and every equity outside KRX then takes
   * the identical typed term and the identical regex it took before. */
  const codeOf = x => String(x || '').trim().toUpperCase();
  const covRow = (covRows || []).find(r => codeOf(r.code) === codeOf(t.code)) || null;
  const covAlias = covRow && String(covRow.tk).toUpperCase() !== TK ? covRow : null;
  const covRe = covAlias
    ? new RegExp('\\b' + esc(covAlias.tk) + '\\b|' + esc(covAlias.name), 'i')
    : null;

  /* THE CUTOVER MOVED THE REGISTER SURFACES (30-Aug-2026). All five of these are
   * redirect stubs at root now; the pages that actually render the registers are
   * the byte-preserved copies under legacy/, which are still served. A file://
   * render of a stub runs its location.replace() against a file URL and lands
   * nowhere, so every surface reported "not in the rendered DOM" or timed out on
   * a selector that only exists on the real page -- five confident failures about
   * a ticker that was present on all five. Resolve each surface to the copy a
   * reader is served, root first, exactly as check_data_freshness.py resolves
   * HAS_BACKTEST and publish_site.py resolves the ticker page. */
  const servedPage = (file, marker) => {
    const rootP = path.join(ROOT, file);
    if (fs.existsSync(rootP) && fs.readFileSync(rootP, 'utf8').includes(marker)) return file;
    const legP = path.join(ROOT, 'legacy', file);
    if (fs.existsSync(legP) && fs.readFileSync(legP, 'utf8').includes(marker)) return 'legacy/' + file;
    // [R-ENF-04] Neither copy is the real page: that is a finding, not a default.
    return null;
  };

  for (const s of targets) {
    const errs = [];
    const onErr = e => errs.push(String(e));
    // Each surface is identified by something only the REAL page carries: its own
    // search box where it has one, else the registry it renders from.
    // A CSS selector is not a substring of the markup: the page carries id="t-sym",
    // never "#t-sym". Matching the raw selector found nothing on either copy and
    // reported "the page layout moved" about a page sitting right there.
    const marker = s.marker || (s.search ? `id="${s.search.slice(1)}"` : 'data.js');
    const served = servedPage(s.file, marker);
    if (!served) {
      bad.push(`${s.file} (${s.what}) — no served copy found at root or legacy/ carrying ` +
               `${marker}; the page layout moved`);
      continue;
    }
    p.on('pageerror', onErr);
    await p.goto(base + served);
    // These pages build their tables from data.js on DOMContentLoaded and some of them
    // simulate paths first; a short wait renders an empty table and reports a false miss.
    await p.waitForTimeout(2000);
    // The identity THIS register publishes for the name — the site key unless the
    // register declares another one (see THE REGISTER'S OWN SYMBOL above).
    const alias = (s.keyedBy === 'coverage' && covAlias) ? covAlias : null;
    const term  = alias ? String(alias.tk) : TK;
    const rx    = alias ? covRe : re;
    let body = '';
    try {
      if (s.search) {
        await p.click(s.search);
        await p.fill(s.search, term);
        await p.waitForTimeout(600);
      }
      body = await p.innerText('body');
    } catch (e) { errs.push(String(e)); }
    p.off('pageerror', onErr);
    const as = alias ? ` (as ${term})` : '';
    if (errs.length) bad.push(`${served} (${s.what}) — page errors: ${errs.slice(0, 2).join(' | ')}`);
    else if (!rx.test(body)) bad.push(`${served} (${s.what}) — ${TK}${as} is not in the rendered DOM`);
    else console.log(`  ok  ${served.padEnd(22)} ${TK} visible on the ${s.what}${as}`);
  }
  await b.close();

  if (bad.length) {
    console.error(`\nFAIL: ${TK} is missing from ${bad.length} surface(s) that should carry it:`);
    for (const m of bad) console.error('   ! ' + m);
    console.error('\nA generated surface is stale until it is regenerated. The usual causes:');
    console.error('  picker.html   -> python3 engine/fv_overlay.py --js assets/fv_overlay.js');
    console.error('  stocks/market -> python3 scripts/build_market_registry.py --write');
    console.error('  ledger.html   -> the LEDGER rows and MARKET_OF in the registry');
    process.exit(1);
  }
  for (const s of skipped)
    console.log(`  --  ${s.file.padEnd(16)} not applicable to ${exch} names`);
  console.log(`\nPASS: ${TK} renders on all ${targets.length} register surfaces`);
})();
