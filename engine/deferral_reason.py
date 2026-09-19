"""[R-REBUILD-01 CLAUSE TWO] A deferral is a decision with a measurement, never a rule.

The clause was adopted 18-09-2026 on AMOC's own forecast-anchor record, which gives
[R-VCAL-01]'s one-lever-at-a-time guard as the reason a correction worth +55% is not
applied. THAT GUARD DOES NOT GOVERN CORRECTIONS. It governs LEVERS PROMOTED FROM THE
VALUATION CALIBRATION -- candidates seeking evidence -- and [R-REBUILD-01] says in its
own words that a study wrong in six ways moves a long way when all six are fixed, and
that what is forbidden is the move being INVISIBLE rather than the move being large.

MEASURED THE SAME DAY THE CLAUSE WAS ADOPTED, the misreading had reached six places in
four studies and a ratchet, and EVERY ONE OF THEM DEFERRED A CORRECTION THAT RAISES
THE VALUE. That asymmetry is the finding: an interpretation that always runs one way
is not an interpretation, it is a lean with a citation.

WHAT THIS MODULE DECIDES, AND WHAT IT DELIBERATELY DOES NOT:

    it decides whether a passage gives the guard AS THE REASON something was not done.
    it does NOT decide whether the deferral was wise.

Sequencing real work is a real judgement and the clause says so. What a record may not
do is dress that judgement as a prohibition, because a rule cited as a reason is not
checked the way a number is -- believed by the study that wrote it, by the digest that
repeated it, and by every reader since.

TWO STRENGTHS, ON PURPOSE. A committed RECORD (a ratchet entry, a study's own numbers)
is where the clause binds and is a hard refusal. A builder COMMENT is prose in code: it
teaches the next reader the wrong reason and it is not a record, so it is MEASURED and
REPORTED and never a bar -- the prose_figures architecture, for the same reason.
"""
import re

# The guard, named any of the ways the book actually names it. Read off the tree
# rather than imagined [L-355].
GUARD = re.compile(r'(\[R-VCAL-01\][^.]{0,40}(guard|one-lever)|one[- ]lever[- ]at[- ]a[- ]time'
                   r'|promotion guard|levers? (?:are|is) taken one at a time'
                   r'|one (?:lever|correction) at a time)', re.I)

# THE SAME REASON WITHOUT THE RULE'S NAME, AND IT IS THE WORSE FORM [added 18-09-2026,
# on AMOC's own model, hours after the guard citations were corrected]. That model
# declines a correction its own text says the standing rule PREFERS and the like-for-like
# test SUPPORTS, and the reason it gives is:
#
#     "a second would land +30.5%, CROSSING FROM ONE SIDE OF THE PRICE TO THE OTHER in a
#      single pass. Levers are taken one at a time and stop at the crossing"
#
# [R-VCAL-01]'s stop rule is about the POOLED BIAS of the valuation calibration crossing
# zero across the book. It is not about one study's distance from one quote. Applying it
# to a single name's gap makes THE PRICE the thing the correction must not pass, which is
# the reverse-engineering this house prohibits outright — arriving as a reason for
# INACTION rather than action, and therefore invisible to every gate that watches for a
# value being moved toward a quote. A value withheld from crossing a price is the same
# offence facing the other way.
PRICE_TARGET = re.compile(
    r'(cross(?:ing|es)? (?:from one side of )?the price|cross(?:ing|es)? the (?:price|spot)'
    r'|stop at the crossing|from one side of the price to the other'
    r'|would (?:land|take|put) (?:it|the study|this study) (?:above|below) (?:the )?'
    r'(?:price|spot))', re.I)

# A DEFERRAL: the passage says the thing was not done, or was put to another pass.
DEFERRED = re.compile(
    r'\b(not (?:simply |then |therefore )?(?:re-?anchored|taken|applied|corrected|done|moved|'
    r'fixed|changed)|neither is taken|left to the [a-z-]+ pass|belongs to (?:that|another) pass'
    r'|withheld|deferred|registered (?:here )?(?:and|rather than)|stays on the [a-z-]+ ratchet'
    r'|not (?:be )?stacked|is not lifted|are not (?:taken|applied)'
    r'|IT IS NOT TAKEN HERE|not taken here|PRICED, NOT ADOPTED|left for the next edition'
    r'|left for a (?:later|future) edition)\b', re.I)

# CORRECT USES THAT MUST NOT FIRE, and they are ordinary: a record may EXPLAIN what the
# guard is, quote it as an analogy, or record that this very misreading was corrected.
# The first draft fired on engine/gbco_study/rebuild_levers.py, whose docstring opens by
# explaining [R-REBUILD-01] BY the guard -- which is the rule's own reasoning, correctly
# stated, in the ledger the rule created.
DESCRIBES = re.compile(
    r'(is explicit about stacking|the same shape and was governed by nothing'
    r'|governs \*{0,2}levers|does not govern|CORRECTED|that reason is false'
    r'|stays symmetric|is symmetric|guard exists|R-REBUILD-01\] ?(clause two)?'
    r'|what that guard governs|not what that guard|never corrections'
    r'|\bwas false\b|it read [\u2018\']|is an OUTCOME and is not a reason'
    r'|is not a reason either way|THE HONEST REASON IS)', re.I)

WINDOW = 320      # characters either side; about two sentences of this prose


def passages(text):
    """[(excerpt, why), ...] where a deferral is given a reason the rules do not supply.

    Two shapes, and the second is the worse one: the guard cited by name, and the
    guard's stop rule applied to a SINGLE STUDY'S DISTANCE FROM ITS PRICE.
    """
    out, seen = [], set()
    t = text or ''
    for pat, label in ((GUARD, 'gives the promotion guard as the reason for %r'),
                       (PRICE_TARGET,
                        'gives CROSSING THE PRICE as the reason for %r -- the price as '
                        'a target, in the direction of inaction')):
        for m in pat.finditer(t):
            lo = max(0, m.start() - WINDOW)
            seg = t[lo:m.end() + WINDOW]
            if DESCRIBES.search(seg):
                continue
            d = DEFERRED.search(seg)
            if not d:
                continue
            key = (lo // WINDOW, label[:20])
            if key in seen:
                continue
            seen.add(key)
            out.append((' '.join(seg.split())[:220], label % d.group(0)))
    return out
