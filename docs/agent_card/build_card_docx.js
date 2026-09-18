const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, ImageRun,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  AlignmentType, PageOrientation, VerticalAlign,
} = require('docx');

const path = require('path');
const HERE = __dirname;   // docs/agent_card/ — inputs and output all live here

// ---------------------------------------------------------------- the page's own palette
// Lifted from the HTML card's light token set, so the two read as one document.
const INK = '141C26';      // --ink
const INK2 = '3D4855';     // --ink2
const MUTED = '697687';    // --muted
const LINE = 'D8DDE5';     // --line
const LINE2 = 'EBEEF3';    // --line2
const SUNK = 'E8EBF0';     // --sunk
const TEAL = '0E6B5E';     // --a
const TEAL_SOFT = 'E3F0ED';// --a-soft
const RUST = 'A4552F';     // --stop
const RUST_SOFT = 'F6E9E1';// --stop-soft

// Three roles, matching the page: a serif display face, a neutral body face, a mono utility
// face. Georgia and Consolas are the HTML's own declared fallbacks for Newsreader and
// IBM Plex Mono, so the substitution is the one the page already specifies.
const SERIF = 'Georgia', SANS = 'Calibri', MONO = 'Consolas';

const W = [1750, 4150, 3500, 5998];                 // column widths, DXA
const TABLE_W = W.reduce((a, b) => a + b, 0);       // 15398 = A4 landscape less 0.5in margins

const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const rule = (color, size = 4) => ({ style: BorderStyle.SINGLE, size, color });

const txt = (text, o = {}) => new TextRun({
  text,
  font: o.font || SANS,
  size: o.size || 18,
  bold: !!o.bold,
  italics: !!o.italics,
  color: o.color || INK,
  allCaps: !!o.caps,
  characterSpacing: o.spacing,
  shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
});

const P = (runs, o = {}) => new Paragraph({
  children: Array.isArray(runs) ? runs : [runs],
  spacing: { before: o.before || 0, after: o.after === undefined ? 60 : o.after, line: o.line || 250 },
  alignment: o.align,
  border: o.border,
  keepNext: o.keepNext,
  pageBreakBefore: o.pageBreakBefore,
});

// a section heading: serif, with the page's small grey gloss trailing it
const H2 = (text, gloss, o = {}) => P([
  txt(text, { font: SERIF, size: 28, bold: true }),
  ...(gloss ? [txt('     ' + gloss, { size: 17, color: MUTED })] : []),
], { before: o.before || 0, after: o.after === undefined ? 100 : o.after, keepNext: true, pageBreakBefore: o.pageBreakBefore });

// a pill, the way the page draws one
const badge = (text, kind) => txt(' ' + text + ' ', {
  size: 16, bold: true,
  color: kind === 'stop' ? RUST : TEAL,
  fill: kind === 'stop' ? RUST_SOFT : TEAL_SOFT,
});

// ---------------------------------------------------------------- the eight rows
const ROWS = [
  {
    task: 'Is the repo clean?',
    say: ['Run the gates before I commit', 'Is the repo clean?'],
    agent: 'testahil-gate-runner',
    rule: 'R-ENF-04 · mirrors CI',
    back: 'One table: gate · population examined · PASS / FAIL / UNRUNNABLE · the command’s own output.',
    mark: 'read-only, never fixes', kind: 'ro',
  },
  {
    task: 'Is a study deliverable?',
    say: ['Audit the PHDC study', 'Is the AMOC study deliverable?'],
    agent: 'testahil-qc-auditor',
    rule: 'R-ENF-02 · R-GAP-01 · depth bar',
    back: 'The filled QC table as QC_GATE_{date}.md, every row naming its artefact, plus one row about the answer against the price.',
    mark: 'writes nothing else', kind: 'ro',
  },
  {
    task: 'The answer looks wrong',
    say: ['How come ARCC’s fair value is half what it trades at?', 'Challenge the ARCC answer'],
    agent: 'testahil-answer-challenger',
    rule: 'R-GAP-01 · R-GAP-02',
    back: 'Every candidate defect priced as a number, ours hunted before the market’s — the terminal reinvestment identity, capex against the volume it buys.',
    mark: 'never edits the study', kind: 'ro',
  },
  {
    task: 'Sources before drivers',
    say: ['Run the sweep for ELEC', 'Start the information sweep on ELEC'],
    agent: 'testahil-sweep-researcher',
    rule: 'Step 2A · four rings',
    back: 'The study’s sweep.py and sweep_register.json, the company IR attempt logged either way.',
    mark: 'stops and asks if official statements cannot be obtained', kind: 'stop',
  },
  {
    task: 'Fresh prices, covered name',
    say: ['Roll forward COMI  (attach the export)', 'Recalibrate and forecast COMI'],
    agent: 'testahil-rollforward-operator',
    rule: 'trigger (b) · R-GRADE-01',
    back: 'Updated page, ledger, technical read, chart and per-name record; the lifecycle invariant asserted.',
    mark: 'never publishes · fair{} untouched', kind: 'ro',
  },
  {
    task: 'Campaign name',
    say: ['Run the fundamental walk-forward on AMOC', 'Next name in the campaign'],
    agent: 'testahil-walkforward-runner',
    rule: 'R-FCAL-01 · R-GAP-01 · R-MERGE-01',
    back: 'Training record, rebuilt study, lesson drafts — then the close: PR, merge on green, the gap reported only past 10%.',
    mark: 'stops before lessons_add.py for your scope ruling', kind: 'stop',
  },
  {
    task: 'A rule changes',
    say: ['Add this rule to the project instructions: …', 'Amend [R-CAL-02]: …'],
    agent: 'testahil-protocol-scribe',
    rule: 'R-DOC-01 · R-DOC-02',
    back: 'Both governing documents amended in one commit, the identifier assigned, both stamps bumped, the gates green.',
    mark: 'hands you the full digest text to paste', kind: 'stop',
  },
  {
    task: 'A critique arrives',
    say: ['Here is a critique of the ADNOCLS study — respond', 'Approved: implement rows CC-5, CW-20'],
    agent: 'testahil-critique-responder',
    rule: 'Critique_Response v2 · R-GAP-01',
    back: 'Every finding on its own row, priced before it is judged, receipts on every rejection.',
    mark: 'stops at the report; implements only on your approval', kind: 'stop',
  },
  {
    task: 'Composite-beta backlog',
    say: ['Re-issue the beta on SCEM', 'Clear the next name in the beta backlog'],
    agent: 'testahil-beta-reissuer',
    rule: 'R-BETA-04 · R-IDX-01 · R-GAP-01',
    back: 'Before and after: regressor, beta, R², tier, Ke, WACC, each lens, the weighted centre.',
    mark: 'stops if v2 sovereign inputs can’t be sourced live', kind: 'stop',
  },
];

// ---------------------------------------------------------------- masthead
const mast = new Table({
  columnWidths: [11198, 4200],
  width: { size: TABLE_W, type: WidthType.DXA },
  borders: { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none },
  rows: [new TableRow({
    children: [
      new TableCell({
        width: { size: 11198, type: WidthType.DXA },
        margins: { top: 0, bottom: 0, left: 0, right: 240 },
        verticalAlign: VerticalAlign.BOTTOM,
        children: [
          P(txt('Operating card · nine subagents', { font: MONO, size: 15, color: MUTED, caps: true, spacing: 16 }), { after: 70 }),
          P(txt('TESTAHIL Agent Card', { font: SERIF, size: 34, bold: true }), { after: 70 }),
          P(txt('Say the task in plain words; the main session routes it to the agent whose description matches, the agent works alone in a fresh context, and its report comes back to you. Name the agent only where a request reads two ways.', { color: INK2 }), { after: 0 }),
        ],
      }),
      new TableCell({
        width: { size: 4200, type: WidthType.DXA },
        margins: { top: 0, bottom: 0, left: 0, right: 0 },
        verticalAlign: VerticalAlign.BOTTOM,
        children: [
          P([txt('stored in ', { font: MONO, size: 16, color: MUTED }), txt('.claude/agents/', { font: MONO, size: 16, bold: true })], { align: AlignmentType.RIGHT, after: 30 }),
          P([txt('loaded from ', { font: MONO, size: 16, color: MUTED }), txt('main', { font: MONO, size: 16, bold: true }), txt(' at session start', { font: MONO, size: 16, color: MUTED })], { align: AlignmentType.RIGHT, after: 30 }),
          P([txt('inspect or edit with ', { font: MONO, size: 16, color: MUTED }), txt('/agents', { font: MONO, size: 16, bold: true })], { align: AlignmentType.RIGHT, after: 0 }),
        ],
      }),
    ],
  })],
});

// ---------------------------------------------------------------- the card
const cell = (children, width, o = {}) => new TableCell({
  children,
  width: { size: width, type: WidthType.DXA },
  shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } : undefined,
  margins: { top: o.pad || 20, bottom: o.pad || 20, left: 118, right: 118 },
  borders: { top: none, bottom: none, left: none, right: none },
});

const headRow = new TableRow({
  tableHeader: true,
  children: ['Task', 'Say this', 'Agent', 'What comes back · where it stops'].map((h, i) =>
    cell([P(txt(h, { font: MONO, size: 15, color: MUTED, caps: true, spacing: 14 }), { after: 0 })],
      W[i], { fill: SUNK, pad: 55 })),
});

const bodyRows = ROWS.map((r) => new TableRow({
  cantSplit: true,
  children: [
    cell([P(txt(r.task, { bold: true }), { after: 0 })], W[0]),
    cell(r.say.map((s, i) => P([
      txt('› ', { font: MONO, size: 15, color: MUTED }),
      txt(s, { font: MONO, size: 15 }),
    ], { after: i === r.say.length - 1 ? 0 : 40 })), W[1]),
    cell([
      P(txt(r.agent, { font: MONO, size: 15, bold: true, color: TEAL }), { after: 26 }),
      P(txt(r.rule, { font: MONO, size: 14, color: MUTED }), { after: 0 }),
    ], W[2]),
    cell([
      P(txt(r.back, { size: 16, color: INK2 }), { after: 34 }),
      P(badge(r.mark, r.kind), { after: 0 }),
    ], W[3]),
  ],
}));

const card = new Table({
  columnWidths: W,
  width: { size: TABLE_W, type: WidthType.DXA },
  borders: {
    top: rule(LINE), bottom: rule(LINE), left: rule(LINE), right: rule(LINE),
    insideHorizontal: rule(LINE2), insideVertical: none,
  },
  rows: [headRow, ...bodyRows],
});

// ---------------------------------------------------------------- the reading notes
// One line each: nine rows plus a three-column grid no longer share a landscape page,
// and a note that wraps is a note nobody reads.
const NOTES = [
  ['Name the agent when a request could read two ways.',
   ' Fresh OHLC for a ticker has the same input shape as a new study — say “roll forward”. “Check the study” splits two ways: repo gates is gate-runner, a delivered study is qc-auditor.'],
  ['Three routes.',
   ' Plain ask is the default and the description does the routing; name the agent when it could go two ways; /agents lists, inspects or edits a definition, and never runs one.'],
  ['What all nine share.',
   ' They read the live state rather than a remembered number, declare what they examined, report evidence rather than verdicts, and never publish on their own.'],
];
const notes = NOTES.map(([lead, body], i) => P([
  txt(lead, { size: 16, bold: true }),
  txt(body, { size: 16, color: INK2 }),
], {
  before: i === 0 ? 90 : 0,
  after: i === NOTES.length - 1 ? 0 : 30,
  border: i === 0 ? { top: rule(TEAL, 12) } : undefined,
}));

// ---------------------------------------------------------------- the figure
const img = fs.readFileSync(path.join(HERE, 'schematic.png'));
const figure = new Table({
  columnWidths: [TABLE_W],
  width: { size: TABLE_W, type: WidthType.DXA },
  borders: {
    top: rule(LINE), bottom: rule(LINE), left: rule(LINE), right: rule(LINE),
    insideHorizontal: none, insideVertical: none,
  },
  rows: [new TableRow({
    children: [new TableCell({
      width: { size: TABLE_W, type: WidthType.DXA },
      margins: { top: 110, bottom: 110, left: 140, right: 140 },
      children: [new Paragraph({
        children: [new ImageRun({ data: img, type: 'png', transformation: { width: 780, height: 516 } })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 0 },
      })],
    })],
  })],
});

// ---------------------------------------------------------------- document
const doc = new Document({
  creator: 'TESTAHIL',
  title: 'TESTAHIL Agent Card',
  description: 'What to say to activate each of the nine TESTAHIL subagents, and where each one sits.',
  styles: { default: { document: { run: { font: SANS, size: 18, color: INK } } } },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE },
        margin: { top: 720, right: 720, bottom: 620, left: 720 },
      },
    },
    children: [
      mast,
      P(txt(''), { after: 0, border: { bottom: rule(LINE) }, line: 120 }),

      H2('What to say', 'the words in the middle column are what the router matches on', { before: 80, after: 70 }),
      card,

      H2('How a prompt travels, and where each agent sits', null, { after: 130, pageBreakBefore: true }),
      figure,
      P(txt('Every prompt goes through the main session to one agent, which works alone and hands back evidence. The seven lanes show what each agent passes to the next step, and the three diamonds mark the points only you can pass: ruling on a lesson’s scope, approving a critique response, and pasting the digest into your own project files.', { size: 17, color: INK2 }), { before: 120, after: 0 }),
      ...notes,
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(path.join(HERE, 'TESTAHIL_Agent_Card.docx'), buf);
  console.log('written:', buf.length, 'bytes');
});
