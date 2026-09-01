"""Every origin's projected-versus-actual income statement, side by side (§4)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B

LINES = ["revenue", "cost_of_sales", "gross_profit", "selling", "admin", "provisions", "other_bucket",
         "reval_gain", "fx", "investment_income", "credit_interest", "debit_interest", "pbt", "tax_current", "net"]


def f(x):
    return "n/a" if x is None else "{:,.0f}".format(x)


def e(p, a):
    if p is None or a is None:
        return ""
    if p > 0 and a > 0:
        return "%+.0f%%" % (100 * (math.exp(math.log(p / a)) - 1))
    return "sign %s" % ("ok" if (p > 0) == (a > 0) else "WRONG")


out = ["# EGCH (KIMA) — projected versus actual income statement, every origin, every horizon",
       "", "EGP thousand. Projection under the pre-registered rules on the knowable path; actual as first "
       "reported. Percentage = projected/actual − 1 where both are positive; otherwise the sign check. "
       "Internal — never shown to a reader.", ""]
for o in B.ORIGINS:
    out.append("## Origin %s (%s, tax rate %.1f%%)" % (o, P.IS[o]["src"], 100 * P.TAX_REGIME[o]))
    out.append("")
    hs = [(h, B.fyname(B.y(o) + h)) for h in B.HORIZONS if B.fyname(B.y(o) + h) in P.IS and B.y(o) + h <= 2025]
    out.append("| line | " + " | ".join("h=%d %s proj | actual | err" % (h, t) for h, t in hs) + " |")
    out.append("|---|" + "---|---|---|" * len(hs))
    projs = {h: B.project(o, h) for h, _ in hs}
    for ln in LINES:
        cells = []
        for h, t in hs:
            p, a = projs[h].get(ln), P.actual(t).get(ln)
            cells.append("%s | %s | %s" % (f(p), f(a), e(p, a)))
        out.append("| %s | %s |" % (ln, " | ".join(cells)))
    out.append("")
open(os.path.join(HERE, "egch_IS_projected_vs_actual_all_origins.md"), "w").write("\n".join(out))
print("wrote egch_IS_projected_vs_actual_all_origins.md (%d origins)" % len(B.ORIGINS))
