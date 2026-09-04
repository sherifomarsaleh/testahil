"""TMGH — the other three lenses, and the sensitivity.

1.2 book value and sustainable return · 1.3 relative multiples ·
1.4 normalised earnings power · 1.9 sensitivity.

The relative lens is built on TMGH's OWN history of multiples, computed from
the committed panel and the committed price series, rather than on a peer table
of numbers this study has not sourced. A named peer set is carried beside it as
context, at the tier its sourcing earns.
"""
import csv, datetime, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ENGINE)
import inputs as IN
import wacc as WC
import valuation as VAL
import model as M

PANEL = os.path.join(ENGINE, "tmgh_walkforward", "panel_annual.json")
OHLC = os.path.join(ENGINE, "raw_ohlc", "EG", "TMGH.csv")


def _v(d, k):
    return d[k]["value"]


def year_end_prices():
    rows = list(csv.DictReader(open(OHLC, encoding="utf-8-sig")))
    out = {}
    for r in rows:
        d = datetime.datetime.strptime(r["Date"].strip('"'), "%m/%d/%Y").date()
        px = float(r["Price"].strip('"').replace(",", ""))
        cur = out.get(d.year)
        if cur is None or d > cur[0]:
            out[d.year] = (d, px)
    return {y: {"date": str(v[0]), "close": v[1]} for y, v in out.items()}


def own_history():
    """TMGH's own P/E and P/B, year by year, from committed data only."""
    P = json.load(open(PANEL))
    px = year_end_prices()
    sh = _v(IN.KPI, "shares_outstanding")
    rows = []
    for y in sorted(int(k) for k in P if not k.startswith("_")):
        c = P[str(y)]["cells"]
        if y not in px:
            continue
        eps = c.get("npat_parent", 0.0) / sh if c.get("npat_parent") else None
        # PARENT equity only. Falling back to group equity mixes two different
        # measures in one column: TMG's minority interest is 45% of the sheet
        # after the 2024 hotel acquisition, so a group-equity year and a
        # parent-equity year are not comparable and the P/B series would show a
        # break that is presentational, not economic.
        eqp = c.get("equity_parent")
        bvps = (eqp / sh) if eqp else None
        rows.append({"year": y, "close": px[y]["close"], "date": px[y]["date"],
                     "eps": eps, "bvps": bvps,
                     "book_basis": "parent equity" if eqp else "not disclosed in panel",
                     "group_bvps": (c.get("total_equity") / sh)
                     if c.get("total_equity") else None,
                     "pe": (px[y]["close"] / eps) if eps and eps > 0 else None,
                     "pb": (px[y]["close"] / bvps) if bvps and bvps > 0 else None})
    return rows


def book_and_return(wacc_json):
    """1.2 — book value and the return the company earns on it."""
    eq = _v(IN.BS, "equity_parent")
    sh = _v(IN.KPI, "shares_outstanding")
    bvps = eq / sh
    npat = _v(IN.IS, "npat_parent_fy25")
    eq_open = _v(IN.BS, "equity_parent_fy25")
    roe = npat / ((eq + eq_open) / 2)
    ke = wacc_json["ke_rating"]
    ke_cds = wacc_json["ke_cds"]
    # A company earning ROE on book, growing at g, is worth book x (ROE-g)/(Ke-g)
    out = {}
    for name, k in (("rating", ke), ("cds", ke_cds)):
        for g in (0.10, 0.15):
            just = (roe - g) / (k - g) if k > g else None
            out["%s|g=%.0f%%" % (name, 100 * g)] = {
                "justified_pb": just,
                "value_per_share": (just * bvps) if just else None}
    return {"book_value_per_share": bvps, "equity_parent": eq, "roe_fy25": roe,
            "ke_rating": ke, "ke_cds": ke_cds, "cases": out,
            "note": ("ROE below the cost of equity means each retained pound is worth "
                     "less than a pound, and the justified multiple falls below one. "
                     "That is what this arithmetic says here, and it is stated rather "
                     "than softened.")}


# Named peers. Market prices are read from this repository's own committed OHLC
# libraries; nothing about a peer's financials is used as a source for TMGH's own
# numbers, per SIGCM clause 5.
PEERS = [
    {"ticker": "EMFD", "name": "Emaar Misr for Development", "market": "EG"},
    {"ticker": "OCDI", "name": "Sixth of October Development & Investment (SODIC)",
     "market": "EG"},
    {"ticker": "PHDC", "name": "Palm Hills Developments", "market": "EG"},
    {"ticker": "HELI", "name": "Heliopolis Housing & Development", "market": "EG"},
    {"ticker": "ORHD", "name": "Orascom Development Egypt", "market": "EG"},
]


def peer_prices():
    out = []
    for p in PEERS:
        f = os.path.join(ENGINE, "raw_ohlc", p["market"], p["ticker"] + ".csv")
        if not os.path.exists(f):
            out.append(dict(p, close=None,
                            note="no committed price library held for this name"))
            continue
        rows = list(csv.DictReader(open(f, encoding="utf-8-sig")))
        best = None
        for r in rows:
            d = datetime.datetime.strptime(r["Date"].strip('"'), "%m/%d/%Y").date()
            if best is None or d > best[0]:
                best = (d, float(r["Price"].strip('"').replace(",", "")))
        out.append(dict(p, close=best[1], as_of=str(best[0]),
                        source="engine/raw_ohlc/%s/%s.csv" % (p["market"], p["ticker"])))
    return out


def normalised_earnings(wacc_json):
    """1.4 — what the business earns through a cycle, capitalised.

    Normalised on the company's OWN three most recent years, with the
    fair-value revaluation gains stripped: they are non-cash, they are not
    forecast, and capitalising them would capitalise a valuation opinion.
    """
    yrs = {
        2023: {"npat": _v(IN.IS, "npat_parent_fy23"), "reval": 0.0},
        2024: {"npat": _v(IN.IS, "npat_parent_fy24"), "reval": 4924.1},
        2025: {"npat": _v(IN.IS, "npat_parent_fy25"),
               "reval": _v(IN.IS, "ip_revaluation_fy25")},
    }
    sh = _v(IN.KPI, "shares_outstanding")
    nci_share = _v(IN.BS, "nci_equity") / _v(IN.BS, "total_equity")
    clean = {}
    for y, d in yrs.items():
        # the revaluation is a group-level gain; only the parent's share of it
        # is in attributable profit, approximated at the parent's equity share
        clean[y] = d["npat"] - d["reval"] * (1 - nci_share)
    avg = sum(clean.values()) / len(clean)
    out = {"years": yrs, "cleaned_attributable_profit": clean,
           "average": avg, "average_eps": avg / sh,
           "revaluation_note": ("FY2024 and FY2025 attributable profit each carry a "
                                "non-cash investment-property revaluation gain (EGP "
                                "4,924.1mn and EGP 3,952.5mn at group level). They are "
                                "stripped: capitalising a revaluation gain capitalises "
                                "a valuation opinion.")}
    for name, ke in (("rating", wacc_json["ke_rating"]), ("cds", wacc_json["ke_cds"])):
        for g in (0.10, 0.15):
            out["cap|%s|g=%.0f%%" % (name, 100 * g)] = (avg / sh) * (1 + g) / (ke - g)
    return out


def sensitivity():
    """1.9 — the crux sensitised in real observable units.

    The discount rate is the study's single most consequential input, and the
    grid runs from the 18% the previous edition used to 40%. 18% is BELOW
    Egypt's own 10-year sovereign yield of 23.00%, so it cannot be a nominal
    EGP discount rate for a levered equity — it prices TMG as safer than the
    government that taxes it. It is on the grid so a reader can see exactly what
    the change of method is worth, not because it is defensible.
    """
    # EVERY PER-SHARE HERE IS THE ADOPTED BASIS [corrected 03-Sep-2026]. The three
    # sensitivity constructions, the football field and the bridge all published
    # per_share_nci_book while this study DEDUCTS THE MINORITY AT ITS SHARE OF VALUE,
    # which is what its summary table, its headline range and [R-BRIDGE-01] all say.
    # Nothing stated a reason; it was simply the key that got written first and copied.
    sh = _v(IN.KPI, "shares_outstanding")
    grid = {}
    # The rate sensitivity shifts the WHOLE SCHEDULE, keeping its shape. Replacing
    # the schedule with a flat rate would ask two questions at once — what if
    # capital costs more, AND what if the economy never normalises — and the
    # second is the assumption the schedule exists to remove [R-COC-01].
    base_sched = VAL.SCHEDULES["cds"]
    for delta in (-0.08, -0.04, -0.02, 0.0, 0.02, 0.04, 0.08):
        sched = base_sched if delta == 0.0 else base_sched.shifted(delta)
        wacc = sched.wacc_exp
        for mode in ("capacity", "recovery"):
            s = VAL.sotp(mode, sched)
            grid["%0.4f|%s" % (wacc, mode)] = {
                "wacc": wacc, "shift": delta, "mode": mode,
                "per_share_nci_value_share": s["per_share_nci_value_share"],
                "per_share_nci_book": s["per_share_nci_book"],
                "per_share_nci_proportional": s["per_share_nci_proportional"],
                "enterprise_value": s["enterprise_value"]}
    # the second sensitivity: the conversion period itself, in years
    conv = {}
    base = M.CAPACITY_YEARS
    for n in (8, 10, 12, 14, 16, 20):
        M.CAPACITY_YEARS = n
        s = VAL.sotp("capacity", VAL.SCHEDULES["rating"])
        conv[str(n)] = s["per_share_nci_value_share"]
    M.CAPACITY_YEARS = base
    return {"wacc_grid": grid, "conversion_years_grid": conv}


def implied_discount_rate(spot):
    """The reverse question: what discount rate does the market appear to use?

    This study discounts on a SCHEDULE, not a single rate, so the honest form of
    the question is: what one flat rate, held for every year, would reproduce the
    traded price? That is a fair thing to show a reader used to seeing one number,
    and it is explicitly a degenerate construction rather than a valuation — the
    schedule it is compared against is the thing this study actually uses.
    """
    import cost_of_capital as COC
    sh = _v(IN.KPI, "shares_outstanding")
    out = {}
    for mode in ("capacity", "recovery"):
        lo, hi = 0.05, 0.90
        for _ in range(80):
            mid = (lo + hi) / 2
            flat = COC.flat_schedule(mid, VAL.SCHEDULES["cds"].years,
                                     why="the reverse question in section 1.7")
            ps = VAL.sotp(mode, flat)["per_share_nci_value_share"]
            if ps > spot:
                lo = mid
            else:
                hi = mid
        out[mode] = (lo + hi) / 2
    return out


def main():
    w = json.load(open(os.path.join(HERE, "wacc.json")))
    out = {"own_multiple_history": own_history(),
           "book_and_sustainable_return": book_and_return(w),
           "peers": peer_prices(),
           "normalised_earnings": normalised_earnings(w),
           "sensitivity": sensitivity(),
           "implied_discount_rate": implied_discount_rate(WC.SPOT),
           "spot": WC.SPOT, "spot_source": WC.SPOT_SOURCE}
    json.dump(out, open(os.path.join(HERE, "lenses.json"), "w"), indent=1)

    print("=== TMGH's own multiples, year end ===")
    print("%6s %8s %8s %8s %7s %7s" % ("year", "close", "EPS", "BVPS", "P/E", "P/B"))
    for r in out["own_multiple_history"][-9:]:
        print("%6d %8.2f %8s %8s %7s %7s"
              % (r["year"], r["close"],
                 "%.2f" % r["eps"] if r["eps"] else "-",
                 "%.2f" % r["bvps"] if r["bvps"] else "-",
                 "%.1f" % r["pe"] if r["pe"] else "-",
                 "%.2f" % r["pb"] if r["pb"] else "-"))
    b = out["book_and_sustainable_return"]
    print("\n=== book value and sustainable return ===")
    print("BVPS %.2f, ROE(FY2025) %.1f%%, Ke %.1f%% (rating) / %.1f%% (CDS)"
          % (b["book_value_per_share"], 100 * b["roe_fy25"],
             100 * b["ke_rating"], 100 * b["ke_cds"]))
    for k, v in b["cases"].items():
        print("   %-16s justified P/B %6s  ->  %8s"
              % (k, "%.2f" % v["justified_pb"] if v["justified_pb"] else "n/m",
                 "%.2f" % v["value_per_share"] if v["value_per_share"] else "n/m"))
    n = out["normalised_earnings"]
    print("\n=== normalised earnings power ===")
    print("cleaned attributable profit: %s ; average %.0f (EPS %.2f)"
          % ({y: round(x) for y, x in n["cleaned_attributable_profit"].items()},
             n["average"], n["average_eps"]))
    for k, v in n.items():
        if k.startswith("cap|"):
            print("   %-22s %8.2f" % (k, v))
    print("\n=== sensitivity: the whole schedule shifted, keeping its shape ===")
    print("%8s %10s %12s %12s" % ("shift", "year 1", "capacity", "recovery"))
    keys = sorted(out["sensitivity"]["wacc_grid"], key=lambda k: float(k.split("|")[0]))
    for k in [x for x in keys if x.endswith("|capacity")]:
        c = out["sensitivity"]["wacc_grid"][k]
        r = out["sensitivity"]["wacc_grid"][k.replace("|capacity", "|recovery")]
        print("%+7.0fbp %9.2f%% %12.2f %12.2f"
              % (10000 * c["shift"], 100 * c["wacc"],
                 c["per_share_nci_value_share"],
                 r["per_share_nci_value_share"]))
    print("\n=== sensitivity: value per share against the conversion period ===")
    for k, v in out["sensitivity"]["conversion_years_grid"].items():
        print("   %2s years  %8.2f" % (k, v))
    idr = out["implied_discount_rate"]
    print("\n=== the discount rate the market appears to use, at spot %.2f ===" % WC.SPOT)
    for mode, r in idr.items():
        print("   %-9s %6.2f%%   (house method: %.2f%% rating / %.2f%% CDS)"
              % (mode, 100 * r, 100 * w["wacc_rating"], 100 * w["wacc_cds"]))

    print("\n=== peers (prices from this repository's own committed libraries) ===")
    for p in out["peers"]:
        print("   %-6s %-46s %8s  %s"
              % (p["ticker"], p["name"][:44],
                 "%.2f" % p["close"] if p.get("close") else "-",
                 p.get("as_of", p.get("note", ""))))


if __name__ == "__main__":
    main()
