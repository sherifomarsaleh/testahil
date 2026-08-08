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
from typing import Optional, List

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


# =============================================================================
# THE MODEL STUDY — SWDY sets the structural template AND the research-depth bar
# [ADDED 08-Aug-2026, per instruction] Machine-readable form of the Standing
# Research Protocol's "THE MODEL STUDY" entry. Verified by IMPORT, not parse.
#
# One-in-one-out, applied: TMPV is retired as the structural template and EAND as
# the operating-company exemplar. SWDY_Valuation_Study_05-08-2026 takes both roles.
# ADCB (bank; RIBL secondary) and ALPHADHABI (holdco) remain LENS-PATTERN
# references only — class adapts the lens and the indicator set, never the
# structure and never the depth.
# =============================================================================

MODEL_STUDY = {
    "ticker": "SWDY",
    "study": "SWDY_Valuation_Study_05-08-2026",
    "directory": "engine/swdy_study/",
    "adopted": "2026-08-08",
    "retires": ["TMPV_Valuation_Study_30-06-2026 (structural template)",
                "EAND (operating-company exemplar)"],
    "lens_pattern_references": {"operating-co": "SWDY", "bank": "ADCB (RIBL secondary)",
                                "holdco": "ALPHADHABI"},
    # 16-section Word, in order
    "sections": [
        "Masthead + READ FIRST",
        "Headline",
        "Valuation summary",
        "Company overview",
        "1 Fundamental valuation",
        "2 Technical and price structure",
        "3 A probabilistic price map",
        "4 Comparison of the lenses",
        "5 Catalysts",
        "6 Reading the probability zones",
        "7 Caveats and what would change our mind",
        "Appendix A Financial statements",
        "Appendix B Peer frame, risk register and research register",
        "Appendix C The expert valuation panel",
        "About",
        "Disclosure",
    ],
    "section_1_subsections": [
        "1.1 The cash-flow model — the primary lens, with the full waterfall",
        "1.2 Book value and sustainable return — the asset lens",
        "1.3 Relative multiples",
        "1.4 Normalised earnings power",
        "1.5 Synthesis — four lenses, one field",
        "1.6 The drivers — each disclosed segment grown on its own driver, margins as OUTPUTS",
        "1.7 The crux",
        "1.8 Macro and country — sourced cost of capital, cost-of-debt evidence table",
        "1.9 Sensitivity",
    ],
    "appendix_a_subsections": [
        "A.1 Income statement — three years historical and five years forecast",
        "A.2 Balance sheet",
        "A.3 Forecast balance sheet and cash-flow markers",
    ],
    "appendix_b_subsections": [
        "B.1 Peers and the sector frame",
        "B.2 Risk register",
        "B.3 The research register — layers, dated, negative results included",
    ],
    "appendix_c_subsections": [
        "C.1 Expert 1", "C.2 Expert 2", "C.3 Expert 3",
        "C.4 Cross-examination",
        "C.5 The three in one room",
        "C.6 Reading the divergence",
    ],
    # 16-sheet Excel, same names, same order
    "sheets": [
        "READ FIRST", "Summary", "Fundamental Valuation", "Assumptions",
        "SOTP Bridge", "Segments", "Relative & Normalized", "DCF",
        "Income Statement", "Balance Sheet", "Cash Flow", "Summary Financials",
        "Monte Carlo", "Sensitivity", "Per-Share & Ratios", "Peer & Sector",
    ],
    "lenses": ["cash flow", "book value and sustainable return",
               "relative multiples", "normalised earnings power"],
}

MODEL_STUDY_DEPTH = {
    "bibliography_standalone": (
        "A separate bibliography document: READ FIRST + research-layer guide, a "
        "primary-documents table (publisher, date, what was taken from each), the FULL "
        "input register (every input with value / date / source-and-construction, "
        "grouped by layer), a judgements table with what-would-overturn-it per row, a "
        "negative-results table, and a note on any material aggregator discrepancy."),
    "provenance_four_field": (
        "Every input carries value, source, date and layer, validated by assertion, and "
        "appears in the bibliography document. No orphan numbers anywhere."),
    "numeric_traceability": (
        "Every builder — Word, Excel, bibliography, figures — reads the study's committed "
        "numbers file exclusively; no financial numeral is typed into a builder. An "
        "independent evaluator recalculates the delivered workbook and reports anything it "
        "cannot parse as a FAILURE, never a skip."),
    "external_reader_scrub": (
        "A programmatic scrub of every delivered document for internal-procedure "
        "vocabulary must return zero hits. Calibration evidence lives in section 3 as "
        "plain-language sentences with the statistics inline; there is NO calibration "
        "appendix."),
    "figure_discipline": (
        "Figures render on a solid light canvas with ink text — zero transparency, "
        "verified programmatically — and every figure is INSPECTED AS A RENDERED IMAGE; "
        "label collisions and contrast defects are fixed in-pass."),
    "table_discipline": (
        "Fixed table layout with explicit per-column and per-cell widths, plus a "
        "programmatic check across every table in every delivered document: none exceeds "
        "the text block, no starved columns, no bloated columns."),
    "expert_appendix_maximum_detail": (
        "Each expert carries worldview; when-it-works / when-it-fails; a worked valuation "
        "table with EVERY intermediate line; a named sensitivity with numbers; and an "
        "explicit falsifier stated in advance. Plus C.4 cross-examination, C.5 the three "
        "in one room with the ranges figure, and C.6 a divergence table."),
    "contested_judgement_both_ways": (
        "The study's single most consequential contested judgement is computed BOTH ways "
        "and published side by side — summary table, body, workbook, and an expert's "
        "range — never averaged into a single number."),
}


@dataclass
class ModelStudyChecklist:
    """Attested alongside SIGCM before issue. Each field is set True only when the
    build can point at the evidence, exactly as the SIGCM checklist works."""
    sections_match: bool = False
    sheets_match: bool = False
    four_lenses_present: bool = False
    bibliography_standalone: bool = False
    provenance_four_field: bool = False
    numeric_traceability: bool = False
    external_reader_scrub: bool = False
    figure_discipline: bool = False
    table_discipline: bool = False
    expert_appendix_maximum_detail: bool = False
    contested_judgement_both_ways: bool = False
    evidence: dict = field(default_factory=dict)

    def failures(self) -> List[str]:
        return [k for k, v in self.__dict__.items()
                if k != "evidence" and v is not True]

    def passed(self) -> bool:
        return not self.failures()


def _norm(s: str) -> str:
    """Collapse whitespace and case so a heading that titles itself more fully than the
    skeleton names it still matches. A study is allowed to write 'Appendix A  Financial
    statements' or 'C.1  Expert 1 — the accountant'; both are the required section."""
    return " ".join(s.replace("\u2014", "—").lower().split())


def check_sections(actual: List[str]) -> List[str]:
    """Return the MODEL_STUDY sections missing from `actual`.

    Matching is on the section's KEY — the part before any em-dash, with a leading
    'Masthead + ' stripped — because the skeleton names a section and the study titles
    it. Whitespace and case are normalised on both sides."""
    missing = []
    joined = " || ".join(_norm(a) for a in actual)
    for want in (MODEL_STUDY["sections"] + MODEL_STUDY["section_1_subsections"]
                 + MODEL_STUDY["appendix_a_subsections"]
                 + MODEL_STUDY["appendix_b_subsections"]
                 + MODEL_STUDY["appendix_c_subsections"]):
        key = _norm(want.split("—")[0])
        if key.startswith("masthead + "):
            key = key[len("masthead + "):]
        # an appendix key may name the appendix more fully than the study titles it, so
        # fall back to the appendix letter plus its first substantive word
        probes = [key]
        parts = key.split()
        if len(parts) > 2 and parts[0] in ("appendix",):
            probes.append(" ".join(parts[:3]))
        if not any(p in joined for p in probes):
            missing.append(want)
    return missing


def check_sheets(actual: List[str]) -> List[str]:
    """Sheet names must match the model study exactly, in order."""
    want = MODEL_STUDY["sheets"]
    if list(actual) == want:
        return []
    return [f"expected {want}", f"got {list(actual)}"]


def assert_model_study(checklist: ModelStudyChecklist) -> None:
    """Raise before a study is allowed to be issued if it does not match the MODEL
    STUDY in structure or depth.

    QC gate item (a) reads: structure, content, format AND DEPTH match the MODEL STUDY
    (SWDY). A study missing the bibliography document, the four-field input register,
    the recalc evidence, the scrub, the figure/table checks, the maximum-detail expert
    appendix, or the side-by-side contested judgement is a QC FAIL — not a noted
    limitation.
    """
    fails = checklist.failures()
    if fails:
        raise AssertionError(
            "MODEL STUDY FAIL — study must not be issued. Unmet standards: "
            + ", ".join(fails)
            + ". See the THE MODEL STUDY entry in Standing_Research_Protocol.md and the "
            + "filled evidence table in engine/swdy_study/QC_GATE_05-08-2026.md."
        )


if __name__ == "__main__":
    # self-check
    c = SIGCMChecklist()
    assert not c.passed(), "empty checklist should fail"
    m = ModelStudyChecklist()
    assert not m.passed(), "empty model-study checklist should fail"
    assert check_sheets(MODEL_STUDY["sheets"]) == [], "model sheet list must self-match"
    print("research_protocol loaded — SIGCM clauses:", len(SIGCM_CLAUSES),
          "| model-study standards:", len(MODEL_STUDY_DEPTH),
          "| sections:", len(MODEL_STUDY["sections"]),
          "| sheets:", len(MODEL_STUDY["sheets"]))
