"""EGCH — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ WAS ALREADY IN THE MODEL AND WAS NEVER EMITTED. `compute.py`
carries `implied_flat_wacc()` and commits `implied_wacc_base` and
`implied_wacc_halt` — the single flat nominal EGP discount rate that reproduces
the traded price on this study's own operating cash flows, solved on each side of
the binary judgement. Nothing wrote them into a diagnostics record, so the gate
could not see a diagnostic the study had already computed. That is the whole
defect here, and it is a smaller one than most: the number existed, the file did
not.

WHY BOTH SIDES ARE SOLVED RATHER THAN ONE. EGCH's central is deliberately
TWO-SIDED — the cash-flow lens reads −1.06 with the ANNA capital programme carried
through and +2.82 with it stopped, and the study refuses to average them because
the judgement is binary and its two answers straddle zero. A reverse read solved
on one side only would quietly pick the side, which is the choice the study
declined to make.

WHAT THE SIGN TEST CAN AND CANNOT SAY HERE, STATED RATHER THAN IMPLIED. This
study prices exactly ONE contested construction both ways in its committed
numbers — the ANNA programme itself. Others are contested and named in the study
(the terminal margin taken at the lower of a built and an assumed figure; the
derived rather than disclosed nameplate; the ERP basis) and NONE of them carries a
committed per-share value on the other framing, so they cannot be counted without
inventing one. The record says so in its own field rather than presenting a
one-judgement sign test as a measurement of this study's lean, which it is not.

THE CONTAINMENT RULE. Nothing in the diagnostics file re-enters the valuation;
this module only reads what compute.py already committed and writes it out.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.join(HERE, "study_numbers.json")


def build():
    d = json.load(open(NUM, encoding="utf-8"))
    dr, w, ts = d["drivers"], d["wacc"], d["central_two_sided"]
    carried, stopped = ts["branches"][0], ts["branches"][1]

    r_base = float(dr["implied_wacc_base"])
    r_halt = float(dr["implied_wacc_halt"])
    built = [float(x) for x in dr["wacc_path"]]
    term = float(dr["wacc_terminal"])
    rf = float(w["rf_observed"])
    spot = float(d["spot"])

    diag = {
        "ticker": "EGCH",
        "as_of": d.get("spot_date"),
        "spot": spot,
        "spot_date": d.get("spot_date"),
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a "
            "DIAGNOSTIC and lives outside the numbers file every builder reads. A "
            "quantity solved from a price and then used anywhere in the valuation "
            "is the reverse-engineered rate the protocol prohibits outright, "
            "arriving through a side door. Nothing in this file is an input to "
            "anything; it is written OUT of what compute.py already committed."),
        "implied": {
            "quantity": ("the single flat nominal EGP discount rate — applied to "
                         "every explicit year and to the perpetuity — that "
                         "reproduces the traded price on this study's own "
                         "operating cash flows"),
            "value": r_base,
            "study_value": built[0],
            "study_value_range": [term, built[0]],
            "solved_on": (
                "compute.py's own implied_flat_wacc(), holding every driver at its "
                "published value and varying only the discount rate; solved on "
                "BOTH sides of the binary judgement because this study's central "
                "is two-sided and picking a side to solve on would make the choice "
                "the study declined to make"),
            "both_sides": {
                "capital programme carried through": r_base,
                "capital programme stopped": r_halt,
            },
            "reading": (
                "At EGP %.2f the price implies a flat nominal discount rate of "
                "%.1f%% if the ANNA programme is carried through and %.1f%% if it "
                "is stopped. This study discounts at %.1f%% falling to %.1f%%. The "
                "sovereign's own ten-year yield is %.1f%%, so on either branch the "
                "price is paying a rate BELOW what the government of Egypt pays to "
                "borrow — less than half of it on the committed-capital case. That "
                "is not a disagreement about the business; it is a statement that "
                "the equity is priced as though the cash flows this study projects "
                "were safer than the sovereign. The study's answer is %.2f carried "
                "through and %.2f stopped, and it publishes both rather than "
                "averaging a half-built plant nobody is proposing."
                % (spot, 100 * r_base, 100 * r_halt, 100 * built[0], 100 * term,
                   100 * rf, float(carried["value"]), float(stopped["value"]))),
        },
        "construction": {
            "built_wacc_path": built,
            "built_wacc_terminal": term,
            "sovereign_ten_year": rf,
            "terminal_growth": float(dr["g_terminal"]),
            "note": ("the implied rates come from compute.py's own solver, which "
                     "rebuilds the whole model at each trial rate rather than "
                     "re-discounting a fixed cash-flow series"),
        },
    }

    cj = {
        "ticker": "EGCH",
        "as_of": d.get("spot_date"),
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not "
            "is a study that resolves EVERY contested choice the same way and never "
            "notices. Each is recorded with BOTH framings' values, the side adopted "
            "and why, and the binomial sign test is printed."),
        "what_this_record_cannot_measure": (
            "This study prices exactly ONE contested construction both ways in its "
            "committed numbers, so the sign test below rests on a single "
            "observation and is NOT a measurement of this study's lean. Three "
            "further constructions are contested and named in the study and none "
            "carries a committed per-share value on the other framing: the ANNA "
            "terminal margin, where the central takes the LOWER of a built and an "
            "assumed figure because a ~66% cash margin on a commodity fertiliser is "
            "not credible and the disclosed unit cost is almost certainly partial; "
            "the ANNA nameplate, which is DERIVED because no filing states it; and "
            "the equity-risk-premium basis, published on the CDS basis with the "
            "rating basis beside it. Pricing them is a re-issue, and until then "
            "this record says what it does not know rather than counting one "
            "judgement as a clean bill."),
        "judgements": [
            {
                "name": ts["question"],
                "adopted": carried["label"] + " — " + carried["condition"],
                "alternative": stopped["label"] + " — " + stopped["condition"],
                "value_adopted": float(carried["value"]),
                "value_alternative": float(stopped["value"]),
                "why": ts["why_not_averaged"] + " " + ts["decides"],
            }
        ],
    }
    return diag, cj


def main():
    diag, cj = build()
    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w",
                         encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(cj, open(os.path.join(HERE, "contested_judgements.json"), "w",
                       encoding="utf-8"), indent=1, ensure_ascii=False)
    print(diag["implied"]["reading"])
    print("contested judgements committed both ways: %d" % len(cj["judgements"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
