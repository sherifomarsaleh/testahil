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




def _house_wacc():
    try:
        return json.load(open(os.path.join(HERE, "wacc.json")))["wacc_rating"]
    except Exception:
        return None


BETA = 1.4718
TAX_ = 0.225

def discounted(mode, wacc):
    p = M.project(mode)
    rows = p["rows"]
    # THE DISCOUNT RATE SLIDES WITH THE INFLATION IT IS QUOTED IN, so the
    # discount factor is a CUMULATIVE PRODUCT of each year's own rate, not a
    # single rate raised to a power. Compounding today's 35.79% for twenty years
    # would discount a converged Egypt at crisis rates, which is the same
    # inconsistency in the other direction.
    import wacc as W
    w_now = wacc
    _w = json.load(open(os.path.join(HERE, "wacc.json")))
    w_term, _ke = W.terminal_wacc(BETA, _w["weight_equity"], _w["weight_debt"], TAX)
    # THE TERMINAL RATE IS A PROPERTY OF THE CONVERGED ECONOMY, NOT OF WHERE
    # THE PATH STARTS. Scaling it by the starting rate made a sensitivity at 22%
    # converge to 10.8%, which is barely above the 6.08% terminal growth and
    # would have printed a number the perpetuity cannot support. Whatever rate
    # Egypt is at today, a normalised Egypt is the same normalised Egypt: the
    # terminal inputs are stated once (rf 8%, ERP 7%, Kd 10.5%) and every path
    # lands there. The glide never rises, so a starting rate already below the
    # terminal one simply stays flat.
    path = W.wacc_path(w_now, min(w_term, w_now), len(rows))
    pv, df = 0.0, 1.0
    for i, r in enumerate(rows):
        r = dict(r)
        df /= (1 + path[i])
        r["wacc_this_year"] = path[i]
        r["discount_factor"] = df
        r["pv"] = r["fcff"] * df
        pv += r["pv"]
        rows[i] = r
    df_end = df
    wacc_terminal = path[-1]
    # TERMINAL — A GOING CONCERN, NOT A PIPELINE RUNNING OUT.
    #
    # The first cut valued the terminal as a level annuity on the RESIDUAL ORDER
    # BOOK, reasoning that "the order book is finite, and capitalising a finite
    # pipeline for ever is a free number." That is true of the book and FALSE of
    # the business. TMG holds a landbank measured in decades, it has replenished
    # its book every year of its history, and it sells about ten times what it
    # delivers -- demand is not what limits it. Treating it as a pipeline
    # emptying out valued EGP 1.6 TRILLION of contracted, already-sold backlog
    # at about EGP 9bn, because at a 35.79% discount rate an annuity that starts
    # in year eleven is worth almost nothing. The user's objection was exactly
    # this: the contracted units WILL be built, delivered, booked as revenue and
    # collected, and that is where most of the value is.
    #
    # So the terminal is a growing perpetuity on the whole business's free cash
    # flow, at a long-run nominal rate NO HIGHER than the economy's -- the
    # company grows with prices and nothing more, which is the conservative
    # reading for a developer with this much land. The residual-book annuity and
    # the separate recurring perpetuity are both GONE: they double-counted with
    # each other at the edges and neither described a company that carries on.
    last = rows[-1]
    n = p["conversion_years"]
    g = M.TERMINAL_GROWTH
    spread = wacc_terminal - g
    if spread < 0.02:
        raise ValueError("terminal growth %.3f is too close to a WACC of %.3f "
                         "for a perpetuity to mean anything"
                         % (g, wacc_terminal))
    tv = last["fcff"] * (1 + g) / spread
    pv_terminal = tv * df_end
    pv_book, pv_rec, pv_excess, excess_pud = 0.0, pv_terminal, 0.0, 0.0
    resid_cf = resid_collections = resid_build = resid_opex = resid_tax = 0.0
    rec_fcff, tv_rec = last["fcff"], tv

    return {"mode": mode, "wacc": wacc, "conversion_years": n,
            "rows": rows, "pv_explicit": pv,
            "residual_book": p["closing_backlog"], "residual_annual_cash": resid_cf,
            "residual_collections": resid_collections, "residual_build": resid_build,
            "residual_opex": resid_opex, "residual_tax": resid_tax,
            "excess_work_in_progress": excess_pud, "pv_excess_wip": pv_excess,
            "closing_advances": last["customer_advances"],
            "closing_properties_under_development": last["properties_under_development"],
            "pv_residual_book": pv_book, "pv_terminal": pv_terminal,
            "terminal_multiple_on_fcff": (1 + M.TERMINAL_GROWTH) / spread,
            "wacc_terminal": wacc_terminal, "wacc_start": w_now,
            "terminal_recurring_fcff": rec_fcff, "terminal_value_recurring": tv_rec,
            "pv_terminal_recurring": pv_rec,
            "enterprise_value": pv + pv_terminal,
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
    gross = d["enterprise_value"] + cash - debt - leases + ip + assoc + fvoci
    sh = _v(IN.KPI, "shares_outstanding")
    return {
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


def sotp(mode, wacc):
    d = discounted(mode, wacc)
    b = bridge(d)
    d.update(b)
    return d


def main():
    w = json.load(open(os.path.join(HERE, "wacc.json")))
    out = {"parameters": {k: getattr(M, k) for k in
                          ("CAPACITY_YEARS", "RECOVERY_YEARS", "CAPACITY_RAMP",
                           "RECOVERY_RAMP", "DELIVERY_REAL_CAPACITY", "DELIVERY_REAL_RECOVERY", "TERMINAL_REAL_GROWTH",
                           "COVER_TARGET_CAPACITY", "BACKLOG_CAPTURE", "FADE_START",
                           "HOSP_GROWTH", "OTHER_GROWTH", "PUD_COVER_YEARS",
                           "PUD_ADJUST_YEARS", "TERMINAL_GROWTH", "PAYOUT", "TAX")},
           "ratios": M.ratios()}
    # THE ADOPTED CONSTRUCTION counts country risk ONCE and slides the whole
    # rate path down as Egypt disinflates. The house construction -- beta
    # multiplied through a country-risk-inclusive premium -- is retained beside
    # it as a labelled cross-check under the dual-framing rule, never dropped.
    import wacc as WC
    b = WC.beta_record()["beta"]
    adopted = {
        "rating": WC.wacc_country_risk_once(
            w["rf_star_rating"], b, WC.CRP_RATING,
            w["weight_equity"], w["weight_debt"], w["kd_aftertax"])[0],
        "cds": WC.wacc_country_risk_once(
            w["rf_star_cds"], b, WC.DAMODARAN_EGYPT["sovereign_cds"],
            w["weight_equity"], w["weight_debt"], w["kd_aftertax"])[0],
    }
    out["cost_of_capital"] = {
        "adopted": adopted,
        "house_cross_check": {"rating": w["wacc_rating"], "cds": w["wacc_cds"]},
        "note": ("Country risk enters ONCE. Beta 1.4718 is measured against "
                 "EGX30, an index that already carries Egyptian country risk, "
                 "so multiplying it through a premium that also contains that "
                 "risk levers the country premium to 14.3 points against a "
                 "sovereign compensated 6.37 for its own default risk. A price "
                 "beta measures relative volatility, not relative exposure to a "
                 "sovereign, and this issuer's revenues are essentially all "
                 "Egyptian. Both constructions are published."),
    }
    for basis, wacc in adopted.items():
        for mode in ("capacity", "recovery"):
            out["%s|%s" % (basis, mode)] = sotp(mode, wacc)
    for basis, wacc in (("rating", w["wacc_rating"]), ("cds", w["wacc_cds"])):
        for mode in ("capacity", "recovery"):
            out["crosscheck_%s|%s" % (basis, mode)] = sotp(mode, wacc)
    json.dump(out, open(os.path.join(HERE, "valuation.json"), "w"), indent=1)

    print("%-9s %-10s %8s %11s %11s %11s %9s %9s"
          % ("ERP", "crux", "WACC", "PV explicit", "PV residual", "EV",
             "per share", "vs 97.80"))
    for k, s in out.items():
        if "|" not in k or k.startswith("crosscheck_"):
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
