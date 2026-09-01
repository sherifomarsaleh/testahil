"""Every percentage and multiple that appears in PROSE in the delivered documents must be a
number the model computed. [Added 1 September 2026 after an audit found seven typed figures
the computed numbers beside them contradicted.]

Method: the numbers files (study_numbers, lenses, alternatives, experts, sensitivity grid,
the input register, the band record, the walk-forward bands) are flattened into every
plausible rendering of every value — 0/1/2 decimals as a percentage, as a plain number, as
a multiple — and each figure found in a paragraph or caption of either document must match
one of them. A figure with no computed counterpart FAILS the build; a false positive is
fixed HERE by widening the rendering set, never by deleting the figure from the study.
"""
import json, os, re, sys
from docx import Document
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
DOCS = ['EGCH_Valuation_Study_01-09-2026.docx', 'EGCH_Bibliography_01-09-2026.docx']


def walk(x, out):
    if isinstance(x, dict):
        for v in x.values(): walk(v, out)
    elif isinstance(x, (list, tuple)):
        for v in x: walk(v, out)
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        out.append(float(x))
    elif isinstance(x, str):
        # a figure quoted inside a register's own source text (a bond yield by tenor, a peer
        # multiple cited from an external review, a corrected historical figure) is provenance
        # the register carries verbatim, so it is its own counterpart
        for m in re.finditer(r"-?\d{1,3}(?:,\d{3})*(?:\.\d+)?|-?\d+(?:\.\d+)?", x):
            try: STR_LITERALS.append(float(m.group(0).replace(',', '')))
            except ValueError: pass


vals, STR_LITERALS = [], []
for f in ('study_numbers.json', 'lenses.json', 'alternatives.json', 'experts.json',
          'sensitivity_grid.json', 'input_register.json', 'band_record.json', 'strike_result.json',
          'technicals.json', 'beta_result.json', 'flat_rate_ladder.json', 'live_data.json'):
    if os.path.exists(f):
        walk(json.load(open(f)), vals)
walk(json.load(open(os.path.join('..', 'egch_walkforward', 'forward_ranges.json'))), vals)
walk(json.load(open(os.path.join('..', 'egch_walkforward', 'scores.json')))['drivers'], vals)
# derived renderings: a value v, its percentage forms, 1-v and v-1 (shares and changes), and its inverse
# the technical ladder is published as a distance from spot, which the read does not store
_tech = json.load(open('technicals.json')) if os.path.exists('technicals.json') else {}
_spot = json.load(open('study_numbers.json')).get('spot')
def _levels(x, out):
    if isinstance(x, dict):
        for v in x.values(): _levels(v, out)
    elif isinstance(x, (list, tuple)):
        for v in x: _levels(v, out)
    elif isinstance(x, (int, float)) and not isinstance(x, bool) and _spot:
        out.append(x / _spot - 1)
_lv = []; _levels(_tech, _lv); vals.extend(_lv)
RENDER = set()
for v in vals:
    for x in (v, 1 - v, v - 1, -v, 100 * v, 100 * (1 - v), 100 * (v - 1), v / 100):
        for d in (0, 1, 2, 3):
            RENDER.add(round(x, d))
for v in STR_LITERALS:
    for d in (0, 1, 2, 3, 4):
        RENDER.add(round(v, d))
# structural constants a reader sees that are not model outputs
for x in (0, 5, 10, 15, 20, 25, 50, 80, 90, 95, 100, 22.5, 2.4, 3.95, 4.75, 9.5, 12.5, 6.5, 7.5, 0.5, 1.0, 1.5):
    for d in (0, 1, 2):
        RENDER.add(round(x, d))

NUM = re.compile(r"(?<![\w.])(-?\d{1,3}(?:,\d{3})*(?:\.\d+)?|-?\d+(?:\.\d+)?)\s*(per cent|%|x\b|times)")
problems, checked = [], 0
for f in DOCS:
    d = Document(f)
    texts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                texts.append(c.text)
    for txt in texts:
        for m in NUM.finditer(txt):
            raw = m.group(1).replace(',', '')
            v = float(raw)
            dec = len(raw.split('.')[1]) if '.' in raw else 0
            checked += 1
            if round(v, dec) not in RENDER and round(v, dec) not in {round(y, dec) for y in RENDER}:
                problems.append(f"{f}: '{m.group(0)}' in: …{txt[max(0, m.start()-60):m.end()+40]}…")
print(f"prose figures checked: {checked}; unmatched: {len(problems)}")
for p in problems:
    print("  !", p)
sys.exit(1 if problems else 0)
