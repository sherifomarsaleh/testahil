"""The mechanical fair value at each past origin, and log(FV/P) against the price
it would have been struck at.  [R-VCAL-01], series (a), score (i).

The construction is fixed in MECHANICAL_LENS_03-09-2026.md, which was sealed
before any value here was computed. Nothing in this module chooses anything: it
reads the walk-forward's own projection at each origin, the point-in-time macro
archive, the footed share count for that year, and the close on or before that
year end, and does the arithmetic the declaration describes.

WHAT IT IS NOT. Not the house method — the delivered studies value a developer on
a cash-flow model with an RNAV cross-check, a bridge and a dozen judgements, none
of which can be rebuilt at a past origin without a person, and a person at a past
origin is exactly what this removes. The LEVEL of these numbers therefore carries
much less than their BEHAVIOUR ACROSS ORIGINS, and the report says so beside every
level it prints.
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, HERE)

import macro_history as MH   # noqa: E402
import panel as P            # noqa: E402

BETA = 1.00          # fixed in the sealed declaration, every name, every origin
REAL_G = 0.0         # fixed in the sealed declaration
HORIZONS = (1, 2, 3, 4, 5)


def cost_of_equity(market, origin):
    """Ke and the terminal growth, from the archive at that origin and nothing else."""
    v = MH.origin(market, origin)
    need = v.require("sovereign_10y", "default_spread", "erp")
    rf_star = need["sovereign_10y"] - need["default_spread"]
    ke = rf_star + BETA * need["erp"]
    # terminal inflation: the vintage's OWN forecast for the last projected year,
    # never a later reading of it
    fwd = (v.extras.get("cpi_annual") or {}).get("forward_path") or {}
    last = str(origin + max(HORIZONS))
    infl = fwd.get(last)
    if infl is None and fwd:
        infl = fwd[max(fwd, key=lambda k: int(k))]
    g = None if infl is None else float(infl) + REAL_G
    return {"ke": ke, "rf_star": rf_star, "g": g,
            "sovereign_10y": need["sovereign_10y"],
            "default_spread": need["default_spread"], "erp": need["erp"],
            "terminal_inflation": infl}


def project_phdc(origin):
    sys.path.insert(0, os.path.join(ENGINE, "phdc_walkforward"))
    import bottom_up as B
    cwd = os.getcwd()
    try:
        os.chdir(os.path.join(ENGINE, "phdc_walkforward"))
        panel = B.load()
        r = B.project(panel, origin, macro="as_known")
    finally:
        os.chdir(cwd)
    return {h: (r.get(h) or {}).get("is.npat_mi") for h in HORIZONS}


PROJECTORS = {"PHDC": project_phdc}


def value(profits, ke, g):
    """Five discounted profits and a perpetuity, at one rate. Nothing else."""
    if g is None or ke - g <= 0:
        return None, "ke %.4f is not above terminal growth %s — dropped, not floored" \
                     % (ke, "unknown" if g is None else "%.4f" % g)
    pv = 0.0
    for h in HORIZONS:
        p = profits.get(h)
        if p is None:
            return None, "the projection has no net profit at horizon %d" % h
        pv += p / (1 + ke) ** h
    last = profits[max(HORIZONS)]
    tv = last * (1 + g) / (ke - g)
    pv += tv / (1 + ke) ** max(HORIZONS)
    return pv, "five profits plus a perpetuity, discounted at %.4f" % ke


def run(market="EG"):
    cells, names, declared, usable = P.build(market)
    rows, dropped = [], []
    for (tk, y), c in sorted(cells.items()):
        if not c["ready"]:
            continue
        if tk not in PROJECTORS:
            dropped.append((tk, y, "no projector wired for this name"))
            continue
        try:
            coc = cost_of_equity(market, y)
        except MH.VintageMissing as exc:
            dropped.append((tk, y, str(exc)[:90]))
            continue
        prof = PROJECTORS[tk](y)
        eq, why = value(prof, coc["ke"], coc["g"])
        if eq is None:
            dropped.append((tk, y, why))
            continue
        per_share = eq / c["shares"]
        px = c["price"]
        rows.append({"ticker": tk, "origin": y, "fv": per_share, "price": px,
                     "log": math.log(per_share / px) if per_share > 0 else None,
                     "ke": coc["ke"], "g": coc["g"], "shares_mn": c["shares"],
                     "equity": eq, "price_date": c["price_date"]})
    return rows, dropped


def report(market="EG"):
    rows, dropped = run(market)
    print("mechanical fair value at each past origin — [R-VCAL-01] series (a)\n")
    print("  construction sealed in MECHANICAL_LENS_03-09-2026.md before any of "
          "this was computed\n")
    if not rows:
        print("  no cell produced a value.")
    else:
        print("  %-6s %-7s %9s %9s %8s %8s %8s"
              % ("name", "origin", "fair/sh", "close", "gap %", "Ke", "g"))
        for r in rows:
            print("  %-6s %-7d %9.3f %9.3f %+7.1f%% %7.2f%% %7.2f%%"
                  % (r["ticker"], r["origin"], r["fv"], r["price"],
                     (r["fv"] / r["price"] - 1) * 100, r["ke"] * 100, r["g"] * 100))
        xs = [r["log"] for r in rows if r["log"] is not None]
        if xs:
            mean = sum(xs) / len(xs)
            xs_s = sorted(xs)
            med = (xs_s[len(xs)//2] if len(xs) % 2
                   else (xs_s[len(xs)//2-1] + xs_s[len(xs)//2]) / 2)
            print("\n  CONTEMPORANEOUS AGREEMENT over %d origin(s)" % len(xs))
            print("    mean log(FV/P)  %+.4f  (%+.1f%%)"
                  % (mean, (math.exp(mean) - 1) * 100))
            print("    median          %+.4f  (%+.1f%%)"
                  % (med, (math.exp(med) - 1) * 100))
            print("    below the price %d of %d" % (sum(1 for x in xs if x < 0), len(xs)))
    if dropped:
        print("\n  dropped (%d):" % len(dropped))
        for tk, y, why in dropped:
            print("    %-6s %d  %s" % (tk, y, why[:100]))
    print("\n  READ THE BEHAVIOUR, NOT THE LEVEL. This is one fixed construction,")
    print("  not the house method, and its absolute level is not a house fair value.")
    print("  With this few origins on one name, nothing here is a finding yet — it is")
    print("  an instrument returning its first readings, and the honest thing to")
    print("  report is how few of them there are.")
    return rows, dropped


if __name__ == "__main__":
    report()
