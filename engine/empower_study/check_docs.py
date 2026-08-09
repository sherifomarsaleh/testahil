"""Scrub + table-discipline checker for the two delivered EMPOWER documents.

1) SCRUB: unzip each .docx, pull word/document.xml, strip tags, and search
   case-insensitively for the banned internal-vocabulary tokens. Multi-word
   tokens are matched as phrases; single words at word boundaries (so
   'engineering', 'during', 'aggregate' do not false-positive, while any bare
   'engine', 'ring', 'gate' is caught).
2) TABLE DISCIPLINE: for every table, compare each column's fixed width against
   its content: a column is STARVED if any single unbreakable word needs more
   width than the column has, and BLOATED if the column is more than 2x the
   width its longest cell line needs. Character width is estimated from the
   largest run font size used in that column (~0.5em per character).
"""
import re, sys, zipfile
import xml.etree.ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = NS['w']

TOKENS = ['step 0', 'step 2a', 'gate', 'ring', 'sweep', 'sigcm', 'parity', 'fail',
          'boundary', 'materiality', 'engine', 'mc_v3', 'protocol', 'qc', 'verdict']

DOCS = ['EMPOWER_Valuation_Study_09-08-2026_public.docx',
        'EMPOWER_Bibliography_09-08-2026.docx']

def doc_xml(path):
    with zipfile.ZipFile(path) as z:
        return z.read('word/document.xml').decode('utf-8')

def plain_text(xml):
    # replace tags with nothing, but keep cell/paragraph separations as spaces
    txt = re.sub(r'<[^>]+>', ' ', xml)
    return re.sub(r'\s+', ' ', txt)

def scrub(path):
    txt = plain_text(doc_xml(path))
    hits = []
    for tok in TOKENS:
        pat = r'\b' + re.escape(tok).replace(r'\ ', r'\s+') + r'\b'
        for m in re.finditer(pat, txt, re.I):
            lo, hi = max(0, m.start() - 60), min(len(txt), m.end() + 60)
            hits.append((tok, '…' + txt[lo:hi] + '…'))
    return hits

def cell_text_and_size(tc):
    parts, szmax = [], 0.0
    for p in tc.findall('.//{%s}p' % W):
        runs = []
        for r in p.findall('.//{%s}r' % W):
            t = r.find('{%s}t' % W)
            if t is not None and t.text:
                runs.append(t.text)
            sz = r.find('.//{%s}sz' % W)
            if sz is not None:
                szmax = max(szmax, float(sz.get('{%s}val' % W)) / 2)
        parts.append(''.join(runs))
    return parts, (szmax or 10.5)

def table_check(path):
    root = ET.fromstring(doc_xml(path))
    problems, tno = [], 0
    for tbl in root.iter('{%s}tbl' % W):
        tno += 1
        first_tc = tbl.find('.//{%s}tc' % W)
        label = (cell_text_and_size(first_tc)[0][0][:38] if first_tc is not None else '?')
        grid = [int(gc.get('{%s}w' % W)) for gc in
                tbl.findall('./{%s}tblGrid/{%s}gridCol' % (W, W))]
        ncols = len(grid)
        colwords = [0] * ncols      # widest single word, twips
        collines = [0] * ncols      # widest cell line, twips
        for tr in tbl.findall('./{%s}tr' % W):
            for j, tc in enumerate(tr.findall('./{%s}tc' % W)):
                if j >= ncols:
                    continue
                lines, sz = cell_text_and_size(tc)
                chw = sz * 10.0          # ~0.5em per char: pt*20 twips/pt * 0.5
                for line in lines:
                    collines[j] = max(collines[j], int(len(line) * chw))
                    for word in re.split(r'[\s/–—-]+', line):
                        colwords[j] = max(colwords[j], int(len(word) * chw))
        margins = 180                    # left+right cell margins, twips
        for j in range(ncols):
            need_word = colwords[j] + margins
            if need_word > grid[j] * 1.02 and colwords[j] > 0:
                problems.append(f"table {tno} [{label}] col {j + 1}: STARVED — longest word "
                                f"needs ~{need_word} twips, column is {grid[j]}")
            if collines[j] > 0 and grid[j] > 2 * (collines[j] + margins):
                problems.append(f"table {tno} [{label}] col {j + 1}: BLOATED — column "
                                f"{grid[j]} twips vs content need ~{collines[j] + margins}")
    return tno, problems

ok = True
for d in DOCS:
    print(f"== {d}")
    hits = scrub(d)
    if hits:
        ok = False
        print(f"  SCRUB: {len(hits)} hit(s)")
        for tok, ctx in hits:
            print(f"    [{tok}] {ctx}")
    else:
        print("  SCRUB: clean — 0 occurrences of any banned token")
    tno, probs = table_check(d)
    if probs:
        ok = False
        print(f"  TABLES: {tno} tables, {len(probs)} width problem(s)")
        for pr in probs:
            print("   ", pr)
    else:
        print(f"  TABLES: {tno} tables, all columns within starved/bloated limits")
sys.exit(0 if ok else 1)
