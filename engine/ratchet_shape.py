"""[R-ENF-08] — a ratchet excuses the failure it RECORDED, not every failure of its class.

FOUND BY THE INJECTION HARNESS ON ITS FIRST RUN, which is the argument for that harness.
A stale-landbank error was planted in PHDC — the very study [R-ASSET-01] was adopted on —
the mutation landed, the gate ran, and the gate DID NOT GO RED. It was right not to by its
own construction: PHDC is on the asset-base ratchet, and a ratchet entry is a TICKER, so
the gate skips that study entirely.

SO EVERY RATCHET IN THIS REPOSITORY IS ALSO A BLIND SPOT. A study listed for one known
defect is excused from its whole gate, and can acquire a SECOND, DIFFERENT defect of the
same class with nothing to catch it. That is not a defect in any ratchet — each was seeded
correctly and each may only shorten — it is a property of what a ratchet ENTRY IS, and
[R-ENF-02] never said otherwise because nobody had asked.

THE FIX IS NOT TO REMOVE THE RATCHETS. [R-ENF-02] exists because a check that is red from
the day it is written is one everybody learns to ignore, and that reasoning is untouched.
What changes is the GRANULARITY: an entry excuses ONE FAILURE, named, and a DIFFERENT
failure on the same study is a NEW breach.

THE COMPARISON IS ON SHAPE, NOT ON TEXT, and that decision is forced rather than chosen. A
gate's failure message carries live figures — a date, a gap in per cent, a basis-point
difference — so an exact-string match would go red every time a price moved, which is the
permanently-red check [R-ENF-02] forbids. Stripping the numbers leaves the CLAIM, which is
the thing the ratchet was seeded against: "asset base as at DATE is BEHIND the information
set ending PERIOD" is one failure however the dates move; "asset_base_record is missing
disclosure" is a different one and must go red.

WHAT IT DELIBERATELY DOES NOT DO: it does not require an entry to carry a signature. An
entry with none behaves exactly as before — excusing the study — because retro-fitting
signatures onto 47 ratchets is a re-issue and a rule that made every existing list red is
the permanently-red check this repository forbids. It BINDS FORWARD: a ratchet whose
entries carry signatures gets the finer check, and the two gates adopted today carry them.
"""
from __future__ import annotations

import re

# Anything that legitimately moves between two runs of the same gate on the same defect.
_NUM = re.compile(r"[-+]?\d[\d,]*\.?\d*(?:e[-+]?\d+)?", re.I)
_WS = re.compile(r"\s+")


def fingerprint(msg):
    """The CLAIM a failure message makes, with every live figure removed.

    Not a hash: a reader has to be able to look at a stored signature and see which
    failure it names, because a ratchet entry nobody can read is an entry nobody can
    close.
    """
    if not isinstance(msg, str):
        return ""
    t = _NUM.sub("#", msg)
    t = _WS.sub(" ", t).strip().lower()
    return t


def excused(entry, current):
    """Does this ratchet entry excuse THIS failure?

    Returns (excused, why_not). An entry with no signature excuses the study, as every
    ratchet in this repository did before this rule; an entry WITH one excuses only the
    failure it names.
    """
    if not isinstance(entry, dict):
        return True, None                      # a bare reason string: the old behaviour
    if "signature" not in entry:
        return True, None                      # predates this rule: the old behaviour
    sig = entry.get("signature")
    if not isinstance(sig, str) or not sig.strip():
        # AN ABSENT KEY AND AN EMPTY ONE ARE NOT THE SAME STATE, and this repository
        # already settled that everywhere else: [R-COC-01 AMENDED] on a re-pointed cost of
        # debt, [R-ASSET-01] on a not-restated declaration, [R-GAP-02] on a dissent — an
        # EMPTY reason has switched the check off rather than declared it. A missing key is
        # a ratchet that predates the rule; a blank one is somebody who started to fill it
        # in and stopped, which is the cheapest possible route back to the old blindness.
        return False, ("the ratchet entry carries an EMPTY signature. A missing signature "
                       "is an entry predating [R-ENF-08] and is excused; a BLANK one has "
                       "switched the check off rather than declared it")
    if not sig:
        return True, None
    want = fingerprint(sig)
    got = fingerprint(current)
    if want == got:
        return True, None

    # A FAILURE THAT HAS SHRUNK IS THE RATCHET WORKING, NOT A NEW BREACH.
    #
    # A message carries one clause per defect, separated by semicolons. Exact comparison
    # made PARTIAL REPAIR indistinguishable from a new defect: FERTIGLOBE's record was
    # listed as carrying "no rf_star, beta, erp or ke_exp"; it has since gained three of
    # the four, the gate correspondingly reports "no ke_exp", and the entry that was
    # written for the larger failure refused to excuse the smaller one. The study got
    # BETTER and went red for it, which makes the next improvement look like a cost.
    #
    # So a live failure whose clauses are all covered by the recorded ones is EXCUSED,
    # and a clause that is not covered is a NEW breach and is named. That is strictly
    # what the ratchet already promises -- it may only ever SHORTEN -- and it cannot be
    # used to hide anything: adding a defect adds a clause, and an added clause is red.
    def _clauses(t):
        return [c.strip() for c in t.split(';') if c.strip()]

    want_c, got_c = _clauses(want), _clauses(got)

    def _words(c):
        return set(re.findall(r"[a-z0-9_#]+", c))

    def _covered(c):
        # A clause is covered when it matches a recorded one exactly, or when every word
        # in it appears in a recorded one -- which is how "no ke_exp" relates to "no
        # rf_star, beta, erp or ke_exp". Substring containment does not work here: the
        # field list is not contiguous, so the shrunken clause is not a substring of the
        # larger one even though it names strictly less.
        #
        # COVERAGE IS TESTED IN ONE DIRECTION ONLY. A live clause may name less than a
        # recorded one; a recorded one may not be a subset of a live one, or a defect
        # that GREW would excuse itself. A new defect introduces a word the recorded
        # clause does not carry -- a field name, a construction, a rule id -- and an
        # uncovered word is red.
        cw = _words(c)
        return any(c == w or cw <= _words(w) for w in want_c)

    extra = [c for c in got_c if not _covered(c)]
    if not extra:
        return True, None
    return False, ("the ratchet excuses %r; the gate now reports a failure it does not "
                   "cover — %s. A defect a listed entry does not name is a NEW breach "
                   "[R-ENF-08]" % (sig[:90], '; '.join(e[:90] for e in extra)))

# A ratchet that records a MAGNITUDE needs a second test, because the shape of its failure
# message never changes. check_published_gap is the case: SABIC breaching at +10.8% and
# SABIC breaching at -60% produce the same sentence, so a fingerprint alone excuses both —
# which the injection harness demonstrated by planting the second and being ignored. An
# entry that records a deviation excuses a deviation UP TO THAT SIZE.

def worsened(entry, current_abs, tolerance):
    """Has a recorded deviation grown beyond what the ratchet excuses?

    Returns (is_new_breach, why). The tolerance is supplied by the caller and must be one
    the house already uses for that quantity — minting a second cutoff here would be the
    free parameter the PROMOTION RULE forbids.
    """
    if not isinstance(entry, dict):
        return False, None
    rec = entry.get("magnitude")
    if not isinstance(rec, (int, float)):
        return False, None
    if abs(current_abs) <= abs(rec) + tolerance:
        return False, None
    return True, ("the ratchet excuses a deviation of %.1f%%; it is now %.1f%%, beyond the "
                  "%.0f-point tolerance — a materially WORSE breach on a listed name is a "
                  "NEW breach [R-ENF-08]"
                  % (abs(rec) * 100, abs(current_abs) * 100, tolerance * 100))
