#!/usr/bin/env python3
"""AMOC — the reverse read: what the traded price must believe [R-ENF-05].

Every study states what IT believes. Almost none states what the PRICE believes,
and the two are the same model read backwards. This turns a disagreement into a
measurable one — not "we are 26% below" but "the price is paying for a gross
margin of X and we forecast Y, against Z the company has actually filed".

THE QUANTITY IS THE CRUX OF THIS CLASS. AMOC is a refiner on a thin spread: it
buys crude-derived feedstock and sells oils, wax and fuels, and essentially all of
the equity value sits in the few points of gross margin between the two. Revenue
is large and margin is small, so the answer is far more sensitive to margin than
to volume, and margin is what a reader can check against the filed accounts.

IT IS SOLVED ON THIS STUDY'S OWN MODEL AND NOTHING ELSE MOVES. The forecast
revenue path, the opex path, depreciation, tax, capex, working capital, the
cost-of-capital glide, the terminal construction, the net-debt bridge and the
minority deduction are all held exactly at their published values. Only the gross
margin path is scaled, by one factor applied to every year, until the model
reproduces the traded price.

THE RECONSTRUCTION IS PROVED BEFORE IT IS USED. A solver built on a model that
does not reproduce the published answer is solving a different study, and its
output would look exactly as authoritative. So this rebuilds the discounted cash
flow from the committed record at a scale factor of 1.0 and REFUSES unless it
returns the published per-share figure to within a tenth of a piastre.

NOTHING HERE IS AN INPUT TO ANYTHING. The result is written to diagnostics.json,
which no builder reads — assert_reverse_dcf() checks that from outside. A rate
solved from a price and fed back into a valuation is the reverse-engineered rate
the protocol prohibits outright, arriving through a side door.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUMBERS = os.path.join(HERE, "study_numbers.json")
OUT = os.path.join(HERE, "diagnostics.json")
TOL_PS = 0.001          # a tenth of a piastre: the reconstruction must be exact,
                        # not merely close, or it is a different model


def load():
    return json.load(open(NUMBERS, encoding="utf-8"))


def per_share(d: dict, margin_scale: float = 1.0) -> dict:
    """Rebuild the study's own discounted cash flow with the margin path scaled.

    Every line below is taken from the committed record. Where a line depends on
    gross profit it is recomputed; where it does not, it is used as published.
    """
    f, w, c = d["fcst"], d["wacc"], d["dcf"]
    rev, opex, dna = f["rev"], f["opex"], f["dna"]
    capex, dnwc, df = f["capex"], f["dnwc"], f["df"]
    gp0, nopat0, ebit0 = f["gp"], f["nopat"], f["ebit"]

    # the effective tax rate the study actually used, recovered from its own
    # published EBIT and NOPAT rather than assumed
    tax = [1.0 - (n / e) if e else 0.0 for n, e in zip(nopat0, ebit0)]

    pv, fcff = 0.0, []
    for i in range(len(rev)):
        gp = gp0[i] * margin_scale
        ebitda = gp - opex[i]
        ebit = ebitda - dna[i]
        nopat = ebit * (1.0 - tax[i])
        ebit_last = ebit
        cf = nopat + dna[i] - capex[i] - dnwc[i]
        fcff.append(cf)
        pv += cf * df[i]

    # THE TERMINAL ON THE STUDY'S OWN CONSTRUCTION, WHICH IS NOT A GROWN FCFF.
    # It capitalises terminal NOPAT net of the reinvestment its terminal return
    # requires — the value-driver form — and the first attempt here used a grown
    # last-year free cash flow instead, which returned 18,025 against the study's
    # 15,691 and was caught by the reconstruction check below rather than shipped.
    # Brought home on the LAST EXPLICIT YEAR'S factor: one date, one price of time.
    g, wacc_t = c["g"], w["wacc_term"]
    nopat_last = ebit_last * (1.0 - tax[-1])
    tv = nopat_last * (1.0 + g) * (1.0 - c["rr_term"]) / (wacc_t - g)
    pv_tv = tv * df[-1]
    ev = pv + pv_tv

    # THE BRIDGE IS THE STUDY'S OWN SIX LINES, NOT NET DEBT AND A MINORITY SHARE.
    # Provisions, the declared dividend and the investment portfolio all sit in it,
    # and a bridge rebuilt from two of its six lines overstated equity by about a
    # pound a share. Every non-enterprise line is carried at its published value;
    # only the enterprise value moves with the margin.
    bridge = {L["label"]: L["value"] for L in d["bridge_record"]["lines"]}
    ev_label = next(k for k in bridge if k.lower().startswith("enterprise"))
    others = sum(v for k, v in bridge.items() if k != ev_label)
    eq_attr = ev + others
    shares = c["eq_attr"] / c["ps"]        # the study's own share count, recovered
    return {"ev": ev, "eq_attr": eq_attr, "ps": eq_attr / shares,
            "pv_explicit": pv, "pv_tv": pv_tv, "tv_share": pv_tv / ev}


def solve(d: dict, target_ps: float) -> float:
    """The margin scale that makes the model reproduce a given price. Bisection —
    the relation is monotone in margin and a closed form would hide that."""
    lo, hi = 0.05, 8.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if per_share(d, mid)["ps"] < target_ps:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def main(spot: float | None = None) -> dict:
    d = load()
    published = d["dcf"]["ps"]

    check = per_share(d, 1.0)
    if abs(check["ps"] - published) > TOL_PS:
        raise SystemExit(
            "REFUSED — the reconstruction returns %.6f against the study's published "
            "%.6f. A solver built on a model that does not reproduce the published "
            "answer is solving a different study, and its output would read as "
            "authoritative anyway." % (check["ps"], published))

    struck = float(d["spot"])
    live = float(spot) if spot is not None else None
    filed = d["audited"]["gm"]                      # the company's own filed margins
    fy25 = d["base"]["gm_cy25"]
    gm_study = d["fcst"]["gm"]

    def at(px):
        sc = solve(d, px)
        gm = [g * sc for g in gm_study]
        return {"price": px, "scale": sc, "avg": sum(gm) / len(gm),
                "path": gm, "first_year": gm[0]}

    reads = {"struck": at(struck)}
    if live is not None:
        reads["latest_supplied"] = at(live)

    out = {
        "ticker": "AMOC",
        "as_of": "2026-09-03",
        "spot": struck,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a DIAGNOSTIC "
            "and lives outside the numbers file every builder reads. A quantity solved "
            "from a price and then used anywhere in the valuation is the "
            "reverse-engineered rate the protocol prohibits outright, arriving through "
            "a side door. Nothing in this file is an input to anything."),
        "filed_gross_margin": filed,
        "filed_note": (
            "The company's OWN reported gross margins, from this study's committed "
            "record. They are the reference the implied and forecast figures are read "
            "against, and they are not a forecast of anything."),
        "implied": {
            "quantity": "the gross margin on refined product, averaged over the "
                        "explicit window",
            "value": reads["struck"]["avg"],
            "study_value": sum(gm_study) / len(gm_study),
            "study_value_range": [min(gm_study), max(gm_study)],
            "study_first_year": gm_study[0],
            "solved_on": (
                "this study's own model: the committed revenue, opex, depreciation, "
                "effective tax, capex and working-capital paths, the cost-of-capital "
                "glide, the value-driver terminal and the six-line bridge all held "
                "exactly at their published values, with only the gross-margin path "
                "scaled until the model reproduces the traded price. The "
                "reconstruction is proved to return the published %.4f a share at a "
                "scale of 1.0 before any solving begins — a first attempt using a "
                "grown last-year free cash flow returned 18,025 against the study's "
                "terminal of 15,691 and was refused rather than shipped."
                % d["dcf"]["ps"]),
            "at_prices": reads,
            "reading": "",
        },
        "reconstruction_check": {"published_ps": d["dcf"]["ps"],
                                 "rebuilt_ps": check["ps"], "tolerance": TOL_PS},
    }

    h1 = filed.get("6M Jun-2026")
    st = out["implied"]["study_value"]
    lines = ["At the EGP %.2f this study was struck at, the price is paying for an "
             "average gross margin of %.2f%% across the explicit window, against the "
             "%.2f%% the study forecasts."
             % (struck, reads["struck"]["avg"] * 100, st * 100)]
    if live is not None:
        lines.append(
            "At EGP %.2f the price is paying for %.2f%%." % (live, reads["latest_supplied"]["avg"] * 100))
    if h1:
        lines.append(
            "THE COMPANY'S OWN LATEST FILED HALF-YEAR MARGIN IS %.2f%% (six months to "
            "30 June 2026), against %.2f%% for the prior full year. This study "
            "forecasts %.2f%% for 2026 itself and a path declining to %.2f%% by 2030. "
            "So the disagreement is not about the valuation machinery: the market is "
            "paying for a margin BETWEEN this study's forecast and the one the company "
            "has just reported, and the study assumes a sharp reversion inside a year "
            "that is already half filed. Whether that reversion is right is a question "
            "about the refining spread, answerable from the second-half accounts, and "
            "it is the single thing to check before concluding the market is wrong."
            % (h1 * 100, fy25 * 100, gm_study[0] * 100, gm_study[-1] * 100))
    out["implied"]["reading"] = " ".join(lines)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(out["implied"]["reading"])
    print("\nwrote %s" % os.path.relpath(OUT, os.path.dirname(os.path.dirname(HERE))))
    return out


if __name__ == "__main__":
    import sys
    main(float(sys.argv[1]) if len(sys.argv) > 1 else None)
