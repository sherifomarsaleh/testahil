"""The mechanical fair value at each past origin, and log(FV/P) against the price
it would have been struck at.  [R-VCAL-01], series (a), score (i).

The construction is fixed in MECHANICAL_LENS_2_03-09-2026.md, sealed before any
value under it was computed. It supersedes the first declaration, whose own first
run is committed unaltered in FIRST_RUN_SEALED_LENS_03-09-2026.json — that run
discounted accounting net profit into a perpetuity on a developer, which
[R-LENS-03] forbids outright, and it read two to seven times the traded price at
every origin. The rule was available before the lens was declared and was missed. Nothing in this module chooses anything: it
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
HORIZONS = (1, 2, 3, 4, 5)

# Declaration 2. Every one of these is fixed in the sealed document and none is
# fitted; they are here so the arithmetic can be read beside the text that fixed it.
DELIVERY_YEARS = 4       # the contracted book converts to profit evenly over four
TAX = 0.225              # statutory
MARGIN_YEARS = 3         # the median reported gross margin of the three years to t


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
    # Declaration 2 has NO TERMINAL VALUE, so terminal growth is not an input to
    # the lens at all. The vintage's own forward inflation is still carried in the
    # record, because it is what the origin knew and a later reader will want it.
    g = None if infl is None else float(infl)
    return {"ke": ke, "rf_star": rf_star, "g": g,
            "sovereign_10y": need["sovereign_10y"],
            "default_spread": need["default_spread"], "erp": need["erp"],
            "terminal_inflation": infl}


def project_phdc(origin):
    """The projection at one origin, plus the reported margins the lens needs."""
    sys.path.insert(0, os.path.join(ENGINE, "phdc_walkforward"))
    import bottom_up as B
    cwd = os.getcwd()
    try:
        os.chdir(os.path.join(ENGINE, "phdc_walkforward"))
        panel = B.load()
        r = B.project(panel, origin, macro="as_known")
        raw = json.load(open("panel.json", encoding="utf-8"))
    finally:
        os.chdir(cwd)
    # the company's OWN realised gross margin in the three years to the origin,
    # read as reported and never from a forecast
    margins = []
    for y in range(origin - MARGIN_YEARS + 1, origin + 1):
        rec = raw.get(str(y)) or {}
        gp = (rec.get("is.gross_profit") or {}).get("value")
        rev = (rec.get("is.revenue") or {}).get("value")
        if gp and rev and rev > 0:
            margins.append(gp / rev)
    return {"backlog": {h: (r.get(h) or {}).get("backlog") for h in HORIZONS},
            "_margins": margins}


PROJECTORS = {"PHDC": project_phdc}


def backlog_value(tk, origin, ke, panel_years):
    """The present value of the company's own contracted order book. No terminal.

    A developer's backlog is revenue already sold and not yet delivered. Converting
    it at the company's OWN realised gross margin over a fixed delivery period and
    discounting at the point-in-time cost of equity is the present-value RNAV shape
    [R-LENS-03] gives the class — and it is a FLOOR, because nothing is added for
    land, options or recurring assets. That downward bias is stated, not hidden.
    """
    bl = (panel_years.get("backlog") or {}).get(1)
    if not bl:
        return None, "the projection carries no backlog at this origin"
    margins = panel_years.get("_margins") or []
    if len(margins) < MARGIN_YEARS:
        return None, ("only %d reported gross margin(s) in the three years to the "
                      "origin; the median needs %d" % (len(margins), MARGIN_YEARS))
    margins = sorted(margins)
    med = margins[len(margins) // 2]
    if not (0 < med < 1):
        return None, "the reported gross margin of %.4f is not a usable rate" % med
    annual = bl * med * (1 - TAX) / DELIVERY_YEARS
    pv = sum(annual / (1 + ke) ** h for h in range(1, DELIVERY_YEARS + 1))
    return pv, ("backlog %.0f at a median reported margin of %.1f%% over %d years, "
                "after tax, discounted at %.2f%% — no terminal, no land"
                % (bl, med * 100, DELIVERY_YEARS, ke * 100))


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
        proj = PROJECTORS[tk](y)
        eq, why = backlog_value(tk, y, coc["ke"], proj)
        if eq is None:
            dropped.append((tk, y, why))
            continue
        per_share = eq / c["shares"]
        px = c["price"]
        rows.append({"ticker": tk, "origin": y, "fv": per_share, "price": px,
                     "log": math.log(per_share / px) if per_share > 0 else None,
                     "ke": coc["ke"], "g": coc["g"], "shares_mn": c["shares"],
                     "equity": eq, "price_date": c["price_date"], "how": why})
    return rows, dropped


def report(market="EG"):
    rows, dropped = run(market)
    print("mechanical fair value at each past origin — [R-VCAL-01] series (a)\n")
    print("  construction sealed in MECHANICAL_LENS_2_03-09-2026.md before any of\n"
          "  this was computed; the withdrawn first declaration and its own run are\n"
          "  committed beside it, unedited\n")
    if not rows:
        print("  no cell produced a value.")
    else:
        print("  %-6s %-7s %9s %9s %8s %8s"
              % ("name", "origin", "floor/sh", "close", "gap %", "Ke"))
        for r in rows:
            print("  %-6s %-7d %9.3f %9.3f %+7.1f%% %7.2f%%"
                  % (r["ticker"], r["origin"], r["fv"], r["price"],
                     (r["fv"] / r["price"] - 1) * 100, r["ke"] * 100))
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
    print("\n  THIS IS A FLOOR, NOT A FAIR VALUE. It values the contracted order book")
    print("  and nothing else — no land, no options, no recurring assets — so a")
    print("  reading BELOW the price is the expected case and says little on its own.")
    print("  What carries information is how the gap MOVES across origins.")
    print("  With this few origins on one name, nothing here is a finding yet — it is")
    print("  an instrument returning its first readings, and the honest thing to")
    print("  report is how few of them there are.")
    return rows, dropped


if __name__ == "__main__":
    report()
