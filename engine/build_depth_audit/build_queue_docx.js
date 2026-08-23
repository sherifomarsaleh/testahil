const fs = require('fs');
const path = require('path');
const d = require('docx');
const {Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow,
       TableCell, WidthType, ShadingType, BorderStyle, PageNumber, Footer, Header} = d;

const HERE = __dirname;
const Q = JSON.parse(fs.readFileSync(path.join(HERE, 'queue.json'), 'utf8'));
const ALL = Q.flatMap(w => w.batches.flatMap(b => b.items));
const N = ALL.length;
const COC = ALL.filter(i => i.needs === 'cost of capital').length;
const BOTH = N - COC;

const INK='141C26', MUT='697687', LINE='D8DDE5', SUNK='EEF1F5', TEAL='0E6B5E', CLAY='9A5A2B';
const W = {box:500, seq:600, tk:1400, nm:4526, nd:2000};
const TOTAL = Object.values(W).reduce((a,b)=>a+b,0);
const NOB = {top:{style:BorderStyle.NONE},bottom:{style:BorderStyle.NONE},
             left:{style:BorderStyle.NONE},right:{style:BorderStyle.NONE}};
const HAIR = {style:BorderStyle.SINGLE, size:2, color:LINE};

const cell = (children, width, opts={}) => new TableCell({
  width:{size:width, type:WidthType.DXA}, children,
  shading: opts.shade ? {type:ShadingType.CLEAR, fill:opts.shade, color:'auto'} : undefined,
  borders:{top:NOB.top, bottom:HAIR, left:NOB.left, right:NOB.right},
  margins:{top:60, bottom:60, left:90, right:90},
  verticalAlign: 'center',
});
const txt = (t, o={}) => new Paragraph({ alignment:o.align, spacing:{before:0, after:0},
  children:[new TextRun({ text:t, bold:o.bold, italics:o.italic, size:o.size||19,
    color:o.color||INK, font:o.mono?'Consolas':'Calibri', allCaps:o.caps,
    characterSpacing:o.caps?20:undefined })]});

const P = (t, o={}) => new Paragraph({
  spacing:{before:o.before??120, after:o.after??120}, alignment:o.align,
  border: o.rule ? {bottom:{style:BorderStyle.SINGLE,size:4,color:LINE,space:6}} : undefined,
  children:[new TextRun({text:t, bold:o.bold, italics:o.italic, size:o.size||21,
    color:o.color||INK, font:'Calibri', allCaps:o.caps, characterSpacing:o.caps?24:undefined})]});

function itemTable(items){
  const head = new TableRow({tableHeader:true, children:[
    cell([txt('', {size:16})], W.box, {shade:SUNK}),
    cell([txt('#', {size:15, caps:true, color:MUT, bold:true})], W.seq, {shade:SUNK}),
    cell([txt('Ticker', {size:15, caps:true, color:MUT, bold:true})], W.tk, {shade:SUNK}),
    cell([txt('Company', {size:15, caps:true, color:MUT, bold:true})], W.nm, {shade:SUNK}),
    cell([txt('What it needs', {size:15, caps:true, color:MUT, bold:true})], W.nd, {shade:SUNK}),
  ]});
  const rows = items.map(i => {
    const only = i.needs === 'cost of capital';
    return new TableRow({children:[
      cell([txt('☐', {size:22})], W.box),
      cell([txt(String(i.seq), {size:17, color:MUT, mono:true})], W.seq),
      cell([txt(i.tk, {size:18, bold:true, mono:true})], W.tk),
      cell([txt(i.nm, {size:18})], W.nm),
      cell([txt(only ? 'risk number' : 'risk number + rebuild',
                {size:16, color: only ? TEAL : CLAY, bold:true})], W.nd),
    ]});
  });
  return new Table({columnWidths:Object.values(W), width:{size:TOTAL,type:WidthType.DXA},
                    rows:[head, ...rows]});
}

const PRE = [
  ['☑','Dubai index — decided 23 Aug 2026.',
   'The eight Dubai-listed names stay on the Abu Dhabi index. Recorded in both protocol files, in the code note and in the index README, so a later session will not switch it back. Condition: every Dubai study must quote the interim disclosure, and none may be called conforming. Wave 3 is unblocked.'],
  ['☐','Remove the duplicate index file.',
   'ADXGENERAL.csv is byte-identical to FADGI.csv. Two studies point at the copy the resolver does not recognise, so their work cannot be verified even though the numbers are right. Delete it and repoint ADNOCDIST and ADNOCDRILL.'],
  ['☐','Decide the ARCC / SCEM fallback.',
   'Neither tracks the Egyptian market closely enough for the measurement to hold. The rules allow a comparison with similar Egyptian companies, or a neutral value. Whichever you choose becomes the precedent for every thinly-traded Egyptian name behind them — so decide once, now, rather than eight times inside Wave 2.'],
  ['☐','Make the checks run automatically.',
   'The checking code exists but each study chooses whether to call it: 8 of 21 study directories do, and no automated job runs any of them. A study passes by not checking itself — which is how the original problem spread while the rule against it was already written down.'],
];
const preTable = new Table({
  columnWidths:[500, 8526], width:{size:9026, type:WidthType.DXA},
  rows: PRE.map(([bx, h, body]) => new TableRow({children:[
    cell([txt(bx, {size:22, color: bx==='☑'?TEAL:INK})], 500),
    cell([ new Paragraph({spacing:{before:0,after:40}, children:[new TextRun({
             text:h, bold:true, size:19, color: bx==='☑'?TEAL:INK, font:'Calibri'})]}),
           new Paragraph({spacing:{before:0,after:0}, children:[new TextRun({
             text:body, size:18, color:INK, font:'Calibri'})]}) ], 8526),
  ]}))});

const body = [
  P('TESTAHIL · STANDING RESEARCH PROTOCOL · 23 AUGUST 2026',
    {caps:true, size:15, color:MUT, after:60}),
  new Paragraph({heading:HeadingLevel.TITLE, spacing:{before:0, after:100},
    children:[new TextRun({text:'The Rebuild Queue', font:'Georgia', size:52, color:INK, bold:true})]}),
  P(`The ${N} studies to redo, in working order.`, {size:24, color:MUT, italic:true, after:200, rule:true}),

  P(`Every covered stock except the ${90-N} already done properly, arranged so the cheapest work comes first and each country’s cost-of-capital homework is done once instead of once per company.`,
    {size:21}),
  P('Two terms, plainly.', {bold:true, size:21, before:200, after:60}),
  P('The risk number — how risky a company is, used to turn future profits into a value today. It is meant to be measured against the company’s own stock market index. In most of these studies it was chosen, not measured.', {size:19, after:60}),
  P('Ground-up rebuild — forecasting revenue as units sold × price each, and cost as cost per unit, rather than growing last year’s total by a percentage.', {size:19}),
  P(`Of the ${N}: ${COC} need only the risk number fixed, because they are already built from the ground up. The other ${BOTH} need both, and each of those is a full model rebuild rather than an edit.`,
    {size:21, before:160}),

  P('Before study number 1', {heading:true, size:28, bold:true, before:320, after:120, rule:true}),
  preTable,
];

Q.forEach(w => {
  body.push(new Paragraph({spacing:{before:400, after:40},
    children:[new TextRun({text:`${w.wave} · ${w.count} STUDIES`, caps:true, size:15,
      color:MUT, characterSpacing:24, font:'Calibri'})]}));
  body.push(new Paragraph({spacing:{before:0, after:80},
    children:[new TextRun({text:w.label, font:'Georgia', size:30, bold:true, color:INK})]}));
  body.push(P(w.why, {italic:true, size:19, color:MUT, after:160}));
  w.batches.forEach(b => {
    body.push(new Paragraph({spacing:{before:200, after:60},
      children:[new TextRun({text:`${b.exchange}  ·  ${b.cls}  (${b.items.length})`,
        bold:true, size:19, color:INK, font:'Calibri'})]}));
    body.push(itemTable(b.items));
  });
});

body.push(P('Order computed by sequence.py from the 23 August 2026 build-depth audit and the beta provenance of each study’s own committed records. Company types are set explicitly, not inferred from the valuation method.',
  {size:16, color:MUT, before:400, italic:true}));

const doc = new Document({
  creator:'TESTAHIL', title:'The Rebuild Queue',
  description:`The ${N} studies to redo, in working order`,
  styles:{default:{document:{run:{font:'Calibri', size:21, color:INK}}}},
  sections:[{
    properties:{page:{margin:{top:1080, bottom:1080, left:1440, right:1440}}},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.RIGHT,
      children:[new TextRun({text:'', size:16, color:MUT}),
                new TextRun({children:[PageNumber.CURRENT], size:16, color:MUT}),
                new TextRun({text:' / ', size:16, color:MUT}),
                new TextRun({children:[PageNumber.TOTAL_PAGES], size:16, color:MUT})]})]})},
    children: body,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(HERE, 'Rebuild_Queue_23-08-2026.docx');
  fs.writeFileSync(out, buf);
  console.log('wrote', out, buf.length, 'bytes |', N, 'studies');
});
