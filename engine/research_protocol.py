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
        "official data is inaccessible, STOP and inform — never substitute unofficial data. Never "
        "issue a report based on unofficial company information."
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
        "that blocks a detailed ground-up build, STOP and inform — do not proceed on assumptions or "
        "unofficial substitutes."
    ),
}


@dataclass
class SIGCMChecklist:
    """One-per-study attestation. Every field must be True (or documented N/A with a reason) before issue."""
    historicals_official_only: bool = False
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
            + "If a clause was blocked by inaccessible official data, STOP and inform Sherif rather than proceeding."
        )


if __name__ == "__main__":
    # self-check
    c = SIGCMChecklist()
    assert not c.passed(), "empty checklist should fail"
    print("SIGCM module loaded; clauses:", len(SIGCM_CLAUSES))
