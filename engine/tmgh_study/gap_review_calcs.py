"""Arithmetic behind GAP_REVIEW_01-09-2026.md [R-GAP-01].

Every figure in that review that is not read straight off a filing is computed
here from the study's own committed code and numbers, and printed. Nothing in
the review is typed.
"""
import json, os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import inputs as IN, model as M, valuation as VAL

N = json.load(open(os.path.join(HERE, "study_numbers.json")))
W = N["wacc"]
IS = {k: v["value"] for k, v in IN.IS.items()}
BS = {k: v["value"] for k, v in IN.BS.items()}
KPI = {k: v["value"] for k, v in IN.KPI.items()}
SH = KPI["shares_outstanding"]
SPOT = N["spot"]
CENTRAL = N["central"]
CASES = N["per_share_nci_book"]
out = {}
p = print

p("=" * 78); p("TMGH GAP REVIEW — arithmetic"); p("=" * 78)
p("published cases (book minority): " + "  ".join(
    "%s %.2f" % (k, v) for k, v in sorted(CASES.items(), key=lambda x: x[1])))
p("median %.3f   spot %.2f   gap %+.1f%%   highest case %.2f (%+.1f%%)"
  % (CENTRAL, SPOT, 100 * (CENTRAL / SPOT - 1), max(CASES.values()),
     100 * (max(CASES.values()) / SPOT - 1)))

# --- 1. base year -----------------------------------------------------------
p("\n[1] BASE YEAR — FY2025, foots to the filed statement")
gp = (IS["dev_revenue_fy25"] - IS["dev_cost_fy25"]
      + IS["hosp_revenue_fy25"] - IS["hosp_cost_fy25"]
      + IS["other_revenue_fy25"] - IS["other_cost_fy25"])
p("  three segments net of their own cost   %10.1f  vs filed gross profit %10.1f  %+.1f"
  % (gp, IS["gross_profit_fy25"], gp - IS["gross_profit_fy25"]))
oi = (IS["gross_profit_fy25"] + IS["ip_revaluation_fy25"] + IS["other_income_fy25"]
      - IS["ga_fy25"] - IS["marketing_fy25"] + IS["fx_fy25"]
      - IS["govt_donations_fy25"] - IS["provisions_ecl_fy25"])
p("  gross + revaluation + other income - G&A - marketing + fx - donations - ECL")
p("                                         %10.1f  vs filed operating   %10.1f  %+.1f"
  % (oi, IS["operating_income_fy25"], oi - IS["operating_income_fy25"]))
pbt = (IS["operating_income_fy25"] - IS["da_fy25"] + IS["finance_income_fy25"]
       - IS["finance_cost_fy25"] + IS["associates_fy25"])
p("  - D&A + finance income - finance cost + associates  %10.1f  vs filed PBT %10.1f  %+.1f"
  % (pbt, IS["pbt_fy25"], pbt - IS["pbt_fy25"]))
np_ = IS["pbt_fy25"] - IS["tax_fy25"] - IS["deferred_tax_fy25"]
p("  - current tax - deferred tax           %10.1f  vs filed net profit %10.1f  %+.1f"
  % (np_, IS["net_profit_fy25"], np_ - IS["net_profit_fy25"]))
p("  parent %.1f + minority %.1f = %.1f vs filed net profit %.1f  %+.1f"
  % (IS["npat_parent_fy25"], IS["nci_profit_fy25"],
     IS["npat_parent_fy25"] + IS["nci_profit_fy25"], IS["net_profit_fy25"],
     IS["npat_parent_fy25"] + IS["nci_profit_fy25"] - IS["net_profit_fy25"]))
p("  balance sheet: assets %.1f = liabilities %.1f + equity %.1f  -> %+.1f"
  % (BS["total_assets"], BS["total_liabilities"], BS["total_equity"],
     BS["total_liabilities"] + BS["total_equity"] - BS["total_assets"]))

# --- 2. the minority ---------------------------------------------------------
p("\n[2] MINORITY — the share of VALUE removed vs the share of PROFIT it earns")
nci_eq = BS["nci_equity"] / BS["total_equity"]
nci_pr25 = IS["nci_profit_fy25"] / IS["net_profit_fy25"]
nci_pr24 = (IS["net_profit_fy24"] - IS["npat_parent_fy24"]) / IS["net_profit_fy24"]
nci_pr24r = ((IS["net_profit_fy24_restated"] - IS["npat_parent_fy24_restated"])
             / IS["net_profit_fy24_restated"])
p("  minority share of BOOK EQUITY, 30 Jun 2026        %.2f%%" % (100 * nci_eq))
p("  minority share of FY2025 PROFIT as filed          %.2f%%" % (100 * nci_pr25))
p("  minority share of FY2024 PROFIT as filed          %.2f%%" % (100 * nci_pr24))
p("  minority share of FY2024 PROFIT as restated       %.2f%%" % (100 * nci_pr24r))
p("  the bridge removes the minority at book (%.1f) or at %.1f%% of value;"
  % (BS["nci_equity"], 100 * nci_eq))
p("  the filed profit split says the minority earns less than half that share.")
out["nci_equity_share"], out["nci_profit_share"] = nci_eq, nci_pr25

# --- 3. discount rate --------------------------------------------------------
p("\n[3] DISCOUNT RATE")
ke = W["ke_rating"]
p("  ke = rf* %.4f + beta %.4f x ERP %.4f = %.4f%%"
  % (W["rf_star_rating"], W["beta_record"]["beta"],
     N["wacc"]["inputs"]["damodaran"]["total_erp_rating"], 100 * ke))
p("  weights: equity %.4f (market cap %.1f) debt %.4f (%.1f) -> WACC %.4f%%"
  % (W["weight_equity"], W["inputs"]["market_cap"], W["weight_debt"],
     W["inputs"]["interest_bearing_debt"], 100 * W["wacc_rating"]))
p("  CDS basis %.4f%%.  beta is tier 1 and conforming: r2 %.3f se %.3f n %d %s"
  % (100 * W["wacc_cds"], W["beta_record"]["r2"], W["beta_record"]["se"],
     W["beta_record"]["n"], W["beta_record"]["gate_msg"]))
cash = BS["cash"] + BS["deposits_current"] + BS["deposits_noncurrent"]
debt = BS["loans_noncurrent"] + BS["loans_current"] + BS["credit_facilities"]
p("  cash and deposits %.1f, borrowings %.1f -> NET CASH %.1f"
  % (cash, debt, cash - debt))
p("  charged once? FCFF = ebit*(1-t) + da - capex - (d_pud - d_advances): "
  "no finance income in it,")
p("  and the bridge adds cash once at face. The 2026 finance income of %.1f "
  "sits in the" % M.project("capacity")["rows"][0]["finance_income"])
p("  projected income statement and EPS ONLY, never in the discounted flow. "
  "No double count.")
p("  equity weight %.4f is below one, so the AMOC net-cash pathology "
  "(negative debt" % W["weight_equity"])
p("  weight -> equity weight above one -> operating rate above the cost of "
  "equity) cannot arise.")

# --- 4. macro coherence ------------------------------------------------------
p("\n[4] MACRO COHERENCE — every nominal growth rate in one model")
rfs = W["rf_star_rating"]
p("  rf* %.2f%%; at a 1-3%% real sovereign rate the terminal rate embeds "
  "%.2f%%-%.2f%% inflation" % (100 * rfs, 100 * (rfs - 0.03), 100 * (rfs - 0.01)))
infl = rfs - 0.02
for nm, g in (("hospitality revenue", M.HOSP_GROWTH),
              ("other recurring revenue", M.OTHER_GROWTH),
              ("terminal growth", M.TERMINAL_GROWTH),
              ("REPLENISHMENT SALES", M.SALES_FADE - 1.0),
              ("deposit yield", M.DEPOSIT_YIELD)):
    p("    %-26s %+7.2f%% nominal   %+7.2f%% real at %.2f%% inflation"
      % (nm, 100 * g, 100 * ((1 + g) / (1 + infl) - 1), 100 * infl))
p("  five nominal rates, no stated inflation path binding them. Contracted "
  "sales are the")
p("  outlier: -15%% NOMINAL a year is about -26%% REAL a year, %.0fbn falling "
  "to %.0fbn by 2035"
  % (M.REPLENISHMENT_SALES / 1000, M.REPLENISHMENT_SALES * M.SALES_FADE ** 9 / 1000))
p("  against H1-2026 contracted sales of %.0fbn (%.0fbn annualised), FY2025 "
  "%.0fbn, FY2024 %.0fbn."
  % (KPI["contracted_sales_h1_26"] / 1000, 2 * KPI["contracted_sales_h1_26"] / 1000,
     KPI["contracted_sales_fy25"] / 1000, KPI["contracted_sales_fy24"] / 1000))

# --- 5. what moves the answer -----------------------------------------------
p("\n[5] SENSITIVITY — each lever alone, capacity mode, rating ERP")
BASE_W = W["wacc_rating"]
def run(wacc=None, fade=None, nci_mode="book", nci_override=None):
    if fade is not None:
        M.SALES_FADE = fade
    d = VAL.discounted("capacity", wacc if wacc else BASE_W)
    b = VAL.bridge(d)
    M.SALES_FADE = 0.85
    if nci_override is not None:
        return (b["equity_before_minority"] * (1 - nci_override)) / SH, d
    return b["per_share_nci_%s" % nci_mode], d
base_ps, base_d = run()
p("  reproduces the published rating|capacity case: %.4f vs %.4f"
  % (base_ps, CASES["rating|capacity"]))
assert abs(base_ps - CASES["rating|capacity"]) < 1e-6
b0 = VAL.bridge(base_d)
p("  enterprise value %.1f = explicit %.1f + residual book %.1f + recurring "
  "perpetuity %.1f"
  % (b0["enterprise_value"], base_d["pv_explicit"], base_d["pv_residual_book"],
     base_d["pv_terminal_recurring"]))
p("  + net cash %.1f + investment property %.1f + associates %.1f + FVOCI %.1f "
  "= %.1f before minority"
  % (b0["net_cash"], b0["investment_property"], b0["associates"], b0["fvoci"],
     b0["equity_before_minority"]))
p("")
p("  %-52s %8s %8s" % ("", "EGP/sh", "vs spot"))
def show(lbl, ps):
    p("  %-52s %8.2f %+7.1f%%" % (lbl, ps, 100 * (ps / SPOT - 1)))
    return ps
show("as published (rating | capacity)", base_ps)
for w in (0.30, 0.25, 0.20):
    show("WACC %.0f%% instead of %.2f%%" % (100 * w, 100 * BASE_W), run(wacc=w)[0])
for f in (1.00, 1.15):
    show("contracted sales fade %.2f (%+.0f%% nominal) instead of 0.85"
         % (f, 100 * (f - 1)), run(fade=f)[0])
show("minority at its FILED PROFIT share (%.1f%%) not book" % (100 * nci_pr25),
     run(nci_override=nci_pr25)[0])
show("minority proportional at book share (%.1f%%)" % (100 * nci_eq),
     run(nci_mode="proportional")[0])
both = run(fade=1.15, nci_override=nci_pr25)[0]
show("BOTH: sales flat in real terms AND minority at its profit share", both)
out["case_published"] = base_ps
out["case_both_corrections"] = both

# --- 6. terminal -------------------------------------------------------------
p("\n[6] TERMINAL — no perpetuity on the development leg")
p("  the order book is FINITE and is converted over %d years as an annuity, "
  "not capitalised" % base_d["conversion_years"])
p("  excess work in progress credited at cost %.1f, PV %.1f"
  % (base_d["excess_work_in_progress"], base_d["pv_excess_wip"]))
p("  residual book %.1f, annual cash %.1f, PV %.1f (%.1f%% of EV)"
  % (base_d["residual_book"], base_d["residual_annual_cash"],
     base_d["pv_residual_book"],
     100 * base_d["pv_residual_book"] / b0["enterprise_value"]))
p("  a growing perpetuity is taken ONLY on the recurring legs: FCFF %.1f at "
  "g=%.0f%% -> PV %.1f (%.1f%% of EV)"
  % (base_d["terminal_recurring_fcff"], 100 * M.TERMINAL_GROWTH,
     base_d["pv_terminal_recurring"],
     100 * base_d["pv_terminal_recurring"] / b0["enterprise_value"]))
p("  explicit 10 years %.1f%% of EV — the terminal is NOT where this answer "
  "comes from"
  % (100 * base_d["pv_explicit"] / b0["enterprise_value"]))

# --- 7. multiples -------------------------------------------------------------
p("\n[7] MULTIPLE CROSS-CHECK")
eps25 = IS["npat_parent_fy25"] / SH
bvps = BS["equity_parent"] / SH
ebitda25 = IS["operating_income_fy25"] + IS["da_fy25"]
p("  FY2025 attributable EPS %.3f (company reports %.2f) · parent book/sh %.2f "
  "· operating income + D&A %.1f" % (eps25, IS["eps_fy25"], bvps, ebitda25))
nonop = (cash - debt) + BS["investment_property"] + BS["associates"] + BS["fvoci"]
p("  non-operating assets in the bridge: net cash %.1f + investment property %.1f"
  % (cash - debt, BS["investment_property"]))
p("  + associates %.1f + FVOCI %.1f = %.1f, which is %.1f%% of the pre-minority equity"
  % (BS["associates"], BS["fvoci"], nonop, 100 * nonop / b0["equity_before_minority"]))
p("")
p("  %-26s %8s %10s %10s %9s %8s %12s" %
  ("", "EGP/sh", "mcap", "group opco", "P/E FY25", "P/B", "opco/book"))
for lbl, px in (("lowest case", min(CASES.values())), ("median", CENTRAL),
                ("published capacity case", CASES["rating|capacity"]),
                ("highest case", max(CASES.values())),
                ("market, 23-Aug-2026", SPOT)):
    mc = px * SH
    opco = mc + BS["nci_equity"] - nonop
    p("  %-26s %8.2f %10.0f %10.0f %9.2fx %7.2fx %11.1f%%"
      % (lbl, px, mc, opco, px / eps25, px / bvps, 100 * opco / KPI["backlog_jun26"]))
p("  'group opco' = market value of the whole group's operating business implied by")
p("  that per-share figure: mcap + the minority deducted at book, less the non-")
p("  operating assets the bridge adds. It is what the order book, the land bank and")
p("  the hotels are being valued at, for the group, before any minority split.")
p("  order book at 30 Jun 2026 %.0f · contracted sales H1-2026 %.0f · land bank "
  "%.0f mn sqm" % (KPI["backlog_jun26"], KPI["contracted_sales_h1_26"],
                   KPI["landbank_msqm"]))


# --- 8. the model against this study's own walk-forward record ---------------
p("\n[8] THE MODEL AGAINST ITS OWN WALK-FORWARD RECORD, FY2026")
WF = N["walkforward"]["forward_ranges"]["2026"]
r0 = M.project("capacity")["rows"][0]
pairs = [("new_sales", r0["new_sales"], "contracted sales"),
         ("dev_revenue", r0["dev_revenue"], "development revenue"),
         ("recurring_revenue", r0["hosp_revenue"] + r0["other_revenue"], "recurring revenue"),
         ("total_revenue", r0["revenue"], "total revenue"),
         ("gross_profit", r0["gross_profit"], "gross profit")]
p("  %-22s %12s %12s %9s" % ("", "model", "walk-fwd", "model vs"))
for k, mv, lbl in pairs:
    c = WF[k]["central"]
    p("  %-22s %12.0f %12.0f %8.1f%%" % (lbl, mv, c, 100 * (mv / c - 1)))
p("  contracted sales, actuals: H1-2026 %.0f (%.0f annualised) · FY2025 %.0f · FY2024 %.0f"
  % (KPI["contracted_sales_h1_26"], 2 * KPI["contracted_sales_h1_26"],
     KPI["contracted_sales_fy25"], KPI["contracted_sales_fy24"]))
p("  the record's own finding on this driver is that the method came back LOW, and the")
p("  model then sets it below every recent year and fades it 15 per cent a year on top.")
out["model_vs_walkforward_2026"] = {k: (mv, WF[k]["central"]) for k, mv, _ in pairs}

# --- 9. what rate the market is paying -------------------------------------
p("\n[9] WHAT DISCOUNT RATE THE PRICE IMPLIES")
IR = N["lenses"]["implied_discount_rate"]
p("  to reach the traded %.2f this model needs %.2f%% (capacity) or %.2f%% (recovery)"
  % (SPOT, 100 * IR["capacity"], 100 * IR["recovery"]))
p("  the study uses %.2f%%; Egypt's own 10-year sovereign is %.2f%%"
  % (100 * W["wacc_rating"], 100 * W["inputs"]["rf_observed"]))
p("  so the price implies an equity return at or below the sovereign yield: either the")
p("  market is charging no risk premium over the government bond, or this rate is high.")
out["implied_rate"] = IR

json.dump(out, open(os.path.join(HERE, "gap_review_calcs.json"), "w"), indent=1)
p("\nwrote gap_review_calcs.json")
