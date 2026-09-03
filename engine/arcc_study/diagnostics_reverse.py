#!/usr/bin/env python3
"""ARCC — the reverse read: what the traded price must believe [R-ENF-05].

THE QUANTITY IS THE CEMENT PRICE, IN POUNDS PER TONNE. This study builds revenue
bottom-up as volume times price on the company's own disclosed tonnages, and its
own crux is the price path: it escalates cost at domestic inflation while
escalating the cement price below it, which is a real-terms squeeze the study
argues for explicitly. So the price per tonne is both the quantity the answer
turns on and one a reader can check against what cement actually sells for — the
"real observable units" the depth bar asks for, rather than a discount rate
nobody can observe.

WHAT MOVES AND WHAT DOES NOT. Only the price path is scaled. Volume, the cost
stack in absolute pounds, depreciation, capex, working capital, the tax rate, the
cost-of-capital glide, the terminal construction and the four-line bridge are all
held exactly at their published values — so a higher price flows to EBITDA pound
for pound, which is what a price change does to a producer whose costs are set by
its own inputs.

THE RECONSTRUCTION IS PROVED BEFORE IT IS USED, and on this study that matters
twice over: its first forecast year is a STUB. The valuation date sits part-way
through FY2026 and the model takes half of that year's free cash flow, discounting
on a 0.25-year first factor. A reconstruction that missed the stub would return a
confident wrong answer, so this refuses unless it returns the published figure to
within a tenth of a piastre.

NOTHING HERE IS AN INPUT TO ANYTHING. The result is written to diagnostics.json,
which no builder reads.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUMBERS = os.path.join(HERE, "study_numbers.json")
OUT = os.path.join(HERE, "diagnostics.json")
TOL_PS = 0.001
STUB = 0.5          # the fraction of FY2026 remaining at the valuation date, read
                    # off the study's own first-year free cash flow below


def load():
    return json.load(open(NUMBERS, encoding="utf-8"))


def per_share(d: dict, price_scale: float = 1.0) -> dict:
    f, w, c = d["forecast"], d["wacc"], d["dcf"]
    vol, price = f["volume_mt"], f["price_t"]
    ebitda0, dna, ebit0 = f["ebitda"], f["dna"], f["ebit"]
    nopat0, capex, dwc, df = f["nopat"], f["capex"], f["dwc"], f["df"]
    rev0 = f["revenue"]

    # the cost stack in absolute pounds, and the tax rate, both recovered from the
    # study's own published lines rather than assumed
    cost = [r - e for r, e in zip(rev0, ebitda0)]
    other = [eb - (e - dn) for eb, e, dn in zip(ebit0, ebitda0, dna)]   # non-EBITDA items in EBIT
    tax = [1.0 - (n / e) if e else 0.0 for n, e in zip(nopat0, ebit0)]

    pv, nopat_path = 0.0, []
    for i in range(len(vol)):
        rev = vol[i] * price[i] * price_scale
        ebitda = rev - cost[i]
        ebit = ebitda - dna[i] + other[i]
        nopat = ebit * (1.0 - tax[i])
        nopat_path.append(nopat)
        cf = nopat + dna[i] - capex[i] - dwc[i]
        if i == 0:
            cf *= STUB              # the first year is a stub: see the docstring
        pv += cf * df[i]

    # the study's own terminal: terminal NOPAT net of the reinvestment its terminal
    # return requires, capitalised at the terminal rate less growth
    g = w["wacc_term"] - c["nopat_term"] * (1.0 - c["rr_term"]) / c["tv"]
    nopat_term = c["nopat_term"] * (nopat_path[-1] / d["forecast"]["nopat"][-1])
    tv = nopat_term * (1.0 - c["rr_term"]) / (w["wacc_term"] - g)
    pv_tv = tv * c["df_tv"]
    ev = pv + pv_tv

    bridge = {L["label"]: L["value"] for L in d["bridge_record"]["lines"]}
    ev_label = next(k for k in bridge if k.lower().startswith("enterprise"))
    equity = ev + sum(v for k, v in bridge.items() if k != ev_label)
    return {"ev": ev, "equity": equity,
            "ps": equity / d["bridge_record"]["shares_mn"],
            "sum_pv": pv, "pv_tv": pv_tv, "tv_share": pv_tv / ev}


def solve(d: dict, target_ps: float) -> float:
    lo, hi = 0.2, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if per_share(d, mid)["ps"] < target_ps:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main(live: float | None = None) -> dict:
    d = load()
    published = d["dcf"]["fv"]
    check = per_share(d, 1.0)
    if abs(check["ps"] - published) > TOL_PS:
        raise SystemExit(
            "REFUSED — the reconstruction returns %.6f against the study's published "
            "%.6f. A solver built on a model that does not reproduce the published "
            "answer is solving a different study." % (check["ps"], published))

    f = d["forecast"]
    struck = float(d["spot"])

    def at(px):
        sc = solve(d, px)
        return {"price": px, "scale": sc,
                "price_t": [p * sc for p in f["price_t"]],
                "first_year": f["price_t"][0] * sc}

    reads = {"struck": at(struck)}
    if live is not None:
        reads["latest_supplied"] = at(float(live))

    out = {
        "ticker": "ARCC",
        "as_of": "2026-09-03",
        "spot": struck,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC "
            "and lives outside the numbers file every builder reads. A quantity solved "
            "from a price and then used anywhere in the valuation is the "
            "reverse-engineered rate the protocol prohibits outright, arriving through "
            "a side door. Nothing in this file is an input to anything."),
        "implied": {
            "quantity": "the realised cement price, EGP per tonne, across the explicit "
                        "window",
            "value": reads["struck"]["first_year"],
            "study_value": f["price_t"][0],
            "study_value_range": [f["price_t"][0], f["price_t"][-1]],
            "volume_held_at": f["volume_mt"],
            "solved_on": (
                "this study's own model: volume, the cost stack in absolute pounds, "
                "depreciation, capex, working capital, the effective tax rate, the "
                "cost-of-capital glide, the terminal construction and the four-line "
                "bridge all held exactly at their published values, with only the "
                "price-per-tonne path scaled until the model reproduces the traded "
                "price. The reconstruction is proved to return the published %.4f a "
                "share at a scale of 1.0 first, including this study's HALF-YEAR STUB "
                "on its opening forecast year, which a reconstruction that missed "
                "would get confidently wrong." % published),
            "at_prices": reads,
            "reading": "",
        },
        "reconstruction_check": {"published_ps": published, "rebuilt_ps": check["ps"],
                                 "tolerance": TOL_PS},
    }
    lines = ["At the EGP %.2f this study was struck at, the price is paying for a "
             "2026 cement price of EGP %.0f a tonne against the EGP %.0f the study "
             "forecasts — a %.1f%% difference."
             % (struck, reads["struck"]["first_year"], f["price_t"][0],
                (reads["struck"]["scale"] - 1) * 100)]
    if live is not None:
        r = reads["latest_supplied"]
        lines.append(
            "At EGP %.2f it is paying for EGP %.0f a tonne, %.1f%% above the study's "
            "path, with volume held at the company's own %.2f million tonnes. That is "
            "the disagreement in the units the business actually sells in: not a view "
            "about discount rates, but a view about what a tonne of cement fetches."
            % (r["price"], r["first_year"], (r["scale"] - 1) * 100, f["volume_mt"][0]))
    out["implied"]["reading"] = " ".join(lines)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(out["implied"]["reading"])
    print("\nwrote %s" % os.path.relpath(OUT, os.path.dirname(os.path.dirname(HERE))))
    return out


if __name__ == "__main__":
    import sys
    main(float(sys.argv[1]) if len(sys.argv) > 1 else None)
