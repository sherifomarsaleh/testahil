#!/usr/bin/env python3
"""GBCO fundamental walk-forward training — bottom-up model at every origin.

Implements PREREGISTRATION.md exactly: mechanical drivers only, point-in-time
visibility (origin Y sees FY <= Y-1 as originally reported, macro through Y-1),
origins 2016..2025, horizons h1..h5 truncated at FY2025, naive freeze/trend
benchmarks, block-bootstrap CIs, era sign tables, macro-vs-company split via a
realized-macro re-run, and the per-origin side-by-side income statements.

Run AFTER gbco_panel.py:
  python3 engine/gbco_training/bottom_up.py            # score raw model
  python3 engine/gbco_training/bottom_up.py --corrections  # + expanding-window corrections test

Outputs (committed training records):
  errors_by_line.csv, errors_by_driver.csv, skill_table.csv,
  GBCO_IS_projected_vs_actual_all_origins.md, corrections_test.json
"""
import argparse
import csv
import json
import math
import os
import random
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "gbco_panel.json")

ORIGINS = list(range(2016, 2026))
LAST_ACTUAL = 2025
ERAS = {"E1": range(2016, 2020), "E2": range(2020, 2022),
        "E3": range(2022, 2025), "E4": range(2025, 2026)}

# stated parameters (pre-registered; sensitivities reported, never selected)
PASS_PRICE = 0.5      # FX pass-through on ASP
PASS_COST = 0.75      # FX pass-through on unit cost
PHI_SGA = 0.5         # fixed share of SG&A
LAMBDA = 0.5          # correction half-strength
SENS = {"PASS_PRICE": (0.25, 0.75), "PASS_COST": (0.5, 1.0), "PHI_SGA": (0.3, 0.7)}


def g(d, y, default=None):
    v = d.get(y, default)
    return v


def build_series(pj):
    """Analysis-ready annual series (EGP mn) from the provenance panel.

    Every mapping states where the number lives in the panel; group statement
    lines are the audited consolidated FS (EGP 000 → mn); segment lines are the
    company's own LoB tables (already EGP mn). Basis breaks per BASIS_BREAKS.md
    are handled by scoring windows, never by chaining values across a break.
    """
    P = pj["panel"]
    S = {k: {} for k in
         ("rev gp sga oth_inc op fin assoc pbt tax np npp inv rec pay debt cash ppe eq ta "
          "da capex cfo pc_rev m3w_rev cv_rev fin_rev resid_rev pc_u m3w_u cv_u").split()}

    def is_(fy):  # noqa: E743
        return P[f"FY{fy}"]["is"], P[f"FY{fy}"]["bs"], P[f"FY{fy}"]["cf"]

    for fy in pj["fiscal_years"]:
        i, b, c = is_(fy)
        k = 1e-3  # EGP 000 → mn
        S["rev"][fy] = i["revenue"] * k
        S["gp"][fy] = i["gross_profit"] * k
        sga = None
        if "sm_exp" in i and "ga_exp" in i:
            sga = -(i["sm_exp"] + i["ga_exp"])
        elif "distribution_exp" in i and "admin_exp" in i:
            sga = abs(i["distribution_exp"]) + abs(i["admin_exp"])
        elif "sga" in i:
            sga = abs(i["sga"])
        if sga is not None:
            S["sga"][fy] = sga * k
        if "other_income" in i and i["other_income"] is not None:
            S["oth_inc"][fy] = i["other_income"] * k
        if "op_profit" in i and i["op_profit"] is not None:
            S["op"][fy] = i["op_profit"] * k
        fin = i.get("finance_cost_net")
        if fin is None:
            fc = i.get("finance_cost") or 0
            fi = i.get("finance_income") or 0
            fin = fc + fi if (fc or fi) else None
        if fin is not None:
            S["fin"][fy] = -abs(fin) * k  # store as negative (net cost) consistently
        assoc = i.get("associates", i.get("associates_income"))
        S["assoc"][fy] = (assoc or 0) * k
        S["pbt"][fy] = i["pbt"] * k
        S["tax"][fy] = -abs(i.get("tax", i.get("income_tax", 0)) or 0) * k
        S["np"][fy] = i["np_total"] * k
        S["npp"][fy] = i.get("np_parent", i["np_total"]) * k

        S["inv"][fy] = (b.get("inventories", b.get("inventory")) or 0) * k
        S["rec"][fy] = (b.get("an_receivables", b.get("trade_notes_receivable")) or 0) * k
        S["pay"][fy] = (b.get("trade_pay", b.get("trade_notes_payable")) or 0) * k
        debt = 0
        for kk in ("loans_c", "loans_nc", "bonds_c", "bonds_nc",
                   "borrowings_current", "borrowings_noncurrent"):
            debt += b.get(kk) or 0
        if debt:
            S["debt"][fy] = debt * k
        if b.get("cash"):
            S["cash"][fy] = b["cash"] * k
        ppe = b.get("ppe", b.get("ppe_net"))
        if ppe:
            S["ppe"][fy] = ppe * k
        eq = b.get("total_equity")
        if eq:
            S["eq"][fy] = eq * k
        ta = b.get("ta", b.get("total_assets"))
        if ta:
            S["ta"][fy] = ta * k
        da = c.get("da", c.get("dep_amort_addback"))
        if da:
            S["da"][fy] = da * k
        capex = c.get("capex_ppe")
        if capex:
            S["capex"][fy] = abs(capex) * k
        cfo = c.get("cfo_net", c.get("cfo"))
        if cfo is not None:
            S["cfo"][fy] = cfo * k

    # --- segment series (EGP mn), from the extraction records in the panel ---
    # Basis windows (BASIS_BREAKS.md): PC and the residual line exist in TWO
    # definitions — Egypt cut ("_eg", through FY2023) and the FY2024 combined
    # Egypt+Iraq+Jordan cut ("_all", FY2023 onward via the ER 4Q24 comparative).
    # Financing exists incl-microfinance ("fin incl-MNT", through FY2022) and
    # ex-MNT ("fin ex-MNT", FY2022 restated onward). No growth rate and no
    # scored cell ever crosses a basis boundary.
    seg_map = {  # fy -> (pc_rev_eg, m3w_rev, cv_rev, fin_rev_incl, pc_u_eg, m3w_u, cv_u)
        2011: (5741.9, 967.3, 330.5, 156.4, None, 73827, None),
        2012: (6072.3, 1156.2, 465.5, 249.0, None, 102175, 1533),
        2013: (6536.9, 1168.4, 481.0, 476.3, None, 94036, 1585),
        2014: (8909.9, 1270.7, 912.9, 722.7, None, 97869, 3347),
        2015: (7489.9, 1892.5, 1327.9, 1046.2, None, 136873, 2587),
        2016: (8016.1, 1708.2, 1113.3, 1739.6, None, 94985, None),
        # 2017+: "Egypt PC" division cut + GB Capital before eliminations
        2017: (6840.5, 2206.2, 1092.2, 3381.1, 31029, 84427, 1699),
        2018: (10407.8, 3470.2, 1507.1, 5118.1, 37055, 128160, 2238),
        2019: (7597.8, 2100.2, 1394.6, 5347.9, 26887, 84999, 2096),
        2020: (7699.0, 2944.7, 770.1, 6399.8, 29650, 112366, 1152),
        2021: (12880.4, 3719.9, 1053.4, 7949.8, 45584, 137252, 1576),
        2022: (9231.1, 1915.0, 1515.0, 9358.7, 31541, 59100, 2005),
        2023: (9545.2, 513.4, 1424.1, None, 16469, 13610, 943),
        2024: (None, 1378.2, 3984.5, None, None, 20189, 2101),
        2025: (None, 2203.8, 5956.8, None, None, 33906, 3404),
    }
    for fy, (pc, m3, cv, fr, pu, mu, cu) in seg_map.items():
        if pc is not None:
            S["pc_rev"][fy] = pc
        if m3 is not None:
            S["m3w_rev"][fy] = m3
        if cv is not None:
            S["cv_rev"][fy] = cv
        if fr is not None:
            S["fin_rev"][fy] = fr
        if pu is not None:
            S["pc_u"][fy] = pu
        if mu is not None:
            S["m3w_u"][fy] = mu
        if cu is not None:
            S["cv_u"][fy] = cu
    # combined-basis PC (ER 4Q24 comparative + ER 4Q25) — FY2023 overlap year
    S["pc_rev_all"] = {2023: 16544.3, 2024: 36533.4, 2025: 52827.3}
    S["pc_u_all"] = {2023: 26994, 2024: 42043, 2025: 56548}
    # ex-MNT financing (ER 4Q23 Table 14 restated FY22; ERs 4Q24/4Q25)
    S["fin_rev_ex"] = {2022: 4274.3, 2023: 4950.9, 2024: 7383.6, 2025: 14743.0}
    # composition eras (see BASIS_BREAKS.md B3/B4/B5): C1 financing = LoB line,
    # C2 = GB Capital before eliminations (incl. microfinance), C3 = ex-MNT.
    # The 2016->2017 fin jump (1,739.6 -> 3,381.1) is a disclosure re-cut (B3),
    # never treated as growth.
    # residual line per basis: rev − (pc + m3w + cv + fin) on matching bases
    S["resid_rev_all"] = {}
    for fy in pj["fiscal_years"]:
        parts = [S[x].get(fy) for x in ("pc_rev", "m3w_rev", "cv_rev", "fin_rev")]
        if all(p is not None for p in parts):
            S["resid_rev"][fy] = S["rev"][fy] - sum(parts)
        parts_all = [S["pc_rev_all"].get(fy), S["m3w_rev"].get(fy),
                     S["cv_rev"].get(fy), S["fin_rev_ex"].get(fy)]
        if all(p is not None for p in parts_all):
            S["resid_rev_all"][fy] = S["rev"][fy] - sum(parts_all)
    return S


# series provenance/derivation flags surfaced in the training record
SEG_NOTES = {
    "pc_u_2017": "DERIVED: sum of GB brand market volumes AR2017 p.24 (Hyundai 21,897 + Chery 5,477 + Geely 2,804 + Mazda 851); ties to 31.1% share x 99,530 market",
    "pc_u_2018": "DERIVED: 25.4% share x 145,886 AMIC market (AR2018)",
    "m3w_u_2012": "68,527 3W + 33,648 MC (AR2012 charts)",
    "m3w_u_2013": "60,801 3W + 33,235 MC",
    "m3w_u_2014": "61,068 3W + 36,801 MC (AR2017 charts)",
    "m3w_u_2015": "85,183 3W + 50,840 MC",
    "m3w_u_2016": "65,988 3W + 28,997 MC",
    "m3w_u_2017": "84,427 as printed in AR2018 (sub-volumes print 79,169 — flagged in extraction)",
    "pc_basis": "PC revenue: LoB series (AR2017 retrospective chart + LoB tables) through 2023 (Egypt cut from 2017); combined Egypt+Iraq+Jordan from 2024 (B5) — growth never computed across the 2023/2024 cut",
    "fin_basis": "financing: MD&A line 2011-2014; GB Capital before eliminations 2017-2022 (incl. microfinance to 2021, part-year 2022); ex-MNT from 2023 (B4) — scored inside windows only",
}


def exog_paths(pj, Y):
    """Exogenous paths as visible at origin Y (through Y-1), per pre-registration."""
    cpi = {int(k): v for k, v in pj["exog"]["cpi_egypt_pct"]["values"].items()}
    fx = {int(k): v for k, v in pj["exog"]["egp_usd_avg"]["values"].items()}
    mkt = {int(k): v for k, v in pj["exog"]["egypt_pc_market_units"]["values"].items()}
    t3 = [cpi[y] for y in (Y - 3, Y - 2, Y - 1)]
    pi = sum(t3) / 300.0  # decimal
    dep3 = [(fx[y] / fx[y - 1] - 1) for y in (Y - 3, Y - 2, Y - 1)]
    d = max(0.0, sum(dep3) / 3)
    mg = (mkt[Y - 1] / mkt[Y - 4]) ** (1 / 3) - 1 if (Y - 4) in mkt else None
    return pi, d, mkt, mg, cpi, fx


def t3cagr(series, Y):
    a, b = series.get(Y - 4), series.get(Y - 1)
    if a and b and a > 0 and b > 0:
        return (b / a) ** (1 / 3) - 1
    # shorter window fallback (flagged by caller through None checks upstream)
    a2 = series.get(Y - 3)
    if a2 and b and a2 > 0 and b > 0:
        return (b / a2) ** (1 / 2) - 1
    return None


def t3mean(fn, years):
    vals = [fn(y) for y in years]
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def forecast_origin(S, pj, Y, hmax=5, realized_macro=False, corr=None):
    """Mechanical bottom-up forecast at origin Y for FY Y..Y+hmax-1.

    Returns dict line -> {fy: value}. corr = {driver: multiplier} applied to
    growth factors (corrections stage); realized_macro swaps forecast pi/d/mkt
    growth for realized values (macro-vs-company split).
    """
    pi, d, mkt, mg, cpi, fx = exog_paths(pj, Y)
    corr = corr or {}
    h_years = [Y + h for h in range(hmax) if Y + h <= LAST_ACTUAL]

    def pit(series):  # point-in-time view
        return {y: v for y, v in series.items() if y < Y}

    rev, gp, sga = pit(S["rev"]), pit(S["gp"]), pit(S["sga"])
    m3w_rev, cv_rev = pit(S["m3w_rev"]), pit(S["cv_rev"])
    m3w_u, cv_u = pit(S["m3w_u"]), pit(S["cv_u"])
    # composition era of this origin (by last visible actual year)
    era_c = "C1" if Y - 1 <= 2016 else ("C2" if Y - 1 <= 2022 else "C3")
    span = {"C1": (2011, 2016), "C2": (2017, 2022), "C3": (2022, 2025)}[era_c]

    def win(series):
        return {y: v for y, v in series.items() if span[0] <= y <= span[1] and y < Y}

    if era_c == "C3":
        pc_rev, pc_u = win(S["pc_rev_all"]), win(S["pc_u_all"])
        fin_rev, resid = win(S["fin_rev_ex"]), win(S["resid_rev_all"])
    else:
        pc_rev, pc_u = win(S["pc_rev"]), win(S["pc_u"])
        fin_rev, resid = win(S["fin_rev"]), win(S["resid_rev"])

    # --- volume drivers -----------------------------------------------------
    # PC: share x market where units+market visible and window basis-consistent
    pc_mode = "rev_cagr"
    last = Y - 1
    if last in pc_u and last in mkt and (Y - 4) in mkt and all(
            y in pc_u for y in (Y - 2, Y - 3) if y >= 2017) and last >= 2019:
        pc_mode = "share_x_market"
        share = pc_u[last] / mkt[last]
    m3w_mode = "units_cagr" if t3cagr(m3w_u, Y) is not None else "rev_cagr"
    cv_mode = "units_cagr" if t3cagr(cv_u, Y) is not None else "rev_cagr"

    def esc_price(x):
        return x * (1 + pi + PASS_PRICE * d) * corr.get("asp", 1.0)

    def esc_cost(x):
        return x * (1 + pi + PASS_COST * d) * corr.get("ucost", 1.0)

    gm_last = gp[last] / rev[last]
    F = {k: {} for k in ("rev pc_rev m3w_rev cv_rev fin_rev resid_rev gp sga oth_inc "
                         "op fin assoc pbt tax np inv rec pay debt da capex cfo "
                         "pc_u m3w_u cv_u").split()}

    # per-line growth rates fixed at origin
    g_fin = t3cagr(fin_rev, Y)
    g_resid = t3cagr(resid, Y)
    g_pcrev = t3cagr(pc_rev, Y)
    g_m3wrev = t3cagr(m3w_rev, Y)
    g_cvrev = t3cagr(cv_rev, Y)
    g_m3wu = t3cagr(m3w_u, Y)
    g_cvu = t3cagr(cv_u, Y)
    if realized_macro:
        pass  # macro substitution happens per-year below

    # WC / capex / D&A / finance / tax parameters at origin
    inv, rec, pay = pit(S["inv"]), pit(S["rec"]), pit(S["pay"])
    debt, ppe, da, capex = pit(S["debt"]), pit(S["ppe"]), pit(S["da"]), pit(S["capex"])
    tax_s, pbt_s = pit(S["tax"]), pit(S["pbt"])
    fin_s, assoc_s, oth = pit(S["fin"]), pit(S["assoc"]), pit(S["oth_inc"])
    cogs = {y: rev[y] - gp[y] for y in gp}
    t3y = [y for y in (Y - 3, Y - 2, Y - 1) if y in rev]
    DIO = t3mean(lambda y: 365 * inv[y] / cogs[y] if y in inv and y in cogs and inv[y] else None, t3y)
    DSO = t3mean(lambda y: 365 * rec[y] / rev[y] if y in rec and rec[y] else None, t3y)
    DPO = t3mean(lambda y: 365 * pay[y] / cogs[y] if y in pay and pay[y] else None, t3y)
    KAPPA = (t3mean(lambda y: capex[y] / rev[y] if y in capex else None, t3y) or 0.02) \
        * corr.get("capex", 1.0)
    DELTA = t3mean(lambda y: da[y] / ppe[y - 1] if y in da and (y - 1) in ppe and ppe[y - 1] else None, t3y) or 0.10
    etr_obs = [(-tax_s[y] / pbt_s[y]) for y in t3y if y in tax_s and pbt_s.get(y, 0) > 0]
    ETR = sum(etr_obs) / len(etr_obs) if etr_obs else \
        pj["exog"]["tax_statutory_pct"]["values"][str(Y)] / 100 \
        if str(Y) in pj["exog"]["tax_statutory_pct"]["values"] else 0.225
    i_eff = None
    if (Y - 1) in fin_s and (Y - 1) in debt and (Y - 2) in debt:
        i_eff = -fin_s[Y - 1] / ((debt[Y - 1] + debt[Y - 2]) / 2)
    oth_share = (oth.get(last, 0) / rev[last]) if last in oth else 0.0
    assoc_last = assoc_s.get(last, 0.0)
    sga_last = sga[last]

    # starting states
    st_ppe = ppe.get(last)
    st_debt = debt.get(last, 0.0)
    prev = {"rev": rev[last], "pc_rev": pc_rev.get(last), "m3w_rev": m3w_rev.get(last),
            "cv_rev": cv_rev.get(last), "fin_rev": fin_rev.get(last),
            "resid_rev": resid.get(last),
            "pc_u": pc_u.get(last), "m3w_u": m3w_u.get(last), "cv_u": cv_u.get(last),
            "inv": inv.get(last), "rec": rec.get(last), "pay": pay.get(last),
            "sga": sga_last}
    pc_asp = (prev["pc_rev"] / prev["pc_u"]) if prev["pc_u"] and prev["pc_rev"] else None
    m3w_asp = (prev["m3w_rev"] / prev["m3w_u"]) if prev["m3w_u"] and prev["m3w_rev"] else None
    cv_asp = (prev["cv_rev"] / prev["cv_u"]) if prev["cv_u"] and prev["cv_rev"] else None
    mkt_last = mkt.get(last)

    for t, fy in enumerate(h_years, start=1):
        if realized_macro:
            pi_t = cpi.get(fy, pi * 100) / 100
            d_t = max(0.0, fx[fy] / fx[fy - 1] - 1) if fy in fx and (fy - 1) in fx else d
            mg_t = (mkt[fy] / mkt[fy - 1] - 1) if fy in mkt and (fy - 1) in mkt else mg
        else:
            pi_t, d_t, mg_t = pi, d, mg

        def epr(x):
            return x * (1 + pi_t + PASS_PRICE * d_t) * corr.get("asp", 1.0)

        def ecs(x):
            return x * (1 + pi_t + PASS_COST * d_t) * corr.get("ucost", 1.0)

        # volumes
        if pc_mode == "share_x_market" and mkt_last:
            mkt_t = mkt_last * (1 + (mg_t if mg_t is not None else 0)) ** t
            u = share * mkt_t * corr.get("pc_units", 1.0)
            F["pc_u"][fy] = u
            pc_asp_t = pc_asp * (1 + pi_t + PASS_PRICE * d_t) ** t if pc_asp else None
            F["pc_rev"][fy] = u * pc_asp_t if pc_asp_t else None
        else:
            gr = (g_pcrev if g_pcrev is not None else 0) if not realized_macro else \
                (g_pcrev if g_pcrev is not None else 0)
            F["pc_rev"][fy] = prev["pc_rev"] * (1 + gr) * corr.get("pc_rev", 1.0) \
                if prev["pc_rev"] else None
        if m3w_mode == "units_cagr" and prev["m3w_u"]:
            u = prev["m3w_u"] * (1 + (g_m3wu or 0)) * corr.get("m3w_units", 1.0)
            F["m3w_u"][fy] = u
            F["m3w_rev"][fy] = u * (m3w_asp * (1 + pi_t + PASS_PRICE * d_t) ** t) \
                if m3w_asp else None
        else:
            F["m3w_rev"][fy] = prev["m3w_rev"] * (1 + (g_m3wrev or 0)) if prev["m3w_rev"] else None
        if cv_mode == "units_cagr" and prev["cv_u"]:
            u = prev["cv_u"] * (1 + (g_cvu or 0)) * corr.get("cv_units", 1.0)
            F["cv_u"][fy] = u
            F["cv_rev"][fy] = u * (cv_asp * (1 + pi_t + PASS_PRICE * d_t) ** t) \
                if cv_asp else None
        else:
            F["cv_rev"][fy] = prev["cv_rev"] * (1 + (g_cvrev or 0)) if prev["cv_rev"] else None
        F["fin_rev"][fy] = prev["fin_rev"] * (1 + (g_fin or 0)) * corr.get("fin_rev", 1.0) \
            if prev["fin_rev"] else None
        F["resid_rev"][fy] = prev["resid_rev"] * (1 + (g_resid if g_resid is not None else pi_t)) \
            if prev["resid_rev"] is not None else None

        parts = [F[x][fy] for x in ("pc_rev", "m3w_rev", "cv_rev", "fin_rev", "resid_rev")]
        if all(p is not None for p in parts):
            F["rev"][fy] = sum(parts)
        else:  # fall back to total-revenue trailing CAGR (flagged by mode)
            gr = t3cagr({y: v for y, v in S["rev"].items() if y < Y}, Y) or 0
            F["rev"][fy] = prev["rev"] * (1 + gr)

        # gross profit: unit-cost wedge on volume segments, frozen ratio elsewhere
        vol_rev = sum(F[x][fy] or 0 for x in ("pc_rev", "m3w_rev", "cv_rev"))
        nonvol_rev = F["rev"][fy] - vol_rev
        wedge = ((1 + pi_t + PASS_COST * d_t) / (1 + pi_t + PASS_PRICE * d_t)) ** t
        cogs_vol = vol_rev * (1 - gm_last) * wedge
        cogs_nonvol = nonvol_rev * (1 - gm_last)
        F["gp"][fy] = F["rev"][fy] - (cogs_vol + cogs_nonvol)

        # opex & the rest of the IS
        F["sga"][fy] = PHI_SGA * prev["sga"] * (1 + pi_t) \
            + (1 - PHI_SGA) * prev["sga"] * (F["rev"][fy] / prev["rev"]) \
            * corr.get("sga", 1.0)
        F["oth_inc"][fy] = oth_share * F["rev"][fy]
        F["op"][fy] = F["gp"][fy] - F["sga"][fy] + F["oth_inc"][fy]
        F["da"][fy] = (DELTA * st_ppe + KAPPA * F["rev"][fy] * DELTA / 2) if st_ppe else None
        F["capex"][fy] = KAPPA * F["rev"][fy]
        cogs_t = F["rev"][fy] - F["gp"][fy]
        F["inv"][fy] = DIO * cogs_t / 365 if DIO else None
        F["rec"][fy] = DSO * F["rev"][fy] / 365 if DSO else None
        F["pay"][fy] = DPO * cogs_t / 365 if DPO else None
        dwc = 0.0
        if all(F[x][fy] is not None for x in ("inv", "rec", "pay")) and \
           all(prev[x] is not None for x in ("inv", "rec", "pay")):
            dwc = (F["inv"][fy] - prev["inv"]) + (F["rec"][fy] - prev["rec"]) \
                - (F["pay"][fy] - prev["pay"])
        # finance cost with a 3-pass fixed point on the debt schedule
        np_t = 0.0
        debt_t = st_debt
        for _ in range(3):
            fin_t = -(i_eff or 0.12) * (st_debt + debt_t) / 2
            pbt_t = F["op"][fy] + fin_t + assoc_last
            np_t = pbt_t * (1 - ETR) if pbt_t > 0 else pbt_t
            fcf = np_t + (F["da"][fy] or 0) - dwc - F["capex"][fy]
            debt_t = max(0.0, st_debt - fcf)
        F["fin"][fy] = fin_t
        F["assoc"][fy] = assoc_last
        F["pbt"][fy] = pbt_t
        F["tax"][fy] = -(pbt_t * ETR) if pbt_t > 0 else 0.0
        F["np"][fy] = np_t
        F["debt"][fy] = debt_t
        F["cfo"][fy] = np_t + (F["da"][fy] or 0) - dwc

        # roll state
        if st_ppe is not None and F["da"][fy] is not None:
            st_ppe = st_ppe + F["capex"][fy] - F["da"][fy]
        st_debt = debt_t
        for x in ("rev", "pc_rev", "m3w_rev", "cv_rev", "fin_rev", "resid_rev",
                  "inv", "rec", "pay", "sga", "pc_u", "m3w_u", "cv_u"):
            if F[x].get(fy) is not None:
                prev[x] = F[x][fy]
        if pc_mode == "share_x_market" and F["pc_u"].get(fy):
            pass  # share & market path already compound via t

    modes = {"pc": pc_mode, "m3w": m3w_mode, "cv": cv_mode, "era_c": era_c}
    params = {"pi": pi, "d": d, "mg": mg, "DIO": DIO, "DSO": DSO, "DPO": DPO,
              "KAPPA": KAPPA, "DELTA": DELTA, "ETR": ETR, "i_eff": i_eff,
              "gm_last": gm_last}
    return F, modes, params


def naive_forecasts(S, Y, hmax=5):
    h_years = [Y + h for h in range(hmax) if Y + h <= LAST_ACTUAL]
    lines = ("rev", "gp", "sga", "op", "fin", "pbt", "np", "inv", "rec", "pay",
             "pc_rev", "m3w_rev", "cv_rev", "fin_rev", "pc_u", "m3w_u", "cv_u")
    freeze, trend = {k: {} for k in lines}, {k: {} for k in lines}
    for k in lines:
        hist = {y: v for y, v in S[k].items() if y < Y}
        last = hist.get(Y - 1)
        gr = t3cagr(hist, Y)
        neg_in_window = any(hist.get(y, 1) is not None and hist.get(y, 1) <= 0
                            for y in (Y - 4, Y - 3, Y - 2, Y - 1) if y in hist)
        for t, fy in enumerate(h_years, start=1):
            if last is None:
                continue
            freeze[k][fy] = last
            trend[k][fy] = last if (gr is None or neg_in_window) else last * (1 + gr) ** t
    return freeze, trend


def log_err(f, a):
    if f is None or a is None:
        return None
    if f > 0 and a > 0:
        return math.log(f / a)
    return None  # non-positive cases scored separately (flagged)


def score_all(S, pj, corr_by_origin=None, realized=False):
    rows = []
    per_origin = {}
    for Y in ORIGINS:
        corr = (corr_by_origin or {}).get(Y)
        F, modes, params = forecast_origin(S, pj, Y, realized_macro=realized, corr=corr)
        FR, TR = naive_forecasts(S, Y)
        per_origin[Y] = (F, modes, params)
        era_c = modes["era_c"]
        span = {"C1": (2011, 2016), "C2": (2017, 2022), "C3": (2022, 2025)}[era_c]
        comp_actual = {
            "pc_rev": S["pc_rev_all"] if era_c == "C3" else S["pc_rev"],
            "pc_u": S["pc_u_all"] if era_c == "C3" else S["pc_u"],
            "fin_rev": S["fin_rev_ex"] if era_c == "C3" else S["fin_rev"],
            "resid_rev": S["resid_rev_all"] if era_c == "C3" else S["resid_rev"],
        }
        for line in ("rev", "gp", "sga", "op", "fin", "pbt", "np",
                     "pc_rev", "m3w_rev", "cv_rev", "fin_rev", "resid_rev",
                     "pc_u", "m3w_u", "cv_u", "inv", "rec", "pay", "capex", "da", "cfo"):
            for fy, f in F.get(line, {}).items():
                if line in comp_actual:
                    if not (span[0] <= fy <= span[1]):
                        continue  # composition line never scored across its era boundary
                    a = comp_actual[line].get(fy)
                else:
                    a = S[line].get(fy)
                h = fy - Y + 1
                e = log_err(abs(f) if line in ("fin", "sga") else f,
                            abs(a) if line in ("fin", "sga") and a is not None else a)
                ef = log_err(abs(FR.get(line, {}).get(fy)) if line in ("fin", "sga") and FR.get(line, {}).get(fy) is not None else FR.get(line, {}).get(fy),
                             abs(a) if line in ("fin", "sga") and a is not None else a)
                et = log_err(abs(TR.get(line, {}).get(fy)) if line in ("fin", "sga") and TR.get(line, {}).get(fy) is not None else TR.get(line, {}).get(fy),
                             abs(a) if line in ("fin", "sga") and a is not None else a)
                scaled = None
                if e is None and f is not None and a is not None:
                    ref = S[line].get(Y - 1)
                    base = abs(ref) if ref else 1.0
                    scaled = (f - a) / base
                rows.append({"origin": Y, "fy": fy, "h": h, "line": line,
                             "forecast": f, "actual": a, "log_err": e,
                             "scaled_err": scaled, "freeze_err": ef, "trend_err": et,
                             "crosses_B4": int(Y <= 2022 and fy >= 2023)})
    return rows, per_origin


def block_bootstrap_ci(errs_by_origin, n=2000, block=3, seed=42):
    origins = sorted(errs_by_origin)
    vals = [errs_by_origin[o] for o in origins]
    if len(vals) < 2:
        return (None, None)
    rng = random.Random(seed)
    means = []
    for _ in range(n):
        picked = []
        while len(picked) < len(vals):
            i = rng.randrange(len(vals))
            picked += vals[i:i + block]
        means.append(sum(picked[:len(vals)]) / len(vals))
    means.sort()
    return (means[int(0.05 * n)], means[int(0.95 * n)])


def era_of(Y):
    for e, r in ERAS.items():
        if Y in r:
            return e
    return "?"


def summarize(rows):
    """bias/MAE/CI/era-sign tables per line & horizon + skill vs naive."""
    out = []
    lines = sorted({r["line"] for r in rows})
    for line in lines:
        for h in range(1, 6):
            sel = [r for r in rows if r["line"] == line and r["h"] == h and r["log_err"] is not None]
            if len(sel) < 3:
                continue
            errs = [r["log_err"] for r in sel]
            by_o = {r["origin"]: r["log_err"] for r in sel}
            lo, hi = block_bootstrap_ci(by_o)
            fe = [abs(r["freeze_err"]) for r in sel if r["freeze_err"] is not None]
            te = [abs(r["trend_err"]) for r in sel if r["trend_err"] is not None]
            mae = st.mean(abs(e) for e in errs)
            era_sign = {}
            for e in ERAS:
                es = [r["log_err"] for r in sel if era_of(r["origin"]) == e]
                if es:
                    era_sign[e] = "+" if st.mean(es) > 0 else "-"
            out.append({"line": line, "h": h, "n": len(sel),
                        "bias": st.mean(errs), "mae": mae,
                        "ci5": lo, "ci95": hi,
                        "over_share": sum(1 for e in errs if e > 0) / len(errs),
                        "era_signs": "".join(f"{k}{v}" for k, v in sorted(era_sign.items())),
                        "skill_vs_freeze": (1 - mae / st.mean(fe)) if fe and st.mean(fe) > 0 else None,
                        "skill_vs_trend": (1 - mae / st.mean(te)) if te and st.mean(te) > 0 else None})
    return out


def driver_rows(rows):
    """Driver-level view: volumes, financing, residual, cogs (unit-cost proxy),
    sga, capex, working-capital lines — the pre-registered driver classes."""
    drivers = ("pc_u", "m3w_u", "cv_u", "pc_rev", "fin_rev", "resid_rev",
               "sga", "capex", "inv", "rec", "pay")
    return [r for r in rows if r["line"] in drivers]


def resolved_h1_errors(rows, line, before_Y):
    """h1 log errors of `line` from origins whose FY resolved before origin Y."""
    out = {}
    for r in rows:
        if r["line"] == line and r["h"] == 1 and r["log_err"] is not None                 and r["origin"] + 1 <= before_Y:
            out[r["origin"]] = r["log_err"]
    return out


CORR_MAP = {  # driver -> correction key applied in forecast_origin
    "pc_u": "pc_units", "pc_rev": "pc_rev", "m3w_u": "m3w_units",
    "cv_u": "cv_units", "fin_rev": "fin_rev", "sga": "sga", "capex": "capex",
}


def eligible(errs_by_origin):
    """Sign consistent across eras holding >=2 resolved observations."""
    if len(errs_by_origin) < 3:
        return False
    era_means = {}
    for e, rng in ERAS.items():
        vals = [v for o, v in errs_by_origin.items() if o in rng]
        if len(vals) >= 2:
            era_means[e] = sum(vals) / len(vals)
    if len(era_means) < 1:
        return False
    signs = {v > 0 for v in era_means.values()}
    if len(signs) != 1:
        return False
    # structural-break reset: latest resolved error beyond 2 sigma of history
    vals = [v for _, v in sorted(errs_by_origin.items())]
    if len(vals) >= 4:
        hist, latest = vals[:-1], vals[-1]
        sd = st.pstdev(hist)
        if sd > 0 and abs(latest - st.mean(hist)) > 2 * sd:
            return False
    return True


def build_corrections(rows):
    """Expanding-window half-strength corrections per origin (prereg section 4)."""
    corr_by_origin, log = {}, []
    for Y in ORIGINS:
        c = {}
        for line, key in CORR_MAP.items():
            errs = resolved_h1_errors(rows, line, Y)
            if eligible(errs):
                med = st.median(errs.values())
                c[key] = math.exp(-LAMBDA * med)
                log.append({"origin": Y, "driver": line, "n_resolved": len(errs),
                            "median_bias": med, "multiplier": c[key]})
        if c:
            corr_by_origin[Y] = c
    return corr_by_origin, log


def is_sidebyside_md(S, pj, per_origin, path):
    lines_show = [("rev", "Revenue"), ("gp", "Gross profit"), ("sga", "SG&A"),
                  ("oth_inc", "Other income"), ("op", "Operating profit"),
                  ("fin", "Net finance cost"), ("assoc", "Associates"),
                  ("pbt", "Profit before tax"), ("tax", "Income tax"),
                  ("np", "Net profit")]
    out = ["# GBCO — projected vs actual income statement, every origin",
           "",
           "Mechanical bottom-up model per PREREGISTRATION.md; EGP mn; actuals as",
           "originally reported (see BASIS_BREAKS.md). h = horizon year index.", ""]
    for Y in ORIGINS:
        F, modes, params = per_origin[Y]
        hy = sorted(F["rev"].keys())
        out.append(f"## Origin {Y} (sees FY≤{Y-1}; PC mode: {modes['pc']}, "
                   f"composition era {modes['era_c']}; π={params['pi']:.1%}, "
                   f"d={params['d']:.1%}, ETR={params['ETR']:.1%})")
        out.append("")
        hdr = "| line | " + " | ".join(f"FY{fy} F / A" for fy in hy) + " |"
        out.append(hdr)
        out.append("|" + "---|" * (len(hy) + 1))
        for k, lab in lines_show:
            cells = []
            for fy in hy:
                f = F.get(k, {}).get(fy)
                a = S[k].get(fy)
                fmt = lambda v: ("−" if v is None else f"{v:,.0f}")
                cells.append(f"{fmt(f)} / {fmt(a)}")
            out.append(f"| {lab} | " + " | ".join(cells) + " |")
        out.append("")
    with open(path, "w") as f:
        f.write("\n".join(out))


def macro_company_split(rows):
    table = []
    for line in ("rev", "np", "pc_rev", "pc_u"):
        for h in (1, 3, 5):
            sel = [r for r in rows if r["line"] == line and r["h"] == h
                   and r["log_err"] is not None
                   and r.get("log_err_realized_macro") is not None]
            if len(sel) < 3:
                continue
            tot = st.mean(abs(r["log_err"]) for r in sel)
            comp = st.mean(abs(r["log_err_realized_macro"]) for r in sel)
            table.append({"line": line, "h": h, "n": len(sel),
                          "mae_total": tot, "mae_company_only": comp,
                          "macro_share_of_mae": max(0.0, 1 - comp / tot) if tot > 0 else None})
    return table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corrections", action="store_true")
    ap.add_argument("--sensitivities", action="store_true")
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()
    pj = json.load(open(PANEL))
    S = build_series(pj)

    # completeness against the known total (R-ENF-04): every scored group line
    # must exist for every panel year; segment lines per their windows.
    missing = [(k, y) for k in ("rev", "gp", "sga", "pbt", "tax", "np")
               for y in pj["fiscal_years"] if y not in S[k]]
    if missing:
        print("PANEL INCOMPLETE for scoring:", missing)
        raise SystemExit(1)

    rows, per_origin = score_all(S, pj)
    rows_rm, _ = score_all(S, pj, realized=True)
    rm_key = {(r["origin"], r["fy"], r["line"]): r["log_err"] for r in rows_rm}
    for r in rows:
        r["log_err_realized_macro"] = rm_key.get((r["origin"], r["fy"], r["line"]))

    with open(os.path.join(args.out, "errors_by_line.csv"), "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)
    summ = summarize(rows)
    with open(os.path.join(args.out, "skill_table.csv"), "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(summ[0].keys()))
        wtr.writeheader()
        wtr.writerows(summ)
    print(f"scored {len(rows)} (origin,fy,line) cells; wrote errors_by_line.csv, skill_table.csv")
    for r in summ:
        if r["line"] in ("rev", "np") and r["h"] in (1, 3, 5):
            print("  ", r["line"], f"h{r['h']}", f"n={r['n']}",
                  f"bias={r['bias']:+.3f}", f"mae={r['mae']:.3f}",
                  f"CI=({r['ci5']:+.3f},{r['ci95']:+.3f})" if r["ci5"] is not None else "CI=NA",
                  f"skill_frz={r['skill_vs_freeze']:+.2f}" if r["skill_vs_freeze"] is not None else "",
                  f"skill_trd={r['skill_vs_trend']:+.2f}" if r["skill_vs_trend"] is not None else "",
                  r["era_signs"])

    with open(os.path.join(args.out, "errors_by_driver.csv"), "w", newline="") as f:
        dr = driver_rows(rows)
        wtr = csv.DictWriter(f, fieldnames=list(dr[0].keys()))
        wtr.writeheader()
        wtr.writerows(dr)

    is_sidebyside_md(S, pj, per_origin,
                     os.path.join(args.out, "GBCO_IS_projected_vs_actual_all_origins.md"))

    split = macro_company_split(rows)
    with open(os.path.join(args.out, "macro_company_split.csv"), "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(split[0].keys()))
        wtr.writeheader()
        wtr.writerows(split)
    print("macro-vs-company split (MAE share attributable to macro paths):")
    for r in split:
        if r["line"] in ("rev", "np"):
            print(f"   {r['line']} h{r['h']}: total {r['mae_total']:.3f} → company-only "
                  f"{r['mae_company_only']:.3f} (macro share {r['macro_share_of_mae']:.0%})")

    if args.corrections:
        corr_by_origin, clog = build_corrections(rows)
        rows_c, _ = score_all(S, pj, corr_by_origin=corr_by_origin)
        # adjusted vs raw on origins that actually carried a correction
        per_origin_cmp = []
        for Y in sorted(corr_by_origin):
            for line in ("rev", "np", "pc_rev", "pc_u", "fin_rev", "sga"):
                raw = [r for r in rows if r["origin"] == Y and r["line"] == line
                       and r["log_err"] is not None]
                adj = [r for r in rows_c if r["origin"] == Y and r["line"] == line
                       and r["log_err"] is not None]
                if raw and adj:
                    per_origin_cmp.append({
                        "origin": Y, "line": line,
                        "mae_raw": st.mean(abs(r["log_err"]) for r in raw),
                        "mae_adj": st.mean(abs(r["log_err"]) for r in adj),
                        "n": len(raw),
                        "drivers_corrected": ",".join(sorted(corr_by_origin[Y]))})
        # non-overlapping confirmation subsets per prereg section 5
        confirm = {}
        for h, subset in ((1, ORIGINS), (3, [2016, 2019, 2022]), (5, [2016, 2021])):
            sel_r = [r for r in rows if r["h"] == h and r["origin"] in subset
                     and r["line"] == "rev" and r["log_err"] is not None]
            sel_c = [r for r in rows_c if r["h"] == h and r["origin"] in subset
                     and r["line"] == "rev" and r["log_err"] is not None]
            if sel_r:
                confirm[f"rev_h{h}"] = {
                    "mae_raw": st.mean(abs(r["log_err"]) for r in sel_r),
                    "mae_adj": st.mean(abs(r["log_err"]) for r in sel_c),
                    "n": len(sel_r)}
        with open(os.path.join(args.out, "corrections_test.json"), "w") as f:
            json.dump({"corrections_log": clog, "per_origin_comparison": per_origin_cmp,
                       "nonoverlap_confirmation": confirm}, f, indent=1)
        print(f"corrections: {len(clog)} driver-origin corrections proposed; "
              f"{len(corr_by_origin)} origins carried at least one")
        for r in per_origin_cmp:
            if r["line"] in ("rev", "np"):
                print(f"   {r['origin']} {r['line']}: raw {r['mae_raw']:.3f} → adj "
                      f"{r['mae_adj']:.3f} [{r['drivers_corrected']}]")

    if args.sensitivities:
        global PASS_PRICE, PASS_COST, PHI_SGA
        base = (PASS_PRICE, PASS_COST, PHI_SGA)
        sens_out = []
        for pname, vals in SENS.items():
            for v in vals:
                PASS_PRICE, PASS_COST, PHI_SGA = base
                if pname == "PASS_PRICE":
                    PASS_PRICE = v
                elif pname == "PASS_COST":
                    PASS_COST = v
                else:
                    PHI_SGA = v
                rws, _ = score_all(S, pj)
                for line in ("rev", "np", "gp", "sga"):
                    sel = [r for r in rws if r["line"] == line and r["h"] == 1
                           and r["log_err"] is not None]
                    if sel:
                        sens_out.append({"param": pname, "value": v, "line": line,
                                         "h": 1, "mae": st.mean(abs(r["log_err"]) for r in sel)})
        PASS_PRICE, PASS_COST, PHI_SGA = base
        with open(os.path.join(args.out, "sensitivities.csv"), "w", newline="") as f:
            wtr = csv.DictWriter(f, fieldnames=["param", "value", "line", "h", "mae"])
            wtr.writeheader()
            wtr.writerows(sens_out)
        print(f"sensitivities written ({len(sens_out)} rows) — reported, never selected")


if __name__ == "__main__":
    main()
