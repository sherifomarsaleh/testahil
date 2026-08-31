const fs = require('fs');
const path = require('path');
const D = require('docx');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
        TableCell, WidthType, ShadingType, AlignmentType, BorderStyle } = D;

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

const kids = [];
kids.push(p([t('TESTAHIL', { bold:true, size:22, color:'888888' })], { spacing:{after:40} }));
kids.push(new Paragraph({ children:[t('The Technical Lessons Register', { bold:true, size:44 })], spacing:{after:80} }));
kids.push(p([t('Everything the price history has taught us about reading a chart, in plain language, and how far each lesson travels.', { size:22, italics:true })]));
kids.push(p([t(`Generated ${P.generated} from the register's own source. Not hand-written, and not hand-editable — every figure is resolved from the calibration results file at build time, so the register cannot drift from the measurement that produced it.`, { size:18, color:'666666' })]));
kids.push(p([t('Nothing in this register binds any study. It is a record, not a gate. No standing rule refers to it and no quality gate consults it, deliberately — a lesson earns its way into the method by being adopted, not by being written down.', { size:18, color:'666666' })]));

kids.push(h1('How to read this'));
kids.push(p('A lesson is useless until you know how far it carries. Every entry is tagged with one of three scopes, and the difference is not a matter of emphasis: applying a one-ticker lesson to another company is superstition, and applying an every-ticker lesson is mandatory. The middle rung is where most of the value sits and it is the one that has to be earned — a set of per-class numbers is not a class-level finding, because ten draws from one distribution also look different. Each candidate class is therefore tested for heterogeneity, and only reported as a class when the classes differ by more than their own standard errors explain.'));
kids.push(table(['Scope','Means','Who must read it'], [
  ['EVERY TICKER','holds pooled across the book, and no class differs beyond noise','everyone, on every name'],
  ['A CLASS OF TICKER','the classes genuinely disagree (Cochran Q)','anyone reading a name in that class'],
  ['ONE TICKER ONLY','proven on that name’s own history alone','anyone reading that name'],
], [1900, 4200, 3100]));
kids.push(p(''));
kids.push(p('Every lesson also records how it was learned, because the strength of the evidence differs enormously, and what would overturn it. A lesson with no falsifier is a habit, not a finding.'));

kids.push(h1('What is in here, and what is honestly missing'));
kids.push(h2('This tests the read, not the cone and not the study'));
kids.push(p(`Three different tests in this project are all called a walk-forward, and they test different machinery on different evidence. This register covers only the first: the technical read, re-run at every historical origin on a truncated library and graded on what the tape actually did. It covers ${P.coverage.names} names carrying enough history to be assessed, over ${P.coverage.obs.toLocaleString()} readings per horizon.`));
kids.push(table(['','What it tests','Names','Resolved observations'], P.evidence_rows, [2400, 4400, 1500, 2100]));
kids.push(p(''));
kids.push(p('Every sentence the read publishes has now been scored. The bull and bear trigger, the fresh golden-cross clause and volume were the three gaps in the first edition and all three are closed below — two of them by finding the published claim points the wrong way, which is why they were worth closing. What remains genuinely untested: intraday structure, which these libraries do not carry, and any level-drawing method other than the one the read uses.'));

const bySc = (s) => P.lessons.filter(l => l.scope === s);
function lesson(l) {
  const sc = SCOPE[l.scope];
  const means = typeof sc.means === 'function' ? sc.means(l.cls) : sc.means;
  kids.push(new Paragraph({ children:[t(`${l.id}  ${l.title}`, { bold:true, size:24 })], spacing:{before:260, after:60} }));
  kids.push(p([t(`${sc.tag}   ${means}   ·   ${METHOD}   ·   STATUS: ${l.status}`, { size:16, color:'777777', allCaps:false })]));
  kids.push(p([t(l.body, { size:21 })]));
  kids.push(p([t('How we know.  ', { bold:true, size:21 }), t(l.know, { size:21 })]));
  kids.push(p([t('What would overturn it.  ', { bold:true, size:21 }), t(l.over, { size:21 })]));
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
kids.push(p('No single-name lesson has been earned yet. What has been established is which claims can ever be stated per name on the evidence available, which is the entry below.'));
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
