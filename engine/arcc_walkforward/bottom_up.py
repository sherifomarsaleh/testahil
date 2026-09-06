"""ARCC walk-forward — the ground-up build at every origin.

Implements PRE_REGISTRATION_01-09-2026.md §2 and §3 exactly. Nothing here
chooses anything: every rule and every parameter was fixed in writing before a
single error was computed, and this module only executes them.

THE INFORMATION SET AT AN ORIGIN is what was available when that origin year's
AUDITED ACCOUNTS were published — roughly the first quarter of the following
year. That is the only coherent reading: the panel takes each company year as
first reported, which is a document published months after the year end, so an
origin that could see those accounts could also see the calendar year's
published inflation and exchange rate. Stated because the alternative reading
(strictly 31 December) would pair a company figure from March with a macro
figure from the previous December, and a mismatched information set is a silent
handicap rather than a discipline.
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P

with open(os.path.join(HERE, "macro.json")) as f:
    MACRO = json.load(f)["series"]

ORIGINS = P.ORIGINS
HORIZONS = P.HORIZONS
W_DEFAULT = 0.5          # pre-registered blend weight on the coal path (D7)
W_SENSITIVITY = (0.3, 0.5, 0.7)
TAX_RATE = 0.225         # Egyptian statutory rate (D18)

# Eras, declared in the pre-registration: E1 spans the 2016 float and the long
# stable stretch after it; E2 the 2022-2024 devaluation sequence.
ERA = {o: ("E1 pre-2022" if int(o[2:]) <= 2021 else "E2 devaluation sequence")
       for o in ORIGINS}


def _y(fy):
    return int(fy[2:])


def _m(key, fy):
    v = MACRO[key]["values"].get(str(_y(fy)))
    return None if v is None else float(v)


def cpi(fy):
    """Egyptian annual consumer price inflation, as a rate."""
    return _m("cpi_pct", fy) / 100.0


def fx_dep(fy):
    """EGP/USD depreciation over the year, as a rate."""
    a, b = _m("egp_usd", "FY%d" % (_y(fy) - 1)), _m("egp_usd", fy)
    return b / a - 1.0


def pop_growth(fy):
    a, b = _m("population", "FY%d" % (_y(fy) - 1)), _m("population", fy)
    return b / a - 1.0


def coal_egp(fy):
    """South African coal, calendar-year mean, in EGP per tonne."""
    return _m("coal_sa", fy) * _m("egp_usd", fy)


# ---------------------------------------------------------------------------
# Actuals — the driver values the projection is scored against.
# ---------------------------------------------------------------------------
def actual(fy):
    loc, exp, tot = P.volumes(fy)
    pl, pe = P.prices(fy)
    rm, tr, ov = P.unit_costs(fy)
    c, r, o, i = P.COST[fy], P.REV[fy], P.OTHER[fy], P.IS[fy]
    return {
        "vol_local": loc, "vol_export": exp, "vol_total": tot,
        "price_local": pl, "price_export": pe,
        "services": r["svc_local"] + r["svc_export"],
        "raw_per_t": rm, "transport_per_t": tr, "overhead_per_t": ov,
        "raw": c["raw"], "transport": c["transport"], "overhead": c["overhead"],
        "mfg_dep": c["mfg_dep"], "amort": c["amort"], "rou": c["rou"],
        "revenue": i["revenue"], "cogs": i["cogs"], "gross_profit": i["gross_profit"],
        "ga": i["ga"], "provisions": -o["provisions"], "reversals": o["reversals"],
        "interest_income": o["interest_income"], "other_income": o["other_income"],
        "impairments": -o["impairments"], "finance_costs": -o["finance_costs"],
        "fx": o["fx"], "disposals": o["disposals"], "jv": o["jv"],
        "pbt": i["pbt"], "tax": i["tax"], "pat": i["pat"], "majority": i["majority"],
    }


# ---------------------------------------------------------------------------
# The projection.
# ---------------------------------------------------------------------------
def _paths(o, h, foresight, cpi_only):
    """The macro multipliers this cell runs on.

    KNOWABLE holds the origin's last published RATE and compounds it; it does
    not hold the level flat, which would be a different and weaker rule. Coal is
    the exception and is held at its LEVEL: a commodity price has no drift and
    assuming one would be a forecast, not a rule.
    """
    t = "FY%d" % (_y(o) + h)
    # cpi_only is a variant OF foresight, not a setting of its own. Asking for it
    # without foresight used to fall through and return the as-known paths, so a
    # caller got the as-known answer under a foresight label -- an absent answer
    # wearing the costume of a result [R-ENF-04]. It refuses now.
    if cpi_only and not foresight:
        raise ValueError("cpi_only requires foresight=True; it is a variant of the "
                         "foresight path, not a setting on the knowable one")
    if foresight:
        pi = (1 + cpi(o)) ** h if False else _cum_cpi_realised(o, h)
        fxm = _m("egp_usd", t) / _m("egp_usd", o)
        coal = 1.0 if cpi_only else coal_egp(t) / coal_egp(o)
        if cpi_only:
            fxm = (1 + fx_dep(o)) ** h
        return pi, fxm, coal
    return (1 + cpi(o)) ** h, (1 + fx_dep(o)) ** h, 1.0


def _cum_cpi_realised(o, h):
    m = 1.0
    for k in range(1, h + 1):
        m *= (1 + cpi("FY%d" % (_y(o) + k)))
    return m


def project(o, h, w=W_DEFAULT, foresight=False, cpi_only=False):
    a = actual(o)
    pi, fxm, coalm = _paths(o, h, foresight, cpi_only)
    pop = (1 + pop_growth(o)) ** h

    vol_local = a["vol_local"] * pop                    # D1
    vol_export = a["vol_export"]                        # D2 (flat)
    vol_total = vol_local + vol_export
    price_local = a["price_local"] * pi                 # D4
    price_export = a["price_export"] * fxm              # D5
    services = a["services"] * pi                       # D6
    raw_t = a["raw_per_t"] * (w * coalm + (1 - w) * pi)  # D7
    tr_t = a["transport_per_t"] * pi                    # D8
    ov_t = a["overhead_per_t"] * pi                     # D9
    mfg_dep, amort, rou = a["mfg_dep"], a["amort"], a["rou"]   # D10, D11
    ga = a["ga"] * pi                                   # D12

    revenue = price_local * vol_local * 1000.0 + price_export * vol_export * 1000.0 + services
    raw = raw_t * vol_total * 1000.0
    transport = tr_t * vol_total * 1000.0
    overhead = ov_t * vol_total * 1000.0
    cogs = raw + transport + overhead + mfg_dep + amort + rou
    gross_profit = revenue - cogs

    provisions = a["provisions"]                        # D13 (flat)
    reversals = a["reversals"]
    impairments = a["impairments"]
    interest_income = a["interest_income"]              # D14 (flat)
    other_income = a["other_income"]                    # D15 (flat)
    finance_costs = a["finance_costs"]                  # D16 — rate x borrowings, both flat
    fx = 0.0                                            # D17 — refused, not modelled
    disposals, jv = a["disposals"], a["jv"]

    pbt = (gross_profit - ga - provisions + reversals - impairments
           + interest_income + other_income - finance_costs + fx + disposals + jv)
    tax = TAX_RATE * pbt if pbt > 0 else 0.0            # D18
    pat = pbt - tax
    share = (a["majority"] / a["pat"]) if a["pat"] else 1.0   # D19
    return {
        "vol_local": vol_local, "vol_export": vol_export, "vol_total": vol_total,
        "price_local": price_local, "price_export": price_export, "services": services,
        "raw_per_t": raw_t, "transport_per_t": tr_t, "overhead_per_t": ov_t,
        "raw": raw, "transport": transport, "overhead": overhead,
        "mfg_dep": mfg_dep, "amort": amort, "rou": rou,
        "revenue": revenue, "cogs": cogs, "gross_profit": gross_profit, "ga": ga,
        "provisions": provisions, "reversals": reversals, "impairments": impairments,
        "interest_income": interest_income, "other_income": other_income,
        "finance_costs": finance_costs, "fx": fx, "disposals": disposals, "jv": jv,
        "pbt": pbt, "tax": tax, "pat": pat, "majority": pat * share,
    }


def freeze(o, h):
    """Every line flat at the origin's last actual."""
    a = dict(actual(o))
    a["fx"] = a["fx"]
    return a


def trend(o, h, cap=3):
    """Every line grown at its own trailing CAGR, window capped at three years.

    A line that is zero or negative at either end of the window has no CAGR; it
    is held flat there and the fallback is COUNTED, because a benchmark that
    quietly becomes FREEZE on the hard lines is a benchmark that flatters the
    method it is meant to test.
    """
    a = actual(o)
    back = min(cap, _y(o) - 2014)
    if back < 1:
        return None, 0
    b = actual("FY%d" % (_y(o) - back))
    out, fell_back = {}, 0
    for k, v in a.items():
        v0 = b.get(k)
        if v is None or v0 is None or v0 <= 0 or v <= 0:
            out[k] = v
            fell_back += 1
            continue
        out[k] = v * (v / v0) ** (float(h) / back)
    return out, fell_back


def cells():
    """(origin, horizon, target) for every cell whose target year exists."""
    out = []
    for o in ORIGINS:
        for h in HORIZONS:
            t = "FY%d" % (_y(o) + h)
            if t in P.IS:
                out.append((o, h, t))
    return out


if __name__ == "__main__":
    cs = cells()
    print("origins %s" % ", ".join(ORIGINS))
    print("scoreable cells: %d" % len(cs))
    for o in ORIGINS:
        hs = [h for (oo, h, _) in cs if oo == o]
        print("  %-8s h=%-14s cpi=%5.1f%%  fx=%6.1f%%  pop=%4.2f%%  coal=%8.0f EGP/t"
              % (o, ",".join(map(str, hs)) or "-", 100 * cpi(o), 100 * fx_dep(o),
                 100 * pop_growth(o), coal_egp(o)))
    print()
    o, h, t = cs[0]
    p, a = project(o, h), actual(t)
    print("worked cell %s h=%d -> %s" % (o, h, t))
    for k in ("vol_total", "price_local", "price_export", "raw_per_t", "revenue",
              "cogs", "gross_profit", "pbt", "pat"):
        print("   %-14s projected %16.1f   actual %16.1f   log err %+7.3f"
              % (k, p[k], a[k], math.log(p[k] / a[k]) if p[k] > 0 and a[k] > 0 else float("nan")))
