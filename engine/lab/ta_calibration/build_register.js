const fs = require('fs');
const path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, AlignmentType, BorderStyle, ImageRun } = D;

const P = JSON.parse(fs.readFileSync(path.join(__dirname, 'register_payload.json'), 'utf8'));
const SCOPE = {
  ALL:   { tag: 'EVERY TICKER',     means: 'applies to every ticker' },
  CLASS: { tag: 'A CLASS OF TICKER',means: (c) => `applies to every ticker in that ${c}` },
  STOCK: { tag: 'ONE TICKER ONLY',  means: 'applies to a named ticker only' },
};
const METHOD = 'learned from a technical walk-forward test, 93-ticker replay, 31-Aug-2026';
const GREY = 'F2F2F2';

const t  = (text, o={}) => new TextRun({ text, ...o });
const p  = (runs, o={}) => new Paragraph({ children: Array.isArray(runs)?runs:[t(runs)], spacing:{after:120}, ...o });
const h1 = (s) => new Paragraph({ text: s, heading: HeadingLevel.HEADING_1, spacing:{before:320,after:160} });
const h2 = (s) => new Paragraph({ text: s, heading: HeadingLevel.HEADING_2, spacing:{before:240,after:120} });

function table(header, rows, widths) {
  const total = widths.reduce((a,b)=>a+b,0);
  const cell = (s, bold, shade) => new TableCell({
    width:{ size: 0, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: GREY } : undefined,
    children:[ new Paragraph({ children:[t(String(s), { bold: !!bold, size: 18 })], spacing:{after:0} }) ],
  });
  const mk = (cells, bold, shade) => new TableRow({
    children: cells.map((c,i)=> new TableCell({
      width:{ size: widths[i], type: WidthType.DXA },
      shading: shade ? { type: ShadingType.CLEAR, fill: GREY } : undefined,
      children:[ new Paragraph({ children:[t(String(c), { bold: !!bold, size: 18 })], spacing:{after:0} }) ],
    })),
  });
  return new Table({ columnWidths: widths, width:{ size: total, type: WidthType.DXA },
                     rows: [ mk(header, true, true), ...rows.map(r=>mk(r)) ] });
}

const FIGDIR = path.join(__dirname, 'figures');
// A figure may appear TWICE at most: once in the opening gallery, once beside
// the lesson that owns it — a summary section repeats its evidence on purpose.
// Beyond that, repetition is suppressed.
const shown = {};
function figure(name, caption) {
  if (!name) return;
  shown[name] = (shown[name] || 0) + 1;
  if (shown[name] > 2) return;
  const f = path.join(FIGDIR, name);
  if (!fs.existsSync(f)) return;
  kids.push(new Paragraph({ children: [ new ImageRun({
    type: 'png', data: fs.readFileSync(f),
    transformation: { width: 604, height: Math.round(604 * imgRatio(f)) } }) ],
    spacing: { before: 140, after: 40 } }));
  if (caption) kids.push(p([t(caption, { size: 16, italics: true, color: '777777' })],
                           { spacing: { after: 200 } }));
}
// read the PNG header for its true aspect ratio, so nothing is squashed
function imgRatio(f) {
  const b = fs.readFileSync(f);
  const w = b.readUInt32BE(16), h = b.readUInt32BE(20);
  return h / w;
}

const kids = [];
kids.push(p([t('TESTAHIL', { bold:true, size:22, color:'888888' })], { spacing:{after:40} }));
kids.push(new Paragraph({ children:[t('The Technical Lessons Register', { bold:true, size:44 })], spacing:{after:80} }));
kids.push(p([t('Everything fifteen years of price history has taught us about reading a chart — in plain language, with the charts to show it, and with real stocks demonstrating each lesson.', { size:22, italics:true })]));
kids.push(p([t(`Generated ${P.generated} from the register's own source. Not hand-written, and not hand-editable — every figure is resolved from the calibration results file at build time, so the register cannot drift from the measurement that produced it.`, { size:18, color:'666666' })]));
kids.push(p([t('Nothing in this register binds any study. It is a record, not a gate. No standing rule refers to it and no quality gate consults it, deliberately — a lesson earns its way into the method by being adopted, not by being written down.', { size:18, color:'666666' })]));

kids.push(h1('How to read this'));
kids.push(p('A lesson is only useful once you know how far it travels. Every entry carries one of three scopes. An EVERY TICKER lesson held across the whole book and no group of stocks disagreed. A CLASS lesson is one where groups of stocks genuinely answer differently — and that has to be proven, not assumed, because slicing any result into groups always produces different-looking numbers by luck alone. A ONE TICKER lesson was proven on that stock\u2019s own history, the hardest bar of the three.'));
kids.push(table(['Scope','Means','Who must read it'], [
  ['EVERY TICKER','holds pooled across the book, and no class differs beyond noise','everyone, on every name'],
  ['A CLASS OF TICKER','the classes genuinely disagree (Cochran Q)','anyone reading a name in that class'],
  ['ONE TICKER ONLY','proven on that name’s own history alone','anyone reading that name'],
], [1900, 4200, 3100]));
kids.push(p(''));
kids.push(p('Every lesson also records how it was learned, because the strength of the evidence differs enormously, and what would overturn it. A lesson with no falsifier is a habit, not a finding.'));

kids.push(h1('How the test works, in plain words'));
kids.push(p('Every finding in this document comes from one repeated exercise. Stand at some week in the past. Compute the page exactly as it would have been published that day, using only the prices up to that day. Write down what it claimed. Then watch the following week, two weeks and month, and score the claim against what actually happened. Move forward a week and do it again — every week of fifteen years, for 92 stocks. That is roughly 45,000 dated readings per horizon, and no reading ever peeks at its own future.'));
figure('14_schematic.png', 'The one picture behind everything here: a read frozen at an origin, a made-up comparison line, and the weeks after.');
kids.push(p('Two habits keep the scoring honest. First, a claim about a level is never judged on its own — it races an invented level a similar distance away, placed where the chart shows nothing, because "price stopped near our line" means little if price also stops near lines that mean nothing. Second, results are quoted as "so many in 100" against the market\u2019s own base rate, never against 50%, because stocks do not flip fair coins (see T-026).'));
kids.push(p('One number to hold onto: "+5 in 100" means that out of 100 comparable situations, the thing being tested came out ahead in five more of them than the benchmark did. Small edges are the honest currency of this subject — anyone offering +40 in 100 is selling something.'));

kids.push(h1('The four things worth knowing, in pictures'));
kids.push(p('If you read nothing else, read these four charts. The rest of the document is the evidence behind them.'));
figure('01_horizon_decay.png', 'Levels matter, and they matter most over days rather than months. This is why the whole calibration was re-run — the first pass scored a short-term read against three-month outcomes and reported the weakest number in this chart.');
figure('04_atr_ladder.png', 'The tape sentence is the best thing the read publishes. Four words, four clearly different amounts of movement in the month that follows.');
figure('09_trigger.png', 'The trigger sentence said clearing a level opens the next one. It does the opposite — and that follows from levels being real, because the far level holds too.');
figure('13_stability.png', 'Split the fifteen years in half and two of the three main claims survive. The trend claim does not.');

kids.push(h1('What is in here, and what is honestly missing'));
kids.push(h2('This tests the read, not the cone and not the study'));
kids.push(p(`Three different tests in this project are all called a walk-forward, and they test different machinery on different evidence. This register covers only the first: the technical read, re-run at every historical origin on a truncated library and graded on what the tape actually did. It covers ${P.coverage.names} names carrying enough history to be assessed, over ${P.coverage.obs.toLocaleString()} readings per horizon.`));
kids.push(table(['','What it tests','Names','Resolved observations'], P.evidence_rows, [2400, 4400, 1500, 2100]));
kids.push(p(''));
kids.push(p('Every sentence the read publishes has now been scored. The bull and bear trigger, the fresh golden-cross clause and volume were the three gaps in the first edition and all three are closed below — two of them by finding the published claim points the wrong way, which is why they were worth closing. What remains genuinely untested: intraday structure, which these libraries do not carry, and any level-drawing method other than the one the read uses.'));

kids.push(h1('The indicators this read is built from'));
kids.push(p('Everything below is computed from the same daily price history the probability cone runs on, through the same data-quality gate. Nothing is fitted and nothing is hand-drawn — every number is a fixed function of the price series, and every sentence on a page is chosen by one of these numbers.'));
kids.push(table(['Indicator', 'Setting', 'What it is'], P.indicators, [2500, 3100, 3600]));
kids.push(p(''));
kids.push(p('The settings are conventional ones, chosen before any of this was measured. They are NOT fitted to the data, which is why the calibration can test them honestly — but it also means several of them are simply inherited, and three lessons below (T-014, T-015, T-017) find that the read\u2019s own ranking and weighting of levels do not match what the levels actually do.'));

const bySc = (s) => P.lessons.filter(l => l.scope === s);
function lesson(l) {
  const sc = SCOPE[l.scope];
  const means = typeof sc.means === 'function' ? sc.means(l.cls) : sc.means;
  kids.push(new Paragraph({ children:[t(`${l.id}  ${l.title}`, { bold:true, size:24 })], spacing:{before:260, after:60} }));
  kids.push(p([t(`${sc.tag}   ${means}   ·   ${METHOD}   ·   STATUS: ${l.status}`, { size:16, color:'777777', allCaps:false })]));
  kids.push(p([t(l.body, { size:21 })]));
  kids.push(p([t('How we know.  ', { bold:true, size:21 }), t(l.know, { size:21 })]));
  kids.push(p([t('What would overturn it.  ', { bold:true, size:21 }), t(l.over, { size:21 })]));
  figure(l.fig, l.figcap || null);
  figure(l.fig2, l.figcap2 || null);
}

kids.push(h1('Lessons that bind on EVERY ticker'));
kids.push(p('Read these before reading any chart, of any company, in any market. Four of them say a sentence the read currently publishes is wrong — the two momentum words, the trigger and the cross — which is what a calibration is for.'));
bySc('ALL').forEach(lesson);

kids.push(h1('Lessons that bind on a CLASS of ticker'));
kids.push(p('Two candidate classes were tested: the market a ticker trades on, and its industry sector. They did not fare equally.'));
kids.push(h2('Market / exchange'));
bySc('CLASS').filter(l=>l.cls==='market').forEach(lesson);
kids.push(h2('Industry sector'));
bySc('CLASS').filter(l=>l.cls==='sector').forEach(lesson);

kids.push(h1('Lessons that bind on ONE ticker'));
kids.push(p('The hardest scope to earn: the stock\u2019s own history has to carry the proof by itself.'));
bySc('STOCK').forEach(lesson);

kids.push(h1('How a lesson gets added'));
kids.push(p('A lesson enters this register when a measurement produces it, never when someone believes it. It carries a scope that has been tested rather than assumed, evidence with the numbers inline, and a condition that would overturn it. It is regenerated from the results file on every calibration pass, so a lesson whose evidence has moved is rewritten rather than left standing.'));

const doc = new Document({
  styles: { default: { document: { run: { font: 'Calibri', size: 21 } } } },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 } } }, children: kids }],
});
Packer.toBuffer(doc).then(b => {
  const out = path.join(__dirname, 'Technical_Lessons_Register.docx');
  fs.writeFileSync(out, b);
  console.log('wrote', out, (b.length/1024).toFixed(0)+'KB', '|', P.lessons.length, 'lessons');
});
