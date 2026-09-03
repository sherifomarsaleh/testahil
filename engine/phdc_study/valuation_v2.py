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
# The bridge stands on the latest disclosed balance sheet (31-Mar-2026, reviewed),
# not on the FY2025 sheet the projection starts from — GAP_REVIEW_01-09-2026 §6.
BS = BU.BS_BRIDGE
NET_DEBT = BU.NET_DEBT_BRIDGE
NCI_SHARE = BU.NCI_VALUE_SHARE   # minority at its share of value, never at book
SPOT = REG["spot"]

# [R-MACRO-01] Terminal growth is NOT chosen here. It is the house path's terminal
# inflation plus a STATED real growth, and the real growth is zero: the company is
# assumed to hold its real size for ever and to grow with prices alone. Earlier
# editions carried 12% against a terminal rate embedding about 14.6% inflation,
# which is a perpetual real DECLINE of two to three points a year that nothing
# disclosed supports and no reader was told about [L-055].
import macro_path as MP
PATH = MP.load("EG")
TERMINAL_REAL_GROWTH = 0.0
TG = PATH.terminal_growth(TERMINAL_REAL_GROWTH)

# [R-COC-01] the committed SCHEDULE, read back rather than recomputed
import cost_of_capital as COC
SCHEDULES = {b: COC.Schedule.from_record(W["schedule"][b]) for b in ("rating", "cds")}


def error_band(field, h):
    """The p10/p50/p90 of this method's OWN error at that horizon."""
    d = WF["years"].get(field, {}).get(str(h))
    if not d or not d["raw_projection"]:
        return None
    raw = d["raw_projection"]
    return (d["p10"] / raw, d["central_after_record_median"] / raw, d["p90"] / raw)


def ranged_revenue():
    """Years three to five as low / point / high, from the measured record.

    Beyond year five the walk-forward record has no measured error, so those years
    carry a point and no range rather than an extrapolated one."""
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


def dcf(cfo_margin, sched):
    """Discount the cash the profit path actually produces.

    Cash conversion stays the crux: the profit above is an accrual figure and
    the company's own cash-flow statements put operating cash between 3.9% and
    17.9% of revenue, so the cash leg is run across that observed range.
    """
    dc = COC.Discounter(sched)
    wacc = sched.wacc_exp
    pv = 0.0
    for i, r in enumerate(ROWS, start=1):
        cfo = r["revenue"] * cfo_margin
        fcff = cfo + r["interest"] * (1 - BU.TAX) - r["revenue"] * 0.01
        pv += fcff * dc.factor(i)
    last = ROWS[-1]
    tail = (last["revenue"] * cfo_margin + last["interest"] * (1 - BU.TAX)
            - last["revenue"] * 0.01)
    # capitalised at the TERMINAL rate, which is the rate that applies when it is
    # struck, and brought home on the window's OWN factor -- one date, one price
    # of time. Capitalising at the explicit-window rate gives the same pound
    # arriving on the same day two different values.
    pv_tv = tail * dc.perpetuity_factor(TG)
    tv = pv_tv / dc.factor(len(ROWS))
    ev = pv + pv_tv
    eq_gross = ev - NET_DEBT + BS["investments_assoc"] + BS["investment_property"]
    nci = eq_gross * NCI_SHARE       # the minority's share of the value, not its book
    eq = eq_gross - nci
    return {"pv_explicit": pv, "pv_terminal": pv_tv, "ev": ev,
            "equity_before_nci": eq_gross, "nci_deduction": nci, "equity": eq,
            "per_share": eq / SHARES, "terminal_share": pv_tv / ev if ev else None,
            "cfo_margin": cfo_margin, "wacc": wacc,
            "wacc_terminal": sched.wacc_terminal,
            "forward_wacc": list(sched.forward_wacc),
            "discount_factors": list(sched.discount_factors)}


def run(cfo_margin, sched, terminal_growth=TG):
    """The same discounted cash flow, in the shape the workbook and the case
    tables read. One model, one set of figures: the study used to carry a
    ten-year capacity-ratio valuation beside this one and publish both as
    "fundamental value", which put two different ranges in one document.
    """
    d = dcf(cfo_margin, sched)
    wacc = sched.wacc_exp
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
    S = SCHEDULES["rating"]
    cfos = [L["lo"], 0.060, L["mid"], 0.120, L["hi"]]
    shifts = [-0.04, -0.02, 0.0, 0.02, 0.04]
    scheds = [S if d == 0.0 else S.shifted(d) for d in shifts]
    waccs = [sc.wacc_exp for sc in scheds]
    return waccs, [(c, [run(c, sc)["per_share"] for sc in scheds]) for c in cfos]


def implied_conversion(spot, sched):
    """The conversion rate the market is paying for, solved on THIS model."""
    lo, hi = 0.001, 0.40
    for _ in range(96):
        m = (lo + hi) / 2
        if run(m, sched)["per_share"] < spot:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def lenses():
    lo = BU.REG["cfo_fy25"] / BU.REG["revenue_fy25"]
    hi = BU.REG["cfo_fy24"] / BU.REG["revenue_fy24"]
    mid = (lo + hi + BU.REG["cfo_fy23"] / BU.REG["revenue_fy23"]) / 3.0

    # the bear and full cases shift the WHOLE schedule, keeping its shape: replacing
    # it with a flat rate would ask two questions at once, and the second one is the
    # assumption the schedule exists to remove
    S = SCHEDULES["rating"]
    d_bear = dcf(lo, S.shifted(0.02))
    d_base = dcf(mid, S)
    d_full = dcf(hi, S.shifted(-0.01))
    # book value on the SAME numerator as the share count: equity attributable
    # to the parent, on the latest disclosed sheet (the 30-Aug edition divided
    # TOTAL equity, minority included, by parent shares)
    book = BS["equity_parent"] / SHARES

    # earnings multiple on the company's OWN history, not on peers: the shares
    # have traded between roughly 6x and 14x trailing earnings over five years
    eps26 = ROWS[0]["npat"] / SHARES
    mult = {"bear": 6.0, "base": 9.0, "full": 14.0}
    rel = {k: eps26 * m for k, m in mult.items()}

    # normalised earnings power: mid-cycle margin on mid-cycle revenue,
    # capitalised at the cost of equity LESS the same terminal growth the
    # cash-flow model carries. The 30-Aug edition capitalised at E / ke — zero
    # nominal growth against a cost of equity that embeds 14-15% inflation,
    # which is a perpetual real decline of about 13% a year, undisclosed
    # (GAP_REVIEW_01-09-2026 §5). One clock: the growth netted here is the
    # DCF's own TG, so the two lenses assume the same future.
    norm_rev = (REG["revenue_fy24"] + REG["revenue_fy25"]) / 2 * (1 + BU.CPI)
    norm_margin = REG["npat_mi_fy25"] / REG["revenue_fy25"]
    norm_earn = norm_rev * norm_margin
    nep = {k: norm_earn / (W["ke_rating"] + adj - TG) / SHARES
           for k, adj in (("bear", 0.03), ("base", 0.0), ("full", -0.03))}

    # [R-LENS-03] ONE PRIMARY IS THE CENTRAL; THE REST ARE CROSS-CHECKS.
    #
    # The 30-Aug and 02-Sep editions published a weighted blend of four lenses at
    # typed weights — 45/15/20/20 — and three of the four value a developer on its
    # reported accounting earnings and its historical-cost book. For a company
    # whose value sits in an undelivered order book carried at historical cost, in
    # a currency that has lost most of its value since 2022, those three measure a
    # FLOOR and not a value. The weights had never cleared any out-of-sample test.
    #
    # Normalised earnings power is dropped as a lens entirely, not re-weighted: a
    # developer recognising revenue on completion reports earnings that are an
    # accident of which project completed in which year, and capitalising a
    # mid-cycle figure treats that schedule as a steady state. The working is kept
    # below as a disclosed diagnostic and carries no value claim.
    rows = [
        ("Discounted cash flow", d_bear["per_share"], d_base["per_share"],
         d_full["per_share"], None),
        ("Earnings multiple on own history", rel["bear"], rel["base"],
         rel["full"], None),
        ("Book value of equity — a disclosed floor", book * 0.9, book, book * 1.3, None),
    ]
    # the envelope is the RANGE of the present-value reads, never an average
    pv_reads = [d_bear["per_share"], d_base["per_share"], d_full["per_share"],
                rel["bear"], rel["base"], rel["full"]]
    w = {"bear": min(pv_reads), "base": d_base["per_share"], "full": max(pv_reads)}
    return {"rows": rows, "weighted": w,
            "primary": {"kind": "dcf", "value": d_base["per_share"]},
            "envelope": {"low": min(pv_reads), "high": max(pv_reads)},
            "normalised_diagnostic": nep,
            "dcf": {"bear": d_bear, "base": d_base, "full": d_full},
            "book": book, "relative": rel, "normalised": nep,
            "normalised_inputs": {"norm_rev": norm_rev, "norm_margin": norm_margin,
                                  "norm_earn": norm_earn, "ke": W["ke_rating"],
                                  "growth_netted": TG,
                                  "as_30aug_edition_e_over_ke": norm_earn / W["ke_rating"] / SHARES},
            "book_reference": {"total_equity_fy25_over_parent_shares": REG["total_equity"] / SHARES,
                               "parent_equity_1q26_over_parent_shares": book},
            "cfo": {"lo": lo, "mid": mid, "hi": hi}}


def bridge(case):
    d = case
    n = len(ROWS)
    return [("Present value of the explicit %d years" % n, d["pv_explicit"]),
            ("Present value beyond year %d" % n, d["pv_terminal"]),
            ("Enterprise value", d["ev"]),
            ("less net debt, 31 March 2026", -NET_DEBT),
            ("plus investments in associates", BS["investments_assoc"]),
            ("plus investment property", BS["investment_property"]),
            ("Equity value before minority interests", d["equity_before_nci"]),
            ("less minority interests at their share of value", -d["nci_deduction"]),
            ("Equity value attributable to shareholders", d["equity"]),
            ("Shares outstanding, millions", SHARES),
            ("Value per share, EGP", d["per_share"])]


if __name__ == "__main__":
    L = lenses()
    print("ONE PRIMARY, THE REST CROSS-CHECKS  (EGP per share)")
    print("%-44s %8s %8s %8s" % ("Lens", "Bear", "Base", "Full"))
    for nm, b, ba, f, _ in L["rows"]:
        print("%-44s %8.2f %8.2f %8.2f" % (nm, b, ba, f))
    print("%-44s %8s %8.2f %8s"
          % ("CENTRAL — the cash-flow lens", "", L["primary"]["value"], ""))
    print("%-44s %8.2f %8s %8.2f"
          % ("envelope of the present-value reads", L["envelope"]["low"], "",
             L["envelope"]["high"]))
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
