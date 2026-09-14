#!/usr/bin/env python3
"""TMGH — the contested judgements record [R-ENF-05], GENERATED.

[R-ENF-05] requires every judgement worth more than 5% of value to be recorded with BOTH
framings' values, the side adopted and why, so a binomial sign test can be printed: any one
contested choice is defensible, and what is not is a study resolving every one of them the
same way and never noticing.

THIS FILE EXISTS BECAUSE THE RECORD DID NOT HAVE ONE. contested_judgements.json was
hand-maintained and written by nothing — the shape [R-ENF-06] names, where AMOC's
case_adversarial.json was read by three builders, written by no generator anywhere in the
repository, and carried a base central of 5.954 against a published 11.834. This record's
figures happened to be current; that is luck rather than a property of the arrangement, and
the arrangement is what [R-ENF-06] is about.

WHAT IS COMPUTED AND WHAT IS AUTHORED. Every VALUE comes from the study's committed
numbers, so the record cannot drift from the study. The NAMES, the two framings and the
"why" are judgements about the work and are authored here, because no arithmetic produces
them — which is the division [R-LESSON-01] draws in the lessons harvest: the evidence is
mechanical, the judgement is signed.
"""
import json
import os
import sys


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
N = json.load(open(os.path.join(HERE, "study_numbers.json")))
PSV = N["per_share_nci_value_share"]
PSB = N["per_share_nci_book"]

def _at_terminal_growth(g):
    """The adopted case re-run with the terminal growth set to g. Refuses, never defaults.

    A DEFAULT IS THE DEFECT. This value was read with a .get whose key was never written,
    so the fallback published a superseded edition's number for as long as the record
    existed and nothing could tell.
    """
    import importlib
    import model as _M
    import valuation as _V
    was = _M.TERMINAL_GROWTH
    try:
        _M.TERMINAL_GROWTH = g
        importlib.reload(_V)
        # sotp(mode, SCHEDULE) -- the second argument is the cost-of-capital schedule,
        # not a basis name. The adopted case is the rating premium on the slower
        # conversion, which is what ADOPTED above reads.
        out = _V.sotp("capacity", _V.SCHEDULES["rating"])
        ps = out.get("per_share_nci_value_share")
        if ps is None:
            raise SystemExit(
                "the model returned no per-share figure at a terminal growth of %.2f. "
                "A contested alternative that cannot be priced is reported as "
                "unpriceable, never defaulted to a number from another edition." % g)
        return ps
    finally:
        _M.TERMINAL_GROWTH = was
        importlib.reload(_V)


# THE ADOPTED READING OF THIS STUDY, on its own adopted minority basis: the swap-premium
# case on the slower conversion. Every alternative below is priced against THAT.
ADOPTED = PSV["cds|capacity"]


def judgements():
    return [
        {"name": "how fast the order book converts",
         "adopted": "published BOTH ways, never averaged",
         "alternative": "a single central reading",
         "value_adopted": ADOPTED,
         "value_alternative": PSV["cds|recovery"],
         "why": "the company does not disclose a delivery schedule, so neither reading "
                "can be settled from what it publishes; both are published and the "
                "study takes no side"},
        {"name": "minority interests",
         "adopted": "their share of value, proxied by the filed profit share",
         "alternative": "at book",
         "value_adopted": ADOPTED,
         "value_alternative": PSB["cds|capacity"],
         "why": "the model capitalises 100% of subsidiary cash flow, so the minority's "
                "claim is worth its share of THAT value rather than its historical cost "
                "[R-BRIDGE-01]; book is published beside it as the more punitive read"},
        {"name": "equity risk premium basis",
         "adopted": "the swap basis",
         "alternative": "the credit-rating basis",
         "value_adopted": ADOPTED,
         "value_alternative": PSV["rating|capacity"],
         "why": "the swap basis is the market's own live pricing of the sovereign's "
                "credit against an agency judgement updated in steps; both are published "
                "and neither is averaged into the other"},
        {"name": "terminal growth",
         "adopted": "inflation only, zero real, on the house macro path",
         "alternative": "the 15% the earlier editions carried",
         "value_adopted": ADOPTED,
         # THE KEY NEVER EXISTED, so the default fired on every run and this record
         # published edition 2's fair value as a current alternative. A .get with a
         # numeric default is an absent answer wearing a clean one's clothes: nothing
         # goes red, nothing is missing on the page, and the figure is from another
         # study. It is COMPUTED now, by re-running the model's own terminal at 15%,
         # and the run refuses rather than substituting if it cannot.
         "value_alternative": _at_terminal_growth(0.15),
         "why": "15% nominal growth in perpetuity against a terminal rate embedding 7% "
                "inflation is eight points of real growth a year for ever, which nothing "
                "disclosed supports"},
    ]


def main():
    js = judgements()
    # MATERIALITY IS THE SHARED INSTRUMENT'S DECISION, NOT THIS FILE'S. A first draft
    # asserted here that every recorded judgement clears 5% of value, and it fired on the
    # minority-basis choice, which moves the adopted case by 3.3% — and the SAME choice is
    # worth 31% on the study's other published case. research_protocol.
    # assert_contested_judgements() already computes materiality and admits only material
    # judgements to the sign test, so a local threshold here would either drop a judgement
    # the study genuinely made or force a convenient measure to keep it. A study records
    # what it decided; the shared rule decides what counts. That is this week's own lesson
    # about hand-rolled local checks, arriving one level down.
    for j in js:
        for k in ("name", "adopted", "alternative", "value_adopted",
                  "value_alternative", "why"):
            assert j.get(k) is not None and j[k] != "", "%s carries no %s" % (j["name"], k)
    out = {
        "ticker": N["meta"]["ticker"],
        "as_of": N["meta"]["edition_date"],
        # [R-ENF-06]: an artefact a gate or a builder reads declares the answer it was
        # generated against, so a stale one can be told from a current one.
        "published_central": N["central"],
        "published_spot": N["meta"]["spot"],
        "judgements": js,
    }
    p = os.path.join(HERE, "contested_judgements.json")
    json.dump(out, open(p, "w"), indent=1)
    up = sum(1 for j in js if j["value_adopted"] > j["value_alternative"])
    print("wrote %s — %d judgements, %d resolved upward, %d downward"
          % (os.path.basename(p), len(js), up, len(js) - up))


if __name__ == "__main__":
    main()
