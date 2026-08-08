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


# --- THE MODEL STUDY (adopted 08 Aug 2026, per Sherif's instruction — SWDY) -------------------
# SWDY_Valuation_Study_05-08-2026 (engine/swdy_study/) is the canonical exemplar EVERY study
# matches for structure AND research depth, adopted because the level of recent valuation
# reports had slipped below par. One-in-one-out: TMPV is retired as the structural template
# and EAND as the operating-company exemplar — SWDY takes both roles. ADCB (bank; RIBL
# secondary) and ALPHADHABI (holdco) remain LENS-PATTERN references only: class adapts the
# lens and the indicator set, never the structure or the depth. This spec holds RULES and
# structure, never numbers.
MODEL_STUDY = {
    "reference": "SWDY_Valuation_Study_05-08-2026",
    "path": "engine/swdy_study/",
    "adopted": "2026-08-08",
    "retired": [
        "TMPV_Valuation_Study_30-06-2026 (structural template)",
        "EAND (operating-company exemplar)",
    ],
    "lens_pattern_references": {
        "operating_company": "SWDY",
        "bank": "ADCB (primary; RIBL secondary)",
        "holdco": "ALPHADHABI",
    },
    "deliverables": [
        "study Word + PDF",
        "Excel model + PDF",
        "standalone bibliography Word + PDF",
        "QC gate as a filled evidence table",
    ],
    # 16 sections, in order — adapt content to market/currency/lens/class, never the skeleton.
    "word_skeleton": [
        "Masthead + READ FIRST",
        "Headline",
        "Valuation summary — every read at a glance",
        "Company overview",
        "1 Fundamental valuation (1.1 cash-flow model with the full FCFF waterfall + the "
        "EV-to-equity bridge; 1.2 book value & sustainable return; 1.3 relative multiples; "
        "1.4 normalised earnings power; 1.5 synthesis — four lenses, one field; 1.6 drivers — "
        "each disclosed segment grown on its own driver, margins as outputs; 1.7 the crux; "
        "1.8 macro & country — sourced cost of capital, the cost-of-debt evidence table, and "
        "every contested construction priced, not just named; 1.9 sensitivity)",
        "2 Technical and price structure",
        "3 A probabilistic price map (percentile map + level-touch ladder; calibration evidence "
        "as plain-language sentences with the statistics inline — no calibration appendix)",
        "4 Comparison of the lenses",
        "5 Catalysts to watch",
        "6 Reading the probability zones",
        "7 Caveats and what would change our mind",
        "Appendix A Financial statements (A.1 income statement, 3y historical + 5y forecast; "
        "A.2 balance sheet; A.3 forecast balance sheet and cash-flow markers)",
        "Appendix B Peer frame, risk register — and the research register",
        "Appendix C Expert panel (C.1-C.3 Expert 1/2/3, cast by method, never persona names; "
        "C.4 cross-examination; C.5 the three in one room; C.6 reading the divergence)",
        "About this series",
        "Disclosure & Disclaimer",
    ],
    # 16 sheets, same names, same order.
    "excel_sheets": [
        "READ FIRST", "Summary", "Fundamental Valuation", "Assumptions", "SOTP Bridge",
        "Segments", "Relative & Normalized", "DCF", "Income Statement", "Balance Sheet",
        "Cash Flow", "Summary Financials", "Monte Carlo", "Sensitivity",
        "Per-Share & Ratios", "Peer & Sector",
    ],
}

# The depth bar — eight standards the SWDY build demonstrated (evidence:
# engine/swdy_study/QC_GATE_05-08-2026.md), so none is aspirational. Each is a QC item,
# not a nice-to-have: missing any one is a FAIL, not a noted limitation.
MODEL_STUDY_DEPTH = {
    "bibliography_document": (
        "A standalone bibliography document ships with every study: READ FIRST + research-layer "
        "guide, a primary-documents table (publisher, date, what was taken from each), the FULL "
        "input register — EVERY input with value / date / source-and-construction, grouped by "
        "layer — a judgements table (each row with what-would-overturn-it), a negative-results "
        "table, and a note on any material aggregator discrepancy found."
    ),
    "provenance_four_field": (
        "Every input is four-field complete (value, source, date, layer), validated by "
        "assertion, and appears in the bibliography document. No orphan numbers."
    ),
    "numeric_traceability": (
        "Every builder (Word, Excel, bibliography, figures) reads the study's committed numbers "
        "file exclusively — no financial numeral typed into a builder. An independent evaluator "
        "recalculates the delivered workbook and reports anything it cannot parse as a FAILURE, "
        "never a skip; cell-level checks against the model, balance-check row zero."
    ),
    "external_reader_scrub": (
        "The reader is an external party: a programmatic scrub of every delivered document for "
        "internal-procedure vocabulary (step names, gate names, sweep/ring vocabulary, engine "
        "module names, verdict tokens, register jargon) returns zero hits. Calibration evidence "
        "lives in the price-map section as plain-language sentences with the statistics inline; "
        "there is no calibration appendix."
    ),
    "figure_discipline": (
        "Figures render on a solid light canvas with ink text — zero transparency, verified "
        "programmatically — and every figure is inspected as a rendered image, not just "
        "generated; label collisions and contrast defects are fixed in-pass."
    ),
    "table_discipline": (
        "Fixed table layout with explicit per-column and per-cell widths, plus a programmatic "
        "check across every table in every delivered document: none exceeds the text block, no "
        "starved columns (mid-word wrapping), no bloated columns."
    ),
    "expert_appendix_max_detail": (
        "Each expert carries: worldview; when-it-works / when-it-fails; a worked valuation table "
        "with every intermediate line; a named sensitivity with numbers; and an explicit "
        "falsifier stated in advance. Plus cross-examination (each challenge conceded or "
        "rejected), the three in one room with the ranges figure, and a divergence table "
        "isolating which assumption drives which gap."
    ),
    "contested_judgement_both_ways": (
        "The study's single most consequential contested judgement is computed BOTH ways, "
        "published side by side (summary table, body, workbook, expert range), and never "
        "averaged into one number that would hide the disagreement — the dual-framing rule, "
        "extended to the study's central judgement."
    ),
}


@dataclass
class ModelStudyChecklist:
    """One-per-study attestation against the model-study depth bar. Every field must be True
    (or documented N/A with a reason) before issue — same discipline as SIGCMChecklist."""
    structure_matches_model: bool = False       # 16-section Word + 16-sheet Excel skeleton
    bibliography_document: bool = False
    provenance_four_field: bool = False
    numeric_traceability: bool = False
    external_reader_scrub: bool = False
    figure_discipline: bool = False
    table_discipline: bool = False
    expert_appendix_max_detail: bool = False
    contested_judgement_both_ways: bool = False
    na_reasons: dict = field(default_factory=dict)

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


def assert_model_study(checklist: ModelStudyChecklist) -> None:
    """Raise before a study is allowed to be issued if it falls short of the model-study bar.

    The model study is SWDY_Valuation_Study_05-08-2026 (engine/swdy_study/): its sections list,
    sheet list and research depth are the standard every study matches. A FAIL here means DO NOT
    ISSUE — depth below the model study is a defect, not a style choice.
    """
    fails = checklist.failures()
    if fails:
        raise AssertionError(
            "MODEL-STUDY BAR NOT MET — study must not be issued. Unmet standards: "
            + ", ".join(fails)
            + ". The bar is SWDY_Valuation_Study_05-08-2026 (engine/swdy_study/, evidence in "
            + "QC_GATE_05-08-2026.md); see MODEL_STUDY / MODEL_STUDY_DEPTH in this module."
        )


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
    m = ModelStudyChecklist()
    assert not m.passed(), "empty model-study checklist should fail"
    assert len(MODEL_STUDY["word_skeleton"]) == 16, "model study is a 16-section Word skeleton"
    assert len(MODEL_STUDY["excel_sheets"]) == 16, "model study is a 16-sheet Excel"
    assert set(MODEL_STUDY_DEPTH) < set(m.__dict__), "every depth standard has a checklist field"
    print("SIGCM module loaded; clauses:", len(SIGCM_CLAUSES),
          "| model-study depth standards:", len(MODEL_STUDY_DEPTH))
