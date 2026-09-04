"""TMGH — Appendix A: the financial statements, reported and projected.

A.1 income statement: three reported years beside five forecast years.
A.2 balance sheet as reported.
A.3 the FULL projected balance sheet and cash-flow statement.

Every projected figure comes out of `model.project`, the study's single model
[L-016]. Years three to five carry RANGES from the walk-forward's own measured
driver-error distribution, never points [L-011].
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import inputs as IN
import model as M

RANGES = os.path.join(ENGINE, "tmgh_walkforward", "forward_ranges.json")
FWD = 5


def _v(d, k):
    return d[k]["value"]


def reported():
    """Three reported years, as first reported. The FY2024 restatement is
    carried beside its original, never substituted for it."""
    return {
        "2023": {"dev_revenue": _v(IN.IS, "dev_revenue_fy23"),
                 "hosp_revenue": _v(IN.IS, "hosp_revenue_fy23"),
                 "other_revenue": _v(IN.IS, "other_revenue_fy23"),
                 "gross_profit": _v(IN.IS, "gross_profit_fy23"),
                 "net_profit": _v(IN.IS, "net_profit_fy23"),
                 "attributable_profit": _v(IN.IS, "npat_parent_fy23")},
        "2024": {"dev_revenue": _v(IN.IS, "dev_revenue_fy24"),
                 "hosp_revenue": _v(IN.IS, "hosp_revenue_fy24"),
                 "other_revenue": _v(IN.IS, "other_revenue_fy24"),
                 "gross_profit": _v(IN.IS, "gross_profit_fy24"),
                 "net_profit": _v(IN.IS, "net_profit_fy24"),
                 "attributable_profit": _v(IN.IS, "npat_parent_fy24"),
                 "restated": {"gross_profit": _v(IN.IS, "gross_profit_fy24_restated"),
                              "net_profit": _v(IN.IS, "net_profit_fy24_restated"),
                              "attributable_profit":
                                  _v(IN.IS, "npat_parent_fy24_restated"),
                              "why": ("purchase-price allocation completed inside the "
                                      "measurement period after the seven-hotel "
                                      "acquisition, per the FY2025 statements")}},
        "2025": {"dev_revenue": _v(IN.IS, "dev_revenue_fy25"),
                 "hosp_revenue": _v(IN.IS, "hosp_revenue_fy25"),
                 "other_revenue": _v(IN.IS, "other_revenue_fy25"),
                 "gross_profit": _v(IN.IS, "gross_profit_fy25"),
                 "net_profit": _v(IN.IS, "net_profit_fy25"),
                 "attributable_profit": _v(IN.IS, "npat_parent_fy25")},
    }


def with_ranges(rows):
    if not os.path.exists(RANGES):
        return rows
    fr = json.load(open(RANGES))["projection"]
    for i, r in enumerate(rows):
        h = i + 1
        if h < 3:
            continue
        band = fr.get(str(2025 + h), {})
        for field, src in (("revenue", "total_revenue"),
                           ("gross_profit", "gross_profit"),
                           ("net_profit", "net_profit")):
            b = band.get(src)
            if not b or "low" not in b or not b.get("central"):
                continue
            # the band is the METHOD's own measured relative error applied to
            # THIS study's central path; the walk-forward's own absolute path is
            # a statement about a mechanical rule, not about the company
            r[field + "_low"] = r[field] * (b["low"] / b["central"])
            r[field + "_high"] = r[field] * (b["high"] / b["central"])
            r[field + "_band_n"] = b.get("n_observations")
    return rows


def build():
    out = {"reported": reported()}
    for mode in ("capacity", "recovery"):
        p = M.project(mode)
        out[mode] = {"conversion_years": p["conversion_years"],
                     "rows": with_ranges([dict(r) for r in p["rows"][:FWD]]),
                     "full_rows": p["rows"]}
    return out


def main():
    """Print the statements. IT NO LONGER WRITES A FILE, AND THAT IS THE FIX.

    It used to dump statements.json beside the study. Nothing read it — build_numbers.py
    imports this module and calls build(), so the live path never touches the file — and
    it sat two days stale while the model moved, carrying a 2030 development revenue of
    76,350 against the 102,747 the delivered document prints, a 35% divergence.

    IT WAS NOT HARMLESS. Sizing a table needed the widest cell in that row, and the first
    attempt read this file, got 76,350, concluded the column was wide enough, and was
    wrong — the page had been printing "102,74" with a lone "7" beneath it for two days.

    [R-ENF-06] says an artefact a builder reads must declare the answer it was built
    against, and its general lesson is to ask what WRITES a file when a builder reads it.
    THE MIRROR CASE IS THIS ONE: a file that something WRITES and nothing reads is a
    number frozen at the moment somebody last ran the script, with no consumer to notice
    and no vintage to check. The cheapest fix for a file with no consumer is not to
    declare its vintage; it is not to write it.
    """
    out = build()
    print("A.1 income statement — reported and projected (capacity reading)\n")
    rep = out["reported"]
    print("%-24s %10s %10s %10s | %s"
          % ("EGP mn", "FY2023", "FY2024", "FY2025",
             " ".join("%10s" % ("FY%d" % r["year"]) for r in out["capacity"]["rows"])))
    for label, key in (("Development revenue", "dev_revenue"),
                       ("Hospitality revenue", "hosp_revenue"),
                       ("Other recurring revenue", "other_revenue"),
                       ("Gross profit", "gross_profit"),
                       ("Net profit", "net_profit"),
                       ("Attributable profit", "attributable_profit")):
        hist = " ".join("%10.0f" % rep[y][key] for y in ("2023", "2024", "2025"))
        fwd = " ".join("%10.0f" % r.get(key, r.get("revenue", 0)) if key in r else "%10s" % "-"
                       for r in out["capacity"]["rows"])
        print("%-24s %s | %s" % (label, hist, fwd))
    print("\nranges carried on years 3-5 (capacity reading):")
    for r in out["capacity"]["rows"]:
        if "revenue_low" in r:
            print("   FY%d revenue %.0f  band %.0f - %.0f  (n=%s)"
                  % (r["year"], r["revenue"], r["revenue_low"], r["revenue_high"],
                     r.get("revenue_band_n")))
    print("\nbalance check, every projected year: max |A - L - E| = %.4f"
          % max(abs(r["balance_check"]) for m in ("capacity", "recovery")
                for r in out[m]["full_rows"]))


if __name__ == "__main__":
    main()
