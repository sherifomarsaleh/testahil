"""EGCH (KIMA) walk-forward — the build at every origin.

Implements PRE_REGISTRATION_01-09-2026.md §2 exactly and nothing else. Every parameter
here appears in that file with its value; none is fitted, and none may be changed now
that errors exist (L-042).

THE MACRO PATH IS ONE PATH (L-048): at every origin the world urea price is held flat in
dollars, the currency moves by relative PPP on the last published CPI differential, and
domestic costs compound on the same Egyptian CPI. Inflation, the currency and the product
price are the same event seen once.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P

MACRO = json.load(open(os.path.join(HERE, "macro.json")))
FY = MACRO["fiscal_year_derived"]

ORIGINS = ["FY%d" % y for y in range(2012, 2025)]
HORIZONS = [1, 2, 3, 4, 5]
BETA_DEFAULT = 1.0            # urea-price pass-through exponent on revenue, pre-registered
RATE_FLOOR = 0.10             # opening borrowings below 10% of revenue -> rate UNDEFINED (L-041)

FREEZE_EQUIVALENT = {"provisions", "other_bucket", "investment_income", "credit_interest", "urea_t"}
NO_MACRO_TERM = set(FREEZE_EQUIVALENT)


def y(fy):
    return int(fy[2:])


def fyname(n):
    return "FY%d" % n


# ---------------------------------------------------------------- macro paths
def cpi_eg_rate(origin, year, foresight):
    """Egyptian CPI rate applied in fiscal `year` (as a fraction)."""
    if foresight:
        return FY[year]["cpi_eg_pct"] / 100.0
    return FY[origin]["cpi_eg_pct_last_published"] / 100.0


def cpi_us_rate(origin):
    return FY[origin]["cpi_us_pct_last_published"] / 100.0


def cpi_path(origin, h, foresight=False):
    f = 1.0
    for k in range(1, h + 1):
        f *= 1.0 + cpi_eg_rate(origin, fyname(y(origin) + k), foresight)
    return f


def fx_level(origin, k, foresight=False):
    """EGP per USD in fiscal year origin+k (k=0 is the origin's own fiscal-year mean).

    knowable: relative PPP on the last published CPI differential at the origin.
    foresight: the realised fiscal-year mean.
    """
    if k == 0 or foresight:
        return FY[fyname(y(origin) + k)]["egp_usd"]
    f = FY[origin]["egp_usd"]
    r = (1.0 + FY[origin]["cpi_eg_pct_last_published"] / 100.0) / (1.0 + cpi_us_rate(origin))
    return f * r ** k


def urea_egp_ratio(origin, h, foresight=False):
    """U_egp(o+h) / U_egp(o): urea flat in dollars on the knowable path, realised otherwise."""
    if foresight:
        return FY[fyname(y(origin) + h)]["urea_egp"] / FY[origin]["urea_egp"]
    return fx_level(origin, h) / fx_level(origin, 0)


# ---------------------------------------------------------------- the build
def borrowing_rate(origin):
    """r(o) = debit interest(o) / OPENING interest-bearing borrowings; None where undefined."""
    a = P.actual(origin)
    prev = P.borrowings_total(fyname(y(origin) - 1))
    if prev is None or a["debit_interest"] is None:
        return None
    if prev < RATE_FLOOR * a["revenue"]:
        return None
    return a["debit_interest"] / prev


def usd_borrowings(origin):
    """Bank borrowings at the origin, treated as dollar-denominated (stated simplification)."""
    b = P.BORROWINGS.get(origin)
    if not b or b["bank"] is None:
        return 0.0
    return b["bank"] + b["current"]


def project(origin, h, beta=BETA_DEFAULT, foresight=False, foresight_cpi_only=False,
            cost_on_fx=False):
    """One origin, one horizon, under the pre-registered rules. None where an input is missing."""
    o = P.actual(origin)
    cpi = cpi_path(origin, h, foresight=foresight or foresight_cpi_only)
    fx_full = foresight and not foresight_cpi_only
    ur = urea_egp_ratio(origin, h, foresight=fx_full)
    fxr = fx_level(origin, h, fx_full) / fx_level(origin, 0)
    fx_step = fx_level(origin, h, fx_full) / fx_level(origin, h - 1, fx_full)

    out = {}
    out["revenue"] = o["revenue"] * ur ** beta
    out["urea_t"] = o["urea_t"]                                  # D1v, flat, unit window only
    out["cost_of_sales"] = o["cost_of_sales"] * (fxr if cost_on_fx else cpi)
    out["selling"] = o["selling"] * cpi if o["selling"] else o["selling"]
    out["admin"] = o["admin"] * cpi
    out["provisions"] = o["provisions"]
    out["other_bucket"] = o["other_bucket"]
    out["reval_gain"] = 0.0
    out["investment_income"] = o["investment_income"]
    out["credit_interest"] = o["credit_interest"]
    # D7 currency result on dollar debt, on the same currency path
    out["fx"] = -usd_borrowings(origin) * (fx_step - 1.0) if usd_borrowings(origin) > 0 else 0.0
    # D10 debit interest from the borrowings that bear it
    r = borrowing_rate(origin)
    B = P.borrowings_total(origin)
    if r is None or B is None:
        out["debit_interest"] = o["debit_interest"]
        out["rate_defined"] = False
    else:
        out["debit_interest"] = r * B * fxr
        out["rate_defined"] = True
        out["rate"] = r
    out["gross_profit"] = None if out["cost_of_sales"] is None else out["revenue"] - out["cost_of_sales"]
    need = ["cost_of_sales", "selling", "admin", "provisions", "other_bucket", "investment_income",
            "credit_interest", "debit_interest"]
    if any(out[k] is None for k in need):
        out["pbt"] = out["tax_current"] = out["net"] = None
        return out
    out["pbt"] = (out["revenue"] - out["cost_of_sales"] - out["selling"] - out["admin"]
                  - out["provisions"] + out["other_bucket"] + out["reval_gain"] + out["fx"]
                  + out["investment_income"] + out["credit_interest"] - out["debit_interest"])
    tau = P.TAX_REGIME[origin]
    out["tax_current"] = tau * max(out["pbt"], 0.0)
    out["deferred_tax"] = 0.0
    out["solidarity"] = 0.0
    out["net"] = out["pbt"] - out["tax_current"]
    return out


def freeze(origin, h):
    return P.actual(origin)


def trend(origin, h):
    """Every line at its own trailing CAGR, longest window available, capped at 3y.
    Non-positive base or origin values are held flat. Returns the window used."""
    i = P.YEARS.index(origin)
    win = min(3, i)
    # walk back to a complete year, shortening the window if a hole is hit
    base = None
    for w in range(win, 0, -1):
        cand = P.YEARS[i - w]
        if cand in P.COMPLETE:
            base, win = cand, w
            break
    if base is None:
        return None, 0
    a_now, a_base = P.actual(origin), P.actual(base)
    out = {}
    for k, v in a_now.items():
        b = a_base.get(k)
        if v is None or b is None or b <= 0 or v <= 0:
            out[k] = v
        else:
            out[k] = v * ((v / b) ** (1.0 / win)) ** h
    return out, win


def cells():
    out = []
    for o in ORIGINS:
        for h in HORIZONS:
            t = fyname(y(o) + h)
            if t in P.IS and y(t) <= 2025:
                out.append((o, h, t))
    return out


if __name__ == "__main__":
    cs = cells()
    print("origins %d, cells %d" % (len(ORIGINS), len(cs)))
    for o, h, t in cs:
        p = project(o, h)
        a = P.actual(t)
        print("  %s h=%d -> %s  rev proj %10.0f act %10.0f   net proj %10s act %10s  rate=%s"
              % (o, h, t, p["revenue"], a["revenue"],
                 "%.0f" % p["net"] if p["net"] is not None else "n/a",
                 "%.0f" % a["net"] if a["net"] is not None else "n/a",
                 "%.3f" % p["rate"] if p.get("rate_defined") else "undef"))
