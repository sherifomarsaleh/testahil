"""[R-LESSON-02] Whether a lesson reaches the layer that binds, declared and checked.

[R-LESSON-01] is explicit that the register BINDS NOTHING: no standing rule refers
to it and no QC gate consults it, and every fundamental walk-forward lesson stays
PROVISIONAL until the method is validated across more names. That is right and this
module does not change it. A lesson is prose, a scope judgement and an evidence
clause; enforcing prose is not available, and a register that can turn the build red
is a register people stop writing to honestly.

WHAT IS MISSING IS NOT A GATE ON THE REGISTER. IT IS THAT NOBODY COUNTS THE
CONVERSION. Measured 18-09-2026 with the register's own machinery excluded from the
probe, 19 of 312 lessons reach the binding layer at all -- 6.1% -- and this house
already has the evidence for what that costs, in its own words: [L-048] and [L-055]
were both registered, both correct, and both re-violated by the studies delivered
after them. A lesson that could have been made arithmetic and was not is a debt, and
until now it was a debt nobody could name, because nothing distinguished

    a lesson enforced by a rule          from
    a lesson that genuinely cannot be    from
    a lesson somebody meant to get to.

THE CLASSIFICATION IS DECLARED, NOT INFERRED, and that is forced rather than
preferred. "States a testable claim" is not decidable from prose: a classifier built
on keywords would be a free parameter with no evidence behind it, which the PROMOTION
RULE forbids, and it would be wrong in the direction that reads as a measurement --
the failure this book keeps finding. So the lesson declares, and the gate holds the
declaration to the world, which is [R-COC-02]'s shape exactly: make the construction
DECLARABLE and then require the declaration.

WHAT THIS GATE CHECKS, AND IT IS THE EASIER HALF -- SAID PLAINLY RATHER THAN IMPLIED
[R-ASSET-02]:

    it checks that a lesson claiming enforcement NAMES something that EXISTS.
    it does not, and cannot, check that the named thing BINDS THAT LESSON.

That second question is judgement, and a gate asserting it would be making a claim it
cannot support. The first question is still worth asking, because a named rule that
was retired, or a module that was deleted, leaves a lesson reading as enforced while
nothing enforces it -- which is [R-DOC-02]'s rot on a different artefact.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# CLOSED, for [R-COC-01 AMENDED]'s reason: an open list lets a lesson opt out by
# inventing a category, and "it is more of a principle really" is not a category.
PROMOTION = ("enforced", "prose", "outstanding")

_RULE_ID = re.compile(r'^\[R-[A-Z]+-\d+\]$')
_PATH = re.compile(r'^[\w./-]+\.(py|js|json|md)$')


def eligible(lesson):
    """Which lessons this rule governs, and why the others are out of scope.

    ALL scope, because a CLASS or STOCK lesson is a fact about one kind of company
    and enforcing it book-wide is the superstition [R-LESSON-01] names outright.

    ADOPTED status, because a PROVISIONAL lesson rests on one name and promoting it
    is precisely what the promotion rule forbids -- so demanding a promotion
    declaration on one would be asking a question whose only honest answer the rule
    already supplies. They are skipped rather than declared, and the gate says how
    many it skipped so the skip is visible rather than silent [R-ENF-04].
    """
    return lesson.get("scope") == "ALL" and lesson.get("status") == "adopted"


def resolve(by, doc_text):
    """Does the thing a lesson names actually exist? Returns (ok, how, detail).

    Two shapes are accepted and anything else is RED rather than skipped, because an
    unrecognised reference is an absent answer in a clean answer's clothes.
    """
    if not by or not str(by).strip():
        return (False, "empty", "declared enforced and names nothing")
    by = str(by).strip()
    if _RULE_ID.match(by):
        # One document is enough here: check_protocol_sync already holds the two to
        # each other, and a gate re-deriving another gate's job is the [R-ENF-03]
        # species.
        return (by in doc_text, "rule",
                "" if by in doc_text else "names a rule id that resolves in neither "
                                          "governing document")
    if _PATH.match(by):
        p = os.path.join(ROOT, by)
        return (os.path.exists(p), "file",
                "" if os.path.exists(p) else "names a file that is not on disk")
    return (False, "unrecognised",
            "reference %r is neither a rule id nor a repository path" % by)


def classify(lesson, doc_text):
    """One lesson -> (state, detail). State is one of PROMOTION, or a failure name."""
    p = lesson.get("promotion")
    if p is None:
        return ("undeclared", "carries no promotion declaration")
    if p not in PROMOTION:
        return ("bad_value",
                "promotion %r is not one of %s -- the list is closed"
                % (p, ", ".join(PROMOTION)))
    if p == "enforced":
        ok, how, why = resolve(lesson.get("promoted_by"), doc_text)
        return ("enforced" if ok else "broken_reference", why or how)
    if p == "prose":
        why = (lesson.get("promotion_note") or "").strip()
        if not why:
            return ("empty_reason",
                    "declared prose with no reason -- an empty reason has switched "
                    "the check off rather than declared it")
        return ("prose", why)
    return ("outstanding", (lesson.get("promotion_note") or "").strip())
