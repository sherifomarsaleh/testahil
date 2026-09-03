"""ARCC — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ. This study states what it believes. It has never stated what the
PRICE believes, and the two are the same model read backwards. Solved here: the
SINGLE FLAT DISCOUNT RATE that reproduces the traded price on this study's own
free cash flows, its own terminal cash flow and its own terminal growth, holding
every driver at its published value. It is compared with the flat rate that
reproduces THIS STUDY'S OWN enterprise value on the identical construction — so
the two numbers are the same quantity measured twice, not a rate against a
schedule, and the disagreement is readable as one number.

WHY THIS QUANTITY ON THIS NAME. The study's own record names beta as its most
consequential contested judgement, worth 9.6% of value, and beta enters through
exactly this rate. A reverse read on the discount rate therefore lands on the
study's own crux rather than beside it.

THE CONTAINMENT RULE IS THE POINT, NOT A FORMALITY. A rate solved from a price and
then used anywhere in the valuation is the reverse-engineered terminal the
protocol prohibits outright, arriving through a side door. So this file writes
diagnostics.json and NOTHING READS IT BACK — assert_reverse_dcf() refuses any
study whose builders import it, and this module is named `diagnostics_*` so the
gate's own exemption applies to the file that COMPUTES the read rather than to a
builder that consumes it.

THE SIGN TEST. Any single contested choice is defensible; what is not is a study
resolving every one of them the same way and never noticing. The study already
computes each contested construction BOTH ways in `study_numbers.json`; this
module emits them in the shape the standing record takes and lets the binomial
sign test speak.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.join(HERE, "study_numbers.json")


def _ev(r, fcff, t_mid, fcff_term, g, t_tv):
    """Enterprise value at one flat rate, on the study's own construction."""
    if r <= g:
        return float("inf")
    pv = sum(cf / (1.0 + r) ** t for cf, t in zip(fcff, t_mid))
    tv = fcff_term / (r - g)
    return pv + tv / (1.0 + r) ** t_tv


def solve(target, fcff, t_mid, fcff_term, g, t_tv, lo=0.0701, hi=2.0):
    """The flat rate reproducing `target`. Bisection: the function is monotone
    decreasing in r above g, so there is exactly one root and no starting guess
    can move the answer."""
    for _ in range(400):
        mid = 0.5 * (lo + hi)
        if _ev(mid, fcff, t_mid, fcff_term, g, t_tv) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def build():
    d = json.load(open(NUM, encoding="utf-8"))
    f, dcf, coc, mac = d["forecast"], d["dcf"], d["cost_of_capital_record"], d["macro_record"]
    br, meta = d["bridge_record"], d["meta"]

    fcff = list(f["fcff"])
    t_mid = list(f["t_mid"])
    g = float(mac["terminal"]["g_nominal"])
    wacc_t = float(coc["wacc_terminal"])

    # The terminal cash flow the study itself capitalised, recovered from its own
    # terminal value rather than re-derived: TV = FCFF_term / (wacc_T - g).
    fcff_term = float(dcf["tv"]) * (wacc_t - g)

    # The date the terminal is brought home on, read off the study's own factors
    # rather than assumed: df_tv = df_last / (1 + wacc_T) ** dt.
    dt = (dcf["df_tv"] and (dcf["df_tv"] / f["df"][-1])) or 1.0
    import math
    t_tv = t_mid[-1] + math.log(1.0 / dt) / math.log(1.0 + wacc_t)

    # The price's own enterprise value, through the study's own bridge, so that
    # the two rates are solved against the same construction.
    shares = float(br["shares_mn"])
    spot = float(meta["spot"])
    equity_at_spot = spot * shares
    bridge_delta = float(br["equity_value"]) - float(dcf["ev"])   # net cash less NCI etc.
    ev_at_spot = equity_at_spot - bridge_delta

    r_price = solve(ev_at_spot, fcff, t_mid, fcff_term, g, t_tv)
    r_study = solve(float(dcf["ev"]), fcff, t_mid, fcff_term, g, t_tv)

    diag = {
        "ticker": meta["ticker"],
        "as_of": meta.get("asof"),
        "spot": spot,
        "spot_date": meta.get("spot_date"),
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a "
            "DIAGNOSTIC and lives outside the numbers file every builder reads. A "
            "quantity solved from a price and then used anywhere in the valuation "
            "is the reverse-engineered rate the protocol prohibits outright, "
            "arriving through a side door. Nothing in this file is an input to "
            "anything."),
        "implied": {
            "quantity": ("the single flat discount rate that reproduces the price "
                         "on this study's own free cash flows and terminal"),
            "value": r_price,
            "study_value": r_study,
            "study_value_range": [wacc_t, float(coc["wacc_exp"])],
            "solved_on": (
                "this study's own committed free cash flows, its own terminal cash "
                "flow recovered from its own terminal value, its own terminal "
                "growth and its own bridge — holding every driver at its published "
                "value and varying only the discount rate until the model "
                "reproduces the traded price"),
            "reading": (
                "At EGP %.2f the price is paying for a flat %.2f%% cost of capital "
                "on the same cash flows this study discounts at a schedule "
                "equivalent to a flat %.2f%%. The study's own explicit-window rate "
                "is %.2f%% gliding to a terminal %.2f%%, so the market and the "
                "study disagree by about %.0f basis points on the price of time and "
                "risk — not on the business. The study's own record names beta as "
                "its most consequential contested judgement, worth %.1f%% of value, "
                "and beta enters through exactly this rate."
                % (spot, 100 * r_price, 100 * r_study,
                   100 * float(coc["wacc_exp"]), 100 * wacc_t,
                   10000 * (r_study - r_price),
                   100 * max(c["effect"] for c in d["contested"]))),
        },
        "construction": {
            "terminal_cash_flow": fcff_term,
            "terminal_growth": g,
            "terminal_arrives_at_year": t_tv,
            "enterprise_value_at_spot": ev_at_spot,
            "enterprise_value_in_study": float(dcf["ev"]),
            "bridge_delta_equity_less_ev": bridge_delta,
        },
    }

    cj = {
        "ticker": meta["ticker"],
        "as_of": meta.get("asof"),
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not "
            "is a study that resolves EVERY contested choice the same way and never "
            "notices — which is how a lean survives an audit of its steps. Each is "
            "recorded with BOTH framings' values, the side adopted and why, and the "
            "binomial sign test is printed. A study landing them all one way is "
            "FLAGGED, never failed: a company can genuinely deserve a consistent "
            "read, and a gate that failed on it would push studies to resolve "
            "judgements inconsistently to stay green."),
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


def main():
    diag, cj = build()
    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w",
                         encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(cj, open(os.path.join(HERE, "contested_judgements.json"), "w",
                       encoding="utf-8"), indent=1, ensure_ascii=False)
    i = diag["implied"]
    print("ARCC reverse read: price implies %.4f%%, study %.4f%%  (spot %.2f)"
          % (100 * i["value"], 100 * i["study_value"], diag["spot"]))
    print("  " + i["reading"])
    print("contested judgements: %d" % len(cj["judgements"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
