"""A waterfall a reader is asked to follow must reach the answer it prints. Shared
instrument, on the pattern of prose_figures and table_footing — declared once, called by
every study, never copied into one.

WHY THIS EXISTS
    table_footing asks whether a row whose LABEL DECLARES IT A TOTAL reproduces from the
    rows above it. That is one of the two ways a table asserts its own arithmetic, and it
    is not the common one. The other is a WATERFALL: a table that names its operations in
    words down the first column — "Plus net cash", "Less depreciation and amortisation",
    "Add back the impairment" — and prints a result. NOTHING IN SUCH A TABLE SAYS "TOTAL",
    so the label test never fires, and a reader following the instructions the page itself
    gives still arrives somewhere the page does not.

    Read page by page on 04-Sep-2026, one study carried five at once, every table having
    passed table_footing, prose_figures, the recalculation gate, the scrub and the column
    audit, because every figure in all of them was computed and individually correct — the
    defect lives in the RELATIONSHIP between the rows:

      * an enterprise-to-equity bridge deducted EGP 120mn of minority interest in the model
        and printed no line for it, so "Enterprise value 6,617" plus "Plus net cash 4,930"
        stood above a printed "Equity value 11,426";
      * a cash-flow waterfall printed depreciation, capital expenditure and working capital
        between NOPAT and free cash flow, three lines that feed the balance-sheet
        projection and nothing else, while the model builds free cash flow as NOPAT less
        reinvestment — a reader adding the printed column reached 1,829 against a printed
        799, under a caption reading "the full waterfall ... every line is a live formula";
      * three cross-check lenses jumped from an enterprise figure straight to value per
        share, so the net cash, the minority and the share count appeared nowhere.

WHY IT IS A BUILD-TIME ASSERTION AND NOT A DOCUMENT GATE, WHICH WAS MEASURED RATHER THAN
ASSUMED, TWICE
    The obvious instrument is to read the delivered documents and test the arithmetic on
    the page. It was built and run over the whole book, and it does not work, for a reason
    that is a property of pages rather than a weakness in the implementation.

    FIRST DRAFT — test every contiguous numeric run against every figure the study
    committed, on the reasoning that a gap landing on a real model figure names the missing
    line. It flagged 42.4% of all 979 tables. The matches were coincidence: a gap of 0.1645
    against a Kolmogorov-Smirnov statistic, a gap of 5 against a regression window length.
    WITH SEVERAL THOUSAND COMMITTED NUMBERS, SOME NUMBER LANDS IN ANY BAND — the check was
    measuring the size of the pool, not the state of the page. It was also testing
    additivity on tables that never claimed to be additive: a lens summary whose rows are
    four different lenses does not add up and is not supposed to.

    SECOND DRAFT — test only blocks of rows whose labels carry an operator word, which is
    the page making a claim in its own voice. Repointed twice more against real tables (the
    opening balance is the nearest row above IN THE ANSWER'S OWN UNIT, because a margin
    line sits between EBITDA and "Less depreciation" in every income statement in this
    book; a block carrying a division is not testable from the column, because "Divided by
    shares in issue (260.8 million)" states its operand in the label). It still flagged
    30.7% of the 127 tables that carry an operator row.

    THE RESIDUE IS IRREDUCIBLE AND THE REASON IS EXACT: A STATEMENT MIXES LABELLED AND
    UNLABELLED STEPS. One study's income statement runs Revenue, EBITDA, margin,
    depreciation, "Plus other operating income", EBIT — and EBIT is EBITDA less that
    depreciation plus that income. The subtraction is real, the page performs it, and the
    page never says so. No reader of the page alone can tell the anchor from a step, and
    neither can any instrument that only reads the page. A check firing on one table in
    three is the permanently-red check [R-ENF-02] forbids, and widening its tolerance to
    quiet it would be the free parameter the promotion rule forbids.

    SO THE CHECK IS MOVED TO WHERE THE ANCHOR IS KNOWN. The builder knows which figure the
    waterfall starts from, because it put it there. `waterfall()` below takes the anchor,
    the steps and the answer, applies the operator each label states, and REFUSES at build
    time — the [R-COC-01] lesson applied to an instrument's own first draft: when a check
    fires on work that is right, re-point it; never widen it, and never move the work to
    satisfy it.

    check_table() is kept as an ADVISORY measurement, never a gate, because the two
    numbers above are evidence about what pages can and cannot be asked, and an instrument
    that reports its own false-positive rate is worth more than one that hides it.

THE STANDING RULE FOR A FALSE POSITIVE, inherited verbatim because it is the whole
discipline: A FALSE POSITIVE IS FIXED BY DECLARING THE EXCEPTION WITH ITS REASON, NEVER BY
DELETING THE ROW OR SOFTENING THE WORD. An answer that legitimately stands on figures the
table does not print is a real thing — but it is a thing the study must SAY, because an
answer a reader cannot reproduce is indistinguishable from one that is wrong.
"""
import json
import os
import re

from table_footing import SUBITEM_RX, grid, parse_cell    # shared parsers, not copied

# THE OPERATOR VOCABULARY IS CLOSED, and closed for [R-COC-01]'s reason: an open list lets
# a study opt out by inventing a word for "plus". Every entry is an ordinary English
# instruction to add, take away, divide or multiply — none of it is house vocabulary, and
# a row using none of them states no operation and is not a step.
ADD_RX = re.compile(r'^\s*(plus|add(?:\s+back)?|added|including|\+)\b', re.I)
SUB_RX = re.compile(r'^\s*(less|minus|deduct(?:ed|ing)?|net\s+of|excluding)\b', re.I)
DIV_RX = re.compile(r'^\s*(divided\s+by|per\s+share\b|/)\b', re.I)
MUL_RX = re.compile(r'^\s*(times|multiplied\s+by|at\s+a\s+multiple\s+of|[x×])\b', re.I)


def op_of(label):
    """The operation a row's own label instructs, or None where it instructs nothing."""
    for rx, op in ((ADD_RX, '+'), (SUB_RX, '-'), (DIV_RX, '/'), (MUL_RX, '*')):
        if rx.match(label or ''):
            return op
    return None


class WaterfallError(AssertionError):
    """A printed waterfall that does not reach its own printed answer."""


def waterfall(anchor, steps, answer, dp=0, what='', extra=0.0, why=''):
    """Assert a printed waterfall reproduces, and return the value it reproduces to.

        anchor  the figure the operations act on, in the units the table prints
        steps   [(label, value), ...] in printed order; the LABEL decides the sign, so a
                deduction printed as a positive magnitude and one printed in parentheses
                are the same instruction and give the same answer
        answer  the figure the table prints as the result
        dp      decimals the table prints to, which is what sets the tolerance
        extra   a quantity the answer legitimately stands on that the table does not
                print — REQUIRES `why`, because an exception with no reason is the check
                switched off rather than declared

    TOLERANCE IS DERIVED FROM THE PRINTED ROUNDING AND NEVER CHOSEN: each printed row can
    be off by half a unit in its last place, so n+2 rows carry a band of (n+2)*0.5*10**-dp.
    That is arithmetic about the page, not a free parameter.
    """
    if extra and not why:
        raise WaterfallError(
            '%s: a figure the table does not print may be declared, but not without a '
            'reason — an exception with an empty reason has switched the check off '
            'rather than declared it' % (what or 'waterfall'))
    val = float(anchor)
    for label, v in steps:
        o = op_of(label)
        if o is None:
            raise WaterfallError(
                "%s: the step %r states no operation, so a reader is not told what to do "
                "with it" % (what or 'waterfall', label))
        if o == '+':
            val += float(v)
        elif o == '-':
            val -= abs(float(v))
        elif o == '*':
            val *= float(v)
        else:
            val /= float(v)
    val += float(extra)
    band = (len(steps) + 2) * (0.5 * 10.0 ** -int(dp))
    if abs(val - float(answer)) > band + 1e-9:
        raise WaterfallError(
            '%s: the printed rows reach %.6g and the table prints %.6g — a gap of %.6g '
            'against a rounding band of %.6g. A line the model uses is not on the page, '
            'or the answer is not what the page says it is.'
            % (what or 'waterfall', val, float(answer), float(answer) - val, band))
    return val


def signed_column(values, answer, dp=0, what='', extra=0.0, why=''):
    """Assert a column of SIGNED cash effects sums to the answer printed below it.

    The sibling of waterfall(), for the other honest convention. A statement can name its
    operations in words over positive magnitudes, or print signed values and let the sign
    do the work — BOTH ARE CLEAR AND MIXING THEM IS NOT, which is what
    scripts/check_sign_convention.py measures on the page. Where a table prints signed
    values, the operator words come off and this assertion goes on, so the claim is still
    checked and the study does not simply leave the waterfall gate's population.
    """
    if extra and not why:
        raise WaterfallError(
            '%s: a figure the table does not print may be declared, but not without a '
            'reason' % (what or 'signed column'))
    val = sum(float(v) for v in values) + float(extra)
    band = (len(values) + 1) * (0.5 * 10.0 ** -int(dp))
    if abs(val - float(answer)) > band + 1e-9:
        raise WaterfallError(
            '%s: the printed rows sum to %.6g and the table prints %.6g — a gap of %.6g '
            'against a rounding band of %.6g'
            % (what or 'signed column', val, float(answer), float(answer) - val, band))
    return val


# ---------------------------------------------------------------------------
# ONE SIGN CONVENTION PER TABLE — exact, page-only, and needing no anchor
# ---------------------------------------------------------------------------
# THE ANCHOR PROBLEM ABOVE DOES NOT ARISE HERE. Whether a deduction is printed in
# parentheses, as a signed negative, or as a bare magnitude is visible on the page and
# nowhere else, and a table that uses two of those under DEDUCTION labels cannot be read:
# the reader does not know whether to take the magnitude off or add the sign.
#
# It is not a style question. Nine tables in the book do it, and in every one the row that
# breaks the convention is a working-capital line THE MODEL ADDS while its label says
# "Less": one prints "(2,650)", "(360)", "(792)" and then "440"; another prints "810",
# "1,900", "350" and then "-373". A reader following the labels comes out 880 low on a
# 4,368 cash flow — 20% of the year — and nothing on the page says so. In three of the
# nine THE SAME ROW SWITCHES CONVENTION BETWEEN ADJACENT YEARS, which no reader can
# possibly get right.
#
# THE SEMANTIC DEFECT BENEATH IT IS THE REAL ONE and is named here because the arithmetic
# check is what makes it visible: a row labelled "Less INCREASE in working capital" over a
# figure that is a RELEASE states the opposite of what happened. The honest fix is a signed
# label ("Change in working capital, a release shown positive") or one convention through
# the table — never a footnote, because a reader adding a column does not stop to read one.
_BARE_FIGURE = re.compile(r'[(\-\u2212+]?\s*[\d,]+(?:\.\d+)?\s*\)?\s*[%x\u00d7]?')
_NOT_A_FIGURE = ('', '—', '-', '–', 'n/a', 'N/A', 'nil')


def _convention(text):
    """(convention, unit) for a printed figure, or None where it is not one.

    The UNIT rides with the convention because a RATE and an AMOUNT are different
    quantities and comparing their conventions is comparing nothing. One row in the book
    reads "less: complexity / conglomerate discount | 10% | (4,629)" — the rate bare, the
    amount in parentheses, and both perfectly clear. The first draft flagged it, and per
    [R-COC-01] a check firing on work that is right is re-pointed rather than widened.
    """
    t = (text or '').strip()
    if t in _NOT_A_FIGURE:
        return None
    # THE CELL MUST BE A FIGURE AND NOTHING ELSE. A note column carrying "26.3% of equity
    # value" parses as a number under any reader that tolerates trailing words, and a note
    # is not a convention — that false positive was in the first measurement.
    if not _BARE_FIGURE.fullmatch(t):
        return None
    c = parse_cell(t)
    if c is None or c[0] == 0:
        return None
    unit = 'rate' if c[2] else 'amount'
    if t.startswith('('):
        return 'bracket', unit
    if t.lstrip()[0] in '-\u2212':
        return 'signed', unit
    return 'bare', unit


def sign_conventions(rows):
    """Every column of one table whose DEDUCTION rows do not agree on a sign convention.

    Returns {column: {convention: [(row, printed), ...]}} for the columns that disagree.
    """
    out = {}
    width = max((len(r) for r in rows), default=1)
    for j in range(1, width):
        seen = {}
        for i, r in enumerate(rows):
            if not i or op_of(r[0] if r else '') != '-':
                continue
            k = _convention(r[j] if j < len(r) else '')
            if k:
                seen.setdefault(k, []).append((i, (r[j] or '').strip()))
        for unit in ('amount', 'rate'):
            kinds = {k[0]: v for k, v in seen.items() if k[1] == unit}
            if len(kinds) > 1:
                out[j] = kinds
    return out


def sign_conventions_across(rows):
    """Deduction ROWS that switch convention between adjacent columns.

    The sharpest form: one line of a forecast printing "855" in one year and "-4,550" in
    the next, under a single label. Nothing a reader does with that is right.
    """
    out = {}
    width = max((len(r) for r in rows), default=1)
    for i, r in enumerate(rows):
        if not i or op_of(r[0] if r else '') != '-':
            continue
        seen = {}
        for j in range(1, min(width, len(r))):
            k = _convention(r[j])
            if k:
                seen.setdefault(k, []).append((j, (r[j] or '').strip()))
        for unit in ('amount', 'rate'):
            kinds = {k[0]: v for k, v in seen.items() if k[1] == unit}
            if len(kinds) > 1:
                out[i] = ((r[0] or '').strip(), kinds)
    return out


# ---------------------------------------------------------------------------
# ADVISORY ONLY — the page-side reading, kept because its measurement is evidence
# ---------------------------------------------------------------------------
def committed(study_dir, files=('study_numbers.json',)):
    """Every number the study committed, as {abs(value): [dotted key, ...]}.

    Used only to NAME a gap in the advisory, never to decide whether there is one — the
    first draft made it the test and measured the size of the pool instead.
    """
    out = {}

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + [str(k)])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + [str(i)])
        elif isinstance(node, bool):
            return
        elif isinstance(node, (int, float)):
            out.setdefault(abs(float(node)), []).append('.'.join(path))

    for f in files:
        p = os.path.join(study_dir, f)
        if not os.path.exists(p):
            continue
        try:
            walk(json.load(open(p)), [f.replace('.json', '')])
        except (ValueError, OSError):
            continue
    return out


def name_gap(gap, pool, band):
    """The committed key nearest to |gap| within `band`, or '' where nothing matches."""
    g = abs(gap)
    hits = sorted((abs(v - g), v, pool[v]) for v in pool
                  if abs(v - g) <= band + 1e-9 and v > band)
    return hits[0][2][0] if hits else ''


def check_table(rows, pool=None):
    """ADVISORY. Operator blocks whose stated arithmetic does not reach the row below them.

    Measured at 30.7% of the tables that carry an operator row, for the reason in this
    module's docstring: a statement mixes labelled and unlabelled steps and the page cannot
    say which is which. NEVER A GATE. Use waterfall() at build time instead.
    """
    pool = pool or {}
    bad = []
    ops = [op_of((r[0] if r else '') or '') for r in rows]
    i = 1
    while i < len(rows):
        if ops[i] is None:
            i += 1
            continue
        start = i
        while i < len(rows) and ops[i] is not None:
            i += 1
        end = result = i
        if result >= len(rows) or start - 1 < 1:
            continue
        if any(ops[k] in ('/', '*') for k in range(start, end)):
            continue                      # the operand is stated in the label, not the cell
        for j in range(1, max(len(r) for r in rows)):
            res = parse_cell(rows[result][j]) if j < len(rows[result]) else None
            if res is None:
                continue
            answer, dp, pct = res
            anchor, o = None, start - 1
            while o >= 1:
                c = parse_cell(rows[o][j]) if j < len(rows[o]) else None
                if c is not None and c[2] == pct and not SUBITEM_RX.match(rows[o][0] or ''):
                    anchor = c
                    break
                o -= 1
            if anchor is None:
                continue
            val, band, n = anchor[0], (0.5 * 10.0 ** -anchor[1]), 0
            ok = True
            for k in range(start, end):
                c = parse_cell(rows[k][j]) if j < len(rows[k]) else None
                if c is None:
                    ok = False
                    break
                if c[2] != pct:
                    continue
                val += c[0] if ops[k] == '+' else -abs(c[0])
                band += 0.5 * 10.0 ** -c[1]
                n += 1
            if not ok or n == 0:
                continue
            band += 0.5 * 10.0 ** -dp
            if abs(answer - val) > band + 1e-9:
                bad.append((result, j, (rows[result][0] or '').strip(), answer, val,
                            answer - val, name_gap(answer - val, pool, band)))
    return bad
