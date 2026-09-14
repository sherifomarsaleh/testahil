"""What the known debt actually NEEDS — the question a work list does not answer.

The repair loop produces a ranked list of what is red or allowed-to-fail. That is the
first question. THE SECOND IS WHETHER ANY OF IT CAN BE AUTOMATED, and the honest answer
decides how much a repair loop is ever worth: a loop that could close most of it is
infrastructure, and one that could close a handful is a reporting tool with a small useful
corner.

FOUR CLASSES, AND THEY ARE NOT DEGREES OF DIFFICULTY — they are different KINDS of blocked:

  TRANSCRIPTION  the gate has already computed the answer and the fix is writing it down.
                 The only class a loop may ever close on its own [R-REPAIR-01].
  DATA           a figure has to come out of a filing. SIGCM clause 1 binds: a figure this
                 desk chose is not a disclosed figure, so no loop can supply it and no
                 amount of engineering changes that.
  JUDGEMENT      somebody has to decide something — which class a company is, which lens
                 carries the weight, whether a mechanism is real. A loop that decided these
                 would be doing the research rather than checking it.
  DECISION       the principal's, not the desk's — publishing, re-issuing, accepting a
                 stated cost.

THE POINT OF COUNTING THEM IS TO STOP OVER-PROMISING. "A framework that fixes what it
finds" is worth exactly what the transcription share is worth, and stating that share is
more useful than an automation plan that quietly assumes it is larger.

The rules are read off the failure text the gates emit, and a message that matches none of
them is UNCLASSIFIED rather than filed under the smallest class — an unclassified item is
an unanswered question, not a clean result [R-ENF-04].
"""
from __future__ import annotations

import re

RULES = [
    # (class, why, pattern)
    ("TRANSCRIPTION", "the gate names the value and the fix is one declared field",
     r"names no construction.*reproduces under '(same_beta)'"),
    ("DATA", "needs a figure out of a filing; SIGCM clause 1 forbids choosing one",
     r"no asset_base_record committed|states no information-set end date|"
     r"carries no rf_star, beta, erp or ke_exp|asset base as at .* is BEHIND"),
    ("DATA", "needs the record built from the statements",
     r"carries no cost-of-capital schedule record|carries no bridge record|"
     r"carries no macro record|carries no lens record|no walk-forward"),
    # A DERIVED FIGURE THAT DOES NOT REPRODUCE IS ARITHMETIC, NOT RESEARCH — the house
    # macro path already holds the inputs, so the study is one rebuild from agreeing with
    # it. It is still not TRANSCRIPTION: rebuilding a study moves more than one field, as
    # the first fix run demonstrated on standard_version, so a person prices the rebuild.
    ("JUDGEMENT", "a derived figure disagrees with the path it derives from; the rebuild "
                  "is arithmetic but moves more than one field",
     r"is not the derived|does not reproduce|against the derived|"
     r"terminal risk-free .* against"),
    # A CIRCULAR LENS IS A DESIGN CHOICE THE STUDY MADE. [R-LENS-03] forbids taking a
    # multiple from the current price; unpicking it is a valuation decision, not a fill-in.
    ("JUDGEMENT", "the lens architecture has to be re-decided, which is research",
     r"LENS FAIL|IS the traded multiple|is not permitted for"),
    # A CORRECTIONS LOG THAT DISAGREES WITH ITS OWN PRE-REGISTRATION cannot be reconciled
    # by anyone but whoever ran it — [R-FCAL-01] fixes the rule BEFORE the errors are
    # computed precisely so this cannot be settled afterwards by argument.
    ("JUDGEMENT", "a corrections log disagrees with its own pre-registration; only the run "
                  "that made it can reconcile that",
     r"applies corrections the pre-registered rule does not adopt|pre-registration|"
     r"the rule adopts .* and the log applies none"),
    ("JUDGEMENT", "a rate solved out of the answer must be confirmed against the filings",
     r"reproduces under 'relevered'"),
    # A MARKET WITH NO SOURCED PATH is [R-MACRO-01]'s own stop-and-inform: it raises
    # rather than falling back to a neighbour, and sourcing one is research.
    ("DATA", "the market has no sourced house macro path; [R-MACRO-01] refuses a fallback",
     r"is not a covered market|no sourced path|path is pending"),
    # A TWO-SIDED ANSWER is a study saying its value depends on a decision. Reconciling the
    # lens record to it means deciding how the two branches are declared, which is design.
    ("JUDGEMENT", "a two-sided answer whose lens record does not declare it; how the "
                  "branches are published is a design decision",
     r"TWO-SIDED answer|two-sided and its lens record"),
    ("DECISION", "needs a review written, or the corrected value published",
     r"no study directory, so nothing can carry a review|"
     r"study directory but no GAP_REVIEW|review .* audits|states no audited"),
    ("DECISION", "the principal's call on scope or publication",
     r"further entries the gate did not print"),
]


def classify(reason):
    for cls, why, pat in RULES:
        if re.search(pat, reason, re.I):
            return cls, why
    return "UNCLASSIFIED", ("no rule matches this failure text — an unclassified item is "
                            "an unanswered question, not a clean one [R-ENF-04]")


def triage(orders):
    out = {}
    for o in orders:
        cls, why = classify(o.get("reason", ""))
        out.setdefault(cls, []).append(dict(o, why=why))
    return out
