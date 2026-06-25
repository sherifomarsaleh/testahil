#!/usr/bin/env node
/* =========================================================================
   generate_feed.js — regenerates feed.xml from assets/data.js (TICKERS).
   Single source of truth: every ticker present in TICKERS becomes a feed
   item. Add a study to data.js -> it appears in the feed automatically.
   No external dependencies (Node built-ins only).
   Usage: node scripts/generate_feed.js [dataPath] [outPath]
   ========================================================================= */
'use strict';
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const DATA_PATH = process.argv[2] || 'assets/data.js';
const OUT_PATH  = process.argv[3] || 'feed.xml';
const BASE = 'https://testahil.com';

// Arabic display names (prefilled for live + coming-soon tickers; English fallback)
const AR_NAMES = {
  PHDC: 'بالم هيلز', TMGH: 'طلعت مصطفى', EMFD: 'إعمار مصر', OCDI: 'سوديك', ORHD: 'أوراسكوم للتنمية',
  ORAS: 'أوراسكوم للإنشاء', COMI: 'البنك التجاري الدولي', CCAP: 'القلعة',
  FWRY: 'فوري', HELI: 'مصر الجديدة للإسكان والتعمير', BTFH: 'بلتون',
  ABUK: 'أبو قير للأسمدة', EFID: 'إيديتا', HRHO: 'المجموعة المالية هيرميس',
  MFPC: 'موبكو'
};

const MONS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const DAYS = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];

function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                  .replace(/"/g,'&quot;').replace(/'/g,'&apos;');
}
function rfc822FromYMD(y, m, d) {           // fixed 08:30 Cairo (+0300)
  const dt = new Date(Date.UTC(y, m - 1, d, 5, 30, 0)); // 05:30Z == 08:30 +0300
  return `${DAYS[dt.getUTCDay()]}, ${String(d).padStart(2,'0')} ${MONS[m-1]} ${y} 08:30:00 +0300`;
}
function nowRfc822() {
  const dt = new Date();
  return `${DAYS[dt.getUTCDay()]}, ${String(dt.getUTCDate()).padStart(2,'0')} ${MONS[dt.getUTCMonth()]} ${dt.getUTCFullYear()} `
       + `${String(dt.getUTCHours()).padStart(2,'0')}:${String(dt.getUTCMinutes()).padStart(2,'0')}:${String(dt.getUTCSeconds()).padStart(2,'0')} +0000`;
}
function fmt(n) { return (typeof n === 'number') ? n.toFixed(2) : String(n); }

// --- load data.js in a sandbox and capture TICKERS / SITE ---
function loadData(p) {
  const src = fs.readFileSync(p, 'utf8');
  const sandbox = {};
  vm.createContext(sandbox);
  vm.runInContext(
    src + '\n;this.TICKERS = (typeof TICKERS!=="undefined")?TICKERS:null;'
        + '\n;this.SITE = (typeof SITE!=="undefined")?SITE:null;',
    sandbox, { filename: 'data.js' }
  );
  if (!sandbox.TICKERS || typeof sandbox.TICKERS !== 'object') {
    throw new Error('TICKERS not found in ' + p);
  }
  return sandbox;
}

function parseStudyDate(t) {
  // prefer the DD-MM-YYYY date embedded in the study filename
  const study = t.files && t.files.study ? t.files.study : '';
  const m = study.match(/(\d{2})-(\d{2})-(\d{4})/);
  if (m) return { y: +m[3], mo: +m[2], d: +m[1] };
  return null;
}

function build() {
  const { TICKERS, SITE } = loadData(DATA_PATH);
  const today = new Date();
  const fallback = { y: today.getUTCFullYear(), mo: today.getUTCMonth() + 1, d: today.getUTCDate() };

  const items = Object.keys(TICKERS).map(code => {
    const t = TICKERS[code];
    const slug = code.toLowerCase();
    const arName = AR_NAMES[code] || t.name || code;
    const dt = parseStudyDate(t) || fallback;
    const link = `${BASE}/ar/${slug}.html`;
    const t60 = (t.dist && t.dist.t60) ? t.dist.t60 : null;
    let desc = 'نطاق القيمة العادلة وتوزيع احتمالي لسعر السهم خلال ٣ شهور — تحليل تعليمي مستقل.';
    if (t60 && typeof t.spot === 'number') {
      desc = `السعر ${fmt(t.spot)} · الوسيط (٣ شهور) ${fmt(t60.p50)} · النطاق ${fmt(t60.p5)}–${fmt(t60.p95)} جنيه — تحليل تعليمي، توزيع وليس توصية.`;
    }
    return {
      sortKey: dt.y * 10000 + dt.mo * 100 + dt.d,
      title: `${arName} (${code}): دراسة تقييم — هل يستحق السهم؟`,
      link, pubDate: rfc822FromYMD(dt.y, dt.mo, dt.d), description: desc
    };
  });

  // newest-first
  items.sort((a, b) => b.sortKey - a.sortKey);

  if (items.length === 0) throw new Error('No items generated — refusing to write an empty feed.');

  // lastBuildDate = newest item's date (stable: only changes when content changes)
  const buildDate = items[0].pubDate;

  const itemXml = items.map(it => `    <item>
      <title>${esc(it.title)}</title>
      <link>${esc(it.link)}</link>
      <guid isPermaLink="true">${esc(it.link)}</guid>
      <description>${esc(it.description)}</description>
      <pubDate>${it.pubDate}</pubDate>
    </item>`).join('\n\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Testahil · تستاهل — دراسات تقييم البورصة المصرية</title>
    <link>${BASE}/</link>
    <atom:link href="${BASE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>دراسات تقييم تعليمية مستقلة لأسهم البورصة المصرية — توزيعات احتمالية، وليست توصيات. Educational EGX valuation studies — distributions, not tips.</description>
    <language>ar</language>
    <lastBuildDate>${buildDate}</lastBuildDate>

${itemXml}

  </channel>
</rss>
`;
  fs.writeFileSync(OUT_PATH, xml, 'utf8');
  console.log(`Wrote ${OUT_PATH} with ${items.length} item(s): ${items.map(i=>i.title.match(/\(([A-Z]+)\)/)[1]).join(', ')}`);
}

build();
