#!/usr/bin/env python3
"""TMGH — the reverse read [R-ENF-05], GENERATED.

Every study states what IT believes and almost none states what the PRICE believes, and the
two are the same model read backwards. This solves the single flat discount rate that
reproduces the traded price under this study's own drivers, holding everything else at its
published value, so a reader can judge the DISAGREEMENT rather than the conclusion.

THE HARD PART IS KEEPING IT OUT OF THE MODEL AND THE RULE IS STRUCTURAL. It lives here and
in diagnostics.json, NEVER in study_numbers.json, and assert_reverse_dcf() refuses any study
whose builders read that file back in: a quantity solved from a price and re-entering the
valuation is the reverse-engineered rate the cost-of-capital procedure prohibits outright,
arriving through a side door.

THIS FILE EXISTS BECAUSE THE RECORD DID NOT HAVE ONE. diagnostics.json was written by
nothing anywhere in the repository, and when the reverse read moved — it had been solving
against a per-share the study does not publish — the file kept the old answer and the
sign-test gate went on quoting 29.05% against a model that now says 31.87%. That is
[R-ENF-06]'s shape exactly: an artefact every reader trusts, a number frozen at the moment
somebody last typed it.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
N = json.load(open(os.path.join(HERE, "study_numbers.json")))


def main():
    L = N["lenses"]["implied_discount_rate"]
    S = N["cost_of_capital_record"]
    out = {
        "ticker": N["meta"]["ticker"],
        "as_of": N["meta"]["edition_date"],
        "spot": N["meta"]["spot"],
        # [R-ENF-06]: the answer this diagnostic was generated against
        "published_central": N["central"],
        "published_spot": N["meta"]["spot"],
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC and "
            "lives outside the numbers file every builder reads. A rate or a growth solved "
            "from a price and then used anywhere in the valuation is the reverse-engineered "
            "terminal the protocol prohibits outright, arriving through a side door. "
            "Nothing in this file is an input to anything."),
        "implied": {
            "quantity": "the single flat discount rate that reproduces the traded price "
                        "on this model",
            "value": L["capacity"],
            "value_other_framing": L["recovery"],
            "study_value": S["forward_wacc"][0],
            "study_value_terminal": S["wacc_terminal"],
            "solved_on": "this study's own model, holding every driver at its published "
                         "value and varying only the discount rate, on each of the two "
                         "readings of the crux, with the minority deducted on the basis "
                         "this study adopts",
            "reading": (
                "The price is paying for a flat %.1f%% on the slower reading of the order "
                "book and %.1f%% on the faster one. This study does not use a flat rate: "
                "it discounts each year at its own, from %.2f%% to %.2f%%. The comparison "
                "is a degenerate construction offered because a reader used to one number "
                "will look for one, and the disagreement it measures is smaller than the "
                "headline rates suggest."
                % (100 * L["capacity"], 100 * L["recovery"],
                   100 * S["forward_wacc"][0], 100 * S["wacc_terminal"])),
        },
    }
    p = os.path.join(HERE, "diagnostics.json")
    json.dump(out, open(p, "w"), indent=1)
    print("wrote %s — price implies %.2f%% / %.2f%% against the study's %.2f%%"
          % (os.path.basename(p), 100 * L["capacity"], 100 * L["recovery"],
             100 * S["forward_wacc"][0]))


if __name__ == "__main__":
    main()
