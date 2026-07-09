"""
wacc_builder.py — standing bottom-up WACC engine (house rule §3.5-G replacement).

Does the ARITHMETIC only. Every input must be sourced by the analyst (web research,
company disclosure, Damodaran's original files, central-bank data) before calling this
module — it deliberately takes no defaults for rf, ERP, beta, or Kd, so a study can
never silently fall back to a guessed number without that guess being visible in the
calling code.

Usage pattern (see __main__ block for a worked example using the GBCO figures):

    from wacc_builder import WaccInputs, build_wacc

    inp = WaccInputs(
        rf=0.2255,                  # target market's own local-currency govt bond yield
        erp_rating=0.1394,          # Damodaran ORIGINAL file, rating-based ERP
        erp_cds=0.0941,             # Damodaran ORIGINAL file, CDS-based ERP (may be None if no CDS)
        beta=1.0,                   # regression beta if reliably computed, else 1.0
        beta_source="assumed_1.0",  # free-text provenance note, printed in the report
        kd_pretax_egp=0.207,        # sourced local-currency lending rate
        kd_pretax_fx=None,         # sourced FX lending rate, or None if ~100% local-currency debt
        pct_debt_local_ccy=1.0,     # fraction of total debt in local currency (sourced or best-evidenced estimate)
        tax_rate=0.28,
        market_cap=31.25*1085.5,
        total_debt=38041.4,
    )
    result = build_wacc(inp)
    print(result.report())

Do-not-revive within this module (mirrors the house do-not-revive list for the MC engine):
  - Flat house-default ERP reused across countries without checking Damodaran's current file.
  - Cross-country sector-peer betas substituted for a genuine regression attempt.
  - A guessed Kd spread when the company's own disclosed facilities/rates are findable.
  - Fixed 65/35 (or any other flat) E/D weights when market cap and disclosed debt are both known.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Tuple


# ---------------------------------------------------------------------------
# Regression-beta sanity gate. If an analyst attempts a real regression beta,
# run it through this gate before it's allowed to be used. This encodes the
# GBCO lesson: n=5 annual EGX30-vs-GBCO regression gave beta=-0.15, R^2=0.008 —
# statistical noise, not a beta. Reject anything this weak automatically.
# ---------------------------------------------------------------------------
@dataclass
class RegressionBetaAttempt:
    beta: float
    r_squared: float
    n_obs: int
    se_beta: float

    def is_usable(self, min_n: int = 24, min_r2: float = 0.05) -> Tuple[bool, str]:
        """Minimum bar: at least 24 observations (roughly 2 years of monthly data,
        or 6 months of weekly data) and R^2 >= 5%. Both are deliberately low bars —
        the point is to catch the GBCO failure mode (n=5, R^2=0.008), not to demand
        textbook-grade statistical power, which is rarely available for single EM
        stocks anyway."""
        if self.n_obs < min_n:
            return False, f"n={self.n_obs} < minimum {min_n} observations — sample too small to trust"
        if self.r_squared < min_r2:
            return False, f"R^2={self.r_squared:.3f} < minimum {min_r2} — index barely explains the stock's returns"
        if self.se_beta >= abs(self.beta):
            return False, f"SE(beta)={self.se_beta:.3f} >= |beta|={abs(self.beta):.3f} — estimate is not distinguishable from noise"
        if self.beta < 0:
            return False, f"beta={self.beta:.3f} is negative — almost certainly noise for an equity vs. its own market index"
        return True, "passes minimum usability gate"


@dataclass
class WaccInputs:
    # --- Cost of equity ---
    rf: float                              # local-currency risk-free rate (sourced market quote)
    erp_rating: float                      # Damodaran ORIGINAL file, rating-based total ERP for the market
    erp_cds: Optional[float] = None        # Damodaran ORIGINAL file, CDS-based total ERP (None if no CDS exists)
    beta: float = 1.0                      # 1.0 unless a regression attempt passed RegressionBetaAttempt.is_usable()
    beta_source: str = "assumed_1.0_no_reliable_regression"

    # --- Cost of debt ---
    kd_pretax_local: float = None          # sourced local-currency lending rate (central bank / disclosed facility rate)
    kd_pretax_fx: Optional[float] = None   # sourced FX lending rate; None if debt is ~100% local currency
    pct_debt_local_ccy: float = 1.0        # fraction of total debt in local currency (sourced, or best-evidenced estimate)
    tax_rate: float = 0.25

    # --- Weights ---
    market_cap: float = None               # spot price x shares outstanding
    total_debt: float = None               # disclosed total borrowings (book value, standard practice)

    # --- Provenance (filled in by the analyst; printed in the report, not used in the math) ---
    rf_source: str = ""
    erp_source: str = ""
    kd_source: str = ""
    debt_currency_evidence: str = ""
    weights_source: str = ""

    def __post_init__(self):
        if self.kd_pretax_fx is not None and self.pct_debt_local_ccy >= 1.0:
            raise ValueError("kd_pretax_fx was provided but pct_debt_local_ccy=1.0 implies no FX debt — reconcile these before proceeding")
        if not (0.0 <= self.pct_debt_local_ccy <= 1.0):
            raise ValueError("pct_debt_local_ccy must be between 0 and 1")


@dataclass
class WaccResult:
    ke_rating: float
    ke_cds: Optional[float]
    kd_pretax_blended: float
    kd_aftertax: float
    we: float
    wd: float
    wacc_rating: float
    wacc_cds: Optional[float]
    inputs: WaccInputs = field(repr=False, default=None)

    def report(self) -> str:
        i = self.inputs
        lines = []
        lines.append("=" * 78)
        lines.append("BOTTOM-UP WACC — house method (§3.5-G)")
        lines.append("=" * 78)
        lines.append("")
        lines.append("COST OF EQUITY")
        lines.append(f"  rf                     = {i.rf*100:6.2f}%   [{i.rf_source or 'SOURCE NOT RECORDED — flag before publishing'}]")
        lines.append(f"  ERP (rating-based)     = {i.erp_rating*100:6.2f}%   [{i.erp_source or 'SOURCE NOT RECORDED'}]")
        if i.erp_cds is not None:
            lines.append(f"  ERP (CDS-based)        = {i.erp_cds*100:6.2f}%   [same source, CDS column]")
        lines.append(f"  beta                   = {i.beta:6.2f}    [{i.beta_source}]")
        lines.append(f"  Ke (rating ERP)        = {self.ke_rating*100:6.2f}%")
        if self.ke_cds is not None:
            lines.append(f"  Ke (CDS ERP)           = {self.ke_cds*100:6.2f}%")
        lines.append("")
        lines.append("COST OF DEBT")
        lines.append(f"  Kd local-ccy, pre-tax  = {i.kd_pretax_local*100:6.2f}%   [{i.kd_source or 'SOURCE NOT RECORDED'}]")
        if i.kd_pretax_fx is not None:
            lines.append(f"  Kd FX, pre-tax         = {i.kd_pretax_fx*100:6.2f}%")
            lines.append(f"  debt currency mix      = {i.pct_debt_local_ccy*100:.0f}% local / {(1-i.pct_debt_local_ccy)*100:.0f}% FX   [{i.debt_currency_evidence or 'SOURCE NOT RECORDED'}]")
        else:
            lines.append(f"  debt currency mix      = {i.pct_debt_local_ccy*100:.0f}% local (no FX tranche)   [{i.debt_currency_evidence or 'SOURCE NOT RECORDED'}]")
        lines.append(f"  tax rate               = {i.tax_rate*100:6.2f}%")
        lines.append(f"  Kd blended, pre-tax    = {self.kd_pretax_blended*100:6.2f}%")
        lines.append(f"  Kd blended, after-tax  = {self.kd_aftertax*100:6.2f}%")
        lines.append("")
        lines.append("WEIGHTS")
        lines.append(f"  Market cap             = {i.market_cap:,.0f}")
        lines.append(f"  Total debt (disclosed) = {i.total_debt:,.0f}   [{i.weights_source or 'SOURCE NOT RECORDED'}]")
        lines.append(f"  E / (D+E)              = {self.we*100:6.2f}%")
        lines.append(f"  D / (D+E)              = {self.wd*100:6.2f}%")
        lines.append("")
        lines.append("WACC")
        lines.append(f"  WACC (rating-based ERP, standard practice) = {self.wacc_rating*100:6.2f}%")
        if self.wacc_cds is not None:
            lines.append(f"  WACC (CDS-based ERP, more current)         = {self.wacc_cds*100:6.2f}%")
        lines.append("=" * 78)
        missing = [f for f in [i.rf_source, i.erp_source, i.kd_source, i.weights_source] if not f]
        if missing:
            lines.append(f"WARNING: {len(missing)} source field(s) not recorded — do not publish until every")
            lines.append("         input above shows a real citation, not a blank.")
            lines.append("=" * 78)
        return "\n".join(lines)


def build_wacc(i: WaccInputs) -> WaccResult:
    if i.kd_pretax_local is None:
        raise ValueError("kd_pretax_local is required — there is no default; source it from central-bank data or a disclosed facility rate")
    if i.market_cap is None or i.total_debt is None:
        raise ValueError("market_cap and total_debt are required — weights are never assumed in this house method")

    ke_rating = i.rf + i.beta * i.erp_rating
    ke_cds = (i.rf + i.beta * i.erp_cds) if i.erp_cds is not None else None

    if i.kd_pretax_fx is not None:
        kd_pretax = i.pct_debt_local_ccy * i.kd_pretax_local + (1 - i.pct_debt_local_ccy) * i.kd_pretax_fx
    else:
        kd_pretax = i.kd_pretax_local
    kd_at = kd_pretax * (1 - i.tax_rate)

    we = i.market_cap / (i.market_cap + i.total_debt)
    wd = 1 - we

    wacc_rating = we * ke_rating + wd * kd_at
    wacc_cds = (we * ke_cds + wd * kd_at) if ke_cds is not None else None

    return WaccResult(
        ke_rating=ke_rating, ke_cds=ke_cds,
        kd_pretax_blended=kd_pretax, kd_aftertax=kd_at,
        we=we, wd=wd,
        wacc_rating=wacc_rating, wacc_cds=wacc_cds,
        inputs=i,
    )


def sensitivity_grid(i: WaccInputs, beta_range: List[float] = None, erp_choice: str = "rating") -> str:
    """Beta sensitivity table — beta is the input most likely to carry real uncertainty
    (either assumed at 1.0, or a regression estimate with a wide confidence interval).
    Always attach this table when beta was assumed rather than reliably estimated."""
    if beta_range is None:
        beta_range = [0.7, 0.85, 1.0, 1.15, 1.3, 1.5]
    erp = i.erp_rating if erp_choice == "rating" else i.erp_cds
    if erp is None:
        raise ValueError("erp_choice='cds' but erp_cds is None for this market")
    lines = [f"Beta sensitivity ({erp_choice}-based ERP = {erp*100:.2f}%):", ""]
    lines.append(f"{'beta':>6} | {'Ke':>8} | {'WACC':>8}")
    lines.append("-" * 30)
    we = i.market_cap / (i.market_cap + i.total_debt); wd = 1 - we
    kd_at = (i.kd_pretax_local if i.kd_pretax_fx is None else
             i.pct_debt_local_ccy*i.kd_pretax_local + (1-i.pct_debt_local_ccy)*i.kd_pretax_fx) * (1 - i.tax_rate)
    for b in beta_range:
        ke = i.rf + b * erp
        wacc = we * ke + wd * kd_at
        marker = "  <- assumed" if abs(b - i.beta) < 1e-9 else ""
        lines.append(f"{b:6.2f} | {ke*100:7.2f}% | {wacc*100:7.2f}%{marker}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Worked example: GBCO (EGX), as built 09-07-2026.
    gbco = WaccInputs(
        rf=0.2255,
        rf_source="investing.com, Egypt 10Y local-currency govt bond yield, 3-Jul-2026",
        erp_rating=0.1394,
        erp_cds=0.0941,
        erp_source="Damodaran ORIGINAL file (pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html), Egypt row, 'Last updated January 2026'",
        beta=1.0,
        beta_source="assumed_1.0 — n=5 annual GBCO-vs-EGX30 regression gave beta=-0.15, R2=0.008 (unusable); "
                     "higher-frequency EGX30 data inaccessible via available tools; house rule default applied",
        kd_pretax_local=0.207,
        kd_source="CBE weighted-average EGP bank lending rate, <12mo tenor, Feb-2026 (via CEIC/TradingEconomics "
                   "quoting CBE); cross-checked against CBE overnight lending-rate ceiling 20.0% held since Apr-2026",
        kd_pretax_fx=None,
        pct_debt_local_ccy=1.0,
        debt_currency_evidence="5 separately disclosed GB Corp/GB Capital financing facilities found (Drive Finance "
                                "EGP5bn syndication, Ghabbour Egypt EGP1.2bn Sadat facility, GB Lease EGP4.16bn "
                                "securitization, Drive Finance EGP2.4bn bond, GB Capital Securitization EGP28.8bn "
                                "book) are ALL EGP-denominated; zero USD facilities found; one source explicitly "
                                "notes no USD-listed instrument exists for the company",
        tax_rate=0.28,
        market_cap=31.25*1085.5,
        total_debt=38041.4,
        weights_source="market cap = spot(31.25) x shares(1,085.5mn); total debt = FY25 disclosed consolidated borrowings",
    )
    result = build_wacc(gbco)
    print(result.report())
    print()
    print(sensitivity_grid(gbco, erp_choice="cds"))
