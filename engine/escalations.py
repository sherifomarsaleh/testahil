#!/usr/bin/env python3
"""The escalation register — every question that reaches the principal, and its cost.

[R-IND-01]. Adopted 3 September 2026, per instruction: *"when I say running
independently, I mean it ... Don't come to me with your problems. Sort it."*

WHY THIS EXISTS, MEASURED RATHER THAN ASSERTED. On the day it was adopted this
session did the same thing twice in three hours:

  (1) It asked the principal for the ten-year yield and policy-rate series they had
      ALREADY SUPPLIED that morning, because it read `main` and the answer sat on
      another session's branch. One `git branch -r` would have found it. The
      archive on main still said "the one thing I would ask you for" and nothing
      compared that sentence to the world.

  (2) It reported that all five re-issued studies were missing two of their four
      deliverables. Every file was on disk. The check had counted keys in a publish
      manifest that lists two by design — it modelled one artefact and reported on
      another.

Neither was a hard problem. Both were ESCALATIONS THAT SHOULD NEVER HAVE LEFT THE
ROOM, and Part H of the programme plan — which already said "never ask" — stopped
neither, because it set no bar for what must be exhausted first, and because prose
that binds nothing is advice.

WHAT THIS MODULE MAKES TRUE. A question reaching the principal is an artefact with
a required shape: the routes actually run and what each returned, the refs actually
searched, what was done in the meantime, the default that will be taken if no answer
comes, and the date that default fires. A gate reads it from outside.

AND THE PART THAT WOULD HAVE CAUGHT (1): an OPEN escalation names the condition
that would resolve it, and the gate RE-CHECKS that condition across every live ref
on every run. An escalation whose answer has arrived goes RED. The register cannot
sit there asking for something already given, because the thing that asks is also
the thing that is checked against reality.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REGISTER = os.path.join(HERE, "escalations.json")

REF_WINDOW_DAYS = 14      # a branch idle longer than this is not work in flight
MAX_REFS = 20             # caps the SEARCH, never the claim

# The ladder. Every rung is RUN, not recalled, before anything is escalated — and a
# rung whose outcome is quoted from a document rather than from a fresh run does not
# count, because a written outcome is a fact about the past.
LADDER = (
    "the artefact itself, opened — never a document, manifest or register that "
    "describes it",
    "the checkout, and then EVERY live ref: work in flight on another branch is "
    "work that exists",
    "a RE-RUN of any probe whose failure is being relied on — an empty result is "
    "first evidence that the probe did not run [R-ENF-04]",
    "every tool this environment actually provides, named in its own description — "
    "a headless browser defeats a JavaScript-rendered source, and declaring one "
    "impossible with the browser installed is a claim about the operator",
    "the repository's own history and registers, for whether the question was "
    "asked and ANSWERED before",
)

CLASSES = {
    "missing_data": "an official figure or filing that cannot be obtained from any "
                    "route (SIGCM clause 1). The only escalation class that is "
                    "purely an access problem.",
    "instruction": "a decision reserved to the principal — a standing-rule change, "
                   "a publish, a spend. Never a question the plan already answers.",
    "contradiction": "an instruction that conflicts with a standing rule, where "
                     "obeying either breaks the other.",
}

REQUIRED = ("key", "opened", "cls", "question", "routes", "refs_searched",
            "why_only_the_principal", "done_meanwhile", "default_if_no_answer",
            "default_date", "status", "resolves_when")


def load() -> dict:
    if not os.path.exists(REGISTER):
        return {"_": "the escalation register [R-IND-01]", "entries": []}
    return json.load(open(REGISTER, encoding="utf-8"))


def save(d: dict) -> None:
    json.dump(d, open(REGISTER, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def git(*a: str) -> str:
    try:
        r = subprocess.run(("git",) + a, cwd=ROOT, capture_output=True,
                           text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def live_refs() -> list:
    """Every ref that could carry an answer: the checkout and each branch ahead of main."""
    out = ["HEAD"]
    # Newest first, and capped: this repository carries hundreds of automated
    # review branches, and a search that took minutes is one nobody would run.
    # The cap is on the SEARCH, never on the claim — an escalation records how
    # many refs it actually reached, so a narrow search shows up as a narrow
    # search rather than as an absence [R-ENF-04].
    raw = git("for-each-ref", "--sort=-committerdate",
              "--format=%(refname:short)|%(committerdate:short)",
              "refs/remotes/origin")
    cutoff = (dt.date.today() - dt.timedelta(days=REF_WINDOW_DAYS)).isoformat()
    for line in raw.splitlines():
        if len(out) > MAX_REFS:
            break
        if "|" not in line:
            continue
        ref, when = line.rsplit("|", 1)
        if ref in ("origin/main", "origin/HEAD") or when < cutoff:
            continue
        if git("rev-list", "--count", "origin/main..%s" % ref) not in ("", "0"):
            out.append(ref)
    if git("rev-parse", "--verify", "origin/main"):
        out.append("origin/main")
    return out


def is_resolved(entry: dict) -> tuple:
    """Has the thing this escalation asks for arrived, on ANY live ref?

    THE POINT OF THE WHOLE MODULE. `resolves_when` names a file and a marker that
    appears in it only once the answer exists. The gate looks for that marker across
    every live ref, so an escalation cannot go on asking for something already given
    — which is exactly the failure of 3 September 2026.
    """
    rw = entry.get("resolves_when") or {}
    path, marker = rw.get("file"), rw.get("must_contain")
    if not path or not marker:
        return False, "resolves_when names no file and marker"
    for ref in live_refs():
        blob = git("show", "%s:%s" % (ref, path))
        if blob and marker in blob:
            return True, ref
    return False, "not present on any live ref"
