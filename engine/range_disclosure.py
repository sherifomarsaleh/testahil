"""The sentence a far-year range owes its reader.  [L-354]

A study publishing years three to five as a RANGE takes that range from how wrong
the method has been before -- the observed span of a handful of past errors.
Measured walk-forward across the book (engine/valuation_calibration/band_holdout.py),
those ranges catch 55.6% of outcomes against an expected 63.5%, degrading to 29%
at five years where sixteen of seventeen misses fall on the low side. A reader
shown a range without its count will read it as an interval, and it is not one.

WHAT THIS MODULE IS AND IS NOT. It does NOT widen anything: a widening factor
chosen to make the coverage table pass is the free parameter the promotion rule
forbids. It supplies the DISCLOSURE -- the count, and what the span of that count
can honestly promise -- so that the same sentence is written once rather than
hand-maintained in five studies with five different holes, which is the shared-
instrument lesson this repository has now learned three times.

TWO NUMBERS, AND QUOTING ONLY THE FIRST WOULD BE THE FLATTERING HALF. The
arithmetic one: under exchangeability a fresh draw falls inside the min-max span
of k previous draws with probability (k-1)/(k+1), computed from the count the
study actually has and never typed. The MEASURED one: across this house's own
tested record those ranges do WORSE than that -- 55.6% against an expected 63.5%
at the last reading, and far worse at five years. A sentence quoting only the
arithmetic figure would overstate the range, which is the cautious-sounding claim
that never gets audited [R-CAL-02]. Both are quoted, and the measured one is READ
LIVE from the band-holdout record rather than typed, because it moves as more
forecasts resolve. A study whose record cannot be read gets the sentence WITHOUT
a measured figure and a note saying so -- never a typed one.

    from engine import range_disclosure as RD
    RD.sentence(4)   ->  the sentence for a range built on four observations

A count below MIN_MEANINGFUL returns a sentence saying the range cannot carry a
probability at all, rather than quoting a number derived from two observations.
"""

import json, os, re

MIN_MEANINGFUL = 4
_RECORD = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "valuation_calibration", "band_holdout.json")


def measured():
    """The house's own tested coverage of these ranges, read live. None where the
    record is absent or unreadable -- an absent figure is never replaced by a
    typed one.

    THE RECORD IS ONLY AS CURRENT AS ITS LAST RUN. band_holdout.py must be re-run
    in the same pass as any change to a run's scored cells, exactly as the
    per-name calibration record must be regenerated with any refit. A sentence
    built on a stale record is a page that states a fact which moves, remembering
    it -- the defect the two-part as-of stamps were adopted to close."""
    try:
        d = json.load(open(_RECORD))["pooled"]
        n, inside = d["n"], d["inside"]
        return (inside / n, n) if n else None
    except Exception:
        return None


def expected_coverage(k):
    """P(a fresh draw lands inside the min-max span of k previous draws) under
    exchangeability. Returns None where k is too small to mean anything."""
    if k is None or k < MIN_MEANINGFUL:
        return None
    return (k - 1.0) / (k + 1.0)


def sentence(k, horizon=None):
    """The disclosure a range built on k past observations owes its reader."""
    where = (" at %s" % horizon) if horizon else ""
    if k is None or k < MIN_MEANINGFUL:
        return ("The range%s is the full span of %s past observation%s of this "
                "method's own error. That is too few to carry a probability, and "
                "none is claimed: it is the widest and narrowest this method has "
                "been on this company, not a confidence interval."
                % (where, "no" if not k else str(k), "" if k == 1 else "s"))
    p = expected_coverage(k)
    core = ("The range%s is the full span of %d past readings of how far out this "
            "method has been on this company. A span of %d readings would be "
            "expected to contain the next one about %d times in 100 — not 90."
            % (where, k, k, round(100 * p)))
    m = measured()
    if m is None:
        return core + (" We hold no tested record of how often these ranges have "
                       "actually contained the outcome, so no measured figure is "
                       "quoted here.")
    cov, n = m
    return core + (" Tested against %d resolved readings across the companies we "
                   "cover, ranges of this kind contained the outcome %d times in "
                   "100, and fewer the further out the year. Read it as the "
                   "widest and narrowest we have been, which is narrower than a "
                   "confidence interval rather than wider."
                   % (n, round(100 * cov)))


# ---------------------------------------------------------------------------
# DOES THE DELIVERED DOCUMENT ACTUALLY CARRY THE RANGE?  [R-FCAL-01]
#
# The sentence above is what a range OWES its reader; this half asks the prior
# question, which nothing had asked: whether the range reaches the reader at
# all. [R-FCAL-01] requires every run's updated fundamental analysis to publish
# YEARS 3-5 AS RANGES from that record's own driver-error distribution, NEVER as
# points. Five runs commit a band; three of the five print it and two print
# points, and the two that do not are exactly the two nobody was looking at.
#
# THE THREE SHAPES ARE READ OFF THE BOOK RATHER THAN INVENTED, which is [L-355]
# applied to the instrument that measures it -- a matcher built from one study's
# convention silently finds nothing in the other two and reports that as a
# result:
#   A  COLUMN PAIR   a table whose header carries a low column and a high column
#                    beside the point ("years three to five | Low | Point | High")
#   B  ROW PAIR      row labels naming the low and the high of the range
#                    ("Revenue - low of the range" / "- high of the range")
#   C  DASH CELL     one cell carrying both ends ("84,517 - 193,380")
#
# AND THE TABLE MUST BE FORECAST-BEARING, which is arithmetic about the page
# rather than a fourth word list: it names a calendar year at least two beyond
# the study's own date, so a range over reported history or over a price library
# cannot satisfy it.
#
# WHAT THIS DELIBERATELY DOES NOT CHECK, stated rather than discovered later: it
# does not verify that the printed range REPRODUCES the run's committed band. A
# study applies a multiplier band to its own point path, so the committed figures
# never appear on the page, and searching every numeric pair for a matching ratio
# is the coincidence the waterfall instrument already measured at 42.4% of all
# tables -- with several thousand committed numbers some pair lands in any band.
# Reconciling the printed range to the record needs the study to DECLARE what it
# printed, on the prose_figures architecture, and that is a re-issue on four
# studies rather than something done in passing. This tells a published range
# from no range at all, which is the breach actually found, and says so.
# ---------------------------------------------------------------------------

_LOW = re.compile(r"\blow\b", re.I)
_HIGH = re.compile(r"\bhigh\b", re.I)
_RANGE_ROW = re.compile(r"\b(low|high)\b[^|]{0,24}\bof the range\b", re.I)
_NUM = r"[0-9][0-9,]*(?:\.[0-9]+)?"
_DASH_CELL = re.compile(r"^\(?%s\)?\s*[\u2013\u2014]\s*\(?%s\)?$" % (_NUM, _NUM))
# NOT \b...\b: EGCH heads its far-year columns "FY2028/29", where no word
# boundary sits between the Y and the 2, so a bounded pattern reads that
# document as carrying no forecast year at all and condemns a study that
# conforms. Caught by a fixture rather than in the book [L-355].
_YEAR = re.compile(r"(?<!\d)(20[2-9][0-9])(?!\d)")

FAR_YEAR_OFFSET = 2   # year three of a five-year forecast struck in year Y is Y+2


def _cells(table):
    for row in table:
        for cell in row:
            yield cell


def _is_year(tok):
    return bool(_YEAR.fullmatch(tok.strip()))


def _far(text, study_year):
    return any(int(y) >= study_year + FAR_YEAR_OFFSET for y in _YEAR.findall(text))


def far_year_range_shapes(tables, study_year):
    """Which of the three shapes a document's TABLES carry, as a sorted list.

    `tables` is a list of tables, each a list of rows, each a list of cell
    strings. `study_year` is the calendar year the study itself is dated in.

    THE RANGE MUST BE POSITIONED AT A FAR YEAR, not merely printed in a table
    that mentions one somewhere, AND THAT CLAUSE WAS REACHED BY MEASUREMENT
    RATHER THAN BY PREFERENCE. A first draft asked only that the table name a
    far year, and on the book as it stands it fired on six studies that have no
    walk-forward at all, in three legible kinds: a PERIOD written with a dash
    ("2026-2027" in a watch-list, "2028-2030" against a loan tranche), a
    multiple range in a lens table ("Range at 10x / 16x"), and a charter-rate
    spread in a vessel table. Not one of those is a far forecast year published
    as a range, and every one sat in a table that happened to carry a year. Per
    [R-COC-01]: WHEN A CHECK FIRES ON WORK THAT IS RIGHT, RE-POINT IT -- never
    widen it and never move what is measured to satisfy it. So the low/high
    evidence must sit in a row LABELLED with a far year or a column HEADED by
    one, which is structural rather than a fourth word list, and a dash cell
    whose two operands are both calendar years is a period rather than a range."""
    found = set()
    for tb in tables:
        if not tb:
            continue
        header = tb[0]
        far_cols = {j for j, c in enumerate(header) if _far(c, study_year)}
        far_rows = {i for i, row in enumerate(tb) if row and _far(row[0], study_year)}
        if not far_cols and not far_rows:
            continue
        if far_rows and (any(_LOW.search(c) for c in header)
                         and any(_HIGH.search(c) for c in header)):
            found.add("A")
        if far_cols and any(_RANGE_ROW.search(row[0]) for row in tb if row):
            found.add("B")
        for i, row in enumerate(tb):
            for j, cell in enumerate(row):
                if i not in far_rows and j not in far_cols:
                    continue
                t = cell.strip()
                if not _DASH_CELL.match(t):
                    continue
                parts = re.split(r"[\u2013\u2014]", t)
                if len(parts) == 2 and all(_is_year(x) for x in parts):
                    continue          # a period, not a range
                found.add("C")
    return sorted(found)


def audit(k):
    """The figures behind the sentence, for a study's own record."""
    m = measured()
    return {"observations": k, "expected_coverage": expected_coverage(k),
            "measured_coverage": (m[0] if m else None),
            "measured_n": (m[1] if m else None),
            "min_meaningful": MIN_MEANINGFUL, "sentence": sentence(k)}


if __name__ == "__main__":
    for k in (2, 3, 4, 5, 6, 8, 12):
        print("k=%-3d %s" % (k, sentence(k)))
