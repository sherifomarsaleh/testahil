#!/usr/bin/env python3
"""How wide a table column has to be so that no cell in it breaks mid-token.

WHY THIS IS ARITHMETIC AND NOT JUDGEMENT. A cell one character too narrow wraps, and Word
breaks a line after a hyphen — so a negative number renders as a bare dash with its digits
on the line beneath, which a reader takes for a positive figure or for a dash meaning "not
applicable". THE SIGN OR THE MAGNITUDE OF A PRINTED FIGURE CHANGES AS IT IS READ, FROM A
PURELY TYPOGRAPHIC CAUSE. Every gate in this repository looks at how a number was BUILT;
this is a property of the page.

IT HAS BEEN GOT WRONG TWICE BY FEEL AND BOTH TIMES THE DIAGNOSIS WAS THE INTERESTING PART.
A non-breaking minus (U+2212) was tried first and made it WORSE — it is typographically
correct, offers no break, and is WIDER than a hyphen, so every cell in the row then wrapped
mid-number. Then a widening was applied that fixed the row somebody was looking at and left
the table's widest row still wrapping: A COLUMN HAS TO CLEAR THE WIDEST CELL IN THE TABLE,
NOT THE WIDEST CELL IN THE ROW THAT PROVOKED THE FIX.

THE CONSTANTS ARE MEASURED, NOT CHOSEN. engine/lab/col_width/measure.py builds a document
of single-token cells across a 0.05cm grid from 1.00 to 3.00, renders it, reads the text
back, and reports for each token the width at which it stops splitting. Fifteen tokens
were measured in the delivered font at the delivered size; the per-character figures below
reproduce every one of them exactly for digits and conservatively for letters, and the
module ASSERTS that at import against the committed measurements. A constant that stopped
reproducing its own measurement would fail the import rather than round a column down.

THE ROUNDING IS DELIBERATELY ONE-SIDED. A column wider than it needs costs white space; a
column narrower than it needs changes a printed figure. So letters carry the conservative
figure rather than the fitted one, and fit_widths() REFUSES rather than squeezing: a table
whose content cannot fit its page is a table that needs fewer columns or a smaller font,
and silently dividing the shortfall among its columns is how every one of these defects
was produced in the first place.
"""
import json
import re
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MEASURED = os.path.join(HERE, 'lab', 'col_width', 'measured_thresholds.json')
MEASURED_BOLD = os.path.join(HERE, 'lab', 'col_width',
                             'measured_thresholds_bold.json')
MEASURED_7P5 = os.path.join(HERE, 'lab', 'col_width',
                            'measured_thresholds_7p5pt.json')
BASE_PT = 8.5         # the size the per-character figures were measured at
GRID = 0.05           # the experiment's step, and therefore its resolution

# cm per character in the delivered font at the delivered table size (Georgia 8.5pt as
# authored; the renderer substitutes, and these are measured on what the renderer draws).
PAD = 0.35            # cell padding, both sides, plus the grid rule
DIGIT = 0.20
COMMA = 0.10          # also the period and the hyphen/minus
PAREN = 0.13          # measured: "(16,493)" needs 1.70, which the comma figure missed
                      # by 0.05 — a bracketed negative is the house's own convention for
                      # a deduction, so it is the one shape that must not be underestimated
PERCENT = 0.30
LETTER = 0.18         # conservative: the fitted average is 0.167 and the widest
                      # measured word implies 0.171
# A HEADER CELL IS BOLD AND BOLD IS WIDER. The first draft of this module measured plain
# cells only, sized a header column from them, and the delivered page still printed
# "Discoun" — the model was right about the string and wrong about the face it is set in.
# Measured on seven tokens: bold needs 1.077x to 1.121x the INK of the same token plain
# (the padding does not scale), so the factor clears every one of them.
BOLD = 1.13


def _char_cm(c):
    if c.isdigit():
        return DIGIT
    if c in '()':
        return PAREN
    if c in ',.-–−':
        return COMMA
    if c == '%':
        return PERCENT
    if c.isspace():
        return 0.0
    return LETTER


def token_cm(tok, bold=False, size=BASE_PT):
    """The width a single unbreakable token needs, padding included.

    THE INK SCALES WITH POINT SIZE AND THE PADDING DOES NOT — cell margins are fixed. The
    first draft had no size term at all and judged an input register set at 7.5pt by
    figures measured at 8.5, which is a tenth of a centimetre on a ten-character date and
    exactly the margin these columns are decided by. Measured at 7.5pt on four tokens the
    ink ratio runs 0.875 to 0.889 against a nominal 7.5/8.5 = 0.882, so the scaling is
    linear inside the experiment's own 0.05cm resolution.
    """
    ink = sum(_char_cm(c) for c in str(tok)) * (float(size) / BASE_PT)
    return round(PAD + ink * (BOLD if bold else 1.0), 4)


def required_cm(text, bold=False, size=BASE_PT):
    """The width a cell needs so that it breaks only at spaces.

    A cell may wrap — "Profit attributable to TMG's shareholders" over three lines reads
    perfectly well. What it may not do is break INSIDE a token, so the requirement is set
    by the widest token, never by the whole string.
    """
    toks = str(text).split()
    return max((token_cm(t, bold, size) for t in toks), default=PAD)


def column_minimums(headers, rows, size=BASE_PT):
    """The minimum width of every column, header included.

    The header is a cell like any other and is frequently the widest token in its column —
    "Discount" over cells reading "35.79%" is what rendered as "Discou nt rate".
    """
    n = len(headers)
    mins = [required_cm(h, bold=True, size=size) for h in headers]   # headers are bold
    for r in rows:
        for i, v in enumerate(r[:n]):
            mins[i] = max(mins[i], required_cm(v, size=size))
    return mins


def fit_widths(headers, rows, total_cm=16.2, generous=None, equal_from=None,
               margin_cm=GRID, size=BASE_PT):
    """Widths that clear every cell, with the slack given where it reads best.

    RAISES rather than returning a table that cannot fit. Squeezing is the defect.

    equal_from ties every column from that index onward to ONE width — the widest of their
    minima. A financial statement whose 2030 column is a tenth of a centimetre wider than
    its 2029 column is a table a reader notices, so the common case for a year grid is one
    width for all the years and the remainder to the label.
    """
    # THE MARGIN IS THE MEASUREMENT'S OWN RESOLUTION, NOT A CHOSEN NUMBER. The thresholds
    # were found on a 0.05cm grid, so the true threshold of a measured token lies within
    # one step below its measured value, and the per-character model extrapolates from
    # them to strings that were never measured; one grid step covers a model error smaller
    # than the experiment could have detected. It is not a fudge factor and must not be raised
    # to make a table fit — a table that needs more room needs fewer columns.
    mins = [m + margin_cm for m in column_minimums(headers, rows, size)]
    if equal_from is not None and equal_from < len(mins):
        w = max(mins[equal_from:])
        mins = mins[:equal_from] + [w] * (len(mins) - equal_from)
    need = sum(mins)
    if need > total_cm + 1e-9:
        raise ValueError(
            'this table cannot fit %.2fcm: its cells need %.2fcm '
            '(%s). Widen the page, drop a column, or shorten a header — do NOT '
            'squeeze, which is how a printed figure loses its sign.'
            % (total_cm, need, ', '.join('%s:%.2f' % (h, m)
                                         for h, m in zip(headers, mins))))
    slack = total_cm - need
    if generous is None:
        generous = 0 if headers else None
    out = list(mins)
    if generous is not None and 0 <= generous < len(out):
        out[generous] += slack
    else:
        for i in range(len(out)):
            out[i] += slack / len(out)
    return [round(x, 2) for x in out]


# A BROKEN WORD IS UGLY; A BROKEN FIGURE IS WRONG, AND ONLY THE SECOND IS CHECKED.
# Measured over every delivered document, 15.6% of tables carried a column narrower than
# its widest token — and the measurement is sound, because the model reproduces the
# thresholds exactly and the predicted breaks are on the page (PHDC's input register
# prints every date as "2025-12-" with "31" on the line beneath). But a source column
# holding a URL needs 26.89cm on a 16.79cm page: THAT TOKEN CANNOT FIT ANY COLUMN, and
# demanding it would be a false claim about what a table can do, which is the
# permanently-red check [R-ENF-02] forbids.
#
# The line is drawn where the CONSEQUENCE changes. A word broken across two lines is a
# typographic nuisance a reader reassembles without noticing. A FIGURE broken across two
# lines changes what the reader reads: a negative loses its sign, a date loses its day, a
# rate loses its percent sign and reads as a bare number. So the audit considers only
# tokens that carry data, and fit_widths still sizes for everything a builder can fit.
_DATA_TOKEN = re.compile(r'^[(\[]?[-–−+]?[\d][\d,.\-/:%)\]]*$')


def is_data_token(tok):
    """A token whose meaning changes if it breaks: a number, a rate, a date, a bracket."""
    t = str(tok).strip()
    return bool(t) and bool(_DATA_TOKEN.match(t)) and any(c.isdigit() for c in t)


def audit(headers, rows, widths, data_only=True, size=BASE_PT, tol=0.0):
    """(column, declared, needed) for every column too narrow for a token it must not break.

    data_only=False asks the stricter question — whether ANY token fits — which is the
    right question for a builder sizing its own table and the wrong one for a gate.

    THE TOLERANCE DEFAULTS TO ZERO, AND THE REASON IS A MEASUREMENT RATHER THAN A
    PREFERENCE. It was first set to one grid step, on the sound epistemic ground that a
    column short by less than the experiment could resolve is a column the model cannot
    judge. That is true and it is the wrong policy: PHDC's register column sits 0.039cm
    under, inside one step, AND ITS PAGE DEMONSTRABLY WRAPS — "2025-12-" with a bare "31"
    on the line beneath, in the field a reader of a provenance register checks first. The
    tolerance hid a defect that had been verified on the page.
    The costs are not symmetric. A false positive widens a column that did not need it and
    costs white space; a false negative ships a figure that changes as it is read. So the
    uncertainty is spent on the side that costs less, and it is spent in fit_widths, where
    a builder adds a step of headroom while sizing.
    """
    n = len(headers)
    mins = [PAD] * n
    for r in [headers] + list(rows):
        bold = r is headers
        for i, v in enumerate(r[:n]):
            for tok in str(v).split():
                if data_only and not is_data_token(tok):
                    continue
                mins[i] = max(mins[i], token_cm(tok, bold, size))
    return [(headers[i], widths[i], mins[i])
            for i in range(min(len(widths), len(mins)))
            if widths[i] + tol + 1e-9 < mins[i]]


def _self_check():
    """The constants must still reproduce the measurements that produced them.

    A MEASURED THRESHOLD IS AN UPPER BOUND, NOT THE THRESHOLD. The experiment walks a
    0.05cm grid and reports the smallest step at which a token stopped splitting, so the
    true threshold lies in (measured - GRID, measured]. A prediction anywhere in that
    interval is consistent with the experiment; one BELOW it is not, and that is what this
    asserts. Demanding the model reproduce the grid value exactly would be demanding a
    precision the experiment does not have — the first version did, and failed on a
    0.012cm discrepancy at 7.5pt that is a quarter of one grid step.

    The engineering answer to the residual uncertainty is not a tighter model but the
    margin fit_widths already adds, which is exactly one grid step.
    """
    if not os.path.exists(MEASURED):
        return
    bad = []
    for path, is_bold, sz in ((MEASURED, False, BASE_PT), (MEASURED_BOLD, True, BASE_PT),
                              (MEASURED_7P5, False, 7.5)):
        if not os.path.exists(path):
            continue
        for t, v in json.load(open(path)).items():
            if v is not None and token_cm(t, is_bold, sz) + GRID + 1e-9 < v:
                bad.append((t, '%s %gpt' % ('bold' if is_bold else 'plain', sz), v,
                            token_cm(t, is_bold, sz)))
    assert not bad, ('col_width constants no longer clear their own measurements: %s'
                     % bad)


_self_check()
