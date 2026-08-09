"""EGCH — the study's INPUT REGISTER.

Every input the study uses, carrying four fields: value, source, date, layer.
Validated by assertion here, consumed by compute.py, and printed in full in the
standalone bibliography document. No financial numeral is typed into any builder:
the builders read study_numbers.json, which compute.py writes from this register.

Layers
  L1 PRIMARY_FILING    the company's own audited or reviewed statements
  L2 PRIMARY_MARKET    exchange, sovereign and commodity quotes
  L3 OFFICIAL_EXTERNAL regulators, central bank, government decisions
  L4 INDUSTRY_CONTEXT  industry and sector research (never a source for the
                       subject's own reported numbers)
  L5 CONSTRUCTED       derived in this study from L1-L4 inputs, with the
                       construction stated in the source field
"""
import json, os
from dataclasses import dataclass, field, asdict

HERE = os.path.dirname(os.path.abspath(__file__))
LAYERS = {"L1": "Primary filing — the company's own statements",
          "L2": "Primary market data",
          "L3": "Official external (regulator, central bank, government)",
          "L4": "Industry and sector context",
          "L5": "Constructed in this study"}

REG = {}


def I(key, value, unit, source, date, layer, note=""):
    assert key not in REG, f"duplicate input key {key}"
    assert layer in LAYERS, f"unknown layer {layer} on {key}"
    assert source and source.strip(), f"{key} has no source"
    assert date and date.strip(), f"{key} has no date"
    assert value is not None, f"{key} has no value"
    REG[key] = dict(key=key, value=value, unit=unit, source=source, date=date,
                    layer=layer, note=note)
    return value


FS25 = "Audited financial statements, year ended 30 June 2025 (Central Auditing Organization, report dated 23 September 2025)"
FS24 = "Audited financial statements, year ended 30 June 2024 (Central Auditing Organization, report dated 23 October 2024)"
FS23 = "Audited financial statements, year ended 30 June 2023 (Central Auditing Organization with PKF Rashed Badr & Co, report dated 8 October 2023)"
Q1 = "Interim statements, three months ended 30 September 2025, limited review dated 13 November 2025"
H1F = "Interim statements, six months ended 31 December 2025, limited review dated 10 February 2026"
M9 = "Interim statements, nine months ended 31 March 2026, limited review dated 20 May 2026"
CPF = "Country risk premium workbook, original file, Egypt row"

# ===================================================== L1 — REPORTED HISTORY ==
# Income statement, EGP million
for yr, tag, src, dt in [("FY2021/22", "22", FS23, "2023-10-08"),
                         ("FY2022/23", "23", FS23, "2023-10-08"),
                         ("FY2023/24", "24", FS24, "2024-10-23"),
                         ("FY2024/25", "25", FS25, "2025-09-24")]:
    pass

I("is_revenue_FY2122", 4440.701, "EGP m", FS23 + ", comparative column", "2023-10-08", "L1")
I("is_cogs_FY2122", 2322.989, "EGP m", FS23 + ", comparative column", "2023-10-08", "L1")
I("is_selling_FY2122", 272.810, "EGP m", FS23 + ", comparative column", "2023-10-08", "L1")
I("is_admin_FY2122", 196.357, "EGP m", FS23 + ", comparative column", "2023-10-08", "L1")
I("is_net_FY2122", 651.486, "EGP m", FS23 + ", comparative column", "2023-10-08", "L1")

I("is_revenue_FY2223", 6612.226, "EGP m", FS23 + ", income statement", "2023-10-08", "L1")
I("is_cogs_FY2223", 3574.483, "EGP m", FS23 + ", income statement", "2023-10-08", "L1")
I("is_selling_FY2223", 473.720, "EGP m", FS23 + ", income statement", "2023-10-08", "L1")
I("is_admin_FY2223", 188.851, "EGP m", FS23 + ", income statement", "2023-10-08", "L1")
I("is_net_FY2223", 1150.767, "EGP m", FS23 + ", income statement", "2023-10-08", "L1")
I("cogs_dep_FY2223", 627.213, "EGP m", FS23 + ", note 21 cost of sales", "2023-10-08", "L1")

I("is_revenue_FY2324", 6532.126, "EGP m", FS24 + ", income statement", "2024-10-23", "L1")
I("is_cogs_FY2324", 4395.788, "EGP m", FS24 + ", income statement", "2024-10-23", "L1")
I("is_selling_FY2324", 562.527, "EGP m", FS24 + ", income statement", "2024-10-23", "L1")
I("is_admin_FY2324", 297.887, "EGP m", FS24 + ", income statement", "2024-10-23", "L1")
I("is_net_FY2324", 2537.934, "EGP m", FS24 + ", income statement", "2024-10-23", "L1")
I("cogs_dep_FY2324", 662.634, "EGP m", FS24 + ", note 21 cost of sales", "2024-10-23", "L1")
I("oneoff_reval_FY2324", 2034.573, "EGP m",
  FS24 + ", income statement — gain on revaluation of investment property", "2024-10-23", "L1",
  "One-off. Stripped from every margin and return in this study.")

I("is_revenue_FY2425", 8602.606, "EGP m", FS25 + ", income statement", "2025-09-24", "L1")
I("is_cogs_FY2425", 5300.310, "EGP m", FS25 + ", income statement", "2025-09-24", "L1")
I("is_selling_FY2425", 786.463, "EGP m", FS25 + ", income statement", "2025-09-24", "L1")
I("is_admin_FY2425", 359.624, "EGP m", FS25 + ", income statement", "2025-09-24", "L1")
I("is_net_FY2425", 986.964, "EGP m", FS25 + ", income statement", "2025-09-24", "L1")
I("is_eps_FY2425", 0.4968, "EGP", FS25 + ", income statement", "2025-09-24", "L1")

# Revenue note 20 — the split that anchors the channel build
I("rev_export_FY2425", 6608.752, "EGP m", FS25 + ", note 20 sales", "2025-09-24", "L1")
I("rev_local_FY2425", 1993.850, "EGP m", FS25 + ", note 20 sales", "2025-09-24", "L1")
I("rev_services_FY2425", 0.004430, "EGP m", FS25 + ", note 20 sales", "2025-09-24", "L1")

# Cost of sales note 21
I("cogs_materials_FY2425", 4398.636, "EGP m", FS25 + ", note 21", "2025-09-24", "L1")
I("cogs_wages_FY2425", 212.857, "EGP m", FS25 + ", note 21", "2025-09-24", "L1")
I("cogs_services_FY2425", 62.557, "EGP m", FS25 + ", note 21", "2025-09-24", "L1")
I("cogs_dep_FY2425", 776.471, "EGP m", FS25 + ", note 21", "2025-09-24", "L1")

# Selling note 22
I("sell_freight_FY2425", 610.158, "EGP m", FS25 + ", note 22 freight and commissions", "2025-09-24", "L1")
I("sell_other_FY2425", 176.305, "EGP m",
  FS25 + ", note 22 selling materials, wages and other selling expense", "2025-09-24", "L1")

# Depreciation register note 6 and intangible note 10
I("dep_charge_FY2425", 771.213, "EGP m", FS25 + ", note 6 fixed-asset register", "2025-09-24", "L1")
I("amort_FY2425", 119.378, "EGP m", FS25 + ", note 10 usufruct intangible", "2025-09-24", "L1")
I("dep_rate_kima2_machinery", 0.0395, "per year", FS25 + ", note 5-2 depreciation rates", "2025-09-24", "L1")
I("fx_terminal_wedge", 0.025, "ratio",
  "Steady-state gap between the terminal inflation target and the currency wedge, held "
  "constant in the terminal year", "2026-08-09", "L5")
I("dep_escalation", 0.02, "per year",
  "Escalation on the existing depreciation base, reflecting ordinary additions to the plant "
  "already in service", "2026-08-09", "L5")
I("dep_rate_intangible", 0.0475, "per year", FS25 + ", note 5-2", "2025-09-24", "L1")

# Auditor production and unit-cost table — the ground-up spine
I("prod_urea_FY2425", 513385, "tonnes", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("prod_ammonia_FY2425", 318242, "tonnes", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("prod_an_gran_FY2425", 17887, "tonnes", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("prod_ldan_FY2425", 8171, "tonnes", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("prod_nitric_FY2425", 35590, "tonnes", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("unitcost_urea_FY2425", 7509, "EGP/t", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("unitcost_ammonia_FY2425", 9114, "EGP/t", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("unitcost_an_gran_FY2425", 4076.31, "EGP/t", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("unitcost_ldan_FY2425", 8154.48, "EGP/t", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("unitcost_nitric_FY2425", 610, "EGP/t", FS25 + ", auditor's product cost table", "2025-09-24", "L1")
I("unitcost_urea_FY2324", 9254, "EGP/t", FS25 + ", auditor's table, prior-year column", "2025-09-24", "L1")

# Capacity plates and gas terms — note 28 and the operating contract
I("design_urea_tpd", 1575, "tonnes/day", FS25 + ", note 28 contractual operating benchmark", "2025-09-24", "L1")
I("design_ammonia_tpd", 1200, "tonnes/day", FS25 + ", note 28 contractual operating benchmark", "2025-09-24", "L1")
I("design_ammonia_tpy", 438000, "tonnes/year", FS25 + ", note 28", "2025-09-24", "L1")
I("gas_contract_usd_mmbtu", 5.75, "US$/mmBtu",
  FS25 + ", note 28 contingent liabilities — gas price raised from US$4.50 under the "
  "November 2021 decision", "2025-09-24", "L1")
I("gas_usage_low_m3_t", 1025, "m3/t", FS25 + ", auditor's report on gas consumption", "2025-09-24", "L1")
I("gas_usage_high_m3_t", 1771, "m3/t", FS25 + ", auditor's report on gas consumption", "2025-09-24", "L1")
I("gas_loss_FY2425_m3", 38480270, "m3", FS25 + ", auditor's report", "2025-09-24", "L1")
I("gas_abnormal_loss_FY2425", 249.0, "EGP m", FS25 + ", auditor's report", "2025-09-24", "L1")
I("gas_abnormal_cum", 781.0, "EGP m",
  FS25 + ", auditor's report — cumulative since 1 July 2022", "2025-09-24", "L1")
I("stoppage_cost_FY2425", 164.478, "EGP m", FS25 + ", note 25 other expenses", "2025-09-24", "L1")
I("stoppage_cost_FY2324", 152.742, "EGP m", FS25 + ", note 25 comparative", "2025-09-24", "L1")
I("gas_loss_Q1_m3", 31313235, "m3", Q1 + ", auditor's report", "2025-11-13", "L1")
I("gas_loss_Q1_egp", 251.0, "EGP m", Q1 + ", auditor's report", "2025-11-13", "L1")
I("gas_standard_m3_t", 1200, "m3/t", Q1 + ", auditor's report — the standard rate", "2025-11-13", "L1")
I("gas_august_m3_t", 8492, "m3/t",
  Q1 + ", auditor's report — August 2025 actual, the plant idling and restarting", "2025-11-13", "L1")

# Balance sheet, EGP million
for tag, dt, src, vals in [
    ("FY2223", "2023-10-08", FS23, dict(fixed=11300.438, cwip=56.405, invprop=0.0, fvoci=1855.435,
        intang=1908.612, inventory=1391.802, receivables=798.577, cash=1416.243,
        capital=5932.895, reserves=1316.686, debt_lt=8424.871, debt_holdco=50.266,
        dtl=1469.472, provisions=144.359, payables=1367.845, debt_cur=21.391)),
    ("FY2324", "2024-10-23", FS24, dict(fixed=14144.067, cwip=2535.135, invprop=2034.589, fvoci=2491.189,
        intang=2376.211, inventory=1615.470, receivables=858.390, cash=3103.365,
        capital=9932.895, reserves=4627.209, debt_lt=11226.246, debt_holdco=0.0,
        dtl=1001.464, provisions=432.156, payables=1587.001, debt_cur=354.051)),
    ("FY2425", "2025-09-24", FS25, dict(fixed=13587.193, cwip=3790.155, invprop=2160.620, fvoci=2163.270,
        intang=2256.834, inventory=2399.625, receivables=631.047, cash=3057.028,
        capital=9932.895, reserves=5430.170, debt_lt=11183.315, debt_holdco=596.896,
        dtl=990.863, provisions=309.113, payables=1207.768, debt_cur=397.314)),
    ("M9FY2526", "2026-05-21", M9, dict(fixed=13057.606, cwip=5653.510, invprop=2155.061, fvoci=1382.886,
        intang=2170.500, inventory=3378.160, receivables=1230.232, cash=4606.522,
        capital=9932.895, reserves=6273.191, debt_lt=14386.056, debt_holdco=45.955,
        dtl=961.184, provisions=291.769, payables=1538.968, debt_cur=206.994))]:
    for k, v in vals.items():
        I(f"bs_{k}_{tag}", v, "EGP m", src + ", statement of financial position", dt, "L1")

# Interim income statements
I("is_revenue_Q1", 1184.805, "EGP m", Q1, "2025-11-13", "L1")
I("is_gross_Q1", 389.837, "EGP m", Q1, "2025-11-13", "L1")
I("is_net_Q1", 482.705, "EGP m", Q1, "2025-11-13", "L1")
I("fx_gain_Q1", 357.162, "EGP m", Q1 + ", income statement", "2025-11-13", "L1")
I("is_revenue_H1", 4156.379, "EGP m", H1F, "2026-02-10", "L1")
I("is_gross_H1", 1672.613, "EGP m", H1F, "2026-02-10", "L1")
I("is_net_H1", 1190.045, "EGP m", H1F, "2026-02-10", "L1")
I("is_revenue_9M", 7314.933, "EGP m", M9, "2026-05-21", "L1")
I("is_gross_9M", 3134.979, "EGP m", M9, "2026-05-21", "L1")
I("is_selling_9M", 734.707, "EGP m", M9, "2026-05-21", "L1")
I("is_admin_9M", 273.831, "EGP m", M9, "2026-05-21", "L1")
I("is_net_9M", 531.310, "EGP m", M9, "2026-05-21", "L1")
I("fx_loss_9M", 1071.975, "EGP m", M9 + ", income statement", "2026-05-21", "L1")
I("is_revenue_Q3", 3158.554, "EGP m", M9 + ", derived from the nine-month and six-month columns", "2026-05-21", "L1")
I("gross_margin_Q3", 0.463, "ratio", M9 + ", derived from the nine-month and six-month columns", "2026-05-21", "L1")
I("budget_net_9M", 1021.912, "EGP m", M9 + ", the company's own budget column", "2026-05-21", "L1")

# Debt, capital and ownership
I("kima2_loan_FY2425", 11580.629, "EGP m", FS25 + ", note 18-1 KIMA-2 bank consortium loan", "2025-09-24", "L1")
I("kima2_usd_interest_FY2425", 1338.013, "EGP m", FS25 + ", note 26 finance cost", "2025-09-24", "L1")
I("holdco_drawn_FY2425", 500.0, "EGP m", FS25 + ", note 18-2 holding-company loan", "2025-09-24", "L1")
I("holdco_interest_FY2425", 96.896, "EGP m", FS25 + ", note 26 finance cost", "2025-09-24", "L1")
I("anna_cost_egp", 6422.418, "EGP m",
  FS25 + ", note 18-3 — bank-approved investment cost, agreement of 25 June 2025", "2025-09-24", "L1")
I("anna_cost_usd", 278.385, "US$ m", FS25 + ", note 18-3", "2025-09-24", "L1")
I("anna_loan_egp", 5930.701, "EGP m", FS25 + ", note 18-3", "2025-09-24", "L1")
I("anna_loan_usd", 82.945, "US$ m", FS25 + ", note 18-3", "2025-09-24", "L1")
I("anna_cwip_FY2425", 3746.0, "EGP m", FS25 + ", auditor's report on the project", "2025-09-24", "L1")
I("anna_progress_sep2025", 0.129, "ratio",
  Q1 + ", auditor's report — physical progress against a 37% plan", "2025-11-13", "L1")
I("anna_plan_sep2025", 0.37, "ratio", Q1 + ", auditor's report", "2025-11-13", "L1")
I("shares_outstanding", 1986578999, "shares", FS25 + ", note 14 share capital", "2025-09-24", "L1")
I("par_value", 5.0, "EGP", FS25 + ", note 14", "2025-09-24", "L1")
I("paid_capital", 9932.895, "EGP m", FS25 + ", note 14", "2025-09-24", "L1")
I("holding_stake", 0.69825, "ratio", FS25 + ", note 14 shareholder register", "2025-09-24", "L1")
I("free_float", 0.06184, "ratio", FS25 + ", note 14 shareholder register", "2025-09-24", "L1")
I("dividend_FY2324", 0.0, "EGP m", FS24 + ", proposed appropriation statement", "2024-10-23", "L1")
I("dividend_FY2425", 0.0, "EGP m", FS25 + ", proposed appropriation statement", "2025-09-24", "L1")
I("tax_statutory", 0.225, "ratio", FS25 + ", note 5-16 income tax", "2025-09-24", "L1")
I("export_price_FY2425_usd", 385.0, "US$/t",
  FS25 + ", auditor's report on the Damietta urea stock — average export selling price for the year",
  "2025-09-24", "L1")
I("export_levy_charged_FY2425", 437.5, "EGP m",
  FS25 + ", auditor's report — levy on the 175kt quota shortfall", "2025-09-24", "L1")
I("quota_required_14m", 322000, "tonnes", FS25 + ", auditor's report", "2025-09-24", "L1")
I("quota_delivered_14m", 147000, "tonnes", FS25 + ", auditor's report", "2025-09-24", "L1")

# ===================================================== L2 — MARKET DATA =======
I("spot_price", 13.98, "EGP", "Exchange close, from the study's own price library", "2026-08-06", "L2")
I("rf_observed", 0.2300, "ratio", "Egypt ten-year government bond yield, market quote", "2026-08-06", "L2")
I("sovereign_bond_coupon", 0.23098, "ratio",
  "New EGP 120.9bn treasury bond maturing 21 May 2029, listed coupon — corroborates the yield above",
  "2026-08-06", "L2")
I("usd_egp_spot", 49.79, "EGP/US$", "Market quote", "2026-08-07", "L2")
I("urea_fob_egypt", 545.0, "US$/t",
  "Listed granular urea free-on-board Egypt futures contract, front-month settle", "2026-08-07", "L2")
I("erp_rating", 0.13937694320020103, "ratio", CPF + ", rating basis total equity risk premium", "2026-01-01", "L2")
I("erp_cds", 0.09424719428808419, "ratio", CPF + ", CDS basis total equity risk premium", "2026-01-01", "L2")
I("sov_spread_rating", 0.06372478453347744, "ratio", CPF + ", adjusted default spread", "2026-01-01", "L2")
I("sov_spread_cds", 0.0341, "ratio", CPF + ", ten-year CDS spread", "2026-01-01", "L2")
I("mature_market_erp", 0.0423, "ratio", CPF + ", mature-market equity risk premium", "2026-01-01", "L2")
I("moodys_rating", "Caa1", "rating", CPF + ", sovereign rating", "2026-01-01", "L2")

# ===================================================== L3 — OFFICIAL EXTERNAL =
I("cpi_latest", 0.143, "ratio", "Egyptian headline urban consumer price inflation, official statistics",
  "2026-06-30", "L3")
I("policy_rate", 0.1950, "ratio", "Central bank main operation rate, corridor 19.00/20.00", "2026-07-09", "L3")
I("cbe_inflation_target", 0.070, "ratio", "Central bank published medium-term inflation target", "2026-07-09", "L3")
I("quota_domestic_share_2021", 0.55, "ratio",
  "Cabinet decision 170 of 24 November 2021 — share of output to the subsidised system", "2021-11-24", "L3")
I("quota_free_local_2021", 0.10, "ratio", "Cabinet decision 170 of 24 November 2021", "2021-11-24", "L3")
I("export_levy_egp_t", 2500.0, "EGP/t",
  "Trade and industry ministry decree 241 of 2021 — levy on the quota shortfall", "2021-06-03", "L3")
I("export_duty_2026", 0.10, "ratio",
  "2026 replacement of the shortfall levy with an ad-valorem duty tied to the global price",
  "2026-01-01", "L3")
I("subsidised_price", 6000.0, "EGP/t", "Cooperative supply price for subsidised fertilizer", "2025-09-08", "L3")
I("quota_revision_sep2025", 0.53, "ratio",
  "Cabinet decision of 8 September 2025 — industry export share after the revision", "2025-09-08", "L3")

# ===================================================== L4 — INDUSTRY CONTEXT ==
I("egypt_urea_capacity", 7250, "kt/year",
  "Industry analysis of Egyptian nitrogen capacity across the named producers", "2026-03-25", "L4")
I("peer_abuqir_capacity", 2000, "kt/year", "Industry capacity survey", "2026-03-25", "L4")
I("peer_mopco_capacity", 1800, "kt/year", "Industry capacity survey", "2026-03-25", "L4")
I("peer_ncic_capacity", 1300, "kt/year", "Industry capacity survey", "2026-03-25", "L4")
I("mideast_seaborne_share", 0.35, "ratio",
  "Commodity research on Middle East share of seaborne ammonia and urea trade", "2026-03-01", "L4")
I("greenfield_capex_usd_t_low", 550.0, "US$/annual t",
  "Industry build-cost range for a urea line with its own ammonia unit", "2026-03-25", "L4")
I("greenfield_capex_usd_t_high", 700.0, "US$/annual t", "Industry build-cost range", "2026-03-25", "L4")
I("egx_industrial_ev_ebitda_low", 3.0, "x", "Observed Egyptian industrial transaction and trading range",
  "2026-08-06", "L4")
I("egx_industrial_ev_ebitda_high", 6.0, "x", "Observed Egyptian industrial transaction and trading range",
  "2026-08-06", "L4")
I("control_discount_eg_state", 0.40, "ratio",
  "Observed discount at which Egyptian state-controlled industrial assets have changed hands",
  "2026-08-06", "L4")
I("an_price_usd_t", 280.0, "US$/t", "Mid-cycle ammonium nitrate pricing", "2026-08-07", "L4")
I("mid_cycle_urea_usd_t", 400.0, "US$/t",
  "Mid-cycle urea free-on-board Egypt: above the 2015-2020 average of roughly US$250 and well "
  "below the August 2026 quote of US$545", "2026-08-07", "L4")

# ===================================================== L5 — CONSTRUCTED =======
I("design_urea_tpy", 574875, "tonnes/year",
  "Constructed: 1,575 t/day contractual plate times 365 days", "2026-08-08", "L5")
I("ammonia_per_urea", 318242 / 513385, "tonnes",
  "Constructed: FY2024/25 ammonia output divided by FY2024/25 urea output, both from the "
  "auditor's product cost table", "2026-08-08", "L5")
I("export_tonnes_FY2425", 6608.752e6 / (385.0 * 49.0), "tonnes",
  "Constructed: note 20 export revenue divided by the auditor's disclosed average export price "
  "of US$385/t at an average rate of 49.0 — reconciles to 350.3kt", "2026-08-08", "L5")
I("usd_egp_avg_FY2425", 49.00, "EGP/US$",
  "Constructed: the rate that reconciles note 20 export revenue to the disclosed export price "
  "and the implied export tonnage", "2026-08-08", "L5")
I("subsidised_tonnes_FY2425", 126000, "tonnes",
  "Constructed: the auditor's 147kt delivered over fourteen months, annualised", "2026-08-08", "L5")
I("gas_share_of_materials", 0.75, "ratio",
  "Constructed and FLAGGED: the statements give a single materials line and do not split gas "
  "from the rest. Gas is set at three quarters of that line, which implies 1,292 m3 per tonne "
  "of ammonia — inside the auditor's own disclosed 1,025 to 1,771 range. This is the largest "
  "modelled allocation in the study.", "2026-08-08", "L5")
I("gas_realised_usd_mmbtu", 4.68, "US$/mmBtu",
  "Constructed: the company's own Q1 disclosure values 31,313,235 m3 of lost gas at EGP 251m, "
  "or EGP 8.016/m3, which converts to about US$4.68/mmBtu at the prevailing rate — below the "
  "US$5.75 contract price, which the study carries as its downside case", "2026-08-08", "L5")
I("mmbtu_per_m3", 0.03531, "mmBtu/m3", "Standard gross calorific conversion", "2026-08-08", "L5")
I("anna_nameplate_disclosed_tpd", 800.0, "tonnes/day",
  "EPC award for this plant (Tecnimont S.p.A. with Orascom Construction, announced 9 June "
  "2023): 600 t/day nitric acid converted to 800 t/day of fertilizer-grade granulated "
  "ammonium nitrate. FOUND BY EXTERNAL CRITIQUE 9 August 2026 -- the study had said 'no "
  "filing states it' and derived the plate from the ammonia surplus instead.",
  "2023-06-09", "L4")
I("anna_operating_days", 330, "days",
  "Operating days a year for a continuous nitrate line, net of the turnaround the company "
  "takes annually", "2026-08-09", "L5")
I("nh3_per_t_an", 0.43, "tonnes",
  "Ammonia per tonne of ammonium nitrate through the nitric-acid route plus direct "
  "neutralisation", "2026-08-08", "L5")
I("anna_nameplate", (438000 - 574875 * (318242 / 513385)) / 0.43, "tonnes/year",
  "Constructed and FLAGGED: no filing states the new plant's capacity. It is the ammonia "
  "design plate less the draw of urea at ITS design plate, converted at the ratio above.",
  "2026-08-08", "L5")
I("dso", 631.047 / 8602.606 * 365, "days",
  "Constructed: FY2024/25 receivables over revenue", "2026-08-08", "L5")
I("dio", 2399.625 / 5300.310 * 365, "days",
  "Constructed: FY2024/25 inventory over cost of sales", "2026-08-08", "L5")
I("dpo", 1207.768 / 5300.310 * 365, "days",
  "Constructed: FY2024/25 payables over cost of sales", "2026-08-08", "L5")
I("kd_usd_nominal", 0.117, "ratio",
  "Constructed: EGP 1,338.0m of FY2024/25 interest on a mean dollar balance of about US$233m",
  "2026-08-08", "L5")
I("us_inflation_lt", 0.024, "ratio",
  "Long-run United States inflation, the other leg of the purchasing-power wedge",
  "2026-08-09", "L3")
I("expected_depreciation", (1 + 0.050) / (1 + 0.024) - 1, "ratio",
  "Constructed: the central bank's LONG-RUN 5% target against about 2.4% in the United "
  "States, on the same relative-purchasing-power identity the study states. CORRECTED 9 "
  "August 2026: the study previously asserted 4.5% flat while stating a derivation that "
  "produces a different number in every year. The wedge is now computed from the identity "
  "rather than asserted, and the currency path is built from it year by year.",
  "2026-08-09", "L5")
I("kd_local", 0.194, "ratio",
  "Constructed: EGP 96,896,001 of interest on the EGP 500,000,000 holding-company facility drawn "
  "in FY2024/25 — the company's own latest local borrowing", "2026-08-08", "L5")
I("real_rate_lt", 0.035, "ratio",
  "Long-run emerging-market real policy rate, used to build the terminal risk-free rate from "
  "its own components rather than from a spot yield", "2026-08-08", "L5")
I("kd_usd_lt", 0.090, "ratio", "Long-run corporate dollar cost of debt", "2026-08-08", "L5")
I("roc_terminal", 0.18, "ratio",
  "Terminal return on invested capital, which sets the terminal reinvestment rate as growth "
  "divided by return on capital", "2026-08-08", "L5")
I("maint_capex_pct", (80.847245 + 42.470154) / (4440.701 + 6612.226), "ratio",
  "Maintenance capital expenditure as a share of revenue, RE-ANCHORED 9 August 2026 on the "
  "company's OWN pre-project cash-flow statements: EGP 123.3m spent across FY2021/22 and "
  "FY2022/23 on EGP 11,052.9m of revenue. The first issue of this study used a 3.0% "
  "mature-plant standard instead, which is 2.7 times what this company has ever spent to "
  "keep its plant running, and which no disclosure supports. The replacement-rate framing "
  "(gross fixed assets at the disclosed 3.95% machinery rate, 6.11% of revenue) is carried "
  "as the published alternative and as the downside case.", "2026-08-09", "L5")
I("anna_cash_margin", 0.32, "ratio",
  "Conversion margin on ammonium nitrate over its own ammonia feedstock", "2026-08-08", "L5")
I("local_free_parity", 0.90, "ratio",
  "Local free-market urea clears at about 90% of export parity, implied by the FY2024/25 note-20 "
  "local revenue net of the subsidised and nitrate legs", "2026-08-08", "L5")

# The project path is DERIVED, not typed: it opens at the company's own observed run rate
# and its final year is whatever is left of the approved cost. Written this way, the path
# completes the programme by construction — it cannot quietly under- or over-spend it.
_RUN_RATE = 1949.134461 * 4 / 3
_REMAINING = 6422.418 + 278.385 * 50.0 - 5653.51

# Forward paths — each a driver, each dated to the day it was set
for k, vals, unit, src in [
    ("urea_util", [0.913, 0.922, 0.930, 0.939, 0.948], "ratio",
     "Utilisation path. Audited output ran 586.4kt in FY2022/23 (2% above plate), 521.9kt in "
     "FY2023/24 and 513.4kt in FY2024/25; the path never returns to plate because the summer "
     "gas curtailment is structural."),
    ("export_usd_path", [530.0, 500.0, 470.0, 450.0, 440.0], "US$/t",
     "Export price path, mean-reverting from the August 2026 quote toward the cash cost of the "
     "marginal gas-based producer."),
    ("export_usd_path_bull", [560.0, 545.0, 530.0, 520.0, 515.0], "US$/t",
     "Upside export price path: urea holds nearer the August 2026 quote."),
    ("usd_egp_path", [51.9, 54.2, 56.7, 59.2, 61.9], "EGP/US$",
     "Currency path at 4.5% depreciation a year from the spot rate — the same wedge used to "
     "carry the dollar debt at local-equivalent cost."),
    ("subsidised_t_path", [155000, 160000, 165000, 170000, 175000], "tonnes",
     "Subsidised delivery path. The company met 147kt of a 322kt requirement in the fourteen "
     "months to August 2025, a 46% compliance rate the forecast does not assume away."),
    ("subsidised_p_path", [7526.0, 8429.0, 9272.0, 10106.0, 10915.0], "EGP/t",
     "Administered subsidised price path from the EGP 6,000 cooperative supply price."),
    ("local_free_path", [40000, 41000, 42000, 43000, 44000], "tonnes",
     "Local free-market volume path from the 37.1kt implied for FY2024/25."),
    ("an_path", [26000, 26000, 26000, 26000, 26000], "tonnes",
     "Nitrate volume path, flat on the FY2024/25 combined granulated and low-density output."),
    ("other_rev_path", [140.0, 152.0, 163.0, 174.0, 186.0], "EGP m",
     "Merchant nitric acid, the ferrosilicon plant's rent and services."),
    ("abnormal_gas_path", [150.0, 120.0, 100.0, 90.0, 80.0], "EGP m",
     "Stoppage and abnormal-gas cost, decaying as supply normalises from the EGP 164.5m charged "
     "in FY2024/25."),
    ("cpi_path", [0.100, 0.085, 0.075, 0.070, 0.070], "ratio",
     "Domestic inflation converging from the June 2026 print on the central bank's target."),
    ("anna_capex_path", [_RUN_RATE, 3100.0, 3300.0, 3200.0,
                         _REMAINING - (_RUN_RATE + 3100.0 + 3300.0 + 3200.0)], "EGP m",
     "Project spending path, RE-ANCHORED 9 August 2026 on the observed run rate. The first "
     "year is the company's own nine-month actual extended to a full year (EGP 1,949.1m x "
     "4/3 = EGP 2,598.8m); the remaining years complete the EGP 14,688m still to spend "
     "against the bank-approved cost. The first issue opened at EGP 3,000m, above anything "
     "the company has actually spent in a year."),
]:
    I(k, vals, unit, src, "2026-08-08", "L5")

I("g_terminal", 0.050, "ratio",
  "Terminal growth set at the central bank's LONGEST-HORIZON published inflation target: 5% "
  "(+/-2) for Q4 2028. CORRECTED 9 August 2026 after external critique: the study previously "
  "used the 7% Q4-2026 target, which expires one quarter after the anchor date, as a "
  "perpetuity anchor -- and then defended it by calling 5% 'below the target', inverting the "
  "central bank's own target structure. A perpetuity takes the longest-horizon target there "
  "is.", "2026-08-09", "L5")
I("anna_util_base", 0.50, "ratio", "Project utilisation in the terminal year, central case",
  "2026-08-08", "L5")
I("anna_util_bull", 0.70, "ratio", "Project utilisation in the terminal year, upside case",
  "2026-08-08", "L5")

I("plant_distance_to_port_km", 1000, "km",
  "Aswan to the Mediterranean export ports — the reason inland freight is a disclosed cost "
  "line of its own", "2026-08-08", "L4")
I("urea_stock_shortfall_t", 1648, "tonnes",
  FS25 + ", auditor's report — shortfall between warehouse records and the physical count "
  "at Damietta", "2025-09-24", "L1")
I("gas_m3_per_t_ammonia_modelled", 1292.0, "m3/t",
  "Constructed and FLAGGED: implied by setting gas at three quarters of the single "
  "disclosed materials line; inside the auditor's own disclosed 1,025-1,771 range",
  "2026-08-08", "L5")
I("local_sack_price_low", 1400.0, "EGP per 50kg",
  "Egyptian press reporting of open-market fertilizer sack prices", "2026-06-30", "L4")
I("local_sack_price_high", 1600.0, "EGP per 50kg",
  "Egyptian press reporting of open-market fertilizer sack prices", "2026-06-30", "L4")
I("stale_listing_share_count", 394042710, "shares",
  "A stale exchange listing document surfaced in search — recorded ONLY as a documented "
  "discrepancy; it predates the March 2024 capital increase and is not used anywhere",
  "2026-08-08", "L4")
I("aggregator_share_count", 197950000, "shares",
  "A widely visible market page, inconsistent with its own market-capitalisation figure by "
  "a factor of ten — recorded ONLY as a documented discrepancy, not used", "2026-08-08", "L4")

# ---- inputs the model reads directly, previously typed inside compute.py -----
# Depth standard 3 (numeric traceability) is not satisfied by a builder that reads a
# numbers file if the numbers file itself types its own literals. Everything below was
# a literal in compute.py and is now sourced here like every other input.
I("prod_urea_FY2223", 586373, "tonnes", FS23 + ", auditor's product cost table",
  "2023-10-08", "L1")
I("prod_urea_FY2324", 521868, "tonnes", FS24 + ", auditor's product cost table",
  "2024-10-23", "L1")
I("amort_FY2223", 92.000, "EGP m", FS23 + ", amortisation of intangible assets",
  "2023-10-08", "L1", "Modelled split of the depreciation and amortisation charge; flagged")
I("amort_FY2324", 110.000, "EGP m", FS24 + ", amortisation of intangible assets",
  "2024-10-23", "L1", "Modelled split of the depreciation and amortisation charge; flagged")
I("an_price_egp_t_FY2425", 20000.0, "EGP/t",
  FS25 + ", note 20 local revenue less the subsidised and free-market urea legs, over the "
  "combined nitrate tonnage", "2025-09-24", "L5")
I("other_rev_FY2425", 30.0, "EGP m",
  FS25 + ", note 20 — merchant nitric acid, plant rent and services", "2025-09-24", "L1")
I("local_free_tonnes_FY2425", 37085, "tonnes",
  "Constructed: note 20 local revenue less the subsidised leg, divided by the implied "
  "free-market price", "2026-08-08", "L5")
I("local_free_price_FY2425", 18485.0, "EGP/t",
  "Constructed: export parity at the FY2024/25 realised price and rate, times the 90% local "
  "clearing ratio", "2026-08-08", "L5")
I("usd_egp_anna_approval", 50.0, "EGP/US$",
  "The rate prevailing when the project cost was approved on 25 June 2025, used to state the "
  "dual-currency approved cost as one figure", "2025-06-25", "L2")
I("anna_winddown_cost", 1000.0, "EGP m",
  "Capital-discipline case only: the cost of stopping the programme in the first forecast "
  "year — contract settlement and site preservation. No filing states it; it is the study's "
  "estimate and is flagged.", "2026-08-08", "L5")
I("q4_runrate_haircut", 0.97, "ratio",
  "The fourth quarter of FY2025/26 is run-rated on the third quarter's revenue with a 3% "
  "haircut for the summer gas curtailment the company discloses every year", "2026-08-08", "L5")
# ---- CAPITAL EXPENDITURE, AS ACTUALLY PAID -----------------------------------
# The cash-flow statement's investing section, line "payments to acquire fixed assets
# (projects under construction)". This is the record that separates what the plant costs
# to KEEP from what the new complex costs to BUILD, and it was not built into the first
# issue of this study — the maintenance driver was set to a house standard instead.
I("capex_paid_FY2122", 80.847245, "EGP m",
  "Audited financial statements, year ended 30 June 2022 (comparative column of the "
  "FY2022/23 statements), cash-flow statement, payments to acquire fixed assets",
  "2023-10-08", "L1")
I("capex_paid_FY2223", 42.470154, "EGP m",
  FS23 + ", cash-flow statement, payments to acquire fixed assets", "2023-10-08", "L1")
I("capex_paid_FY2324", 2396.608259, "EGP m",
  FS25 + ", cash-flow statement comparative column, payments to acquire fixed assets "
  "(projects under construction) — reconciles exactly to the disclosed investing total "
  "with the asset-sale and loan-collection lines", "2025-09-24", "L1")
I("capex_paid_FY2425", 1545.053761, "EGP m",
  FS25 + ", cash-flow statement, payments to acquire fixed assets (projects under "
  "construction)", "2025-09-24", "L1")
I("capex_paid_9M_FY2526", 1949.134461, "EGP m",
  M9 + ", cash-flow statement, payments to acquire fixed assets", "2026-05-20", "L1")
I("capex_run_rate_FY2526E", 1949.134461 * 4 / 3, "EGP m",
  "Constructed: the nine-month actual extended to a full year — the company's own latest "
  "observed project spending rate, and the near-term anchor for the forecast path",
  "2026-08-09", "L5")
I("maint_capex_pct_observed", (80.847245 + 42.470154) / (4440.701 + 6612.226), "ratio",
  "Constructed: the two clean PRE-PROJECT years pooled — EGP 123.3m of capital "
  "expenditure on EGP 11,052.9m of revenue. This is what the plant costs to keep running "
  "when it is not building anything, from the company's own cash-flow statements.",
  "2026-08-09", "L5")
I("maint_capex_pct_replacement", 17022.493 * 0.0395 / 11014.0, "ratio",
  "Constructed: gross fixed assets at the disclosed 3.95% machinery depreciation rate, "
  "over first-forecast-year revenue — replacement-rate maintenance, the upper framing of "
  "the same driver", "2026-08-09", "L5")

I("bs_gross_fixed_M9FY2526", 17022.493, "EGP m",
  M9 + ", note 6 fixed assets at cost", "2026-05-20", "L1")
I("bs_acc_dep_M9FY2526", 3435.300, "EGP m",
  M9 + ", note 6 accumulated depreciation", "2026-05-20", "L1")
I("spot_price_date", "2026-08-06", "date",
  "Egyptian Exchange closing session used as the study's anchor date", "2026-08-06", "L2")
I("dimson_sum_beta", 0.8275754032593131, "ratio",
  "Dimson sum-beta over one lead, the contemporaneous term and two lags of the same weekly "
  "regression — the thin-trading correction, carried as the beta alternative", "2026-08-08", "L5")
I("g_terminal_alt", 0.050, "ratio",
  "The alternative terminal growth rate: two points below the inflation target, which is "
  "negative real maintenance growth", "2026-08-08", "L5")
for k, v, u, s in [
    ("prod_urea_FY2526E", 520000, "tonnes",
     "Nine months reviewed output extended on the fourth-quarter run rate"),
    ("subsidised_t_FY2526E", 150000, "tonnes",
     "Subsidised deliveries for the study year on the revised quota schedule"),
    ("local_free_t_FY2526E", 40000, "tonnes", "Free-market volume for the study year"),
    ("export_usd_FY2526E", 505.0, "US$/t",
     "Study-year export price: the auditor's disclosed first-quarter increase of 43% on the "
     "FY2024/25 realised price, moderated toward the forward curve"),
    ("usd_egp_FY2526E", 49.60, "EGP/US$", "Average rate across the study year"),
    ("subsidised_p_FY2526E", 6720.0, "EGP/t", "Administered price for the study year"),
    ("local_free_p_FY2526E", 22000.0, "EGP/t", "Free-market price for the study year"),
    ("an_t_FY2526E", 26000, "tonnes", "Nitrate output for the study year"),
    ("other_rev_FY2526E", 120.0, "EGP m", "Other revenue for the study year"),
]:
    I(k, v, u, "Constructed for the FY2025/26 bridge year: " + s + ", from the nine-month "
      "reviewed accounts and the disclosed quarterly detail", "2026-08-08", "L5")

# ------------------------------------------------------------------ validate --
def validate():
    bad = []
    for k, r in REG.items():
        for fld in ("value", "source", "date", "layer"):
            if r.get(fld) in (None, "", []):
                bad.append(f"{k}: missing {fld}")
        if r["layer"] not in LAYERS:
            bad.append(f"{k}: unknown layer")
        if len(r["date"]) != 10 or r["date"][4] != "-":
            bad.append(f"{k}: date not ISO ({r['date']})")
    return bad


V = lambda k: REG[k]["value"]

if __name__ == "__main__" or True:
    errs = validate()
    assert not errs, "INPUT REGISTER FAILS FOUR-FIELD VALIDATION:\n  " + "\n  ".join(errs)
    json.dump({"layers": LAYERS, "inputs": REG},
              open(os.path.join(HERE, 'input_register.json'), 'w'), indent=1, default=float)

if __name__ == "__main__":
    from collections import Counter
    c = Counter(r["layer"] for r in REG.values())
    print(f"input register: {len(REG)} inputs, all four-field complete")
    for L in sorted(LAYERS):
        print(f"  {L} {LAYERS[L]:52s} {c[L]:3d}")
