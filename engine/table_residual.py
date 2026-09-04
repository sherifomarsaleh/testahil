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
