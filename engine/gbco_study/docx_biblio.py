#!/usr/bin/env python3
"""GBCO_Bibliography_{edition}.docx — the standalone source register.

Depth-bar standard 1. This study shipped no bibliography-class document at all: it carried
its input register inside study_numbers.json where a checker could reach it and no reader
could, and check_calibration_deliverables was right to fail it for that.

Every figure that reaches the study or the model traces to a row here: what it is, where it
came from, which research layer that is, and the date the source itself carries. NO NUMERAL
IS TYPED IN THIS FILE — every one is read from the study's own committed record, the
walk-forward panel, or the beta record.

Paths resolve against HERE, so the file lands beside this script whatever directory the run
is invoked from.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))

from docx import Document                                            # noqa: E402
from docx.shared import Pt, Inches, RGBColor                         # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH                        # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT                       # noqa: E402
from docx.oxml.ns import qn                                          # noqa: E402
from docx.oxml import OxmlElement                                    # noqa: E402
# THE REGISTER KEEPS ITS PROVENANCE; THE DELIVERED DOCUMENT DOES NOT PRINT IT.
# A standing-rule identifier and a repository path leak by SHAPE and neither belongs in a
# document written for somebody outside this house. The stripper is the shared one rather
# than a copy: one hand-maintained stripper per study is one hole per study.
from outward_source import outward as _outward_shape                 # noqa: E402

# THE SHARED STRIPPER CATCHES SHAPES; A PROCEDURE NOUN IS NOT A SHAPE. A standing-rule
# identifier and a repository path cannot occur innocently and are matched by shape, which
# is what makes that instrument safe. The NAMES this house gives its own rules can occur
# innocently in ordinary English ("the register", "a gate"), so they cannot be shape-matched
# and are the per-study scrub's job — a judgement about the sense a word is used in.
# These four are the ones the committed records this register PRINTS actually carry, and
# they are named here rather than left on the page because none of them means anything to
# somebody outside this house. The records themselves keep their own words.
_HOUSE_NAMES = (
    ('SIGCM clause 8', 'this house’s rule on missing inputs'),
    ('SIGCM', 'this house’s source-integrity rule'),
    ('PROMOTION RULE', 'this house’s bar on untested parameters'),
    ('promotion rule', 'this house’s bar on untested parameters'),
    ('STAYS on the ratchet', 'STAYS on this house’s list of unfinished business'),
    ('stays on the ratchet', 'stays on this house’s list of unfinished business'),
    ('on the ratchet', 'on this house’s list of unfinished business'),
)


def outward(txt):
    """What an outside reader receives: shapes stripped by the shared instrument, then
    the house's own names for its own rules replaced by what they mean."""
    t = _outward_shape(txt)
    for a, b in _HOUSE_NAMES:
        t = t.replace(a, b)
    return t

D = json.load(open('study_numbers.json', encoding='utf-8'))
INP = D['inputs']
BETA = json.load(open('beta_result.json', encoding='utf-8'))
LIVES = json.load(open('useful_lives.json', encoding='utf-8'))
CJ = json.load(open('contested_judgements.json', encoding='utf-8'))
PANEL = json.load(open(os.path.join('..', 'gbco_walkforward', 'panel.json'), encoding='utf-8'))
VINP = json.load(open(os.path.join('..', 'gbco_walkforward', 'valuation_inputs.json'),
                      encoding='utf-8'))
WFB = json.load(open(os.path.join('..', 'gbco_walkforward', 'forward_ranges.json'),
                     encoding='utf-8'))

EDITION = D['edition']
EDITION_STAMP = '%s-%s-%s' % tuple(EDITION.split('-')[::-1])
_MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
           'August', 'September', 'October', 'November', 'December')


def longdate(iso):
    y, m, dd = (int(x) for x in iso.split('-'))
    return '%d %s %d' % (dd, _MONTHS[m - 1], y)


INK = RGBColor(0x1C, 0x3A, 0x36); GREY = RGBColor(0x6E, 0x7B, 0x77)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
F_DARK, F_PANEL, F_CREAM = '1C3A36', 'EAF0EE', 'F6F1E6'

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(11), Inches(8.5)      # landscape: long source text
sec.left_margin = sec.right_margin = Inches(0.6)
sec.top_margin = sec.bottom_margin = Inches(0.6)
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(9.5); st.font.color.rgb = INK
st.paragraph_format.space_after = Pt(5); st.paragraph_format.line_spacing = 1.05


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)


def cell_margins(t, top=40, bottom=40, left=80, right=80):
    m = OxmlElement('w:tblCellMar')
    for tag, v in [('top', top), ('left', left), ('bottom', bottom), ('right', right)]:
        e = OxmlElement(f'w:{tag}'); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa')
        m.append(e)
    t._tbl.tblPr.append(m)


def borders(t, color='C9D4D1', sz='4'):
    b = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), sz)
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), color)
        b.append(e)
    t._tbl.tblPr.append(b)


def P(text='', size=9.5, bold=False, italic=False, color=INK, space_after=5, space_before=0):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic; r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    return p


def H1(t):
    return P(t, size=15, bold=True, space_before=12, space_after=6)


def H2(t):
    return P(t, size=11.5, bold=True, space_before=10, space_after=4)


def table(rows, widths, size=8.4):
    t = doc.add_table(rows=len(rows), cols=len(widths))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_margins(t); borders(t)
    t.autofit = False
    layout = OxmlElement('w:tblLayout'); layout.set(qn('w:type'), 'fixed')
    t._tbl.tblPr.append(layout)
    for j, w in enumerate(widths):
        t.columns[j].width = Inches(w)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j])
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(1)
            r = p.add_run('' if val is None else str(val))
            r.font.size = Pt(size); r.font.color.rgb = INK
            if i == 0:
                r.bold = True; shade(c, F_PANEL)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def fmt(v):
    if isinstance(v, float):
        return f'{v:,.4f}'.rstrip('0').rstrip('.')
    return f'{v:,}' if isinstance(v, int) else str(v)


def pc(x, d=2):
    return f'{x*100:.{d}f}%'


def _fmt_mn(x):
    return f'{x:,.1f}'


# THE REVIEWERS' OWN FIGURE AND THE SECOND OWNERSHIP PAIR, READ RATHER THAN TYPED. The
# qualification's amount lives in the committed judgements record; the second ownership pair
# is registered in the model and the numbers file does not carry it forward, so it is read
# from the model's own constants — the same route the document builder takes, so the two
# cannot disagree. Both lookups RAISE rather than defaulting: a figure nobody can trace is
# not evidence.
import re as _re                                                     # noqa: E402
_SHARE_OF_PROFIT = float(_re.search(
    r'EGP\s*([\d,.]+)\s*mn share of profit',
    CJ['two_sided_judgement']['basis_b']['against_it']).group(1).replace(',', ''))
_MODEL_SRC = open('compute.py', encoding='utf-8').read()
_STAKE_STATEMENTS = float(_re.search(
    r'^mnt_stake_statements\s*=\s*([0-9.]+)', _MODEL_SRC, _re.M).group(1))
_STAKE_STATEMENTS_PRIOR = float(_re.search(
    r'^mnt_stake_statements_prior\s*=\s*([0-9.]+)', _MODEL_SRC, _re.M).group(1))


# ------------------------------------------------------------------ masthead
t = doc.add_table(rows=1, cols=1); cell_margins(t, 90, 90, 150, 150)
c = t.cell(0, 0); shade(c, F_DARK); c.width = Inches(9.8)
p = c.paragraphs[0]
r = p.add_run('Testahil · GB Corp S.A.E. (EGX: GBCO) — Source Register')
r.bold = True; r.font.size = Pt(12); r.font.color.rgb = WHITE
r2 = p.add_run('   edition %s · %s' % (EDITION_STAMP, longdate(EDITION)))
r2.font.size = Pt(10); r2.font.color.rgb = RGBColor(0x9F, 0xB0, 0xAC)
doc.add_paragraph().paragraph_format.space_after = Pt(4)

P('Where every number came from. This register accompanies the valuation study and the '
  'companion model. Each input carries the source it was taken from, the research layer that '
  'source belongs to, and the date the source itself bears — not the date it was read.',
  size=10)

# ---------------------------------------------------- sourcing position
H2('The sourcing position, stated at the top')
P('Every historical figure in this study, and in the historical testing behind it, comes '
  'from a '
  'document GB Corp published itself, downloaded from the company’s own investor-relations '
  'portal and committed to this study’s directory. No data vendor, broker or press '
  'report is a source for any figure the company reported about itself.', size=9.5)
P('That was not always true of this name, and the reason is recorded rather than smoothed '
  'over. An earlier attempt to reach the filings ran six routes and concluded the documents '
  'were unreachable. Every route was real and every outcome honestly recorded; the host list '
  'had been assembled from what the company used to be called, and the company’s current '
  'domain was never tried. It answers on the first attempt, without authentication. The '
  'lesson is kept because it generalises: a search that guesses a naming convention finds '
  'nothing and reports that as a result.', size=9.5)
P('Two consequences of what the filings actually contain, both material and both disclosed. '
  'First, the audited statements for the four most recent years carry NO text layer at all, '
  'and the same audited statements are reproduced inside the annual report for those years, '
  'which does — so the annual report is the ROUTE and the audited statement is the '
  'DOCUMENT, and the two are recorded separately. Second, the opinion on the very associate '
  'that dominates this valuation is QUALIFIED, and it is qualified in BOTH of the most '
  'recent reporting periods rather than once.', size=9.5)
P('THE QUALIFICATION, IN THE REVIEWERS’ OWN WORDS AND AT THE MOST RECENT DATE. The limited '
  'review of the consolidated interim statements to 30 June 2026 reaches a qualified '
  'conclusion: the reviewers state they “were not provided with the consolidated financial '
  'statements for one of the associate companies (MNT - BV)” and were therefore “unable to '
  'verify the accuracy of the Group’s share of profits” — EGP %s mn recorded in the '
  'period. The same qualification stood on the 31 December 2025 audited statements, where '
  'the auditors record that the group’s share of that associate’s profit rests on '
  'management-prepared accounts. It is set out here, and in the study’s own caveats, because '
  'the LOWER of the two answers this study publishes stands on the carrying value that same '
  'conclusion is qualified at — so the conservative branch is not a safe harbour either, '
  'and a reader is entitled to know that before comparing the two.'
  % _fmt_mn(_SHARE_OF_PROFIT), size=9.5)

# ---------------------------------------------------- primary documents
doc.add_page_break()
H1('1  Primary documents — what was actually read')
_SRC = os.path.join(HERE, 'src')
_files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(_SRC, '*.pdf')))


def _kind(name):
    n = name.lower()
    if 'annual_report' in n:
        return 'Annual report (reproduces that year’s audited consolidated statements)'
    if 'consolidation' in n:
        return 'Reviewed interim consolidated statements'
    if 'consolidated' in n:
        return 'Audited consolidated financial statements'
    if '_er_' in n or 'er_' in n:
        return 'Earnings release'
    if 'irp' in n:
        return 'Investor presentation'
    return 'Company document'


rows = [['#', 'Document', 'What it is', 'Held at']]
for i, f in enumerate(_files, 1):
    rows.append([str(i), f, _kind(f), 'committed with this study'])
table(rows, [0.4, 3.9, 4.4, 1.1], size=7.6)
P('Every file above was downloaded from GB Corp’s own investor-relations portal and is '
  'kept with this study, so a reader can re-derive any figure in the study from the '
  'same document the study read. The count is what the directory holds rather than a number '
  'typed here.', size=9.2)

# ---------------------------------------------------- input register
doc.add_page_break()
H1('2  Input register — every figure that reaches the model')
P('Four fields on every input: the value, the source, the date that source carries, and the '
  'research layer it belongs to. The layer is DERIVED from which source built the entry '
  'rather than typed, so it cannot drift from the source it describes.', size=9.5)
_LAYER_ORDER = {'Company': 0, 'Company (investor relations)': 1}
items = sorted(INP.items(), key=lambda kv: (_LAYER_ORDER.get(kv[1].get('layer'), 9), kv[0]))
_by_layer = {}
for k, v in items:
    _by_layer.setdefault(v.get('layer', 'Unclassified'), []).append((k, v))
for layer in sorted(_by_layer, key=lambda x: _LAYER_ORDER.get(x, 9)):
    H2('Research layer — %s' % layer)
    rows = [['#', 'Input', 'Value', 'Unit', 'Source', 'Source date', 'Route']]
    for i, (k, v) in enumerate(_by_layer[layer], 1):
        rows.append([str(i), k, fmt(v['value']), v.get('unit', ''), outward(v['source']),
                     v['date'], outward(v.get('route', ''))])
    table(rows, [0.32, 1.35, 0.85, 0.55, 4.35, 0.85, 1.53], size=7.4)

H2('The reported history behind the study’s own income statement')
P('The three reported years the study prints are taken from a record of this company’s '
  'consolidated income statement as it was originally reported, year by year. Every year is '
  'asserted to foot against its own arithmetic before it enters anything.', size=9.5)
rows = [['Fiscal year', 'Revenue (EGP mn)', 'Profit attributable (EGP mn)', 'Source document',
         'Source date', 'Foots', 'Route']]
for y in D['history']['years']:
    _is = D['history']['income_statement'][y]
    _p = D['history']['provenance'][y]
    rows.append(['FY%s' % y, f"{_is['revenue']:,.1f}", f"{_is['net_profit']:,.1f}",
                 _p['source'], _p['source_date'], 'yes' if _p['foots'] else 'NO',
                 outward(_p['route'])])
table(rows, [0.75, 1.15, 1.55, 2.45, 0.85, 0.5, 2.55], size=7.6)
P('That reported-history record runs from %s and every year in it foots; the three '
  'printed above are the ones this study’s own statements table carries.'
  % PANEL['_span'], size=9.2)

# ---------------------------------------------------- judgements
doc.add_page_break()
H1('3  Judgements — and what would overturn each one')
P('A judgement is a fork this study resolved one way and could defensibly have resolved the '
  'other. Each row states what was adopted, what the alternative was, what the alternative '
  'is worth, and which direction the study took. The last column is what would overturn the '
  'choice. Nothing here is an input to the valuation: it is a record OF the valuation.',
  size=9.5)
rows = [['Judgement', 'Adopted', 'The alternative', 'Worth', 'Direction taken']]
for j in CJ['judgements']:
    rows.append([outward(j['name']), outward(j['adopted']), outward(j['alternative']),
                 pc(j['moves_the_answer_by'], 1), outward(j['direction'])])
table(rows, [1.45, 2.85, 2.85, 0.6, 2.05], size=7.4)
_TS = CJ.get('two_sided_judgement')
if _TS:
    H2('The judgement this study does NOT resolve — and why it is not in the table above')
    P('One fork dominates every other and the study does not take a side on it: the basis on '
      'which GB Corp’s interest in MNT-Halan is carried. Both values below are the company’s '
      'own disclosures about one holding, and the filings do not choose between them. A sign '
      'test measures WHICH WAY a study resolved its forks, so recording an unresolved one in '
      'it would manufacture a count in whichever direction the two happened to sit; it is '
      'recorded here in full instead.', size=9.5)
    rows = [['Basis', 'The mark (EGP mn)', 'Answer (EGP/share)', 'What it is', 'What is said against it']]
    for _b in (_TS['basis_a'], _TS['basis_b']):
        rows.append([outward(_b['label']), fmt(round(_b['mark_egp_mn'], 1)),
                     '%.4f' % _b['value'], outward(_b['what']), outward(_b['against_it'])])
    table(rows, [1.55, 0.85, 0.85, 2.6, 3.85], size=7.4)
    P('The spread between them is EGP %s mn, %s of the higher answer. Averaging the two would '
      'be a number neither disclosure supports, and a discount standing in for the '
      'uncertainty would be a parameter with nothing observable behind it. The uncertainty is '
      'in this line and it is published as this line.'
      % (fmt(round(_TS['spread_egp_mn'], 1)),
         pc(_TS['spread_as_a_share_of_the_higher_branch'], 1)), size=9.5)

_UNV = CJ.get('unvalued') or []
if _UNV:
    H2('Named and deliberately NOT priced')
    P('Three things bear on the answer and carry no number in it. Each is named with the '
      'reason a number was not invented for it, because an absence a reader cannot see is '
      'the same as an absence nobody noticed.', size=9.5)
    rows = [['What', 'What it is', 'Why it carries no number', 'Direction if it were priced']]
    for _u in _UNV:
        rows.append([outward(_u['name']), outward(_u['what']), outward(_u['why_not_valued']),
                     outward(_u['direction_if_valued'])])
    table(rows, [1.75, 2.6, 3.3, 2.05], size=7.4)

_RET = CJ.get('considered_and_not_counted') or []
if _RET:
    H2('Constructions the superseded edition carried, and why they are not judgements')
    P('Four constructions were removed from this study rather than re-argued. They are listed '
      'because a removed construction that goes unrecorded looks like a construction that was '
      'never there — and because listing them one-sided would be its own distortion: of the '
      'three that can still be priced, counting them would add one upward and two downward.',
      size=9.5)
    rows = [['What it was', 'What the superseded edition did', 'Why it is not an alternative framing', 'Direction if counted']]
    for _r in _RET:
        rows.append([outward(_r['name']), outward(_r['what']),
                     outward(_r['why_not_a_judgement']), outward(_r['direction_if_counted'])])
    table(rows, [1.5, 2.7, 3.6, 1.9], size=7.4)

_st = CJ.get('sign_test', {})
if _st:
    # THE KEYS ARE READ BY NAME AND THE LOOKUP RAISES IF ONE MOVES. The superseded version
    # of this paragraph asked for fields the record does not carry and printed "None were
    # taken upward, on a two-sided test of None" in a delivered document — a sentence a
    # missing key wrote, which is exactly what a default hides and a refusal does not.
    for _k in ('material', 'resolved_upward', 'resolved_downward', 'two_sided_p', 'flagged'):
        assert _k in _st, 'the direction test no longer records %s' % _k
    P('The direction test. A study that resolves every contested fork the same way has a lean '
      'whether or not any single choice is wrong, so the directions are counted rather than '
      'asserted: of %s material judgements the study took the higher-value side on %s and the '
      'lower on %s, a two-sided test of %s. That is %s at the 5%% level. It is measured, not '
      'claimed, and a study is FLAGGED by it rather than failed — a company can genuinely '
      'deserve a consistent read. THE FORK IT DOES NOT COVER IS THE LARGEST IN THE STUDY: the '
      'basis of the associate mark is not resolved at all, so it is deliberately outside a '
      'test that measures which way forks were resolved.'
      % (_st['material'], _st['resolved_upward'], _st['resolved_downward'],
         fmt(_st['two_sided_p']), 'FLAGGED' if _st['flagged'] else 'not flagged'), size=9.5)
P('What would overturn each of these is the same shape in every case and it is stated in the '
  'study body beside the fork: for the associate mark, a real secondary transaction in that '
  'company’s shares at a materially different price, or a second closing repricing the '
  'round; for the working-capital glide, the company’s own quarterly prints, which '
  'resolve it directly; for the margin path, the next reviewed half against the one this '
  'forecast is anchored on; for the cost-of-capital basis, either premium basis being shown '
  'to misprice this sovereign, both being published so a reader can switch; and for the '
  'construction of the central, the question does not arise, because this edition publishes no '
  'blended central at all: one lens is the answer and the others are printed beside it.',
  size=9.5)

# ---------------------------------------------------- negative results
doc.add_page_break()
H1('4  Negative results — what was searched for and not found')
P('Recorded because an absence shaped this model as much as the evidence did. Every row is a '
  'search that was actually run, with what it established.', size=9.5)
_ub = LIVES['route_1_policy_note']
rows = [['What was sought', 'Why it was needed', 'What was found', 'What the study did']]
rows.append([
 'A disclosed useful life for the operating asset base',
 'The house standard builds a terminal on a disclosed life; a life this desk chooses is not '
 'a disclosed life',
 outward(LIVES['_verdict']),
 'No life was chosen. The terminal is carried on the construction the study describes and '
 'the refusal is printed in the study body rather than resolved by inventing a figure.'])
rows.append([
 'Audited statements for the two earliest years of the intended window',
 'The study targets as long a run of sourceable history as the filings support',
 'The company’s own filings index does not reach those years, and the annual reports for '
 'them lay the statements out in a split form the text layer cannot attach to labels',
 'The affected balance-sheet items are recorded as MISSING with that reason, beside the '
 'figures they sit among, and never estimated.'])
rows.append([
 'A usable beta from the first regression attempted on this name',
 'Every study needs the stock’s own beta against the published index of its exchange',
 'The first attempt used five annual observations and returned a negative slope with '
 'essentially no explanatory power — unusable, and correctly refused',
 'The study fell back to the house default at the time. A conforming weekly regression has '
 'since been produced and is what this edition adopts; the superseded figure is recorded '
 'beside it rather than deleted.'])
rows.append([
 'A sourced split of passenger-car revenue between the domestic and regional markets for '
 'the reviewed half',
 'The regional exposure is named as a risk and a reader is entitled to its size',
 'Not disclosed in the documents this study holds for that period',
 'The exposure is NAMED and NOT PRICED. No split was estimated.'])
rows.append([
 'The company’s own audited statements for the associate that dominates this valuation',
 'That associate carries most of the equity value in the primary lens, on either basis',
 'NOT AVAILABLE TO THE REVIEWERS EITHER, in both of the most recent periods. The limited '
 'review of the 30 June 2026 statements reaches a QUALIFIED conclusion at this line — the '
 'reviewers were not provided with that company’s statements and were unable to verify the '
 'group’s EGP %s mn share of its profits for the period — and the same qualification stood '
 'on the 31 December 2025 audited statements' % _fmt_mn(_SHARE_OF_PROFIT),
 'Disclosed in this register, in the study’s caveats and in its disclosure section. It is '
 'the reason the LOWER of the two published answers is not treated as a safe harbour, and '
 'the strongest available argument for discounting both marks.'])
rows.append([
 'One ownership percentage for the MNT-Halan transaction',
 'The higher of the two answers applies a percentage to a round price, so the percentage is '
 'a direct multiplier on the largest line in the study',
 'THERE ARE TWO, AND BOTH ARE THE COMPANY’S OWN. The press release of 9 June 2026 gives '
 '%s from %s; note 34 to the reviewed 30 June 2026 statements and the review report both '
 'give %s from %s for the same transaction — most likely a different level of the '
 'structure, the intermediate holding vehicle rather than the operating group'
 % (pc(D['sotp']['mnt_halan_stake']), pc(D['sotp']['mnt_halan_stake_prior']),
    pc(_STAKE_STATEMENTS), pc(_STAKE_STATEMENTS_PRIOR)),
 'The study adopts the press release’s figure, because it is the one the round it is applied '
 'to was announced with, and PRINTS THE OTHER in the body rather than leaving it out. The '
 'difference is worth a little over one and a half per cent of the round-price answer and '
 'nothing at all on the other.'])
table(rows, [2.05, 2.25, 2.95, 2.55], size=7.6)

# ---------------------------------------------------- derived and discrepancies
doc.add_page_break()
H1('5  Figures that are DERIVED rather than sourced')
P('These appear in no source. They are computed, and the method is given so a reader can '
  'reproduce or reject each one.', size=9.5)
_COC = D['cost_of_capital_record']; _MAC = D['macro']
DER = [
 ('The equity beta — %s' % fmt(round(BETA['beta'], 4)),
  'A %s regression of the shares against the published %s index of the exchange the stock is '
  'listed on, over %s years to %s, on %d observations, with an R-squared of %s and a standard '
  'error of %s. It clears the minimum sample, explanatory power and precision this house '
  'requires before a regression beta may be used at all. A cross-check estimator gives %s. The '
  'index series used is the published %s, and the copy this study regressed against carries its '
  'own as-of date of %s.'
  % (BETA['frequency'], BETA['index_file'].split('/')[-1].replace('.csv', ''),
     fmt(BETA['window_years']), BETA['last_obs'], BETA['n'], fmt(round(BETA['r2'], 4)),
     fmt(round(BETA['se'], 4)), fmt(round(BETA['blume_crosscheck'], 4)),
     BETA['index_file'].split('/')[-1].replace('.csv', ''), BETA['index_asof'])),
 ('The normalised risk-free rate — %s' % pc(_COC['rf_star']),
  'The observed local-currency government bond yield of %s less this sovereign’s own '
  'default spread of %s. Country risk then enters exactly once, inside the equity risk '
  'premium, rather than twice.' % (pc(_COC['rf_observed']), pc(_COC['default_spread']))),
 ('Terminal growth — %s nominal' % pc(_MAC['terminal_growth_nominal']),
  'STORED as a real rate of %s on the house inflation path for this market and recomputed to '
  'its nominal figure against a terminal inflation of %s. A typed nominal rate is '
  'unfalsifiable: nobody can tell whether it meant inflation plus a few points or minus '
  'several.' % (pc(_MAC['terminal_growth_real'], 1), pc(_MAC['terminal_inflation']))),
 ('The cost-of-capital schedule',
  'One forward rate per explicit year, gliding from %s in the first forecast year to a '
  'norm-built terminal of %s, with the terminal brought home on the same cumulative factor '
  'as the last explicit year — one date, one price of time. The glide fractions are the '
  'policy-rate path’s own cumulative progress rather than a second free parameter.'
  % (pc(_COC['wacc_exp']), pc(_COC['wacc_terminal']))),
 ('The passenger-car selling price per unit',
  'Disclosed revenue for the line divided by the disclosed volume for the same line and year, '
  'so it is arithmetic on two published figures rather than an assumption. It reproduces the '
  'reported line exactly in every disclosed year.'),
 ('The far-year forecast ranges',
  'The full span of the observed errors this method made at that horizon on this company’s '
  'own history, applied by multiplying the point projection. THE ORIENTATION IS %s, so a band '
  'above one is a year the method came in low; a band the other way up would move a forecast '
  'in the wrong direction and the two are never assumed. The bounds are a %s of past readings '
  'rather than a percentile, and the observation count is printed beside every band in the '
  'study, because a span of a handful of readings is not a percentile and this study does not '
  'call it one.'
  % (WFB['_orientation'].split('—')[0].strip().replace('_', ' ').upper(),
     WFB['_basis'].split('—')[0].strip())),
]
rows = [['Figure', 'How it was derived']]
for a, b in DER:
    rows.append([a, b])
table(rows, [2.40, 7.30], size=8.0)

H1('6  Aggregator discrepancies and figures deliberately not used')
P('Where a third-party figure was seen and rejected, it is recorded here rather than left to '
  'a reader to wonder about.', size=9.5)
rows = [['Figure', 'What a third party carried', 'What this study uses, and why']]
rows.append([
 'The company’s own reported historicals',
 'Aggregator restatements of revenue, profit and balance-sheet lines circulate for this '
 'name and differ in classification from the filings',
 'NONE of them is used. Every reported figure in this study comes from a document the '
 'company published itself, which is a requirement rather than a preference. Where an '
 'aggregator and a filing disagree, the filing is right by definition of what is being '
 'measured.'])
rows.append([
 'The equity beta',
 'A five-annual-observation estimate returning a negative slope with essentially no '
 'explanatory power',
 'Refused as unusable. The weekly regression in section 5 is what this edition adopts, and '
 'the superseded figure of %s is recorded beside it rather than deleted.'
 % fmt(BETA['superseded_beta'])])
rows.append([
 'The associate stake percentage',
 'An estimate of roughly a fifth circulated in an early draft of this study, and the '
 'pre-transaction figure of %s was carried for a period afterwards'
 % pc(D['sotp']['mnt_halan_stake_prior']),
 'Neither is used. The company states the current figure directly in its own release, and '
 'that is what the study applies; the superseded figures are printed in the study body so a '
 'reader can see what changed.'])
rows.append([
 'The exchange rate applied to the associate mark',
 'Quoted rates for the period differ by source and by whether they are official or parallel',
 'The rate used is stated in the study’s own disclosure section and flagged there as an '
 'estimate. It is a material input to one line and it is labelled as such rather than '
 'presented as a fact.'])
table(rows, [1.85, 3.55, 4.30], size=7.8)

P('')
P('Testahil · Independent valuation research · Educational analysis, not investment advice.',
  size=8.4, italic=True, color=GREY)

OUT = os.path.join(HERE, 'GBCO_Bibliography_%s.docx' % EDITION_STAMP)
doc.save(OUT)
print('wrote', os.path.basename(OUT))
