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


def interest_addback(mode):
    """The 15-year interest add-back, priced on each coherent footing.

    THE WEAKEST JOINT IN THIS MODEL, FOUND 17-09-2026 AND PRICED RATHER THAN TUNED.

    Free cash flow here is operating cash, plus the finance charge after tax, less
    maintenance capital expenditure. Operating cash is set as a SHARE OF REVENUE, measured
    on the three years the company has published a cash-flow statement. The finance charge
    is held at the FY2025 level, flat and nominal, for all fifteen years.

    Those two do not sit on the same footing, and the mismatch is measurable: the charge ran
    at 9.26% of revenue in FY2025 and the model holds it at a level that is 8.3% of revenue
    in 2026 and 1.4% by 2040, while the conversion rate it adjusts stays flat. Either debt
    is flat in nominal terms — in which case the interest drag inside operating cash falls
    away and the conversion rate should RISE across the window — or debt scales with the
    business, in which case the charge should scale and the conversion rate can stay flat.
    The model has taken the conservative half of each world.

    AND THE FIX IS NOT AVAILABLE, WHICH IS THE POINT. Because operating cash is exogenous,
    RAISING the modelled charge raises free cash flow: nothing falls when the charge rises.
    Putting the add-back on the revenue ratio — the internally consistent reading of world
    two — is worth +70% of the answer. A consistency correction worth seventy per cent that
    happens to raise the number is the shape of fitting, and this house does not publish it
    as a central. Whether the add-back belongs there at all depends on where PHDC presents
    interest paid in its cash-flow statement, and that statement is a scan this study has
    not read (see the cash-flow-detail gap). So the conservative construction is kept, the
    alternative is priced here, and the dependency is named in the study.
    """
    dc = COC.Discounter(SCHED)
    ratio = BU.REG["finance_cost_fy25"] / BU.REG["revenue_fy25"]

    def charge(r):
        return r["revenue"] * ratio if mode == "revenue_ratio" else r["interest"]

    pv = 0.0
    for i, r in enumerate(V.ROWS, start=1):
        fcff = (r["revenue"] * CFO_MID + charge(r) * (1 - BU.TAX)
                - r["revenue"] * 0.01)
        pv += fcff * dc.factor(i)
    last = V.ROWS[-1]
    tail = (last["revenue"] * CFO_MID + charge(last) * (1 - BU.TAX)
            - last["revenue"] * 0.01)
    pv_tv = dc.perpetuity_pv(tail, V.TG)
    ev = pv + pv_tv
    eq = ev - V.NET_DEBT + V.BS["investments_assoc"] + V.BS["investment_property"]
    return (eq - eq * V.NCI_SHARE) / V.SHARES


def nci_at(share):
    """The bridge on a different minority share of value; nothing else moves."""
    d = V.dcf(CFO_MID, SCHED)
    eq_gross = d["equity_before_nci"]
    return (eq_gross - eq_gross * share) / V.SHARES


def main():
    rows = [
        {"name": "the interest add-back's footing",
         "adopted": "the FY2025 finance charge, flat and nominal, for fifteen years",
         "alternative": "the same charge at its FY2025 share of revenue, scaling with "
                        "the business, which is what the flat conversion rate implies",
         "value_alternative": interest_addback("revenue_ratio"),
         "why": "operating cash is exogenous here, so raising the charge raises free cash "
                "flow and nothing offsets it. The conservative footing is kept BECAUSE "
                "the alternative is worth seventy per cent upward and a consistency "
                "correction that large in that direction is indistinguishable from "
                "fitting. Which footing is right depends on where the company presents "
                "interest paid, and its cash-flow statement is a scan this study has not "
                "read — so this is the study's largest unresolved construction, named "
                "rather than resolved in the direction that flatters it"},
        {"name": "the minority's share of value",
         "adopted": "the MEAN of the minority's filed profit share over FY2023-FY2025",
         "alternative": "the FY2025 share alone, as the superseded editions carried",
         "value_alternative": nci_at(BU.NCI_PROFIT_SHARE_FY25),
         "why": "a one-observation anchor is the construction this study refuses "
                "elsewhere, and the single year is also the branch that maximises equity "
                "value. Adopted on instruction of 17-09-2026 after an external audit "
                "priced the choice"},
        {"name": "the minority at book instead of at value",
         "adopted": "the minority's share of VALUE",
         "alternative": "its book share of equity on the 31-Mar-2026 sheet",
         "value_alternative": nci_at(BU.NCI_BOOK_SHARE_1Q26),
         "why": ("the model capitalises all of a subsidiary's cash flow, so the "
                 "minority's claim is worth its share of that value and not what it "
                 "historically cost. Published because an external audit named book as a "
                 "third basis, quoting 8.35 per cent, where this study's own 31-Mar-2026 "
                 "sheet gives %.2f per cent — the audit's figure for it is wrong"
                 % (100 * BU.NCI_BOOK_SHARE_1Q26))},
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
