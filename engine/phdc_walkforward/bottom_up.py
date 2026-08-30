"""PHDC bottom-up projection at every historical origin.

Implements the rules fixed in PRE_REGISTRATION_30-08-2026.md, unchanged. At an
origin the model sees only fiscal years <= that origin, and only figures as
first reported. Every parameter is a stated function of the information set at
the origin; nothing is fitted to the outcome it is later scored on.

Each origin is projected TWICE:
  as_known           the inflation path a forecaster could have used at the origin
  perfect_foresight  the realised inflation path
The gap between the two is the macro share of the error, which is the only
honest way to separate an Egyptian developer's forecasting record from four
currency devaluations.
"""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))
HORIZONS = [1, 2, 3, 4, 5]


def load():
    p = json.load(open(os.path.join(HERE, "panel.json")))
    out = {}
    for ystr, fields in p.items():
        y = int(ystr)
        out[y] = {k: v["value"] for k, v in fields.items()}
    return out


class View:
    """The panel as it stood at one origin: nothing later, nothing restated."""

    def __init__(self, panel, origin):
        self.panel = panel
        self.origin = origin

    def get(self, year, field, default=None):
        if year > self.origin:
            return default
        return self.panel.get(year, {}).get(field, default)

    def series(self, field, lo=None, hi=None):
        hi = self.origin if hi is None else min(hi, self.origin)
        out = {}
        for y in range(lo or 1990, hi + 1):
            v = self.get(y, field)
            if v is not None:
                out[y] = v
        return out

    def latest(self, field, back=6):
        """Most recent disclosed (year, value) at or before the origin.

        The pre-registered rules key each base level on the origin year itself.
        Where the company has not disclosed that driver for the origin year —
        PHDC published no full-year results release for FY2025, so units sold
        and new sales stop at FY2024 and FY2023 — the rule is undefined rather
        than zero. It is extended, uniformly and disclosed, to the most recent
        year the driver IS disclosed, with the exogenous anchor measured in that
        same year so the intensity stays dimensionally consistent. The lag is
        recorded on every projection that uses one.
        """
        for y in range(self.origin, self.origin - back, -1):
            v = self.get(y, field)
            if v is not None:
                return y, v
        return None, None

    def ttm(self, field, n=3, transform=None):
        s = self.series(field)
        ys = sorted(s)[-n:]
        vals = [transform(y) if transform else s[y] for y in ys]
        vals = [v for v in vals if v is not None]
        return sum(vals) / len(vals) if vals else None

    def ttm_ratio(self, num, den, n=3):
        vals = []
        for y in range(self.origin - n + 1, self.origin + 1):
            a, b = self.get(y, num), self.get(y, den)
            if a is not None and b not in (None, 0):
                vals.append(a / b)
        return sum(vals) / len(vals) if vals else None


def cagr(view, field, back=3):
    a = view.get(view.origin, field)
    b = view.get(view.origin - back, field)
    if a is None or b is None or b <= 0 or a <= 0:
        return None
    return (a / b) ** (1.0 / back) - 1.0


# --------------------------------------------------------------------------
def project(panel, origin, macro="as_known", horizons=HORIZONS):
    """Bottom-up projection for origin+1 .. origin+max(horizons)."""
    v = View(panel, origin)
    H = max(horizons)
    out = {h: {} for h in horizons}

    # ---- exogenous paths ---------------------------------------------------
    if macro == "as_known":
        pi = v.ttm("macro.cpi_pct", 3)
        cpi_path = {h: (pi or 0.0) / 100.0 for h in range(1, H + 1)}
    else:
        cpi_path = {}
        for h in range(1, H + 1):
            r = panel.get(origin + h, {}).get("macro.cpi_pct")
            cpi_path[h] = (r if r is not None else 0.0) / 100.0

    def urban_at(y):
        return v.get(y, "macro.urban_pop")

    def urban(h, base=origin):
        """Urban population h years after `base`, at the rate known at the origin."""
        u0 = urban_at(origin)
        u3 = urban_at(origin - 3)
        if u0 is None:
            return None
        g = (u0 / u3) ** (1 / 3.0) - 1.0 if u3 else 0.0
        return u0 * (1 + g) ** (origin + h - base if base != origin else h)

    # ---- D1 units sold: exogenous volume anchor ---------------------------
    uy, units0 = v.latest("units_sold")
    u_base = urban_at(uy) if uy else None
    intensity = (units0 / u_base) if (units0 and u_base) else None
    lag_units = (origin - uy) if uy else None

    # ---- D2 average selling price -----------------------------------------
    # A price per unit is only a price if both halves come from the SAME year.
    # PHDC's disclosure stops at different years for the two — new sales run to
    # FY2024, units sold to FY2023 — so taking each one's latest separately
    # would divide one year's value by another year's volume and call the
    # result a price. The anchor is the latest year that discloses both.
    ay, asp0 = None, None
    for y in range(origin, origin - 6, -1):
        ns_y, u_y = v.get(y, "new_sales"), v.get(y, "units_sold")
        if ns_y and u_y:
            ay, asp0 = y, ns_y / u_y
            break
    lag_asp = (origin - ay) if ay else None

    # ---- D4 recognition rate ----------------------------------------------
    delta = recognition_rate(v)

    # ---- D5/D6 deliveries and cost per unit --------------------------------
    deliv0 = v.get(origin, "units_delivered")
    deliv_ttm = v.ttm("units_delivered", 3)
    cpu0 = v.ttm_ratio("is.cogs", "units_delivered", 3)

    # ---- D7 SG&A: fixed + variable, OLS on the trailing five years --------
    a_sga, b_sga = ols_sga(v)

    # ---- D8 D&A from a PP&E roll-forward ----------------------------------
    d_rate = None
    for y in range(origin - 2, origin + 1):
        da, ppe0 = v.get(y, "is.admin_depr"), v.get(y - 1, "bs.fixed_assets")
        if da is not None and ppe0:
            d_rate = (d_rate or 0) + da / ppe0
    if d_rate is not None:
        n_obs = sum(1 for y in range(origin - 2, origin + 1)
                    if v.get(y, "is.admin_depr") is not None and v.get(y - 1, "bs.fixed_assets"))
        d_rate = d_rate / max(1, n_obs)
    ppe = v.get(origin, "bs.fixed_assets")
    capex_rate = v.ttm_ratio("construction_spend", "is.revenue", 3)

    # ---- D9 interest, D10 tax ---------------------------------------------
    kd = v.ttm_ratio("is.finance_cost", "bs.total_current_liabs", 3)
    debt0 = v.get(origin, "bs.total_current_liabs")
    tax_rate = 0.225 if origin >= 2015 else 0.25          # regime known at origin

    # ---- roll forward ------------------------------------------------------
    backlog = rolled_backlog(v)
    bl = backlog.get(origin)
    if bl is None and backlog:
        bl = backlog[max(backlog)]          # latest rolled or disclosed anchor
    rev_prev = v.get(origin, "is.revenue")
    for h in range(1, H + 1):
        infl = 1.0
        for k in range(1, h + 1):
            infl *= (1 + cpi_path[k])

        units = intensity * urban(h) if (intensity and urban(h)) else None
        # an ASP anchored on a lagged year is escalated over the full gap, not
        # just the forecast horizon, or the price path silently starts late
        asp = asp0 * infl * ((1 + cpi_path[1]) ** (lag_asp or 0)) if asp0 else None
        new_sales = units * asp if (units and asp) else None

        rev = None
        if delta is not None and bl is not None and new_sales is not None:
            rev = delta * (bl + new_sales)
            bl = bl + new_sales - rev

        deliveries = None
        if deliv_ttm is not None and units0 and units:
            deliveries = deliv_ttm * (units / units0)

        cogs = None
        if cpu0 is not None and deliveries is not None:
            cogs = cpu0 * infl * deliveries
        gross = (rev - cogs) if (rev is not None and cogs is not None) else None

        sga = None
        if a_sga is not None and rev is not None:
            sga = a_sga * infl + b_sga * rev

        da = None
        if d_rate is not None and ppe is not None:
            da = d_rate * ppe
            capex = (capex_rate * rev) if (capex_rate is not None and rev) else 0.0
            ppe = ppe + capex - da

        interest = kd * debt0 if (kd is not None and debt0 is not None) else None
        ebit = None
        if gross is not None and sga is not None:
            ebit = gross - sga - (da or 0.0)
        npbt = (ebit - interest) if (ebit is not None and interest is not None) else None
        npat = npbt * (1 - tax_rate) if (npbt is not None and npbt > 0) else \
            (npbt if npbt is not None else None)

        if h in out:
            out[h] = {"units_sold": units, "asp": asp, "new_sales": new_sales,
                      "is.revenue": rev, "is.cogs": cogs, "is.gross_profit": gross,
                      "units_delivered": deliveries, "is.sga": sga,
                      "is.finance_cost": interest, "is.admin_depr": da,
                      "is.npbt": npbt,
                      "is.npat_mi": npat, "backlog": bl,
                      "_lag_units": lag_units, "_lag_asp": lag_asp}
        rev_prev = rev
    return out


def recognition_rate(v):
    """delta = revenue / (opening backlog + new sales), trailing three years."""
    bl = rolled_backlog(v)
    vals = []
    for y in range(v.origin - 2, v.origin + 1):
        rev, ns, b0 = v.get(y, "is.revenue"), v.get(y, "new_sales"), bl.get(y - 1)
        if rev is not None and ns is not None and b0 is not None and (b0 + ns) > 0:
            vals.append(rev / (b0 + ns))
    return sum(vals) / len(vals) if vals else None


def rolled_backlog(v):
    """Backlog rolled from the earliest DISCLOSED anchor at or before the origin.

    The company discloses backlog in only some releases, so the series is rolled
    as backlog_t = backlog_{t-1} + new sales_t - revenue_t from the earliest
    anchor visible at this origin. Where a later disclosed backlog is also
    visible the roll is re-anchored on it, so a disclosed figure always beats a
    rolled one and the roll never drifts across more years than it must.
    """
    ns = v.series("new_sales")
    rev = v.series("is.revenue")
    disc = v.series("backlog")
    if not disc:
        return {}
    out = {}
    start = min(disc)
    cur = disc[start]
    out[start] = cur
    for y in range(start + 1, v.origin + 1):
        if y in disc:
            cur = disc[y]
        elif y in ns and y in rev:
            cur = cur + ns[y] - rev[y]
        else:
            continue
        out[y] = cur
    return out


def ols_sga(v, n=5):
    """SG&A = a + b x revenue, ordinary least squares on the trailing n years."""
    xs, ys = [], []
    for y in range(v.origin - n + 1, v.origin + 1):
        r, s = v.get(y, "is.revenue"), v.get(y, "is.sga")
        if r is not None and s is not None:
            xs.append(r)
            ys.append(s)
    if len(xs) < 3:
        return None, None
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return my, 0.0
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den
    return my - b * mx, b


# --------------------------------------------------------------------------
BENCH_FIELDS = ["units_sold", "asp", "new_sales", "is.revenue", "is.cogs",
                "is.gross_profit", "units_delivered", "is.sga", "is.admin_depr",
                "is.finance_cost", "is.npbt", "is.npat_mi"]


def actual(panel, year, field):
    if field == "asp":
        ns = panel.get(year, {}).get("new_sales")
        u = panel.get(year, {}).get("units_sold")
        return (ns / u) if (ns and u) else None
    return panel.get(year, {}).get(field)


def freeze(panel, origin, horizons=HORIZONS):
    return {h: {f: actual(panel, origin, f) for f in BENCH_FIELDS} for h in horizons}


def trend(panel, origin, horizons=HORIZONS, back=3):
    v = View(panel, origin)
    out = {}
    for h in horizons:
        row = {}
        for f in BENCH_FIELDS:
            a0 = actual(panel, origin, f)
            ab = actual(panel, origin - back, f)
            if a0 is None or ab is None or ab <= 0 or a0 <= 0:
                row[f] = None
            else:
                row[f] = a0 * ((a0 / ab) ** (h / float(back)))
        out[h] = row
    return out


if __name__ == "__main__":
    panel = load()
    for o in (2018, 2020):
        p = project(panel, o)
        print("=== origin FY%d (as-known macro) ===" % o)
        print("  h  %-10s %-10s %-10s %-10s %-10s" %
              ("units", "asp", "new sales", "revenue", "net profit"))
        for h in HORIZONS:
            r = p[h]
            f = lambda k: "-" if r.get(k) is None else "%.1f" % r[k]
            print("  %d  %-10s %-10s %-10s %-10s %-10s" %
                  (h, f("units_sold"), f("asp"), f("new_sales"),
                   f("is.revenue"), f("is.npat_mi")))
        print("     actual:", {y: round(actual(panel, y, "is.revenue") or 0, 1)
                               for y in range(o + 1, min(o + 6, 2026))})
