"""
research_protocol.py — SOURCE-INTEGRITY & GROUND-UP CONSTRUCTION MANDATE (SIGCM)

STANDING HARD GATE for every TESTAHIL study and update, every ticker, every market.
Adopted 21 Jul 2026 at Sherif's instruction. This module is the machine-readable form of
the mandate; the canonical prose lives in Source_Integrity_and_Ground_Up_Mandate.md and the
condensed rule lives in the project instruction block. A study that fails any clause is a
HARD FAIL and MUST NOT be issued.

This file holds RULES, not numbers — it never goes stale and is never overridden by a fit.
"""

from dataclasses import dataclass, field
from typing import Optional

# --- The eight binding clauses (verbatim intent, enforceable) ---------------------------------
SIGCM_CLAUSES = {
    "historicals_official_only": (
        "Build the past IS/BS/CF using ONLY the company's own issued financial statements and full "
        "disclosures. No vendors, brokers, press-as-source, or third-party estimates. If required "
        "official data is inaccessible, STOP and ASK — never substitute unofficial data. Never "
        "issue a report based on unofficial company information."
    ),
    "primary_source_access": (
        "[ADDED 06-Aug-2026, per instruction] PRIMARY-SOURCE ACCESS GATE. The company's own issued "
        "statements must actually be READ, from an official home: the company website / IR page, the "
        "exchange disclosure portal (EGX, Tadawul, ADX, DFM, QE, KRX/DART, NSE/BSE, EDGAR, LSE RNS), "
        "or the regulator's filing archive. IF THEY CANNOT BE REACHED, STOP WORK AND ASK SHERIF WHAT "
        "TO DO — do not reconstruct, do not substitute an aggregator, and do not ship a model behind a "
        "'best available data, labelled as such' caveat. THE FLOOR IS TWO COMPLETE FINANCIAL YEARS "
        "(full IS+BS+CF plus notes per year, officially sourced): 0-1 = STOP AND ASK; exactly 2 = build "
        "and DISCLOSE the shortfall against QC items (e) and (s); 3+ = normal run. A "
        "403/405/407 or TLS failure is an EGRESS-PROXY fault until checked, not a company-website "
        "failure. This gate OUTRANKS the run-end-to-end-without-asking default."
    ),
    "forecast_ground_up": (
        "Construct the forecast from the ground up: product-by-product / service-by-service wherever "
        "segments are disclosed; revenue = volume x price, cost = cost-per-unit, growth projected in "
        "BOTH volume and price. Where unit/segment data is not disclosed, drop to the finest sourced "
        "level and FLAG the gap."
    ),
    "debt_lc_fx_split": (
        "Study balance-sheet debt in full; split local-currency vs foreign-currency tranches; carry "
        "FX debt at local-equivalent cost (v2 WACC method)."
    ),
    "asset_conversion_cycle": (
        "Study DSO/DIO/DPO and the cash-conversion cycle from the statements and PROJECT the balance-"
        "sheet and cash-flow items from them — no unexplained plugs where the drivers are disclosed."
    ),
    "competitors": (
        "Study competitors within and outside the country for operating KPIs and valuation multiples "
        "(cross-check / relative multiples only — never a source for the subject's historicals)."
    ),
    "beta_own_history_vs_egx30": (
        "Estimate beta from the stock's own price history regressed against the EGX30 history, per the "
        "standing beta hierarchy (own 2-5yr weekly first; same-country peer second; 1.0 only if neither)."
    ),
    "formula_based_model": (
        "Every constructed financial statement is a live formula model (driver -> IS -> BS -> CF -> DCF), "
        "blue = input / black = formula. Fair value must recompute when a driver changes. Hardcoded-value "
        "statements are not acceptable deliverables."
    ),
    "flag_before_issue_and_stop": (
        "Flag any missing input BEFORE issuing. If the website or disclosed statements cannot be read and "
        "that blocks a detailed ground-up build, STOP and ASK — do not proceed on assumptions or "
        "unofficial substitutes."
    ),
}

# Sources that are official for BUILDING historicals. Anything not on this list is a cross-check only.
OFFICIAL_SOURCE_CLASSES = (
    "company_website_ir",      # the company's own IR page / annual & interim report PDFs
    "exchange_disclosure",     # EGX, Tadawul, ADX, DFM, QE, KRX/DART, NSE/BSE, EDGAR, LSE RNS
    "regulator_archive",       # FRA, CMA and equivalents where separate from the exchange
)

# Named here so a build can never quietly treat one as a source. Cross-check use is fine and must be labelled.
NEVER_A_BUILD_SOURCE = (
    "stockanalysis.com", "investing.com", "simplywall.st", "tradingview", "mubasher", "zawya",
    "arabfinance", "wsj", "broker_note", "press", "search_result_extract", "third_party_estimate",
)


# A "complete financial year" = full IS + BS + CF PLUS the notes for that year, from an official
# source. A summary income statement with no cash flow, or no notes behind debt/D&A, does not count.
MIN_COMPLETE_FINANCIAL_YEARS = 2   # below this: STOP AND ASK
TARGET_COMPLETE_FINANCIAL_YEARS = 3  # QC item (e); between floor and target: build and DISCLOSE


class PrimarySourceUnavailable(RuntimeError):
    """Raised when the company's own statements cannot be read. The correct handling is to STOP AND ASK."""


def assert_primary_source_access(
    ticker: str,
    statements_obtained: bool,
    complete_years_obtained: Optional[int] = None,
    sources_tried: Optional[list] = None,
    missing: Optional[list] = None,
    proxy_checked: bool = False,
) -> Optional[str]:
    """Gate the financials build on having actually read the company's own statements.

    Call this BEFORE any forecast driver is set.

    Raises `PrimarySourceUnavailable` when the statements cannot be reached at all, or when fewer
    than MIN_COMPLETE_FINANCIAL_YEARS (2) complete years can be assembled from official sources.
    There is no 'proceed with a caveat' path below the floor: the caller's job on catching it is to
    STOP and put the question to Sherif, never to fall back to an aggregator.

    Between the floor and TARGET_COMPLETE_FINANCIAL_YEARS (3) the build proceeds and this returns the
    disclosure string that MUST be carried on delivery and against QC items (e) and (s). At or above
    the target it returns None.

    `complete_years_obtained` must be stated once `statements_obtained` is True — the count is the
    evidence for item (s), so it is never inferred. `sources_tried` is a list of
    (source_class_or_url, failure_mode) pairs; `missing` names what could not be assembled.
    `proxy_checked` records that a 403/405/407 or TLS failure was diagnosed against the egress proxy
    before the source was called unreachable.
    """
    if statements_obtained:
        if complete_years_obtained is None:
            raise ValueError(
                "State complete_years_obtained — the count of complete financial years (full IS+BS+CF "
                "plus notes, officially sourced) is the evidence for QC item (s) and is never inferred."
            )
        if complete_years_obtained >= TARGET_COMPLETE_FINANCIAL_YEARS:
            return None
        if complete_years_obtained >= MIN_COMPLETE_FINANCIAL_YEARS:
            note = (
                f"SHORT OF THE HOUSE STANDARD — {complete_years_obtained} complete financial years "
                f"obtained, {TARGET_COMPLETE_FINANCIAL_YEARS} wanted by QC item (e). At or above the "
                f"{MIN_COMPLETE_FINANCIAL_YEARS}-year floor, so the build proceeds. DISCLOSE ON DELIVERY: "
                "which year is missing, where it was looked for, and what it costs the forecast. Record "
                "against items (e) and (s) — never a silent pass."
            )
            print("WARNING: " + note)
            return note
        # below the floor -> fall through to the stop-and-ask raise
        missing = list(missing or []) + [
            f"only {complete_years_obtained} complete financial year(s) — below the "
            f"{MIN_COMPLETE_FINANCIAL_YEARS}-year floor"
        ]
    tried = sources_tried or []
    lines = [
        f"PRIMARY-SOURCE ACCESS GATE — STOP AND ASK ({ticker or 'ticker not stated'}).",
        (
            "The company's own issued financial statements could not be read, so the forecast cannot be built."
            if not statements_obtained
            else f"Fewer than {MIN_COMPLETE_FINANCIAL_YEARS} complete financial years could be assembled from "
                 "official sources, so there is nothing to observe a growth rate, a working-capital movement "
                 "or a capex relationship from — the forecast cannot be built."
        ),
        "Missing: " + (", ".join(missing) if missing else "not itemised — itemise before asking."),
        "Official sources attempted: "
        + ("; ".join(f"{s} -> {f}" for s, f in tried) if tried else "NONE RECORDED — attempt them before stopping."),
    ]
    if not proxy_checked and not statements_obtained:
        lines.append(
            "Egress proxy NOT yet ruled out — a 403/405/407 or TLS failure is an environment fault until "
            "checked (/root/.ccr/README.md). Check it before declaring the source unreachable."
        )
    lines.append(
        "Do NOT substitute an aggregator, reconstruct the statements, or deliver behind a disclosed caveat. "
        "Report ticker, what was needed, every source tried with its failure mode, what is blocked downstream, "
        "and the options (Sherif supplies the filings / Sherif authorises a named unofficial source as a "
        "disclosed SIGCM breach / coverage deferred) — then WAIT for the answer."
    )
    raise PrimarySourceUnavailable("\n".join(lines))


@dataclass
class SIGCMChecklist:
    """One-per-study attestation. Every field must be True (or documented N/A with a reason) before issue."""
    historicals_official_only: bool = False
    primary_source_access_confirmed: bool = False  # the official statements were actually read (QC item (s))
    forecast_ground_up: bool = False
    debt_lc_fx_split: bool = False
    asset_conversion_cycle: bool = False
    competitors: bool = False
    beta_own_history_vs_egx30: bool = False
    formula_based_model: bool = False
    flags_raised_before_issue: bool = False
    stop_and_inform_honoured: bool = True   # True unless a blocking gap was hit and NOT escalated
    na_reasons: dict = field(default_factory=dict)  # clause -> reason, for any legitimately N/A item

    def failures(self) -> list:
        out = []
        for k, v in self.__dict__.items():
            if k in ("na_reasons",):
                continue
            if v is not True and k not in self.na_reasons:
                out.append(k)
        return out

    def passed(self) -> bool:
        return not self.failures()


def assert_sigcm(checklist: SIGCMChecklist) -> None:
    """Raise before a study/model is allowed to be issued if any SIGCM clause is unmet.

    Precedent this enforces: reports must be built only on official company disclosures, from the
    ground up, formula-based, with every gap flagged before issue. A HARD FAIL here means DO NOT ISSUE.
    """
    fails = checklist.failures()
    if fails:
        raise AssertionError(
            "SIGCM HARD FAIL — study must not be issued. Unmet clauses: "
            + ", ".join(fails)
            + ". See Source_Integrity_and_Ground_Up_Mandate.md. "
            + "If a clause was blocked by inaccessible official data, STOP AND ASK Sherif what to do rather "
            + "than proceeding — see assert_primary_source_access()."
        )


if __name__ == "__main__":
    # self-check
    c = SIGCMChecklist()
    assert not c.passed(), "empty checklist should fail"
    assert "primary_source_access_confirmed" in c.failures(), "access gate must be an unmet clause by default"

    # 3+ complete years -> clean pass
    assert assert_primary_source_access("TEST", True, complete_years_obtained=3) is None
    # exactly the floor -> proceeds, but returns the disclosure the delivery must carry
    note = assert_primary_source_access("TEST", True, complete_years_obtained=2)
    assert note and "DISCLOSE ON DELIVERY" in note
    # reachable but the year count was never stated -> caller error, not a silent pass
    try:
        assert_primary_source_access("TEST", True)
    except ValueError:
        pass
    else:
        raise AssertionError("complete_years_obtained must be stated")
    # below the floor -> stop and ask, even though the statements were partly readable
    try:
        assert_primary_source_access("TEST", True, complete_years_obtained=1)
    except PrimarySourceUnavailable as e:
        assert "STOP AND ASK" in str(e) and "below the 2-year floor" in str(e)
    else:
        raise AssertionError("below-floor year count must raise PrimarySourceUnavailable")
    # unreachable -> stop and ask
    try:
        assert_primary_source_access(
            "TEST",
            statements_obtained=False,
            sources_tried=[("company_website_ir", "egress blocked (403)")],
            missing=["FY2025 IS/BS/CF + notes"],
        )
    except PrimarySourceUnavailable as e:
        assert "STOP AND ASK" in str(e)
    else:
        raise AssertionError("blocked access must raise PrimarySourceUnavailable")

    print("SIGCM module loaded; clauses:", len(SIGCM_CLAUSES))
