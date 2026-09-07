"""[R-REPAIR-01] — the repair recipes, and the post-conditions that make them safe.

A repair loop that guesses is worse than no repair loop, because its output looks like
work. So a recipe exists only where the GATE ITSELF has already done the arithmetic and the
repair is transcription — and even then it is not trusted, it is VERIFIED.

FOUR POST-CONDITIONS, EVERY ONE CHECKED, AND ANY FAILURE REVERTS BOTH EDITS:

  1. THE FIX GOES INTO THE GENERATOR, NEVER THE ARTEFACT. Writing a field straight into a
     committed numbers file makes the gate green and the next regeneration silently drops
     it. A repair that does not survive a rebuild is not a repair.
  2. THE REGENERATED ARTEFACT DIFFERS BY EXACTLY THE INTENDED FIELDS AND NOTHING ELSE.
     This is the one that matters: a generator is a program, and re-running it can move a
     date stamped from the clock, a figure that depends on today's price, anything. The
     diff is computed field by field and a single unexpected change reverts the whole
     repair. A precedent exists — one generator stamped its study date with the clock, so
     rebuilding restamped a delivered document's account of when the work was done.
  3. THE GATE THAT FAILED GOES GREEN. Not "the build passes": that gate, on that subject.
  4. NOTHING FORBIDDEN MOVED. Enforced by the loop, not by the recipe, so a recipe cannot
     opt out of it.

A recipe that cannot satisfy all four leaves the failure exactly as it found it and the
work order stands. FAILING TO REPAIR IS A NORMAL OUTCOME; repairing something and not
noticing what else moved is not.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

ENGINE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ENGINE)


# ------------------------------------------------------------------ helpers

def flatten(o, p=""):
    d = {}
    if isinstance(o, dict):
        for k, v in o.items():
            d.update(flatten(v, p + "." + str(k)))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            d.update(flatten(v, p + "[%d]" % i))
    else:
        d[p] = o
    return d


def numbers_path(repo, tk):
    d = os.path.join(repo, "engine", "%s_study" % tk.lower())
    for n in ("study_numbers.json", "numbers.json"):
        p = os.path.join(d, n)
        if os.path.exists(p):
            return p
    return None


def field_diff(before, after):
    """(added, removed, changed) as dotted field paths."""
    fa, fb = flatten(before), flatten(after)
    return (sorted(set(fb) - set(fa)), sorted(set(fa) - set(fb)),
            sorted(k for k in set(fa) & set(fb) if fa[k] != fb[k]))


# ------------------------------------------------------------------ recipes

class Recipe:
    gate = None
    name = None

    def matches(self, msg):
        raise NotImplementedError

    def plan(self, repo, subject, msg):
        """Return (generator_path, old_text, new_text, expected_added_fields) or None."""
        raise NotImplementedError


class DeclareKeTerminalConstruction(Recipe):
    """[R-COC-02]: the record must NAME the construction its terminal Ke was built under.

    The gate has already reproduced the figure and says in its own refusal which
    construction it reproduces under, and at what tax rate where it relevers. So the value
    is not inferred here — it is READ OUT OF THE GATE'S OWN MESSAGE. A recipe that solved
    for it independently would be a second implementation of the arithmetic [R-ENF-03], and
    a recipe that guessed would be the thing this loop must never do.
    """
    gate = "check_ke_reproduction.py"
    name = "declare-ke-terminal-construction"

    _SAME = re.compile(r"reproduces under 'same_beta'")
    _RELV = re.compile(r"reproduces under 'relevered' at an implied tax rate of "
                       r"([0-9.]+)%")

    def matches(self, msg):
        return ("names no construction" in msg
                and (self._SAME.search(msg) or self._RELV.search(msg)))

    def plan(self, repo, subject, msg):
        if self._SAME.search(msg):
            fields = {"ke_terminal_construction": "same_beta"}
        else:
            m = self._RELV.search(msg)
            if not m:
                return None
            # THE RATE IS TAKEN FROM THE GATE'S MESSAGE, WHICH SOLVED IT AS A DIAGNOSTIC —
            # and that is exactly why this branch does NOT auto-apply. A rate solved out of
            # the answer it explains is the reverse-engineered construction this house
            # prohibits; a person has to confirm it against the filings.
            return None

        sdir = os.path.join(repo, "engine", "%s_study" % subject.lower())
        gens = [p for p in sorted(os.listdir(sdir)) if p.endswith(".py")]
        hits = []
        for g in gens:
            path = os.path.join(sdir, g)
            try:
                src = open(path, encoding="utf-8").read()
            except Exception:
                continue
            for pat in (r"(\n(\s*)ke_terminal\s*=\s*[^\n,]+,)",
                        r"(\n(\s*)['\"]ke_terminal['\"]\s*:\s*[^\n,]+,)"):
                ms = list(re.finditer(pat, src))
                if len(ms) == 1:
                    hits.append((path, src, ms[0]))
        if len(hits) != 1:
            # AMBIGUOUS OR ABSENT IS NOT A REPAIR. Two candidate sites means a person has
            # to say which; none means the record is not built where this recipe looks.
            return None

        path, src, m = hits[0]
        indent = m.group(2)
        key = ("ke_terminal_construction='same_beta',"
               if "=" in m.group(1).split("ke_terminal")[1][:3]
               else '"ke_terminal_construction": "same_beta",')
        insert = (m.group(1) + "\n" + indent
                  + "# [R-COC-02]: the record NAMES the construction its terminal cost of\n"
                  + indent + "# equity was built under. Added by the repair loop from the\n"
                  + indent + "# gate's own reproduction, not inferred here.\n"
                  + indent + key)
        return (path, m.group(1), insert,
                ["cost_of_capital_record.ke_terminal_construction",
                 "coc_record.ke_terminal_construction",
                 "wacc_record.ke_terminal_construction",
                 "wacc.cost_of_capital_record.ke_terminal_construction"])



class RegenerateForModuleField(Recipe):
    """The safest repair there is: RUN THE GENERATOR AGAIN AND CHANGE NO CODE.

    When a shared module grows a record field — engine/cost_of_capital.py gained
    ke_terminal_construction under [R-COC-02] — every study that takes its record FROM that
    module is one regeneration away from conforming, and studies that build the record by
    hand are not. The first draft of the sibling recipe assumed the second case and
    declined on all five studies of the first, which is the more common shape: three of the
    six carry no ke_terminal assignment anywhere in their own code because they never
    wrote one.

    THIS RECIPE EDITS NOTHING. It re-runs the generator and holds the result to the same
    four post-conditions, which means the entire risk is the one that always existed —
    that a generator does something else when it runs — and that risk is what post-condition
    2 exists to catch. It is the repair with the smallest possible surface.
    """
    gate = "check_ke_reproduction.py"
    name = "regenerate-for-module-field"

    def matches(self, msg):
        return ("names no construction" in msg
                and "reproduces under 'same_beta'" in msg)

    def plan(self, repo, subject, msg):
        sdir = os.path.join(repo, "engine", "%s_study" % subject.lower())
        if not os.path.isdir(sdir):
            return None
        # The generator is the script that WRITES the numbers file. Named by convention,
        # and both conventions in this book are tried rather than one guessed at [L-355].
        for cand in ("build_numbers.py", "compute.py"):
            path = os.path.join(sdir, cand)
            if os.path.exists(path):
                # It must actually take the record from the module, or regenerating
                # cannot pick the field up and this is the wrong recipe.
                src = open(path, encoding="utf-8").read()
                if "cost_of_capital" not in src:
                    continue
                if re.search(r"\bke_terminal\s*=", src):
                    # It builds the record by hand; a regeneration will not add the field
                    # and the sibling recipe is the right one.
                    continue
                return (path, None, None,
                        ["cost_of_capital_record.ke_terminal_construction",
                         "coc_record.ke_terminal_construction",
                         "wacc_record.ke_terminal_construction",
                         "wacc.cost_of_capital_record.ke_terminal_construction"])
        return None


# WHAT THE FIRST FIX RUN FOUND, AND IT IS THE POST-CONDITION EARNING ITS PLACE RATHER THAN
# A DEFECT. Regenerating PHDC and TMGH picks up the ke_terminal_construction field AND moves
# standard_version from 2026.09.01 to 2026.09.07, because [R-STD-01]'s version was bumped
# the same day. Both changes are correct; they are not the same DECISION. A repair loop that
# let a version bump ride along under a one-field fix would be deciding, silently, that
# every study it touched is now built to today's standard — which is a re-issue and a
# person's call. So the repair reverts and the work order stands, saying exactly what moved.
#
# The temptation is to declare standard_version an expected co-change and move on. That is
# the widening this house forbids: the post-condition exists precisely to catch a rebuild
# doing more than the repair intended, and the first time it fires is not the time to relax
# it. A REPAIR THAT ALSO RE-STAMPS A STUDY'S STANDARD IS A RE-ISSUE, NOT A REPAIR.
#
# STC declined for a different and equally honest reason: its record is written by
# diagnostics_stc.py, which is neither of the two generator names this recipe knows. That is
# L-355 — a reader that guesses a naming convention finds nothing — reported rather than
# papered over, because the alternative is a recipe that runs whatever script it finds.

RECIPES = [RegenerateForModuleField(),
           DeclareKeTerminalConstruction()]


def find_recipe(gate, msg):
    for r in RECIPES:
        if r.gate == gate and r.matches(msg):
            return r
    return None


# ------------------------------------------------------------------ the attempt

def attempt(repo, gate, subject, msg, run_gate, log=print):
    """Try one repair. Returns (repaired, note). Reverts everything on any surprise."""
    recipe = find_recipe(gate, msg)
    if recipe is None:
        return False, "no recipe: this failure is not one a gate has already solved"

    planned = recipe.plan(repo, subject, msg)
    if planned is None:
        return False, ("recipe %s declined — either the fix needs a figure a person must "
                       "confirm against the filings, or the site it would edit is not "
                       "unique. A refusal a reader cannot act on is half a refusal, so "
                       "this says which case applies rather than only that one does."
                       % recipe.name)
    gen_path, old, new, expected = planned

    npath = numbers_path(repo, subject)
    if not npath:
        return False, "no committed numbers file to verify against"
    before_gen = open(gen_path, encoding="utf-8").read()
    before_num = open(npath, "rb").read()
    before_doc = json.loads(before_num.decode("utf-8"))

    def revert(why):
        open(gen_path, "w", encoding="utf-8").write(before_gen)
        open(npath, "wb").write(before_num)
        return False, why

    if old is not None:
        if before_gen.count(old) != 1:
            return False, "anchor is not unique in %s" % os.path.basename(gen_path)
        open(gen_path, "w", encoding="utf-8").write(before_gen.replace(old, new, 1))

    r = subprocess.run([sys.executable, os.path.relpath(gen_path, repo)],
                       cwd=repo, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        return revert("the generator failed to run after the edit: %s"
                      % (r.stderr or "")[-160:])

    try:
        after_doc = json.load(open(npath, encoding="utf-8"))
    except Exception as e:
        return revert("the regenerated numbers file will not parse: %s" % e)

    added, removed, changed = field_diff(before_doc, after_doc)
    unexpected = [a for a in added if not any(a.endswith("." + e.split(".")[-1])
                                              for e in expected)]
    if removed or changed or unexpected:
        return revert("POST-CONDITION 2 FAILED — the rebuild moved more than the intended "
                      "field: %d added unexpectedly, %d removed, %d changed (%s)"
                      % (len(unexpected), len(removed), len(changed),
                         ", ".join((unexpected + removed + changed)[:3])))
    if not added:
        return revert("the rebuild added nothing; the field did not reach the record")

    rc, out = run_gate(gate)
    if rc != 0 and subject in out:
        return revert("the gate is still red on %s after the repair" % subject)

    return True, ("repaired: %s, adding %s" % (recipe.name, ", ".join(added)))
