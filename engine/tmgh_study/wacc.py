"""TMGH cost of capital — house v2 method, built bottom-up.

Country risk enters ONCE, through the CRP inside the ERP. The observed local
yield is normalised by Egypt's OWN adjusted default spread before the ERP is
added, on the matching basis (rating with rating, CDS with CDS). Using the raw
local yield alongside a CRP-loaded ERP is the v1 double-count that reached GBCO
and forced a re-issue across the book.

Both ERP bases are published, per the dual-framing rule.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, HERE)

from wacc_builder import WaccInputs, build_wacc
import beta_regression as BR
import research_protocol as RP
import inputs as IN

# --- Damodaran, EGYPT row, read fresh from the ORIGINAL country-premium file --
# Fetched 1-Sep-2026 from
# https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html
# Egypt is looked up on its OWN row; no regional or borrowed figure is used.
DAMODARAN_EGYPT = {
    "moodys_rating": "Caa1",
    "adj_default_spread": 0.0637,
    "country_risk_premium": 0.0971,
    "total_erp_rating": 0.1394,
    "corporate_tax_rate": 0.2250,
    "sovereign_cds": 0.0341,
    "total_erp_cds": 0.0941,
    "source": ("Damodaran country-premium file ctryprem.html, EGYPT row, read fresh "
               "1-Sep-2026 from pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/"
               "ctryprem.html"),
}

# --- Risk-free: observed EGP sovereign yield --------------------------------
RF_OBSERVED = 0.2300
RF_SOURCE = (
    "Egypt 10-year EGP government bond yield 23.00%, market quote dated 6-Aug-2026, "
    "the same sourced quote this repository's current Egyptian editions carry. "
    "CROSS-CHECKS taken 1-Sep-2026: the Central Bank of Egypt held its policy rate at "
    "19.00% at its August 2026 meeting with an overnight lending rate of 20.00% and an "
    "interbank rate of 19.51% (Trading Economics, Egypt interest rate); Investing.com's "
    "Egypt 10-year page quotes 22.880%, but its own timestamp reads 2-Feb-2026 and it is "
    "therefore recorded as a stale second reading rather than a refresh. A 10-year at "
    "23.00% against a 19.00% policy rate implies a term premium of about four points, "
    "which is plausible for this curve. FLAGGED: the adopted quote is 26 days old at "
    "this build date. Section 1.9 prices the sensitivity of fair value to it."
)

# --- Marginal cost of debt ---------------------------------------------------
# The company's OWN latest issue would be the right anchor. TMG's FY2025 and
# 1H2026 statements disclose loans, credit facilities and lease liabilities by
# balance but DO NOT disclose a rate on any of them, and no facility pricing
# appears in any release held. The coupon is therefore not sourced and is not
# invented; the sovereign-plus-spread route is used and labelled.
KD_SPREAD = 0.0250
KD_LOCAL = RF_OBSERVED + KD_SPREAD
KD_SOURCE = (
    "Marginal, forward-looking, in the cash-flow currency: Egypt 10-year sovereign "
    "23.00% plus a 250bp corporate spread, giving 25.50%. TMG's own facility pricing is "
    "NOT disclosed in any statement or release held (recorded as a GAP in the input "
    "register), so the company's own latest issue cannot be used. The result sits ABOVE "
    "the local sovereign, as a same-currency corporate must. TMG's borrowings are "
    "EGP-denominated bank facilities and loans; no foreign-currency tranche is disclosed "
    "separately, so no local-equivalent FX adjustment applies."
)

SPOT = 97.80
SPOT_SOURCE = ("Egyptian Exchange close, 23 August 2026, from the same cleaned "
               "price history the probability distribution is fitted to")


def beta_record():
    rec = BR.own_stock_beta("TMGH", "EG", "EGX")
    RP.assert_beta_provenance(rec)      # raises unless the regressor is published
    return rec


# The INDEPENDENTLY computed effective rate, as the cost-of-debt gate requires: the
# finance charge over the average of the interest-bearing lines only. The denominator
# matters more than the numerator here — dividing by a broader liabilities total that
# includes customer advances and payables to land sellers, none of which bear interest,
# understates the rate by a multiple and manufactures a bias that looks like evidence.
EFFECTIVE_KD_RATES = (0.2432, 0.2508)
EFFECTIVE_KD_PERIODS = ("FY2025", "1H2026 annualised")
EFFECTIVE_KD_DENOMINATOR = (
    "finance cost over the average of loans (current and non-current), credit facilities "
    "and lease liabilities on the company's own balance sheets; customer advances, "
    "payables to land sellers and trade payables are excluded because they bear no interest")


def build():
    b = beta_record()
    shares = IN.KPI["shares_outstanding"]["value"]
    debt = (IN.BS["loans_noncurrent"]["value"] + IN.BS["loans_current"]["value"]
            + IN.BS["credit_facilities"]["value"] + IN.BS["lease_noncurrent"]["value"]
            + IN.BS["lease_current"]["value"])
    wi = WaccInputs(
        rf_observed=RF_OBSERVED,
        erp_rating=DAMODARAN_EGYPT["total_erp_rating"],
        sov_default_spread_rating=DAMODARAN_EGYPT["adj_default_spread"],
        erp_cds=DAMODARAN_EGYPT["total_erp_cds"],
        sov_default_spread_cds=DAMODARAN_EGYPT["sovereign_cds"],
        beta=b["beta"],
        beta_source=("own-stock weekly regression against EGX30, the published index of "
                     "the exchange TMGH is listed on, resolved through "
                     "beta_regression.own_stock_beta — tier 1"),
        kd_pretax_local=KD_LOCAL,
        pct_debt_local_ccy=1.0,
        tax_rate=DAMODARAN_EGYPT["corporate_tax_rate"],
        market_cap=SPOT * shares,
        total_debt=debt,
        rf_source=RF_SOURCE,
        erp_source=DAMODARAN_EGYPT["source"],
        kd_source=KD_SOURCE,
        kd_is_marginal=True,
    )
    return build_wacc(wi), b, debt, shares


def main():
    w, b, debt, shares = build()
    out = {
        "ke_rating": w.ke_rating, "ke_cds": w.ke_cds,
        "rf_star_rating": w.rf_star_rating, "rf_star_cds": w.rf_star_cds,
        "kd_pretax": w.kd_pretax_blended, "kd_aftertax": w.kd_aftertax,
        "weight_equity": w.we, "weight_debt": w.wd,
        "wacc_rating": w.wacc_rating, "wacc_cds": w.wacc_cds,
        "warnings": list(w.warnings),
        "beta_record": b,
        "inputs": {"rf_observed": RF_OBSERVED, "rf_source": RF_SOURCE,
                   "kd_local": KD_LOCAL, "kd_source": KD_SOURCE,
                   "spot": SPOT, "spot_source": SPOT_SOURCE,
                   "shares_mn": shares, "interest_bearing_debt": debt,
                   "market_cap": SPOT * shares,
                   "damodaran": DAMODARAN_EGYPT},
    }
    # [R-COC-01] the SCHEDULE, from the one module. The flat rates above are kept
    # as the explicit-window anchors and as the audit trail of the 01/02-Sep-2026
    # editions; what the valuation discounts on is the ladder.
    import cost_of_capital as COC
    sched = {}
    for basis in ("cds", "rating"):
        sc = COC.schedule(
            "EG",
            COC.BetaRecord(beta=b["beta"], tier=1, source="own-stock weekly regression "
                           "against EGX30 through beta_regression.own_stock_beta",
                           r2=b.get("r2"), se=b.get("se"), n=b.get("n"),
                           index_file=b.get("index_file"), index_asof=b.get("index_asof"),
                           conforming=b.get("conforming", True)),
            COC.DebtBook(gross_debt=debt, pct_local_currency=1.0,
                         currency_source=("all borrowings, facilities and leases on the "
                                          "30-June-2026 balance sheet are EGP; no "
                                          "foreign-currency tranche is separately disclosed"),
                         kd_local_pretax=KD_LOCAL, kd_source=KD_SOURCE,
                         effective_rates=EFFECTIVE_KD_RATES,
                         effective_rate_periods=EFFECTIVE_KD_PERIODS,
                         interest_bearing_note=EFFECTIVE_KD_DENOMINATOR),
            market_cap=SPOT * shares,
            tax_rate=DAMODARAN_EGYPT["corporate_tax_rate"],
            # TMG's explicit window is TEN years, not five: the order book converts
            # over that long and the schedule must cover every year the model
            # discounts. Years beyond the policy path's own horizon sit at the
            # terminal rate, which is the honest completion — the glide finishes
            # when the easing calendar does, and nothing is extrapolated past it.
            years=10, erp_explicit=(DAMODARAN_EGYPT["total_erp_cds"] if basis == "cds"
                                   else DAMODARAN_EGYPT["total_erp_rating"]),
            erp_basis=basis,
            allow_stale_sovereign=True)
        sched[basis] = sc.as_record()
        if basis == "cds":
            print(sc.report())
    out["schedule"] = sched
    out["cost_of_capital_record"] = sched["cds"]      # the CENTRAL basis
    json.dump(out, open(os.path.join(HERE, "wacc.json"), "w"), indent=1, default=str)
    print("rating basis : rf* %.4f  Ke %.4f  WACC %.4f" %
          (w.rf_star_rating, w.ke_rating, w.wacc_rating))
    print("CDS basis    : rf* %.4f  Ke %.4f  WACC %.4f" %
          (w.rf_star_cds, w.ke_cds, w.wacc_cds))
    print("Kd pre-tax %.4f, after tax %.4f; weights E %.4f / D %.4f"
          % (w.kd_pretax_blended, w.kd_aftertax, w.we, w.wd))
    print("beta %.4f (R2 %.3f, SE %.4f, n=%d) vs %s"
          % (b["beta"], b["r2"], b["se"], b["n"], b["index_file"]))
    for x in w.warnings:
        print("  WARNING:", x)


if __name__ == "__main__":
    main()
