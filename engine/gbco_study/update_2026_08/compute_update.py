#!/usr/bin/env python3
"""GBCO fundamental update — 30-Aug-2026 edition. Fair value re-derived under the
v2 cost-of-capital method with the attested EGX30 beta, on the 15-year tier-A panel
built by engine/gbco_training/ (walk-forward-trained; TRAINING_RECORD.md carries the
method evidence and the years-3-5 range construction used here).

Split-leg architecture (operating co + captive lender + associate stake):
  leg 1  GB Auto           — ground-up units x price, FCFF DCF at v2 WACC
  leg 2  GB Capital ex-MNT — book-anchored with earnings cross-check
  leg 3  MNT-BV stake      — DUAL-FRAMED (carrying value vs June-2026 round mark),
                             published side by side, never averaged (house rule)
  leg 4  other associates & FV investments — at carrying

Gates called here per R-ENF-02: assert_beta_provenance, assert_sigcm,
assert_ground_up (+ assert_model_study is NOT claimed — see QC table: this is a
fair-value/compute re-issue; the full model-report document rebuild remains open).

Sources: every input carries (value, source, date, tier) in INPUTS below; the
company ring is the training panel (all tier A); live market inputs fetched
30-Aug-2026 and logged in SWEEP_REGISTER_UPDATE.md. No rating, no price target —
fair-value ranges only. Nothing here publishes to the live site.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ENGINE)

from beta_regression import own_stock_beta                      # noqa: E402
from wacc_builder import WaccInputs, build_wacc                 # noqa: E402
from research_protocol import (                                 # noqa: E402
    SIGCMChecklist, assert_sigcm, assert_beta_provenance,
    DriverLine, assert_ground_up, STANDARD_VERSION)

EGP = "EGP mn"

# ---------------------------------------------------------------------------
# INPUTS — four-field register (value / source / date / tier)
# ---------------------------------------------------------------------------
INPUTS = {
    # --- market / macro (fetched live 30-Aug-2026; SWEEP_REGISTER_UPDATE.md) ---
    "rf_observed": (0.2287, "investing.com Egypt 10Y EGP govt yield (15.387% cpn, May-2032)", "2026-08-27", "C"),
    "sov_spread_rating": (0.0637, "Damodaran ctryprem.html ORIGINAL file, Egypt row, Caa1 adjusted default spread", "2026-01-05", "C"),
    "sov_spread_cds": (0.0341, "Damodaran ctryprem.html, Egypt sovereign CDS default spread", "2026-01-05", "C"),
    "erp_rating": (0.1394, "Damodaran ctryprem.html, Egypt total ERP rating basis", "2026-01-05", "C"),
    "erp_cds": (0.0941, "Damodaran ctryprem.html, Egypt total ERP CDS basis", "2026-01-05", "C"),
    "cbe_lending": (0.20, "CBE MPC 20-Aug-2026: o/n lending 20.0% (4th consecutive hold); core CPI 14.7% Jul-26", "2026-08-20", "B"),
    "kd_pretax": (0.2437, "sovereign 10Y 22.87% + 150bp corporate spread (marginal, EGP; rule: above sovereign). Short-tenor alternative (CBE o/n lending 20.0% + 200bp = 22.0%) reported as sensitivity", "2026-08-30", "C"),
    "egp_usd": (50.25, "investing.com USD/EGP close", "2026-08-28", "C"),
    "tax_statutory": (0.225, "Egypt corporate rate (Law 96/2015; also Damodaran Egypt row)", "2026-01-05", "B"),
    # --- company (tier A — company documents; training panel + FY25 FS notes) ---
    "spot": (29.51, "EGX close, engine/raw_ohlc/EG/GBCO.csv last row (as rendered on the live page)", "2026-08-23", "A"),
    "shares_mn": (1085.5, "ER 4Q25: shares outstanding 1,085,500,000", "2026-02-26", "A"),
    "auto_rev_fy25": (66358.3, "ER 4Q25 Table 11, GB Auto total revenue before eliminations", "2026-02-26", "A"),
    "auto_rev_h1_26": (40021.5, "ER 2Q26: GB Auto revenues before intercompany eliminations, 1H26", "2026-08-13", "A"),
    "cap_rev_fy25": (14743.0, "ER 4Q25 Table 13, GB Capital total revenue before eliminations", "2026-02-26", "A"),
    "cap_rev_h1_26": (9088.2, "ER 2Q26: GB Capital revenues before eliminations 1H26 (+62.9% y-o-y)", "2026-08-13", "A"),
    "cap_np_h1_26": (649.6, "ER 2Q26: GB Capital net profit after tax & NCI 1H26", "2026-08-13", "A"),
    "cap_portfolio_h1_26": (24.0e3, "ER 2Q26: net on-book portfolio EGP 24.0bn, +33.6% y-o-y; NPL 2.8%", "2026-08-13", "A"),
    "auto_nd_fy25": (15210.0, "ER 4Q25 Table 7: GB Auto net debt", "2026-02-26", "A"),
    "auto_nci_eq_fy25": (800.4, "ER 4Q25 Table 12: GB Auto segment NCI equity", "2026-02-26", "A"),
    "auto_ebitda_h1_26": (3484.8, "ER 2Q26: GB Auto EBITDA 1H26 (+13.4% y-o-y); GPM 14.3%", "2026-08-13", "A"),
    "cap_equity_fy25": (19314.4, "ER 4Q25 Table 12: GB Capital segment total equity (incl. NCI 1,001.8)", "2026-02-26", "A"),
    "cap_nci_eq_fy25": (1001.8, "ER 4Q25 Table 12", "2026-02-26", "A"),
    "mnt_carrying_fy25": (12853.321, "FY25 FS note 34: MNT Investment B.V. Group carrying value, 44.01%", "2026-02-26", "A"),
    "mnt_stake_current": (0.4293, "H1-26 limited review report: group owns approximately 42.93% of MNT-BV", "2026-08-13", "A"),
    "mnt_stake_post2nd": (0.4161, "GB Corp PR 9-Jun-2026: stake will be adjusted to 41.61% (vs 42.58% prior) on completion", "2026-06-09", "A"),
    "mnt_round_usd_bn": (1.4, "press (Wamda/EnterpriseAM/Reuters via TradingView, Jun-2026): USD 1.4bn post-round valuation, Al Ahly Capital-led, first closing; NOT stated in the company PR", "2026-06-09", "C"),
    "other_assoc_book": (836.1, "FY25 FS notes 34/35-A: Bedaya 152.98 + Kaf 140.20 + Mice 125.70 + FVOCI investments 417.20", "2026-02-26", "A"),
    "capex_committed": (525.479, "FY25 FS note 31: contractual capital commitments (new production lines + branches)", "2026-02-26", "A"),
    "fx_net_exposure": (-2192.075, "FY25 FS note 29: net USD exposure EGP (2,192,075)k; EUR +135,364k — debt book effectively EGP", "2026-02-26", "A"),
    "group_np_parent_h1_26": (1262.006, "H1-26 interim FS: NP attributable to parent, 6M", "2026-08-13", "A"),
}
SRC = {k: v[1] + f" [{v[2]}, tier {v[3]}]" for k, v in INPUTS.items()}
V = {k: v[0] for k, v in INPUTS.items()}

# ---------------------------------------------------------------------------
# 1) BETA — the sanctioned resolver, attested (tier 1, conforming)
# ---------------------------------------------------------------------------
beta_rec = own_stock_beta("GBCO", "EG", "EGX", root=ENGINE)
assert_beta_provenance(beta_rec)
BETA = beta_rec["beta"]

# ---------------------------------------------------------------------------
# 2) WACC — v2 (rf* = observed − sovereign's own default spread; both ERP bases)
#    Weights: group MV equity vs GB Auto borrowings (the DCF discounts the auto
#    leg; GB Capital's funding is working inventory of the lender, valued in its
#    own leg — blending it into WACC would double-charge the financing business).
# ---------------------------------------------------------------------------
MV_EQUITY = V["spot"] * V["shares_mn"]                     # 32,033 EGP mn
AUTO_DEBT = 21486.3                                        # ER 4Q25 Table 7 total debt (GB Auto)
wacc_in = WaccInputs(
    rf_observed=V["rf_observed"],
    erp_rating=V["erp_rating"], sov_default_spread_rating=V["sov_spread_rating"],
    erp_cds=V["erp_cds"], sov_default_spread_cds=V["sov_spread_cds"],
    beta=BETA, beta_source=f"own_stock_beta GBCO vs EGX30, weekly Dimson, n={beta_rec['n']}, "
                           f"R2={beta_rec['r2']:.3f}, window {beta_rec['first_obs']}..{beta_rec['last_obs']}, tier 1 conforming",
    kd_pretax_local=V["kd_pretax"], pct_debt_local_ccy=1.0,
    tax_rate=V["tax_statutory"],
    market_cap=MV_EQUITY, total_debt=AUTO_DEBT,
    rf_source=SRC["rf_observed"], erp_source=SRC["erp_rating"], kd_source=SRC["kd_pretax"],
    kd_is_marginal=True,
    debt_currency_evidence=SRC["fx_net_exposure"] + "; FY25 FS: variable-rate loans/OD EGP 37.9bn, "
                           "net FX liability only ~EGP 2.2bn — EGP-denominated book, no FX tranche modelled",
    weights_source="MV equity = 29.51 x 1,085.5mn shares; debt = GB Auto total debt 21,486.3 (ER 4Q25 Table 7)",
)
wacc = build_wacc(wacc_in)
WACC = wacc.wacc_cds          # primary basis (continuity with the delivered study)
WACC_R = wacc.wacc_rating

# ---------------------------------------------------------------------------
# 3) GROUND-UP FORECAST FY2026-2030 (EGP mn)
#    Panel basis: training panel (C3 composition: PC = Egypt+Iraq+Jordan incl.
#    after-sales; financing ex-MNT). H2-2026 projected from H1 actuals with the
#    stated momentum assumptions; every line logged as a DriverLine.
# ---------------------------------------------------------------------------
YRS = [2026, 2027, 2028, 2029, 2030]
CPI = {2026: 0.145, 2027: 0.115, 2028: 0.095, 2029: 0.080, 2030: 0.075}   # CBE Jul-26 actuals + convergence path to 7±2 target H2-2027+ (CBE outlook, tier B)
DEP = 0.04                                                                # EGP/USD drift assumption at ~50.25 (stability narrative, mild slide)
ASP_G = {y: CPI[y] + 0.5 * DEP for y in YRS}                              # house price escalator (training pre-registration parameter)

# volumes (units): FY26 = H1-26 actual + H2-25 base x stated momentum; then growth path
pc_u = {2026: 29554 + round((56548 - 25989) * 1.082)}     # H2 momentum: H1 y/y +13.7% damped to +8.2% for H2 (regional drag persists per ER 2Q26; Jordan relief only from Q4)
lm_u = {2026: 21173 + round((33906 - 14216) * 1.30)}      # H1 +48.9% y/y; H2 damped to +30%
cv_u = {2026: 2490 + round((3404 - 1534) * 1.45)}         # H1 +62.3%; exports + Elegance ramp, damped to +45%; Sokhna extra shift under consideration
PC_G = {2027: 0.09, 2028: 0.08, 2029: 0.07, 2030: 0.06}   # Egypt market ~+10%/yr easing cycle x share held ~21% + regional normalization from 2027 (GSO enforcement, ER 2Q26)
LM_G = {2027: 0.15, 2028: 0.12, 2029: 0.10, 2030: 0.08}
CV_G = {2027: 0.12, 2028: 0.10, 2029: 0.08, 2030: 0.06}
for y in YRS[1:]:
    pc_u[y] = pc_u[y - 1] * (1 + PC_G[y])
    lm_u[y] = lm_u[y - 1] * (1 + LM_G[y])
    cv_u[y] = cv_u[y - 1] * (1 + CV_G[y])

# ASPs (EGP mn/unit): FY26 = H1-26 actual ASP x mild H2 drift; then escalator
pc_asp = {2026: (30595.7 / 29554) * 1.02}
lm_asp = {2026: (1435.2 / 21173) * 1.02}
cv_asp = {2026: (4749.1 / 2490) * 1.02}
for y in YRS[1:]:
    pc_asp[y] = pc_asp[y - 1] * (1 + ASP_G[y])
    lm_asp[y] = lm_asp[y - 1] * (1 + ASP_G[y])
    cv_asp[y] = cv_asp[y - 1] * (1 + ASP_G[y])

pc_rev = {y: pc_u[y] * pc_asp[y] for y in YRS}
lm_rev = {y: lm_u[y] * lm_asp[y] for y in YRS}
cv_rev = {y: cv_u[y] * cv_asp[y] for y in YRS}
tr_rev = {2026: 2572.3 + (4242.8 - 2438.2) * 1.10}        # trading: H1 actual + H2-25 x +10%
oth_auto = {2026: 1127.6 * (1 + CPI[2026])}               # FY25 auto residual (66,358.3 - four lines) grows with CPI
for y in YRS[1:]:
    tr_rev[y] = tr_rev[y - 1] * (1 + CPI[y] + 0.02)
    oth_auto[y] = oth_auto[y - 1] * (1 + CPI[y])
auto_rev = {y: pc_rev[y] + lm_rev[y] + cv_rev[y] + tr_rev[y] + oth_auto[y] for y in YRS}

# GB Capital (ex-MNT consolidated perimeter): H1 momentum then decaying growth
cap_rev = {2026: V["cap_rev_h1_26"] * 2.05}               # H2 seasonally heavier (FY25: H2 = 52.4% of year); +26% y/y vs +62.9% H1 — deliberate deceleration as securitization normalizes (ER 2Q26 guidance)
CAP_G = {2027: 0.22, 2028: 0.20, 2029: 0.18, 2030: 0.16}
for y in YRS[1:]:
    cap_rev[y] = cap_rev[y - 1] * (1 + CAP_G[y])

ELIM = 0.011                                              # FY25 eliminations 871.5 / (66,358.3+14,743.0) = 1.07% — held
rev = {y: (auto_rev[y] + cap_rev[y]) * (1 - ELIM) for y in YRS}

# margins as OUTPUTS of the leg mix (segment GP margins; unit cost stacks are not
# disclosed per leg — gap flagged in the driver record):
AUTO_GPM = {2026: 0.143, 2027: 0.148, 2028: 0.152, 2029: 0.155, 2030: 0.155}  # H1-26 actual 14.3% -> FY24 level 19.2% never re-assumed; Sadat localization + easing recover ~1pp/yr
CAP_GPM = {y: 0.188 for y in YRS}                                             # FY25 actual 18.8% (2,766.4/14,743.0) held flat
gp = {y: auto_rev[y] * AUTO_GPM[y] + cap_rev[y] * CAP_GPM[y] for y in YRS}
gpm = {y: gp[y] / rev[y] for y in YRS}

SGA_PCT = 0.080     # FY25 8.16%, H1-26 7.84% — held at 8.0% (watch flag SGA_UP_5PCT applied as a RANGE widener, not to the point path — TRAINING_RECORD §4)
OTH_PCT = 0.010     # other income, FY25 1.14% held conservatively at 1.0%
ECL_PCT = 0.0035    # FY25 0.29%; growing book
sga = {y: rev[y] * SGA_PCT for y in YRS}
op = {y: gp[y] - sga[y] + rev[y] * OTH_PCT - rev[y] * ECL_PCT for y in YRS}

assoc = {2026: 850.0}                                     # H1-26 actual 410.1 x2 + mild H2 recovery (Turkey hyperinflation fading); FY25 986.4
for y in YRS[1:]:
    assoc[y] = assoc[y - 1] * 1.25                        # book compounding; MNT loan book USD 1.7bn+, +25%/yr nominal EGP

fin_net = {2026: -4700.0, 2027: -4300.0, 2028: -3900.0, 2029: -3600.0, 2030: -3400.0}
# H1-26 actual net finance cost 2,281.0; path eases with CBE cuts (CBE outlook: single digits H2-2027) and auto working-capital normalization

pbt = {y: op[y] + fin_net[y] + assoc[y] for y in YRS}
ETR = {2026: 0.40, 2027: 0.30, 2028: 0.27, 2029: 0.25, 2030: 0.24}  # H1-26 actual 41.0% (Egypt profits taxed, regional losses unrelieved); converges toward 22.5% statutory + non-deductibles
np_total = {y: pbt[y] * (1 - ETR[y]) for y in YRS}
NCI = {2026: -250.0, 2027: -50.0, 2028: 100.0, 2029: 200.0, 2030: 280.0}  # H1-26 actual -206.4 (regional losses at NCI); fades per management Q4-26 guidance
np_parent = {y: np_total[y] - NCI[y] for y in YRS}
eps = {y: np_parent[y] / V["shares_mn"] for y in YRS}

# ---------------------------------------------------------------------------
# 4) DRIVER RECORD — assert_ground_up on the FY26 revenue base
# ---------------------------------------------------------------------------
base = auto_rev[2026] + cap_rev[2026]
lines = [
    DriverLine("PC & after-sales (EG+IQ+JO)", "unit", pc_rev[2026] / base,
               unit="vehicles (CKD+CBU)", unit_source="ER 2Q26 Table 2 (H1-26 29,554 units); ER 4Q25 Table 2 (FY25 56,548)",
               price_basis="disclosed segment revenue / units = ASP (H1-26 EGP 1.035mn), escalated at CPI+0.5×dep",
               cost_basis="segment GP margin path (H1-26 14.3% actual); unit cost stack not disclosed",
               gap_note=None),
    DriverLine("Light Mobility (2/3/4W)", "unit", lm_rev[2026] / base,
               unit="vehicles", unit_source="ER 2Q26 Table 5 (H1-26 21,173); ER 4Q25 Table 5",
               price_basis="disclosed revenue/units ASP, escalated at CPI+0.5×dep",
               cost_basis="inside GB Auto GP margin path", gap_note=None),
    DriverLine("CV & construction equipment", "unit", cv_rev[2026] / base,
               unit="vehicles/units", unit_source="ER 2Q26 Table 4 (H1-26 2,490); ER 4Q25 Table 4",
               price_basis="disclosed revenue/units ASP, escalated at CPI+0.5×dep",
               cost_basis="inside GB Auto GP margin path", gap_note=None),
    DriverLine("Trading (tires + ready parts)", "segment", tr_rev[2026] / base,
               gap_note="revenue-only LoB (no unit volumes disclosed); grown at CPI+2pp off H1-26 actual"),
    DriverLine("Other auto / intersegment residual", "segment", oth_auto[2026] / base,
               gap_note="FY25 residual of GB Auto total vs four disclosed LoBs (1.7% of leg); grown at CPI"),
    DriverLine("GB Capital (financing, ex-MNT)", "derived", cap_rev[2026] / base,
               unit="net on-book portfolio (EGP bn)", unit_source="ER 2Q26: 24.0bn at 1H26, +33.6% y/y",
               price_basis="revenue momentum off H1-26 actual (x2.05 seasonal), decaying growth path",
               cost_basis="segment GP margin 18.8% (FY25 actual) held",
               gap_note="product-level yields not disclosed; modelled on portfolio momentum, not unit economics"),
]
ground_up = assert_ground_up(lines, ticker="GBCO")

# ---------------------------------------------------------------------------
# 5) LEG 1 — GB Auto FCFF DCF (v2 WACC, CDS basis primary)
# ---------------------------------------------------------------------------
AUTO_OPM = {2026: 0.070, 2027: 0.080, 2028: 0.088, 2029: 0.093, 2030: 0.095}  # H1-26 EBITDA margin 8.7% less D&A ~1.6pp -> ~7.0%; recovery toward (below) FY24's 11.8%
auto_ebit = {y: auto_rev[y] * AUTO_OPM[y] for y in YRS}
auto_da = {2026: 800.0}                                    # FY25 683.3 + Sadat commissioning
for y in YRS[1:]:
    auto_da[y] = auto_da[y - 1] * 1.15
auto_capex = {2026: V["capex_committed"] + 0.015 * auto_rev[2026]}   # committed programme (FS note 31) + 1.5% maintenance
for y in YRS[1:]:
    auto_capex[y] = 0.015 * auto_rev[y]
WC_PCT = {2026: 0.27, 2027: 0.255, 2028: 0.245, 2029: 0.24, 2030: 0.24}  # FY25 28.5% (18,917/66,358) normalizing (inventory optimization, ER 2Q26)
auto_wc = {y: auto_rev[y] * WC_PCT[y] for y in YRS}
wc_prev = 18917.0                                          # FY25 actual GB Auto WC (ER 4Q25 Table 6)
auto_fcff, wcp = {}, wc_prev
for y in YRS:
    dwc = auto_wc[y] - wcp
    auto_fcff[y] = auto_ebit[y] * (1 - V["tax_statutory"]) + auto_da[y] - auto_capex[y] - dwc
    wcp = auto_wc[y]

TG = 0.10   # terminal nominal growth: CPI target 7% + ~3% real; sensitivity 0.09/0.115
pv, df = 0.0, 1.0
for y in YRS:
    df /= (1 + WACC)
    pv += auto_fcff[y] * df
tv = auto_fcff[2030] * (1 + TG) / (WACC - TG)
pv_tv = tv * df
auto_ev = pv + pv_tv
auto_eq = auto_ev - V["auto_nd_fy25"] - V["auto_nci_eq_fy25"]

# ---------------------------------------------------------------------------
# 6) LEG 2 — GB Capital ex-MNT (book-anchored; earnings cross-check)
# ---------------------------------------------------------------------------
cap_book_exmnt = V["cap_equity_fy25"] - V["cap_nci_eq_fy25"] - V["mnt_carrying_fy25"]  # parent, ex-MNT carrying
cap_np_exmnt_fy25 = 1365.9 - 986.4                        # ER 4Q25 Table 13: NP after NCI less associates pickup
cap_val = {"bear": 0.8 * cap_book_exmnt, "base": 1.0 * cap_book_exmnt, "bull": 1.4 * cap_book_exmnt}
# cross-check: base implies ~13.7x FY25 ex-MNT earnings (a depressed-earnings year:
# provisions + funding costs at peak rates); at H1-26 run-rate ex-MNT (~650 x2 less
# MNT pickup share) the multiple is ~6-8x — inside the EGX NBFS range.

# ---------------------------------------------------------------------------
# 7) LEG 3 — MNT-BV stake, DUAL-FRAMED (published side by side, never averaged)
# ---------------------------------------------------------------------------
mnt_book = V["mnt_carrying_fy25"]                                          # framing A: audited carrying (qualified — MNT-BV FS not provided to auditor)
mnt_round_now = V["mnt_round_usd_bn"] * 1e3 * V["egp_usd"] * V["mnt_stake_current"]     # framing B: USD 1.4bn round x 42.93% x 50.25
mnt_round_post = V["mnt_round_usd_bn"] * 1e3 * V["egp_usd"] * V["mnt_stake_post2nd"]    # after second closing dilution to 41.61%

# ---------------------------------------------------------------------------
# 8) SOTP + lenses + synthesis
# ---------------------------------------------------------------------------
HOLDCO_DISC = 0.10
def sotp(auto, capv, mnt):
    total = auto + capv + mnt + V["other_assoc_book"]
    return total, total * (1 - HOLDCO_DISC)

sotp_book_total, sotp_book = sotp(auto_eq, cap_val["base"], mnt_book)
sotp_round_total, sotp_round = sotp(auto_eq, cap_val["base"], mnt_round_now)
sotp_bear_total, sotp_bear = sotp(max(auto_eq * 0.6, 0.0), cap_val["bear"], mnt_book)
sotp_bull_total, sotp_bull = sotp(auto_eq * 1.4, cap_val["bull"], mnt_round_post * 1.25)  # bull: round mark grows 25% by next mark

ps = lambda x: x / V["shares_mn"]
sotp_ps = {"bear": ps(sotp_bear), "base_book": ps(sotp_book), "base_round": ps(sotp_round),
           "bull": ps(sotp_bull), "prediscount_base_round": ps(sotp_round_total)}

# relative lens: forward P/E band on BLENDED FY26E/FY27E parent EPS. FY27 alone
# embeds the full ETR normalization (40%->30%) in one step; the blend keeps the
# lens from leaning on a single execution-dependent tax-year jump.
PE_BAND = (5.0, 7.0, 9.0)   # EGX diversified/auto-financials forward band under Ke ~28%
eps_fwd = (eps[2026] + eps[2027]) / 2
rel = {k: m * eps_fwd for k, m in zip(("bear", "base", "bull"), PE_BAND)}

# normalized-earnings-power lens: mid-cycle ROE on parent book
book_ps = 28788.713 / V["shares_mn"]         # FY25 parent equity as originally reported
NORM_ROE, KE_G = 0.15, (wacc.ke_cds, 0.10)   # mid-cycle ROE; Ke_cds and long-run g
norm_eps = NORM_ROE * book_ps
norm_pe = (1 - KE_G[1] / NORM_ROE) / (KE_G[0] - KE_G[1])
norm = {"base": norm_eps * norm_pe}
norm["bear"], norm["bull"] = norm["base"] * 0.75, norm["base"] * 1.30

prediscount = {"bear": ps(sotp_book_total), "base": ps(sotp_round_total), "full": ps(sotp_bull_total)}

# full SOTP reconciliation by scenario column (presentation block for the report:
# legs -> sum -> per share -> minus holding discount -> total; same formulas as above)
def recon(auto, capv, mntv):
    tot = auto + capv + mntv + V["other_assoc_book"]
    return {"auto": auto, "cap": capv, "mnt": mntv, "other": V["other_assoc_book"],
            "sum": tot, "sum_ps": ps(tot), "discount": -HOLDCO_DISC * tot,
            "total": tot * (1 - HOLDCO_DISC), "total_ps": ps(tot * (1 - HOLDCO_DISC))}
sotp_recon = {
    "bear": recon(max(auto_eq * 0.6, 0.0), cap_val["bear"], mnt_book),
    "base_book": recon(auto_eq, cap_val["base"], mnt_book),
    "base_round": recon(auto_eq, cap_val["base"], mnt_round_now),
    "full": recon(auto_eq * 1.4, cap_val["bull"], mnt_round_post * 1.25),
}

# prior-edition comparatives — READ from the delivered study's committed numbers
# file (numeric traceability: the report builder types no numeral)
with open(os.path.join(HERE, "..", "study_numbers.json")) as _f:
    _prev = json.load(_f)
prior_edition = {
    "date": "2026-07-08 (amended 09-Jul-2026)",
    "rf_observed": _prev["dcf"]["wacc_build"]["rf"],
    "ke_cds": _prev["dcf"]["wacc_build"]["ke_cds"],
    "wacc_cds": _prev["dcf"]["wacc_build"]["wacc_cds"],
    "wacc_rating": _prev["dcf"]["wacc_build"]["wacc_rating"],
    "beta": _prev["dcf"]["wacc_build"]["beta"],
    "fair": {"bear": _prev["lenses"]["central"]["bear"],
             "base": _prev["lenses"]["central"]["base"],
             "full": _prev["lenses"]["central"]["bull"]},
    "cap_val": _prev["sotp"]["cap_val"],
    "mnt_stake": _prev["sotp"]["mnt_halan_stake"],
    "mnt_round_usd_bn": _prev["sotp"]["mnt_halan_round_usd"] / 1e3,
    "spot": _prev["spot"],
}

# synthesis (continuity weights from the delivered study)
W = {"sotp": 0.40, "prediscount": 0.15, "relative": 0.20, "normalized": 0.25}
central = {
    "bear": W["sotp"] * sotp_ps["bear"] + W["prediscount"] * ps(sotp_book_total)
            + W["relative"] * rel["bear"] + W["normalized"] * norm["bear"],
    "base": W["sotp"] * sotp_ps["base_round"] + W["prediscount"] * sotp_ps["prediscount_base_round"]
            + W["relative"] * rel["base"] + W["normalized"] * norm["base"],
    "full": W["sotp"] * sotp_ps["bull"] + W["prediscount"] * ps(sotp_bull_total)
            + W["relative"] * rel["bull"] + W["normalized"] * norm["bull"],
}

# USD cross-check (v2 reminder for high-inflation EM)
usd_check = {
    "mktcap_usd_mn": MV_EQUITY / V["egp_usd"],
    "mnt_stake_usd_mn": V["mnt_round_usd_bn"] * 1e3 * V["mnt_stake_current"],
    "note": "at the June-2026 round mark the MNT stake alone is ~USD 601mn against a "
            "~USD 637mn market cap; the USD lens sits closer to the SOTP round-mark "
            "framing than to the blended central value",
}

# years 3-5 published as ranges (training record §5 — empirical error quantiles)
RANGE_MULT = {2028: (0.61, 1.40), 2029: (0.38, 1.30), 2030: (0.41, 1.12)}
rev_ranges = {y: (rev[y] * lo, rev[y], rev[y] * hi) for y, (lo, hi) in RANGE_MULT.items()}

usd_check["fair_base_usd_mn"] = central["base"] * V["shares_mn"] / V["egp_usd"]

# ---------------------------------------------------------------------------
# 9) SIGCM attestation (the record above is the evidence)
# ---------------------------------------------------------------------------
sigcm = SIGCMChecklist(
    historicals_official_only=True,      # 15y panel: audited FS / ARs / ERs only (engine/gbco_training/, all tier A)
    forecast_ground_up=True,             # attested on the DriverLine record via assert_ground_up above
    debt_lc_fx_split=True,               # FY25 FS note 29: net FX exposure ~EGP 2.2bn vs 38bn book — EGP book, evidence recorded
    asset_conversion_cycle=True,         # WC modelled from disclosed cycle (training DIO/DSO/DPO study + ER Table 6 path)
    competitors=True,                    # relative lens band cross-checked vs EGX NBFS/auto peers (CCAP et al. as evidence, not references)
    beta_own_history_vs_egx30=True,      # attested by assert_beta_provenance on the fresh own_stock_beta record
    formula_based_model=True,            # this script: drivers -> IS -> legs -> DCF/SOTP; all downstream numbers recompute from INPUTS
    flags_raised_before_issue=True,      # gaps flagged: MNT-BV audit qualification; per-leg unit-cost stacks undisclosed; NP range small-n
)
assert_sigcm(sigcm)

# ---------------------------------------------------------------------------
# 10) OUTPUT
# ---------------------------------------------------------------------------
out = {
    "edition": "GBCO fundamental update 30-08-2026",
    "standard_version_built_to": STANDARD_VERSION,
    "spot": V["spot"], "spot_date": "2026-08-23", "shares_mn": V["shares_mn"],
    "mktcap_egp_mn": MV_EQUITY,
    "beta": {k: beta_rec[k] for k in ("beta", "r2", "se", "n", "ci90", "window_years",
                                      "first_obs", "last_obs", "index_file", "index_asof",
                                      "tier", "conforming") if k in beta_rec} | {"tier": 1},
    "wacc": {"rf_observed": V["rf_observed"], "rf_star_rating": wacc.rf_star_rating,
             "rf_star_cds": wacc.rf_star_cds, "ke_rating": wacc.ke_rating, "ke_cds": wacc.ke_cds,
             "kd_pretax": V["kd_pretax"], "kd_aftertax": wacc.kd_aftertax,
             "we": wacc.we, "wd": wacc.wd,
             "wacc_rating": WACC_R, "wacc_cds": WACC, "primary_basis": "cds",
             "kd_sensitivity_short_tenor": 0.22, "warnings": wacc.warnings,
             "sources": {k: SRC[k] for k in ("rf_observed", "erp_rating", "erp_cds", "kd_pretax")}},
    "forecast": {str(y): {"rev": rev[y], "auto_rev": auto_rev[y], "cap_rev": cap_rev[y],
                          "pc_units": pc_u[y], "lm_units": lm_u[y], "cv_units": cv_u[y],
                          "gp": gp[y], "gpm": gpm[y], "sga": sga[y], "op": op[y],
                          "assoc": assoc[y], "fin_net": fin_net[y], "pbt": pbt[y],
                          "etr": ETR[y], "np_total": np_total[y], "np_parent": np_parent[y],
                          "eps": eps[y]} for y in YRS},
    "rev_ranges_h3_h5": {str(y): {"low": lo, "point": p, "high": hi}
                         for y, (lo, p, hi) in rev_ranges.items()},
    "auto_dcf": {"ebit": auto_ebit, "fcff": auto_fcff, "wacc_used": WACC, "tg": TG,
                 "pv_explicit": pv, "tv": tv, "pv_tv": pv_tv, "ev": auto_ev,
                 "net_debt": V["auto_nd_fy25"], "nci": V["auto_nci_eq_fy25"], "equity": auto_eq,
                 "tv_pct_of_ev": pv_tv / auto_ev if auto_ev else None},
    "gb_capital_leg": {"book_exmnt_parent": cap_book_exmnt, "np_exmnt_fy25": cap_np_exmnt_fy25,
                       "values": cap_val},
    "mnt_leg_dual": {"framing_A_carrying": mnt_book,
                     "framing_B_round_mark_current_stake": mnt_round_now,
                     "framing_B_post_second_closing": mnt_round_post,
                     "stake_current": V["mnt_stake_current"], "stake_post": V["mnt_stake_post2nd"],
                     "round_usd_bn": V["mnt_round_usd_bn"], "egp_usd": V["egp_usd"],
                     "note": "published side by side; base fair value uses framing B (the market's own June-2026 price of the asset, press-reported, tier C); framing A anchors the bear leg; the audit qualification on MNT-BV information is restated wherever this leg is quoted"},
    "sotp": {"auto_eq": auto_eq, "cap_base": cap_val["base"], "other_assoc": V["other_assoc_book"],
             "holdco_discount": HOLDCO_DISC,
             "total_book_framing": sotp_book_total, "total_round_framing": sotp_round_total,
             "ps": sotp_ps},
    "lenses": {"sotp": {"bear": sotp_ps["bear"], "base": sotp_ps["base_round"], "bull": sotp_ps["bull"]},
               "prediscount": prediscount,
               "relative": rel, "normalized": norm, "weights": W},
    "params": {"pe_band": PE_BAND, "cap_pb_band": (0.8, 1.0, 1.4), "holdco_disc": HOLDCO_DISC,
               "tg": TG, "range_mult": RANGE_MULT, "corp_spread_bp": 150,
               "kd_short_tenor_alt": 0.22, "norm_roe": NORM_ROE},
    "sotp_recon": sotp_recon,
    "prior_edition": prior_edition,
    "fair": {"bear": central["bear"], "base": central["base"], "full": central["full"]},
    "usd_cross_check": usd_check,
    "ground_up": ground_up,
    "training_carry_ins": ["years 3-5 revenue as ranges (rev x[0.61..1.40]/[0.38..1.30]/[0.41..1.12])",
                            "associates modelled explicitly (frozen-assoc failure mode)",
                            "capex anchored on FS note 31 committed programme, not a revenue ratio",
                            "SGA_UP_5PCT watch flag applied as range widener, not point bump",
                            "PC volumes market-anchored with stated share, never frozen off a truncated window"],
    "inputs_register": {k: {"value": v[0], "source": v[1], "date": v[2], "tier": v[3]}
                        for k, v in INPUTS.items()},
}
with open(os.path.join(HERE, "update_numbers_30082026.json"), "w") as f:
    json.dump(out, f, indent=1, default=str)

print(wacc.report())
print(f"\nGROUND-UP: {ground_up['lines']} lines, unit share {ground_up['unit_share']:.0%}, "
      f"levels {ground_up['share_by_level']}")
print(f"\nFY26E rev {rev[2026]:,.0f} | FY27E {rev[2027]:,.0f} | FY30E {rev[2030]:,.0f}  ({EGP})")
print(f"FY26E EPS {eps[2026]:.2f} | FY27E {eps[2027]:.2f} | FY28E {eps[2028]:.2f}")
print(f"auto leg: EV {auto_ev:,.0f} → equity {auto_eq:,.0f} (TV share {pv_tv/auto_ev:.0%})")
print(f"GB Capital ex-MNT book {cap_book_exmnt:,.0f}; MNT dual: A {mnt_book:,.0f} / B {mnt_round_now:,.0f}")
print(f"SOTP/share: bear {sotp_ps['bear']:.2f} | base(book) {ps(sotp_book):.2f} | "
      f"base(round) {sotp_ps['base_round']:.2f} | bull {sotp_ps['bull']:.2f}")
print(f"lenses base: rel {rel['base']:.2f} | norm {norm['base']:.2f}")
print(f"\nFAIR VALUE (EGP/share): bear {central['bear']:.2f} | base {central['base']:.2f} | full {central['full']:.2f}")
print(f"vs spot {V['spot']} ({V['spot']and (central['base']/V['spot']-1):+.0%} to base)")
