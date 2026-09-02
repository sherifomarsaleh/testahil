"""TMGH valuation — one model, discounted; a sum-of-the-parts bridge to equity.

The lens is chosen by class: a real-estate developer is valued on a
sum-of-the-parts, and TMG is three businesses inside one holding — a
development platform recognising revenue on handover, a hospitality platform,
and a recurring-income leg of clubs, retail and community services.

Every cash flow discounted here comes out of `model.project`. There is one
model and one set of numbers [L-016]; the workbook, the statements and this
file all read it.

THE CRUX, AND IT IS PUBLISHED BOTH WAYS. TMG's disclosed order book is EGP
491.0bn at 30 June 2026 against 1H2026 development revenue of EGP 17.0bn —
about fourteen years of handovers at the current rate. The company's own
conversion rate has fallen from about 15% before 2023 to 5.4% in FY2025,
because DELIVERY IS CONSTRAINED BY CONSTRUCTION CAPACITY AND NOT BY THE SIZE OF
THE ORDER BOOK. Whether handovers converge on that book slowly or quickly
changes the answer materially, and it changes it in BOTH directions at once:
faster conversion recognises the margin sooner, and it also consumes cash
sooner, because a developer that accelerates handovers builds before it
collects. Neither reading can be dismissed from what the company discloses.
Both are computed and both are published; they are never averaged.

No margin is an input. Every cost line is a disclosed ratio of its own segment's
revenue and the margin falls out [L-005].
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import inputs as IN
import model as M

TAX = M.TAX


def _v(d, k):
    return d[k]["value"]


def _load_schedules():
    """The committed schedules, read back rather than recomputed, so the workbook,
    the document and the gate all stand on one object."""
    import cost_of_capital as COC
    w = json.load(open(os.path.join(HERE, "wacc.json")))
    return {b: COC.Schedule.from_record(w["schedule"][b]) for b in ("rating", "cds")}


SCHEDULES = _load_schedules()


def discounted(mode, sched):
    """Discount on the SCHEDULE, not on a flat rate.

    [R-COC-01]. Every explicit year carries its own forward rate, and everything
    beyond the window — the residual order book converting over a further ten or
    fourteen years, the recurring legs' perpetuity — compounds on the last
    explicit factor at the terminal rate. This matters more on this company than
    on almost any other in the book: its conversion runs to year nineteen, where
    a flat crisis-level rate values a pound at a QUARTER of what the schedule
    values it at, and the whole of that difference was an assumption that Egypt
    never normalises.
    """
    import cost_of_capital as COC
    dc = COC.Discounter(sched)
    wacc = sched.wacc_exp
    p = M.project(mode)
    rows = p["rows"]
    pv = 0.0
    for i, r in enumerate(rows):
        r = dict(r)
        r["discount_factor"] = dc.factor(i + 1)
        r["forward_wacc"] = sched.forward_wacc[i]
        r["pv"] = r["fcff"] * r["discount_factor"]
        pv += r["pv"]
        rows[i] = r
    # TERMINAL. Two pieces, and neither is a perpetuity on the development leg:
    # the order book is finite, and capitalising a finite pipeline for ever is a
    # free number.
    #   (a) the residual order book converts over a further n years at the same
    #       margin, discounted as a level annuity from the window's end;
    #   (b) the recurring legs get a growing perpetuity on their OWN last
    #       explicit-year cash flow, because a hotel and a shopping centre do
    #       carry on.
    last = rows[-1]
    n = p["conversion_years"]
    gm = p["ratios"]["gm_dev_h1_26"]
    # The residual is built the same way the explicit years are, on the CLOSING
    # balance sheet: what is still owed on the book, less what is still to be
    # built after crediting the work in progress already paid for, less overhead
    # and tax. Valuing the residual on margin alone ignored EGP 400bn+ of
    # properties under development that the faster reading had just spent the
    # window building, and turned that reading's whole enterprise value
    # negative — the model was charging for the construction twice and crediting
    # the inventory once.
    resid_rev = p["closing_backlog"] / n
    resid_collections = max(p["closing_backlog"] - last["customer_advances"], 0.0) / n
    resid_build = max(p["closing_backlog"] * (1 - gm)
                      - last["properties_under_development"], 0.0) / n
    resid_opex = resid_rev * p["ratios"]["opex_ratio_fy25"]
    resid_tax = max(resid_rev * gm - resid_opex, 0.0) * TAX
    resid_cf = resid_collections - resid_build - resid_opex - resid_tax
    ann = dc.annuity(len(rows) + 1, n)
    # Work in progress beyond what the residual book needs is a real asset the
    # company has already paid for. It is credited AT COST, not at margin — the
    # conservative reading, and the only one the disclosure supports.
    excess_pud = max(last["properties_under_development"]
                     - p["closing_backlog"] * (1 - gm), 0.0)
    pv_excess = excess_pud * dc.factor(len(rows))
    pv_book = resid_cf * ann + pv_excess

    rec_rev = last["hosp_revenue"] + last["other_revenue"]
    rec_gp = (last["hosp_revenue"] - last["hosp_cost"]
              + last["other_revenue"] - last["other_cost"])
    rec_ebit = rec_gp - rec_rev * p["ratios"]["opex_ratio_fy25"]
    rec_capex = (last["hosp_revenue"] * M.HOSP_CAPEX_RATIO
                 + last["other_revenue"] * M.OTHER_CAPEX_RATIO)
    rec_fcff = rec_ebit * (1 - TAX) - rec_capex
    # the recurring perpetuity is capitalised at the TERMINAL rate — the rate that
    # applies when it is struck — and brought home on the window's own factor. The
    # earlier editions capitalised it at the explicit-window rate and floored the
    # denominator at 2%, which is a free parameter hiding an impossible assumption.
    pv_rec = rec_fcff * dc.perpetuity_factor(M.TERMINAL_GROWTH)
    tv_rec = pv_rec / dc.factor(len(rows))

    return {"mode": mode, "wacc": wacc, "conversion_years": n,
            "rows": rows, "pv_explicit": pv,
            "residual_book": p["closing_backlog"], "residual_annual_cash": resid_cf,
            "residual_collections": resid_collections, "residual_build": resid_build,
            "residual_opex": resid_opex, "residual_tax": resid_tax,
            "excess_work_in_progress": excess_pud, "pv_excess_wip": pv_excess,
            "closing_advances": last["customer_advances"],
            "closing_properties_under_development": last["properties_under_development"],
            "pv_residual_book": pv_book,
            "terminal_recurring_fcff": rec_fcff, "terminal_value_recurring": tv_rec,
            "pv_terminal_recurring": pv_rec,
            "enterprise_value": pv + pv_book + pv_rec,
            "ratios": p["ratios"], "model": p}


def bridge(d):
    """EV to equity, and the minority computed BOTH ways."""
    cash = (_v(IN.BS, "cash") + _v(IN.BS, "deposits_current")
            + _v(IN.BS, "deposits_noncurrent"))
    debt = (_v(IN.BS, "loans_noncurrent") + _v(IN.BS, "loans_current")
            + _v(IN.BS, "credit_facilities"))
    leases = _v(IN.BS, "lease_noncurrent") + _v(IN.BS, "lease_current")
    ip = _v(IN.BS, "investment_property")
    assoc = _v(IN.BS, "associates")
    fvoci = _v(IN.BS, "fvoci")
    nci_book = _v(IN.BS, "nci_equity")
    nci_share = nci_book / _v(IN.BS, "total_equity")
    # [CLASS-A CORRECTION, 02-Sep-2026 — Standing_Research_Protocol.md lines 383-387, 13-Jul
    # r3: "NCI — deduct at FAIR VALUE, never at book"; applied from GAP_REVIEW_01-09-2026
    # heading 6.] The minority's subsidiaries are not disclosed individually, so its share of
    # VALUE is proxied by its FILED share of group profit (FY2025: 3,818.1 / 18,202.0 = 20.98%),
    # against a 45.21% share of BOOK equity that the two earlier framings both used. Book and
    # proportional stay printed beside it as the more punitive reads; the adopted basis is
    # the value-share proxy. The subsidiary-level fair value the rule asks for is the gap
    # this closes when the disclosure arrives.
    nci_profit_share = _v(IN.IS, "nci_profit_fy25") / _v(IN.IS, "net_profit_fy25")
    gross = d["enterprise_value"] + cash - debt - leases + ip + assoc + fvoci
    sh = _v(IN.KPI, "shares_outstanding")
    return {
        "nci_profit_share": nci_profit_share,
        "equity_after_nci_value_share": gross * (1 - nci_profit_share),
        "per_share_nci_value_share": gross * (1 - nci_profit_share) / sh,
        "nci_basis_adopted": "value share (filed profit share proxy)",
        "enterprise_value": d["enterprise_value"],
        "cash_and_deposits": cash, "borrowings": debt, "lease_liabilities": leases,
        "net_cash": cash - debt - leases,
        "investment_property": ip, "associates": assoc, "fvoci": fvoci,
        "equity_before_minority": gross,
        "nci_book": nci_book, "nci_share_of_equity": nci_share,
        "equity_after_nci_book": gross - nci_book,
        "equity_after_nci_proportional": gross * (1 - nci_share),
        "per_share_nci_book": (gross - nci_book) / sh,
        "per_share_nci_proportional": gross * (1 - nci_share) / sh,
        "shares_mn": sh,
    }


def sotp(mode, sched):
    d = discounted(mode, sched)
    b = bridge(d)
    d.update(b)
    return d


def main():
    w = json.load(open(os.path.join(HERE, "wacc.json")))
    out = {"parameters": {k: getattr(M, k) for k in
                          ("CAPACITY_YEARS", "RECOVERY_YEARS", "CAPACITY_RAMP",
                           "RECOVERY_RAMP", "REPLENISHMENT_SALES", "SALES_FADE",
                           "HOSP_GROWTH", "OTHER_GROWTH", "PUD_COVER_YEARS",
                           "PUD_ADJUST_YEARS", "TERMINAL_GROWTH", "PAYOUT", "TAX")},
           "ratios": M.ratios()}
    for basis, sched in (("rating", SCHEDULES["rating"]), ("cds", SCHEDULES["cds"])):
        wacc = sched.wacc_exp
        for mode in ("capacity", "recovery"):
            out["%s|%s" % (basis, mode)] = sotp(mode, sched)
    json.dump(out, open(os.path.join(HERE, "valuation.json"), "w"), indent=1)

    print("%-9s %-10s %8s %11s %11s %11s %9s %9s"
          % ("ERP", "crux", "WACC", "PV explicit", "PV residual", "EV",
             "per share", "vs 97.80"))
    for k, s in out.items():
        if "|" not in k:
            continue
        basis, mode = k.split("|")
        ps = s["per_share_nci_book"]
        print("%-9s %-10s %7.2f%% %11.0f %11.0f %11.0f %9.2f %8.0f%%"
              % (basis, mode, 100 * s["wacc"], s["pv_explicit"],
                 s["pv_residual_book"] + s["pv_terminal_recurring"],
                 s["enterprise_value"], ps, 100 * (ps / 97.80 - 1)))
    print("\nminority framed both ways (rating basis):")
    for mode in ("capacity", "recovery"):
        s = out["rating|%s" % mode]
        print("  %-9s  at book %7.2f   proportional %7.2f   (NCI is %.1f%% of equity)"
              % (mode, s["per_share_nci_book"], s["per_share_nci_proportional"],
                 100 * s["nci_share_of_equity"]))


if __name__ == "__main__":
    main()
