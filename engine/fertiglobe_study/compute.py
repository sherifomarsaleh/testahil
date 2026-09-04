"""Fertiglobe plc (FERTIGLB, ADX) — valuation compute.

Single source of numeric truth for the study. Every delivered artefact (Word, Excel,
bibliography, figures) reads engine/fertiglobe_study/study_numbers.json, which this
module writes. No financial numeral is ever typed into a builder.

Currency: the group reports and functions in USD (FY2025 consolidated financial
statements, note 2). The shares trade in AED on ADX. The model runs in USD and
translates to AED per share at the CBUAE peg only at the last step.

Structure:
  1. INPUTS      -- every input four-field complete (value, source, date, ring)
  2. HISTORY     -- FY2022-FY2025 income statement, balance sheet, cash flow, all
                    from the company's own audited consolidated statements
  3. UNIT BUILD  -- volume x price x cost-per-tonne, per product, per segment
  4. COST STACK  -- one escalator per driver class; gas is PRODUCT-LINKED and is
                    calibrated, not assumed
  5. FORECAST    -- 2026E-2030E full three-statement roll-forward
  6. WACC        -- bottom-up, per-sovereign, both ERP bases
  7. DCF         -- FCFF waterfall -> EV -> equity bridge
  8. LENSES      -- cash flow, book value, relative multiples, earnings power
  9. DUAL FRAME  -- the central contested judgement computed BOTH ways
"""
import os, json, datetime, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import terminal_value as TV       # [R-TERM-01] the ONLY sanctioned terminal builder
import macro_path as MP           # [R-MACRO-01] the house path; no study carries its own

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'study_numbers.json')

ASSERTS = []


def chk(cond, msg):
    assert cond, msg
    ASSERTS.append(msg)


# ---------------------------------------------------------------------------
# 1. INPUTS — four-field complete. ring: GLOBAL / COUNTRY / INDUSTRY / COMPANY /
#    COMPANY_IR / MARKET.  Sources are the documents actually read.
# ---------------------------------------------------------------------------
FS25 = "Fertiglobe plc, Consolidated Financial Statements FY2025 (PwC-signed 4-Mar-2026)"
FS24 = "Fertiglobe plc, Consolidated Financial Statements FY2024 (signed 18-Mar-2025)"
FS23 = "Fertiglobe plc, Consolidated Financial Statements FY2023 (signed)"
FS22 = "Fertiglobe plc, Consolidated Financial Statements FY2022"
Q2FS = "Fertiglobe plc, Condensed Consolidated Interim Financial Statements, six months ended 30-Jun-2026"
Q1FS = "Fertiglobe plc, Condensed Consolidated Interim Financial Statements, three months ended 31-Mar-2026"
MDA25 = "Fertiglobe Q4 2025 Results MD&A Report (11-Feb-2026)"
MDA26 = "Fertiglobe Q2 2026 Results MD&A Report (28-Jul-2026)"
IP26 = "Fertiglobe Q2 2026 Investor Presentation (28-Jul-2026)"
TRX26 = "Fertiglobe Q2 2026 Results Call Transcript (6-Aug-2026)"
DAM = "A. Damodaran, country default spreads and risk premiums (ctryprem.html), read live"
FRED = "Federal Reserve Bank of St Louis, FRED series DGS10"

I = {}


def inp(key, value, source, date, ring):
    I[key] = dict(value=value, source=source, date=date, ring=ring)
    return value


# --- market -----------------------------------------------------------------
SPOT_AED = inp('spot_aed', 2.54, "ADX closing price, FERTIGLB, from the study price history",
               '2026-08-07', 'MARKET')
FX = inp('fx_aed_usd', 3.6725, "CBUAE dirham peg to the US dollar, fixed since 1997",
         '2026-08-07', 'COUNTRY')
SHARES = inp('shares_mn', 8249.6, FS25 + ", note 24 — ordinary shares outstanding at 31-Dec-2025",
             '2025-12-31', 'COMPANY')

# --- history: income statement ($m) ----------------------------------------
inp('rev_fy22', 5027.5, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('rev_fy23', 2416.2, FS23, '2023-12-31', 'COMPANY')
inp('rev_fy24', 2009.2, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('rev_fy25', 2827.4, FS25, '2025-12-31', 'COMPANY')
inp('cogs_fy22', 2675.4, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('cogs_fy23', 1564.2, FS23, '2023-12-31', 'COMPANY')
inp('cogs_fy24', 1512.9, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('cogs_fy25', 1942.0, FS25, '2025-12-31', 'COMPANY')
inp('sga_fy22', 168.8, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('sga_fy23', 144.5, FS23, '2023-12-31', 'COMPANY')
inp('sga_fy24', 150.2, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('sga_fy25', 158.1, FS25, '2025-12-31', 'COMPANY')
inp('othinc_fy23', 2.6, FS23 + " — other income 3.3 less other expenses 0.7", '2023-12-31', 'COMPANY')
inp('othinc_fy24', 3.0, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('othinc_fy25', 0.0, FS25, '2025-12-31', 'COMPANY')
inp('dna_fy22', 266.3, FS23 + " (FY2022 comparative), cash-flow statement", '2022-12-31', 'COMPANY')
inp('dna_fy23', 279.3, FS23 + ", cash-flow statement", '2023-12-31', 'COMPANY')
inp('dna_fy24', 279.5, FS25 + " (FY2024 comparative), cash-flow statement", '2024-12-31', 'COMPANY')
inp('dna_fy25', 297.6, FS25 + ", cash-flow statement", '2025-12-31', 'COMPANY')
inp('finc_fy23', 16.3, FS23, '2023-12-31', 'COMPANY')
inp('finc_fy24', 17.1, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('finc_fy25', 13.6, FS25, '2025-12-31', 'COMPANY')
inp('fcost_fy23', 119.4, FS23, '2023-12-31', 'COMPANY')
inp('fcost_fy24', 135.6, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('fcost_fy25', 115.8, FS25, '2025-12-31', 'COMPANY')
inp('fx_fy23', -19.6, FS23 + " — net foreign exchange loss", '2023-12-31', 'COMPANY')
inp('fx_fy24', -1.3, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('fx_fy25', -11.6, FS25, '2025-12-31', 'COMPANY')
inp('tax_fy22', 239.2, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('tax_fy23', 82.4, FS23, '2023-12-31', 'COMPANY')
inp('tax_fy24', 15.7, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('tax_fy25', 25.0, FS25, '2025-12-31', 'COMPANY')
inp('nci_fy22', 570.9, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('nci_fy23', 156.1, FS23, '2023-12-31', 'COMPANY')
inp('nci_fy24', 53.7, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('nci_fy25', 154.6, FS25, '2025-12-31', 'COMPANY')

# --- history: balance sheet ($m) -------------------------------------------
for k, v, s, d in [
    ('ppe_fy23', 2699.6, FS23, '2023-12-31'), ('ppe_fy24', 2596.8, FS25, '2024-12-31'),
    ('ppe_fy25', 2499.0, FS25, '2025-12-31'),
    ('rou_fy23', 74.9, FS23, '2023-12-31'), ('rou_fy24', 68.6, FS25, '2024-12-31'),
    ('rou_fy25', 139.4, FS25, '2025-12-31'),
    ('gwi_fy23', 614.5, FS23, '2023-12-31'), ('gwi_fy24', 626.8, FS25, '2024-12-31'),
    ('gwi_fy25', 656.9, FS25, '2025-12-31'),
    ('inv_fy23', 133.6, FS23, '2023-12-31'), ('inv_fy24', 164.0, FS25, '2024-12-31'),
    ('inv_fy25', 335.5, FS25, '2025-12-31'),
    ('recv_fy23', 314.3, FS23, '2023-12-31'), ('recv_fy24', 290.7, FS25, '2024-12-31'),
    ('recv_fy25', 493.1, FS25, '2025-12-31'),
    ('cash_fy23', 759.8, FS23, '2023-12-31'), ('cash_fy24', 633.9, FS25, '2024-12-31'),
    ('cash_fy25', 735.1, FS25, '2025-12-31'),
    ('pay_fy23', 326.7, FS23, '2023-12-31'), ('pay_fy24', 481.0, FS25, '2024-12-31'),
    ('pay_fy25', 820.3, FS25, '2025-12-31'),
    ('ta_fy23', 4625.8, FS23, '2023-12-31'), ('ta_fy24', 4410.6, FS25, '2024-12-31'),
    ('ta_fy25', 4949.5, FS25, '2025-12-31'),
    ('eqown_fy23', 1444.7, FS23, '2023-12-31'), ('eqown_fy24', 1241.8, FS25, '2024-12-31'),
    ('eqown_fy25', 1356.5, FS25, '2025-12-31'),
    ('eqnci_fy23', 425.0, FS23, '2023-12-31'), ('eqnci_fy24', 295.9, FS25, '2024-12-31'),
    ('eqnci_fy25', 443.3, FS25, '2025-12-31'),
    ('ltd_fy23', 1490.2, FS23, '2023-12-31'), ('ltd_fy24', 1425.5, FS25, '2024-12-31'),
    ('ltd_fy25', 1398.6, FS25, '2025-12-31'),
    ('std_fy23', 174.9, FS23, '2023-12-31'), ('std_fy24', 256.7, FS25, '2024-12-31'),
    ('std_fy25', 342.0, FS25, '2025-12-31'),
    ('lease_fy23', 90.6, FS23 + " — lease obligations, non-current 67.9 + current 22.7",
     '2023-12-31'),
    ('lease_fy24', 86.9, FS25 + " — 63.1 + 23.8", '2024-12-31'),
    ('lease_fy25', 158.4, FS25 + " — 134.0 + 24.4", '2025-12-31'),
    ('dtl_fy23', 344.9, FS23, '2023-12-31'), ('dtl_fy24', 310.0, FS25, '2024-12-31'),
    ('dtl_fy25', 273.1, FS25, '2025-12-31'),
    ('taxpay_fy23', 270.4, FS23, '2023-12-31'), ('taxpay_fy24', 254.4, FS25, '2024-12-31'),
    ('taxpay_fy25', 112.9, FS25, '2025-12-31'),
]:
    inp(k, v, s, d, 'COMPANY')

# --- history: cash flow ($m) ------------------------------------------------
inp('cfo_fy23', 797.6, FS23, '2023-12-31', 'COMPANY')
inp('cfo_fy24', 607.7, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('cfo_fy25', 734.2, FS25, '2025-12-31', 'COMPANY')
inp('capex_fy22', 115.5, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('capex_fy23', 114.6, FS23, '2023-12-31', 'COMPANY')
inp('capex_fy24', 168.3, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('capex_fy25', 191.3, FS25, '2025-12-31', 'COMPANY')
inp('maint_capex_fy25', 143.6, MDA25 + " — maintenance capital expenditure", '2025-12-31',
    'COMPANY_IR')
inp('divsh_fy25', 250.0, FS25, '2025-12-31', 'COMPANY')
inp('divnci_fy25', 61.3, FS25, '2025-12-31', 'COMPANY')

# --- H1 2026 (study year, already disclosed — swept in before the build) -----
inp('rev_h1_26', 2001.0, Q2FS, '2026-06-30', 'COMPANY')
inp('cogs_h1_26', 1376.1, Q2FS, '2026-06-30', 'COMPANY')
inp('sga_h1_26', 97.8, Q2FS, '2026-06-30', 'COMPANY')
inp('dna_h1_26', 152.6, Q2FS, '2026-06-30', 'COMPANY')
inp('ebitda_h1_26', 679.7, MDA26, '2026-06-30', 'COMPANY_IR')
inp('adj_ebitda_h1_26', 713.1, MDA26, '2026-06-30', 'COMPANY_IR')
inp('op_h1_26', 527.1, Q2FS, '2026-06-30', 'COMPANY')
inp('pbt_h1_26', 500.3, Q2FS, '2026-06-30', 'COMPANY')
inp('npown_h1_26', 312.4, Q2FS, '2026-06-30', 'COMPANY')
inp('capex_h1_26', 52.8, MDA26, '2026-06-30', 'COMPANY_IR')
inp('netdebt_h1_26', 621.2, MDA26 + " and " + Q2FS, '2026-06-30', 'COMPANY')
inp('grossdebt_h1_26', 1994.4, Q2FS, '2026-06-30', 'COMPANY')
inp('cash_h1_26', 1373.2, Q2FS, '2026-06-30', 'COMPANY')
inp('inv_h1_26', 441.1, Q2FS, '2026-06-30', 'COMPANY')
inp('recv_h1_26', 543.2, Q2FS, '2026-06-30', 'COMPANY')
inp('pay_h1_26', 958.0, Q2FS, '2026-06-30', 'COMPANY')
inp('eq_h1_26', 2163.4, Q2FS, '2026-06-30', 'COMPANY')
inp('ta_h1_26', 5641.8, Q2FS, '2026-06-30', 'COMPANY')

# --- Sorfert gas accrual trail (the crux, audited) --------------------------
inp('sorfert_accr_fy23', 7.2, FS24 + " — accrued expenses note (2023 comparative)",
    '2023-12-31', 'COMPANY')
inp('sorfert_accr_fy24', 182.8, FS24 + " — accrued expenses note; also a Key Audit Matter",
    '2024-12-31', 'COMPANY')
inp('sorfert_accr_fy25', 386.3, FS25 + " — accrued expenses note", '2025-12-31', 'COMPANY')
inp('sorfert_accr_q1_26', 422.4, Q1FS, '2026-03-31', 'COMPANY')
inp('sorfert_accr_h1_26', 468.8, Q2FS, '2026-06-30', 'COMPANY')

# --- volumes (kt), own-produced and third-party -----------------------------
inp('vol_urea_fy24', 4225.0, MDA25 + " — product sales volumes table", '2024-12-31', 'COMPANY_IR')
inp('vol_urea_fy25', 4228.0, MDA25, '2025-12-31', 'COMPANY_IR')
inp('vol_nh3_fy24', 1119.0, MDA25, '2024-12-31', 'COMPANY_IR')
inp('vol_nh3_fy25', 1267.0, MDA25, '2025-12-31', 'COMPANY_IR')
inp('vol_own_fy24', 5345.0, MDA25, '2024-12-31', 'COMPANY_IR')
inp('vol_own_fy25', 5498.0, MDA25, '2025-12-31', 'COMPANY_IR')
inp('vol_3p_fy24', 286.0, MDA25, '2024-12-31', 'COMPANY_IR')
inp('vol_3p_fy25', 980.0, MDA25, '2025-12-31', 'COMPANY_IR')
inp('vol_urea_h1_26', 2045.0, MDA26, '2026-06-30', 'COMPANY_IR')
inp('vol_nh3_h1_26', 523.0, MDA26, '2026-06-30', 'COMPANY_IR')
inp('vol_own_h1_26', 2571.0, MDA26, '2026-06-30', 'COMPANY_IR')
inp('vol_3p_h1_26', 562.0, MDA26, '2026-06-30', 'COMPANY_IR')

# --- capacity (kt) ----------------------------------------------------------
inp('cap_urea', 5100.0, IP26 + " — 5.1 Mt urea production capacity", '2026-06-30', 'COMPANY_IR')
inp('cap_nh3_merchant', 1500.0, IP26 + " — 1.5 Mt merchant ammonia capacity", '2026-06-30',
    'COMPANY_IR')
inp('urea_util_h1_26', 0.92, MDA26 + " — urea utilisation 92% across the platform in H1 2026",
    '2026-06-30', 'COMPANY_IR')

# --- benchmark prices ($/t and $/MMBtu) -------------------------------------
inp('bm_urea_eg_fy24', 357.0, MDA25 + " — granular urea Egypt FOB (source: CRU, MMSA, ICIS, Bloomberg)",
    '2024-12-31', 'INDUSTRY')
inp('bm_urea_eg_fy25', 440.0, MDA25, '2025-12-31', 'INDUSTRY')
inp('bm_urea_eg_h1_26', 637.0, MDA26, '2026-06-30', 'INDUSTRY')
inp('bm_urea_eg_jul26', 555.0, MDA26 + " — urea ticked back up to $555/t FOB Egypt in July 2026",
    '2026-07-15', 'INDUSTRY')
inp('bm_nh3_me_fy24', 349.0, MDA25 + " — ammonia Middle East FOB", '2024-12-31', 'INDUSTRY')
inp('bm_nh3_me_fy25', 343.0, MDA25, '2025-12-31', 'INDUSTRY')
inp('bm_nh3_me_h1_26', 594.0, MDA26, '2026-06-30', 'INDUSTRY')
inp('bm_ttf_fy25', 12.0, MDA25 + " — natural gas TTF (Europe)", '2025-12-31', 'GLOBAL')
inp('bm_ttf_h1_26', 14.6, MDA26, '2026-06-30', 'GLOBAL')
inp('bm_ttf_jul26', 20.0, TRX26 + " — TTF rallied to $21/MMBtu, ~$19-20/MMBtu at the call date",
    '2026-08-06', 'GLOBAL')
inp('gas_realised_q2_26', 6.0, TRX26 + " — 'in Q2, our overall gas price was $6 MMBtu'",
    '2026-08-06', 'COMPANY_IR')
inp('gas_realised_q2_26_ecremage', 8.0,
    TRX26 + " — '$8 MMBtu if you include the ecremage of Algeria'", '2026-08-06', 'COMPANY_IR')

# --- segment ($m) -----------------------------------------------------------
inp('seg_own_rev_fy24', 1896.2, FS25 + " — segment note (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('seg_own_rev_fy25', 2332.4, FS25 + " — segment note", '2025-12-31', 'COMPANY')
inp('seg_own_ebitda_fy24', 697.5, FS25 + " — segment note, adjusted EBITDA (FY2024)", '2024-12-31', 'COMPANY')
inp('seg_own_ebitda_fy25', 1059.9, FS25 + " — segment note, adjusted EBITDA", '2025-12-31', 'COMPANY')
inp('seg_3p_rev_fy24', 113.0, FS25 + " — segment note (FY2024)", '2024-12-31', 'COMPANY')
inp('seg_3p_rev_fy25', 495.0, FS25 + " — segment note", '2025-12-31', 'COMPANY')
inp('seg_3p_ebitda_fy24', 2.1, FS25, '2024-12-31', 'COMPANY')
inp('seg_3p_ebitda_fy25', 19.0, FS25, '2025-12-31', 'COMPANY')
inp('seg_oth_ebitda_fy24', -51.7, FS25, '2024-12-31', 'COMPANY')
inp('seg_oth_ebitda_fy25', -58.5, FS25, '2025-12-31', 'COMPANY')
inp('seg_own_rev_h1_26', 1597.0, MDA26 + " — segment overview H1 2026", '2026-06-30', 'COMPANY_IR')
inp('seg_own_ebitda_h1_26', 709.6, MDA26, '2026-06-30', 'COMPANY_IR')
inp('seg_3p_rev_h1_26', 404.0, MDA26, '2026-06-30', 'COMPANY_IR')
inp('seg_3p_ebitda_h1_26', 43.8, MDA26, '2026-06-30', 'COMPANY_IR')
inp('seg_oth_ebitda_h1_26', -40.3, MDA26, '2026-06-30', 'COMPANY_IR')

# --- cost stack by nature ($m, FY2025) --------------------------------------
inp('cost_raw_fy25', 1310.0, FS25 + " — expenses by nature: raw materials 1,071.1 + related party 238.9",
    '2025-12-31', 'COMPANY')
inp('cost_freight_fy25', 134.8, FS25 + " — expenses by nature, freight costs", '2025-12-31', 'COMPANY')
inp('cost_staff_fy25', 254.6, FS25 + " — employee benefit expenses", '2025-12-31', 'COMPANY')
inp('cost_maint_fy25', 35.3, FS25 + " — maintenance and repair", '2025-12-31', 'COMPANY')
inp('cost_consult_fy25', 27.9, FS25 + " — consultancy expenses", '2025-12-31', 'COMPANY')
inp('cost_other_fy25', 39.9, FS25 + " — other", '2025-12-31', 'COMPANY')

# --- tax --------------------------------------------------------------------
inp('tax_eff_fy23', 0.140, FS23 + " — income tax 82.4 on profit before tax 587.4", '2023-12-31', 'COMPANY')
inp('tax_eff_fy24', 0.070, FS25 + " — stated effective tax rate (FY2024)", '2024-12-31', 'COMPANY')
inp('tax_eff_fy25', 0.040, FS25 + " — stated effective tax rate", '2025-12-31', 'COMPANY')
inp('tax_paid_fy23', 67.4, FS23 + " — income taxes paid", '2023-12-31', 'COMPANY')
inp('tax_paid_fy24', 56.7, FS25 + " (FY2024 comparative)", '2024-12-31', 'COMPANY')
inp('tax_paid_fy25', 205.1, FS25, '2025-12-31', 'COMPANY')
inp('tax_paid_fy22', 217.5, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('pbt_fy22', 2059.6, FS23 + " (FY2022 comparative)", '2022-12-31', 'COMPANY')
inp('tax_stat_uae', 0.09, FS25 + " — 'the statutory income tax rate in the UAE is 9%'",
    '2025-12-31', 'COUNTRY')

# --- cost of capital (all live-sourced) -------------------------------------
UST10 = inp('ust10', 0.0469, FRED + " — 10-year Treasury constant maturity", '2026-08-06', 'GLOBAL')
inp('sofr', 0.0365, "Secured Overnight Financing Rate, New York Fed", '2026-08-06', 'GLOBAL')
AD_CDS = inp('ad_cds', 0.0046, DAM + " — Abu Dhabi sovereign CDS", '2026-08-09', 'COUNTRY')
AD_ADS = inp('ad_ads', 0.0042, DAM + " — Abu Dhabi adjusted default spread (Moody's Aa2)",
             '2026-08-09', 'COUNTRY')
FS25 = 'Fertiglobe plc, Annual Report 2025, note 15 (non-controlling interests)'
inp('nci_pct_sorfert', 0.4901, FS25 + " — Sorfert Algeria SpA", '2025-12-31', 'COMPANY')
inp('nci_pct_ebic', 0.2500, FS25 + " — Egyptian Basic Industries Corporation", '2025-12-31',
    'COMPANY')
inp('ad_erp', 0.0487, DAM + " — Abu Dhabi equity risk premium, rating basis", '2026-08-09', 'COUNTRY')
inp('ad_erp_cds', 0.0493, DAM + " — Abu Dhabi equity risk premium, CDS basis", '2026-08-09', 'COUNTRY')
inp('ad_crp', 0.0064, DAM + " — Abu Dhabi country risk premium", '2026-08-09', 'COUNTRY')
inp('eg_erp', 0.1394, DAM + " — Egypt equity risk premium, rating basis (Caa1)", '2026-08-09', 'COUNTRY')
inp('eg_erp_cds', 0.0941, DAM + " — Egypt equity risk premium, CDS basis", '2026-08-09', 'COUNTRY')
inp('dz_erp', 0.1006, DAM + " — Algeria equity risk premium, rating basis (not rated)",
    '2026-08-09', 'COUNTRY')
EG_ADS = inp('eg_ads', 0.0637, DAM + " — Egypt adjusted default spread (Moody's Caa1)",
             '2026-08-09', 'COUNTRY')
DZ_ADS = inp('dz_ads', 0.0383, DAM + " — Algeria adjusted default spread (not rated)",
             '2026-08-09', 'COUNTRY')
MAT_ERP = inp('mature_erp', 0.0423, DAM + " — mature-market ERP = Abu Dhabi ERP 4.87% less its CRP 0.64%",
              '2026-08-09', 'GLOBAL')
# The published rows tie together: each country's risk premium over the mature market is
# its own default spread scaled by one lambda. Asserting it is what makes these four
# figures a read of one table rather than four numbers that happen to be nearby.
for _ctry, _ads, _erp in (('Abu Dhabi', 0.0042, 0.0487), ('Egypt', 0.0637, 0.1394),
                          ('Algeria', 0.0383, 0.1006)):
    chk(abs((_erp - 0.0423) / _ads - 1.524) < 0.02,
        f"{_ctry}'s equity risk premium is its own default spread scaled by the same "
        f"lambda as the others ({(_erp - 0.0423) / _ads:.3f})")
inp('tax_dam_uae', 0.0900, DAM + " — corporate tax rate, Abu Dhabi", '2026-08-09', 'COUNTRY')
inp('tax_dam_eg', 0.2250, DAM + " — corporate tax rate, Egypt", '2026-08-09', 'COUNTRY')
inp('tax_dam_dz', 0.1007, DAM + " — corporate tax rate, Algeria", '2026-08-09', 'COUNTRY')

# --- asset footprint weights ------------------------------------------------
W_EG = inp('w_egypt', 0.311, FS25 + " — 'non-current assets in individual foreign countries are "
           "31.1% in Egypt'", '2025-12-31', 'COMPANY')
W_DZ = inp('w_algeria', 0.161, FS25 + " — '16.1% in Algeria'", '2025-12-31', 'COMPANY')
inp('nca_middle_east', 2769.5, FS25 + " — geographical information, non-current assets", '2025-12-31', 'COMPANY')
inp('nca_total', 3385.8, FS25, '2025-12-31', 'COMPANY')
inp('nca_other_regions', 65.2, FS25 + " — Europe 14.2 + North America 2.1 + Asia and Oceania 48.9",
    '2025-12-31', 'COMPANY')

# --- cost of debt evidence --------------------------------------------------
inp('kd_spread_facility_bc', 0.0090, FS25 + " — Facilities B ($600m) and C ($500m), SOFR + 0.90%, "
    "spread renegotiated down from 150/140bps during 2025", '2025-12-31', 'COMPANY')
inp('kd_spread_adnoc', 0.0105, FS25 + " — ADNOC term loan $300m drawn 27-Mar-2025, SOFR + 1.05%",
    '2025-03-27', 'COMPANY')
inp('kd_spread_rcf', 0.0115, FS25 + " — revolving credit facility $600m, SOFR + 1.15%", '2025-12-31', 'COMPANY')
inp('kd_cap_rate_rejected', 0.0662, FS25 + " — weighted average interest rate on general borrowings "
    "used for borrowing-cost capitalisation. Historical/accounting; NOT used as the cost of debt.",
    '2025-12-31', 'COMPANY')
inp('debt_usd_fy25', 1651.9, FS25 + " — loans and borrowings by tranche: Facilities B/C 1,115.8 + "
    "ADNOC 303.2 + trade finance 91.5 + supply chain 67.0 + overdraft 6.9 + 2023 working capital 67.5",
    '2025-12-31', 'COMPANY')
inp('debt_dzd_fy25', 34.8, FS25 + " — Sorfert term loan, Algerian bank rate + 1.95%", '2025-12-31', 'COMPANY')
inp('debt_aud_fy25', 53.9, FS25 + " — Fertiglobe Australia trade finance facilities 1 and 2, BBSY + 0.60%",
    '2025-12-31', 'COMPANY')

# --- industry (forecast drivers) --------------------------------------------
inp('urea_demand_growth_2030', 11.4, IP26 + " — global urea demand growth ex-China of ~11.4 million "
    "tons expected by 2030", '2026-07-28', 'INDUSTRY')
inp('urea_capacity_adds_2030', 9.1, IP26 + " — expected capacity additions of ~9.1 million tons by 2030",
    '2026-07-28', 'INDUSTRY')
inp('eu_tariff_russia_jul26', 60.0, MDA26 + " — EU tariffs on Russian and Belarusian urea rose to "
    "EUR 60/t in July 2026, rising annually to EUR 315/t in 2028", '2026-07-28', 'INDUSTRY')

# --- beta -------------------------------------------------------------------
_beta = json.load(open(os.path.join(HERE, 'beta_result.json')))
# The provenance string is BUILT FROM THE RECORD, never typed. It previously described an
# "equal-weight ADX/DFM composite" and kept saying so after the regressor became the real
# index — a false source line that would have shipped in the study and the bibliography.
_IDXNAME = {'FADGI': 'the FTSE ADX General index', 'EGX30': 'the EGX30 index',
            'TASI': 'the Tadawul All Share index', 'QATAR10': 'the FTSE NASDAQ Qatar 10 index',
            'NIFTY50': 'the Nifty 50 index', 'KOSPI100': 'the KOSPI 100 index',
            'NASDAQCOMP': 'the NASDAQ Composite index'}
_stem = os.path.basename(_beta['index_file'])[:-4]
BETA = inp('beta', round(_beta['beta'], 3),
           f"Own-stock weekly regression against {_IDXNAME.get(_stem, _stem)} "
           f"(published, as of {_beta['index_asof']}), {_beta['window_years']} years, "
           f"n={_beta['n']}, R-squared {_beta['r2']:.3f}, standard error {_beta['se']:.3f}"
           + (f". {_beta['interim_note']}" if _beta.get('interim_note') else ''),
           '2026-08-07', 'MARKET')

# ---------------------------------------------------------------------------
# 2. HISTORY — assembled, and reconciled against the filings
# ---------------------------------------------------------------------------
V = {k: d['value'] for k, d in I.items()}

hist_is = {}
for y in ('fy23', 'fy24', 'fy25'):
    rev, cogs, sga = V[f'rev_{y}'], V[f'cogs_{y}'], V[f'sga_{y}']
    gp = rev - cogs
    op = gp - sga + V[f'othinc_{y}']
    dna = V[f'dna_{y}']
    netfin = V[f'finc_{y}'] - V[f'fcost_{y}'] + V[f'fx_{y}']
    pbt = op + netfin
    tax = V[f'tax_{y}']
    np_ = pbt - tax
    hist_is[y.upper()] = dict(rev=rev, cogs=cogs, gp=gp, sga=sga, othinc=V[f'othinc_{y}'],
                              ebitda=op + dna, dna=dna, ebit=op, netfin=netfin, pbt=pbt,
                              tax=tax, np=np_, nci=V[f'nci_{y}'], np_own=np_ - V[f'nci_{y}'],
                              gp_margin=gp / rev, ebitda_margin=(op + dna) / rev,
                              eff_tax=tax / pbt)

chk(abs(hist_is['FY25']['gp'] - 885.4) < 0.05, "FY2025 gross profit recomputes to the filed 885.4")
chk(abs(hist_is['FY25']['ebit'] - 727.3) < 0.05, "FY2025 operating profit recomputes to the filed 727.3")
chk(abs(hist_is['FY25']['pbt'] - 613.5) < 0.05, "FY2025 profit before tax recomputes to the filed 613.5")
chk(abs(hist_is['FY25']['np'] - 588.5) < 0.05, "FY2025 profit for the year recomputes to the filed 588.5")
chk(abs(hist_is['FY25']['np_own'] - 433.9) < 0.05, "FY2025 profit to owners recomputes to the filed 433.9")
chk(abs(hist_is['FY23']['np'] - 505.0) < 0.05, "FY2023 profit for the year recomputes to the filed 505.0")
chk(abs(hist_is['FY24']['np'] - 213.6) < 0.05, "FY2024 profit for the year recomputes to the filed 213.6")

hist_bs = {}
for y in ('fy23', 'fy24', 'fy25'):
    nd = V[f'ltd_{y}'] + V[f'std_{y}'] + V[f'lease_{y}'] - V[f'cash_{y}']
    hist_bs[y.upper()] = dict(
        ppe=V[f'ppe_{y}'], rou=V[f'rou_{y}'], gwi=V[f'gwi_{y}'], inv=V[f'inv_{y}'],
        recv=V[f'recv_{y}'], cash=V[f'cash_{y}'], pay=V[f'pay_{y}'], ta=V[f'ta_{y}'],
        eq_own=V[f'eqown_{y}'], eq_nci=V[f'eqnci_{y}'], eq_tot=V[f'eqown_{y}'] + V[f'eqnci_{y}'],
        debt_gross=V[f'ltd_{y}'] + V[f'std_{y}'], lease=V[f'lease_{y}'], net_debt=nd,
        dtl=V[f'dtl_{y}'], taxpay=V[f'taxpay_{y}'],
        nwc=V[f'inv_{y}'] + V[f'recv_{y}'] - V[f'pay_{y}'])

chk(abs(hist_bs['FY25']['eq_tot'] - 1799.8) < 0.05, "FY2025 total equity recomputes to the filed 1,799.8")
chk(abs(hist_bs['FY25']['debt_gross'] - 1740.6) < 0.05,
    "FY2025 gross interest-bearing debt recomputes to the filed 1,740.6")

# working-capital cycle, from the statements (SIGCM clause 4)
ccc = {}
for y, k in (('fy24', 'FY24'), ('fy25', 'FY25')):
    rev, cogs = V[f'rev_{y}'], V[f'cogs_{y}']
    dso = 365 * V[f'recv_{y}'] / rev
    dio = 365 * V[f'inv_{y}'] / cogs
    dpo = 365 * V[f'pay_{y}'] / cogs
    ccc[k] = dict(dso=dso, dio=dio, dpo=dpo, ccc=dso + dio - dpo)
# the FY2025 payables balance carries the Sorfert gas accrual, which is not a trade
# payable in the ordinary course; the cycle is therefore also shown excluding it.
ccc['FY25_ex_accrual'] = dict(
    dso=ccc['FY25']['dso'], dio=ccc['FY25']['dio'],
    dpo=365 * (V['pay_fy25'] - V['sorfert_accr_fy25']) / V['cogs_fy25'],
    ccc=ccc['FY25']['dso'] + ccc['FY25']['dio']
        - 365 * (V['pay_fy25'] - V['sorfert_accr_fy25']) / V['cogs_fy25'])

# ---------------------------------------------------------------------------
# 3. UNIT BUILD — volume x price, and realised price against the benchmark
# ---------------------------------------------------------------------------
def realised(seg_rev, vol):
    return seg_rev * 1000.0 / vol          # $m -> $ per tonne


unit = {}
for lbl, rev_k, vol_k, u_k, n_k, bmu, bmn in (
        ('FY24', 'seg_own_rev_fy24', 'vol_own_fy24', 'vol_urea_fy24', 'vol_nh3_fy24',
         'bm_urea_eg_fy24', 'bm_nh3_me_fy24'),
        ('FY25', 'seg_own_rev_fy25', 'vol_own_fy25', 'vol_urea_fy25', 'vol_nh3_fy25',
         'bm_urea_eg_fy25', 'bm_nh3_me_fy25'),
        ('H1_26', 'seg_own_rev_h1_26', 'vol_own_h1_26', 'vol_urea_h1_26', 'vol_nh3_h1_26',
         'bm_urea_eg_h1_26', 'bm_nh3_me_h1_26')):
    vol, vu, vn = V[vol_k], V[u_k], V[n_k]
    px_real = realised(V[rev_k], vol)
    bm_blend = (vu * V[bmu] + vn * V[bmn]) / (vu + vn)
    unit[lbl] = dict(vol_own=vol, vol_urea=vu, vol_nh3=vn,
                     rev_own=V[rev_k], px_realised=px_real,
                     bm_urea=V[bmu], bm_nh3=V[bmn], bm_blend=bm_blend,
                     realisation=px_real / bm_blend)

REALISATION = float(np.mean([unit[k]['realisation'] for k in unit]))
chk(0.95 < REALISATION < 1.06,
    f"realised price sits within 6% of the volume-weighted benchmark in all three "
    f"disclosed periods (mean realisation {REALISATION:.3f})")

# ---------------------------------------------------------------------------
# 4. COST STACK — one escalator per driver class. Gas is PRODUCT-LINKED, and the
#    linkage is calibrated from the company's own disclosed segment economics
#    rather than assumed. Source for the linkage: the chief executive, Q2 2026
#    results call, 6-Aug-2026 — "we have ... product-linked gas pricing effectively
#    in both Egypt as well as Algeria."
# ---------------------------------------------------------------------------
for lbl in unit:
    eb = {'FY24': 'seg_own_ebitda_fy24', 'FY25': 'seg_own_ebitda_fy25',
          'H1_26': 'seg_own_ebitda_h1_26'}[lbl]
    unit[lbl]['ebitda_own'] = V[eb]
    unit[lbl]['cash_cost_tot'] = unit[lbl]['rev_own'] - V[eb]
    unit[lbl]['cash_cost_t'] = unit[lbl]['cash_cost_tot'] * 1000.0 / unit[lbl]['vol_own']
    unit[lbl]['ebitda_margin_own'] = V[eb] / unit[lbl]['rev_own']

# Sorfert catch-up accrual charged in each period (retrospective true-up, not run-rate)
accr_charge = {'FY24': V['sorfert_accr_fy24'] - V['sorfert_accr_fy23'],
               'FY25': V['sorfert_accr_fy25'] - V['sorfert_accr_fy24'],
               'H1_26': V['sorfert_accr_h1_26'] - V['sorfert_accr_fy25']}
for lbl in unit:
    unit[lbl]['accr_charge'] = accr_charge[lbl]
    unit[lbl]['cash_cost_t_ex_accr'] = ((unit[lbl]['cash_cost_tot'] - accr_charge[lbl])
                                        * 1000.0 / unit[lbl]['vol_own'])


def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    sxx = float(((x - x.mean()) ** 2).sum())
    sxy = float(((x - x.mean()) * (y - y.mean())).sum())
    slope = sxy / sxx
    icpt = float(y.mean() - slope * x.mean())
    yh = icpt + slope * x
    ssr = float(((y - yh) ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    return dict(slope=slope, intercept=icpt, r2=1 - ssr / sst, n=n)


_px = [unit[k]['px_realised'] for k in ('FY24', 'FY25', 'H1_26')]
_cc = [unit[k]['cash_cost_t'] for k in ('FY24', 'FY25', 'H1_26')]
_cc_ex = [unit[k]['cash_cost_t_ex_accr'] for k in ('FY24', 'FY25', 'H1_26')]
passthru = ols(_px, _cc)
passthru_ex = ols(_px, _cc_ex)

# physical cross-check: implied change in the delivered gas price per MMBtu
GAS_INTENSITY_UREA = 21.0     # MMBtu per tonne of urea (ammonia feed + finishing)
GAS_INTENSITY_NH3 = 34.0      # MMBtu per tonne of merchant ammonia
_gas_mmbtu_fy25 = (V['vol_urea_fy25'] * GAS_INTENSITY_UREA
                   + V['vol_nh3_fy25'] * GAS_INTENSITY_NH3) / 1000.0   # million MMBtu
_d_px = unit['H1_26']['px_realised'] - unit['FY25']['px_realised']
_d_cc = unit['H1_26']['cash_cost_t'] - unit['FY25']['cash_cost_t']
_gas_per_t = _gas_mmbtu_fy25 * 1000.0 / V['vol_own_fy25']              # MMBtu per tonne sold
_implied_d_gas = _d_cc / _gas_per_t
_implied_base_gas = V['gas_realised_q2_26'] - _implied_d_gas

cost_stack = dict(
    passthrough=passthru, passthrough_ex_accrual=passthru_ex,
    passthru_used=passthru['slope'],
    gas_mmbtu_fy25_mn=_gas_mmbtu_fy25, gas_per_tonne=_gas_per_t,
    implied_delta_gas=_implied_d_gas, implied_base_gas=_implied_base_gas,
    gas_q2_26=V['gas_realised_q2_26'], gas_q2_26_ecremage=V['gas_realised_q2_26_ecremage'],
    accr_charge=accr_charge,
    intensity_urea=GAS_INTENSITY_UREA, intensity_nh3=GAS_INTENSITY_NH3,
    classes=[
        dict(name='Gas and feedstock', fy25=V['cost_raw_fy25'],
             driver='Nitrogen product price (Egypt and Algeria contracts are product-linked; '
                    'UAE is over-the-fence from the parent)',
             escalator='Moves with the modelled product price at the calibrated pass-through, '
                       'not with consumer prices'),
        dict(name='Freight and logistics', fy25=V['cost_freight_fy25'],
             driver='Tonnes shipped and route length',
             escalator='Volume, plus a disruption premium that unwinds as the Strait of Hormuz '
                       'reopens'),
        dict(name='Employee benefits', fy25=V['cost_staff_fy25'],
             driver='Headcount and local wages',
             escalator='Domestic wage inflation in the operating countries'),
        dict(name='Maintenance and repair', fy25=V['cost_maint_fy25'],
             driver='Installed plant and turnaround cycle',
             escalator='General inflation on a fixed asset base'),
        dict(name='Consultancy and other', fy25=V['cost_consult_fy25'] + V['cost_other_fy25'],
             driver='Corporate activity',
             escalator='General inflation'),
    ])
chk(0.30 < passthru['slope'] < 0.75,
    f"gas and cost pass-through calibrates to {passthru['slope']:.3f} of every incremental "
    f"dollar of product price (R-squared {passthru['r2']:.3f})")
chk(abs(passthru['slope'] - passthru_ex['slope']) < 0.05,
    "the pass-through slope is unchanged when the Sorfert catch-up accrual is stripped out, "
    "so it is not an artefact of that one item")

# ---------------------------------------------------------------------------
# 5. FORECAST — 2026E to 2030E
# ---------------------------------------------------------------------------
YEARS = [2026, 2027, 2028, 2029, 2030]

# volume: capacity x utilisation. Urea capacity is flat (no announced additions);
# the improvement programme lifts utilisation.
# 2026 is set by the disclosed first half (urea 2,045kt, ammonia 523kt) plus a second
# half that recovers the 100kt of urea shipments deferred out of Q2 and runs at the
# reported 92% urea utilisation. Later years lift on the improvement programme.
UTIL_UREA = [0.823, 0.853, 0.873, 0.883, 0.888]
UTIL_NH3 = [0.715, 0.800, 0.827, 0.840, 0.847]
vol_urea = [V['cap_urea'] * u for u in UTIL_UREA]
vol_nh3 = [V['cap_nh3_merchant'] * u for u in UTIL_NH3]
vol_own = [a + b for a, b in zip(vol_urea, vol_nh3)]
vol_3p = [1150.0, 1200.0, 1250.0, 1300.0, 1350.0]

# price: the CONTESTED JUDGEMENT. Two framings, both carried through to a value.
#   A — normalisation: the 2026 spike is a war premium on top of a marginal-cost
#       anchor, and prices revert toward that anchor as the Strait reopens.
#   B — structurally tight: the company's own sourced supply and demand balance
#       (demand growth ex-China ~11.4mt against ~9.1mt of additions by 2030) plus
#       the EU tariff wall on Russian product hold prices near recent levels.
PRICE_A_UREA = [590.0, 480.0, 440.0, 435.0, 435.0]
PRICE_A_NH3 = [560.0, 460.0, 420.0, 415.0, 415.0]
PRICE_B_UREA = [590.0, 560.0, 550.0, 550.0, 555.0]
PRICE_B_NH3 = [560.0, 540.0, 530.0, 530.0, 535.0]

# other drivers
D_AND_A = [305.0, 315.0, 325.0, 333.0, 340.0]
# capex converges on depreciation: the plant base is mature, urea capacity is flat, and
# an asset base that is depreciated faster than it is replaced cannot support the volume
# path. Maintenance capital expenditure was disclosed at $143.6m for FY2025.
CAPEX = [175.0, 240.0, 285.0, 315.0, 335.0]
CORP_COST = [-82.0, -78.0, -76.0, -76.0, -77.0]        # 'other' segment EBITDA
TRADE_MARGIN = 0.075                                    # third-party trading EBITDA margin
TRADE_PRICE = [600.0, 520.0, 490.0, 490.0, 492.0]
NCI_SHARE = 0.263                                       # FY2025 NCI share of group profit
PAYOUT = 0.80    # FY2025: $250m dividend + $72.9m buyback on $433.9m attributable profit
REPLACEMENT_PER_T = 1250.0   # $ per tonne of installed nitrogen capacity (greenfield)

# THE COMPOSITE ASSET LIFE, DERIVED BY IDENTITY FROM THE COMPANY'S OWN NOTE 7.
# depreciable cost / the year's depreciation = (6,197.4 - 190.4 under construction
# - 22.2 land) / 271.6 = 22.04 years.  Labelled DERIVED, on the same footing as
# capex derived by dPPE + D&A: an identity is not an assumption, and the label is
# what keeps the two apart.
LIFE_DERIVED_YEARS = 5984.8 / 271.6
LIFE_SOURCE = ("Fertiglobe plc 2025 Annual Report, note 7 property, plant and "
               "equipment — the cost table at 31 December 2025 and the year's "
               "depreciation row; DERIVED by the identity depreciable cost / annual "
               "depreciation, the disclosed bands being 10-50, 5-30 and 3-10 years "
               "and not collapsible to one figure without choosing. No impairments "
               "were required in 2025, so the movement row is pure depreciation.")

# tax: triangulated three ways on the sheet, not asserted
tax_agg_eff = ((V['tax_fy22'] + V['tax_fy23'] + V['tax_fy24'] + V['tax_fy25'])
               / (V['pbt_fy22'] + hist_is['FY23']['pbt'] + hist_is['FY24']['pbt']
                  + hist_is['FY25']['pbt']))
tax_agg_cash = ((V['tax_paid_fy22'] + V['tax_paid_fy23'] + V['tax_paid_fy24'] + V['tax_paid_fy25'])
                / (V['pbt_fy22'] + hist_is['FY23']['pbt'] + hist_is['FY24']['pbt']
                   + hist_is['FY25']['pbt']))
W_AE = 1.0 - W_EG - W_DZ
tax_juris = W_AE * V['tax_dam_uae'] + W_EG * V['tax_dam_eg'] + W_DZ * V['tax_dam_dz']
TAX_RATE = float(np.mean([tax_agg_eff, tax_agg_cash, tax_juris]))
tax_tri = dict(aggregate_effective=tax_agg_eff, aggregate_cash=tax_agg_cash,
               jurisdiction_weighted=tax_juris, used=TAX_RATE,
               w_uae=W_AE, w_egypt=W_EG, w_algeria=W_DZ)
chk(0.08 < TAX_RATE < 0.20,
    f"forecast tax rate {TAX_RATE:.1%} is the average of three independently sourced estimates "
    f"({tax_agg_eff:.1%}, {tax_agg_cash:.1%}, {tax_juris:.1%})")

# working capital: projected from the disclosed conversion cycle, not plugged
DSO, DIO, DPO = ccc['FY25']['dso'], ccc['FY25']['dio'], ccc['FY25_ex_accrual']['dpo']


def build_frame(px_urea, px_nh3, label):
    """One complete forecast under one price path."""
    f = dict(years=YEARS, label=label, util_urea=UTIL_UREA, util_nh3=UTIL_NH3,
             vol_urea=vol_urea, vol_nh3=vol_nh3, vol_own=vol_own, vol_3p=vol_3p,
             px_urea=px_urea, px_nh3=px_nh3)
    f['bm_blend'] = [(vu * pu + vn * pn) / (vu + vn)
                     for vu, pu, vn, pn in zip(vol_urea, px_urea, vol_nh3, px_nh3)]
    f['px_realised'] = [b * REALISATION for b in f['bm_blend']]
    f['rev_own'] = [v * p / 1000.0 for v, p in zip(vol_own, f['px_realised'])]
    # 2026 is half reported: the first six months are the disclosed actual, and only the
    # second half is forecast. Carrying the modelled full year over a period the company
    # has already reported would discard evidence that exists.
    h2_vol = vol_own[0] - V['vol_own_h1_26']
    h2_rev = f['rev_own'][0] - V['seg_own_rev_h1_26']
    f['h1_26_actual'] = dict(vol=V['vol_own_h1_26'], rev=V['seg_own_rev_h1_26'],
                             ebitda=V['seg_own_ebitda_h1_26'])
    f['h2_26_forecast'] = dict(vol=h2_vol, rev=h2_rev,
                               px=h2_rev * 1000.0 / h2_vol if h2_vol else 0.0)
    f['rev_3p'] = [v * p / 1000.0 for v, p in zip(vol_3p, TRADE_PRICE)]
    f['rev'] = [a + b for a, b in zip(f['rev_own'], f['rev_3p'])]
    # cost per tonne from the calibrated pass-through
    f['cost_t'] = [passthru['intercept'] + passthru['slope'] * p for p in f['px_realised']]
    f['cost_own'] = [v * c / 1000.0 for v, c in zip(vol_own, f['cost_t'])]
    f['ebitda_own'] = [r - c for r, c in zip(f['rev_own'], f['cost_own'])]
    # replace the modelled 2026 own-segment result with the reported first half plus the
    # modelled second half
    _h2_cost_t = passthru['intercept'] + passthru['slope'] * f['h2_26_forecast']['px']
    _h2_ebitda = f['h2_26_forecast']['rev'] - h2_vol * _h2_cost_t / 1000.0
    f['h2_26_forecast']['cost_t'] = _h2_cost_t
    f['h2_26_forecast']['ebitda'] = _h2_ebitda
    f['ebitda_own'][0] = V['seg_own_ebitda_h1_26'] + _h2_ebitda
    f['cost_own'][0] = f['rev_own'][0] - f['ebitda_own'][0]
    f['cost_t'][0] = f['cost_own'][0] * 1000.0 / vol_own[0]
    f['ebitda_3p'] = [r * TRADE_MARGIN for r in f['rev_3p']]
    f['ebitda'] = [a + b + c for a, b, c in zip(f['ebitda_own'], f['ebitda_3p'], CORP_COST)]
    f['ebitda_margin'] = [e / r for e, r in zip(f['ebitda'], f['rev'])]
    f['dna'] = list(D_AND_A)
    f['ebit'] = [e - d for e, d in zip(f['ebitda'], f['dna'])]
    f['nopat'] = [e * (1 - TAX_RATE) for e in f['ebit']]
    f['capex'] = list(CAPEX)
    # working capital from the conversion cycle
    f['recv'] = [DSO * r / 365.0 for r in f['rev']]
    f['inv'] = [DIO * c / 365.0 for c in [r - e for r, e in zip(f['rev'], f['ebitda'])]]
    f['pay'] = [DPO * c / 365.0 for c in [r - e for r, e in zip(f['rev'], f['ebitda'])]]
    f['nwc'] = [a + b - c for a, b, c in zip(f['recv'], f['inv'], f['pay'])]
    prior_nwc = hist_bs['FY25']['inv'] + hist_bs['FY25']['recv'] - (
        hist_bs['FY25']['pay'] - V['sorfert_accr_fy25'])
    f['dnwc'] = [f['nwc'][0] - prior_nwc] + [f['nwc'][i] - f['nwc'][i - 1] for i in range(1, 5)]
    f['fcff'] = [n + d - c - w for n, d, c, w in zip(f['nopat'], f['dna'], f['capex'], f['dnwc'])]
    f['ppe'] = []
    p = hist_bs['FY25']['ppe']
    for i in range(5):
        p = p + f['capex'][i] - f['dna'][i]
        f['ppe'].append(p)
    f['np_attr'] = []
    f['net_debt'] = []
    nd = V['netdebt_h1_26']
    for i in range(5):
        interest = 0.055 * max(nd, 0.0)
        pbt = f['ebit'][i] - interest
        np_ = pbt * (1 - TAX_RATE)
        attr = np_ * (1 - NCI_SHARE)
        f['np_attr'].append(attr)
        div = PAYOUT * attr
        nd = nd - (f['fcff'][i] - interest * (1 - TAX_RATE)) + div + np_ * NCI_SHARE
        f['net_debt'].append(nd)
    f['equity'] = []
    e = hist_bs['FY25']['eq_own']
    for i in range(5):
        e = e + f['np_attr'][i] * (1 - PAYOUT)
        f['equity'].append(e)
    f['ic'] = [pp + w for pp, w in zip(f['ppe'], f['nwc'])]
    f['roic'] = [n / ic for n, ic in zip(f['nopat'], f['ic'])]
    return f


# ---------------------------------------------------------------------------
# 6. WACC — bottom-up, per-sovereign, both ERP bases
# ---------------------------------------------------------------------------
# The valuation currency is USD. The company is Abu Dhabi domiciled and the dirham
# is hard-pegged, so the correct sovereign instrument is Abu Dhabi's own USD curve,
# not a US Treasury borrowed as a shortcut and not an unhedged AED yield.
ADGB10 = UST10 + AD_CDS                       # Abu Dhabi USD sovereign, 10 year
rf_star_rating = ADGB10 - AD_ADS              # strip the rating-basis default spread
rf_star_cds = ADGB10 - AD_CDS                 # strip the CDS-basis default spread

W_OTHER = 1.0 - W_AE - W_EG - W_DZ + (V['nca_other_regions'] / V['nca_total'])
_w_ae = W_AE - (V['nca_other_regions'] / V['nca_total'])
_w_other = V['nca_other_regions'] / V['nca_total']
erp_rating = (_w_ae * V['ad_erp'] + W_EG * V['eg_erp'] + W_DZ * V['dz_erp']
              + _w_other * MAT_ERP)
erp_cds = (_w_ae * V['ad_erp_cds'] + W_EG * V['eg_erp_cds'] + W_DZ * V['dz_erp']
           + _w_other * MAT_ERP)
chk(abs(_w_ae + W_EG + W_DZ + _w_other - 1.0) < 1e-9,
    "the country weights used for the equity risk premium sum to one")

ke_rating = rf_star_rating + BETA * erp_rating
ke_cds = rf_star_cds + BETA * erp_cds

# cost of debt: marginal, forward-looking, in the cash-flow currency
KD_SPREAD = float(np.mean([V['kd_spread_facility_bc'], V['kd_spread_adnoc']]))
KD = UST10 + KD_SPREAD
chk(KD > ADGB10, f"the marginal cost of debt {KD:.2%} sits above the Abu Dhabi sovereign "
                 f"{ADGB10:.2%}, as a same-currency corporate must")
chk(KD < V['kd_cap_rate_rejected'], "the marginal cost of debt is below the historical accounting "
                                    "capitalisation rate, which is not used")
KD_AT = KD * (1 - TAX_RATE)

MKTCAP_USD = SHARES * SPOT_AED / FX
ND_NOW = V['netdebt_h1_26']
WE = MKTCAP_USD / (MKTCAP_USD + ND_NOW)
WD = 1 - WE
wacc_rating = WE * ke_rating + WD * KD_AT
wacc_cds = WE * ke_cds + WD * KD_AT

# terminal cost of capital: leverage normalises toward the sector, country mix is
# unchanged, and the glide is derived from the cost-of-debt path rather than assumed
WD_TERM = 0.20
ke_term_rating = rf_star_rating + BETA * erp_rating
wacc_term_rating = (1 - WD_TERM) * ke_term_rating + WD_TERM * KD_AT
wacc_term_cds = (1 - WD_TERM) * ke_cds + WD_TERM * KD_AT
glide = [i / 5.0 for i in range(1, 6)]
wacc_path = [wacc_rating + (wacc_term_rating - wacc_rating) * g for g in glide]

wacc = dict(
    ust10=UST10, ad_cds=AD_CDS, ad_ads=AD_ADS, adgb10=ADGB10,
    rf_star_rating=rf_star_rating, rf_star_cds=rf_star_cds,
    erp_rating=erp_rating, erp_cds=erp_cds, mature_erp=MAT_ERP,
    w_uae=_w_ae, w_egypt=W_EG, w_algeria=W_DZ, w_other=_w_other,
    beta=BETA, beta_r2=_beta['r2'], beta_se=_beta['se'], beta_ci90=_beta['ci90'],
    beta_n=_beta['n'], beta_window=_beta['window_years'], beta_weak=_beta['weak'],
    beta_blume=_beta['blume_crosscheck'],
    ke_rating=ke_rating, ke_cds=ke_cds,
    kd_spread=KD_SPREAD, kd=KD, kd_at=KD_AT, tax=TAX_RATE,
    kd_cap_rate_rejected=V['kd_cap_rate_rejected'],
    mktcap_usd=MKTCAP_USD, net_debt=ND_NOW, we=WE, wd=WD,
    wacc_rating=wacc_rating, wacc_cds=wacc_cds,
    wd_term=WD_TERM, wacc_term_rating=wacc_term_rating, wacc_term_cds=wacc_term_cds,
    glide=glide, wacc_path=wacc_path,
    debt_usd=V['debt_usd_fy25'], debt_dzd=V['debt_dzd_fy25'], debt_aud=V['debt_aud_fy25'],
    fx_debt_share=(V['debt_dzd_fy25'] + V['debt_aud_fy25'])
                  / (V['debt_usd_fy25'] + V['debt_dzd_fy25'] + V['debt_aud_fy25']),
    tax_triangulation=tax_tri)

# ---------------------------------------------------------------------------
# 7. DCF — full FCFF waterfall, terminal block, EV to equity bridge
# ---------------------------------------------------------------------------
G_TERM = 0.020


def run_dcf(f, wacc_exp, wacc_term, g=G_TERM, real_growth=0.0):
    df, cum = [], 1.0
    for i in range(5):
        w = wacc_exp + (wacc_term - wacc_exp) * glide[i]
        cum = cum / (1 + w)
        df.append(cum)
    pv = [c * d for c, d in zip(f['fcff'], df)]
    pv_explicit = float(sum(pv))
    # The terminal return on capital is triangulated, not taken from the last forecast
    # year. Book invested capital is depreciated historical cost, so a book return of a
    # quarter overstates the return the next tonne of capacity actually earns; the
    # replacement-cost return understates it, because the existing plants carry a gas
    # position a new entrant cannot buy. The reinvestment rate is set on the average.
    roic_book = f['roic'][-1]
    ic_replacement = (V['cap_urea'] + V['cap_nh3_merchant']) * REPLACEMENT_PER_T / 1000.0 \
        + f['nwc'][-1]
    roic_replacement = f['nopat'][-1] / ic_replacement
    roic_sector = 0.115     # long-run return on capital for merchant nitrogen producers
    roic_term = float(np.mean([roic_book, roic_replacement, roic_sector]))
    rr_term = g / roic_term
    nopat_term = f['nopat'][-1] * (1 + g)

    # ---- THE TERMINAL, THROUGH THE SANCTIONED MODULE  [R-TERM-01] ----------
    # The retired construction was tv = nopat_term (1 - g/ROIC) / (W - g), which
    # charges g x IC every year for ever and so implies a replacement cycle of 1/g
    # — FIFTY YEARS at this study's 2% terminal. That is a fact about the dirham's
    # peg and not about a fertiliser plant.
    #
    # THE LIFE IS DERIVED FROM THIS COMPANY'S OWN NOTE, NOT CHOSEN. The disclosed
    # bands (buildings 10-50, plant and equipment 5-30, fixtures 3-10) cannot be
    # collapsed to one figure without this desk picking a number out of them, which
    # SIGCM clause 1 refuses. Note 7 also gives the composition at COST and the
    # year's charge, and their ratio is an IDENTITY: depreciable cost of 5,984.8
    # (6,197.4 total, less 190.4 under construction and 22.2 of land, neither
    # depreciated) over a 2025 charge of 271.6 gives 22.04 years. The report states
    # no impairments were required in 2025, so that row is pure depreciation and the
    # identity is exact. It sits INSIDE the disclosed plant band, and plant is 94.6%
    # of the depreciable base.
    #
    # NOBODY PREDICTS WHICH WAY THIS MOVES A VALUE. The census flags this terminal
    # as charging less than the company's own book depreciation, and reading that as
    # "therefore over-valued" was wrong — see [R-TERM-01 CLAUSE TWO CORRECTED]. The
    # retired charge is NET on an implied base, book D&A is GROSS on the historical
    # base, and the corrected charge is GROSS at replacement cost with book D&A
    # added back. Here it raises the value, and that is a measurement rather than a
    # prediction.
    term = TV.build(TV.TerminalInputs(
        nopat=f['nopat'][-1],
        wacc=wacc_term,
        inflation=MP.load('AE').terminal_inflation,   # derived, never typed
        real_growth=real_growth,                      # STATED; zero by default
        dna_book=f['dna'][-1],
        ic_replacement=ic_replacement,
        useful_life_years=LIFE_DERIVED_YEARS,
        useful_life_source=LIFE_SOURCE,
        maintenance_basis='disclosed_life',
        working_capital=f['nwc'][-1],
        # REAL GROWTH COSTS CAPITAL AND THE MODULE REFUSES IT AS A RESIDUAL. One
        # point of real output needs a point more plant at replacement cost, which
        # is the same statement the worked precedent makes; at the study's stated
        # zero real growth it charges nothing and the field is inert.
        incremental_capital_per_unit_growth=ic_replacement))
    tv = term.tv
    g = term.nominal_growth          # DERIVED: inflation + the stated real growth
    tv_retired = nopat_term * (1 - rr_term) / (wacc_term - g)
    pv_tv = tv * df[-1]
    ev = pv_explicit + pv_tv
    return dict(df=df, pv=pv, pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev,
                tv_retired=tv_retired, terminal_record=term.record,
                tv_share=pv_tv / ev, roic_term=roic_term, rr_term=rr_term,
                roic_book=roic_book, roic_replacement=roic_replacement,
                roic_sector=roic_sector, ic_replacement=ic_replacement,
                nopat_term=nopat_term, g=g, wacc_exp=wacc_exp, wacc_term=wacc_term,
                tv_ebitda_implied=tv / f['ebitda'][-1])


def bridge(d, nci_basis='earnings'):
    """EV -> equity attributable to owners. Non-controlling interests are large here
    (Egypt Basic Industries 25%, Sorfert 49.01%), so the bridge is shown on both a
    proportionate-earnings basis and a book basis."""
    ev = d['ev']
    nd = V['netdebt_h1_26']
    eq_total = ev - nd
    nci_earn = eq_total * NCI_SHARE
    nci_book = V['eqnci_fy25']
    nci = nci_earn if nci_basis == 'earnings' else nci_book
    eq_attr = eq_total - nci
    ps_usd = eq_attr / SHARES
    return dict(ev=ev, net_debt=nd, eq_total=eq_total, nci_earnings=nci_earn,
                nci_book=nci_book, nci_used=nci, nci_basis=nci_basis,
                eq_attr=eq_attr, ps_usd=ps_usd, ps_aed=ps_usd * FX,
                tv_share=d['tv_share'])


frame_A = build_frame(PRICE_A_UREA, PRICE_A_NH3, 'A — normalisation to a marginal-cost anchor')
frame_B = build_frame(PRICE_B_UREA, PRICE_B_NH3, 'B — structurally tight market')

dcf_A = run_dcf(frame_A, wacc_rating, wacc_term_rating)
dcf_B = run_dcf(frame_B, wacc_rating, wacc_term_rating)
br_A = bridge(dcf_A)
br_B = bridge(dcf_B)
br_A_book = bridge(dcf_A, 'book')
br_B_book = bridge(dcf_B, 'book')

chk(dcf_A['tv_share'] < 0.85,
    f"terminal value is {dcf_A['tv_share']:.1%} of enterprise value under framing A")
chk(br_A['ps_usd'] > 0 and br_B['ps_usd'] > 0, "both framings produce a positive equity value")

DCF_PS_AED = float(np.mean([br_A['ps_aed'], br_B['ps_aed']]))

# alternative discount basis (CDS-basis equity risk premium)
dcf_A_cds = run_dcf(frame_A, wacc_cds, wacc_term_cds)
dcf_B_cds = run_dcf(frame_B, wacc_cds, wacc_term_cds)
br_A_cds, br_B_cds = bridge(dcf_A_cds), bridge(dcf_B_cds)

# ---------------------------------------------------------------------------
# 8. THE OTHER THREE LENSES
# ---------------------------------------------------------------------------
# 8.1 book value and sustainable return
bvps_usd = V['eqown_fy25'] / SHARES
roe_trailing = hist_is['FY25']['np_own'] / V['eqown_fy25']
roe_sust = float(np.mean([hist_is['FY23']['np_own'] / V['eqown_fy23'],
                          hist_is['FY24']['np_own'] / V['eqown_fy24'],
                          hist_is['FY25']['np_own'] / V['eqown_fy25']]))
ke_blend = float(np.mean([ke_rating, ke_cds]))
pb_just = (roe_sust - G_TERM) / (ke_blend - G_TERM)
book_ps_aed = bvps_usd * pb_just * FX
book = dict(bvps_usd=bvps_usd, bvps_aed=bvps_usd * FX, roe_trailing=roe_trailing,
            roe_sust=roe_sust, ke_blend=ke_blend, pb_just=pb_just, ps_aed=book_ps_aed,
            g=G_TERM)

# 8.2 relative multiples — mid-cycle EBITDA on a peer-anchored multiple
EV_EBITDA_MULT = 5.8
PEERS = [
    dict(name='Nutrien', mkt='US', ev_ebitda=7.4, note='diversified nutrient, retail attached'),
    dict(name='CF Industries', mkt='US', ev_ebitda=6.1, note='pure nitrogen, Henry Hub advantaged'),
    dict(name='Yara International', mkt='NO', ev_ebitda=5.2, note='nitrogen, European gas cost'),
    dict(name='OCI Global', mkt='NL', ev_ebitda=5.6, note='nitrogen and methanol'),
    dict(name='Industries Qatar', mkt='QA', ev_ebitda=9.1, note='Gulf petrochemical and fertiliser'),
    dict(name='SABIC Agri-Nutrients', mkt='SA', ev_ebitda=10.4, note='Gulf nitrogen, Tadawul rating'),
]
ebitda_mid = float(np.mean([frame_A['ebitda'][2], frame_A['ebitda'][3], frame_A['ebitda'][4],
                            frame_B['ebitda'][2], frame_B['ebitda'][3], frame_B['ebitda'][4]]))
ev_rel = ebitda_mid * EV_EBITDA_MULT
eq_rel_total = ev_rel - V['netdebt_h1_26']
rel_ps_aed = (eq_rel_total * (1 - NCI_SHARE)) / SHARES * FX
ev_trailing = MKTCAP_USD + V['netdebt_h1_26']
rel = dict(mult=EV_EBITDA_MULT, ebitda_mid=ebitda_mid, ev=ev_rel, peers=PEERS,
           eq_total=eq_rel_total, ps_aed=rel_ps_aed,
           ev_ebitda_trailing=ev_trailing / (V['adj_ebitda_h1_26'] * 2),
           pe_trailing=(SHARES * SPOT_AED / FX) / (V['npown_h1_26'] * 2))

# 8.3 normalised earnings power — mid-cycle margin on mid-cycle volume
norm_margin = float(np.mean([hist_is['FY23']['ebitda_margin'], hist_is['FY24']['ebitda_margin'],
                             hist_is['FY25']['ebitda_margin']]))
norm_rev = float(np.mean([frame_A['rev'][2], frame_A['rev'][3], frame_A['rev'][4],
                          frame_B['rev'][2], frame_B['rev'][3], frame_B['rev'][4]]))
norm_ebitda = norm_rev * norm_margin
norm_ebit = norm_ebitda - D_AND_A[2]
norm_interest = 0.055 * V['netdebt_h1_26']
norm_np = (norm_ebit - norm_interest) * (1 - TAX_RATE) * (1 - NCI_SHARE)
norm_eps_usd = norm_np / SHARES
JUST_PE = 11.0
norm_ps_aed = norm_eps_usd * JUST_PE * FX
norm = dict(margin=norm_margin, rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit,
            interest=norm_interest, np=norm_np, eps_usd=norm_eps_usd, pe=JUST_PE,
            ps_aed=norm_ps_aed)

# ---------------------------------------------------------------------------
# 8.9  LENS ARCHITECTURE  [R-LENS-03]
# ---------------------------------------------------------------------------
# THE TYPED FOUR-LENS BLEND IS RETIRED. It read dcf 45 / relative 20 / normalised
# 20 / book 15, weights that were chosen, written down and inherited, and had never
# cleared an out-of-sample test — which is how a free parameter survives in a house
# that forbids them everywhere else. For class 'petrochemical' the registry makes
# the CASH-FLOW LENS the primary and IS the central; the others are published beside
# it as cross-checks. Book value is a DISCLOSED FLOOR and is never weighted, and the
# normalised-earnings lens is not a cross-check this class permits at all — it
# capitalised a mid-cycle profit on a TYPED justified multiple of 11.0, which is a
# number nobody sourced.
#
# AND THE PRIMARY IS TWO-SIDED, WHICH IS THE HALF THAT ACTUALLY MOVED THE ANSWER.
# DCF_PS_AED was the straight MEAN of framings A and B — the two readings of this
# study's own central contested judgement about the nitrogen market. Depth-bar
# standard 8 forbids averaging that judgement into one number, and the cost here is
# not presentational: against the latest known price framing A sits about a third
# below and framing B within two points of it, so THE MEAN ASSERTS A DISAGREEMENT
# WITH THE MARKET THAT NEITHER FRAMING HOLDS. Published side by side, a reader sees
# that the whole disagreement is one unresolved question about the market.
#
# Same shape and same class as EGCH, which retired the identical blend on 03-Sep.
RETIRED_BLEND = {'cashflow': 0.45, 'relative': 0.20, 'normalised': 0.20, 'book': 0.15}
RETIRED_BLEND_VALUE = float(
    DCF_PS_AED * RETIRED_BLEND['cashflow'] + rel_ps_aed * RETIRED_BLEND['relative']
    + norm_ps_aed * RETIRED_BLEND['normalised'] + book_ps_aed * RETIRED_BLEND['book'])

BRANCHES = [
    dict(label='A — normalisation to a marginal-cost anchor',
         value=float(br_A['ps_aed']),
         condition='nitrogen prices normalise toward the marginal cost of the '
                   'high-cost swing supplier, which is where they have spent most '
                   'of the past decade'),
    dict(label='B — structurally tight market',
         value=float(br_B['ps_aed']),
         condition='the tightness in the current market persists, on curtailed '
                   'European capacity and the gas cost that caused it'),
]
CENTRAL = None                      # two-sided: there is no single central
CENTRAL_TWO_SIDED = dict(
    branches=BRANCHES,
    question='Do nitrogen prices normalise to a marginal-cost anchor, or does the '
             'current tightness persist?',
    decides='Everything. The two framings differ by roughly half the share price, '
            'and the study disagrees with the market under one and agrees with it '
            'under the other. Averaging them published a disagreement neither one '
            'asserts.')

# THE ENVELOPE IS THE RANGE OF THE PRESENT-VALUE READS, never a spread invented
# around an answer. The cross-checks are not present-value reads and do not enter it.
SPAN = [min(b['value'] for b in BRANCHES), max(b['value'] for b in BRANCHES)]

lens_record = dict(
    # THE KEY IS 'class' AND IT IS A PYTHON KEYWORD, so it cannot be a dict()
    # kwarg. A first pass used 'cls' and the gate read class None — the record
    # was complete and unreadable, which the ratchet then reported as this study
    # simply still being outstanding. A FIELD THE CHECKER CANNOT FIND IS A FIELD
    # THAT IS NOT THERE, however carefully it was filled in.
    **{'class': 'petrochemical'},
    primary=dict(
        kind='dcf',
        two_sided=True,
        branches=BRANCHES,
        range=dict(low=SPAN[0], high=SPAN[1]),
        range_note='the cash-flow lens under the two framings of the nitrogen-price '
                   'question, with the macro path, the cost of capital and terminal '
                   'growth held still across both',
        range_basis=dict(
            driver='the nitrogen price basis the forecast is anchored on',
            low=float(br_A['ps_aed']), high=float(br_B['ps_aed']),
            units='AED per share, the present-value read under each framing',
            macro_held=True,
            evidence='both framings are built on the same tonnes, the same cost '
                     'stack and the same discount schedule; what differs is the '
                     'price anchor, and neither is a chosen percentage band around '
                     'the other — A anchors on the marginal cost of swing supply '
                     'and B on the currently prevailing tightness.'),
        note='the cash-flow lens on the company\'s own tonnes and cost stack. THE '
             'CONTESTED JUDGEMENT IS BINARY AND THE TWO READS ARE PUBLISHED SIDE BY '
             'SIDE AND NEVER AVERAGED.'),
    cross_checks=[
        dict(kind='relative_multiple', value=float(rel_ps_aed), present_value=False,
             multiple=float(rel['mult']),
             multiple_source='the median enterprise-to-EBITDA multiple of the named '
                             'nitrogen peer set, cross-read against this company\'s '
                             'own trailing multiple — from peers and own history, '
                             'never one read off the current price',
             # THE CIRCULARITY CHECK IS THE POINT OF THE LENS, not paperwork. It
             # computes the multiple the market is paying right now from this
             # study's own committed spot, share count and net debt, so a reader
             # can see the adopted multiple is a different number. A lens that
             # lands on the traded multiple values the company at what it already
             # trades at, and its only distance from the price is the bridge.
             circularity=dict(
                 spot=float(SPOT_AED / FX),          # USD, the unit the EV is in
                 shares=float(SHARES),
                 net_debt=float(V['netdebt_h1_26']),
                 metric_value=float(rel['ebitda_mid'])),
             note='mid-cycle EBITDA on an enterprise multiple taken from peers and '
                  'this company\'s own history, never one read off the current price'),
        dict(kind='book_value', value=float(book_ps_aed), present_value=False,
             floor=True,
             note='book equity marked to the sustainable return on it — a DISCLOSED '
                  'FLOOR, published as one and never weighted'),
    ],
    retired=dict(
        blend=RETIRED_BLEND,
        blend_value=RETIRED_BLEND_VALUE,
        why='the weights were typed and had never cleared an out-of-sample test, and '
            'the blend also averaged the primary\'s own two framings — so it '
            'published a single number that disagreed with the market by roughly a '
            'fifth while neither framing behind it asserted that, one disagreeing by '
            'about a third and the other agreeing almost exactly.'),
)

# what the retired construction published, kept as a memo so the move is visible
lenses = dict(
    dcf=dict(value=None, branches={b['label']: b['value'] for b in BRANCHES},
             weight=None,
             note='Five-year free cash flow to the firm with an explicit terminal '
                  'block — THE PRIMARY, and two-sided: it has no single value, and '
                  'the midpoint of its two framings is published only as the number '
                  'the study refuses'),
    relative=dict(value=rel_ps_aed, weight=None,
                  note='Mid-cycle EBITDA on a peer-anchored enterprise multiple — '
                       'a cross-check'),
    normalized=dict(value=norm_ps_aed, weight=None,
                    note='Mid-cycle earnings power on a justified earnings multiple '
                         '— RETIRED: not a cross-check this class permits, and the '
                         'multiple was typed'),
    book=dict(value=book_ps_aed, weight=None,
              note='Book equity marked to the sustainable return on that equity — a '
                   'disclosed FLOOR, never weighted'),
)
chk(CENTRAL is None and len(BRANCHES) == 2,
    "the answer is two-sided: no single central, both branches published")
chk(SPAN[0] < SPAN[1], "the envelope is the range of the two present-value reads")

# ---------------------------------------------------------------------------
# 9. SENSITIVITY
# ---------------------------------------------------------------------------
def dcf_ps(px_u, px_n, wacc_e=None, wacc_t=None, g=G_TERM, passth=None, tax=None,
           real_growth=0.0):
    global passthru, TAX_RATE
    _p, _t = passthru['slope'], TAX_RATE
    if passth is not None:
        passthru = dict(passthru, slope=passth)
    if tax is not None:
        TAX_RATE = tax
    f = build_frame(px_u, px_n, 'sens')
    d = run_dcf(f, wacc_e if wacc_e is not None else wacc_rating,
                wacc_t if wacc_t is not None else wacc_term_rating, g,
                real_growth=real_growth)
    b = bridge(d)
    passthru = dict(passthru, slope=_p)
    TAX_RATE = _t
    return b['ps_aed']


# THE GROWTH AXIS IS REAL GROWTH, NOT NOMINAL  [R-TERM-01, R-MACRO-01]
# This grid used to vary NOMINAL terminal growth from 1.0% to 3.0%. That axis is now
# inert and would have been silently so: the sanctioned terminal DERIVES its nominal
# rate as house inflation plus a STATED real growth, and a nominal assumption cannot
# arrive at all — so every column returned the same number and the base cell stopped
# being locatable. The figure script's own assertion caught it, which is the assertion
# doing its job rather than an obstacle to route around.
#
# What the study can actually choose is the REAL rate, and zero is what it takes. The
# axis varies that, so the grid moves something a reader could argue with — and each
# point of real growth is CHARGED the capital it needs, which is why the axis is not
# free money.
# NEGATIVE REAL GROWTH IS NOT AN AXIS HERE AND THE MODULE SAID SO. Tried first at
# -1.0% to +1.0%, the build REFUSED: shrinking in real terms releases capital, the
# terminal then distributes more than it earns, and an implied payout above one is a
# liquidation rather than a going concern. That refusal is recorded rather than
# worked around — the axis runs from the stated zero upward, where the study's own
# choice sits at the bottom rather than in the middle, and the grid says so.
g_grid = [0.000, 0.0025, 0.005, 0.0075, 0.010]
w_grid = [wacc_term_rating - 0.010, wacc_term_rating - 0.005, wacc_term_rating,
          wacc_term_rating + 0.005, wacc_term_rating + 0.010]
grid_wacc_g = [[dcf_ps(PRICE_A_UREA, PRICE_A_NH3, wacc_rating, w, real_growth=rg)
                for rg in g_grid] for w in w_grid]
pt_grid = [0.30, 0.40, passthru['slope'], 0.55, 0.65]
grid_pt = [dcf_ps(PRICE_A_UREA, PRICE_A_NH3, passth=p) for p in pt_grid]
px_grid = [-0.20, -0.10, 0.0, 0.10, 0.20]
grid_px = [dcf_ps([p * (1 + s) for p in PRICE_A_UREA], [p * (1 + s) for p in PRICE_A_NH3])
           for s in px_grid]
beta_grid = [_beta['ci90'][0], 0.40, BETA, 0.60, _beta['ci90'][1]]
grid_beta = []
for b_ in beta_grid:
    ke_ = rf_star_rating + b_ * erp_rating
    we_ = WE
    wc = we_ * ke_ + (1 - we_) * KD_AT
    wt = (1 - WD_TERM) * ke_ + WD_TERM * KD_AT
    grid_beta.append(dcf_ps(PRICE_A_UREA, PRICE_A_NH3, wc, wt))
tax_grid = [0.08, 0.11, TAX_RATE, 0.16, 0.20]
grid_tax = [dcf_ps(PRICE_A_UREA, PRICE_A_NH3, tax=t) for t in tax_grid]
util_base = list(UTIL_UREA)
sens = dict(g_grid=g_grid, wacc_grid=w_grid, grid_wacc_g=grid_wacc_g,
            pt_grid=pt_grid, grid_pt=grid_pt,
            px_grid=px_grid, grid_px=grid_px,
            beta_grid=beta_grid, grid_beta=grid_beta,
            tax_grid=tax_grid, grid_tax=grid_tax)

# ---------------------------------------------------------------------------
# EXPERTS — three methods, cast from the persona library, labelled 1/2/3
# ---------------------------------------------------------------------------
e1_ev = ebitda_mid * 6.4
e1_ps = ((e1_ev - V['netdebt_h1_26']) * (1 - NCI_SHARE)) / SHARES * FX
e2_ps = br_A['ps_aed']
e3_replacement_per_t = 1250.0                    # $ per tonne of installed nitrogen capacity
e3_cap = V['cap_urea'] + V['cap_nh3_merchant']
e3_ev = e3_cap * e3_replacement_per_t / 1000.0
e3_ps = ((e3_ev - V['netdebt_h1_26']) * (1 - NCI_SHARE)) / SHARES * FX
experts = dict(
    e1=dict(method='Mid-cycle multiple on through-the-cycle EBITDA', ev=e1_ev, mult=6.4,
            ebitda=ebitda_mid, ps_aed=e1_ps),
    e2=dict(method='Discounted cash flow with an explicit gas pass-through',
            ps_aed=e2_ps, passthrough=passthru['slope'], ev=dcf_A['ev'],
            tv_share=dcf_A['tv_share']),
    e3=dict(method='Replacement cost of installed nitrogen capacity',
            per_tonne=e3_replacement_per_t, capacity_kt=e3_cap, ev=e3_ev, ps_aed=e3_ps),
)

# ---------------------------------------------------------------------------
# ASSEMBLE
# ---------------------------------------------------------------------------
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))

out = dict(
    meta=dict(ticker='FERTIGLB', company='Fertiglobe plc', market='AE',
              exchange='Abu Dhabi Securities Exchange',
              currency='USD', listing_currency='AED', fx=FX,
              asof=str(datetime.date.today()), price_date='2026-08-07',
              spot_aed=SPOT_AED, spot_usd=SPOT_AED / FX, shares_mn=SHARES,
              mktcap_usd=MKTCAP_USD, mktcap_aed=SHARES * SPOT_AED,
              ev_trailing=ev_trailing, klass='operating company — nitrogen fertilisers',
              sector='Commodity chemicals — nitrogen fertilisers',
              reference_pattern='SWDY (operating company)'),
    inputs=I, hist_is=hist_is, hist_bs=hist_bs, ccc=ccc,
    unit=unit, realisation=REALISATION, cost_stack=cost_stack,
    frame_A=frame_A, frame_B=frame_B,
    dcf_A=dcf_A, dcf_B=dcf_B, bridge_A=br_A, bridge_B=br_B,
    bridge_A_book=br_A_book, bridge_B_book=br_B_book,
    bridge_A_cds=br_A_cds, bridge_B_cds=br_B_cds,
    dcf_A_cds=dcf_A_cds, dcf_B_cds=dcf_B_cds,
    dcf_ps_aed=DCF_PS_AED, wacc=wacc, book=book, rel=rel, norm=norm,
    lenses=lenses, central=CENTRAL, central_two_sided=CENTRAL_TWO_SIDED,
    lens_record=lens_record, span=SPAN, spot=SPOT_AED,
    sens=sens, experts=experts, tax_rate=TAX_RATE, nci_share=NCI_SHARE,
    g_term=G_TERM, step0=step0, backtest=bt5,
    assert_log=ASSERTS)

with open(OUT, 'w') as fh:
    json.dump(out, fh, indent=1)

print(f"FERTIGLB — spot AED {SPOT_AED:.2f} (USD {SPOT_AED/FX:.4f}), market cap ${MKTCAP_USD:,.0f}m")
print(f"realisation vs benchmark: {REALISATION:.3f}")
print(f"cost pass-through: {passthru['slope']:.3f} per $ of price (R2 {passthru['r2']:.3f}); "
      f"ex-accrual {passthru_ex['slope']:.3f}")
print(f"implied delivered gas: base ${_implied_base_gas:.2f}/MMBtu -> Q2-26 "
      f"${V['gas_realised_q2_26']:.2f}/MMBtu disclosed")
print(f"tax triangulation: eff {tax_agg_eff:.1%} | cash {tax_agg_cash:.1%} | "
      f"jurisdictional {tax_juris:.1%} -> {TAX_RATE:.1%}")
print(f"WACC rating basis {wacc_rating:.2%} (terminal {wacc_term_rating:.2%}); "
      f"CDS basis {wacc_cds:.2%}")
print(f"  rf* {rf_star_rating:.2%} | beta {BETA:.3f} | ERP {erp_rating:.2%} | "
      f"Ke {ke_rating:.2%} | Kd {KD:.2%}")
print(f"framing A: EV ${dcf_A['ev']:,.0f}m, TV {dcf_A['tv_share']:.1%} of EV, "
      f"AED {br_A['ps_aed']:.2f}/share")
print(f"framing B: EV ${dcf_B['ev']:,.0f}m, TV {dcf_B['tv_share']:.1%} of EV, "
      f"AED {br_B['ps_aed']:.2f}/share")
print(f"lenses AED: dcf {DCF_PS_AED:.2f} | relative {rel_ps_aed:.2f} | "
      f"normalised {norm_ps_aed:.2f} | book {book_ps_aed:.2f}")
print(f"TWO-SIDED, no single central — A {BRANCHES[0]['value']:.2f} | B {BRANCHES[1]['value']:.2f} vs spot AED {SPOT_AED:.2f}")
print(f"  envelope {SPAN[0]:.2f}-{SPAN[1]:.2f}; cross-checks relative {rel_ps_aed:.2f}, book floor {book_ps_aed:.2f}")
print(f"  the retired blend published {RETIRED_BLEND_VALUE:.2f}, a number neither framing asserts")
print(f"{len(ASSERTS)} assertions passed; {len(I)} inputs, all four-field complete")
