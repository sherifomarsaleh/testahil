"""The country risk premium, split out of the total — LEVER 4.

I RECORDED THIS LEVER UNBUILDABLE AND THAT WAS WRONG, and the correction is worth
more than the lever. The point-in-time archive holds Egypt's TOTAL equity premium
per vintage on two bases and no mature-market figure, and I concluded from that one
look that the split could not be recovered. It can, exactly, because TWO BASES ARE
TWO EQUATIONS:

    erp_rating = ERP_mature + default_spread_rating x lambda
    erp_cds    = ERP_mature + cds_spread_net_of_us  x lambda

Two unknowns, solved per vintage. The check is not internal: the recovered mature
premium reproduces Damodaran's OWN published implied premium for the S&P 500 to four
decimal places at eight of the eleven solvable vintages and to within 22 basis points
at the other three. A derivation that lands on a number somebody else published
independently is not a coincidence.

    2014  lambda 1.5000  mature 0.0575   published 0.0578
    2016  lambda 1.2305  mature 0.0569   published 0.0569
    2019  lambda 1.1796  mature 0.0520   published 0.0520
    2021  lambda 1.1623  mature 0.0424   published 0.0424
    2023  lambda 1.3424  mature 0.0460   published 0.0455

Verified independently against a held ctryprem workbook, which publishes all three
quantities as separate cells for the 2026 vintage and reproduces the identity to the
sixth decimal: mature 0.0423, lambda 1.5234, Egypt's country premium 0.097077 against
a rating default spread of 0.063725.

WHAT THE LEVER IS. [R-COC-01] says the country premium's lambda DEFAULTS TO 1.00 and
any other value is a stated judgement published beside the equity-to-bond scaling it
is an alternative to. The declared run inherits Damodaran's OWN lambda silently,
because it consumes his total premium — 1.10 to 1.50 across these vintages, never
1.00, and never stated anywhere. So the lever is not "invent a lambda"; it is "apply
the house default the protocol already names, and see".

THE GENERAL LESSON, AND IT IS ABOUT PROBES RATHER THAN PREMIUMS: an absent FIELD is
not an absent QUANTITY. The first probe asked whether the archive stored a mature
premium, found none, and reported unbuildable — an absent answer wearing a clean
answer's clothes [R-ENF-04], from a probe that was looking for a column rather than
for the number.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
_EXTRACT = os.path.join(ENGINE, "macro_history", "_extract_damodaran_egypt.json")
HOUSE_LAMBDA = 1.00      # [R-COC-01]'s stated default, not a figure chosen here
_D = None


def _load():
    global _D
    if _D is None:
        with open(_EXTRACT) as f:
            _D = json.load(f)
    return _D


def split(vintage):
    """(mature_erp, lambda, default_spread_rating) at a vintage, or None.

    A vintage publishing only ONE basis cannot be solved and returns None rather
    than a guess — one equation in two unknowns has no answer and inventing the
    missing one would put a chosen number where a derived one belongs.
    """
    r = _load().get(str(vintage))
    if not r:
        return None
    er, ds = r.get("erp_rating"), r.get("default_spread_rating")
    ec, dc = r.get("erp_cds"), r.get("cds_spread_net_of_us")
    if None in (er, ds, ec, dc) or abs(ds - dc) < 1e-9:
        return None
    lam = (er - ec) / (ds - dc)
    return {"mature_erp": er - ds * lam, "lambda_damodaran": lam,
            "default_spread_rating": ds, "cds_spread": dc,
            "erp_rating": er, "erp_cds": ec}


def erp_at(vintage, lam=HOUSE_LAMBDA, basis="cds"):
    """The total equity premium rebuilt at a STATED lambda, on one basis.

    Rating-to-rating and CDS-to-CDS: the spread that scales must be the spread the
    risk-free is normalised by, or the sovereign is counted on two measuring sticks.
    """
    s = split(vintage)
    if s is None:
        return None, None
    spread = s["default_spread_rating"] if basis == "rating" else s["cds_spread"]
    return s["mature_erp"] + spread * lam, spread


if __name__ == "__main__":
    print("vintage  lambda(Damodaran)  mature ERP   ERP at house lambda=1.00 (cds basis)")
    for y in sorted(_load(), key=int):
        s = split(y)
        if s is None:
            print("  %s   only one basis — not solvable" % y)
            continue
        e, _ = erp_at(y, HOUSE_LAMBDA, "cds")
        print("  %s        %6.4f        %6.4f       %6.4f   (declared run uses %6.4f)"
              % (y, s["lambda_damodaran"], s["mature_erp"], e, s["erp_cds"]))
