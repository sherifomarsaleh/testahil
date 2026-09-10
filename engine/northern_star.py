"""THE TRADED PRICE IS THE NORTHERN STAR  [R-STAR-01]

The principal, 10 September 2026, on a study whose central sat 56% below the market:

    "When I stated that the actual traded price is your northern star, you took that
    lightly. IT IS YOUR NORTHERN STAR. And you have to have a very strong case to
    provide a fair value that is below it. Because essentially you are saying that
    the investors are all idiots including institutions and that they are overpaying.
    You have to have an AIR TIGHT case to put forward. On the other hand, the fair
    value can be higher than a price and that is normal, because the fair price may
    relate to a potential that is yet to be realised in a year or so and investors
    are taking a short term attitude."

THE RULE IS ASYMMETRIC AND THE ASYMMETRY IS THE POINT. A central BELOW the traded
price is a claim that the market -- including institutions who have read the same
filings -- is overpaying. That claim can be true, and this house has made it and been
right. What it cannot be is CASUAL. So the burden of evidence rises with the gap, and
it rises on one side only. A central ABOVE the price needs no such case: that is the
ordinary situation of value not yet realised, where the market is taking a shorter
view than the model.

WHAT THIS RULE DOES NOT DO, AND MUST NEVER BE READ TO DO. It does not license moving
a fair value toward a price. A value adjusted to meet a quote is the reverse-engineered
rate this house prohibits outright, and nothing here softens that. This module raises
a BAR OF EVIDENCE. The honest responses to a bar you cannot clear are to find the
defect, or to publish the study saying in as many words that the case is not made --
never to nudge the number until the bar goes away.

HOW IT COMPOSES WITH [R-GAP-04]. That rule already requires an exhaustive, recorded
hunt for OUR OWN error before a gap is called genuine. This one says what happens
after that hunt comes back empty: the hunt's own findings are the material the case
is built from, and if they do not amount to a case, that is the finding.

    python3 engine/northern_star.py SWDY
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


class NorthernStarError(RuntimeError):
    """A central below the traded price without the case the gap requires."""


# The bar, by how far below the price the central sits. A band, not a cliff: the
# same claim is cheap at 5% and extraordinary at 60%, and a single threshold would
# say the two are the same thing.
BANDS = (
    (0.10, "none",
     "Within 10% of the market. A valuation and a price disagreeing by less than "
     "this is ordinary dispersion and needs no case at all."),
    (0.25, "stated",
     "The study STATES, in the body and not in a footnote, what the market appears "
     "to be pricing that this model is not, and why."),
    (0.40, "priced",
     "The above, plus the disagreement DECOMPOSED: which drivers carry the gap, "
     "each priced in currency per share, summing to the gap. A reader must be able "
     "to see which single assumption would have to be wrong to close it."),
    (1.00, "airtight",
     "The above, plus a recorded exhaustive hunt for our own error that came back "
     "empty [R-GAP-04], the specific thing the market is asserted to be getting "
     "wrong NAMED, and the falsifier stated in advance -- what would have to "
     "happen for this study to be the one that is wrong."),
)



def _latest_close(ticker):
    """(price, ISO date) of the most recent close in the library, or (None, None).

    Reads the committed OHLC series directly rather than any study's own copy of a
    price: a study records the quote it was struck at, which is the question this
    function is NOT asking.
    """
    root = os.path.join(HERE, "raw_ohlc")
    if not os.path.isdir(root):
        return None, None
    for mkt in sorted(os.listdir(root)):
        p = os.path.join(root, mkt, "%s.csv" % ticker.upper())
        if not os.path.exists(p):
            continue
        try:
            with open(p, encoding="utf-8-sig") as fh:
                rows = [r for r in fh.read().splitlines() if r.strip()]
        except OSError:
            return None, None
        if len(rows) < 2:
            return None, None
        best = None
        for r in rows[1:]:
            f = [c.strip().strip('"') for c in r.split(",")]
            if len(f) < 2:
                continue
            try:
                d = _dt.datetime.strptime(f[0], "%m/%d/%Y").date()
                v = float(f[1].replace(",", ""))
            except ValueError:
                continue
            if best is None or d > best[0]:
                best = (d, v)
        if best:
            return best[1], best[0].isoformat()
    return None, None


def band(gap_down: float):
    """(name, requirement) for a central this far BELOW the price. 0.0 if above."""
    for edge, name, req in BANDS:
        if gap_down <= edge:
            return name, req
    return BANDS[-1][1], BANDS[-1][2]


def assess(central, spot, case=None, hunt_recorded=False, decomposition=None,
           falsifier=None, ticker=""):
    """The bar this study has to clear, and whether what it carries clears it.

    `case` is the study's own written argument; `decomposition` a mapping of driver
    to currency-per-share; `falsifier` the stated in-advance condition. Returns a
    record. Raises only through `enforce`, so a study can inspect before it ships.
    """
    if spot is None or spot <= 0:
        raise NorthernStarError("no traded price to measure against; a study without a "
                                "price has no northern star and cannot be assessed")
    ratio = central / spot - 1.0
    above = ratio >= 0
    gap_down = 0.0 if above else -ratio
    name, req = band(gap_down)
    rec = dict(rule="R-STAR-01", ticker=ticker.upper(), central=central, spot=spot,
               gap=ratio, direction="above" if above else "below",
               tier="none" if above else name, requirement=None if above else req)
    if above:
        rec["verdict"] = "PASS"
        rec["note"] = ("The central sits ABOVE the traded price, which needs no case: "
                       "value not yet realised is the ordinary situation, and the market "
                       "taking a shorter view is not a defect in either.")
        return rec

    missing = []
    if name in ("stated", "priced", "airtight") and not (case or "").strip():
        missing.append("a written case naming what the market appears to be pricing "
                       "that this model is not")
    if name in ("priced", "airtight"):
        if not decomposition:
            missing.append("a decomposition of the gap by driver, priced per share")
        else:
            total = sum(abs(v) for v in decomposition.values())
            want = abs(spot - central)
            if total < 0.5 * want:
                missing.append(
                    "a decomposition that accounts for the gap: the named drivers sum "
                    "to %.2f against a gap of %.2f, so more than half of the "
                    "disagreement is unexplained" % (total, want))
    if name == "airtight":
        if not hunt_recorded:
            missing.append("a RECORDED exhaustive hunt for our own error [R-GAP-04]")
        if not (falsifier or "").strip():
            missing.append("a falsifier stated in advance")
    rec["missing"] = missing
    rec["verdict"] = "PASS" if not missing else "FAIL"
    return rec


def enforce(*a, **kw):
    """assess(), but a study that has not made its case does not issue."""
    rec = assess(*a, **kw)
    if rec["verdict"] != "PASS":
        raise NorthernStarError(
            "%s: the central of %.2f sits %.1f%% BELOW the traded price of %.2f, which "
            "is the '%s' tier. %s\nMISSING: %s\n\nThe fix is NEVER to move the number "
            "toward the price. Find the defect, or say in the study that the case is "
            "not made."
            % (rec["ticker"] or "this study", rec["central"], 100 * -rec["gap"],
               rec["spot"], rec["tier"], rec["requirement"],
               "; ".join(rec["missing"])))
    return rec


# HOW A STUDY RECORDS ITS CASE. The gate reads THIS BLOCK from the numbers file and
# nothing else -- deliberately, and it is the whole point. Every study below the
# price already argues its case somewhere in its prose, at length and often well.
# Prose is exactly what a gate cannot read, cannot count, and cannot tell apart
# from a paragraph that sounds like a case and establishes nothing. So the claim
# is made STRUCTURALLY, in the study's own committed numbers, where it can be
# checked, and the prose then explains what the block asserts.
#
# It is not paperwork. Writing the decomposition forces the question the principal
# actually asked -- if the market is wrong, WHERE is it wrong and by how much per
# share -- and a gap that cannot be decomposed is a gap nobody has understood yet.
STAR_CASE = dict(
    case="What the market appears to be pricing that this model is not, in the "
         "study's own words. A sentence that names a mechanism, not a mood.",
    decomposition="{driver: currency per share}. Must account for at least half of "
                  "the gap, or the study is saying most of its disagreement with "
                  "the market is unexplained -- which may be true, and then it is "
                  "the finding rather than the case.",
    hunt_recorded="True only where an exhaustive search for OUR OWN error has been "
                  "run and RECORDED [R-GAP-04]. Not 'we looked'.",
    falsifier="Stated in advance: what would have to happen for this study to be "
              "the one that is wrong.",
)


def from_numbers(ticker, numbers=None, **kw):
    """Assess a study from its committed numbers file.

    The study's own `star_case` block supplies the case unless the caller overrides
    it. A study with no such block is assessed as having made no case, which is the
    honest reading: an argument a gate cannot find is an argument that is not there
    as far as anything downstream is concerned [R-ENF-04].

    A TWO-SIDED CENTRAL IS ASSESSED ON BOTH BRANCHES AND NEVER COLLAPSED. Four
    studies in this book carry `central = None` and a `central_two_sided` record,
    because their single most consequential contested judgement is computed both
    ways and published side by side rather than averaged -- which is the standing
    depth requirement, not an omission. Averaging them here to get one number to
    compare with the price would do inside a gate exactly what the study refuses
    to do on the page. So each branch gets its own bar, and the study's obligation
    is the HARDEST of them: if either reading says the market is overpaying, that
    reading needs its case.
    """
    if numbers is None:
        p = os.path.join(HERE, "%s_study" % ticker.lower(), "study_numbers.json")
        with open(p) as fh:
            numbers = json.load(fh)
    # THE NORTHERN STAR IS THE LATEST TRADED PRICE, NOT THE ONE THE STUDY WAS
    # STRUCK AT. They are different dates by construction [R-DOC-03] and a study
    # is not re-struck every time the market moves. But the bar this rule sets is
    # a claim about what investors ARE paying, and a stale quote makes that bar
    # EASIER to clear — which is precisely the wrong direction for a rule about
    # burden of proof. Where the price library holds a later close than the study,
    # the later one is used and both are recorded.
    sc = numbers.get("star_case") or {}
    for k in ("case", "decomposition", "hunt_recorded", "falsifier"):
        if k in sc and k not in kw:
            kw[k] = sc[k]
    spot = numbers.get("spot")
    struck = spot
    latest, latest_date = _latest_close(ticker)
    if latest and (not spot or latest != spot):
        spot = latest
    central = numbers.get("central")
    if central is not None:
        r = assess(central, spot, ticker=ticker, **kw)
        r["spot_struck"], r["spot_latest"], r["spot_latest_date"] = struck, latest, latest_date
        return r

    two = numbers.get("central_two_sided") or {}
    branches = two.get("branches") or []
    if not branches:
        raise NorthernStarError(
            "%s carries neither a central nor a two-sided central record. An absent "
            "central is not a passing one [R-ENF-04]: a study with no answer cannot "
            "be held to the price it disagrees with." % ticker.upper())
    out = []
    for b in branches:
        v = b.get("value")
        if v is None:
            raise NorthernStarError(
                "%s: a branch of the two-sided central (%r) carries no value"
                % (ticker.upper(), b.get("label")))
        r = assess(v, spot, ticker=ticker, **kw)
        r["branch"] = b.get("label")
        out.append(r)
    order = {n: i for i, (_, n, _) in enumerate(BANDS)}
    hardest = max(out, key=lambda r: order.get(r["tier"], 0))
    return dict(rule="R-STAR-01", ticker=ticker.upper(), spot=spot,
                two_sided=True, branches=out, tier=hardest["tier"],
                requirement=hardest.get("requirement"), central=hardest["central"],
                gap=hardest["gap"], direction=hardest["direction"],
                verdict="PASS" if all(r["verdict"] == "PASS" for r in out) else "FAIL",
                note="Both branches assessed; the obligation is the hardest of them. "
                     "They are never averaged into one number to compare with a price.")


if __name__ == "__main__":
    for tk in (sys.argv[1:] or ["SWDY"]):
        try:
            r = from_numbers(tk)
        except Exception as e:
            print("%-6s RED: %s" % (tk.upper(), str(e)[:110]))
            continue
        tag = " (two-sided, hardest branch)" if r.get("two_sided") else ""
        print("%-6s central %8.2f vs spot %8.2f  %+6.1f%%  tier=%-8s %s%s"
              % (r["ticker"], r["central"], r["spot"], 100 * r["gap"], r["tier"],
                 r["verdict"], tag))
        for b in r.get("branches", []):
            print("         %-52s %8.2f  %+6.1f%%  %s"
                  % (str(b.get("branch"))[:52], b["central"], 100 * b["gap"],
                     b["verdict"]))
