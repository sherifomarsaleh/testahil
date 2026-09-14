#!/usr/bin/env python3
"""Every judgement worth more than about 5% of value, priced BOTH WAYS, live.

WHY THIS EXISTS AS A SCRIPT. contested_judgements.json was hand-written and went two
editions stale: it carried `as_of 2026-09-02` and every `value_adopted` read EGP 17.1517
against a published central of 21.0897. Worse than the staleness, the ALTERNATIVES had
not been repriced either — the 12% terminal growth this study rejects was recorded at
EGP 21.00 a share, and against the current model it is worth 38.84. A record of what a
judgement COSTS, priced against a model two editions old, understates or overstates the
cost by whatever moved in between, and a reader counting the direction of the contested
choices is counting the wrong numbers.

A judgement whose alternative cannot be re-run is recorded as such, with the edition it
was last priced at. It is not dropped and it is not quietly carried forward.

    python3 engine/phdc_study/contested.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bottom_up_model as BU                                        # noqa: E402
import valuation_v2 as V                                            # noqa: E402
import edition as _ed                                               # noqa: E402
import cost_of_capital as COC                                       # noqa: E402

SCHED = V.SCHEDULES["cds"]
CFO = BU.CFO_MID if hasattr(BU, "CFO_MID") else V.REG["cfo_mid"]["value"] \
    if isinstance(V.REG.get("cfo_mid"), dict) else None


def _cfo_mid():
    N = json.load(open(os.path.join(HERE, "study_numbers.json")))
    return N["derived"]["cfo_mid"]


CFO_MID = _cfo_mid()
ADOPTED = V.run(CFO_MID, SCHED)["per_share"]


def flat_rate_schedule():
    """The first-year rate held for the whole window and the perpetuity."""
    rec = json.loads(json.dumps(
        json.load(open(os.path.join(HERE, "wacc_result.json")))["schedule"]["cds"]))
    flat = rec["forward_wacc"][0]
    rec["forward_wacc"] = [flat] * len(rec["forward_wacc"])
    rec["wacc_terminal"] = flat
    df, acc = [], 1.0
    for w in rec["forward_wacc"]:
        acc /= (1 + w)
        df.append(acc)
    rec["discount_factors"] = df
    return COC.Schedule.from_record(rec)


def short_window(n=5):
    """The same model read to year n, as the earlier editions carried it."""
    keep = V.ROWS[:n]
    saved = V.ROWS
    try:
        V.ROWS = keep
        return V.run(CFO_MID, SCHED)["per_share"]
    finally:
        V.ROWS = saved


def main():
    rows = [
        {"name": "the central lens",
         "adopted": "the cash-flow lens alone",
         "alternative": "the retired 45/15/20/20 blend of four lenses",
         "value_alternative": None,
         "alternative_priced_at": "the edition of 2 September 2026, EGP 10.9412",
         "why_not_repriced": "three of the four lenses in that blend were retired with "
                             "it and are not built by this model, so the alternative "
                             "cannot be run against the current numbers. The figure "
                             "beside it is what it was worth when it was retired, and "
                             "it is named as that rather than carried as current.",
         "why": "three of the four blended lenses value a developer on reported "
                "earnings and historical-cost book, which for a company whose worth "
                "sits in an undelivered order book measures a floor; and the weights "
                "had never cleared any out-of-sample test"},
        {"name": "the discount rate's shape",
         "adopted": "a rate that glides with the house Egyptian macro path",
         "alternative": "a flat rate held for the whole window and the perpetuity",
         "value_alternative": V.run(CFO_MID, flat_rate_schedule())["per_share"],
         "why": "holding a crisis-level rate to year fifteen and into perpetuity "
                "asserts that Egypt never normalises, while this study's own cost of "
                "debt already follows the disinflation path"},
        {"name": "the length of the explicit window",
         "adopted": "fifteen years, run until growth meets the terminal",
         "alternative": "five years, as the earlier editions carried",
         "value_alternative": short_window(5),
         "why": "a five-year window closes while deliveries are still compounding, so "
                "the terminal capitalises a growth rate the model never reached"},
        {"name": "terminal growth",
         "adopted": "the house Egyptian terminal at zero real growth",
         "alternative": "the 12% the earlier editions carried",
         "value_alternative": V.run(CFO_MID, SCHED, terminal_growth=0.12)["per_share"],
         "why": "12% nominal in perpetuity is above Egypt's own long-run nominal GDP "
                "in the same currency, which makes the company the economy eventually"},
        {"name": "the delivery path",
         "adopted": "the disclosed run of handovers, fading",
         "alternative": "the 15% run held flat across the window",
         "value_alternative": None,
         "alternative_priced_at": "the edition of 2 September 2026, EGP 32.5882",
         "why_not_repriced": "the fade is built into the model's own delivery ladder "
                             "rather than exposed as a parameter, so holding it flat "
                             "is a rebuild and not a re-run. Named as the edition it "
                             "was priced at.",
         "why": "the company's own handover record fades; holding the peak year flat "
                "for fifteen years is a claim about something it has not done"},
    ]
    for r in rows:
        r["value_adopted"] = ADOPTED
        if r.get("value_alternative") is not None:
            r["cost_of_the_judgement"] = r["value_alternative"] - ADOPTED
            r["share_of_value"] = abs(r["cost_of_the_judgement"]) / ADOPTED

    priced = [r for r in rows if r.get("value_alternative") is not None]
    up = sum(1 for r in priced if r["cost_of_the_judgement"] > 0)
    out = {
        "ticker": "PHDC",
        "as_of": _ed.ISO,
        "central_adopted": ADOPTED,
        "generated_by": "engine/phdc_study/contested.py — never hand-edited",
        "direction_count": {
            "priced": len(priced),
            "alternative_worth_more": up,
            "alternative_worth_less": len(priced) - up,
            "note": "a study resolving every contested choice the same way is how a "
                    "lean survives an audit of its steps. This is a flag and not a "
                    "failure.",
        },
        "judgements": rows,
    }
    json.dump(out, open(os.path.join(HERE, "contested_judgements.json"), "w"), indent=1)
    print("contested_judgements.json — central %.4f, %d of %d alternatives repriced"
          % (ADOPTED, len(priced), len(rows)))
    for r in rows:
        v = r.get("value_alternative")
        print("  %-34s %s" % (r["name"][:34],
                              ("%9.4f  (%+.1f%%)"
                               % (v, 100 * r["cost_of_the_judgement"] / ADOPTED))
                              if v is not None else "not re-runnable; see the record"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
