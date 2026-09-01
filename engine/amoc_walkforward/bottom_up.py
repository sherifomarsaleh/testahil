"""AMOC walk-forward — the ground-up build at every origin.

Implements PRE_REGISTRATION_01-09-2026.md §2 exactly and nothing else. Every
parameter here appears in that file with its value; none is fitted, and none may
be changed now that errors exist (L-042).

The build is per product line for revenue (volume x realisation, on the constant
eight-line taxonomy of B-2) and by NATURE for cost, because that is the level the
filings disclose cost at and the company itself could not cost per product before
July 2023 (B-7).
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P

MACRO = json.load(open(os.path.join(HERE, "macro.json")))
FY = MACRO["fiscal_year_derived"]

ORIGINS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
HORIZONS = [1, 2, 3]
TAX_RATE = 0.225                 # Egyptian statutory corporate rate, pre-registered
BETA_DEFAULT = 1.0               # crude pass-through exponent, pre-registered

# Which drivers are level-persistence rules and therefore EQUAL the freeze
# benchmark by construction. Declared in the pre-registration, listed here so
# the scorer reports "n/a - rule equals benchmark" rather than a zero skill it
# might be mistaken for a measurement.
FREEZE_EQUIVALENT = {"volume_t", "depreciation", "other_expenses",
                     "claims_provision", "investment_revenues", "finance_expenses"}
# Drivers with no CPI and no Brent term: their macro share MUST be exactly zero.
NO_MACRO_TERM = set(FREEZE_EQUIVALENT)


def y(fy):
    return int(fy[2:])


def cpi_path(origin, h, foresight=False):
    """Compounding CPI over h years.

    knowable: the last published annual rate at the origin, held flat forward.
    foresight: the realised rate each year.
    """
    f = 1.0
    for k in range(1, h + 1):
        if foresight:
            r = FY["FY%d" % (y(origin) + k)]["cpi_pct"] / 100.0
        else:
            r = FY[origin]["cpi_pct"] / 100.0
        f *= (1.0 + r)
    return f


def brent_ratio(origin, h, foresight=False):
    """BR(o+h)/BR(o) in EGP.

    knowable: no forecast of crude or of the currency is permitted at an origin,
    so the ratio is 1.0 — the origin's own crude-in-EGP level carried forward.
    That is the honest reading of 'each origin sees only what was published by
    that date': nobody at the origin knew the devaluation was coming.
    """
    if not foresight:
        return 1.0
    return FY["FY%d" % (y(origin) + h)]["brent_egp"] / FY[origin]["brent_egp"]


def project(origin, h, beta=BETA_DEFAULT, foresight=False, foresight_cpi_only=False):
    """One origin, one horizon, under the pre-registered rules."""
    o = P.IS[origin]
    lines_o = P.common_lines(origin)
    cost_o = P.COST_STACK[origin]
    orev_o = P.OTHER_REVENUE[origin]
    tonnes_o = P.PRODUCTS[origin]["total"][0]

    cpi = cpi_path(origin, h, foresight=foresight or foresight_cpi_only)
    br = brent_ratio(origin, h, foresight=foresight and not foresight_cpi_only)

    # D1/D2 volume and mix flat at the origin
    tonnes = tonnes_o
    line_t = {k: v[0] for k, v in lines_o.items()}

    # D3 realisation per line, crude pass-through
    line_rev = {}
    for k, (t, e) in lines_o.items():
        r = (e / t) if t else 0.0
        line_rev[k] = line_t[k] * r * (br ** beta)
    net_sales = sum(line_rev.values())

    # D4 feedstock, SAME index, SAME exponent as D3
    raw_per_t = cost_o["raw_materials"] / tonnes_o
    raw = raw_per_t * tonnes * (br ** beta)
    # D5-D8 conversion
    salaries = cost_o["salaries"] * cpi
    supporting = (cost_o["supporting_materials"] / tonnes_o) * tonnes * cpi
    other_cos = (cost_o["other"] / tonnes_o) * tonnes * cpi
    depreciation = cost_o["depreciation"]
    cost_of_sales = raw + salaries + supporting + depreciation + other_cos

    # D9-D11 operating expenses
    ga = o["ga"] * cpi
    marketing = (o["marketing"] / tonnes_o) * tonnes * cpi
    other_expenses = o["other_expenses"]

    # D12 provision, D14 investment revenue, D15 finance charge
    claims = o["claims_provision"]
    inv_rev = o["investment_revenues"]
    finance = o.get("finance_expenses", 0)

    # D13 other revenue: credit interest only; FX and the rest are zero
    credit_interest = orev_o["credit_interest"] * cpi
    other_revenues = credit_interest

    gross_profit = net_sales - cost_of_sales
    operating_profit = gross_profit - ga - marketing - other_expenses
    pbt = operating_profit - claims - finance + other_revenues + inv_rev
    tax = TAX_RATE * pbt                                   # D16; D17 deferred tax = 0
    npat = pbt - tax
    nci_share = o["nci"] / o["npat"] if o["npat"] else 0.0  # D18
    nci = nci_share * npat
    majority = npat - nci

    return dict(volume_t=tonnes, net_sales=net_sales, raw_materials=raw, salaries=salaries,
                supporting_materials=supporting, depreciation=depreciation,
                other_cos=other_cos, cost_of_sales=cost_of_sales, gross_profit=gross_profit,
                ga=ga, marketing=marketing, other_expenses=other_expenses,
                operating_profit=operating_profit, claims_provision=claims,
                finance_expenses=finance, other_revenues=other_revenues,
                credit_interest=credit_interest, investment_revenues=inv_rev, pbt=pbt,
                income_tax=tax, npat=npat, nci=nci, majority=majority,
                line_revenue=line_rev, line_tonnes=line_t)


def freeze(origin, h):
    """Every line flat at the origin's actual, nominal."""
    return _actual_shape(origin)


def trend(origin, h):
    """Every line at its own trailing CAGR, longest window available, capped at 3y.

    Returns None at FY2021, where no prior year exists — declared in advance.
    """
    i = ORIGINS.index(origin)
    win = min(i, 3)
    if win == 0:
        return None
    base = ORIGINS[i - win]
    a_now, a_base = _actual_shape(origin), _actual_shape(base)
    out = {}
    for k, v in a_now.items():
        b = a_base.get(k)
        if b is None or b <= 0 or v <= 0:
            out[k] = v
        else:
            out[k] = v * ((v / b) ** (1.0 / win)) ** h
    return out


def _actual_shape(fy):
    """The reported year in the same shape a projection carries."""
    o = P.IS[fy]
    c = P.COST_STACK[fy]
    orev = P.OTHER_REVENUE[fy]
    return dict(volume_t=P.PRODUCTS[fy]["total"][0], net_sales=o["net_sales"],
                raw_materials=c["raw_materials"], salaries=c["salaries"],
                supporting_materials=c["supporting_materials"], depreciation=c["depreciation"],
                other_cos=c["other"], cost_of_sales=o["cost_of_sales"],
                gross_profit=o["gross_profit"], ga=o["ga"], marketing=o["marketing"],
                other_expenses=o["other_expenses"],
                operating_profit=o["gross_profit"] - o["ga"] - o["marketing"] - o["other_expenses"],
                claims_provision=o["claims_provision"],
                finance_expenses=o.get("finance_expenses", 0),
                other_revenues=o["other_revenues"], credit_interest=orev["credit_interest"],
                investment_revenues=o["investment_revenues"], pbt=o["pbt"],
                income_tax=o["income_tax"], npat=o["npat"], nci=o["nci"],
                majority=o["majority"])


def actual(fy):
    return _actual_shape(fy)


def cells():
    """Every scoreable (origin, horizon) pair."""
    out = []
    for o in ORIGINS:
        for h in HORIZONS:
            t = "FY%d" % (y(o) + h)
            if t in P.IS:
                out.append((o, h, t))
    return out


if __name__ == "__main__":
    cs = cells()
    print("scoreable cells: %d" % len(cs))
    for o, h, t in cs:
        p = project(o, h)
        a = actual(t)
        print("  %s h=%d -> %s   sales proj %12.0f vs act %12.0f   majority proj %11.0f vs act %11.0f"
              % (o, h, t, p["net_sales"], a["net_sales"], p["majority"], a["majority"]))
