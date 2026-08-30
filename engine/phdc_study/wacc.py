"""PHDC cost of capital — house v2 method, built bottom-up.

The 11-Jun-2026 edition carried a single hardcoded input, "WACC (nominal EGP)
0.18", with no beta, no risk-free and no ERP behind it. That number is BELOW
Egypt's own 10-year sovereign yield, so it cannot be a nominal EGP discount
rate for a levered equity: it prices Palm Hills as safer than the government
that taxes it. This module replaces it with a sourced, bottom-up build.

Country risk enters ONCE, through the CRP inside the ERP. The observed local
yield is normalised by Egypt's OWN default spread before the ERP is added, on
the matching basis (rating with rating, CDS with CDS) — using the raw local
yield alongside a CRP-loaded ERP is the v1 double-count that reached GBCO.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)

from wacc_builder import WaccInputs, build_wacc
import beta_regression as BR
import research_protocol as RP

# --- Damodaran, EGYPT row, read fresh from the ORIGINAL country-premium file --
# Fetched 30-Aug-2026 from
# https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html
DAMODARAN_EGYPT = {
    "moodys_rating": "Caa1",
    "adj_default_spread": 0.0637,
    "country_risk_premium": 0.0971,
    "total_erp_rating": 0.1394,
    "corporate_tax_rate": 0.2250,
    "sovereign_cds": 0.0341,
    "total_erp_cds": 0.0941,
    "source": ("Damodaran country-premium file ctryprem.html, EGYPT row, read fresh "
               "30-Aug-2026 from pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/"
               "ctryprem.html. Egypt is looked up on its own row; no regional or "
               "borrowed figure is used."),
}

# --- Risk-free: observed EGP sovereign yield -------------------------------
RF_OBSERVED = 0.2300
RF_SOURCE = (
    "Egypt 10-year EGP government bond yield 23.00%, market quote dated 6-Aug-2026 "
    "(investing.com), the same sourced quote this repository's EGCH edition carries. "
    "Cross-checks recorded there: an EGP 120.9bn treasury bond maturing May-2029 "
    "listed at a 23.098% coupon, and secondary T-bill yields of 24.86% (3M) to "
    "25.52% (12M). FLAGGED: the quote is 24 days old at this build date. It must be "
    "refreshed before the study is issued externally, and section 1.9 prices the "
    "sensitivity of fair value to it."
)

# --- Marginal cost of debt --------------------------------------------------
# The company's OWN latest issue is the right anchor and it exists — an EGP 2.015bn
# securitisation closed 4-Feb-2026, the first draw on a newly approved EGP 30bn
# programme, in four tranches of 13/36/60/84 months rated AA+/AA/A+/A- on the
# Egyptian national scale. Its PRICING IS NOT DISCLOSED, in the release or in any
# report of it, so the coupon cannot be sourced and is not invented.
KD_SPREAD = 0.0250
KD_LOCAL = RF_OBSERVED + KD_SPREAD
KD_SOURCE = (
    "MARGINAL, forward-looking, in the cash-flow currency. The company's own latest "
    "issue — the EGP 2.015bn securitisation closed 4-Feb-2026 under its EGP 30bn "
    "programme, tranches of 13/36/60/84 months rated AA+/AA/A+/A- (national scale) — "
    "is the correct anchor, but NO COUPON IS DISCLOSED for any tranche, so it cannot "
    "be used. Kd is therefore built as the sovereign 10-year (23.00%) plus a 250bp "
    "corporate credit spread, which places it above the sovereign as the method "
    "requires. THE 250bp SPREAD IS THIS BUILD'S ONE UNSOURCED COST-OF-CAPITAL INPUT "
    "and is flagged as such; it is sensitised in section 1.9. The FY2025 accounting "
    "rate is deliberately NOT used: finance cost of EGP 3,347.5mn on mean gross debt "
    "of EGP 26,740.6mn implies 12.5%, far below the sovereign, because much of the "
    "balance (notes payable to land sellers, customer-facing balances) is "
    "non-interest-bearing and part of the charge is capitalised into work in "
    "progress. A historical or capitalisation rate is not a marginal rate."
)

# --- Balance sheet, FY2025 audited (EGP mn) --------------------------------
# Read from the FY2025 consolidated statement of financial position, which foots:
# total assets 172,129.8 = total liabilities 153,364.1 + total equity 18,765.8.
DEBT_FY25 = {
    "loans_long_term": 10543.1,
    "notes_payable_long_term": 4505.0,
    "credit_facilities": 11337.5,
    "banks_credit_balances": 938.8,
    "current_portion_short_term_loans": 1250.0,
    "notes_payable_short_term": 4875.7,
    "lease_liabilities_long_term": 60.7,
    "lease_liabilities_short_term": 41.9,
}
GROSS_DEBT = sum(DEBT_FY25.values())
CASH_FY25 = 9419.5
NET_DEBT = GROSS_DEBT - CASH_FY25

SHARES_BN = 2.85992          # ordinary shares outstanding
SPOT = 15.20                 # EGX close 23-Aug-2026, as carried in assets/data.js
MARKET_CAP = SHARES_BN * 1000.0 * SPOT     # EGP mn


def build():
    beta = BR.own_stock_beta("PHDC", "EG", "EGX")
    RP.assert_beta_provenance(beta)

    i = WaccInputs(
        rf_observed=RF_OBSERVED,
        rf_source=RF_SOURCE,
        erp_rating=DAMODARAN_EGYPT["total_erp_rating"],
        sov_default_spread_rating=DAMODARAN_EGYPT["adj_default_spread"],
        erp_cds=DAMODARAN_EGYPT["total_erp_cds"],
        sov_default_spread_cds=DAMODARAN_EGYPT["sovereign_cds"],
        erp_source=DAMODARAN_EGYPT["source"],
        beta=beta["beta"],
        beta_source=(
            "Tier 1 — own-stock weekly regression against the PUBLISHED index of the "
            "exchange PHDC is listed on (EGX30, raw_indices/EG/EGX30.csv, as-of "
            "%s), produced by engine/beta_regression.own_stock_beta() and attested by "
            "research_protocol.assert_beta_provenance(). beta %.4f, R^2 %.1f%%, "
            "SE %.4f, n=%d weekly observations over %.2f years, Dimson-adjusted; "
            "90%% CI [%.3f, %.3f]; Blume cross-check %.4f. No constituent composite "
            "is used anywhere in this study."
            % (beta["index_asof"], beta["beta"], beta["r2"] * 100, beta["se"],
               beta["n"], beta["window_years"], beta["ci90"][0], beta["ci90"][1],
               beta["blume_crosscheck"])),
        kd_pretax_local=KD_LOCAL,
        kd_source=KD_SOURCE,
        kd_is_marginal=True,
        pct_debt_local_ccy=1.0,
        debt_currency_evidence=(
            "All borrowings on the FY2025 consolidated statement of financial position "
            "are EGP-denominated: loans long-term 10,543.1, notes payable long-term "
            "4,505.0, credit facilities 11,337.5, banks credit balances 938.8, current "
            "portion of short-term loans 1,250.0, notes payable short-term 4,875.7 and "
            "lease liabilities 102.6, all EGP mn. No foreign-currency tranche is "
            "disclosed, so no local-equivalent FX conversion applies and "
            "pct_debt_local_ccy is 1.0."),
        tax_rate=DAMODARAN_EGYPT["corporate_tax_rate"],
        market_cap=MARKET_CAP,
        total_debt=GROSS_DEBT,
        weights_source=(
            "Equity at MARKET value: %.5fbn shares x EGP %.2f close of 23-Aug-2026 = "
            "EGP %.0fmn. Debt at book as the proxy for market value: EGP %.1fmn gross "
            "borrowings per the FY2025 audited balance sheet. Book equity of EGP "
            "18,765.8mn is NOT used as a weight; it is carried in section 1.2 as the "
            "sustainable-return lens."
            % (SHARES_BN, SPOT, MARKET_CAP, GROSS_DEBT)),
    )
    r = build_wacc(i)
    return beta, i, r


if __name__ == "__main__":
    beta, i, r = build()
    print(r.report())
    out = {
        "beta_record": beta,
        "damodaran_egypt": DAMODARAN_EGYPT,
        "rf_observed": RF_OBSERVED, "rf_source": RF_SOURCE,
        "kd_pretax_local": KD_LOCAL, "kd_source": KD_SOURCE,
        "gross_debt": GROSS_DEBT, "cash": CASH_FY25, "net_debt": NET_DEBT,
        "market_cap": MARKET_CAP, "shares_bn": SHARES_BN, "spot": SPOT,
        "ke_rating": r.ke_rating, "ke_cds": r.ke_cds,
        "rf_star_rating": r.rf_star_rating, "rf_star_cds": r.rf_star_cds,
        "kd_aftertax": r.kd_aftertax, "we": r.we, "wd": r.wd,
        "wacc_rating": r.wacc_rating, "wacc_cds": r.wacc_cds,
        "warnings": r.warnings,
    }
    json.dump(out, open(os.path.join(HERE, "wacc_result.json"), "w"), indent=1, default=str)
    print("\nwrote wacc_result.json")
