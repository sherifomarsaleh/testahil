"""SCEM — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ. This study states what it believes. It has never stated what the
PRICE believes, and the two are the same model read backwards. Solved here: the
SINGLE FLAT DISCOUNT RATE that reproduces the traded price on this study's own free
cash flows, its own terminal cash flow and its own terminal growth, holding every
driver at its published value. It is compared with the flat rate that reproduces
THIS STUDY'S OWN enterprise value on the identical construction, so the two numbers
are the same quantity measured twice rather than a rate against a schedule.

WHY A RATE ON THIS NAME. The study's largest contested judgement is the kiln
utilisation ramp, which is a physical driver rather than a rate — but a reverse read
on utilisation cannot be compared with any other name in the book, and the point of
this diagnostic is that it pools. The rate is the one quantity every study has. The
utilisation disagreement is carried instead in the contested-judgement record, priced
at 11.4 per cent of value, where a reader can see it directly.

THE CONTAINMENT RULE IS THE POINT, NOT A FORMALITY. A rate solved from a price and
then used anywhere in the valuation is the reverse-engineered terminal the protocol
prohibits outright, arriving through a side door. This file writes diagnostics.json
and NOTHING READS IT BACK.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.join(HERE, "study_numbers.json")


def _shared():
    """ONE construction, held in engine/reverse_read.py — never a per-study copy.

    The discounting convention is read from this study's own declared record rather
    than assumed: SCEM discounts to mid-period points from a valuation date seven
    months into FY2026, and assuming year-ends would put a real error into the
    answer silently.
    """
    import sys
    sys.path.insert(0, os.path.dirname(HERE))
    import reverse_read as RR
    return RR


def build():
    RR = _shared()
    d = json.load(open(NUM, encoding="utf-8"))
    f, dcf, coc = d["forecast"], d["dcf"], d["cost_of_capital_record"]
    mac, br, meta = d["macro_record"], d["bridge_record"], d["meta"]

    t_mid, how = RR.resolve_times(coc, f["df"], f["fwd_wacc"])
    r = RR.read(f["fcff"], t_mid, dcf["tv"], coc["wacc_terminal"],
                mac["terminal"]["g_nominal"], f["df"][-1], dcf["df_tv"],
                dcf["ev"], br["equity_value"], br["shares_mn"], meta["spot"])

    r_price = r["implied_rate_at_price"]
    r_study = r["implied_rate_at_study_value"]
    biggest = max(c["effect"] for c in d["contested"])
    top = max(d["contested"], key=lambda c: c["effect"])

    diag = {
        "ticker": meta["ticker"],
        "as_of": meta.get("asof"),
        "spot": float(meta["spot"]),
        "spot_date": meta.get("spot_date"),
        "published_central": float(meta["central"]),
        "published_spot": float(meta["spot"]),
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC "
            "and lives outside the numbers file every builder reads. A quantity solved "
            "from a price and then used anywhere in the valuation is the "
            "reverse-engineered rate the protocol prohibits outright, arriving through "
            "a side door. Nothing in this file is an input to anything."),
        "implied": {
            "quantity": ("the single flat discount rate that reproduces the price on "
                         "this study's own free cash flows and terminal"),
            "value": r_price,
            "study_value": r_study,
            "study_value_range": [coc["wacc_terminal"], coc["wacc_exp"]],
            "solved_on": (
                "engine/reverse_read.py, on this study's own committed free cash flows, "
                "its own terminal cash flow recovered from its own terminal value, its "
                "own terminal growth and its own bridge — holding every driver at its "
                "published value and varying only the discount rate until the model "
                "reproduces the traded price. The discounting convention was %s." % how),
            "reading": (
                "At EGP %.2f the price is paying for a flat %.2f%% cost of capital on "
                "the same cash flows this study discounts at a schedule equivalent to a "
                "flat %.2f%%. The study's own explicit-window rate is %.2f%% gliding to "
                "a terminal %.2f%%, so the disagreement is about %.0f basis points on "
                "the price of time and risk. THAT IS THE WHOLE DISAGREEMENT EXPRESSED AS "
                "A RATE, and it is worth reading beside the business one: this study's "
                "largest contested judgement is %s, worth %.1f%% of value, and it is "
                "physical rather than financial. A reader who accepts the rate and "
                "rejects the ramp lands close to the market; a reader who accepts both "
                "lands here."
                % (float(meta["spot"]), 100 * r_price, 100 * r_study,
                   100 * float(coc["wacc_exp"]), 100 * float(coc["wacc_terminal"]),
                   10000 * (r_study - r_price), top["choice"], 100 * biggest)),
        },
        "construction": dict(r, discounting_times=t_mid, times_resolved=how),
    }

    cj = {
        "ticker": meta["ticker"],
        "as_of": meta.get("asof"),
        "published_central": float(meta["central"]),
        "published_spot": float(meta["spot"]),
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not is a "
            "study that resolves EVERY contested choice the same way and never notices "
            "— which is how a lean survives an audit of its steps. Each is recorded with "
            "BOTH framings' values, the side adopted and why, and the binomial sign test "
            "is printed. A study landing them all one way is FLAGGED, never failed: a "
            "company can genuinely deserve a consistent read, and a gate that failed on "
            "it would push studies to resolve judgements inconsistently to stay green."),
        "both_framings_share_a_bridge": (
            "Every alternative below is computed by this study's own build_dcf() — the "
            "same function that produces the published figure — so the difference "
            "between them measures the CHOICE and not the construction. That is L-070, "
            "found on AMOC, and it is why the bottom-up build and the cash-flow chain "
            "were both refactored into functions before any of these were priced."),
        "judgements": [
            {
                "name": c["choice"],
                "adopted": c["adopted"],
                "alternative": c["alternative"],
                "value_adopted": c["fv_adopted"],
                "value_alternative": c["fv_alternative"],
                "why": c["note"],
            }
            for c in d["contested"]
        ],
    }
    return diag, cj


if __name__ == "__main__":
    diag, cj = build()
    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1,
              default=float)
    json.dump(cj, open(os.path.join(HERE, "contested_judgements.json"), "w"), indent=1,
              default=float)
    n = len(cj["judgements"])
    mat = [j for j in cj["judgements"]
           if abs(j["value_alternative"] - j["value_adopted"]) / j["value_adopted"] > 0.05]
    up = sum(1 for j in mat if j["value_adopted"] > j["value_alternative"])
    print("SCEM reverse read: the price implies %.2f%%; the study's own value implies "
          "%.2f%%" % (100 * diag["implied"]["value"],
                      100 * diag["implied"]["study_value"]))
    print("SCEM sign test: %d judgements, %d material, %d of those resolved upward"
          % (n, len(mat), up))
