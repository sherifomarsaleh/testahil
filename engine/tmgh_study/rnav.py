"""TMGH — the RNAV lens the class requires, and the land the DCF credits at zero.

WHY THIS EXISTS.  The standing rule is `LENS BY CLASS: RE developer ->
SOTP/RNAV`.  The study shipped four cases that were two cost-of-capital bases
crossed with two readings of one DCF — one lens with four settings, not four
lenses — and the word "land" appeared nowhere in any of them.  Every gate passed
it, because `assert_model_study()` checks that the sixteen sections and sixteen
sheets are present and never asks whether the VALUATION METHOD matches the
class.  Structure verified, substance unexamined: the [R-SANITY-01] species one
level up.

WHAT THE DCF MISSES.  It monetises land only as it is built on inside the
window.  TMG holds 20mn sqm.  At the delivery rate the projection carries, that
is decades of inventory, and everything past the window is credited at nothing.
A developer's landbank is not a residual — for this class it is the asset.

THE ONE INPUT THAT IS NOT SOURCED, AND IT IS THE CRUX.  TMG discloses the
landbank's AREA (20mn sqm, 1H2026 release) and does not disclose what it is
worth, what it paid, or how it splits by project — the release's project pages
are scanned graphics and carry no land figures at all.  No price per square
metre for Egyptian new-city land is available from any company document.  Under
SIGCM that number may not be estimated into a headline, so it is carried as an
EXPLICIT INPUT, sensitised across a wide range, and REVERSE-SOLVED against the
market so a reader can see what price the market itself is paying.  The gap is
registered, not hidden.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import inputs as IN
import model as M
import valuation as VAL

# The land TMG says it holds. Company-sourced, area only.
LANDBANK_MSQM = IN.KPI["landbank_msqm"]["value"]
LANDBANK_SOURCE = IN.KPI["landbank_msqm"]["source"]

# What a square metre of it is worth. NOT SOURCED — the crux of this lens.
# The grid spans from a nominal raw-desert allocation to serviced new-city land,
# deliberately wide, because a narrow range here would imply a precision the
# disclosure does not support.
PRICE_GRID_EGP_PER_SQM = (0, 1000, 2000, 3500, 5000, 7500, 10000, 15000)

# Only part of a landbank is sellable: roads, services, parks and setbacks are
# not. TMG does not disclose its ratio, so this too is stated and sensitised.
SELLABLE_SHARE = 0.35
SELLABLE_GRID = (0.25, 0.35, 0.45)


def _v(d, k):
    return d[k]["value"]


def net_non_land_equity(mode="capacity", basis="rating"):
    """Everything the RNAV needs that is NOT land, taken from the DCF's own
    bridge so the two lenses cannot disagree about cash, debt or the minority."""
    w = json.load(open(os.path.join(HERE, "wacc.json")))
    import wacc as WC
    b = WC.beta_record()["beta"]
    rate = WC.wacc_country_risk_once(
        w["rf_star_%s" % basis], b,
        WC.CRP_RATING if basis == "rating"
        else WC.DAMODARAN_EGYPT["sovereign_cds"],
        w["weight_equity"], w["weight_debt"], w["kd_aftertax"])[0]
    d = VAL.sotp(mode, rate)
    return d, rate


def rnav(price_per_sqm, sellable=SELLABLE_SHARE, mode="capacity",
         basis="rating"):
    """The DCF's equity value, plus the land it never credited.

    The development business is valued as the DCF values it — that projection
    already consumes the land it builds on inside the window. What is added is
    the REMAINDER: the bank net of what the window uses. Adding the whole bank
    on top would count the same square metres twice.
    """
    d, rate = net_non_land_equity(mode, basis)
    # NO CONSUMPTION MODEL, BECAUSE THE DISCLOSURE CANNOT SUPPORT ONE.
    # A first cut netted off the land the projection builds on, sizing it with
    # revenue per square metre taken as the backlog over the bank. That anchor
    # is wrong: the EGP 491bn book is for units ALREADY SOLD, sitting on land
    # already committed, while the 20mn sqm is what REMAINS. The two do not
    # divide into each other, and TMG discloses no revenue per square metre of
    # land, so the overlap between the window's build-out and the bank cannot
    # be quantified from anything the company publishes.
    #
    # Rather than invent the link, the lens states the whole bank's value at a
    # given price and says plainly that some of it is already inside the DCF.
    # That makes this an UPPER bound on the addition, and the study says so —
    # a stated bound is honest; a fabricated netting is not.
    sellable_sqm = LANDBANK_MSQM * 1e6 * sellable
    land_value = sellable_sqm * price_per_sqm / 1e6      # EGP mn
    sh = _v(IN.KPI, "shares_outstanding")
    nci = _v(IN.BS, "nci_equity") / _v(IN.BS, "total_equity")
    add_per_share = land_value * (1 - nci) / sh
    return {
        "price_per_sqm": price_per_sqm, "sellable_share": sellable,
        "mode": mode, "basis": basis, "wacc_start": rate,
        "dcf_per_share": d["per_share_nci_book"],
        "sellable_sqm": sellable_sqm,
        "land_value_egp_mn": land_value,
        "land_per_share": add_per_share,
        "rnav_upper_per_share": d["per_share_nci_book"] + add_per_share,
        "overlap_note": ("an UPPER bound: part of this land is already built on "
                         "inside the DCF window and is therefore counted twice. "
                         "The overlap cannot be sized from disclosure."),
    }


def implied_price(target, mode="capacity", basis="rating"):
    """What price per square metre the market is paying for the remainder."""
    base = rnav(0.0, mode=mode, basis=basis)
    sh = _v(IN.KPI, "shares_outstanding")
    nci = _v(IN.BS, "nci_equity") / _v(IN.BS, "total_equity")
    need = (target - base["dcf_per_share"]) * sh / (1 - nci) * 1e6
    return need / base["sellable_sqm"]


def build():
    import wacc as WC
    out = {
        "landbank_msqm": LANDBANK_MSQM,
        "landbank_source": LANDBANK_SOURCE,
        "sellable_share": SELLABLE_SHARE,
        "gap": ("No price per square metre for TMG's land is disclosed by the "
                "company, and its project pages carry no land figures. The "
                "price is therefore an explicit input, sensitised, and "
                "reverse-solved against the market price. Closed by: a land "
                "valuation, a disclosed land carrying value by project, or "
                "transacted comparables for new-city land."),
        "grid": {}, "implied_by_market": {},
    }
    for basis in ("rating", "cds"):
        for mode in ("capacity", "recovery"):
            for p in PRICE_GRID_EGP_PER_SQM:
                r = rnav(p, mode=mode, basis=basis)
                out["grid"]["%s|%s|%d" % (basis, mode, p)] = r
            out["implied_by_market"]["%s|%s" % (basis, mode)] = implied_price(
                WC.SPOT, mode=mode, basis=basis)
    json.dump(out, open(os.path.join(HERE, "rnav.json"), "w"), indent=1)
    return out


def main():
    import wacc as WC
    o = build()
    print("RNAV — the DCF plus the land it does not credit\n")
    print("landbank %.1f mn sqm, of which %.0f%% taken as sellable = %.1f mn "
          "sqm.\nAn UPPER bound: part is already built on inside the DCF and "
          "the overlap is not disclosable.\n"
          % (o["landbank_msqm"], 100 * o["sellable_share"],
             o["grid"]["rating|capacity|0"]["sellable_sqm"] / 1e6))
    print("%-14s %10s %10s %10s %10s" % ("EGP/sqm", "slower", "faster",
                                         "slower CDS", "faster CDS"))
    for p in PRICE_GRID_EGP_PER_SQM:
        print("%-14s %10.2f %10.2f %10.2f %10.2f"
              % (("%d" % p) if p else "0 (DCF only)",
                 o["grid"]["rating|capacity|%d" % p]["rnav_upper_per_share"],
                 o["grid"]["rating|recovery|%d" % p]["rnav_upper_per_share"],
                 o["grid"]["cds|capacity|%d" % p]["rnav_upper_per_share"],
                 o["grid"]["cds|recovery|%d" % p]["rnav_upper_per_share"]))
    print("\nwhat the market price of EGP %.2f implies for the remaining land:"
          % WC.SPOT)
    for k, v in o["implied_by_market"].items():
        print("  %-18s EGP %8.0f per sqm" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
