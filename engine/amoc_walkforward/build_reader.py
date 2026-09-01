"""Emit the per-origin projected-versus-actual income statements ([R-FCAL-01] §4)."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B, diagnose as D, panel as P

LINES = [("net_sales", "Net sales"), ("cost_of_sales", "Cost of sales"),
         ("gross_profit", "Gross profit"), ("ga", "General and administrative"),
         ("marketing", "Marketing and selling"), ("other_expenses", "Other operating expenses"),
         ("operating_profit", "Operating profit"), ("claims_provision", "Claims and disputes provision"),
         ("other_revenues", "Other revenues"), ("investment_revenues", "Investment revenues"),
         ("pbt", "Profit before tax"), ("income_tax", "Income tax"),
         ("npat", "Profit after tax"), ("nci", "Non-controlling interest"),
         ("majority", "Majority's share")]


def m(x):
    return "—" if x is None else "{:,.0f}".format(x / 1e6)


def pct(p, a):
    if p is None or a is None or a == 0:
        return "n/a"
    return "%+.0f%%" % ((p / a - 1) * 100)


def main():
    out = ["# AMOC — projected versus actual, every origin and horizon",
           "",
           "Internal. EGP millions. **Projections are the pre-registered rules of "
           "`PRE_REGISTRATION_01-09-2026.md` §2**, run at the origin with only what was published "
           "by that date. Actuals are as first reported (FY2024 therefore shows 1,699.2 majority, "
           "its own filing's figure, not the 1,439.6 the FY2025 filing later restated it to — B-6).",
           "",
           "The `PPP` column is the post-hoc diagnostic of `diagnose.py`, shown so the "
           "specification defect is visible line by line rather than only in the summary. It is "
           "NOT evidence and nothing is adopted from it.",
           ""]
    for o, h, t in B.cells():
        a = B.actual(t)
        p = B.project(o, h)
        q = D.ppp_project(o, h)
        out.append("## Origin %s, horizon %d — scored against %s actual\n" % (o, h, t))
        out.append("| line | projected | actual | error | PPP diagnostic | PPP error |")
        out.append("|---|---:|---:|---:|---:|---:|")
        for k, label in LINES:
            pv, av, qv = p.get(k), a.get(k), q.get(k)
            out.append("| %s | %s | %s | %s | %s | %s |"
                       % (label, m(pv), m(av), pct(pv, av),
                          m(qv) if qv is not None else "—",
                          pct(qv, av) if qv is not None else "—"))
        out.append("")
        out.append("Throughput: projected {:,.0f} t against {:,.0f} t actual ({}).\n".format(
            p["volume_t"], a["volume_t"], pct(p["volume_t"], a["volume_t"])))
    path = os.path.join(HERE, "amoc_IS_projected_vs_actual_all_origins.md")
    open(path, "w").write("\n".join(out))
    print("wrote %s (%d lines)" % (os.path.basename(path), len(out)))


if __name__ == "__main__":
    main()
