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

import json, os

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
