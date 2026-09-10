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
    return False, ("the ratchet excuses %r; the gate now reports %r — a DIFFERENT failure "
                   "on a listed study is a NEW breach [R-ENF-08]" % (sig[:90], current[:90]))

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
