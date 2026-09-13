#!/usr/bin/env python3
"""ADIB — the contested judgements record, GENERATED. [R-ENF-05]

[R-ENF-05] requires every judgement worth more than about 5% of value to be recorded with
BOTH framings' values, the side adopted and why, so the direction of the contested choices
can be counted: any one of them is defensible, and what is not is a study resolving every
one the same way and never noticing.

THIS STUDY CARRIED NO SUCH RECORD AT ALL — check_output_records reported ADIB as carrying
neither a reverse read nor a contested-judgement record, which is the one state worse than
carrying a stale one: nothing to go stale, and nothing to count.

WHAT IS COMPUTED AND WHAT IS AUTHORED. Every VALUE comes from the study's own committed
sensitivity record, so the figures cannot drift from the study. The NAMES, the two framings
and the "why" are judgements about the work and are authored here, because no arithmetic
produces them.

    python3 engine/adib_study/contested.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edition as _ed                                                 # noqa: E402

N = json.load(open(os.path.join(HERE, "study_numbers.json"), encoding="utf-8"))
SENS = {s["driver"]: s for s in N["sensitivity"]}
ADOPTED = N["central"]


def at(driver):
    """The published value under one named sensitivity. Refuses rather than defaulting."""
    if driver not in SENS:
        raise SystemExit(
            "the sensitivity record carries no %r. A contested alternative that cannot be "
            "priced from the study's own record is reported as unpriceable, never "
            "defaulted to a number — which is how TMGH's record came to publish a "
            "superseded edition's fair value through a .get fallback on a key that never "
            "existed." % driver)
    return SENS[driver]["value"]


JUDGEMENTS = [
    {"name": "the asset yield through the rate cycle",
     "adopted": "the yield falls with the administered policy path",
     "alternative": "fifty basis points less of decline than the path implies",
     "value_alternative": at("asset yield +50bp"),
     "why": "this is the largest single lever in the study, and it is a claim about how "
            "fast a central bank finishing a disinflation lets lending rates fall. The "
            "path is the house one; holding the yield higher is a bet on the policy "
            "stance persisting"},
    {"name": "the cost of funds through the same cycle",
     "adopted": "deposit costs fall with the policy path",
     "alternative": "fifty basis points more of deposit cost than the path implies",
     "value_alternative": at("cost of funds +50bp"),
     "why": "the other half of the margin, and it moves the answer nearly as far. A bank "
            "whose asset yield falls faster than its funding cost is the compression this "
            "study forecasts; the alternative is that competition for deposits holds "
            "funding costs up"},
    {"name": "the cost of risk",
     "adopted": "the charge normalises toward the disclosed through-cycle rate",
     "alternative": "fifty basis points more of provisioning, held",
     "value_alternative": at("cost of risk +50bp"),
     "why": "the filings disclose the charge but not the vintage behind it, so a "
            "normalisation is a judgement rather than a reading"},
    {"name": "the financing growth path",
     "adopted": "the disclosed run, fading toward the terminal",
     "alternative": "five points a year less across the whole window",
     "value_alternative": at("financing growth -5pp/yr"),
     "why": "credit deepening in an economy whose private credit is about a quarter of "
            "GDP is real and it is also finite; the window's own end is the open item "
            "this study's macro record declares"},
]


def main():
    for j in JUDGEMENTS:
        j["value_adopted"] = ADOPTED
        j["cost_of_the_judgement"] = j["value_alternative"] - ADOPTED
        j["share_of_value"] = abs(j["cost_of_the_judgement"]) / ADOPTED
    material = [j for j in JUDGEMENTS if j["share_of_value"] >= 0.05]
    up = sum(1 for j in material if j["cost_of_the_judgement"] > 0)
    out = {
        "ticker": "ADIB",
        "as_of": _ed.ISO,
        "central_adopted": ADOPTED,
        "generated_by": "engine/adib_study/contested.py — never hand-edited",
        "direction_count": {
            "judgements": len(JUDGEMENTS),
            "material": len(material),
            "alternative_worth_more": up,
            "alternative_worth_less": len(material) - up,
            "note": "a study resolving every contested choice the same way is how a lean "
                    "survives an audit of its steps. This is a flag and not a failure: a "
                    "company can genuinely deserve a consistent read.",
        },
        "judgements": JUDGEMENTS,
    }
    json.dump(out, open(os.path.join(HERE, "contested_judgements.json"), "w"), indent=1)
    print("wrote contested_judgements.json — %d judgements, %d material, %d up / %d down"
          % (len(JUDGEMENTS), len(material), up, len(material) - up))
    for j in JUDGEMENTS:
        print("  %-38s %8.2f  (%+.1f%%)"
              % (j["name"][:38], j["value_alternative"],
                 100 * j["cost_of_the_judgement"] / ADOPTED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
