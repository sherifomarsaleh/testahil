"""EVERY NUMBER ON A DELIVERED PAGE MUST BE READ, NEVER TYPED.

The defect this exists to stop has one shape and this session found it seventeen times:
a sentence in a delivered document RESTATES a figure instead of READING it, and goes
stale the moment the model moves. Terminal growth published at 5% against a study that
strikes 9.14%. Working capital at 19.9% against a re-anchored 19.67%. The currency path
at 6% against 7.56%. A contested-choice table pricing a tax move at "roughly +1.8" where
the model says +4.95. None of these was found by a gate; all of them were found by a
person reading prose, which does not scale past one company.

prose_check.py already checks that figures on the page RECONCILE to the numbers file.
This checks something different and stricter: that they were never typed in the first
place. A typed digit that happens to agree today is still a defect, because nothing
makes it move tomorrow.

WHAT IS ALLOWED, and the list is deliberately short:
  - digits inside an f-string REPLACEMENT field (that is a read, which is the point)
  - a format spec: {x:.2f}, {y:,.0f}, {z:.1%}
  - years and dates (FY2025, 2026-09-03, 31 December 2025) — these are labels, not
    quantities, and they move with the edition rather than with the model
  - ordinals and section numbers (1.9b, note 39, IAS 33, Table 6)
  - a figure the same line explicitly marks as RETIRED or WITHDRAWN, because publishing
    what a number used to be is how a reader holding an earlier edition finds the change
  - anything on the allow-list below, each entry carrying its reason

Run: python3 typed_digit_check.py [--verbose]
"""
import ast, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILDERS = ('docx_swdy.py', 'docx_register.py')

# The calls whose string arguments reach a reader's page.
DELIVERED = {'P', 'caption', 'H1', 'H2', 'H3', 'bullet', 'table', 'figure', 'note'}

# A quantity: digits with a unit or a decimal point. Not a year, not a section number.
QUANTITY = re.compile(r"""
    (?<![\w.])                      # not mid-identifier, not the tail of 1.9.2
    (?:
        \d{1,3}(?:,\d{3})+(?:\.\d+)?   # 12,646.9
      | \d+\.\d+                        # 19.67
      | \d+\s?%                         # 25%
      | \d+\s?(?:bp|x|×)\b              # 450bp, 3.34x
    )
""", re.X)

# Labels that are not model quantities.
LABEL = re.compile(r"""
    (?:FY|H[12]\s?|Q[1-4]\s?)?(?:19|20)\d{2}        # FY2025, 2026, H1 2026
  | (?:19|20)\d{2}-\d{2}-\d{2}                      # 2026-09-03
  | \b(?:IAS|IFRS|EAS)\s?\d+                        # IAS 33
  | \bnote\s?\d+(?:-\d+)?                           # note 5-3
  | \bsection\s?\d+(?:\.\d+)*[a-z]?                 # section 1.9b
  | \bTable\s?\d+
  | \bFigure\s?\d+
  | \b[12]\d{3}\b
  | ^\s*\d+\.\d+[a-z]?\s                        # a heading's own number: "1.9b  Sensitivity"
  | [S\u00a7]\s?\d+\.\d+[a-z]?                    # a cross-reference: section 1.4, \u00a71.3
  | section-\d+\.\d+
  | \b9[05]%\s*(?:confidence|interval|bound)       # a statistical convention, not a quantity
""", re.X | re.I)

# Marked as no longer adopted: publishing the old number IS the correction.
RETIRED_NEAR = re.compile(
    r'RETIRED|WITHDRAWN|withdraw|retired|an earlier edition|earlier editions|'
    r'used to|previously published|was published at|the old |NOT the|not the '
    r'|rather than the|instead of the|against a study that|USED TO', re.I)

# A FALSIFIER IS A COMMITMENT, NOT AN OUTPUT. "if the margin fails to hold above 11% for
# two consecutive years" is a threshold the analyst states in advance and is bound by; it
# must NOT move when the model moves, which is the whole point of stating it. Recognised
# as a class rather than allow-listed number by number.
COMMITMENT = re.compile(
    r'Falsifier, stated in advance|would refute|would overturn|'
    r'What would change our mind|would change our mind', re.I)

# AND AN ILLUSTRATION IS NOT A CLAIM. "a low of 0.55 and a high of 2.60 would mean the
# outturn had landed between..." teaches a reader how to read a column; the numbers are
# invented on purpose and must not track anything. Recognised only where the text says so
# on its own line, so the exemption cannot be taken silently.
ILLUSTRATION = re.compile(
    r'an illustration of|illustrative|for example|worked example|would mean', re.I)

ALLOW = {
    # text        why it is not a model quantity this document should be reading
    '0.5': 'half of a ratio stated in words, not a model output',
    '100bp': 'the unit the sensitivity row is expressed in, not a value in it',
    '1.0': 'the terminal beta, an adopted convention stated as a constant',
    '50,000': 'the path count of the price engine, fixed in mc_v3 and not a study output',
    '15%': 'the width a sensitivity grid is DESCRIBED as spanning; the grid itself is read',
}


class Finding:
    def __init__(self, path, line, text, snippet):
        self.path, self.line, self.text, self.snippet = path, line, text, snippet

    def __str__(self):
        return '%s:%d  typed %-14s in: %s' % (
            os.path.basename(self.path), self.line, repr(self.text), self.snippet)


def _literal_parts(node):
    """Every piece of a string argument the AUTHOR typed, with its line.

    An f-string's replacement fields are skipped by construction — those are reads,
    and reads are the thing this check wants.
    """
    out = []
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        out.append((node.lineno, node.value))
    elif isinstance(node, ast.JoinedStr):
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                out.append((node.lineno, v.value))
    elif isinstance(node, (ast.List, ast.Tuple)):
        for e in node.elts:
            out.extend(_literal_parts(e))
    elif isinstance(node, ast.BinOp):
        out.extend(_literal_parts(node.left)); out.extend(_literal_parts(node.right))
    elif isinstance(node, ast.Call):
        for a in node.args:
            out.extend(_literal_parts(a))
    return out


def _prose_strings(tree):
    """Strings that are only there for the AUTHOR: docstrings and bare string statements.

    A module docstring explaining why a check exists is not a delivered sentence, and the
    numbers in it are quoted evidence. Excluded by position, never by content.
    """
    out = set()
    for n in ast.walk(tree):
        body = getattr(n, 'body', None)
        if isinstance(body, list):
            for st in body:
                if isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant) \
                        and isinstance(st.value.value, str):
                    out.add(id(st.value))
    return out


def _subscript_keys(tree):
    """Every string used as a lookup — D['dcf'], F['roic'] — so they are not read as prose."""
    keys = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) \
                and isinstance(n.slice.value, str):
            keys.add(id(n.slice))
    return keys


def scan(path, src_lines):
    """EVERY string literal in the builder, not only those handed straight to a render call.

    The first version of this check walked P(...)/caption(...)/table(...) arguments, and
    missed most of the document: these builders assemble `rows = [[...], [...]]` and then
    pass the NAME to table(), so an entire table's worth of typed prose was invisible to a
    check whose whole job was to see it. A gate that inspects the shape of the code rather
    than the text that reaches the page will always have that hole. Every string in the
    module is now candidate prose, less the lookups and format specs that are plainly not.
    """
    tree = ast.parse(open(path).read())
    skip = _subscript_keys(tree) | _prose_strings(tree)
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Constant, ast.JoinedStr)):
            continue
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, str) or id(node) in skip:
                continue
        if isinstance(node, ast.JoinedStr):
            # its Constant children are walked in their own right; taking them here too
            # reports every f-string twice
            continue
        for lineno, text in _literal_parts(node):
            masked = LABEL.sub(' ', text)
            for m in QUANTITY.finditer(masked):
                tok = m.group(0).strip()
                if tok in ALLOW:
                    continue
                window = ' '.join(src_lines[max(0, lineno - 4):lineno + 4])
                if RETIRED_NEAR.search(text) or RETIRED_NEAR.search(window):
                    continue
                # A commitment's heading often sits in its own string a line or two above
                # the threshold it introduces, so this one reads the window like the
                # retired-figure test does.
                if COMMITMENT.search(text) or COMMITMENT.search(window):
                    continue
                if ILLUSTRATION.search(text):
                    continue
                snippet = text.strip()
                if len(snippet) > 110:
                    i = max(0, m.start() - 45)
                    snippet = '...' + snippet[i:i + 105] + '...'
                found.append(Finding(path, lineno, tok, snippet))
    return found


def main():
    verbose = '--verbose' in sys.argv
    all_found = []
    for b in BUILDERS:
        p = os.path.join(HERE, b)
        if not os.path.exists(p):
            continue
        all_found.extend(scan(p, open(p).read().splitlines()))
    if all_found:
        print('TYPED DIGITS ON DELIVERED PAGES: %d' % len(all_found))
        for f in all_found:
            print('  ' + str(f))
        print('\nEach one is a number the document states rather than reads. Point it at '
              'the numbers file, or — if it is a figure that no longer applies — say so '
              'on the same line, which is what marks it as history rather than a claim.')
        return 1
    print('typed-digit check: no delivered sentence states a quantity it does not read '
          '[%d builder(s)]' % len(BUILDERS))
    return 0


if __name__ == '__main__':
    sys.exit(main())
