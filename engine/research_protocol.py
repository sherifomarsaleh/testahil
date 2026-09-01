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



# THE VALUATION METHOD MUST MATCH THE CLASS.  [added 01-Sep-2026]
#
# assert_model_study() verified that the sixteen sections and sixteen sheets
# were present and never once asked whether the study valued the company the way
# its class requires. TMGH shipped four "cases" that were two cost-of-capital
# bases crossed with two readings of ONE discounted cash flow -- one lens with
# four settings -- for a real-estate developer, whose class rule is SOTP/RNAV.
# The word "land" appeared nowhere in any lens, and every gate passed it.
# Structure verified, substance unexamined: the same species of hole that
# [R-SANITY-01] closes one level up.
LENS_BY_CLASS = {
    "real-estate developer, off-plan, percentage-of-completion": ("sotp", "rnav"),
    "real-estate developer, off-plan, point-in-time on handover": ("sotp", "rnav"),
    "telecom operator": ("dcf",),
    "cement and heavy industrial": ("dcf",),
    "petrochemical": ("dcf",),
    "airline": ("dcf",),
    "bank": ("ddm", "fcfe", "residual_income"),
    "holding company": ("sotp", "nav"),
    "commodity and metals": ("dcf",),
}


def assert_class_lens(klass, lenses):
    """A study of a class must carry at least one lens that class requires.

    `lenses` is the study's own list of lens names. The check is deliberately
    weak -- one required lens, not all of them -- because the rule permits
    adapting the nearest pattern where a class does not fit exactly. What it
    refuses is a study that carries NONE of them, which is what happened.
    """
    want = LENS_BY_CLASS.get(klass)
    if want is None:
        raise AssertionError(
            "%r is not a class with a registered lens rule; register it or "
            "state which pattern was adapted and why." % klass)
    have = {str(x).lower() for x in lenses}
    if not any(w in h for w in want for h in have):
        raise AssertionError(
            "CLASS-LENS RULE NOT MET — study must not be issued. A %s is valued "
            "on %s; this study carries only %s. A discounted cash flow with "
            "several settings is one lens, not several."
            % (klass, " or ".join(want), sorted(have) or "no lens at all"))


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
STANDARD_VERSION = "2026.08.23"
STANDARD_VERSION_NOTE = (
    "v2 cost of capital (rf normalised by the sovereign's own default spread); beta via "
    "beta_regression.own_stock_beta() against the registered index of the listing exchange, "
    "attested by assert_beta_provenance(); forecast built ground-up to the finest sourced "
    "level and attested by assert_ground_up() on a driver record; margins as outputs; "
    "terminal growth reconciled; the three gates called in the study's own code."
)


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
