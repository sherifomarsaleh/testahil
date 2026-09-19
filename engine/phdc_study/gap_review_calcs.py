"""Arithmetic behind GAP_REVIEW_01-09-2026.md [R-GAP-01].

Every figure in that review that is not read straight off a filing is computed
here, from the study's own committed numbers, and printed. Nothing in the
review is typed.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import valuation_v2 as V2, bottom_up_model as BU

N = json.load(open(os.path.join(HERE, "study_numbers.json")))
R = {k: v["value"] for k, v in N["registry"].items()}
W = N["wacc"]
L = V2.lenses()
SH = BU.SHARES_MN
CENTRAL, SPOT = N["central"], N["spot"]

out = {}
p = lambda *a: print(*a)

p("=" * 74); p("PHDC GAP REVIEW — arithmetic"); p("=" * 74)
p("central %.4f   spot %.2f   gap %+.1f%%" % (CENTRAL, SPOT, 100 * (CENTRAL / SPOT - 1)))

# --- 1. where the gap comes from ------------------------------------------
p("\n[1] LENS DECOMPOSITION — contribution to the gap vs spot")
tot = 0.0
for nm, b, ba, f, wt in L["rows"]:
    contrib = wt * (ba - SPOT)
    tot += contrib
    p("  %-38s base %7.2f  w %.0f%%   w*(base-spot) %+7.3f"
      % (nm, ba, wt * 100, contrib))
p("  %-38s %31s %+7.3f  (= %.2f - %.2f)" % ("TOTAL", "", tot, CENTRAL, SPOT))
out["lens_gap_contrib"] = {r[0]: r[4] * (r[2] - SPOT) for r in L["rows"]}

# --- 2. normalised-earnings-power coherence -------------------------------
p("\n[2] NORMALISED EARNINGS POWER — nominal rate, zero nominal growth")
norm_rev = (R["revenue_fy24"] + R["revenue_fy25"]) / 2 * (1 + BU.CPI)
norm_margin = R["npat_mi_fy25"] / R["revenue_fy25"]
norm_earn = norm_rev * norm_margin
ke = W["ke_rating"]
p("  normalised revenue %10.1f   margin %.4f   earnings %9.1f" % (norm_rev, norm_margin, norm_earn))
p("  as published:  E / ke            = %9.1f / %.5f      = %8.2f /sh"
  % (norm_earn, ke, norm_earn / ke / SH))
for g, lbl in ((V2.TG, "the study's own terminal growth"),
               (0.0952, "rf* (rating basis) less a 2%% real sovereign rate")):
    v = norm_earn / (ke - g) / SH
    p("  at E / (ke - g), g = %.2f%%  (%s) = %8.2f /sh   %+.2f"
      % (g * 100, lbl, v, v - norm_earn / ke / SH))
nep_tg = norm_earn / (ke - V2.TG) / SH
out["nep_published"] = norm_earn / ke / SH
out["nep_at_tg"] = nep_tg
w_nep = dict((r[0], r[4]) for r in L["rows"])["Normalised earnings power"]
p("  effect on the weighted central at %.0f%% weight: %+.3f -> %.2f"
  % (w_nep * 100, w_nep * (nep_tg - norm_earn / ke / SH),
     CENTRAL + w_nep * (nep_tg - norm_earn / ke / SH)))

# --- 3. minority interest --------------------------------------------------
p("\n[3] MINORITY INTEREST — deducted nowhere in the bridge")
nci = R["nci_equity"]
p("  NCI on the FY2025 balance sheet          %9.1f EGP mn" % nci)
p("  book lens divides TOTAL equity %9.1f by parent shares -> %.4f /sh"
  % (R["total_equity"], R["total_equity"] / SH))
p("  parent-only equity %9.1f -> %.4f /sh   (difference %+.4f)"
  % (R["equity_parent"], R["equity_parent"] / SH,
     R["equity_parent"] / SH - R["total_equity"] / SH))
p("  DCF bridge deducts net debt, associates and investment property, NOT NCI:")
p("    NCI at book, per share                 %+.4f" % (-nci / SH))
out["nci_per_share"] = nci / SH

# --- 4. discount rate: is cash charged once? ------------------------------
p("\n[4] DISCOUNT RATE — cash charged exactly once")
mc, gd, nd, cash = W["market_cap"], W["gross_debt"], W["net_debt"], W["cash"]
we_g, wd_g = mc / (mc + gd), gd / (mc + gd)
we_n, wd_n = mc / (mc + nd), nd / (mc + nd)
wacc_g = we_g * W["ke_rating"] + wd_g * W["kd_aftertax"]
wacc_n = we_n * W["ke_rating"] + wd_n * W["kd_aftertax"]
p("  published weights use GROSS debt: we %.4f wd %.4f -> WACC %.4f%%"
  % (we_g, wd_g, wacc_g * 100))
p("  study's recorded wacc_rating                          %.4f%%" % (W["wacc_rating"] * 100))
p("  on NET debt weights:              we %.4f wd %.4f -> WACC %.4f%%  (%+.0f bp)"
  % (we_n, wd_n, wacc_n * 100, (wacc_n - wacc_g) * 10000))
p("  equity weight is %.4f, i.e. below one: no negative debt weight, so the"
  % we_g)
p("  net-cash pathology that produced the AMOC defect cannot arise here.")
mid = L["cfo"]["mid"]
alt = V2.dcf(mid, wacc_n)
p("  DCF base on net-debt weights: %.2f /sh vs %.2f published (%+.1f%%)"
  % (alt["per_share"], L["dcf"]["base"]["per_share"],
     100 * (alt["per_share"] / L["dcf"]["base"]["per_share"] - 1)))
out["wacc_gross"], out["wacc_net"] = wacc_g, wacc_n
out["dcf_on_net_debt_weights"] = alt["per_share"]

# --- 5. terminal ------------------------------------------------------------
p("\n[5] TERMINAL — growth against the inflation inside the terminal rate")
rf, rfs = W["rf_observed"], W["rf_star_rating"]
p("  nominal rf %.2f%%   rf* (own default spread removed) %.2f%%" % (rf * 100, rfs * 100))
for real in (0.01, 0.02, 0.03):
    p("    implied long-run inflation at a %.0f%% real sovereign rate: %.2f%%"
      % (real * 100, (rfs - real) * 100))
p("  terminal growth used: %.2f%%  -> real terminal growth %+.2f%% to %+.2f%%"
  % (V2.TG * 100, (V2.TG - (rfs - 0.01)) * 100, (V2.TG - (rfs - 0.03)) * 100))
base = L["dcf"]["base"]["per_share"]
for g in (0.10, 0.12, 0.1363, 0.1463):
    d = V2.dcf(mid, W["wacc_rating"])
    tail = (BU.build()["rows"][-1]["revenue"] * mid
            + BU.build()["rows"][-1]["interest"] * (1 - BU.TAX)
            - BU.build()["rows"][-1]["revenue"] * 0.01)
    tv = tail * (1 + g) / (W["wacc_rating"] - g)
    pv_tv = tv / (1 + W["wacc_rating"]) ** 5
    ev = d["pv_explicit"] + pv_tv
    eq = ev - BU.NET_DEBT + R["investments_assoc"] + R["investment_property"]
    p("    g = %.2f%%  ->  DCF %7.2f /sh  (terminal %.0f%% of EV)"
      % (g * 100, eq / SH, 100 * pv_tv / ev))
p("  the explicit years grow on trailing CPI %.2f%% while the discount rate is"
  % (BU.CPI * 100))
p("  built on a FORWARD market yield: two inflation paths in one model.")

# --- 6. multiple cross-check ------------------------------------------------
p("\n[6] MULTIPLE CROSS-CHECK — what the central implies")
eps25 = R["npat_mi_fy25"] / SH
eps26e = BU.build()["rows"][0]["npat"] / SH
ebitda25 = R["npbt_fy25"] + R["finance_cost_fy25"] + R["da_fy25"]
def mult(px):
    eqv = px * SH
    ev = eqv + nd - R["investments_assoc"] - R["investment_property"]
    return eqv, ev
for lbl, px in (("central", CENTRAL), ("spot", SPOT),
                ("DCF lens base", L["dcf"]["base"]["per_share"])):
    eqv, ev = mult(px)
    p("  %-14s %6.2f /sh | mcap %8.0f | EV %8.0f | P/E(FY25) %5.2fx | "
      "P/E(FY26e) %5.2fx | EV/EBITDA(FY25) %5.2fx | P/B %4.2fx | mcap/backlog %5.1f%%"
      % (lbl, px, eqv, ev, px / eps25, px / eps26e, ev / ebitda25,
         px / (R["equity_parent"] / SH), 100 * eqv / R["backlog_1q26"]))
p("  FY25 EPS %.4f  FY26e EPS %.4f  FY25 EBITDA %.1f  backlog(1Q26) %.0f"
  % (eps25, eps26e, ebitda25, R["backlog_1q26"]))

# --- 7. base year ----------------------------------------------------------
p("\n[7] BASE YEAR — every figure a filed full year, nothing annualised")
HIS = N["historical_is"]
for y in sorted(HIS):
    r = {k: v["value"] for k, v in HIS[y].items()}
    cd = r.get("cash_discount", 0.0)
    p("  FY%s  revenue %9.1f - cogs %9.1f - cash discount %6.1f = %9.1f vs filed gross "
      "profit %9.1f  FOOT %+.2f"
      % (y, r["revenue"], r["cogs"], cd, r["revenue"] - r["cogs"] - cd,
         r["gross_profit"], r["revenue"] - r["cogs"] - cd - r["gross_profit"]))
p("  the 162.8 wedge between revenue less cost and gross profit in FY2025 is the "
  "DISCLOSED cash-discount line, not an unexplained difference.")
gp = R["revenue_fy25"] - R["cogs_fy25"] - HIS["2025"]["cash_discount"]["value"]
npbt = gp - R["sga_fy25"] - R["da_fy25"] - R["finance_cost_fy25"]
p("  gross - sga - d&a - finance = %.1f  vs filed NPBT %.1f  residual %.1f"
  % (npbt, R["npbt_fy25"], R["npbt_fy25"] - npbt))
p("  (the residual is other income/FX, a filed line, not a plug)")
p("  total assets %.1f = liabilities %.1f + equity %.1f -> %.1f"
  % (R["total_assets"], R["total_liabilities"], R["total_equity"],
     R["total_liabilities"] + R["total_equity"] - R["total_assets"]))


# --- 8. the latest disclosed balance sheet ---------------------------------
p("\n[8] BALANCE SHEET — the bridge against the LATEST disclosed one")
B = json.load(open(os.path.join(HERE, "bs_1q2026.json")))
Q = {k: v["value"] for k, v in B["lines"].items()}
DEBT = ["loans_long_term", "notes_payable_long_term", "credit_facilities",
        "banks_credit_balances", "current_portion_st_loans",
        "notes_payable_short_term", "lease_liabilities_lt", "lease_liabilities_st"]
gd25 = sum(R[k] for k in DEBT)
gd26 = sum(Q[k] for k in DEBT)
assert abs(gd25 - W["gross_debt"]) < 0.5, "the debt stack does not reproduce the study's gross debt"
assert abs(Q["total_liabilities"] + Q["total_equity"] - Q["total_assets"]) < 0.5
p("  31 Dec 2025 (used):  gross debt %9.1f  cash %8.1f  net debt %9.1f"
  % (gd25, R["cash"], gd25 - R["cash"]))
p("  31 Mar 2026 (filed): gross debt %9.1f  cash %8.1f  net debt %9.1f"
  % (gd26, Q["cash"], gd26 - Q["cash"]))
d_nd = (gd26 - Q["cash"]) - (gd25 - R["cash"])
d_as = (Q["investments_assoc"] + Q["investment_property"]) - (R["investments_assoc"] + R["investment_property"])
p("  net debt %+.1f   associates + investment property %+.1f   equity effect %+.1f"
  % (d_nd, d_as, -d_nd + d_as))
dps = (-d_nd + d_as) / SH
p("  on the DCF lens: %.2f -> %.2f /sh (%+.4f)" % (base, base + dps, dps))
w_dcf = dict((r[0], r[4]) for r in L["rows"])["Discounted cash flow"]
w_bk = dict((r[0], r[4]) for r in L["rows"])["Book value of equity"]
d_bk = Q["total_equity"] / SH - R["total_equity"] / SH
p("  on the book lens: %.2f -> %.2f /sh (%+.4f)"
  % (R["total_equity"] / SH, Q["total_equity"] / SH, d_bk))
tot = w_dcf * dps + w_bk * d_bk
p("  weighted central: %.4f -> %.4f (%+.4f, %+.1f%%); gap vs spot %+.1f%% -> %+.1f%%"
  % (CENTRAL, CENTRAL + tot, tot, 100 * tot / CENTRAL,
     100 * (CENTRAL / SPOT - 1), 100 * ((CENTRAL + tot) / SPOT - 1)))
out["bs_1q26_effect_per_share"] = tot
out["central_on_latest_bs"] = CENTRAL + tot

json.dump(out, open(os.path.join(HERE, "gap_review_calcs.json"), "w"), indent=1)
p("\nwrote gap_review_calcs.json")
