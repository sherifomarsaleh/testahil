"""ABUK — the macro/company decomposition on the four lines that decide the scope.

Asked for after the drafts were harvested: DRAFT-ABUK-11 and -12 ran the test on
non-operating income and overheads, which are the two SMALLEST lines. This runs
the identical test on revenue, cost of sales, gross profit and the volume proxy,
per era as well as pooled, and adds the exact additive decomposition of the
revenue error that the model's own construction makes available.

REVENUE ERROR DECOMPOSES EXACTLY, WITH NO RESIDUAL. The model sets
    revenue = volume proxy x urea price x EGP per USD
and the volume proxy is DERIVED as revenue / (urea x FX), so

    ln(rev_proj/rev_act) = ln(vol_proj/vol_act) + ln(urea_o/urea_act) + ln(fx_o/fx_act)

is an identity, not a regression. The three terms are the volume leg, the
commodity-price leg and the currency leg, and they sum to the revenue error to
machine precision. That is what tells volume-versus-price apart here.
"""
import json, math, os
import bottom_up as bu

HERE = os.path.dirname(os.path.abspath(__file__))
ERA = {"FY2020": "E1", "FY2021": "E1", "FY2022": "E2", "FY2023": "E2",
       "FY2024": "E2", "FY2025": "E2"}


def mae(xs):
    return sum(abs(x) for x in xs) / len(xs) if xs else None


def bias(xs):
    return sum(xs) / len(xs) if xs else None


def main():
    panel, macro = bu.load()
    proj = json.load(open(os.path.join(HERE, "projections.json")))
    Y = panel["years"]

    rows = {}
    for d in ("vol_proxy", "rev", "cogs", "gp"):
        rows[d] = {"pooled": {}, "E1": {}, "E2": {}}
        for era in ("pooled", "E1", "E2"):
            e_known, e_macro, e_fore = [], [], []
            for o in bu.ORIGINS:
                for t, r in proj["model"][o].items():
                    if era != "pooled" and ERA[t] != era:
                        continue
                    a = Y[t][d]
                    if not a or a <= 0:
                        continue
                    e_known.append(math.log(r[d] / a))
                    e_macro.append(math.log(proj["macro_perfect"][o][t][d] / a))
                    e_fore.append(math.log(proj["foresight"][o][t][d] / a))
            mk, mm, mf = mae(e_known), mae(e_macro), mae(e_fore)
            rows[d][era] = dict(n=len(e_known), bias=bias(e_known),
                                mae_as_known=mk, mae_macro_perfect=mm,
                                mae_full_foresight=mf,
                                macro_share=None if not mk else (mk - mm) / mk,
                                company_share=None if not mk else (mm - mf) / mk)

    # the exact additive decomposition of the revenue error
    legs = {"pooled": {"vol": [], "urea": [], "fx": [], "total": [], "check": []},
            "E1": {"vol": [], "urea": [], "fx": [], "total": [], "check": []},
            "E2": {"vol": [], "urea": [], "fx": [], "total": [], "check": []}}
    percell = []
    for o in bu.ORIGINS:
        base = Y[o]
        for t, r in sorted(proj["model"][o].items()):
            a = Y[t]
            lv = math.log(r["vol_proxy"] / a["vol_proxy"])
            lu = math.log(base["urea_usd_t"] / a["urea_usd_t"])
            lf = math.log(base["egp_usd"] / a["egp_usd"])
            lt = math.log(r["rev"] / a["rev"])
            for era in ("pooled", ERA[t]):
                legs[era]["vol"].append(lv)
                legs[era]["urea"].append(lu)
                legs[era]["fx"].append(lf)
                legs[era]["total"].append(lt)
                legs[era]["check"].append(lt - (lv + lu + lf))
            percell.append(dict(origin=o, target=t, h=r["h"], vol=lv, urea=lu,
                                fx=lf, total=lt, residual=lt - (lv + lu + lf)))

    dec = {}
    for era, L in legs.items():
        dec[era] = dict(n=len(L["total"]),
                        mean_volume_leg=bias(L["vol"]),
                        mean_commodity_price_leg=bias(L["urea"]),
                        mean_currency_leg=bias(L["fx"]),
                        mean_total=bias(L["total"]),
                        max_abs_identity_residual=max(abs(x) for x in L["check"]))

    doc = {"_what_this_is": (
        "The macro/company decomposition run on the four lines the valuation "
        "turns on, pooled and by era, plus the exact additive decomposition of "
        "the revenue error into its volume, commodity-price and currency legs."),
        "_eras": {"E1": "FY2020-FY2021, pre-spike",
                  "E2": "FY2022-FY2025, spike and after"},
        "macro_company_split": rows,
        "revenue_error_decomposition": dec,
        "revenue_error_cells": percell}
    json.dump(doc, open(os.path.join(HERE, "macro_decomposition.json"), "w"),
              indent=1, sort_keys=True, default=float)
    return doc


if __name__ == "__main__":
    d = main()
    print("MACRO / COMPANY SPLIT — the four lines that decide the scope")
    print("%-12s %-7s %4s %8s %10s %12s %10s %10s" % (
        "driver", "era", "n", "bias", "MAE known", "MAE macro-ok", "macro%", "company%"))
    for drv in ("rev", "cogs", "gp", "vol_proxy"):
        for era in ("pooled", "E1", "E2"):
            r = d["macro_company_split"][drv][era]
            print("%-12s %-7s %4d %+8.3f %10.3f %12.3f %9.0f%% %9.0f%%" % (
                drv, era, r["n"], r["bias"], r["mae_as_known"],
                r["mae_macro_perfect"], 100 * r["macro_share"],
                100 * r["company_share"]))
    print()
    print("REVENUE ERROR, DECOMPOSED EXACTLY (mean log error; the three legs SUM to the total)")
    print("%-8s %4s %12s %14s %12s %10s %14s" % (
        "era", "n", "volume leg", "commodity leg", "currency leg", "total",
        "max residual"))
    for era in ("pooled", "E1", "E2"):
        r = d["revenue_error_decomposition"][era]
        print("%-8s %4d %+12.3f %+14.3f %+12.3f %+10.3f %14.2e" % (
            era, r["n"], r["mean_volume_leg"], r["mean_commodity_price_leg"],
            r["mean_currency_leg"], r["mean_total"],
            r["max_abs_identity_residual"]))


# ---------------------------------------------------------------------------
# Which macro variable carries it — the currency or the commodity.
#
# The revenue decomposition above separates them exactly because revenue is a
# product of the three legs. Gross profit and net profit are not, so they need
# their own re-runs: one with the ACTUAL currency and a flat commodity price,
# one with the ACTUAL commodity price and a flat currency.
# ---------------------------------------------------------------------------
def project_partial(panel, macro, o, use_fx=False, use_urea=False):
    Y = panel["years"]
    base = Y[o]
    full = bu.project(panel, macro, o)
    flatm = bu.project(panel, macro, o)
    out = {}
    for t, r in full.items():
        a = Y[t]
        urea = a["urea_usd_t"] if use_urea else base["urea_usd_t"]
        fx = a["egp_usd"] if use_fx else base["egp_usd"]
        rev = r["vol_proxy"] * urea * fx
        scale = rev / r["rev"]
        row = dict(r)
        row["rev"] = rev
        row["cogs"] = r["cogs"] * scale
        row["gp"] = rev - row["cogs"]
        row["sell"] = r["sell"] * scale
        row["pbt"] = row["gp"] - row["sell"] - r["admin"] + (r["nonop"] or 0.0)
        etr = r["tax"] / r["pbt"] if r["pbt"] else 0.0
        row["tax"] = etr * row["pbt"]
        row["np"] = row["pbt"] - row["tax"]
        out[t] = row
    return out


def which_variable():
    panel, macro = bu.load()
    Y = panel["years"]
    res = {}
    for label, kw in (("as known (both flat)", {}),
                      ("actual currency only", dict(use_fx=True)),
                      ("actual commodity price only", dict(use_urea=True)),
                      ("both actual", dict(use_fx=True, use_urea=True))):
        acc = {d: [] for d in ("rev", "cogs", "gp", "np")}
        for o in bu.ORIGINS:
            p = project_partial(panel, macro, o, **kw)
            for t, r in p.items():
                for d in acc:
                    a = Y[t][d]
                    if a and a > 0 and r[d] > 0:
                        acc[d].append(math.log(r[d] / a))
        res[label] = {d: dict(n=len(v), bias=bias(v), mae=mae(v))
                      for d, v in acc.items()}
    return res


def leg_correlation():
    doc = json.load(open(os.path.join(HERE, "macro_decomposition.json")))
    cells = doc["revenue_error_cells"]
    xs = [c["vol"] for c in cells]
    ys = [c["urea"] for c in cells]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    r = sxy / (sxx * syy) ** 0.5 if sxx and syy else None
    slope = sxy / sxx if sxx else None
    return dict(n=n, pearson_r=r, slope_urea_on_volume=slope,
                mean_sum_of_the_two_legs=sum(x + y for x, y in zip(xs, ys)) / n)


if __name__ != "__main__":
    pass
