"""Value PHDC off the units-and-prices forecast, with every step shown.

Four lenses, weighted, in the house form: a discounted cash flow on the
bottom-up profit path, book value, an earnings multiple on the company's own
history, and normalised earnings power. Years three to five are published as
RANGES taken from this method's measured error on Palm Hills' own 2011-2025
history, not as points.
"""
import json, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import inputs as IN
import bottom_up_model as BU

REG = BU.REG
W = json.load(open(os.path.join(HERE, "wacc_result.json")))
WF = json.load(open(os.path.join(os.path.dirname(HERE), "phdc_walkforward",
                                 "forward_ranges.json")))

M = BU.build()
ROWS = M["rows"]
SHARES = BU.SHARES_MN
NET_DEBT = BU.NET_DEBT
SPOT = REG["spot"]
TG = 0.12                        # terminal growth, below nominal growth


def error_band(field, h):
    """The p10/p50/p90 of this method's OWN error at that horizon."""
    d = WF["years"].get(field, {}).get(str(h))
    if not d or not d["raw_projection"]:
        return None
    raw = d["raw_projection"]
    return (d["p10"] / raw, d["central_after_record_median"] / raw, d["p90"] / raw)


def ranged_revenue():
    """Years three to five as low / point / high, from the measured record."""
    out = []
    for h, r in zip(range(1, 6), ROWS):
        b = error_band("is.revenue", h)
        if h < 3 or not b:
            out.append({"year": r["year"], "point": r["revenue"],
                        "low": None, "high": None})
        else:
            out.append({"year": r["year"], "point": r["revenue"],
                        "low": r["revenue"] * b[0], "high": r["revenue"] * b[2]})
    return out


def dcf(cfo_margin, wacc):
    """Discount the cash the profit path actually produces.

    Cash conversion stays the crux: the profit above is an accrual figure and
    the company's own cash-flow statements put operating cash between 3.9% and
    17.9% of revenue, so the cash leg is run across that observed range.
    """
    pv = 0.0
    for i, r in enumerate(ROWS, start=1):
        cfo = r["revenue"] * cfo_margin
        fcff = cfo + r["interest"] * (1 - BU.TAX) - r["revenue"] * 0.01
        pv += fcff / (1 + wacc) ** i
    last = ROWS[-1]
    tail = (last["revenue"] * cfo_margin + last["interest"] * (1 - BU.TAX)
            - last["revenue"] * 0.01)
    tv = tail * (1 + TG) / (wacc - TG)
    pv_tv = tv / (1 + wacc) ** len(ROWS)
    ev = pv + pv_tv
    eq = ev - NET_DEBT + REG["investments_assoc"] + REG["investment_property"]
    return {"pv_explicit": pv, "pv_terminal": pv_tv, "ev": ev, "equity": eq,
            "per_share": eq / SHARES, "terminal_share": pv_tv / ev if ev else None,
            "cfo_margin": cfo_margin, "wacc": wacc}


def run(cfo_margin, wacc, terminal_growth=TG):
    """The same discounted cash flow, in the shape the workbook and the case
    tables read. One model, one set of figures: the study used to carry a
    ten-year capacity-ratio valuation beside this one and publish both as
    "fundamental value", which put two different ranges in one document.
    """
    d = dcf(cfo_margin, wacc)
    rows = []
    for r in ROWS:
        cfo = r["revenue"] * cfo_margin
        rows.append({"year": r["year"], "revenue": r["revenue"],
                     "gross": r["gross"], "npbt": r["npbt"],
                     "npat": r["npat"], "backlog": r["backlog"],
                     "cfo": cfo,
                     "fcff": cfo + r["interest"] * (1 - BU.TAX)
                     - r["revenue"] * 0.01})
    return {**d, "rows": rows,
            "inputs": {"cfo_margin": cfo_margin, "wacc": wacc,
                       "terminal_growth": terminal_growth}}


def sensitivity():
    """The crux, priced in real observable units.

    Value is dominated by one quantity whose mechanics the company does not
    disclose: how fast contracted sales convert to cash. Three disclosed
    cash-flow statements put it across a spread wide enough that it, not the
    discount rate, decides the answer.
    """
    L = lenses()["cfo"]
    wr = W["wacc_rating"]
    cfos = [L["lo"], 0.060, L["mid"], 0.120, L["hi"]]
    waccs = [wr - 0.04, wr - 0.02, wr, wr + 0.02, wr + 0.04]
    return waccs, [(c, [run(c, w)["per_share"] for w in waccs]) for c in cfos]


def implied_conversion(spot, wacc):
    """The conversion rate the market is paying for, solved on THIS model."""
    lo, hi = 0.001, 0.40
    for _ in range(96):
        m = (lo + hi) / 2
        if run(m, wacc)["per_share"] < spot:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def lenses():
    wr = W["wacc_rating"]
    lo = BU.REG["cfo_fy25"] / BU.REG["revenue_fy25"]
    hi = BU.REG["cfo_fy24"] / BU.REG["revenue_fy24"]
    mid = (lo + hi + BU.REG["cfo_fy23"] / BU.REG["revenue_fy23"]) / 3.0

    d_bear, d_base, d_full = dcf(lo, wr + 0.02), dcf(mid, wr), dcf(hi, wr - 0.01)
    book = REG["total_equity"] / SHARES

    # earnings multiple on the company's OWN history, not on peers: the shares
    # have traded between roughly 6x and 14x trailing earnings over five years
    eps26 = ROWS[0]["npat"] / SHARES
    mult = {"bear": 6.0, "base": 9.0, "full": 14.0}
    rel = {k: eps26 * m for k, m in mult.items()}

    # normalised earnings power: mid-cycle margin on mid-cycle revenue,
    # capitalised at the cost of equity
    norm_rev = (REG["revenue_fy24"] + REG["revenue_fy25"]) / 2 * (1 + BU.CPI)
    norm_margin = REG["npat_mi_fy25"] / REG["revenue_fy25"]
    norm_earn = norm_rev * norm_margin
    nep = {k: norm_earn / (W["ke_rating"] + adj) / SHARES
           for k, adj in (("bear", 0.03), ("base", 0.0), ("full", -0.03))}

    rows = [
        ("Discounted cash flow", d_bear["per_share"], d_base["per_share"],
         d_full["per_share"], 0.45),
        ("Book value of equity", book * 0.9, book, book * 1.3, 0.15),
        ("Earnings multiple on own history", rel["bear"], rel["base"],
         rel["full"], 0.20),
        ("Normalised earnings power", nep["bear"], nep["base"], nep["full"], 0.20),
    ]
    w = {k: sum(r[i] * r[4] for r in rows)
         for i, k in ((1, "bear"), (2, "base"), (3, "full"))}
    return {"rows": rows, "weighted": w,
            "dcf": {"bear": d_bear, "base": d_base, "full": d_full},
            "book": book, "relative": rel, "normalised": nep,
            "cfo": {"lo": lo, "mid": mid, "hi": hi}}


def bridge(case):
    d = case
    return [("Present value of the explicit five years", d["pv_explicit"]),
            ("Present value beyond year five", d["pv_terminal"]),
            ("Enterprise value", d["ev"]),
            ("less net debt", -NET_DEBT),
            ("plus investments in associates", REG["investments_assoc"]),
            ("plus investment property", REG["investment_property"]),
            ("Equity value", d["equity"]),
            ("Shares outstanding, millions", SHARES),
            ("Value per share, EGP", d["per_share"])]


if __name__ == "__main__":
    L = lenses()
    print("FOUR LENSES, ONE FIELD  (EGP per share)")
    print("%-36s %8s %8s %8s %8s" % ("Lens", "Bear", "Base", "Full", "Weight"))
    for nm, b, ba, f, wt in L["rows"]:
        print("%-36s %8.2f %8.2f %8.2f %7.0f%%" % (nm, b, ba, f, wt * 100))
    print("%-36s %8.2f %8.2f %8.2f %7.0f%%"
          % ("Weighted central", L["weighted"]["bear"], L["weighted"]["base"],
             L["weighted"]["full"], 100))
    print("%-36s %8.2f" % ("Market price, 23 Aug 2026", SPOT))
    print()
    print("BRIDGE — base case, every step")
    for lbl, val in bridge(L["dcf"]["base"]):
        print("  %-44s %12.1f" % (lbl, val))
    print()
    print("REVENUE, YEARS THREE TO FIVE AS RANGES (EGP mn)")
    print("  %-8s %12s %12s %12s" % ("year", "low", "point", "high"))
    for r in ranged_revenue():
        print("  %-8d %12s %12.0f %12s"
              % (r["year"], "-" if r["low"] is None else "%.0f" % r["low"],
                 r["point"], "-" if r["high"] is None else "%.0f" % r["high"]))
    json.dump({"lenses": {"rows": [list(r) for r in L["rows"]],
                          "weighted": L["weighted"], "cfo": L["cfo"],
                          "book": L["book"], "relative": L["relative"],
                          "normalised": L["normalised"]},
               "dcf": {k: v for k, v in L["dcf"].items()},
               "bridge": [list(x) for x in bridge(L["dcf"]["base"])],
               "ranged_revenue": ranged_revenue(),
               "model": M},
              open(os.path.join(HERE, "valuation_v2.json"), "w"), indent=1, default=str)
