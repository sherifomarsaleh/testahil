"""TMGH walk-forward — the mechanical build, run at every origin.

Every rule here is the one written down in PRE_REGISTRATION_01-09-2026.md before
any error was computed. Nothing is fitted; where a rule needs a number the number
is a stated function of data available AT THE ORIGIN. There are no judgement
drivers: the exercise tests the method, not the analyst.

Two things are enforced structurally rather than remembered:

  * INTEREST COMES FROM THE BORROWINGS THAT ACTUALLY BEAR IT. `interest_bearing_debt`
    is loans, credit facilities, overdrafts and lease liabilities. Customer
    advances (EGP 117.7bn at FY2025), suppliers and contractors, and obligations
    against notes receivable are funding that pays no coupon, and none of them is
    in the denominator.
  * REVENUE AND COST SIT ON THE SAME RECOGNITION CLOCK. Development cost is a
    ratio of development revenue, both being handover quantities, so the two
    cannot drift apart and manufacture operating leverage on a thin residual.
"""
import json, math, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kpi_verified

FIRST_ORIGIN, LAST_ORIGIN, LAST_ACTUAL = 2015, 2025, 2025
HORIZONS = [1, 2, 3, 4, 5]
EGYPT_TAX = 0.225                     # statutory rate from FY2015; applied to positive PBT
DEBT_FIELDS = ["lt_loans", "current_loans", "bank_facilities", "overdraft",
               "lease_liab_nc", "lease_liab_c", "sukuk", "sukuk_current"]


# ---------------------------------------------------------------- panel access
def load():
    P = json.load(open(os.path.join(HERE, "panel_annual.json")))
    K = kpi_verified.build()
    A = {}                                            # actuals, by year
    for y, blk in P.items():
        if y.startswith("_"):
            continue
        c = dict(blk["cells"])
        # DERIVED, by identity only — never an estimate. The recurring leg is
        # reported combined in FY2017-FY2018 and split elsewhere (basis break
        # B1); one driver spans both by construction.
        if "recurring_combined_revenue" in c:
            c["recurring_revenue"] = c["recurring_combined_revenue"]
            c["recurring_cost"] = c.get("recurring_combined_cost")
        elif "hosp_revenue" in c and "other_revenue" in c:
            c["recurring_revenue"] = c["hosp_revenue"] + c["other_revenue"]
            if "hosp_cost" in c and "other_cost" in c:
                c["recurring_cost"] = c["hosp_cost"] + c["other_cost"]
        if "total_revenue" not in c and "dev_revenue" in c and "recurring_revenue" in c:
            c["total_revenue"] = c["dev_revenue"] + c["recurring_revenue"]
        if "net_profit" not in c and all(k in c for k in ("pbt", "tax")):
            c["net_profit"] = c["pbt"] + c["tax"] + c.get("deferred_tax", 0.0)
        if c.get("finance_cost") is None and c.get("finance_expenses") is not None:
            c["finance_cost"] = c["finance_expenses"] + c.get("bank_charges", 0.0)
        debt = [c[f] for f in DEBT_FIELDS if f in c]
        if debt:
            c["interest_bearing_debt"] = sum(debt)
        A[int(y)] = c
    for y, r in K["new_sales_value"].items():
        A.setdefault(int(y), {})["new_sales"] = r["value"]
    for y, r in K["backlog"].items():
        A.setdefault(int(y), {})["backlog"] = r["value"]
    M = json.load(open(os.path.join(HERE, "macro.json")))
    return A, M


def macro_paths(M):
    cpi = {int(k): v / 100.0 for k, v in M["cpi_pct"].items()}
    urb = {int(k): v for k, v in M["urban_pop"].items()}
    return cpi, urb


# ------------------------------------------------------------------- utilities
def ttm(A, field, o, n=3, fn=None):
    """Trailing n-year mean of a field (or of a function of the year's cells)."""
    vals = []
    for y in range(o - n + 1, o + 1):
        c = A.get(y)
        if not c:
            continue
        v = fn(A, y) if fn else c.get(field)
        if v is not None and math.isfinite(v):
            vals.append(v)
    return sum(vals) / len(vals) if vals else None


def _ratio(num, den):
    def f(A, y):
        c = A.get(y, {})
        a, b = c.get(num), c.get(den)
        if a is None or b in (None, 0):
            return None
        return a / b
    return f


def _conv(A, y):
    """Development revenue as a fraction of (opening backlog + new sales)."""
    c, p = A.get(y, {}), A.get(y - 1, {})
    rev, ns, bl = c.get("dev_revenue"), c.get("new_sales"), p.get("backlog")
    if None in (rev, ns, bl) or (bl + ns) <= 0:
        return None
    return rev / (bl + ns)


def ols(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - b * mx, b


# ------------------------------------------------------------------- the build
def project(A, cpi, urb, o, horizons=HORIZONS, foresight=False):
    """One origin's whole projection, on one macro setting."""
    out, notes = {}, []

    # --- macro path -------------------------------------------------------
    known_cpi = ttm(A, None, o, 3, fn=lambda A, y: cpi.get(y))
    if known_cpi is None:
        return None, ["no CPI history at origin"]
    def infl(h):
        if foresight:
            return math.prod(1 + cpi.get(o + k, known_cpi) for k in range(1, h + 1))
        return (1 + known_cpi) ** h
    # urban population, at the growth rate observable BEFORE the origin
    g_urb = ((urb[o] / urb[o - 3]) ** (1 / 3) - 1) if (o in urb and o - 3 in urb) else 0.0

    # --- driver parameters, all read at the origin ------------------------
    ns0 = A.get(o, {}).get("new_sales")
    intensity = (ns0 / urb[o]) if (ns0 and o in urb) else None
    delta = ttm(A, None, o, 3, fn=_conv)
    cost_ratio = ttm(A, None, o, 3, fn=_ratio("dev_cost", "dev_revenue"))
    rec0 = A.get(o, {}).get("recurring_revenue")
    rec_ratio = ttm(A, None, o, 3, fn=_ratio("recurring_cost", "recurring_revenue"))
    # trailing REAL growth of the recurring leg, so inflation is applied once
    rg = []
    for y in range(o - 2, o + 1):
        a, b = A.get(y, {}).get("recurring_revenue"), A.get(y - 1, {}).get("recurring_revenue")
        if a and b and b > 0 and cpi.get(y) is not None:
            rg.append((a / b) / (1 + cpi[y]) - 1)
    rec_real_g = sum(rg) / len(rg) if rg else 0.0

    xs, ys = [], []
    for y in range(o - 4, o + 1):
        c = A.get(y, {})
        if c.get("total_revenue") is not None and c.get("sga") is not None:
            xs.append(c["total_revenue"]); ys.append(-c["sga"])
    sga_fit = ols(xs, ys)

    d_rate = ttm(A, None, o, 3, fn=_ratio("da", "ppe"))
    kd = ttm(A, None, o, 3, fn=_ratio("finance_cost", "interest_bearing_debt"))
    debt0 = A.get(o, {}).get("interest_bearing_debt")
    ppe0 = A.get(o, {}).get("ppe")
    capex0 = ttm(A, None, o, 3, fn=lambda A, y: (
        (A.get(y, {}).get("ppe") - A.get(y - 1, {}).get("ppe") - A.get(y, {}).get("da"))
        if all(A.get(yy, {}).get(f) is not None
               for yy, f in ((y, "ppe"), (y - 1, "ppe"), (y, "da"))) else None))

    bl = A.get(o, {}).get("backlog")
    adv0 = A.get(o, {}).get("customer_advances")
    dp0 = A.get(o, {}).get("development_properties")
    col = ttm(A, None, o, 3, fn=lambda A, y: (
        ((A.get(y, {}).get("customer_advances", 0) - A.get(y - 1, {}).get("customer_advances", 0)
          + A.get(y, {}).get("dev_revenue", 0)) / A.get(y, {}).get("new_sales"))
        if (A.get(y, {}).get("customer_advances") is not None
            and A.get(y - 1, {}).get("customer_advances") is not None
            and A.get(y, {}).get("new_sales")) else None))
    if col is not None:
        col = min(max(col, 0.0), 1.5)

    # --- roll forward -----------------------------------------------------
    state = {"backlog": bl, "ppe": ppe0, "debt": debt0,
             "advances": adv0, "dev_props": dp0}
    for h in horizons:
        y = o + h
        f = {}
        if intensity is not None:
            # projected at the growth rate observable BEFORE the origin, as the
            # rule says. Gating this on the future actual being present in the
            # macro file silently produced no forward projection at all from the
            # last origin — and would have been a look-ahead if the file went
            # further.
            up = urb[o] * (1 + g_urb) ** h
            f["new_sales"] = up * intensity * infl(h)
        if delta is not None and state["backlog"] is not None and "new_sales" in f:
            d = min(max(delta, 1e-6), 1.0)          # deliveries cannot outrun the book
            base = state["backlog"] + f["new_sales"]
            f["dev_revenue"] = d * base
            state["backlog"] = base - f["dev_revenue"]
            f["backlog"] = state["backlog"]
        if cost_ratio is not None and "dev_revenue" in f:
            f["dev_cost"] = -abs(cost_ratio) * f["dev_revenue"]
        if rec0 is not None:
            f["recurring_revenue"] = rec0 * infl(h) * (1 + rec_real_g) ** h
            if rec_ratio is not None:
                f["recurring_cost"] = -abs(rec_ratio) * f["recurring_revenue"]
        if "dev_revenue" in f and "recurring_revenue" in f:
            f["total_revenue"] = f["dev_revenue"] + f["recurring_revenue"]
            if "dev_cost" in f and "recurring_cost" in f:
                f["gross_profit"] = f["total_revenue"] + f["dev_cost"] + f["recurring_cost"]
        if sga_fit and "total_revenue" in f:
            a, b = sga_fit
            f["sga"] = -(a * infl(h) + b * f["total_revenue"])
        if d_rate is not None and state["ppe"] is not None:
            da = d_rate * state["ppe"]
            f["da"] = -da
            cx = (capex0 or 0.0) * infl(h)
            state["ppe"] = state["ppe"] + cx - da
            f["ppe"] = state["ppe"]
            f["capex"] = cx
        if kd is not None and state["debt"] is not None:
            f["finance_cost"] = -abs(kd) * state["debt"]      # debt held flat: stated, not fitted
        if "gross_profit" in f:
            f["pbt"] = (f["gross_profit"] + f.get("sga", 0.0) + f.get("da", 0.0)
                        + f.get("finance_cost", 0.0))
            f["tax"] = -EGYPT_TAX * f["pbt"] if f["pbt"] > 0 else 0.0
            f["net_profit"] = f["pbt"] + f["tax"]
        if col is not None and state["advances"] is not None and "new_sales" in f:
            state["advances"] = (state["advances"] + col * f["new_sales"]
                                 - f.get("dev_revenue", 0.0))
            f["customer_advances"] = max(state["advances"], 0.0)
        if state["dev_props"] is not None and "dev_cost" in f:
            build = abs(cost_ratio or 0.0) * f.get("dev_revenue", 0.0) * infl(0)
            state["dev_props"] = state["dev_props"] + build + f["dev_cost"]
            f["development_properties"] = state["dev_props"]
        out[h] = f

    params = {"cpi_known": known_cpi, "urban_growth": g_urb, "intensity": intensity,
              "delta": delta, "dev_cost_ratio": cost_ratio, "rec_real_growth": rec_real_g,
              "rec_cost_ratio": rec_ratio, "sga_fit": sga_fit, "da_rate": d_rate,
              "kd": kd, "debt_at_origin": debt0, "capex": capex0,
              "collection_ratio": col, "foresight": foresight}
    return {"projection": out, "params": params}, notes


# --------------------------------------------------------------- benchmarks
def freeze(A, o, field, h):
    return A.get(o, {}).get(field)


def trend(A, o, field, h):
    a, b = A.get(o, {}).get(field), A.get(o - 3, {}).get(field)
    if a is None or b is None or b == 0 or (a / b) <= 0:
        return None
    return a * (a / b) ** (h / 3.0)


def main():
    A, M = load()
    cpi, urb = macro_paths(M)
    runs = {}
    for o in range(FIRST_ORIGIN, LAST_ORIGIN + 1):
        for fs in (False, True):
            r, notes = project(A, cpi, urb, o, foresight=fs)
            if r is None:
                continue
            runs["%d|%s" % (o, "foresight" if fs else "asknown")] = r
    json.dump({"runs": runs,
               "actuals": {str(y): A[y] for y in sorted(A)},
               "first_origin": FIRST_ORIGIN, "last_origin": LAST_ORIGIN,
               "last_actual": LAST_ACTUAL},
              open(os.path.join(HERE, "bottom_up.json"), "w"), indent=1)
    print("built %d origin-runs (%d origins x 2 macro settings)"
          % (len(runs), len(runs) // 2))
    o = 2019
    p = runs["2019|asknown"]["projection"]
    print("\\nexample — origin FY2019, as-known macro:")
    print("%-24s %10s %10s %10s %10s %10s" % ("", *["h=%d" % h for h in HORIZONS]))
    for f in ("new_sales", "dev_revenue", "total_revenue", "gross_profit", "net_profit"):
        print("%-24s" % f + "".join("%10.0f" % p[h][f] if f in p[h] else "%10s" % "-"
                                    for h in HORIZONS))
    print("%-24s" % "ACTUAL total_revenue" + "".join(
        "%10.0f" % A[o + h]["total_revenue"] if A.get(o + h, {}).get("total_revenue") else "%10s" % "-"
        for h in HORIZONS))


if __name__ == "__main__":
    main()
