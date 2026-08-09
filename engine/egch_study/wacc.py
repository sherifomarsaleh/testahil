"""EGCH — bottom-up WACC under the house v2 cost-of-capital method.

Every input is sourced and dated. The two ERP bases (rating and CDS) are built and
published separately, each with its OWN normalized risk-free rate, because mixing a
CDS-based CRP into a rating-normalized rf double-counts sovereign risk.

Kd is genuinely marginal and genuinely split by currency, which matters more here than
in most Egyptian studies: KIMA's debt book is ~95% US-dollar. The USD tranches are
carried at LOCAL-EQUIVALENT cost (USD coupon + expected EGP depreciation), never at
their raw dollar coupon inside an EGP-nominal WACC.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from wacc_builder import WaccInputs, build_wacc, sensitivity_grid

LIVE = json.load(open(os.path.join(HERE, 'live_data.json')))
BETA = json.load(open(os.path.join(HERE, 'beta_result.json')))
FY25 = json.load(open(os.path.join(HERE, 'extract_fy2425.json')))

dam = LIVE['damodaran_egypt']['value']
SPOT = 13.98                      # EGX close 6-Aug-2026 (the study's OHLC library)
SHARES = 1_986_578_999            # note 14, audited FY2024/25 statements (NOT an aggregator)
MKT_CAP = SPOT * SHARES

# ---- debt: 31-Mar-2026 balance sheet (latest reviewed), EGP thousand -> EGP -------
d = json.load(open(os.path.join(HERE, 'extract_9m_fy2526.json')))['balance_31mar2026']
DEBT = (d['lt_bank_loans'] + d['holdco_loans'] + d['current_lt']) * 1_000

# ---- Kd, marginal, by currency ---------------------------------------------------
# USD tranche: FY2024/25 interest 1,338.0m EGP on a mean balance of ~$233m at a mean
# USD/EGP of ~49 => ~11.7% USD nominal. Local-equivalent = USD cost + expected EGP
# depreciation. Expected depreciation is taken as the CBE's own inflation-target gap
# rather than an extrapolated spot trend: EGP inflation converging to ~7% vs US ~2.4%
# gives ~4.5%/yr steady-state depreciation.
KD_USD_NOMINAL = 0.117
EXPECTED_DEPRECIATION = 0.045
KD_FX_LOCAL_EQUIV = (1 + KD_USD_NOMINAL) * (1 + EXPECTED_DEPRECIATION) - 1

# EGP tranche: the holding-company facility drawn in FY2024/25 — 96,896,001 of interest
# on 500,000,000 drawn = 19.4%, the company's OWN latest local-currency borrowing.
KD_LOCAL = 0.194

PCT_LOCAL = (d['holdco_loans'] * 1_000) / DEBT     # ~0.3% — the book is essentially all USD

# ---- tax: the company pays no current income tax (settled/appealed years, deferred
# credits both years); statutory 22.5% is used for the shield, disclosed as such.
TAX = 0.225

i = WaccInputs(
    rf_observed=0.230,
    rf_source=("Egypt 10-year EGP government bond yield 23.00%, quote dated 6-Aug-2026 "
               "(investing.com, helper snapshot live_data.json). Cross-checks: a new "
               "EGP 120.9bn treasury bond maturing May-2029 listed at a 23.098% coupon; "
               "secondary T-bill yields 24.86% (3M) to 25.52% (12M)."),
    erp_rating=dam['rating_based_total_equity_risk_premium'],
    sov_default_spread_rating=dam['rating_based_adjusted_default_spread'],
    erp_cds=dam['cds_based_total_equity_risk_premium'],
    sov_default_spread_cds=dam['cds_spread_2025_12_31'],
    erp_source=(f"Damodaran country-premium file (ctryprem.xlsx, updated "
                f"{LIVE['damodaran_egypt']['asof']}), EGYPT row read fresh from the "
                f"original workbook: Moody's {dam['moodys_rating']}, adjusted default "
                f"spread {dam['rating_based_adjusted_default_spread']*100:.2f}%, CRP "
                f"{dam['rating_based_country_risk_premium']*100:.2f}%, total ERP "
                f"{dam['rating_based_total_equity_risk_premium']*100:.2f}% on a mature-"
                f"market ERP of {dam['mature_market_erp']*100:.2f}%. CDS basis: spread "
                f"{dam['cds_spread_2025_12_31']*100:.2f}%, total ERP "
                f"{dam['cds_based_total_equity_risk_premium']*100:.2f}%."),
    beta=BETA['beta'],
    beta_source=(f"Tier-1 own-stock regression: {BETA['n']} weekly observations over 5 "
                 f"years against an equal-weight EGX composite of "
                 f"{BETA['composite_names']} names (EGCH excluded from its own index), "
                 f"R-squared {BETA['r2']:.3f}, SE {BETA['se']:.3f}, 90% CI "
                 f"[{BETA['ci90'][0]:.2f}, {BETA['ci90'][1]:.2f}] — usability gate PASSED. "
                 f"Dimson sum-beta {BETA['dimson']['sum_beta']:.3f} as cross-check."),
    kd_pretax_local=KD_LOCAL,
    kd_source=("MARGINAL, from the company's own two live facilities. Local: the EGP "
               "500,000,000 holding-company loan drawn in FY2024/25 carried EGP "
               "96,896,001 of interest = 19.4% (note 18-2, audited FY2024/25). FX: the "
               "KIMA-2 USD consortium loan cost EGP 1,338,012,810 of interest in "
               "FY2024/25 on a ~US$233m mean balance at ~EGP 49/USD = ~11.7% in USD, "
               "carried here at local-equivalent cost (1.117 x 1.045 - 1 = 16.7%) using "
               "a 4.5% expected-depreciation wedge built from the CBE's own ~7% "
               "inflation target against ~2.4% US inflation. The ANNA facility signed "
               "25-Jun-2025 (US$82.9m + EGP 5,930.7m, amortizing to 2035/36) confirms "
               "the same dual-currency structure forward."),
    kd_pretax_fx_local_equiv=KD_FX_LOCAL_EQUIV,
    pct_debt_local_ccy=PCT_LOCAL,
    debt_currency_evidence=(f"31-Mar-2026 reviewed balance sheet: bank loans "
                            f"{d['lt_bank_loans']:,}k + current portion {d['current_lt']:,}k "
                            f"+ holdco {d['holdco_loans']:,}k = {DEBT/1e9:.2f}bn EGP. The "
                            f"EGP tranche of the KIMA-2 loan was fully repaid in June-2024 "
                            f"(note 18-1), so {(1-PCT_LOCAL)*100:.1f}% of the book is "
                            f"US-dollar — the reason the FX leg dominates this Kd."),
    kd_is_marginal=True,
    tax_rate=TAX,
    market_cap=MKT_CAP,
    total_debt=DEBT,
    weights_source=(f"Market-value equity: EGX close EGP {SPOT} (6-Aug-2026) x "
                    f"{SHARES:,} shares (note 14 of the audited FY2024/25 statements — "
                    f"paid-in capital EGP 9,932,894,995 at EGP 5 par) = EGP "
                    f"{MKT_CAP/1e9:.2f}bn. Debt at book (31-Mar-2026)."),
)

res = build_wacc(i)
print(res.report())
print()
print(sensitivity_grid(i, beta_range=[0.6, 0.8, 1.0, 1.053, 1.2, 1.4]))

out = dict(
    spot=SPOT, shares=SHARES, market_cap=MKT_CAP, total_debt=DEBT,
    rf_observed=i.rf_observed, sov_spread_rating=i.sov_default_spread_rating,
    sov_spread_cds=i.sov_default_spread_cds,
    rf_star_rating=res.rf_star_rating, rf_star_cds=res.rf_star_cds,
    erp_rating=i.erp_rating, erp_cds=i.erp_cds, beta=i.beta,
    ke_rating=res.ke_rating, ke_cds=res.ke_cds,
    kd_local=KD_LOCAL, kd_usd_nominal=KD_USD_NOMINAL,
    expected_depreciation=EXPECTED_DEPRECIATION, kd_fx_local_equiv=KD_FX_LOCAL_EQUIV,
    pct_debt_local=PCT_LOCAL, tax_rate=TAX,
    kd_pretax_blended=res.kd_pretax_blended, kd_aftertax=res.kd_aftertax,
    we=res.we, wd=res.wd,
    wacc_rating=res.wacc_rating, wacc_cds=res.wacc_cds,
    wacc_published=res.wacc_rating,
    warnings=res.warnings,
    sources=dict(rf=i.rf_source, erp=i.erp_source, beta=i.beta_source,
                 kd=i.kd_source, weights=i.weights_source,
                 debt_currency=i.debt_currency_evidence),
)
json.dump(out, open(os.path.join(HERE, 'wacc_result.json'), 'w'), indent=1)
print("\nwrote wacc_result.json")
