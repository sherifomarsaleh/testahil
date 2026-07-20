#!/usr/bin/env node
/* =========================================================================
   generate_seo.js — keeps the site's SEO surfaces in sync from source data,
   so a new study needs no hand-editing of the sitemap or homepage links.

   On every run it regenerates:
     1) sitemap.xml           — from assets/data.js (TICKERS + METALS) plus a
                                static allowlist of hub/utility pages. Every
                                live study lands in the sitemap automatically
                                (English + Arabic when the /ar/ file exists);
                                <lastmod> = last git-commit date per file.
     2) homepage Studies strip — the footer list in index.html (and ar/index.html
                                if it carries the markers) is rebuilt from
                                assets/coverage.js (SHORT labels), newest first,
                                capped, between <!--STUDIES:START/END--> markers.

   Idempotent (running twice changes nothing). No external deps (Node built-ins).
   Usage: node scripts/generate_seo.js
   ========================================================================= */
'use strict';
const fs = require('fs');
const vm = require('vm');
const { execSync } = require('child_process');

const BASE = 'https://testahil.com';
const DATA_PATH = 'assets/data.js';
const COV_PATH  = 'assets/coverage.js';
const SITEMAP_OUT = 'sitemap.xml';
const FOOTER_MAX = 10;            // most-recent studies shown in the homepage footer strip
const INCLUDE_AR = false;         // Arabic pages are hidden (redirect to English); flip to true to restore

const TODAY = new Date().toISOString().slice(0, 10);
const MONS = { Jan:1, Feb:2, Mar:3, Apr:4, May:5, Jun:6, Jul:7, Aug:8, Sep:9, Oct:10, Nov:11, Dec:12 };

// ---- static hub / utility pages: [file, priority, changefreq] ------------
const STATIC = [
  ['',                '1.0', 'weekly'],
  ['stocks.html',     '0.9', 'weekly'],
  ['metals.html',     '0.9', 'weekly'],
  ['ledger.html',     '0.9', 'weekly'],
  ['method.html',     '0.6', 'monthly'],
  ['compare.html',    '0.8', 'weekly'],
  ['calculator.html', '0.6', 'monthly'],
  ['archive.html',    '0.5', 'monthly'],
  ['ar/',             '0.9', 'weekly'],
  ['ar/stocks.html',  '0.7', 'monthly'],
  ['ar/metals.html',  '0.7', 'monthly'],
  ['ar/method.html',  '0.7', 'monthly'],
];

function loadGlobals(path, names) {
  const src = fs.readFileSync(path, 'utf8');
  const sb = {};
  vm.createContext(sb);
  vm.runInContext(
    src + '\n' + names.map(n => `this.${n}=(typeof ${n}!=="undefined")?${n}:null;`).join('\n'),
    sb, { filename: path }
  );
  return sb;
}

function esc(s) {
  return String(s).replace(/&(?![a-zA-Z#0-9]+;)/g, '&amp;'); // leave existing entities intact
}

function fileFor(rel) {
  if (rel === '')    return 'index.html';
  if (rel === 'ar/') return 'ar/index.html';
  return rel;
}

function gitLastMod(file, fallback) {
  try {
    const out = execSync(`git log -1 --format=%cs -- "${file}"`, { encoding: 'utf8' }).trim();
    if (/^\d{4}-\d{2}-\d{2}$/.test(out)) return out;
  } catch (e) { /* no git history */ }
  return fallback;
}

// ---------------------------------------------------------------- sitemap
function buildSitemap() {
  const { TICKERS, METALS, SITE } = loadGlobals(DATA_PATH, ['TICKERS', 'METALS', 'SITE']);
  if (!TICKERS || typeof TICKERS !== 'object') throw new Error('TICKERS not found in ' + DATA_PATH);
  const fallbackDate = (SITE && SITE.updated) ? SITE.updated : TODAY;

  const rows = [];
  const seen = new Set();
  function add(rel, priority, changefreq) {
    if (!INCLUDE_AR && String(rel).startsWith('ar/')) return;   // Arabic hidden
    const file = fileFor(rel);
    if (!fs.existsSync(file)) return;   // never emit a URL with no page
    if (seen.has(rel)) return;
    seen.add(rel);
    rows.push({
      loc: BASE + '/' + rel,
      lastmod: gitLastMod(file, fallbackDate),
      changefreq, priority,
    });
  }

  STATIC.forEach(([rel, pr, cf]) => add(rel, pr, cf));

  Object.keys(TICKERS).forEach(code => {
    const slug = String(TICKERS[code].slug || code).toLowerCase();
    add(`${slug}.html`,    '0.9', 'weekly');
    add(`ar/${slug}.html`, '0.8', 'weekly');
  });

  const M = (METALS && typeof METALS === 'object') ? METALS : {};
  Object.keys(M).forEach(code => {
    const slug = String(M[code].slug || code).toLowerCase();
    add(`${slug}.html`,    '0.9', 'weekly');
    add(`ar/${slug}.html`, '0.8', 'weekly');
  });

  if (rows.length === 0) throw new Error('No URLs generated — refusing to write an empty sitemap.');

  const body = rows.map(r =>
    `  <url><loc>${r.loc}</loc><lastmod>${r.lastmod}</lastmod>` +
    `<changefreq>${r.changefreq}</changefreq><priority>${r.priority}</priority></url>`
  ).join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;

  return writeIfChanged(SITEMAP_OUT, xml, `sitemap.xml (${rows.length} URLs)`);
}

// -------------------------------------------------------- homepage footer
// English dates ("11 Jun 2026") parse cleanly; Arabic coverage rows carry the
// same tickers in the same order, so we key the sort off the English dates for
// both languages (Arabic month names would otherwise need their own map).
function dateKeyMap() {
  const { COVERAGE_EN } = loadGlobals(COV_PATH, ['COVERAGE_EN']);
  const parse = s => {
    const m = String(s || '').match(/(\d{1,2})\s+([A-Za-z]{3})\w*\s+(\d{4})/);
    return m ? (Number(m[3]) * 10000 + (MONS[m[2]] || 0) * 100 + Number(m[1])) : 0;
  };
  const map = {};
  (COVERAGE_EN || []).forEach(d => { map[d.tk] = parse(d.date); });
  return map;
}

function stripFrom(cov, labelFn, keyMap) {
  return (cov || [])
    .map(d => ({ url: d.url, label: labelFn(d), key: keyMap[d.tk] || 0 }))
    .sort((a, b) => b.key - a.key)
    .slice(0, FOOTER_MAX)
    .map(d => `<a href="${d.url}">${esc(d.label)}</a>`)
    .join(' &middot; ');
}

function updateFooter(path) {
  if (!fs.existsSync(path)) return null;
  const s = fs.readFileSync(path, 'utf8');
  const START = '<!--STUDIES:START-->', END = '<!--STUDIES:END-->';
  const i = s.indexOf(START), j = s.indexOf(END);
  if (i === -1 || j === -1 || j < i) return null;   // no markers -> skip this file
  const { COVERAGE_EN, COVERAGE_AR, SHORT } = loadGlobals(COV_PATH, ['COVERAGE_EN', 'COVERAGE_AR', 'SHORT']);
  const keyMap = dateKeyMap();
  const isAr = path.startsWith('ar/');
  const strip = isAr
    ? stripFrom(COVERAGE_AR, d => d.name, keyMap)              // Arabic labels are already short
    : stripFrom(COVERAGE_EN, d => (SHORT || {})[d.tk] || d.name, keyMap);
  const next = s.slice(0, i + START.length) + strip + s.slice(j);
  return writeIfChanged(path, next, `footer studies strip in ${path}`);
}

// -------------------------------------------------------------- utilities
function writeIfChanged(path, content, label) {
  const prev = fs.existsSync(path) ? fs.readFileSync(path, 'utf8') : null;
  if (prev === content) { console.log(`unchanged: ${label}`); return false; }
  fs.writeFileSync(path, content, 'utf8');
  console.log(`wrote: ${label}`);
  return true;
}

function main() {
  let changed = false;
  changed = buildSitemap() || changed;
  changed = updateFooter('index.html') || changed;
  if (INCLUDE_AR) changed = updateFooter('ar/index.html') || changed;   // no-op unless it carries markers
  console.log(changed ? 'SEO surfaces updated.' : 'SEO surfaces already current.');
}

main();
