#!/usr/bin/env python3
"""ADIB — the reverse read and the sign test. [R-ENF-05]

THE REVERSE READ. This study states what it believes. It has never stated what the PRICE
believes, and the two are the same model read backwards. Solved here: the SINGLE FLAT
COST OF EQUITY that reproduces the traded price on this study's own dividend stream, its
own terminal payout and its own terminal growth, holding every driver at its published
value. It is compared with the flat rate that reproduces THIS STUDY'S OWN answer on the
identical construction, so the two numbers are one quantity measured twice rather than a
rate read against a glide path.

WHY A RATE ON A BANK. The dividend-discount lens is the primary read for a bank and a
rate is the one quantity every study in this book has, so a reverse read on it pools
across names where a reverse read on net interest margin would not. The margin
disagreement is carried in the contested-judgement record instead, priced, where a reader
can see it directly.

THE CONTAINMENT RULE IS THE POINT, NOT A FORMALITY. A rate solved from a price and then
used anywhere in the valuation is the reverse-engineered rate the protocol prohibits
outright, arriving through a side door. This file writes diagnostics.json and NOTHING
READS IT BACK — the build order declares it as an output and no builder opens it.

    python3 engine/adib_study/diagnostics_adib.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edition as _ed                                                 # noqa: E402

N = json.load(open(os.path.join(HERE, "study_numbers.json"), encoding="utf-8"))
COC, PROJ = N["cost_of_capital"], N["projection"]
SPOT, CENTRAL, SHARES = N["spot"], N["central"], N["meta"]["shares_mn"]


def _rows():
    r = PROJ["rows"] if isinstance(PROJ, dict) and "rows" in PROJ else PROJ
    if not isinstance(r, list):
        raise SystemExit("the projection is not a list of years; the reverse read cannot "
                         "be solved without the dividend stream it reverses")
    return r


def per_share_at(ke):
    """The dividend-discount lens at ONE flat cost of equity, everything else published.

    The published lens discounts on a glide path; this reads the same stream at a single
    rate, and the study's own answer is re-read the same way, so the comparison is of two
    numbers built identically.
    """
    rows = _rows()
    g, roe_term = COC["terminal_growth"], rows[-1]["roe"]
    if ke <= g:
        return float("inf")
    pv = sum(rw["dividend"] / (1 + ke) ** (i + 1) for i, rw in enumerate(rows))
    payout_term = max(0.0, min(1.0, 1 - g / roe_term))
    d_next = rows[-1]["np_parent"] * (1 + g) * payout_term
    tv = d_next / (ke - g)
    return (pv + tv / (1 + ke) ** len(rows)) / SHARES


def solve(target):
    """The flat cost of equity that reproduces `target` a share. Bisection, no fitting."""
    lo, hi = COC["terminal_growth"] + 1e-4, 1.50
    if per_share_at(hi) > target:
        raise SystemExit("no cost of equity below 150%% reproduces %.4f a share; the "
                         "reverse read refuses rather than reporting a bound as an "
                         "answer" % target)
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if per_share_at(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main():
    implied = solve(SPOT)
    own = solve(CENTRAL)
    out = {
        "ticker": "ADIB",
        "as_of": _ed.ISO,
        "spot": SPOT,
        "published_central": CENTRAL,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC and "
            "lives outside the numbers file every builder reads. A quantity solved from "
            "a price and then used anywhere in the valuation is the reverse-engineered "
            "rate the protocol prohibits, arriving through a side door. Nothing in this "
            "file is an input to anything; it is COMPUTED by diagnostics_adib.py."),
        "implied": {
            "quantity": "the single flat cost of equity that reproduces the traded price "
                        "on this study's own dividend stream",
            "value": implied,
            "study_value": own,
            "study_glide_path": {"first_year": COC["ke"], "terminal": COC["ke_terminal"]},
            "solved_on": "the published dividend-discount lens through "
                         "diagnostics_adib.per_share_at, holding every driver at its "
                         "committed value and varying only the flat discount rate until "
                         "the model reproduces the traded price. The study's own answer "
                         "is re-read at a flat rate the same way, so the pair is one "
                         "quantity measured twice.",
            "reading": (
                "At EGP %.2f the price is paying for a flat cost of equity of %.2f%%, "
                "against the %.2f%% that reproduces this study's own EGP %.4f on the "
                "identical construction — a disagreement of %.0f basis points on ONE "
                "number a reader can check. The study's published path runs %.2f%% in "
                "the first year to %.2f%% at the terminal; a flat rate is not that path "
                "and is not presented as it, it is the common quantity that lets this "
                "name be compared with every other in the book."
                % (SPOT, 100 * implied, 100 * own, CENTRAL,
                   10000 * (implied - own), 100 * COC["ke"], 100 * COC["ke_terminal"])),
        },
    }
    json.dump(out, open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1)
    print("wrote diagnostics.json — price implies a flat %.2f%% against the study's "
          "%.2f%% (%.0f bp)" % (100 * implied, 100 * own, 10000 * (implied - own)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
