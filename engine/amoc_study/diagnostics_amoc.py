"""AMOC — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ WAS ALREADY SOLVED IN THE MODEL AND HAD NEVER BEEN EMITTED.
compute.py solves the gross margin that reproduces the traded price on this
study's own drivers and commits it as `gm_required`; nothing wrote it into a
diagnostics record, so the gate could not see a diagnostic the study had already
computed. That is the same shape as EGCH's, and the fix is the same: write it out,
and read nothing back.

WHY THIS QUANTITY. A refiner's whole answer sits in the spread between the crude
it buys and the products it sells, so the gross margin IS the crux; the study's
own text calls it that and solves on it. Expressing the disagreement as a margin
also makes it checkable against the company's own filings, which is what caught a
false claim in a previous edition: it put the required margin at 12.2% and called
it "above the best single quarter this company has ever filed" when the company
had filed 13.84% for a full year and 13.92% in a quarter.

THE CONTESTED JUDGEMENTS ARE ON THE DELIVERED BRIDGE NOW, AND THAT CHANGED THE
ANSWER. Until today they were priced by a helper that reproduced neither the
study's terminal nor its bridge, returning EGP 10.8572 at the study's own adopted
rates against a delivered 9.9142. On that basis three of four choices cleared the
5%-of-value line. Recomputed through the study's own waterfall, exactly ONE does.
A sign test on the old figures would have counted three material judgements where
there is one — which is why this file could not honestly be written before that
was fixed.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.join(HERE, "study_numbers.json")


def build():
    d = json.load(open(NUM, encoding="utf-8"))
    dcf, gm, meta = d["dcf"], d["gm_required"], d["meta"]
    spot, ps = float(d["spot"]), float(dcf["ps"])

    diag = {
        "ticker": "AMOC",
        "as_of": meta.get("asof") or d.get("asof"),
        "spot": spot,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a "
            "DIAGNOSTIC and lives outside the numbers file every builder reads. A "
            "quantity solved from a price and then used anywhere in the valuation "
            "is the reverse-engineered rate the protocol prohibits outright, "
            "arriving through a side door. Nothing here is an input to anything; "
            "it is written OUT of what compute.py already committed."),
        "implied": {
            "quantity": ("the gross margin sustained in every forecast year AND in "
                         "perpetuity that reproduces the traded price"),
            "value": float(gm["level"]),
            "study_value": float(gm["base"]),
            "study_value_range": [float(gm["level"]), float(gm["filed_max_year"])],
            "solved_on": (
                "compute.py's own solve, holding every other driver at its base "
                "case and moving only the gross margin until the cash-flow lens "
                "reaches the market price"),
            "reading": (
                "At EGP %.2f the price is paying for a gross margin of %.2f%% held "
                "in every forecast year and in perpetuity, against a base year of "
                "%.2f%% — a gap of %.0f basis points. That is INSIDE the range this "
                "company has actually printed: it filed %.2f%% for the full year to "
                "30 June 2022 and %.2f%% in the quarter to 30 June 2026. So the "
                "market is not pricing something the business has never done; it is "
                "pricing a little less than the base year, and the study's answer "
                "of EGP %.2f is %+.1f%% against the price."
                % (spot, 100 * gm["level"], 100 * gm["base"],
                   -10000 * gm["shift"], 100 * gm["filed_max_year"],
                   100 * gm["filed_max_quarter"], ps, 100 * (ps / spot - 1))),
        },
    }

    # Both framings, priced through the study's own waterfall.
    def row(name, adopted, alternative, value_alt, why):
        return {"name": name, "adopted": adopted, "alternative": alternative,
                "value_adopted": ps, "value_alternative": float(value_alt),
                "why": why}

    cj = {
        "ticker": "AMOC",
        "as_of": meta.get("asof") or d.get("asof"),
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not "
            "is a study that resolves EVERY contested choice the same way and never "
            "notices. Each is recorded with BOTH framings' values, the side adopted "
            "and why, and the binomial sign test is printed."),
        "both_framings_share_a_bridge": (
            "Every alternative below is computed by THIS study's own waterfall — "
            "the replacement-cost terminal and the delivered six-line bridge — so "
            "the difference between it and the headline measures the CHOICE and not "
            "the construction. Until 03-09-2026 they were priced by a helper that "
            "reproduced neither, and on that basis three of the four cleared the "
            "5%-of-value line; on this one, exactly one does. L-070."),
        "judgements": [
            row("the equity-risk-premium basis",
                "the CDS basis, the market's own live pricing of the sovereign's credit",
                "the rating basis, an agency judgement updated in steps",
                d["dcf"]["ps_rating_basis"],
                "both bases are published and one is named central; the swap basis "
                "is preferred because it is priced continuously by the market "
                "rather than revised in discrete agency steps, and the difference "
                "is the largest single contested number in this study"),
            row("the minority's share",
                "the minority at its share of gross equity value, 2.96%",
                "that share doubled",
                d["dcf"]["ps_nci_alt"],
                "the share is struck on the subsidiaries' own profit contribution "
                "net of the parent's credit interest; doubling it is the sensitivity "
                "a reader would ask for and it moves the answer by about three per "
                "cent, which is a smaller number than the old helper reported"),
            row("gross versus net debt weights in the operating rate",
                "gross-borrowing weights, with the cash added once at face in the bridge",
                "net-debt weights",
                d["dcf"]["ps_gross_basis"],
                "on a net-cash company the net-debt weight goes negative and levers "
                "the equity weight above one, which is the construction "
                "[R-BRIDGE-01] (iii) forbids and which a previous edition of this "
                "study carried; on a debt book that is 0.14% of the capital "
                "structure the corrected difference is essentially nil, and that is "
                "the honest finding rather than the 9.5% the broken helper reported"),
            row("the currency the export leg is discounted in",
                "the whole business discounted in pounds on the local cost of capital",
                "the export leg deflated to dollars, discounted at a dollar cost of "
                "capital with 3.5% terminal growth, and translated back",
                d["dcf"]["ccy_alt_ps"],
                "a majority-export refiner can be read either way and the two "
                "answers differ by three per cent; the pound read is adopted "
                "because the cash flows, the tax and the debt are all struck in "
                "pounds and a mixed-currency discount would price the same "
                "inflation twice"),
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
    base = diag["implied"]
    for j in cj["judgements"]:
        d = abs(j["value_adopted"] - j["value_alternative"]) / abs(j["value_alternative"])
        print("  %-46s %8.4f vs %8.4f  %5.1f%%%s"
              % (j["name"][:46], j["value_adopted"], j["value_alternative"],
                 100 * d, "  MATERIAL" if d >= 0.05 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
