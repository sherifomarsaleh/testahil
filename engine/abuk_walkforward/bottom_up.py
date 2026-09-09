"""ABUK fundamental walk-forward — the ground-up build at every origin.

Exactly the rules pre-registered on 09-09-2026, and nothing else.  No parameter
here was chosen after seeing an error.

POINT-IN-TIME IS ABSOLUTE.  Each origin sees the panel only up to and including
its own fiscal year, and the exogenous series only up to the same year.  There
is no forward look anywhere, including in the trailing means.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGINS = ["FY2019", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]
LAST = 2025
HMAX = 5


def _y(t):
    return int(t[2:])


def load():
    p = json.load(open(os.path.join(HERE, "panel.json")))
    m = json.load(open(os.path.join(HERE, "macro.json")))
    return p, m


def trailing_mean(panel, o, key, n=3):
    ys = ["FY%d" % y for y in range(_y(o) - n + 1, _y(o) + 1)]
    return sum(panel["years"][y][key] for y in ys) / len(ys)


def trailing_cagr(panel, o, key, n=3):
    a = panel["years"]["FY%d" % (_y(o) - n)][key]
    b = panel["years"][o][key]
    if a <= 0 or b <= 0:
        return 0.0
    return (b / a) ** (1.0 / n) - 1.0


def pop_cagr(macro, o, n=5):
    a = macro["population_cy"].get(str(_y(o) - n))
    b = macro["population_cy"].get(str(_y(o)))
    if not a or not b:
        return 0.0
    return (b / a) ** (1.0 / n) - 1.0


def investable(panel, o):
    bs = panel["balance_sheet"].get(o) or {}
    c, i = bs.get("cash"), bs.get("invest")
    if c is None and i is None:
        return None
    return (c or 0) + (i or 0)


def project(panel, macro, o, macro_actual=False, foresight=False,
            corr=None):
    """The pre-registered model at one origin, out to five horizons.

    macro_actual  substitute the ACTUAL urea / FX / CPI path (macro share)
    foresight     also substitute the ACTUAL company ratios (company share)
    corr          {driver: multiplicative factor} applied to the projection
    """
    corr = corr or {}
    Y = panel["years"]
    base = Y[o]
    g = pop_cagr(macro, o)
    vcap = max(Y["FY%d" % y]["vol_proxy"] for y in range(_y(o) - 4, _y(o) + 1))
    d4 = trailing_mean(panel, o, "cogs_ratio")
    d5 = trailing_mean(panel, o, "sell_ratio")
    d8 = trailing_mean(panel, o, "etr")
    pi = trailing_mean(panel, o, "cpi_pct") / 100.0
    B = investable(panel, o)
    nonop_hist = [Y["FY%d" % y]["nonop"] for y in range(_y(o) - 2, _y(o) + 1)]
    Bs = [investable(panel, "FY%d" % y) for y in range(_y(o) - 2, _y(o) + 1)]
    ys = [n / b for n, b in zip(nonop_hist, Bs) if b]
    yld = sum(ys) / len(ys) if ys else None

    out = {}
    for h in range(1, HMAX + 1):
        ty = _y(o) + h
        if ty > LAST:
            break
        t = "FY%d" % ty
        act = Y[t]
        v = min(base["vol_proxy"] * (1 + g) ** h, vcap)
        urea = act["urea_usd_t"] if macro_actual else base["urea_usd_t"]
        fx = act["egp_usd"] if macro_actual else base["egp_usd"]
        pi_h = None
        if macro_actual:
            # the knowable inflation path becomes the actual one
            pi_h = [Y["FY%d" % k]["cpi_pct"] / 100.0
                    for k in range(_y(o) + 1, ty + 1)]
        cogs_r, sell_r, etr = d4, d5, d8
        if foresight:
            v = act["vol_proxy"]
            cogs_r, sell_r, etr = act["cogs_ratio"], act["sell_ratio"], act["etr"]
        v *= corr.get("vol", 1.0)
        rev = v * urea * fx * corr.get("rev", 1.0)
        cogs = cogs_r * rev * corr.get("cogs", 1.0)
        gp = rev - cogs
        sell = sell_r * rev * corr.get("sell", 1.0)
        if pi_h is None:
            adm = base["admin"] * (1 + pi) ** h
            nop = (yld * B * (1 + pi) ** h) if (yld is not None and B) else None
        else:
            f = 1.0
            for x in pi_h:
                f *= (1 + x)
            adm = base["admin"] * f
            nop = (yld * B * f) if (yld is not None and B) else None
        adm *= corr.get("admin", 1.0)
        if foresight:
            nop = act["nonop"]
        if nop is not None:
            nop *= corr.get("nonop", 1.0)
        pbt = gp - sell - adm + (nop or 0.0)
        tax = etr * pbt
        np_ = pbt - tax
        out[t] = dict(h=h, rev=rev, cogs=cogs, gp=gp, sell=sell, admin=adm,
                      nonop=nop, pbt=pbt, tax=tax, np=np_, vol_proxy=v,
                      urea_usd_t=urea, egp_usd=fx)
    return out


def freeze(panel, o):
    Y = panel["years"]
    base = Y[o]
    out = {}
    for h in range(1, HMAX + 1):
        ty = _y(o) + h
        if ty > LAST:
            break
        out["FY%d" % ty] = {k: base[k] for k in
                            ("rev", "cogs", "gp", "sell", "admin", "nonop",
                             "pbt", "tax", "np", "vol_proxy")}
        out["FY%d" % ty]["h"] = h
    return out


def trend(panel, o):
    Y = panel["years"]
    base = Y[o]
    keys = ("rev", "cogs", "gp", "sell", "admin", "nonop", "pbt", "tax", "np",
            "vol_proxy")
    gs = {k: trailing_cagr(panel, o, k) for k in keys}
    out = {}
    for h in range(1, HMAX + 1):
        ty = _y(o) + h
        if ty > LAST:
            break
        out["FY%d" % ty] = {k: base[k] * (1 + gs[k]) ** h for k in keys}
        out["FY%d" % ty]["h"] = h
    return out


def build_all():
    panel, macro = load()
    res = {"model": {}, "freeze": {}, "trend": {}, "macro_perfect": {},
           "foresight": {}, "params": {}}
    for o in ORIGINS:
        res["model"][o] = project(panel, macro, o)
        res["macro_perfect"][o] = project(panel, macro, o, macro_actual=True)
        res["foresight"][o] = project(panel, macro, o, macro_actual=True,
                                      foresight=True)
        res["freeze"][o] = freeze(panel, o)
        res["trend"][o] = trend(panel, o)
        res["params"][o] = dict(
            pop_cagr=pop_cagr(macro, o),
            cogs_ratio=trailing_mean(panel, o, "cogs_ratio"),
            sell_ratio=trailing_mean(panel, o, "sell_ratio"),
            etr=trailing_mean(panel, o, "etr"),
            cpi=trailing_mean(panel, o, "cpi_pct") / 100.0,
            investable=investable(panel, o),
            urea_usd_t=panel["years"][o]["urea_usd_t"],
            egp_usd=panel["years"][o]["egp_usd"],
            vol_cap=max(panel["years"]["FY%d" % y]["vol_proxy"]
                        for y in range(_y(o) - 4, _y(o) + 1)))
    json.dump(res, open(os.path.join(HERE, "projections.json"), "w"), indent=1,
              sort_keys=True, default=float)
    return res


if __name__ == "__main__":
    r = build_all()
    for o in ORIGINS:
        p = r["params"][o]
        print("%s  popCAGR %.3f%%  cogs%% %.1f  sell%% %.2f  etr%% %.1f  cpi %.1f%%  "
              "investable %s" % (
                  o, 100 * p["pop_cagr"], 100 * p["cogs_ratio"],
                  100 * p["sell_ratio"], 100 * p["etr"], 100 * p["cpi"],
                  "n/a" if p["investable"] is None else "%.2fbn" % (p["investable"] / 1e9)))
