"""A quantity held flat in nominal terms is a real-decline forecast, not the absence of one.

[R-MACRO-01] requires growth rates to be stored as (real, inflation-path id) and to
recompute to their nominal, *because a typed nominal rate is unfalsifiable -- nobody can
tell whether 12% meant inflation plus one point or inflation minus three*. A quantity
HELD FLAT is a typed nominal rate of zero. Its real component is minus whatever
inflation applies, and that is a forecast.

WHAT THIS MODULE REFUSES IS THE CLAIM, NOT THE CONSTRUCTION, and the distinction is the
whole of it. Holding a traded commodity price flat in dollars is a legitimate, common
and often sensible thing to do. Describing it as *"no forecast of a traded commodity
price is defensible"* is a FALSE STATEMENT ABOUT THE MODEL: the model is forecasting a
price that falls every year for ever, and a reader is told the opposite.

MEASURED 18-09-2026 ACROSS THE FOUR STUDIES THAT CARRY THE CONVENTION, and the split is
what makes this narrow enough to check:

    TWO NAME IT. One records EGP 3,664.2mn a year "flat in nominal terms, which is a
    REAL DECLINE across the window"; another that "holding earnings flat in NOMINAL
    terms while discounting at a NOMINAL rate is a" real-terms assumption, in its own
    diagnostics.

    TWO DENY IT. "held FLAT in dollars -- NO FORECAST OF IT IS DEFENSIBLE"; "Held FLAT
    in nominal dollars at US$530 a tonne ... no forecast of a traded commodity price is
    defensible".

THE TWO THAT NAME IT ARE THE CLEAN CASES AND THEY COME OUT OF THE BOOK. A control
testing only the denial would prove nothing about the studies that get it right.

THE COST OF THE DENIAL IS MEASURED ELSEWHERE AND IS NOT SMALL: closing the resulting
escalator wedge is worth +17.8% on one of the two and +68.7% on the other, and in both
the costs escalate at FULL domestic inflation while the revenue does not -- so the
manufactured margin decline is then reported as a finding.
"""
import re

# HELD FLAT, in the ways the book actually writes it [L-355].
# THE OBJECT SITS BETWEEN THE VERB AND THE ADVERB and the first draft's fixed list of
# objects (it / them / earnings / the <word>) missed the book's own sentence -- "Holding
# A TRADED COMMODITY PRICE flat rather than forecasting it". It matched in the real file
# only because another occurrence sat nearby, so the gate was right by accident and the
# negative control caught it on a fixture carrying the sentence alone. Widened to any
# short noun phrase carrying no sentence punctuation, which cannot cross a clause.
FLAT = re.compile(
    r'\bheld\s+flat\b|\bhold(?:ing|s)?\s+[^.;:!?]{0,48}?\bflat\b'
    r'|\bflat\s+in\s+(?:nominal|dollars|US\$|USD)\b|\bkept\s+flat\b', re.I)

# THE DENIAL: the claim that holding flat is not a forecast.
DENIAL = re.compile(
    r'no forecast[^.]{0,60}(?:is|are)\s+defensible'
    r'|expresses?\s+no\s+(?:view|opinion|forecast)'
    r'|(?:makes?|taking)\s+no\s+(?:view|forecast)\s+(?:on|of|about)'
    r'|rather than forecast(?:ing)? it'
    r'|the absence of a forecast'
    r'|we do not forecast it', re.I)

# THE DISCLOSURE that makes it honest: the real consequence, stated.
NAMED = re.compile(
    r'real[- ]terms?\s+(?:decline|fall|erosion|decay)|a\s+REAL\s+DECLINE'
    r'|declin\w+\s+in\s+real\s+terms|falls?\s+in\s+real\s+terms'
    r'|real\s+price\s+(?:decline|fall)|erodes?\s+in\s+real\s+terms'
    r'|in\s+real\s+terms[^.]{0,40}(?:declin|fall|erod)'
    r'|escalated\s+at\s+(?:US|foreign|dollar)\s+inflation'
    r'|flat\s+in\s+REAL\s+terms', re.I)

WINDOW = 400


def passages(text):
    """[(excerpt, why), ...] where a flat nominal path is called the absence of a forecast."""
    out, seen = [], set()
    t = text or ''
    for m in FLAT.finditer(t):
        lo = max(0, m.start() - WINDOW)
        seg = t[lo:m.end() + WINDOW]
        if NAMED.search(seg):
            continue                    # the real consequence is stated: honest
        d = DENIAL.search(seg)
        if not d:
            continue                    # held flat and claims nothing: out of scope
        key = lo // WINDOW
        if key in seen:
            continue
        seen.add(key)
        out.append((' '.join(seg.split())[:220],
                    'holds a quantity flat in nominal terms and calls it %r, which is a '
                    'claim about the model that is false: flat in nominal is a real '
                    'decline every year' % d.group(0)[:44]))
    return out
