"""
wacc_builder.py — standing bottom-up WACC engine (house rule §3.5-G replacement).

Does the ARITHMETIC only. Every input must be sourced by the analyst (web research,
company disclosure, Damodaran's original files, central-bank data) before calling this
module — it deliberately takes no defaults for rf, ERP, beta, or Kd, so a study can
never silently fall back to a guessed number without that guess being visible in the
calling code.

═══════════════════════════════════════════════════════════════════════════════
STANDING METHOD — CORRECTED 21-Jul-2026 (v2). READ THIS BEFORE EDITING.
═══════════════════════════════════════════════════════════════════════════════
An independent expert review of the ORHD build caught a FATAL, SYSTEMIC bug in the
v1 method and it is now fixed here. The two changes are mandatory on every study:

1. NORMALIZE THE RISK-FREE RATE — do NOT double-count sovereign risk.
   The v1 engine used the raw local-currency government-bond yield as rf AND added a
   country-risk-loaded ERP (Damodaran's ERP already contains the country risk premium,
   which is itself derived from the sovereign default spread). That counts the country's
   default risk TWICE. Per Damodaran's own method:

        rf*  =  local government-bond yield  −  sovereign default spread

   Country risk then enters ONCE, through the CRP inside the ERP. For a mature AAA market
   the default spread is ~0 and rf* == observed yield (nothing changes). For an EM like
   Egypt the effect is large (Egypt Jan-2026 default spread = 6.37%, so a 22.31% yield
   normalizes to a 15.94% rf*).

   CONSISTENCY RULE: strip the SAME-basis default spread as the CRP you add back —
   rating-spread stripped ↔ rating ERP;  CDS-spread stripped ↔ CDS ERP. Never mix.

2. COST OF DEBT IS MARGINAL, FORWARD-LOOKING, AND IN THE CASH-FLOW CURRENCY.
   Not a historical/accounting capitalization rate. A same-currency corporate CANNOT
   borrow below its own sovereign, so a local-currency marginal Kd must sit ABOVE the
   local sovereign yield (sanity-checked below). FX-denominated debt must be expressed
   on a LOCAL-EQUIVALENT basis (raw FX coupon + expected local depreciation) before it
   enters a local-nominal WACC — a cheap USD coupon is NOT cheap once carried in EGP.

Everything is NOMINAL unless stated. Nominal WACC discounts nominal cash flows only.
For high-inflation EM, also run a USD (or real) cross-check — see report() footer.

Worked examples in __main__: ORHD (corrected, 21-Jul-2026) and GBCO (FLAGGED for re-run).
═══════════════════════════════════════════════════════════════════════════════

Do-not-revive within this module:
  - Raw local-currency yield as rf while also adding a CRP-loaded ERP (the double-count).
  - Historical/accounting capitalized borrowing rate used as the WACC cost of debt.
  - A raw FX coupon dropped into a local-nominal WACC without depreciation adjustment.
  - Flat house-default ERP reused across countries without checking Damodaran's file.
  - Cross-country sector-peer betas substituted for a genuine regression/bottom-up attempt.
  - Book-value EQUITY weights, or any flat (e.g. 65/35) E/D weights when market data exists.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


# ---------------------------------------------------------------------------
# Regression-beta sanity gate. Encodes the GBCO lesson (n=5 annual regression,
# beta=-0.15, R^2=0.008 = noise). PREFERENCE ORDER for beta, per the 21-Jul-2026
# review: (1) 2-5yr WEEKLY (or monthly) regression; (2) a bottom-up beta from
# comparable unlevered peers re-levered to the target structure (see relever_beta);
# (3) a short-window daily regression ONLY as a flagged interim; (4) 1.0 only on a
# genuine usability-gate failure. Daily EM returns carry illiquidity / non-synchronous
# -trading bias and understate/￼noise-up beta — treat a daily fit as provisional.
# ---------------------------------------------------------------------------
@dataclass
class RegressionBetaAttempt:
    beta: float
    r_squared: float
    n_obs: int
    se_beta: float
    frequency: str = "unspecified"   # "weekly" | "monthly" | "daily" — provenance + interim flag

    def is_usable(self, min_n: int = 24, min_r2: float = 0.05) -> Tuple[bool, str]:
        if self.n_obs < min_n:
            return False, f"n={self.n_obs} < minimum {min_n} observations — sample too small to trust"
        if self.r_squared < min_r2:
            return False, f"R^2={self.r_squared:.3f} < minimum {min_r2} — index barely explains the stock's returns"
        if self.se_beta >= abs(self.beta):
            return False, f"SE(beta)={self.se_beta:.3f} >= |beta|={abs(self.beta):.3f} — estimate is not distinguishable from noise"
        if self.beta < 0:
            return False, f"beta={self.beta:.3f} is negative — almost certainly noise for an equity vs. its own market index"
        return True, "passes minimum usability gate"

    def interim_warnings(self) -> List[str]:
        """Soft flags that do NOT fail the gate but must be disclosed."""
        w = []
        if self.frequency == "daily":
            w.append("beta from DAILY returns — illiquidity/non-synchronous-trading bias likely; "
                     "provisional only, replace with a 2-5yr weekly regression or a bottom-up beta")
        if self.n_obs < 100:
            w.append(f"beta window is short (n={self.n_obs}) — structural risk not well identified")
        return w


def relever_beta(unlevered_beta_peers_median: float, target_debt_to_equity: float,
                 tax_rate: float) -> float:
    """Bottom-up beta: re-lever the median UNLEVERED peer beta to the target D/E
    (Hamada). Preferred over a thin single-name regression for EM names. For a
    multi-segment company (e.g. developer + hotels) build the unlevered beta as a
    business-value-weighted blend of the two segment peer sets BEFORE calling this."""
    return unlevered_beta_peers_median * (1 + (1 - tax_rate) * target_debt_to_equity)


@dataclass
class WaccInputs:
    # --- Cost of equity ---
    rf_observed: float                     # OBSERVED local-currency govt bond yield (sourced market quote)
    erp_rating: float                      # Damodaran ORIGINAL file, rating-based total ERP for the market
    # NORMALIZATION (the fix): sovereign default spread to strip from the observed yield.
    #   Mature AAA market -> 0.0. EM -> Damodaran's adjusted default spread for the rating.
    sov_default_spread_rating: float = 0.0
    erp_cds: Optional[float] = None        # Damodaran CDS-based total ERP (None if no CDS exists)
    sov_default_spread_cds: Optional[float] = None  # CDS-implied default spread; if None, rating spread is reused (flagged)
    beta: float = 1.0                      # 1.0 ONLY on a real usability-gate failure
    beta_source: str = "assumed_1.0_no_reliable_regression"

    # --- Cost of debt (MARGINAL, forward-looking, cash-flow currency) ---
    kd_pretax_local: float = None          # MARGINAL local-currency rate: company's own latest issue, else sovereign+corp spread
    kd_pretax_fx_local_equiv: Optional[float] = None  # FX tranche cost EXPRESSED IN LOCAL-EQUIVALENT terms (coupon + expected deprec.)
    pct_debt_local_ccy: float = 1.0
    tax_rate: float = 0.25

    # --- Weights (market value for equity; book≈market for debt unless distressed) ---
    market_cap: float = None               # spot price x shares outstanding
    total_debt: float = None               # disclosed total borrowings (book value proxy for debt MV)

    # --- Provenance (printed in the report, not used in the math) ---
    rf_source: str = ""
    erp_source: str = ""
    kd_source: str = ""
    kd_is_marginal: bool = False           # must be True to publish — asserts Kd is a marginal, not historical, rate
    debt_currency_evidence: str = ""
    weights_source: str = ""

    def __post_init__(self):
        if self.kd_pretax_fx_local_equiv is not None and self.pct_debt_local_ccy >= 1.0:
            raise ValueError("kd_pretax_fx_local_equiv provided but pct_debt_local_ccy=1.0 implies no FX debt — reconcile")
        if not (0.0 <= self.pct_debt_local_ccy <= 1.0):
            raise ValueError("pct_debt_local_ccy must be between 0 and 1")
        if self.sov_default_spread_rating < 0:
            raise ValueError("sov_default_spread_rating cannot be negative")

    # Normalized risk-free rates (the fix), one per ERP basis for internal consistency.
    @property
    def rf_star_rating(self) -> float:
        return self.rf_observed - self.sov_default_spread_rating

    @property
    def rf_star_cds(self) -> float:
        ds = self.sov_default_spread_cds if self.sov_default_spread_cds is not None else self.sov_default_spread_rating
        return self.rf_observed - ds


@dataclass
class WaccResult:
    ke_rating: float
    ke_cds: Optional[float]
    rf_star_rating: float
    rf_star_cds: Optional[float]
    kd_pretax_blended: float
    kd_aftertax: float
    we: float
    wd: float
    wacc_rating: float
    wacc_cds: Optional[float]
    warnings: List[str] = field(default_factory=list)
    inputs: WaccInputs = field(repr=False, default=None)

    def report(self) -> str:
        i = self.inputs
        L = []
        L.append("=" * 78)
        L.append("BOTTOM-UP WACC — house method (§3.5-G, v2 corrected 21-Jul-2026)")
        L.append("=" * 78)
        L.append("")
        L.append("COST OF EQUITY  (rf normalized: rf* = observed yield − sovereign default spread)")
        L.append(f"  observed local yield   = {i.rf_observed*100:6.2f}%   [{i.rf_source or 'SOURCE NOT RECORDED — flag before publishing'}]")
        L.append(f"  sov default spread (rt)= {i.sov_default_spread_rating*100:6.2f}%   [Damodaran adj. default spread, rating basis]")
        L.append(f"  rf* (rating basis)     = {self.rf_star_rating*100:6.2f}%")
        if i.erp_cds is not None:
            _ds_cds = i.sov_default_spread_cds if i.sov_default_spread_cds is not None else i.sov_default_spread_rating
            L.append(f"  sov default spread(cds)= {_ds_cds*100:6.2f}%   [CDS-implied]")
            L.append(f"  rf* (CDS basis)        = {self.rf_star_cds*100:6.2f}%")
        L.append(f"  ERP (rating-based)     = {i.erp_rating*100:6.2f}%   [{i.erp_source or 'SOURCE NOT RECORDED'}]")
        if i.erp_cds is not None:
            L.append(f"  ERP (CDS-based)        = {i.erp_cds*100:6.2f}%   [same source, CDS column]")
        L.append(f"  beta                   = {i.beta:6.2f}    [{i.beta_source}]")
        L.append(f"  Ke (rating ERP)        = {self.ke_rating*100:6.2f}%   = rf*_rating + beta x ERP_rating")
        if self.ke_cds is not None:
            L.append(f"  Ke (CDS ERP)           = {self.ke_cds*100:6.2f}%   = rf*_cds + beta x ERP_cds")
        L.append("")
        L.append("COST OF DEBT  (MARGINAL, forward-looking, cash-flow currency)")
        L.append(f"  Kd local, pre-tax      = {i.kd_pretax_local*100:6.2f}%   [{i.kd_source or 'SOURCE NOT RECORDED'}]")
        L.append(f"  marginal-rate asserted = {i.kd_is_marginal}")
        if i.kd_pretax_fx_local_equiv is not None:
            L.append(f"  Kd FX (local-equiv)    = {i.kd_pretax_fx_local_equiv*100:6.2f}%   [coupon + expected depreciation]")
            L.append(f"  debt mix               = {i.pct_debt_local_ccy*100:.0f}% local / {(1-i.pct_debt_local_ccy)*100:.0f}% FX   [{i.debt_currency_evidence or 'SOURCE NOT RECORDED'}]")
        else:
            L.append(f"  debt mix               = {i.pct_debt_local_ccy*100:.0f}% local (no FX tranche)   [{i.debt_currency_evidence or 'SOURCE NOT RECORDED'}]")
        L.append(f"  tax rate               = {i.tax_rate*100:6.2f}%")
        L.append(f"  Kd blended, pre-tax    = {self.kd_pretax_blended*100:6.2f}%")
        L.append(f"  Kd blended, after-tax  = {self.kd_aftertax*100:6.2f}%")
        L.append("")
        L.append("WEIGHTS  (market-value equity; book-value debt proxy)")
        L.append(f"  Market cap             = {i.market_cap:,.0f}")
        L.append(f"  Total debt (disclosed) = {i.total_debt:,.0f}   [{i.weights_source or 'SOURCE NOT RECORDED'}]")
        L.append(f"  E / (D+E)              = {self.we*100:6.2f}%")
        L.append(f"  D / (D+E)              = {self.wd*100:6.2f}%")
        L.append("")
        L.append("WACC")
        L.append(f"  WACC (rating-based ERP) = {self.wacc_rating*100:6.2f}%")
        if self.wacc_cds is not None:
            L.append(f"  WACC (CDS-based ERP)    = {self.wacc_cds*100:6.2f}%")
        L.append("=" * 78)
        if self.warnings:
            L.append("CONSISTENCY / SANITY WARNINGS — resolve or disclose before publishing:")
            for w in self.warnings:
                L.append(f"  ! {w}")
            L.append("=" * 78)
        L.append("REMINDERS: (1) nominal WACC discounts nominal cash flows only; match real-to-real.")
        L.append("           (2) high-inflation EM: also run a USD (or real) valuation cross-check.")
        L.append("=" * 78)
        return "\n".join(L)


def _consistency_checks(i: WaccInputs, kd_pretax_blended: float) -> List[str]:
    w = []
    # Double-count trap: EM ERP with no default-spread normalization.
    if i.erp_rating > 0.06 and i.sov_default_spread_rating == 0.0:
        w.append("ERP looks country-risk-loaded (>6%) but sov_default_spread_rating=0 — "
                 "you are almost certainly DOUBLE-COUNTING sovereign risk in rf. Set the default spread.")
    # rf* sanity
    if i.rf_star_rating <= 0:
        w.append(f"rf*_rating={i.rf_star_rating*100:.2f}% <= 0 — default spread exceeds the yield; check inputs.")
    # Marginal-rate assertion
    if not i.kd_is_marginal:
        w.append("kd_is_marginal=False — Kd must be a MARGINAL forward-looking rate, not a historical/accounting rate.")
    # Corporate-below-sovereign paradox (same-currency)
    if i.pct_debt_local_ccy >= 0.999 and i.kd_pretax_local < i.rf_observed:
        w.append(f"local Kd {i.kd_pretax_local*100:.2f}% < sovereign yield {i.rf_observed*100:.2f}% — "
                 "a same-currency corporate cannot borrow below its sovereign; likely a stale or FX-blended rate.")
    # Un-adjusted FX coupon trap
    if i.kd_pretax_fx_local_equiv is not None and i.kd_pretax_fx_local_equiv < i.rf_star_rating:
        w.append(f"FX(local-equiv) Kd {i.kd_pretax_fx_local_equiv*100:.2f}% < rf* {i.rf_star_rating*100:.2f}% — "
                 "looks like a raw FX coupon not grossed up for expected depreciation.")
    return w


def build_wacc(i: WaccInputs) -> WaccResult:
    if i.kd_pretax_local is None:
        raise ValueError("kd_pretax_local is required — source a MARGINAL rate (own latest issue, or sovereign+corp spread)")
    if i.market_cap is None or i.total_debt is None:
        raise ValueError("market_cap and total_debt are required — weights are never assumed in this house method")

    ke_rating = i.rf_star_rating + i.beta * i.erp_rating
    ke_cds = (i.rf_star_cds + i.beta * i.erp_cds) if i.erp_cds is not None else None

    if i.kd_pretax_fx_local_equiv is not None:
        kd_pretax = i.pct_debt_local_ccy * i.kd_pretax_local + (1 - i.pct_debt_local_ccy) * i.kd_pretax_fx_local_equiv
    else:
        kd_pretax = i.kd_pretax_local
    kd_at = kd_pretax * (1 - i.tax_rate)

    we = i.market_cap / (i.market_cap + i.total_debt)
    wd = 1 - we

    wacc_rating = we * ke_rating + wd * kd_at
    wacc_cds = (we * ke_cds + wd * kd_at) if ke_cds is not None else None

    return WaccResult(
        ke_rating=ke_rating, ke_cds=ke_cds,
        rf_star_rating=i.rf_star_rating, rf_star_cds=(i.rf_star_cds if i.erp_cds is not None else None),
        kd_pretax_blended=kd_pretax, kd_aftertax=kd_at,
        we=we, wd=wd, wacc_rating=wacc_rating, wacc_cds=wacc_cds,
        warnings=_consistency_checks(i, kd_pretax), inputs=i,
    )


def sensitivity_grid(i: WaccInputs, beta_range: List[float] = None, erp_choice: str = "rating") -> str:
    if beta_range is None:
        beta_range = [0.7, 0.85, 1.0, 1.15, 1.3, 1.5]
    if erp_choice == "rating":
        erp, rfstar = i.erp_rating, i.rf_star_rating
    else:
        erp, rfstar = i.erp_cds, i.rf_star_cds
    if erp is None:
        raise ValueError("erp_choice='cds' but erp_cds is None for this market")
    lines = [f"Beta sensitivity ({erp_choice}-based: rf*={rfstar*100:.2f}%, ERP={erp*100:.2f}%):", ""]
    lines.append(f"{'beta':>6} | {'Ke':>8} | {'WACC':>8}")
    lines.append("-" * 30)
    we = i.market_cap / (i.market_cap + i.total_debt); wd = 1 - we
    kd_at = (i.kd_pretax_local if i.kd_pretax_fx_local_equiv is None else
             i.pct_debt_local_ccy*i.kd_pretax_local + (1-i.pct_debt_local_ccy)*i.kd_pretax_fx_local_equiv) * (1 - i.tax_rate)
    for b in beta_range:
        ke = rfstar + b * erp
        wacc = we * ke + wd * kd_at
        marker = "  <- used" if abs(b - i.beta) < 1e-9 else ""
        lines.append(f"{b:6.2f} | {ke*100:7.2f}% | {wacc*100:7.2f}%{marker}")
    return "\n".join(lines)


if __name__ == "__main__":
    # ── Worked example 1: ORHD (EGX), CORRECTED build, 21-Jul-2026 ────────────
    orhd = WaccInputs(
        rf_observed=0.2231,
        rf_source="investing.com, Egypt 10Y local-currency govt bond yield, 21-Jul-2026",
        sov_default_spread_rating=0.0637,
        sov_default_spread_cds=0.0340,
        erp_rating=0.1394,
        erp_cds=0.0941,
        erp_source="Damodaran ORIGINAL ctryprem.html, Egypt row, 'Last updated January 5, 2026' "
                   "(base 4.23%, CRP 9.71%, default spread 6.37%, Caa1)",
        beta=1.313,
        beta_source="INTERIM daily regression ORHD vs EGX30-ETF, n=49 (3May-20Jul2026), R2=30.6%, SE=0.29 "
                    "— passes gate but daily/short; TODO replace with 2-5yr weekly or bottom-up peer beta",
        kd_pretax_local=0.23,
        kd_is_marginal=True,
        kd_source="marginal EGP: sovereign 22.31% + ~0.7% corp spread; ideal anchor = O West EGP18bn "
                  "syndicated (Jul-2026) coupon once disclosed. NOT the FY2023 21.7% capitalization rate (rejected).",
        kd_pretax_fx_local_equiv=None,   # small IFC USD/EUR sleeve treated on EGP-equivalent basis; immaterial to blend
        pct_debt_local_ccy=1.0,
        debt_currency_evidence="Debt predominantly EGP (EGP6bn 2023 syndication; EGP18bn O West 2026). IFC USD96mn+EUR55mn "
                               "SLL is the only true FX; on a local-nominal WACC it carries at EGP-equivalent cost.",
        tax_rate=0.225,
        market_cap=38.40*1130,           # spot 38.40 (20-Jul-2026) x ~1,130mn shares
        total_debt=10500.0,              # ~EGP 10.5bn gross debt (opening)
        weights_source="market cap = spot 38.40 x 1,130mn shares; total debt = ~EGP10.5bn disclosed gross borrowings",
    )
    r = build_wacc(orhd)
    print(r.report())
    print()
    print(sensitivity_grid(orhd, erp_choice="rating"))
    print()

    # ── Worked example 2: GBCO (EGX) — FLAGGED, must be re-run under v2 ───────
    # The original GBCO build used rf = raw 22.55% yield with a CRP-loaded ERP and NO
    # default-spread normalization -> DOUBLE-COUNTED sovereign risk. Re-stated below
    # with sov_default_spread_rating set. Any published GBCO WACC predating 21-Jul-2026
    # is overstated by ~the default spread on the equity leg and MUST be re-issued.
    print("\n" + "#" * 78)
    print("# GBCO — RE-RUN under v2 (original delivered WACC carried the double-count).")
    print("#" * 78)
    gbco = WaccInputs(
        rf_observed=0.2255,
        rf_source="investing.com, Egypt 10Y, 3-Jul-2026 (RE-CHECK date on re-issue)",
        sov_default_spread_rating=0.0637,   # <-- THE FIX that was missing in the original build
        sov_default_spread_cds=0.0340,
        erp_rating=0.1394, erp_cds=0.0941,
        erp_source="Damodaran ctryprem.html, Egypt row, Jan-2026",
        beta=1.0,
        beta_source="assumed_1.0 — n=5 annual regression unusable (beta=-0.15, R2=0.008)",
        kd_pretax_local=0.24,   # marginal EGP (sovereign + corp spread), REPLACING the 20.7% avg-lending proxy
        kd_is_marginal=True,
        kd_source="marginal EGP financing co. rate; re-source from GB Capital's latest EGP issue on re-issue",
        pct_debt_local_ccy=1.0,
        debt_currency_evidence="all disclosed facilities EGP; zero USD",
        tax_rate=0.28,
        market_cap=31.25*1085.5, total_debt=38041.4,
        weights_source="mkt cap = 31.25 x 1,085.5mn; total debt = FY25 disclosed borrowings",
    )
    print(build_wacc(gbco).report())
