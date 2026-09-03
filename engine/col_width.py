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
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MEASURED = os.path.join(HERE, 'lab', 'col_width', 'measured_thresholds.json')
MEASURED_BOLD = os.path.join(HERE, 'lab', 'col_width',
                             'measured_thresholds_bold.json')

# cm per character in the delivered font at the delivered table size (Georgia 8.5pt as
# authored; the renderer substitutes, and these are measured on what the renderer draws).
PAD = 0.35            # cell padding, both sides, plus the grid rule
DIGIT = 0.20
COMMA = 0.10          # also the period and the hyphen/minus
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
    if c in ',.-–−()':
        return COMMA
    if c == '%':
        return PERCENT
    if c.isspace():
        return 0.0
    return LETTER


def token_cm(tok, bold=False):
    """The width a single unbreakable token needs, padding included."""
    ink = sum(_char_cm(c) for c in str(tok))
    return round(PAD + ink * (BOLD if bold else 1.0), 4)


def required_cm(text, bold=False):
    """The width a cell needs so that it breaks only at spaces.

    A cell may wrap — "Profit attributable to TMG's shareholders" over three lines reads
    perfectly well. What it may not do is break INSIDE a token, so the requirement is set
    by the widest token, never by the whole string.
    """
    toks = str(text).split()
    return max((token_cm(t, bold) for t in toks), default=PAD)


def column_minimums(headers, rows):
    """The minimum width of every column, header included.

    The header is a cell like any other and is frequently the widest token in its column —
    "Discount" over cells reading "35.79%" is what rendered as "Discou nt rate".
    """
    n = len(headers)
    mins = [required_cm(h, bold=True) for h in headers]     # the header row is bold
    for r in rows:
        for i, v in enumerate(r[:n]):
            mins[i] = max(mins[i], required_cm(v))
    return mins


def fit_widths(headers, rows, total_cm=16.2, generous=None, equal_from=None,
               margin_cm=0.05):
    """Widths that clear every cell, with the slack given where it reads best.

    RAISES rather than returning a table that cannot fit. Squeezing is the defect.

    equal_from ties every column from that index onward to ONE width — the widest of their
    minima. A financial statement whose 2030 column is a tenth of a centimetre wider than
    its 2029 column is a table a reader notices, so the common case for a year grid is one
    width for all the years and the remainder to the label.
    """
    # THE MARGIN IS THE MEASUREMENT'S OWN RESOLUTION, NOT A CHOSEN NUMBER. The thresholds
    # were found on a 0.05cm grid, and the per-character model extrapolates from them to
    # strings that were never measured; one grid step covers a model error smaller than
    # the experiment could have detected. It is not a fudge factor and must not be raised
    # to make a table fit — a table that needs more room needs fewer columns.
    mins = [m + margin_cm for m in column_minimums(headers, rows)]
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


def audit(headers, rows, widths):
    """(column, declared, needed) for every column too narrow for its own content."""
    mins = column_minimums(headers, rows)
    return [(headers[i], widths[i], mins[i])
            for i in range(min(len(widths), len(mins)))
            if widths[i] + 1e-9 < mins[i]]


def _self_check():
    """The constants must still reproduce the measurements that produced them.

    NEVER BELOW: a prediction under a measured threshold is a column that will wrap, which
    is the whole defect. Above is allowed and is the intended direction.
    """
    if not os.path.exists(MEASURED):
        return
    bad = []
    for path, is_bold in ((MEASURED, False), (MEASURED_BOLD, True)):
        if not os.path.exists(path):
            continue
        for t, v in json.load(open(path)).items():
            if v is not None and token_cm(t, is_bold) + 1e-9 < v:
                bad.append((t, 'bold' if is_bold else 'plain', v, token_cm(t, is_bold)))
    assert not bad, ('col_width constants no longer clear their own measurements: %s'
                     % bad)


_self_check()
