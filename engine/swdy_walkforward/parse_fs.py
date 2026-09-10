"""Parse SWDY's own consolidated financial statements into the panel's raw cells.

FOUR FIELDS ON EVERY NUMBER and ARITHMETIC IS THE ARBITER. Nothing here trusts the
extractor: every statement block is accepted only where it foots against its own
printed subtotals, and a block that does not foot is reported as UNFOOTED rather than
carried. A figure that looks clean and is wrong is the whole hazard [R-FCAL-01] §1.

The text layer is NOT evidence of a good text layer. SWDY's FY2015 filing yields
173,819 characters over 42 pages — dense by any measure — off an EMBEDDED OCR layer
that renders 2,583,062,094 as "2S83062094" and 598,240,111 as "598 240 Ill". Density
passes; arithmetic does not. That is why the footing test decides the route and the
character count only decides where to start.
"""
import re, os, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = os.path.join(HERE, 'text')

# EGP figures are printed with SPACE thousand separators in the audited statements and
# COMMA separators in the investor documents; negatives arrive in parentheses, with a
# space sometimes inside the bracket. Both are accepted; nothing else is.
#
# THE SEPARATOR IS A SINGLE SPACE AND THE COLUMN GAP IS SEVERAL. A first draft matched
# [\d ,]* and read "281 049 081 719   231 981 835 577" — two columns of one statement —
# as ONE number of 2.8e23. It parsed cleanly, produced a float, and was wrong by eleven
# orders of magnitude. Groups are therefore anchored at three digits with exactly one
# separator between them, which is what a thousand separator is.
#
# A BRACKET IS ONLY A MINUS SIGN WHEN IT IS MATCHED. The audited statements print note
# references right-to-left as ")6(,)44-10(", so an unmatched ")" precedes real figures
# on almost every line of the income statement.
NUM = re.compile(r'\(\s*-?\d{1,3}(?:[ ,]\d{3})*(?:\.\d+)?\s*\)'
                 r'|-?\d{1,3}(?:[ ,]\d{3})*(?:\.\d+)?')


def numbers(line):
    """Every number on a line, in printed order, signed by its MATCHED brackets."""
    out = []
    for m in NUM.finditer(line):
        tok = m.group(0)
        neg = tok.startswith('(')
        body = tok.strip('() ').replace(',', '').replace(' ', '')
        if not body or body in ('-',):
            continue
        try:
            v = float(body)
        except ValueError:
            continue
        out.append((-v if neg else v, m.start()))
    return out


def big(line, minabs=1e5):
    return [v for v, _ in numbers(line) if abs(v) >= minabs]


def find_block(txt, start_pats, stop_pats, after=0):
    lines = txt.splitlines()
    for i in range(after, len(lines)):
        if any(re.search(p, lines[i], re.I) for p in start_pats):
            j = i + 1
            while j < len(lines) and j < i + 400:
                if any(re.search(p, lines[j], re.I) for p in stop_pats):
                    break
                j += 1
            return i, lines[i:j]
    return None, []


def grab(lines, pat, col=0, minabs=1e5, exclude=None):
    """The `col`-th figure on the first line matching `pat`."""
    for ln in lines:
        if exclude and re.search(exclude, ln, re.I):
            continue
        if re.search(pat, ln, re.I):
            v = big(ln, minabs)
            if len(v) > col:
                return v[col], ln.strip()
    return None, None


def load(name):
    p = os.path.join(TEXT, name)
    return open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else None
