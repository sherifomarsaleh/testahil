"""ADNOCLS — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ. This study states what it believes. It has never stated what the
PRICE believes, and the two are the same model read backwards. Solved here: the
SINGLE FLAT DISCOUNT RATE that reproduces the traded price on this study's own free
cash flows, its own terminal cash flow and its own terminal growth, holding every
driver at its published value.

WHY A RATE ON THIS NAME, AND IT IS UNUSUALLY APT HERE. This study's largest contested
judgement is HOW THE MARKET IS MEASURED for the beta regression — the published index
against an equal-weight composite — and beta enters the valuation through exactly this
rate and nowhere else. So the reverse read lands on the study's own crux rather than
beside it, and a reader can see immediately whether the price sits inside the span the
two regressors give.

THE CONTAINMENT RULE IS THE POINT, NOT A FORMALITY. A rate solved from a price and then
used anywhere in the valuation is the reverse-engineered terminal the protocol prohibits
outright, arriving through a side door. This file writes diagnostics.json and NOTHING
READS IT BACK.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.join(HERE, "study_numbers.json")


def _shared():
    """ONE construction, held in engine/reverse_read.py — never a per-study copy."""
    import sys
    sys.path.insert(0, os.path.dirname(HERE))
    import reverse_read as RR
    return RR


def build():
    RR = _shared()
    d = json.load(open(NUM, encoding="utf-8"))
    dcf, coc = d["dcf"], d["cost_of_capital_record"]
    mac, br, meta = d["macro_record"], d["bridge_record"], d["meta"]
    fcff = list(d["fcst"]["fcff"])
    fcff[0] -= d["inputs"]["q1_26_fcf"]["value"]      # already inside net debt at the date

    t_mid, how = RR.resolve_times(coc, dcf["df"], coc["forward_wacc"])
    # THE UNIT IS THE THING TO CHECK. The bridge is in USD THOUSANDS and its share count
    # is in thousands to match, so the price handed to the reader must be USD PER SHARE —
    # dollars, not thousands of dollars. Multiplying by a thousand here made the price
    # imply a flat 2.01 per cent cost of capital, which is not a finding about the market,
    # it is a finding about arithmetic. The peg is applied once and nothing else moves.
    peg = float(meta["fx"])
    spot_usd = float(meta["spot"]) / peg
    r = RR.read(fcff, t_mid, dcf["tv"], coc["wacc_terminal"],
                mac["terminal"]["g_nominal"], dcf["df"][-1], dcf["df"][-1],
                dcf["ev"], br["equity_value"], br["shares_mn"], spot_usd)

    r_price = r["implied_rate_at_price"]
    r_study = r["implied_rate_at_study_value"]
    top = max(d["contested"], key=lambda c: c["effect"])

    diag = {
        "ticker": meta["ticker"],
        "as_of": meta.get("asof"),
        "spot": float(meta["spot"]),
        "spot_date": meta.get("spot_date"),
        "published_central": float(meta["central"]),
        "published_spot": float(meta["spot"]),
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC and "
            "lives outside the numbers file every builder reads. A quantity solved from a "
            "price and then used anywhere in the valuation is the reverse-engineered rate "
            "the protocol prohibits outright, arriving through a side door. Nothing in "
            "this file is an input to anything."),
        "implied": {
            "quantity": ("the single flat discount rate that reproduces the price on this "
                         "study's own free cash flows and terminal"),
            "value": r_price,
            "study_value": r_study,
            "study_value_range": [coc["wacc_terminal"], coc["wacc_exp"]],
            "solved_on": (
                "engine/reverse_read.py, on this study's own committed free cash flows, "
                "its own terminal cash flow recovered from its own terminal value, its "
                "own terminal growth and its own bridge — holding every driver at its "
                "published value and varying only the discount rate until the model "
                "reproduces the traded price. The price is converted into the model's own "
                "currency through the peg, once. The discounting convention was %s." % how),
            "reading": (
                "At AED %.2f the price is paying for a flat %.2f%% cost of capital on the "
                "same cash flows this study discounts at a schedule equivalent to a flat "
                "%.2f%%. THE DISAGREEMENT IS A RATE AND THIS STUDY'S OWN CRUX IS A RATE: "
                "its largest contested judgement is %s, worth %.1f%% of value, and beta "
                "enters through exactly this number. A reader who prefers the other "
                "regressor lands close to the market; a reader who accepts the beta rule "
                "as written lands here."
                % (float(meta["spot"]), 100 * r_price, 100 * r_study,
                   top["choice"], 100 * top["effect"])),
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
            "study that resolves EVERY contested choice the same way and never notices — "
            "which is how a lean survives an audit of its steps. Each is recorded with "
            "BOTH framings' values, the side adopted and why, and the binomial sign test "
            "is printed. A study landing them all one way is FLAGGED, never failed: a "
            "company can genuinely deserve a consistent read, and a gate that failed on "
            "it would push studies to resolve judgements inconsistently to stay green."),
        "both_framings_share_a_bridge": (
            "Every alternative below is computed by this study's own dcf() — the same "
            "function that produces the published figure — through the same bridge, so "
            "the difference between them measures the CHOICE and not the construction."),
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
    mat = [j for j in cj["judgements"]
           if abs(j["value_alternative"] - j["value_adopted"]) / j["value_adopted"] > 0.05]
    up = sum(1 for j in mat if j["value_adopted"] > j["value_alternative"])
    print("ADNOCLS reverse read: the price implies %.2f%%; the study's own value implies "
          "%.2f%%" % (100 * diag["implied"]["value"],
                      100 * diag["implied"]["study_value"]))
    print("ADNOCLS sign test: %d judgements, %d material, %d of those resolved upward"
          % (len(cj["judgements"]), len(mat), up))
