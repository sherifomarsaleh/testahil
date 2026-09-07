"""
research_protocol.py — SOURCE-INTEGRITY & GROUND-UP CONSTRUCTION MANDATE (SIGCM)

STANDING HARD GATE for every TESTAHIL study and update, every ticker, every market.
Adopted 21 Jul 2026 at Sherif's instruction. This module is the machine-readable form of
the mandate; the canonical prose lives in Source_Integrity_and_Ground_Up_Mandate.md and the
condensed rule lives in the project instruction block. A study that fails any clause is a
HARD FAIL and MUST NOT be issued.

This file holds RULES, not numbers — it never goes stale and is never overridden by a fit.
"""

import re

from dataclasses import dataclass, field
from typing import List, Optional

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


# --- THE MODEL REPORT (adopted 19 Aug 2026, per Sherif's instruction — ADNOCLS) ---------------
# ADNOCLS_Valuation_Study_09-08-2026 (engine/adnocls_study/) is the canonical exemplar EVERY
# study matches for structure AND research depth. It DISPLACES SWDY under the standing
# one-in-one-out rule, chosen on depth and analysis: it prices every contested construction
# instead of naming it, shows the beta both ways, builds the cost of debt from six disclosed
# instruments rather than one asserted range, drives seven disclosed units on seven drivers
# with margins falling out as outputs, and gives each expert a worked table with every
# intermediate line. ADCB (bank) and ALPHADHABI (holdco) remain LENS-PATTERN references only:
# class adapts the lens and the indicator set, never the structure or the depth. This spec
# holds RULES and structure, never numbers.
#
# ONE SECTION OF THE EXEMPLAR IS NOT PART OF THE MODEL: "What changed in these editions, and
# why" [excluded 19-Aug-2026, per instruction] — edition history is internal QC evidence and
# belongs in the QC gate and the critique adjudication, not in a document an external reader
# receives. The model report document is the exemplar with that section removed, built and
# asserted by engine/model_report/build_model_report_docx.py.
#
# THE REFERENCE SET IS CLOSED — exactly three names, enforced by REFERENCE_SET below
# [08-Aug-2026, per Sherif's instruction]. No other company is a template, an exemplar or a
# reference study anywhere in the protocol; every previously-named exemplar is gone from the
# reference layer entirely rather than carried as a retired entry — SWDY included, as of
# 19-Aug-2026. A secondary exemplar of a class whose primary already covers it is redundant by
# construction and is not admitted. Adding a fourth name is a protocol change, not a
# documentation edit: it must displace one of these three, and this assertion is what forces
# that decision to be made explicitly.
REFERENCE_SET = ("ADNOCLS", "ADCB", "ALPHADHABI")

MODEL_STUDY = {
    "reference": "ADNOCLS_Valuation_Study_09-08-2026",
    "path": "engine/adnocls_study/",
    "adopted": "2026-08-19",
    "displaced": "SWDY_Valuation_Study_05-08-2026",
    "model_report_document": "engine/model_report/MODEL_REPORT_09-08-2026.docx",
    "excluded_sections": ("What changed in these editions, and why",),
    "lens_pattern_references": {
        "operating_company": "ADNOCLS",
        "bank": "ADCB",
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
        "1.4 normalised earnings power; 1.5 synthesis — the class primary IS the central under [R-LENS-03], the other lenses published beside it as cross-checks and the RANGE of their present-value reads as the envelope; NEVER a weighted blend, and never a set of typed weights; 1.6 drivers — "
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
        "Appendix B Peer frame, risk register — and the research register "
        "(B.1 peers and the sector frame; B.2 risk register; B.3 the research "
        "register — layers, dated, negative results included)",
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

# The depth bar — eight standards the ADNOCLS build demonstrated (evidence:
# engine/adnocls_study/QC_GATE_09-08-2026.md), so none is aspirational. Each is a QC item,
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
        "there is no calibration appendix. [R-CAL-02] The verdict tokens are named and testable: "
        "band_record.assert_no_verdict_tokens() is the scrub for that class, and what the price-map "
        "section states instead is the BAND RECORD \u2014 how often the price finished inside the "
        "90% band, over how many resolved forecasts \u2014 never PASS/PARITY/FAIL, which is the "
        "internal Step 0 gate and is never shown to a reader."
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
    """Raise before a study is allowed to be issued if it falls short of the model-report bar.

    The model report is ADNOCLS_Valuation_Study_09-08-2026 (engine/adnocls_study/), minus the
    excluded edition-history section; the built document is
    engine/model_report/MODEL_REPORT_09-08-2026.docx. Its sections list, sheet list, content
    and research depth are the standard every study matches. A FAIL here means DO NOT ISSUE —
    depth below the model report is a defect, not a style choice.
    """
    fails = checklist.failures()
    if fails:
        raise AssertionError(
            "MODEL-REPORT BAR NOT MET — study must not be issued. Unmet standards: "
            + ", ".join(fails)
            + ". The bar is ADNOCLS_Valuation_Study_09-08-2026 (engine/adnocls_study/, evidence "
            + "in QC_GATE_09-08-2026.md); see MODEL_STUDY / MODEL_STUDY_DEPTH in this module."
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
    # The reference set is CLOSED at exactly three names. This assertion is the enforcement:
    # a fourth exemplar cannot be added without displacing one of these and failing here first.
    assert set(MODEL_STUDY["lens_pattern_references"].values()) == set(REFERENCE_SET), (
        "the reference set is closed — exactly ADNOCLS / ADCB / ALPHADHABI, no other company "
        "is a template, exemplar or reference study anywhere in the protocol"
    )
    assert MODEL_STUDY["lens_pattern_references"]["operating_company"] == "ADNOCLS", (
        "ADNOCLS is the model report and therefore also the operating-company lens pattern"
    )
    assert "SWDY" not in REFERENCE_SET, (
        "one-in-one-out: ADNOCLS displaced SWDY on 19-Aug-2026 and SWDY is removed from the "
        "reference layer outright, not carried as a retired or secondary entry"
    )

    print("SIGCM module loaded; clauses:", len(SIGCM_CLAUSES),
          "| model-report depth standards:", len(MODEL_STUDY_DEPTH),
          "| reference set:", "/".join(REFERENCE_SET),
          "| model report:", MODEL_STUDY["reference"])


# ---------------------------------------------------------------------------
# BETA PROVENANCE GATE  [ADDED 10-Aug-2026]
#
# SIGCMChecklist.beta_own_history_vs_egx30 is a BOOLEAN a study sets itself, and every
# study in this repo set it True while regressing against an equal-weight composite of
# the covered names. A self-attestation cannot catch that. This gate inspects the actual
# beta record produced by engine/beta_regression.py and fails on the evidence.
# ---------------------------------------------------------------------------
def assert_beta_provenance(rec: dict, tier2_fallback_documented: bool = False) -> None:
    """Raise unless this beta came from the exchange's PUBLISHED index.

    `rec` is the dict returned by beta_regression.own_stock_beta(). Passing a
    hand-assembled dict without provenance fails, which is the point.
    """
    required = ('beta', 'r2', 'se', 'n', 'usable', 'index_file', 'index_asof',
                'market', 'exchange', 'conforming')
    missing = [k for k in required if k not in rec]
    if missing:
        raise AssertionError(
            f"BETA PROVENANCE FAIL — record is missing {missing}. A beta is only quotable "
            f"with its regressor and diagnostics attached; produce it with "
            f"engine/beta_regression.own_stock_beta(), never a study-local composite."
        )
    idx = str(rec['index_file']).replace('\\', '/')
    if 'raw_indices/' not in idx:
        raise AssertionError(
            f"BETA PROVENANCE FAIL — regressor {idx!r} is not a published index under "
            f"raw_indices/. A constituent composite is not a substitute and not a tier."
        )
    if not rec['usable'] and not tier2_fallback_documented:
        raise AssertionError(
            f"BETA PROVENANCE FAIL — {rec.get('ticker','?')} fails the usability gate "
            f"({rec.get('gate_msg')}). It must fall to a SAME-COUNTRY peer beta (tier 2) or "
            f"beta=1.0 (tier 3) shown with the failed diagnostics — it may NOT keep a "
            f"composite number. Pass tier2_fallback_documented=True once that is done."
        )
    if not rec['conforming'] and not rec.get('interim_note'):
        raise AssertionError(
            "BETA PROVENANCE FAIL — an interim index substitution is in force but its "
            "disclosure note is absent. Any beta on an interim regressor must quote it."
        )


# ---------------------------------------------------------------------------
# THE STUDY STANDARD, VERSIONED  [R-STD-01, ADDED 23-Aug-2026, per instruction]
#
# Until now nothing stamped a study with the standard it was built against, so
# "is this study finished, or finished-for-now?" had no answer in the repository
# and a name re-issued in September could silently need re-issuing in November.
# A study records the version it was built to; the repo-level gate reports any
# study built to an older one. Bump this ONLY when a change would alter a
# delivered number or a required artefact — not for prose.
# ---------------------------------------------------------------------------
STANDARD_VERSION = "2026.09.01"
STANDARD_VERSION_NOTE = (
    "v2 cost of capital (rf normalised by the sovereign's own default spread); beta via "
    "beta_regression.own_stock_beta() against the registered index of the listing exchange, "
    "attested by assert_beta_provenance(); forecast built ground-up to the finest sourced "
    "level and attested by assert_ground_up() on a driver record; margins as outputs; "
    "terminal growth reconciled; the three gates called in the study's own code; and "
    "[R-GAP-01] a dated GAP_REVIEW covering all eight headings wherever the central fair "
    "value sits more than 10% below the latest known market price."
)
# Bumped 01-Sep-2026 for [R-GAP-01]. This clears the "prose only" bar deliberately: the
# rule adds a REQUIRED ARTEFACT — a study whose central sits more than 10% below the
# traded price is not complete without its gap review — and the whole point of the
# version stamp is that a study built before that requirement is countable rather than
# silently assumed current. On adoption day four delivered studies were breaching with no
# review; see engine/build_depth_audit/gap_outstanding.json.


# ---------------------------------------------------------------------------
# GROUND-UP CONSTRUCTION GATE  [R-SIGCM-02, ADDED 23-Aug-2026, per instruction]
#
# The protocol already diagnosed this failure mode exactly, for beta:
# "SIGCMChecklist.beta_own_history_vs_egx30 is a flag a study sets itself, and every
# study set it True while regressing on a composite. A self-attestation cannot catch
# that." That diagnosis was acted on for beta ONLY. The other eight clauses stayed
# self-attested booleans -- forecast_ground_up among them -- and the 23-Aug-2026
# build-depth audit found 63 of 90 delivered studies were NOT built ground-up while
# the flag was available to be set True. Same hole, one clause over.
#
# This gate does for the ground-up clause what assert_beta_provenance() did for beta:
# it inspects a RECORD of how each revenue line was actually built, and fails on the
# evidence rather than on the study's opinion of itself.
# ---------------------------------------------------------------------------
GROUND_UP_LEVELS = {
    "unit":     "volume x price on a DISCLOSED physical unit, cost per unit; margin an output",
    "derived":  "unit economics on a volume that is indexed, estimated or back-solved rather "
                "than disclosed -- permitted, but the gap must be stated in the study",
    "segment":  "the disclosed segment on its own driver; no unit economics available",
    "topdown":  "a growth path plus a margin assumption -- the floor of last resort",
}


@dataclass
class DriverLine:
    """One revenue line, and how it was actually built."""
    name: str
    level: str                      # one of GROUND_UP_LEVELS
    share_of_revenue: float         # 0..1, of the forecast base year
    unit: Optional[str] = None      # e.g. "litres", "vessel-days", "packs", "connected RT"
    unit_source: Optional[str] = None   # the disclosure the unit came from
    price_basis: Optional[str] = None   # the rate applied to the unit
    cost_basis: Optional[str] = None    # cost per unit, or why not
    gap_note: Optional[str] = None      # REQUIRED for any level below "unit"


def assert_ground_up(lines, ticker: str = "?", tolerance: float = 0.01) -> dict:
    """Raise unless the forecast was built to the finest sourced level, with gaps stated.

    Returns a summary dict so the QC gate can print the evidence rather than a boolean.
    """
    if not lines:
        raise AssertionError(
            f"GROUND-UP FAIL — {ticker} supplied no driver record. The ground-up clause is "
            f"no longer attestable by a flag; build a DriverLine per revenue line."
        )
    bad = [l.name for l in lines if l.level not in GROUND_UP_LEVELS]
    if bad:
        raise AssertionError(f"GROUND-UP FAIL — {ticker}: unknown build level on {bad}")

    total = sum(l.share_of_revenue for l in lines)
    if abs(total - 1.0) > tolerance:
        raise AssertionError(
            f"GROUND-UP FAIL — {ticker}: the driver lines cover {total:.1%} of revenue, not "
            f"100%. A line omitted from the record is a line nobody checked."
        )
    for l in lines:
        if l.level == "unit" and not (l.unit and l.unit_source and l.price_basis):
            raise AssertionError(
                f"GROUND-UP FAIL — {ticker}/{l.name} claims a disclosed-unit build but does "
                f"not name the unit, its source and the price basis. Claiming the level is "
                f"not the same as having built it."
            )
        if l.level != "unit" and not l.gap_note:
            raise AssertionError(
                f"GROUND-UP FAIL — {ticker}/{l.name} is built at '{l.level}' with no gap "
                f"stated. The rule permits a coarser level where the disclosure stops; it "
                f"has never permitted going quiet about it."
            )
    by = {k: sum(l.share_of_revenue for l in lines if l.level == k) for k in GROUND_UP_LEVELS}
    return {"ticker": ticker, "lines": len(lines), "share_by_level": by,
            "unit_share": by["unit"], "standard_version": STANDARD_VERSION}


MACRO_TOLERANCE = 0.0005        # 5bp: below the precision any of these numbers is stated to
HORIZON_CONVERGENCE = 0.02      # the explicit window runs until growth is within 2pp of terminal


@dataclass
class GrowthLine:
    """One growth rate in a model, stored the only way it can be checked.

    A nominal rate typed into a model is unfalsifiable: nobody can tell whether
    12% was meant as inflation plus one point of real growth or as inflation
    minus three. Stored as (real, inflation-path id) it recomputes, and the two
    lessons this exists to enforce become arithmetic instead of advice:
    [L-048] a scenario whose macro inputs cannot all be true at once invents its
    own bias, and [L-055] terminal growth and the terminal discount rate must
    agree about inflation.
    """
    name: str
    years: List[int]
    nominal: List[float]
    real: float = 0.0
    basis: str = "inflation + stated real"
    # a line the path deliberately does not drive -- a volume ladder, a
    # contracted price, a regulated tariff -- says so and is exempted BY NAME
    exempt_reason: Optional[str] = None


# The mappings a study may declare for an inflation-class input. CLOSED, for the reason
# every closed list in this protocol is closed [R-COC-01 AMENDED, R-ANCHOR-01]: an open one
# lets a study opt out by inventing a mapping, and "our year is different" is not a mapping.
MACRO_INFLATION_MAPPINGS = {
    # the house ladder as published, calendar year for calendar year
    "calendar": "the house ladder as published, year for year",
    # a fiscal year ending 30 June spans H2 of one calendar year and H1 of the next, so it
    # takes half of each. Arithmetic, not a judgement -- which is why it is reproducible.
    "fiscal_june": "a 30-June fiscal year: half of each of the two calendar years it spans",
    # likewise a 31-March year end: three quarters of the opening calendar year
    "fiscal_march": "a 31-March fiscal year: three quarters of the opening calendar year",
    # the terminal held flat, for a line that escalates at the long-run rate only
    "terminal_flat": "the house terminal inflation, held flat",
    # A REPORTED FACT, NOT AN ASSUMPTION. A trailing actual used to anchor a base year is a
    # filed observation with a date, which SIGCM already governs, and holding it to a
    # forward ladder would be wrong -- the ladder is a forecast and the observation is not.
    # The loophole this would otherwise open is closed by arithmetic rather than by trust:
    # an observed entry must be a SCALAR with a date, so a five-year path cannot be
    # relabelled as an observation.
    "observed": "a dated reported figure, not a forecast -- must be a single value",
}


def macro_inflation_series(path, mapping: str, n: int,
                           first_year: Optional[int] = None) -> List[float]:
    """The house ladder under one of the closed mappings above.

    Beyond the ladder's last published year the house TERMINAL is used, never an
    extrapolation of the study's own -- extrapolating the study's own is the thing
    [R-MACRO-01] forbids, and it is how a five-year array quietly invents a sixth number.
    """
    lad = dict(zip(path.inflation_years, path.inflation_path))
    y0 = first_year if first_year is not None else min(path.inflation_years)
    term = path.terminal_inflation

    def cal(y):
        return lad.get(y, term)

    if mapping == "calendar":
        return [cal(y0 + i) for i in range(n)]
    if mapping == "fiscal_june":
        return [0.5 * cal(y0 + i) + 0.5 * cal(y0 + i + 1) for i in range(n)]
    if mapping == "fiscal_march":
        return [0.75 * cal(y0 + i) + 0.25 * cal(y0 + i + 1) for i in range(n)]
    if mapping == "terminal_flat":
        return [term] * n
    raise AssertionError("unknown inflation mapping %r" % mapping)


def assert_macro_coherence(record: dict, market: Optional[str] = None,
                           ticker: str = "?") -> dict:
    """Raise unless every growth rate in a model sits on the house macro path.

    `record` is the study's own committed macro record:
        market, path_as_of, growth_lines (GrowthLine or dicts), terminal
        {g_nominal, real, rf, inflation_in_rf}, optional fx_path, and
        explicit_years with growth_at_horizon_end.

    Checks, each of which has a named failure behind it:
      1. every non-exempt nominal rate recomputes to (1+inflation)(1+real)-1 on
         the path's own ladder                                        [L-048]
      2. terminal growth = terminal inflation + a STATED real growth, and the
         inflation inside the terminal risk-free rate is that same number
                                                                      [L-055]
      3. the currency path, where the model has one, is the derived
         purchasing-power path and not a hand-set one                 [L-048]
      4. the explicit window runs until growth is within 2pp of terminal --
         a five-year window on a name compounding at 44% nominal, capitalised
         at a normalised terminal rate, puts 75-87% of value in the terminal
         and is the second half of the PHDC swing
      5. the path the study used is the path on disk, by as-of date
    """
    import macro_path as MP

    mkt = (market or record.get("market") or "").upper()
    path = MP.load(mkt)
    fails = []

    if record.get("path_as_of") and record["path_as_of"] != path.as_of:
        fails.append(
            "the study was built against the %s macro path as of %s; the path on "
            "disk is as of %s. Re-run the study or say in it which vintage it "
            "stands on -- a model quoting a path it did not use is the stale-copy "
            "defect [R-DOC-01] in another costume."
            % (mkt, record["path_as_of"], path.as_of))

    lines = []
    for g in record.get("growth_lines", []):
        lines.append(g if isinstance(g, GrowthLine) else GrowthLine(**g))
    if not lines:
        fails.append("no growth lines recorded. A model with no recorded growth "
                     "rates is not coherent by default; it is unchecked.")
    for g in lines:
        if g.exempt_reason:
            continue
        if len(g.years) != len(g.nominal):
            fails.append("%s: %d years against %d rates" % (g.name, len(g.years), len(g.nominal)))
            continue
        for y, nom in zip(g.years, g.nominal):
            want = (1.0 + path.inflation(y)) * (1.0 + g.real) - 1.0
            if abs(nom - want) > MACRO_TOLERANCE:
                fails.append(
                    "%s in %d is %.4f; the path's inflation of %.4f with the stated "
                    "real growth of %+.4f gives %.4f (out by %+.0fbp). Either the "
                    "real growth is not what the model says it is, or the rate was "
                    "typed."
                    % (g.name, y, nom, path.inflation(y), g.real, want,
                       10000 * (nom - want)))

    t = record.get("terminal") or {}
    if not t:
        fails.append("no terminal block recorded")
    else:
        want_g = path.terminal_growth(t.get("real", 0.0))
        if abs(t.get("g_nominal", 0.0) - want_g) > MACRO_TOLERANCE:
            fails.append(
                "terminal growth %.4f against terminal inflation %.4f plus the "
                "stated real growth %+.4f = %.4f. A terminal growth below the "
                "inflation inside its own discount rate is a perpetual real "
                "decline; it may be assumed, but it must be STATED as the real "
                "number it is."
                % (t.get("g_nominal", 0.0), path.terminal_inflation,
                   t.get("real", 0.0), want_g))
        if "inflation_in_rf" in t and abs(t["inflation_in_rf"] - path.terminal_inflation) > MACRO_TOLERANCE:
            fails.append(
                "the terminal discount rate embeds inflation of %.4f while the "
                "path's terminal inflation is %.4f. One economy, one inflation."
                % (t["inflation_in_rf"], path.terminal_inflation))
        if "rf" in t and abs(t["rf"] - path.terminal_rf) > MACRO_TOLERANCE:
            fails.append(
                "terminal risk-free %.4f against the derived %.4f (terminal "
                "inflation %.4f + the real-rate convention %.4f). The terminal "
                "risk-free rate is DERIVED; a quoted one is the lever the "
                "protocol prohibits outright."
                % (t["rf"], path.terminal_rf, path.terminal_inflation,
                   path.real_rate_convention))

    fx = record.get("fx_path")
    if fx:
        base = record.get("fx_base")
        want = path.fx_path(len(fx), base=base)
        off = [i for i, (a, b) in enumerate(zip(fx, want)) if abs(a - b) > max(0.01, 0.002 * b)]
        if off:
            fails.append(
                "the currency path is not the derived purchasing-power path: year "
                "%d has %.4f against %.4f. Escalating costs at domestic inflation "
                "while depreciating the currency at some other rate is the same "
                "event counted once and ignored once."
                % (off[0] + 1, fx[off[0]], want[off[0]]))

    # ---- 6. EVERY INFLATION-CLASS INPUT, NOT ONLY THE DECLARED GROWTH LINES ----
    # [added 03-Sep-2026 after EGCH]. Checks 1-5 read what a study DECLARES. EGCH declared
    # its one growth line exempt on grounds that were perfectly true -- its revenue is built
    # from tonnes and dollar prices, so there is no nominal growth rate on that line to sit
    # on the ladder -- while an input called cpi_path, nowhere in the record, drove the
    # purchasing-power wedge (and so the entire currency path, and so both the translation of
    # dollar revenue into pounds AND the gas cost) and escalated every domestic cost line.
    # It read 10.0 / 7.0 / 6.0 / 5.0 / 5.0 against a house ladder of 16.0 / 12.0 / 9.0 / 7.5
    # / 7.0 and terminated at 5% against a house terminal of 7% the same record carried.
    #
    # The study's own gap review named it in plain words -- "the study's own Egyptian
    # inflation path" -- inside the heading whose purpose is to catch it, and passed, because
    # the number was DERIVED rather than typed and nobody asked derived from what.
    #
    # So a study must now DECLARE every inflation-class input it registers, with the mapping
    # that produces it from the house ladder, and this reproduces each one. The rule is not
    # "no inflation array" -- a fiscal year straddling two calendar years legitimately needs
    # its own mapping -- it is that the mapping is stated and reproducible from outside.
    infl = record.get("inflation_inputs")
    if infl is None:
        fails.append(
            "no inflation_inputs block. A study must name EVERY inflation-class input it "
            "registers and the mapping that derives it from the house ladder, even if that "
            "list is empty -- declare it as [] where the model genuinely carries none. "
            "EGCH's growth lines were all legitimately exempt while an undeclared cpi_path "
            "drove the currency path and every cost escalator, and both this assertion and "
            "the study's own gap review passed it.")
    else:
        if not isinstance(infl, (list, tuple)):
            fails.append("inflation_inputs must be a list of {key, mapping, values} entries")
            infl = []
        for e in infl:
            key = (e or {}).get("key") or "?"
            mapping = (e or {}).get("mapping")
            vals = (e or {}).get("values")
            if mapping not in MACRO_INFLATION_MAPPINGS:
                fails.append(
                    "inflation input %r declares mapping %r, which is not one of %s. The "
                    "list is CLOSED for the reason every closed list in this protocol is "
                    "closed: an open one lets any study opt out by inventing a mapping, and "
                    "adding one is a rule amendment."
                    % (key, mapping, ", ".join(sorted(MACRO_INFLATION_MAPPINGS))))
                continue
            if mapping == "observed":
                if isinstance(vals, (list, tuple)):
                    fails.append(
                        "inflation input %r is declared 'observed' but carries %d values. An "
                        "observation is a single dated figure; a per-year array is a "
                        "forecast, and relabelling one as the other is how a study would "
                        "opt out of this check."
                        % (key, len(vals)))
                elif not (e or {}).get("date"):
                    fails.append(
                        "inflation input %r is declared 'observed' with no date. A reported "
                        "figure without its date is not an observation [SIGCM]." % key)
                continue
            if not isinstance(vals, (list, tuple)) or not vals:
                fails.append("inflation input %r declares no values to check" % key)
                continue
            # A BOUNDED, COUNTED, REASONED EXEMPTION FOR LEADING YEARS. ARCC's first
            # forecast year carries an EVIDENCED company anchor — its own filed price and
            # cost step — and its years two to five are the house ladder to the basis
            # point. That is legitimate and the study already reasons it. What is NOT
            # legitimate is EGCH's shape, where a whole line was exempted and an
            # undeclared array did the work, so the exemption here is a COUNT of leading
            # years with a reason, never a blanket.
            head = int((e or {}).get("exempt_head") or 0)
            if head:
                if not (e or {}).get("exempt_reason"):
                    fails.append(
                        "inflation input %r exempts its first %d year(s) with no reason. An "
                        "exemption is a claim and carries its evidence." % (key, head))
                if head >= len(vals):
                    fails.append(
                        "inflation input %r exempts all %d of its years, which is not an "
                        "exemption but an opt-out. Exempt the leading years an evidenced "
                        "anchor actually covers." % (key, len(vals)))
                    continue
                vals = list(vals)[head:]
            want = macro_inflation_series(path, mapping, len(vals),
                                          (e or {}).get("first_year"))
            off = [i for i, (a, b) in enumerate(zip(vals, want))
                   if abs(float(a) - b) > MACRO_TOLERANCE]
            if off:
                i = off[0]
                fails.append(
                    "inflation input %r, year %d (after %d exempted leading year(s)): "
                    "the study carries %.4f and the house ladder under the declared %r "
                    "mapping gives %.4f (out by %+.0fbp). A study may not carry an "
                    "inflation number of its own [R-MACRO-01]; if the mapping is right the "
                    "array was typed, and if the array is right the mapping is not what "
                    "the study says it is."
                    % (key, i + 1, head, float(vals[i]), mapping, want[i],
                       10000 * (float(vals[i]) - want[i])))

    n = record.get("explicit_years")
    gend = record.get("growth_at_horizon_end")
    if n is not None and gend is not None and t:
        gap = abs(gend - t.get("g_nominal", 0.0))
        if gap > HORIZON_CONVERGENCE:
            fails.append(
                "the explicit window ends with growth at %.2f%% against a terminal "
                "of %.2f%% -- %.1fpp apart. The window must run until the two are "
                "within %.0fpp, or the terminal capitalises a growth rate the model "
                "never reached and takes most of the value with it."
                % (100 * gend, 100 * t.get("g_nominal", 0.0), 100 * gap,
                   100 * HORIZON_CONVERGENCE))

    if fails:
        raise AssertionError(
            "MACRO COHERENCE FAIL -- %s (%s):\n  - %s" % (ticker, mkt, "\n  - ".join(fails)))
    return {"ticker": ticker, "market": mkt, "path_as_of": path.as_of,
            "growth_lines": len(lines),
            "exempt_lines": sum(1 for g in lines if g.exempt_reason),
            "terminal_growth": (record.get("terminal") or {}).get("g_nominal"),
            "terminal_inflation": path.terminal_inflation,
            "terminal_rf_derived": path.terminal_rf,
            "standard_version": STANDARD_VERSION}


NCI_BASES = {
    "subsidiary": "the subsidiaries carrying the minority, valued on their own disclosed "
                  "economics, and the minority percentage of that deducted -- the standard",
    "value_share": "the minority's share of EQUITY value, proxied where the subsidiaries are "
                   "not separately disclosed; the proxy and its source must be named",
    "none_disclosed": "the company has no minority interests -- must be evidenced, not assumed",
}

ASSOCIATE_BASES = ("market", "book", "none")
CASH_TREATMENTS = ("added_at_face", "inside_the_flow", "none")
WEIGHT_BASES = ("gross", "net", "not_applicable")


def assert_bridge(record: dict, ticker: str = "?") -> dict:
    """Raise unless the enterprise-to-equity bridge obeys the standing rules.  [R-BRIDGE-01]

    Four defects this closes, each of which shipped:

      THE BRIDGE STOOD ON A STALE SHEET. PHDC's bridge stood on 31-Dec-2025
      while a reviewed 31-Mar-2026 balance sheet sat on the company's own
      archive, in the same document set the study had already drawn its
      first-quarter income figures from. AMOC's did the same. The bridge stands
      on the LATEST DISCLOSED sheet, and the record must name the register that
      establishes what "latest" is -- a name with neither a sweep register nor
      an investor-relations register is a FAIL, not a skip [R-ENF-04].

      THE MINORITY CAME OUT AT BOOK, OR NOT AT ALL. The model capitalises 100%
      of the subsidiaries' cash flow, so the minority's claim is worth its share
      of that VALUE, not what it historically cost. CLHO deducted book and
      overstated parent equity by roughly a third of the minority; PHDC deducted
      nothing at all while dividing by parent shares. Book is published as a
      reference framing and is never the adopted basis.

      THE CASH WAS CHARGED FOR TWICE. AMOC discounted its operations at a
      net-debt-weighted rate -- which, on a net-cash company, levers the equity
      weight above one and puts the operating rate above the cost of equity --
      and then added the same cash back at face in the bridge. A reader may
      value the whole firm at a blended rate and add nothing, or value the
      operations at the operating rate and add the cash. Not both.

      THE ARITHMETIC WAS NOT CHECKED. The lines are asserted to sum to the
      equity value, and the equity value to divide to the per-share figure.
    """
    fails = []
    r = record or {}

    bs = r.get("balance_sheet_date")
    latest = r.get("latest_disclosed_date")
    src = r.get("latest_disclosed_source")
    if not bs:
        fails.append("no balance-sheet date recorded: the bridge does not say which sheet it stands on")
    if not latest or not src:
        fails.append(
            "the record does not establish what the LATEST disclosed balance sheet is "
            "(need latest_disclosed_date and latest_disclosed_source naming the sweep or "
            "investor-relations register). A study with neither register cannot claim to "
            "stand on the latest sheet, and an unestablished answer is not a clean one.")
    elif bs and bs != latest:
        fails.append(
            "the bridge stands on the %s balance sheet while the latest disclosed is %s "
            "(%s). A filing on the company's own archive that nobody opened is the "
            "defect this rule exists for." % (bs, latest, str(src)[:120]))

    nci = r.get("nci") or {}
    basis = nci.get("basis")
    if basis not in NCI_BASES:
        fails.append("minority-interest basis %r is not one of %s"
                     % (basis, ", ".join(sorted(NCI_BASES))))
    elif basis == "none_disclosed":
        if not nci.get("evidence"):
            fails.append("the record claims there are no minority interests but cites no "
                         "evidence. Absence is evidenced, never assumed.")
    else:
        if nci.get("deduction") in (None, 0) and not nci.get("zero_reason"):
            fails.append("a minority basis is named but nothing is deducted, and no reason "
                         "is given. The 30-Aug-2026 PHDC edition deducted nothing while "
                         "dividing by parent shares.")
        for alt in ("book", "profit_share", "proportional"):
            if alt not in nci:
                fails.append("the %s reference framing for the minority is not published. "
                             "The adopted basis is published beside the alternatives so a "
                             "reader can see the choice, not just its result." % alt)
        if basis == "value_share" and not nci.get("proxy_source"):
            fails.append("the value-share basis is a PROXY where the minority's subsidiaries "
                         "are not separately disclosed; the proxy and its source must be named.")
        if nci.get("applied_to") == "enterprise_value":
            fails.append("the minority is deducted from ENTERPRISE value. That applies an "
                         "equity share to an enterprise number and hands the minority a share "
                         "of growth assets it does not own.")

    cash = r.get("cash") or {}
    treat = cash.get("treatment")
    wb = cash.get("weights_basis")
    if treat not in CASH_TREATMENTS:
        fails.append("cash treatment %r is not one of %s" % (treat, ", ".join(CASH_TREATMENTS)))
    if wb not in WEIGHT_BASES:
        fails.append("discount-rate weights basis %r is not one of %s"
                     % (wb, ", ".join(WEIGHT_BASES)))
    if treat == "added_at_face" and wb == "net":
        fails.append(
            "cash is added at face in the bridge AND netted inside the discount-rate "
            "weights. That is the same cash charged twice -- once by discounting the "
            "operations as though holding a deposit made them riskier, and once by "
            "counting the deposit at par.")

    assoc = r.get("associates") or {}
    if assoc.get("basis") not in ASSOCIATE_BASES:
        fails.append("associates basis %r is not one of %s"
                     % (assoc.get("basis"), ", ".join(ASSOCIATE_BASES)))
    elif assoc.get("basis") == "book" and assoc.get("listed") and not assoc.get("book_reason"):
        fails.append("a LISTED associate is carried at book with no reason given; where a "
                     "market price exists it is the evidence.")

    div = r.get("dividend") or {}
    if div.get("deducted"):
        if not div.get("declared_date") or not bs:
            fails.append("a dividend is deducted with no declaration date to test against "
                         "the balance-sheet date")
        elif div["declared_date"] <= bs:
            fails.append(
                "a dividend declared %s is deducted from a bridge standing on the %s "
                "balance sheet -- it is already out of the equity it is being deducted "
                "from, so it comes out twice." % (div["declared_date"], bs))

    lines = r.get("lines") or []
    eq = r.get("equity_value")
    sh = r.get("shares_mn")
    ps = r.get("per_share")
    if lines and eq is not None:
        tot = sum(float(l.get("value", 0.0)) for l in lines)
        if abs(tot - float(eq)) > max(1.0, 0.0005 * abs(float(eq))):
            fails.append("the bridge lines sum to %.1f against a stated equity value of "
                         "%.1f. A bridge that does not foot is not a bridge." % (tot, eq))
    if eq is not None and sh and ps is not None:
        if abs(float(eq) / float(sh) - float(ps)) > max(0.01, 0.001 * abs(float(ps))):
            fails.append("equity value %.1f over %.1f shares is %.4f, not the stated %.4f"
                         % (eq, sh, float(eq) / float(sh), ps))

    if fails:
        raise AssertionError(
            "BRIDGE FAIL -- %s:\n  - %s" % (ticker, "\n  - ".join(fails)))
    return {"ticker": ticker, "balance_sheet_date": bs,
            "nci_basis": basis, "nci_deduction": nci.get("deduction"),
            "cash_treatment": treat, "weights_basis": wb,
            "lines": len(lines), "per_share": ps,
            "standard_version": STANDARD_VERSION}


# --------------------------------------------------------------------------
# LENS ARCHITECTURE v2  [R-LENS-03]
#
# The failure. PHDC's central was a weighted blend of four lenses at typed
# weights -- 45% discounted cash flow, 15% book value, 20% an earnings multiple,
# 20% normalised earnings power -- and three of the four value a developer on
# its REPORTED ACCOUNTING EARNINGS AND HISTORICAL-COST BOOK. For a company whose
# value sits in an undelivered order book carried at historical cost in a
# currency that has lost most of its value since 2022, those three measure a
# floor and not a value. The cash-flow lens landed within 2.2% of the market
# price; the blend landed 28% below it. Nothing in the study was wrong except
# the architecture, and the weights had never cleared any out-of-sample bar --
# they were chosen, written down, and inherited.
#
# What is adopted. ONE class primary is the central. The other lenses are
# CROSS-CHECKS: published in the same table, defining the bear/full envelope as
# the range of PRESENT-VALUE reads, never averaged into the answer. Whether any
# blend beats the primary alone is a question for the valuation calibration to
# answer out of sample [R-VCAL-01]; until it does, the typed blend is retired,
# because it never cleared the bar it was always required to clear.
#
# The registry is keyed on lessons_register.CLASSES BY IMPORT. A second taxonomy
# for the same companies is how two registers drift apart, and this repository
# has already paid for that once.
LENS_KINDS = {
    "dcf":          "a present-value discounted cash flow on the study's own drivers",
    "rnav":         "a PRESENT-VALUE net asset value: land at cost with a labelled market "
                    "cross-check, absorption on the company's own delivery rate, discounted "
                    "on the cost-of-capital schedule -- never a gross NAV",
    "sotp":         "disciplined sum of the parts, each part on its own present-value lens",
    "ddm":          "dividend discount model",
    "residual_income": "residual income on the same clock as the book it starts from",
    "ev_ebitda_own_history": "enterprise value to EBITDA on the company's OWN history",
    "ev_per_tonne": "enterprise value per tonne of capacity, on transactions or own history",
    "replacement_cost": "what the assets would cost to build, at today's prices",
    "relative_multiple": "forward earnings times a multiple from peers or own history -- "
                         "never from the current price, which is circular",
    "normalised_earnings": "mid-cycle earnings capitalised Fisher-consistently, at a real "
                           "rate against real earnings or at a nominal rate net of growth",
    "book_value":   "a DISCLOSED FLOOR, published as such -- not a lens and never weighted",
}

# class -> (primary, permitted cross-checks). The primary is the central.
# NORMALISED EARNINGS IS NOT A DEVELOPER LENS, and its absence from the two
# developer rows is deliberate rather than an oversight. A developer recognising
# revenue on handover reports earnings that are an accident of which project
# completed in which year; capitalising a mid-cycle figure treats that schedule
# as if it were a steady state. It was PHDC's worst read at EGP 5.17 a share
# against a cash-flow lens of 14.86, and it carried a fifth of the weight.
LENS_REGISTRY = {
    "real-estate developer, off-plan, percentage-of-completion":
        ("dcf", ("rnav", "relative_multiple", "book_value")),
    "real-estate developer, off-plan, point-in-time on handover":
        ("dcf", ("rnav", "relative_multiple", "book_value")),
    "telecom operator":
        ("dcf", ("ev_ebitda_own_history", "relative_multiple", "book_value")),
    "cement and heavy industrial":
        ("dcf", ("ev_per_tonne", "replacement_cost", "relative_multiple", "book_value")),
    "petrochemical":
        ("dcf", ("ev_ebitda_own_history", "replacement_cost", "relative_multiple", "book_value")),
    "refiner, commodity pass-through on a thin spread":
        ("dcf", ("ev_ebitda_own_history", "replacement_cost", "relative_multiple", "book_value")),
    "airline":
        ("dcf", ("ev_ebitda_own_history", "relative_multiple", "book_value")),
    # DELIBERATELY THE SAME ROW AS THE AIRLINE AND TELECOM ONES. A vertically integrated
    # generic and branded manufacturer is valued on its cash flows with an own-history
    # enterprise multiple, a peer multiple and book beside them; nothing about the
    # industry gives a DIFFERENT lens the weight, which is the only ground [R-LENS-03]
    # allows for adding a class here. The class exists because lessons_register.CLASSES
    # keys the LESSON taxonomy, where a finding about registered price ceilings or an
    # active-ingredient import bill is not evidence about an airline. Two classes may
    # share a lens set; they may not share a lesson set.
    "pharmaceutical manufacturer, generic and branded":
        ("dcf", ("ev_ebitda_own_history", "relative_multiple", "book_value")),
    "bank":
        ("ddm", ("residual_income", "relative_multiple", "book_value")),
    "holding company":
        ("sotp", ("relative_multiple", "book_value")),
    "commodity and metals":
        ("dcf", ("replacement_cost", "relative_multiple", "book_value")),
    # A SHIP IS NOT A KILN, AND THE DIFFERENCE IS IN WHICH CROSS-CHECK MEANS ANYTHING.
    # Replacement cost is the strongest lens here rather than the weakest: secondhand
    # vessel values are quoted by brokers in a liquid international market, so "what the
    # assets are worth" is an OBSERVED PRICE rather than an industry rule of thumb. The
    # multiple on the company's own history matters for the opposite reason -- day rates
    # are cyclical enough that any single year's earnings multiple is close to
    # meaningless, and only the company's own span across a cycle says anything.
    # SUM-OF-THE-PARTS IS A CROSS-CHECK HERE AND NOT A PRIMARY. It is a holdco's primary
    # because a holdco IS its stakes; on an operating fleet it earns its place for a
    # narrower reason — the legs sit on materially different contract structures, one
    # earning under long-term contracts and one exposed to spot day rates, so a single
    # group multiple averages two businesses that reprice on different clocks. Summing
    # them is a real reading; it is not the answer, because the legs share one balance
    # sheet, one crew pool and one management.
    "marine logistics and shipping, chartered fleet on global day rates":
        ("dcf", ("replacement_cost", "ev_ebitda_own_history", "relative_multiple",
                 "sotp", "book_value")),
    # A diversified industrial whose legs sit on different CONTRACT STRUCTURES: a cable
    # is made and sold into a market at a price the market sets, a turnkey project is a
    # multi-year contract whose margin turns on which phases complete when. DCF primary,
    # with a disciplined sum of the parts earning a place beside the usual cross-checks
    # because the legs would be valued differently by anyone buying them apart — the same
    # argument the shipping row above makes for its own SOTP entry, and not merely that
    # the industry differs. Replacement cost is NOT here: a cable plant cannot be sold
    # abroad the way a vessel can, so replacement cost is an industry rule of thumb rather
    # than an observed price. NORMALISED EARNINGS POWER IS DELIBERATELY ABSENT, on the two
    # developer rows' reasoning: a contractor's reported earnings are an accident of
    # completion timing, so normalising them normalises noise.
    "diversified industrial with a contracting arm":
        ("dcf", ("ev_ebitda_own_history", "relative_multiple", "sotp", "book_value")),
}

# RNAV may be a class PRIMARY only where the disclosure supports it. Where land
# value per square metre is an undisclosed gap, the primary stays the discounted
# cash flow and RNAV is a cross-check -- SIGCM clause 8, stop rather than invent.
RNAV_PRIMARY_REQUIRES = (
    "disclosed land area by project",
    "a sourced land value per unit of area, or a transaction that establishes one",
    "the company's own delivery or absorption rate",
)


def _lens_classes_match_register():
    """The registry is keyed on the lessons register's classes, by import."""
    try:
        import lessons_register as LR
    except Exception:                                        # noqa: BLE001
        return                                               # checked in CI, not here
    missing = sorted(set(LR.CLASSES) - set(LENS_REGISTRY))
    extra = sorted(set(LENS_REGISTRY) - set(LR.CLASSES))
    if missing or extra:
        raise AssertionError(
            "LENS REGISTRY FAIL -- the registry and the lessons register disagree about "
            "the classes. Missing from the registry: %s. Not a registered class: %s. "
            "A second taxonomy for the same companies is how two registers drift apart."
            % (missing or "none", extra or "none"))


_lens_classes_match_register()


# Macro and cost-of-capital dials: moving one of these to manufacture a bear or a
# bull is the construction [R-MACRO-01] forbids, because they are DERIVED from the
# house path and share its terminal inflation. Business drivers -- volumes, prices,
# margins, conversion, absorption, delivery rate -- are the ones a range may move.
MACRO_DIALS = (
    "terminal growth", "terminal_growth", "perpetuity growth", "terminal rate",
    "terminal risk-free", "terminal risk free", "risk-free", "risk free",
    "inflation", "cost of equity", "cost_of_equity", "cost of capital", "wacc",
    "discount rate", "discount_rate", "ke", "kd", "exit multiple",
)


def assert_lens_design(record: dict, ticker: str = "?") -> dict:
    """Raise unless the study's lens architecture obeys [R-LENS-03].

    `record`: class, primary {kind, value}, cross_checks [{kind, value, note}],
    envelope {low, high}, central, and for each lens whatever its own clause
    needs -- a relative multiple's source, a normalised-earnings basis, the
    RNAV's disclosure evidence.
    """
    fails = []
    r = record or {}
    cls = r.get("class")
    if cls not in LENS_REGISTRY:
        fails.append("class %r is not registered. The lens architecture is decided by "
                     "class, so an unregistered class has no primary." % cls)
        raise AssertionError("LENS FAIL -- %s:\n  - %s" % (ticker, "\n  - ".join(fails)))

    want_primary, permitted = LENS_REGISTRY[cls]
    # the class's own primary is always an acceptable lens for that class,
    # whichever role it plays: where RNAV substitutes as the primary on a
    # developer, the cash-flow lens becomes a cross-check and must be permitted
    permitted = tuple(permitted) + (want_primary,)
    prim = r.get("primary") or {}
    if prim.get("kind") != want_primary:
        # a class primary may be substituted only with a stated reason, and never
        # for a lens the class does not permit at all
        if prim.get("kind") not in permitted or not prim.get("substitution_reason"):
            fails.append(
                "the primary lens is %r; the registry gives %r for this class. A "
                "substitution is permitted only from the class's own cross-checks and "
                "only with a stated reason." % (prim.get("kind"), want_primary))
    if prim.get("kind") == "rnav":
        have = set(prim.get("disclosure_evidence") or [])
        missing = [k for k in RNAV_PRIMARY_REQUIRES if k not in have]
        if missing:
            fails.append(
                "RNAV is the primary but the disclosure it needs is not evidenced: %s. "
                "Where land value per unit of area is an undisclosed gap the primary "
                "stays the cash-flow lens and RNAV is a cross-check." % "; ".join(missing))
    if prim.get("value") is None and not (prim.get("range") or {}):
        fails.append("the primary lens carries neither a value nor a published range")
    pr = prim.get("range") or {}
    if pr and not (pr.get("low") is not None and pr.get("high") is not None
                   and float(pr["low"]) <= float(pr["high"])):
        fails.append("the primary's published range is not an ordered low/high pair")

    # THE SENTENCE THIS RULE IS NAMED FOR WAS THE ONE THING NOT CHECKED. [R-LENS-03] is
    # "ONE CLASS PRIMARY *IS* THE CENTRAL", and every clause above tests the primary's
    # KIND, its permitted cross-checks, whether book is weighted, whether a multiple is
    # circular -- and none of them ever compared the primary's VALUE with the answer the
    # study publishes. So a study could name a conforming primary and publish something
    # else entirely, which is what ADNOCDIST does: its published central reproduces to
    # 8.9e-16 as 0.40 x cash flow + 0.25 x normalised + 0.20 x relative + 0.15 x BOOK --
    # the retired four-lens blend, with book value carrying weight, which this rule
    # forbids outright as a disclosed floor that is never weighted.
    #
    # check_lens_vocabulary reads the DOCUMENT for the words; this holds the QUANTITY,
    # which is [R-MACRO-01]'s lesson -- a check that reads what a process DECLARES is not
    # checking what the process DOES, and where a rule governs a quantity, hold it.
    #
    # BOTH SHAPES ARE HONEST AND BOTH ARE TESTED. A primary carrying a VALUE must equal
    # the central. A primary carrying only a RANGE -- which the clause above deliberately
    # permits, because a two-sided answer must not be forced to invent a point -- must
    # CONTAIN it. A record exposing neither a central nor a comparable primary is not
    # failed here: `central` is optional in this record's shape and inventing a
    # requirement for it belongs to a rule amendment rather than to an assertion.
    # ------------------------------------------------- a TWO-SIDED answer
    # [ADDED 06-09-2026] THE IDENTITY CLAUSE WAS FIRING ON WORK THAT WAS RIGHT.
    # A study whose answer depends on a contested judgement publishes BOTH
    # framings side by side and is forbidden to average them, so it has no
    # scalar central to expose -- and the check that a record must expose one
    # therefore demanded the very midpoint the dual-framing rule prohibits.
    # Three studies were in that state. Per [R-COC-01] the check is RE-POINTED
    # rather than widened or switched off: a two-sided record is held to a test
    # of the same claim, branch-wise, and the test is HARDER than the one it
    # replaces, because `two_sided` must not become the cheapest route past the
    # clause that catches a blend.
    _ts = bool(prim.get("two_sided"))
    _branches = prim.get("branches") or []
    if _ts:
        if len(_branches) < 2:
            fails.append(
                "the primary declares two_sided and carries %d branch(es). A two-sided "
                "answer IS its branches: without them the record states that there is no "
                "single central and never says what the two answers are, which switches "
                "the identity clause off rather than satisfying it."
                % len(_branches))
        seen_v = []
        for i, b in enumerate(_branches):
            if not str((b or {}).get("label") or "").strip():
                fails.append("branch %d carries no label. A reader shown two numbers and "
                             "not told which judgement produces which has been shown one "
                             "number twice." % (i + 1))
            bv = (b or {}).get("value")
            if not isinstance(bv, (int, float)):
                fails.append("branch %d carries no numeric value" % (i + 1))
            else:
                seen_v.append(float(bv))
        if len(seen_v) >= 2 and len(set(round(v, 10) for v in seen_v)) < len(seen_v):
            fails.append(
                "two branches carry the same value. Two framings that reach the same "
                "answer are not a two-sided answer; the judgement is not contested.")
        if prim.get("value") is not None:
            fails.append(
                "the primary declares two_sided AND carries a scalar value of %.6f. It is "
                "one or the other: a scalar beside the branches is the single number a "
                "reader will quote, and choosing it is the averaging this rule forbids."
                % float(prim["value"]))
        if r.get("central") is not None:
            fails.append(
                "the record declares a two-sided primary and also exposes a central of "
                "%.6f. A two-sided answer has no central -- that is what makes it "
                "two-sided." % float(r["central"]))
        if pr and seen_v:
            _lo, _hi = float(pr["low"]), float(pr["high"])
            if _lo - abs(_lo) * 1e-9 > min(seen_v) or _hi + abs(_hi) * 1e-9 < max(seen_v):
                fails.append(
                    "the primary's published range %.6f to %.6f does not contain its own "
                    "branches (%s). An envelope that excludes the study's own answer is "
                    "not that study's envelope."
                    % (_lo, _hi, ", ".join("%.6f" % v for v in seen_v)))
    elif _branches:
        fails.append(
            "the primary carries %d branches and does not declare two_sided. A record "
            "that publishes two answers and does not say so is read as single-sided by "
            "everything downstream, and the branch nobody reads is the one that "
            "disagrees." % len(_branches))
    _pub = r.get("central")
    if _pub is not None:
        _pub = float(_pub)
        _pv = prim.get("value")
        if _pv is not None:
            if abs(float(_pv) - _pub) > max(abs(_pub), 1.0) * 1e-9:
                fails.append(
                    "the primary lens reads %.6f and the record publishes a central of "
                    "%.6f. ONE CLASS PRIMARY IS THE CENTRAL: a central that is not the "
                    "primary's own answer is some other construction, and the commonest "
                    "one is the weighted blend this rule retired." % (float(_pv), _pub))
        elif pr:
            _lo, _hi = float(pr["low"]), float(pr["high"])
            if not (_lo - abs(_lo) * 1e-9 <= _pub <= _hi + abs(_hi) * 1e-9):
                fails.append(
                    "the record publishes a central of %.6f and the primary's own range "
                    "runs %.6f to %.6f, which does not contain it." % (_pub, _lo, _hi))

    seen = []
    for x in (r.get("cross_checks") or []):
        k = x.get("kind")
        seen.append(k)
        if k not in LENS_KINDS:
            fails.append("cross-check %r is not a registered lens kind" % k)
            continue
        if k not in permitted:
            fails.append("cross-check %r is not permitted for this class" % k)
        if k == "relative_multiple":
            src = (x.get("multiple_source") or "").lower()
            # look for the multiple being TAKEN from the price, not for the words
            # appearing at all -- a source that says "never the current price" is
            # doing the right thing, and a check that cannot tell the difference
            # is one people learn to write around
            circular = any(t in src for t in (
                "from the current price", "from the price", "from spot",
                "implied by the current price", "implied by the price",
                "at the current price", "the multiple the shares trade at",
                "today's multiple", "the market's own multiple"))
            if not src:
                fails.append("the relative multiple names no source for its multiple")
            elif circular:
                fails.append(
                    "the relative multiple takes its multiple from the CURRENT PRICE, which "
                    "values the company at what it already trades at. The multiple comes "
                    "from peers or from the company's own history.")
            # ---- THE STRING WAS THE WHOLE CHECK, AND A STRING IS AN ATTESTATION
            # [ADDED 03-Sep-2026, found by the AMOC re-strike]. Everything above
            # this line reads the multiple_source PROSE. AMOC's record said the
            # multiple came "from the company's own history and its regional
            # peers, never a multiple read off the current price" while its code
            # computed ev_trailing = MARKET CAP + net debt and divided by base-year
            # EBITDA -- the traded multiple exactly, re-rated by zero. The gate
            # read the sentence, found the reassuring words, and passed. The
            # re-strike is what exposed it: the lens moved +51% when the price
            # moved +48%, which is what a lens anchored on the price does and what
            # a lens anchored on history cannot do.
            #
            # So the claim is now ARITHMETIC. A relative multiple commits the
            # multiple it adopted and the three numbers that would reproduce the
            # traded one, and the gate divides. A record that supplies no
            # ingredients has switched the check off rather than passed it --
            # [R-COC-01]'s lesson, which is why they are REQUIRED and not optional.
            circ = x.get("circularity") or {}
            mult = x.get("multiple")
            if mult is None:
                fails.append(
                    "the relative multiple does not commit the MULTIPLE it adopted. A "
                    "source named in prose is an attestation; the multiple is the thing "
                    "that can be checked.")
            need = ("spot", "shares", "net_debt", "metric_value")
            missing = [k for k in need if circ.get(k) is None]
            if missing:
                fails.append(
                    "the relative multiple commits no circularity check (%s). The traded "
                    "multiple is (spot x shares + net debt) / the metric, and a lens that "
                    "cannot be compared with it is one nobody can tell apart from the "
                    "price." % ", ".join(missing))
            elif mult is not None:
                try:
                    _mv = float(circ["metric_value"])
                    _traded = (float(circ["spot"]) * float(circ["shares"])
                               + float(circ["net_debt"])) / _mv
                except (TypeError, ValueError, ZeroDivisionError):
                    fails.append("the relative multiple's circularity check does not "
                                 "compute: its own numbers do not divide.")
                else:
                    x["_traded_multiple"] = _traded
                    if _traded and abs(float(mult) / _traded - 1.0) < 0.005:
                        fails.append(
                            "the relative multiple %.4fx IS the traded multiple %.4fx to "
                            "within half a per cent. Whatever the source says, this lens "
                            "values the company at what it already trades at, and its only "
                            "distance from the price is the bridge." % (float(mult), _traded))
        if k == "normalised_earnings":
            basis = (x.get("basis") or "").lower()
            if "real" not in basis and "less growth" not in basis and "ke - g" not in basis:
                fails.append(
                    "normalised earnings is capitalised at a nominal rate with no growth "
                    "netted and no real-terms basis stated. In a currency whose discount "
                    "rate embeds inflation that is a perpetual real decline, not prudence.")
        if k == "book_value" and x.get("weight"):
            fails.append("book value carries a weight. It is a disclosed floor, published "
                         "as such, and is never weighted into a central.")

    # the defect this rule exists for: a typed blend
    weights = [x.get("weight") for x in (r.get("cross_checks") or []) if x.get("weight")]
    if prim.get("weight") or weights:
        fails.append(
            "the lenses carry weights. The central is the class primary; the cross-checks "
            "are published beside it and define the envelope. A typed weight is a free "
            "parameter that has never cleared an out-of-sample test, and the blend it "
            "produced put PHDC 28% below a market its own cash-flow lens sat within 2.2% of.")

    central = r.get("central")
    if central is not None and prim.get("value") is not None:
        if abs(float(central) - float(prim["value"])) > max(0.01, 0.001 * abs(float(central))):
            fails.append("the published central %.4f is not the primary lens's %.4f. The "
                         "central IS the primary." % (central, prim["value"]))
    elif central is not None and (prim.get("range") or {}):
        # a primary published as a range: the exposed figure must sit inside it and
        # must say what it is, because a midpoint presented as an answer is the
        # averaging the dual-framing rule forbids
        pr = prim["range"]
        if not (float(pr["low"]) <= float(central) <= float(pr["high"])):
            fails.append("the exposed central %.4f sits outside the primary's own published "
                         "range %.4f to %.4f" % (central, pr["low"], pr["high"]))
        if not r.get("central_note"):
            fails.append("the primary is published as a range and a single figure is exposed "
                         "with no note saying what it is. A midpoint presented as an answer "
                         "is the averaging the dual-framing rule forbids; exposing one for a "
                         "gate to read is fine, and it says so.")

    # ---------------------------------------------------------------- the origin
    # THE BEAR AND THE BULL ARE CLAIMS AND MUST SAY WHERE THEY CAME FROM
    # [per instruction, 03-Sep-2026]. Until now this gate checked the envelope's
    # ARITHMETIC -- that low and high are the min and max of the present-value
    # reads -- and never asked what was moved to produce them. That is the whole
    # question. A range produced by flexing a driver across the span the company's
    # own filings actually show is evidence; a range produced by nudging terminal
    # growth and the discount rate until the corners look wide enough is a free
    # parameter wearing a range's clothes, and its width is the analyst's choice
    # rather than the world's.
    #
    # It is also INCOHERENT under [R-MACRO-01]: terminal growth and the terminal
    # risk-free rate both contain the same terminal inflation, so the bull corner
    # of a growth-by-discount-rate grid is inflation high and low simultaneously,
    # and the two corners a study would publish as bear and bull are the two least
    # coherent cells in it. That is [L-048] and [L-055] rebuilt as a matrix.
    #
    # What is NOT prohibited is a framing the protocol itself requires to be
    # published both ways -- the CDS and rating premium bases of [R-COC-01] are
    # the standing example, and TMGH's envelope legitimately spans them. Those are
    # named, not invented, so the record names which rule sanctions them.
    pr = prim.get("range") or {}
    if pr:
        rb = prim.get("range_basis") or {}
        if not rb:
            fails.append(
                "the primary publishes a range -- which is what the study will show as "
                "its bear and bull -- and no range_basis says where it came from. The "
                "origin of the range is a claim and is declared: what was moved, "
                "between which values, on what evidence, and that the macro path "
                "stood still while it moved.")
        else:
            for f in ("driver", "evidence"):
                if not str(rb.get(f) or "").strip():
                    fails.append("range_basis names no %s. A range whose origin is not "
                                 "stated cannot be audited by anyone." % f)
            for side in ("low", "high"):
                if rb.get(side) is None:
                    fails.append("range_basis does not say what value the driver took at "
                                 "the %s end of the range." % side)
            sanctioned = str(rb.get("sanctioned_framing") or "").strip()
            # `driver` NAMES WHAT MOVED, and nothing else. A study that also writes
            # here which dials stood still trips this check while doing exactly the
            # right thing -- so the MESSAGE says which of the two mistakes it is. A
            # regex that cut the text at a holding word was tried and backed out: the
            # dial usually precedes the verb ("the cost of capital ... is held"), so it
            # caught one phrasing and not the common one, and a check that half-works on
            # prose is worse than one whose message tells the author where the sentence
            # belongs. The structured assertion that the macro stood still is
            # macro_held, checked immediately below.
            drv = str(rb.get("driver") or "").lower()
            hits = [t for t in MACRO_DIALS if t in drv]
            if hits and not sanctioned:
                fails.append(
                    "the range is produced by moving %s -- a macro or cost-of-capital "
                    "dial, not a business driver. Under [R-MACRO-01] terminal growth and "
                    "the terminal risk-free rate are DERIVED from one house path and both "
                    "carry the same terminal inflation, so the corners of such a range are "
                    "internally contradictory and its width is chosen rather than "
                    "observed. Flex the crux in observable units and hold the macro path "
                    "fixed, or name the rule that requires the framing to be published "
                    "both ways. IF THE MACRO PATH WAS HELD AND THIS FIELD SAYS SO, the "
                    "sentence is in the wrong field: `driver` names what MOVED, the "
                    "structured assertion is macro_held, and the explanation belongs in "
                    "`evidence`." % ", ".join(hits))
            if rb.get("macro_held") is not True and not sanctioned:
                fails.append(
                    "range_basis does not assert that the macro path was held fixed across "
                    "the range. One inflation, one currency, one price of time -- moving "
                    "them with the driver is the incoherence [R-MACRO-01] exists to close.")

    env = r.get("envelope") or {}
    if env:
        # A primary computed BOTH WAYS on a contested judgement publishes a RANGE
        # rather than a point -- the dual-framing rule, which forbids averaging the
        # two framings into one number. Where it does, the range is part of the
        # envelope on the same footing as any other present-value read.
        pv = [prim.get("value")]
        pr = prim.get("range") or {}
        pv += [pr.get("low"), pr.get("high")]
        pv += [x.get("value") for x in (r.get("cross_checks") or [])
               if x.get("kind") != "book_value" and x.get("value") is not None
               and x.get("present_value", True)]
        pv = [float(v) for v in pv if v is not None]
        if pv:
            lo, hi = min(pv), max(pv)
            for side, got, want in (("low", env.get("low"), lo), ("high", env.get("high"), hi)):
                if got is not None and abs(float(got) - want) > max(0.01, 0.002 * abs(want)):
                    fails.append(
                        "the envelope's %s is %.4f against %.4f, the %s of the "
                        "present-value lenses. The envelope is the RANGE of the "
                        "present-value reads on one clock, not an average and not a "
                        "spread invented around the central."
                        % (side, float(got), want, side))

    if fails:
        raise AssertionError("LENS FAIL -- %s (%s):\n  - %s"
                             % (ticker, cls, "\n  - ".join(fails)))
    return {"ticker": ticker, "class": cls, "primary": prim.get("kind"),
            "central": central, "cross_checks": seen,
            # the gate needs these to run the identity clause BRANCH-WISE against
            # what the study publishes; the assertion sees only the record and so
            # can test the record's own shape and nothing further
            "two_sided": _ts,
            "branches": [float(b["value"]) for b in _branches
                         if isinstance((b or {}).get("value"), (int, float))],
            "standard_version": STANDARD_VERSION}


def assert_reverse_dcf(diag: dict, study_dir: str, ticker: str = "?") -> dict:
    """Raise unless the study publishes what the PRICE must believe, and keeps it out
    of the model.  [R-ENF-05]

    The instrument. Every study states what IT believes; almost none states what
    the market believes, and the two are the same model read backwards. A reverse
    DCF -- the growth, margin, conversion or discount rate the traded price
    implies under the study's own drivers -- turns a disagreement into a
    measurable one: not "we are 28% below" but "the price is paying for a
    conversion rate of 7.9% and we forecast 8.7%".

    THE HARD PART IS KEEPING IT OUT OF THE MODEL. A rate solved from a price and
    then used anywhere in a valuation is the reverse-engineered terminal the
    protocol prohibits outright, arriving through a side door. So the diagnostic
    lives in its own file, and this assert checks that NO BUILDER IMPORTS IT: a
    study whose cost-of-capital or forecast code reads the diagnostics file fails
    here, whatever the file says.
    """
    import glob as _glob
    import json as _json
    import os as _os
    import re as _re

    fails = []
    d = diag or {}
    if not d.get("implied"):
        fails.append("no implied quantity recorded. The reverse read names the ONE "
                     "quantity the price is paying for, solved on the study's own model.")
    for k in ("quantity", "value", "study_value", "solved_on"):
        if k not in (d.get("implied") or {}):
            fails.append("the implied record carries no %s" % k)
    if d.get("spot") is None:
        fails.append("no spot recorded: a reverse read with no price is not one")

    # the containment check: no builder may import the diagnostics
    leaks = []
    for f in sorted(_glob.glob(_os.path.join(study_dir, "*.py"))):
        base = _os.path.basename(f)
        if base.startswith(("diagnostic", "gap_review", "recalc", "gate_check")):
            continue
        try:
            txt = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if _re.search(r"diagnostics\.json|reverse_dcf|implied_discount|implied_conversion",
                      txt):
            # a builder that COMPUTES the reverse read is fine; one that reads the
            # file back into the model is not.
            #
            # AND THE FILE HAS TO BE THIS STUDY'S OWN. `diagnostics.json` is not a
            # reserved name: every statement walk-forward writes one too, holding
            # its own per-driver error diagnostics, and a study consuming THAT is
            # doing what [R-FCAL-01] asks — carrying its calibration into the
            # delivered document. EGCH's compute.py opens
            # ../egch_walkforward/diagnostics.json and was failed for it, which is
            # a check firing on work that is right; the answer to that is never to
            # widen the check but to point it at the right file. A reference
            # qualified to another directory is not a leak; a bare one is, because
            # a bare open() resolves inside the study.
            for line in txt.splitlines():
                if "diagnostics.json" not in line:
                    continue
                window = txt[max(0, txt.index(line) - 400):
                             txt.index(line) + len(line) + 200]
                if _re.search(r"_walkforward|\.\.[/'\"]|walkforward", window):
                    continue
                leaks.append(base)
                break
    # THE VALUE ITSELF MUST NOT BE IN THE NUMBERS FILE, which is what the rule
    # actually says: the reverse read lives outside "the numbers file builders
    # read". Checking WHICH FILE reads WHAT is a proxy for that, and it needed two
    # unexplained by-name exemptions (lenses.py, docx_arcc.py) to stop firing on
    # studies doing the right thing — a study that COMPUTES the read, and a builder
    # that only DISPLAYS it, are both fine and neither is distinguishable from a
    # leak by grepping for a filename.
    #
    # This is checkable without guessing: take the diagnostic's OWN implied value
    # and look for it in study_numbers.json. A float carried to full precision does
    # not appear there by coincidence, so a hit means the quantity solved from the
    # price is sitting in the file every builder reads — which is the thing
    # prohibited, whether or not any builder currently computes from it. TMGH is
    # the case that prompted this: its implied_discount_rate is in lenses.json and
    # from there in study_numbers.json, and every use of it is display, so the
    # rule's PURPOSE is met and its DEVICE is broken. The device is what is
    # checkable, and widening the check to allow "display only" would delete it
    # rather than sharpen it.
    val = (d.get("implied") or {}).get("value")
    nums = _os.path.join(study_dir, "study_numbers.json")
    if isinstance(val, float) and _os.path.exists(nums):
        try:
            _doc = _json.load(open(nums, encoding="utf-8"))
        except Exception:
            _doc = None

        def _hunt(node, trail=""):
            if isinstance(node, dict):
                for k, v in node.items():
                    r = _hunt(v, trail + "/" + str(k))
                    if r:
                        return r
            elif isinstance(node, list):
                for i2, v in enumerate(node[:200]):
                    r = _hunt(v, trail + "[%d]" % i2)
                    if r:
                        return r
            elif isinstance(node, float) and node == val:
                return trail
            return None

        where = _hunt(_doc) if _doc is not None else None
        if where:
            fails.append(
                "the reverse read's own value (%r) is committed in "
                "study_numbers.json at %s. A quantity solved from the traded price "
                "must not sit in the numbers file every builder reads, whether or "
                "not a builder currently computes from it — that is the "
                "reverse-engineered rate arriving through a side door, and the "
                "prohibition is worth nothing if the side door is open."
                % (val, where))

    if leaks:
        fails.append(
            "these builders read the diagnostics file: %s. A quantity solved from the "
            "traded price must never re-enter the model — that is the "
            "reverse-engineered rate the protocol prohibits, arriving through a side "
            "door." % ", ".join(leaks))

    if fails:
        raise AssertionError("REVERSE-DCF FAIL -- %s:\n  - %s" % (ticker, "\n  - ".join(fails)))
    imp = d["implied"]
    return {"ticker": ticker, "quantity": imp["quantity"], "implied": imp["value"],
             "study": imp["study_value"], "spot": d["spot"],
             "standard_version": STANDARD_VERSION}


def assert_contested_judgements(record: dict, ticker: str = "?",
                                threshold: float = 0.05) -> dict:
    """Raise unless every judgement worth more than `threshold` of value is recorded
    both ways, and report the SIGN TEST on which way they were resolved.

    The instrument against the selection lean. Any single choice in a valuation is
    defensible; what is not defensible is a study that resolves EVERY contested
    choice in the same direction and never notices. This records each one with
    both framings' values and the side adopted, and prints a binomial sign test:
    a study that lands them all one way at p < 0.05 is flagged, not failed —
    the flag is information, and a company can genuinely deserve a consistent
    read. What it may not do is go unmeasured.
    """
    fails = []
    items = (record or {}).get("judgements") or []
    if not items:
        fails.append("no contested judgements recorded. A valuation with no contested "
                     "judgement is a valuation nobody looked at hard enough.")
    signs = []
    for j in items:
        for k in ("name", "adopted", "alternative", "value_adopted", "value_alternative"):
            if k not in j:
                fails.append("judgement %r carries no %s" % (j.get("name", "?"), k))
                break
        else:
            va, vb = float(j["value_adopted"]), float(j["value_alternative"])
            base = abs(vb) or 1.0
            j["_material"] = abs(va - vb) / base >= threshold
            if j["_material"]:
                signs.append(1 if va > vb else (-1 if va < vb else 0))
            if not j.get("why"):
                fails.append("judgement %r says which side was adopted but not why"
                             % j.get("name", "?"))
    if fails:
        raise AssertionError("CONTESTED-JUDGEMENT FAIL -- %s:\n  - %s"
                             % (ticker, "\n  - ".join(fails)))

    n = len([s for s in signs if s])
    k = len([s for s in signs if s > 0])
    p = None
    if n:
        from math import comb
        tail = sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / float(2 ** n)
        p = min(1.0, 2 * tail)
    return {"ticker": ticker, "judgements": len(items), "material": n,
            "resolved_upward": k, "sign_test_p": p,
            "flag": bool(p is not None and p < 0.05 and n >= 3),
            "note": ("a study that resolves every material contested judgement the same "
                     "way is not necessarily wrong, and it is always worth knowing"),
            "standard_version": STANDARD_VERSION}


def assert_gates_called(study_dir: str) -> None:
    """Raise unless the study's own code calls the three gates.  [R-ENF-02]

    Written because 13 of the 21 study directories called none of them, and a study
    that does not check itself passes by default. The repo-level job
    scripts/check_study_provenance.py runs this over every study so it cannot be skipped.
    """
    import os
    wanted = ('assert_beta_provenance', 'assert_sigcm', 'assert_model_study')
    seen = set()
    for f in os.listdir(study_dir):
        if not f.endswith('.py'):
            continue
        try:
            src = open(os.path.join(study_dir, f), encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        seen.update(g for g in wanted if g in src)
    missing = [g for g in wanted if g not in seen]
    if missing:
        raise AssertionError(
            f"GATE FAIL — {os.path.basename(study_dir)} never calls {missing}. Writing a "
            f"rule down does not execute it: the composite beta spread through every study "
            f"in this repo while the rule against it was already written."
        )
