"""Refuse to ship a valuation that does not make sense.  [R-SANITY-01]

ADOPTED 01-Sep-2026, per instruction — "Whenever you have nonsensical things
like that refer back to me. Also this is a rule that you should write and record
and implement."

WHY IT EXISTS.  TMGH's rebuild delivered a fair-value range of EGP 22.30-59.67
against a market price of EGP 97.80 and a prior published range centred on
147.12 -- a 73% cut that said the market was paying about two and a half times what the
company is worth.  Every gate in this repository passed it.  SIGCM passed, the
model-study checklist passed, the beta was conforming, the recalculation
reconciled to 84 checks, the external-reader scrub was clean.  NOT ONE OF THEM
ASKS WHETHER THE ANSWER IS SENSIBLE, because every one of them checks that the
arithmetic is faithful to the inputs and none checks the inputs against the
world.  A study can be perfectly self-consistent and absurd.

The two defects behind that number were both visible in the study's own outputs
and neither was flagged:

  * NEW SALES WERE MODELLED BELOW THE LAST ACTUAL AND THEN DECAYED.  FY2025
    actual new sales were EGP 382,200mn.  The projection opened at 300,000 and
    faded 15% a year to 96,173 by 2033 -- a nominal collapse in an economy
    running near 20% inflation, for a company whose order book was at a record.
    The fade was added to stop an earlier version's order book exploding; it
    over-corrected straight past sensible into the opposite error.
  * THE DISCOUNT RATE DISAGREED WITH THE MARKET BY TWELVE POINTS AND THE STUDY
    HAD ALREADY MEASURED THE GAP.  Its own reverse DCF put the market's implied
    rate at 23.09%; the model discounted at 35.79%.  That number was computed,
    printed, and not acted on.

THE CHECK IS NOT A THRESHOLD ON THE ANSWER.  A fair value far from the market
price is sometimes the whole point of doing the work, and a gate that forbade it
would be a gate that forbids finding anything.  What this refuses is shipping
such a number SILENTLY.  Every trip below returns a QUESTION FOR THE USER, and
the standing rule is that the question goes to them before the study is
delivered -- not into a caveats section, and not resolved by the model's own
author.  A study may still publish a number that trips a check; it may not
publish one nobody was told about.
"""

import os
import sys

# Each rule states what it compares and what a trip MEANS. The bands are wide on
# purpose: this is looking for absurdity, not for disagreement with the market.
# Set from the case that forced this rule rather than from taste. TMGH's central
# came out at 40.2% of spot -- a 0.40 cutoff MISSED IT BY TWO TENTHS OF A POINT,
# and a gate that does not catch the defect it was written for is decorative,
# which is exactly what [R-CAL-03] retired a test for being. 0.50 catches it with
# room, and still says only "the market is paying twice what we think it is
# worth" -- a claim worth a sentence to the user in any event.
SPOT_LOW = 0.50      # central below half of spot -> the market pays 2x+
SPOT_HIGH = 2.00     # central above 2x spot -> we think the market is half-price
PRIOR_MOVE = 0.50    # a rebuild that moves the central leg by more than half
IMPLIED_GAP = 0.05   # our discount rate vs the market's implied, in points
DRIVER_BELOW_ACTUAL = 1.00   # a year-1 driver set below the last reported year


class Question:
    """One thing that must be put to the user before the study is delivered."""

    def __init__(self, code, headline, detail, numbers):
        self.code, self.headline = code, headline
        self.detail, self.numbers = detail, numbers

    def __str__(self):
        return "[%s] %s\n      %s\n      %s" % (
            self.code, self.headline, self.detail,
            "  ·  ".join("%s %s" % (k, v) for k, v in self.numbers.items()))


def check(ticker, central, spot=None, prior_central=None, wacc=None,
          implied_rate=None, year1_drivers=None, last_actual_drivers=None,
          low=None, high=None):
    """Return the questions this valuation raises. Empty means none.

    `year1_drivers` and `last_actual_drivers` are dicts keyed the same way; any
    driver whose first projected year sits below the last REPORTED year is
    questioned, because that is a forecast of decline and must be a decision
    rather than a side effect of a guard added for another purpose.
    """
    qs = []

    if spot:
        if central < SPOT_LOW * spot:
            qs.append(Question(
                "BELOW-MARKET",
                "The valuation says the market is paying %.1f times what the "
                "company is worth." % (spot / central),
                "That is a large claim. It may be right, and it is the kind of "
                "thing this work exists to find -- but it is not shipped "
                "without being raised first.",
                {"central": round(central, 2), "spot": spot,
                 "ratio": round(central / spot, 2)}))
        elif central > SPOT_HIGH * spot:
            qs.append(Question(
                "ABOVE-MARKET",
                "The valuation says the shares are worth %.1f times the market "
                "price." % (central / spot),
                "Before this is delivered, say what the market is missing and "
                "why we can see it.",
                {"central": round(central, 2), "spot": spot,
                 "ratio": round(central / spot, 2)}))

    if prior_central:
        move = (central - prior_central) / prior_central
        if abs(move) > PRIOR_MOVE:
            qs.append(Question(
                "MOVED-A-LOT",
                "The rebuild moves the published central value by %+.0f%%."
                % (100 * move),
                "A move this size is either a real correction worth stating "
                "plainly or a defect. It is never a detail.",
                {"before": prior_central, "after": round(central, 2),
                 "move": "%+.1f%%" % (100 * move)}))

    if wacc and implied_rate and abs(wacc - implied_rate) > IMPLIED_GAP:
        qs.append(Question(
            "RATE-DISAGREES",
            "Our discount rate is %.1f points from the rate the market implies."
            % (100 * abs(wacc - implied_rate)),
            "The study computed both. Either we can say why the market is "
            "wrong by that much, or the rate is doing the work the analysis "
            "should be doing.",
            {"ours": "%.2f%%" % (100 * wacc),
             "market implies": "%.2f%%" % (100 * implied_rate)}))

    if year1_drivers and last_actual_drivers:
        for k, v in year1_drivers.items():
            a = last_actual_drivers.get(k)
            if a and v < DRIVER_BELOW_ACTUAL * a:
                qs.append(Question(
                    "DRIVER-BELOW-ACTUAL",
                    "The first projected year of %s is below the last year the "
                    "company actually reported." % k,
                    "A forecast of decline has to be a decision someone made "
                    "and can defend, not a guard added for another purpose "
                    "that kept going.",
                    {"last actual": round(a, 1), "year 1": round(v, 1),
                     "change": "%+.1f%%" % (100 * (v - a) / a)}))

    if low is not None and high is not None and low > 0 and high / low > 6.0:
        qs.append(Question(
            "RANGE-VERY-WIDE",
            "The published range spans %.1f times from low to high."
            % (high / low),
            "State plainly what a reader is meant to do with a range that "
            "wide, or narrow what drives it.",
            {"low": round(low, 2), "high": round(high, 2)}))

    return qs


def report(ticker, qs):
    if not qs:
        print("%s — sanity check: nothing to raise." % ticker)
        return 0
    print("\n%s — %d QUESTION%s FOR THE USER BEFORE THIS IS DELIVERED\n"
          % (ticker, len(qs), "" if len(qs) == 1 else "S"))
    for q in qs:
        print("  %s\n" % q)
    print("  [R-SANITY-01]: put these to the user. Do not resolve them alone "
          "and do not bury them in a caveats section.\n")
    return 1
