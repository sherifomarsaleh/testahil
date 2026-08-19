"""
model_report_spec.py — THE MODEL REPORT, machine-readable.

The canonical prose lives in engine/model_report/MODEL_REPORT_19-08-2026.md. This module is
its enforceable form: a per-section CONTENT CONTRACT plus checkers that read a DELIVERED
document and count what is actually in it.

WHY THIS EXISTS. Until 19-Aug-2026 the model-study bar was a list of self-attested booleans
(ModelStudyChecklist). Two studies built four months apart both reported "[model-study bar]
PASS — all depth standards met" while differing by a factor of SEVEN in delivered substance:

    ADNOCLS 09-Aug-2026     29,989 words   51 tables   473 table rows    9 figures
    SWDY    05-Aug-2026     12,416 words   36 tables   290 table rows    8 figures
    RIYADHCABLE 18-Aug-2026  4,408 words   12 tables    80 table rows    7 figures

All three carry the 16-section skeleton and the 16-sheet workbook, so a skeleton check cannot
tell them apart. In the third, sections 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.9, 2, 4, 5, 6, 7 and
the whole expert appendix carry NO TABLE AT ALL — four valuation lenses assert their answers
in 61-97 words each instead of showing the arithmetic; the level-touch ladder that section 3
is required to carry is absent; the balance sheet is history-only where the contract says
three historical plus five forecast years; and no expert shows a worked valuation.

This is the same disease assert_beta_provenance() was written to cure, in a different organ:
a checklist boolean cannot see the work it is attesting to. So this module INSPECTS THE
EVIDENCE — it parses the delivered .docx, .xlsx and bibliography and reports per-section
findings. It is negative-controlled: it must PASS the model report and FAIL the 18-Aug study.

This file holds RULES and STRUCTURE, never numbers from a fit. Verified by IMPORT, not parse.
"""

from dataclasses import dataclass, field
from typing import Optional
import re
import zipfile
from xml.etree import ElementTree as ET

# --------------------------------------------------------------------------------------
# THE MODEL REPORT
# --------------------------------------------------------------------------------------
# ADNOCLS_Valuation_Study_09-08-2026 is THE MODEL REPORT [adopted 19-Aug-2026, per Sherif's
# instruction], displacing SWDY under the standing one-in-one-out rule. It was chosen on
# depth and analysis: it is the study that prices every contested construction instead of
# naming it, shows the beta both ways, builds the cost of debt from six disclosed
# instruments rather than one asserted range, drives seven disclosed units on seven drivers
# with margins falling out as outputs, and gives each expert a worked table with every
# intermediate line.
#
# ONE SECTION OF THE EXEMPLAR IS NOT PART OF THE MODEL: "What changed in these editions, and
# why". It is excluded per instruction — the edition-correction record is internal QC
# evidence and belongs in the study's QC gate and critique adjudication, not in a document
# an external reader receives. FORBIDDEN_SECTIONS enforces its absence.
MODEL_REPORT = {
    "reference": "ADNOCLS_Valuation_Study_09-08-2026",
    "path": "engine/adnocls_study/",
    "adopted": "2026-08-19",
    "displaced": "SWDY_Valuation_Study_05-08-2026 (one-in-one-out; removed from the "
                 "reference layer outright, not carried as a retired entry)",
    "spec_document": "engine/model_report/MODEL_REPORT_19-08-2026.md",
    "deliverables": [
        "study Word + PDF",
        "Excel model + PDF",
        "standalone bibliography Word + PDF",
        "QC gate as a filled evidence table, with this contract's per-section output pasted in",
    ],
    "lens_pattern_references": {
        "operating_company": "ADNOCLS",
        "bank": "ADCB",
        "holdco": "ALPHADHABI",
    },
}

# Sections the model report EXCLUDES. Present in the exemplar, deliberately not in the model.
FORBIDDEN_SECTIONS = {
    "what changed in these editions": (
        "The edition-by-edition correction record is internal QC evidence [excluded "
        "19-Aug-2026, per instruction]. It belongs in the study's QC gate file and its "
        "critique adjudication, not in the delivered document. What the reader is owed "
        "instead is the CURRENT state of every contested choice, priced — which sections "
        "1.1, 1.8, 4 and 7 already carry — and the standing correction policy, which is one "
        "paragraph in About this series."
    ),
}


@dataclass
class RequiredTable:
    """A table the section must actually carry, matched on its header row + stub column.

    `all_of` terms must EACH appear somewhere in the table's header-plus-stub text; `any_of`
    needs one hit. Matching is on lowercased text, so it survives rewording of the labels
    around the required content but not the content going missing.
    """
    name: str
    all_of: tuple = ()
    any_of: tuple = ()
    min_rows: int = 2
    min_cols: int = 2
    why: str = ""


@dataclass
class SectionSpec:
    """The content contract for one section of the model report.

    Floors are BACKSTOPS, not targets: they sit far below the model report and exist to catch
    a section that was asserted rather than built. The binding requirements are the named
    tables and prose beats — a section can clear every floor and still fail, which is correct.
    """
    key: str
    title: str
    min_words: int = 0
    min_paras: int = 0
    min_tables: int = 0
    min_table_rows: int = 0
    tables: tuple = ()          # tuple[RequiredTable]
    prose_any: tuple = ()       # tuple[tuple[str, ...]] — each inner tuple needs one hit
    purpose: str = ""
    model_actual: str = ""      # what the model report itself carries, for calibration


SECTIONS = (
    SectionSpec(
        key="front",
        title="Masthead + READ FIRST",
        min_words=120, min_tables=2,
        purpose="Identity, class, exchange, reporting vs trading currency, the anchor close "
                "and its date, the balance-sheet date the model is built at; then a READ "
                "FIRST box saying what the document is and is not.",
        model_actual="2 boxes, 683 words",
    ),
    SectionSpec(
        key="headline",
        title="Headline",
        min_words=400, min_paras=4,
        prose_any=(("anchor", "closing price", "close of", "anchored"),),
        purpose="The whole argument in prose before any table: what the business is, what "
                "moves it, which single judgement decides the answer, and why the conclusion "
                "is stronger or weaker than it looks. Written so a reader who stops here has "
                "the thesis and its main weakness.",
        model_actual="6 paragraphs, 1,214 words",
    ),
    SectionSpec(
        key="summary",
        title="Valuation summary — every read at a glance",
        min_words=250, min_tables=1, min_table_rows=8,
        tables=(
            RequiredTable(
                "every-read table", min_rows=8, min_cols=4,
                all_of=("weighted central",),
                any_of=("market price", "vs price", "vs spot", "against the market"),
                why="Four lenses, the weighted central and the market price on one grid, each "
                    "with its bear-base-bull span and its weight.",
            ),
            RequiredTable(
                "alternative readings", min_rows=1,
                any_of=("alternative", "not included in the weighted", "on the alternative"),
                why="THE CONTESTED JUDGEMENT, BOTH WAYS, must be visible in the summary "
                    "itself — a row carrying the value on the alternative construction, "
                    "never averaged into the central. A prose box saying a judgement is "
                    "contested does not satisfy this; the alternative must carry a number.",
            ),
        ),
        purpose="Every read on one grid, plus the alternative readings that are excluded from "
                "the weighting but shown so the reader can price them.",
        model_actual="11 rows x 5 cols incl. 4 alternative-reading rows, 806 words",
    ),
    SectionSpec(
        key="overview",
        title="Company overview",
        min_words=300, min_tables=1, min_table_rows=12,
        purpose="An at-a-glance fact table — listing and parent, what it does, physical scale, "
                "how much is contracted vs exposed, currencies, shares, market capitalisation, "
                "net debt, hybrids, distribution policy, tax — then the two or three structural "
                "facts that govern everything downstream.",
        model_actual="15-row Item/Detail table + the structural read, 891 words",
    ),
    SectionSpec(key="s1", title="1 Fundamental valuation", purpose="Section head only."),
    SectionSpec(
        key="s1_1",
        title="1.1 The cash-flow model",
        min_words=800, min_tables=3, min_table_rows=35,
        tables=(
            RequiredTable(
                "FCFF waterfall", min_rows=10, min_cols=5,
                all_of=("free cash flow",),
                any_of=("depreciation", "capital expenditure", "working capital"),
                why="The FULL waterfall inline — revenue, operating cost, EBITDA, D&A, EBIT, "
                    "tax, NOPAT, +D&A, -capex, -change in working capital, FCFF, discount "
                    "factor, PV. Stopping at FCFF is a hard fail.",
            ),
            RequiredTable(
                "EV to equity bridge", min_rows=6,
                all_of=("enterprise value",),
                any_of=("net debt", "equity value"),
                why="Every claim between enterprise value and the ordinary share counted "
                    "once and named: net debt, deferred consideration, hybrids, minorities, "
                    "joint ventures — with the terminal-value share of enterprise value on "
                    "its own row.",
            ),
            RequiredTable(
                "capital-intensity evidence", min_rows=2,
                any_of=("depreciation", "receivable", "working capital", "capital expenditure"),
                why="The two or three lines that a reviewer will challenge (the depreciation "
                    "rate, the receivable days) set out with the evidence behind each, not "
                    "left as assumptions inside the waterfall.",
            ),
        ),
        purpose="The primary lens, built at the most recent reviewed balance-sheet date, with "
                "every line computed rather than typed.",
        model_actual="4 tables / 50 rows, 2,255 words",
    ),
    SectionSpec(
        key="s1_2",
        title="1.2 Book value and sustainable return",
        min_words=400, min_tables=2, min_table_rows=10,
        tables=(
            RequiredTable(
                "return schedule", min_rows=4,
                any_of=("residual income", "economic profit", "return on", "book"),
                why="The asset lens shows a schedule — opening book, the return on it, the "
                    "cost of equity charged against it, the residual, discounted — not a "
                    "justified-multiple assertion.",
            ),
            RequiredTable(
                "value build", min_rows=5,
                any_of=("book value per share", "fair value", "equity value", "price to book"),
                why="Book per share to fair value per share, every step visible, with the "
                    "memorandum lines that let a reader check it against the market.",
            ),
        ),
        purpose="What the balance sheet is worth and what the company sustainably earns on it.",
        model_actual="2 tables / 20 rows, 1,492 words",
    ),
    SectionSpec(
        key="s1_3",
        title="1.3 Relative multiples",
        min_words=400, min_tables=2, min_table_rows=12,
        tables=(
            RequiredTable(
                "peer multiple frame", min_rows=3, min_cols=4,
                any_of=("peer", "company", "market", "business model"),
                why="Named comparators with their market, their business model and their "
                    "multiples — and the subject on the same row basis.",
            ),
            RequiredTable(
                "applied multiple build", min_rows=5,
                any_of=("multiple", "blended", "enterprise value", "fair value"),
                why="Which multiple is applied to what, at what weight, arriving at a value "
                    "per share. A multiple quoted in prose is not a lens.",
            ),
        ),
        purpose="What the market pays for comparable earnings, and where no clean comparable "
                "exists, the construction built to stand in for one — stated as such.",
        model_actual="4 tables / 31 rows incl. a sum-of-the-parts on the same multiples, 1,504 words",
    ),
    SectionSpec(
        key="s1_4",
        title="1.4 Normalised earnings power",
        min_words=200, min_tables=1, min_table_rows=6,
        tables=(
            RequiredTable(
                "normalised build", min_rows=6,
                any_of=("average", "mid-cycle", "normalised", "normalized"),
                why="The mid-cycle build line by line, and what it is measured against — the "
                    "last reported year and the current-year build.",
            ),
        ),
        purpose="What the group earns in an ordinary year, neither the peak nor the trough.",
        model_actual="1 table / 10 rows, 402 words",
    ),
    SectionSpec(
        key="s1_5",
        title="1.5 Synthesis — four lenses, one field",
        min_words=250, min_tables=1, min_table_rows=6,
        tables=(
            RequiredTable(
                "weighting table", min_rows=6, min_cols=5,
                any_of=("weight", "contribution"),
                why="Bear / base / bull / weight / contribution for each lens, contributions "
                    "adding to the weighted central exactly. Both constructions of any "
                    "contested input get their own weighted-central row.",
            ),
        ),
        prose_any=(("disagree", "divergence", "do not agree", "weakness"),),
        purpose="The four lenses on one field, the weighting stated, and the weakness in that "
                "weighting told to the reader rather than left to be found.",
        model_actual="1 table / 8 rows + the stated weakness in the weighting, 810 words",
    ),
    SectionSpec(
        key="s1_6",
        title="1.6 The drivers",
        min_words=600, min_tables=3, min_table_rows=20,
        tables=(
            RequiredTable(
                "disclosed units, historically", min_rows=4, min_cols=4,
                any_of=("unit", "segment", "revenue", "margin"),
                why="Every disclosed unit with its own historical revenue and its own margin, "
                    "taken from the filings — the base the forecast is built off.",
            ),
            RequiredTable(
                "driver map", min_rows=3,
                any_of=("driver", "grown on", "volume", "price"),
                why="One row per unit naming the physical driver it is grown on. This is where "
                    "volume x price and cost-per-unit are shown to exist.",
            ),
            RequiredTable(
                "built output, margins as outputs", min_rows=6, min_cols=5,
                any_of=("margin", "revenue"),
                why="The forecast by unit with margin FALLING OUT of the build. A margin set "
                    "as an input where the filings disclose enough to build cost per unit is "
                    "a QC fail on its own.",
            ),
        ),
        purpose="Each disclosed unit grown on its own driver, with margins as outputs, and the "
                "build reconciled against management's own guidance where guidance exists.",
        model_actual="5 tables / 46 rows incl. the guidance reconciliation, 1,836 words",
    ),
    SectionSpec(
        key="s1_7",
        title="1.7 The crux",
        min_words=500, min_tables=2, min_table_rows=8,
        prose_any=(("evidence", "outside evidence", "independent"),),
        purpose="The single question the answer turns on, isolated, quantified in real "
                "observable units, and the reversion or persistence judgement supported by "
                "evidence that is NOT this study's own construction.",
        model_actual="3 tables / 24 rows incl. the disclosed contract table and the "
                     "outside-evidence table, 1,886 words",
    ),
    SectionSpec(
        key="s1_8",
        title="1.8 Macro and country — the sourced cost of capital",
        min_words=700, min_tables=4, min_table_rows=25,
        tables=(
            RequiredTable(
                "cost-of-capital components", min_rows=8, min_cols=3,
                all_of=("cost of equity",),
                any_of=("source", "construction", "note"),
                why="Every component with its source and construction in its own column: "
                    "observed risk-free, less the sovereign's OWN default spread, adjusted "
                    "risk-free, beta, equity risk premium, cost of equity, pre- and after-tax "
                    "cost of debt, hybrid cost, the weights, the cost of capital and its glide.",
            ),
            RequiredTable(
                "beta diagnostics", min_rows=5,
                all_of=("beta",),
                any_of=("r-squared", "r squared", "standard error", "observations", "confidence"),
                why="The regressor named, its span, the observation count, beta, standard "
                    "error, R-squared, the confidence interval — and the same regression on "
                    "the alternative series, so the reader sees what the choice of market is "
                    "worth. A beta quoted without its diagnostics is not sourced.",
            ),
            RequiredTable(
                "cost-of-debt evidence", min_rows=4,
                all_of=("cost of debt",),
                why="The instruments actually visible in the statements, each with its basis "
                    "and its rate, and the adopted marginal rate read off them. A single "
                    "disclosed range is not evidence of what a company pays.",
            ),
            RequiredTable(
                "contested constructions, priced", min_rows=3, min_cols=3,
                any_of=("alternative", "the choice made", "why ours"),
                why="Each arguable convention with the alternative, THE VALUE ON THE "
                    "ALTERNATIVE, and why this one was taken. Naming a contested choice "
                    "without pricing it is the defect this row exists to catch.",
            ),
        ),
        purpose="The cost of capital built bottom-up under the v2 method, every component "
                "sourced, and every contested construction priced rather than named.",
        model_actual="4 tables / 43 rows, 2,420 words",
    ),
    SectionSpec(
        key="s1_9",
        title="1.9 Sensitivity",
        min_words=250, min_tables=2, min_table_rows=8,
        tables=(
            RequiredTable(
                "two-way grid", min_rows=3, min_cols=4,
                why="A two-way grid over the two inputs that move the answer most, with the "
                    "adopted cell identified.",
            ),
            RequiredTable(
                "ranked single-driver swings", min_rows=5, min_cols=3,
                any_of=("swing", "range tested", "span"),
                why="Every driver varied independently around its own base, ranked by swing, "
                    "so the reader can see which one input dominates.",
            ),
        ),
        purpose="What the valuation needs each thing to do, in real observable units.",
        model_actual="2 tables / 13 rows, 572 words",
    ),
    SectionSpec(
        key="s2",
        title="2 Technical and price structure",
        min_words=200, min_tables=1, min_table_rows=10,
        tables=(
            RequiredTable(
                "computed marker table", min_rows=10,
                any_of=("resistance", "support", "moving average", "relative strength"),
                why="The computed read: last close, the 20/50/200 averages with slope, nearest "
                    "resistance and support, the 52-week range, RSI(14), ATR(14), crossover "
                    "recency, annualised volatility. Every clause of the narrative selected by "
                    "one of these numbers, and NO fundamental assertion in this section.",
            ),
        ),
        purpose="The computed technical read and the structure to watch, on the same cleaned "
                "series the price map runs on.",
        model_actual="1 table / 12 rows + the structure read, 450 words",
    ),
    SectionSpec(
        key="s3",
        title="3 A probabilistic price map",
        min_words=350, min_tables=2, min_table_rows=6,
        tables=(
            RequiredTable(
                "percentile map", min_rows=2, min_cols=6,
                any_of=("median", "5th", "95th", "percentile"),
                why="The percentile map at one and three calendar months, with the check dates "
                    "stated as calendar dates.",
            ),
            RequiredTable(
                "level-touch ladder", min_rows=3,
                all_of=("touch",),
                why="TOUCH probabilities, distinct from finish probabilities, because a path "
                    "can visit a level and come back. The 18-Aug study omitted this table "
                    "entirely and still self-certified a pass — this row is the negative "
                    "control for that defect.",
            ),
        ),
        prose_any=(("tested", "coverage", "calibrat"),),
        purpose="Where the price could go, as distinct from what the business is worth — never "
                "blended with the fundamental work, with the calibration evidence in plain "
                "language and the statistics inline. No calibration appendix.",
        model_actual="2 tables / 8 rows + 2 outcome-distribution figures, 670 words",
    ),
    SectionSpec(
        key="s4",
        title="4 Comparison of the lenses",
        min_words=250, min_tables=1, min_table_rows=6,
        tables=(
            RequiredTable(
                "what it says / what it assumes", min_rows=6, min_cols=3,
                any_of=("assumes", "what it says"),
                why="Every read, what it says, and the assumption that has to hold for it to "
                    "be right — including the price map and the market itself as reads.",
            ),
        ),
        purpose="The reads side by side with their load-bearing assumptions, and an explicit "
                "statement that no recommendation and no price forecast is expressed.",
        model_actual="1 table / 10 rows, 605 words",
    ),
    SectionSpec(
        key="s5",
        title="5 Catalysts to watch",
        min_words=150, min_tables=1, min_table_rows=6,
        tables=(
            RequiredTable(
                "catalyst / why it matters / what to watch", min_rows=6, min_cols=3,
                why="Each catalyst tied to the mechanism it moves and to an observable a "
                    "reader can actually check.",
            ),
        ),
        purpose="What would move the answer, and the specific observable that would show it.",
        model_actual="1 table / 9 rows, 387 words",
    ),
    SectionSpec(
        key="s6",
        title="6 Reading the probability zones",
        min_words=150, min_tables=1, min_table_rows=6,
        tables=(
            RequiredTable(
                "zone table", min_rows=6, min_cols=3,
                any_of=("zone", "tail", "range"),
                why="The zones of the three-month distribution with where each lens's central "
                    "sits inside them, so the reader can locate the fundamental work on the "
                    "price map without the two being blended.",
            ),
        ),
        purpose="How to read the distribution, and where each central sits in it.",
        model_actual="1 table / 10 rows, 342 words",
    ),
    SectionSpec(
        key="s7",
        title="7 Caveats and what would change our mind",
        min_words=600, min_paras=8,
        prose_any=(("what would change our mind", "would change our mind"),),
        purpose="Every material weakness as its own paragraph — the input that dominates, the "
                "terminal-value share, where the build sits against guidance, what the model "
                "does that the company will not allow, the lens that is missing and why, every "
                "solved-rather-than-sourced input — closing with what would change our mind, "
                "specifically, in both directions.",
        model_actual="16 substantive paragraphs, 2,226 words",
    ),
    SectionSpec(
        key="appA",
        title="Appendix A Financial statements",
        min_words=500, min_tables=3, min_table_rows=30,
        tables=(
            RequiredTable(
                "A.1 income statement, 3 historical + 5 forecast", min_rows=12, min_cols=9,
                why="Three reported years and five forecast years in one grid — nine columns "
                    "including the label column. House derivations labelled as such.",
            ),
            RequiredTable(
                "A.2 balance sheet, 3 historical + 5 forecast", min_rows=10, min_cols=9,
                why="The balance sheet is FORECAST TOO, not history-only. The 18-Aug study "
                    "printed three actual years and stopped; a cash-flow model whose balance "
                    "sheet does not roll forward cannot show the asset-conversion cycle it is "
                    "required to project from.",
            ),
            RequiredTable(
                "A.3 forecast balance-sheet and cash-flow markers", min_rows=8, min_cols=5,
                any_of=("capital expenditure", "free cash flow", "net debt", "invested capital"),
                why="Capex, change in working capital, FCFF, interest, distributions, payout, "
                    "gross and net debt, leverage, invested capital, ROIC, the cost of capital "
                    "that year and the spread.",
            ),
        ),
        purpose="The statements the model is built on and the ones it produces, in full.",
        model_actual="3 tables / 55 rows, 1,216 words",
    ),
    SectionSpec(
        key="appB",
        title="Appendix B Peer frame, risk register and the research register",
        min_words=500, min_tables=3, min_table_rows=15,
        tables=(
            RequiredTable(
                "B.1 peers and the sector frame", min_rows=3, min_cols=3,
                any_of=("relevance", "caution", "peer", "market"),
                why="Each comparator with why it is relevant AND why it is imperfect.",
            ),
            RequiredTable(
                "B.2 risk register", min_rows=6, min_cols=3,
                any_of=("mechanism", "impact", "risk"),
                why="Each risk with its mechanism and a rough valuation impact — a risk "
                    "without a mechanism and a number is a word.",
            ),
            RequiredTable(
                "B.3 research register", min_rows=6, min_cols=3,
                any_of=("layer", "what it provided", "source"),
                why="Sources by research layer with what each provided, followed by the "
                    "NEGATIVE RESULTS in prose: what was looked for, not found, and how the "
                    "study handled the gap.",
            ),
        ),
        prose_any=(("could not be obtained", "not disclosed", "were not used", "no ",
                    "could not be"),),
        purpose="Who the peers are and why they are imperfect, what can go wrong and by how "
                "much, and what the research actually consulted — including what it failed to "
                "find.",
        model_actual="3 tables / 26 rows + 6 negative results, 1,480 words",
    ),
    SectionSpec(
        key="appC",
        title="Appendix C The expert valuation panel",
        min_words=1200, min_tables=5, min_table_rows=30,
        tables=(
            RequiredTable(
                "worked valuation, expert 1", min_rows=6,
                why="A worked table with EVERY intermediate line, from the method's starting "
                    "quantity to fair value per share.",
            ),
            RequiredTable(
                "worked valuation, expert 2", min_rows=6,
                why="Same standard, a genuinely different method.",
            ),
            RequiredTable(
                "worked valuation, expert 3", min_rows=6,
                why="Same standard, a third genuinely different method.",
            ),
            RequiredTable(
                "C.4 cross-examination", min_rows=3, min_cols=3,
                any_of=("conceded", "rejected", "challenge"),
                why="Each challenge explicitly conceded or rejected — not summarised.",
            ),
            RequiredTable(
                "C.6 divergence table", min_rows=4, min_cols=4,
                any_of=("assumption", "swings", "divergence"),
                why="Which assumption drives which gap, expert by expert, so the reader is "
                    "told to DECIDE between premises rather than average three numbers.",
            ),
        ),
        prose_any=(
            ("worldview",),
            ("when it works", "works when", "when it fails", "fails when"),
            ("falsifier", "would prove it wrong", "stated in advance"),
            ("named sensitivity", "sensitivity:"),
        ),
        purpose="Three methods run against the same disclosed facts by three experts labelled "
                "Expert 1/2/3 and cast by method, never by persona name; then the "
                "cross-examination, the three in one room, and the divergence read.",
        model_actual="6 tables / 51 rows, 3 worked valuations, 2,900 words",
    ),
    SectionSpec(
        key="about", title="About this series", min_words=100,
        prose_any=(("both are computed", "both are published", "side by side", "dual"),),
        purpose="What the series is, how it is built, the both-ways rule, the correction "
                "policy, and how the price map is tested before it is allowed to publish.",
        model_actual="4 paragraphs, 430 words",
    ),
    SectionSpec(
        key="disclosure", title="Disclosure and disclaimer", min_words=80,
        purpose="Educational analysis, not advice; no rating and no price target anywhere.",
        model_actual="145 words",
    ),
)

# Figures the model report carries. The named set, not a bare count: the two outcome
# distributions were the ones missing from the 18-Aug study's seven.
REQUIRED_FIGURES = (
    "valuation football field — every lens's span against the market price",
    "the driver build — earnings by disclosed unit, reported and forecast, with the margin",
    "the crux, made visible in its own observable units",
    "sensitivity across the two inputs that move the answer most",
    "price against the 20/50/200 moving averages with the computed support and resistance",
    "the forward price cone to three months, with the fundamental centrals marked",
    "the one-month outcome distribution",
    "the three-month outcome distribution",
    "the three experts' ranges with the panel centre",
)
MIN_FIGURES = 8

# The workbook — 16 sheets, same names, same order, as before. Unchanged by this adoption:
# the depth failure of 18-Aug was in the DOCUMENT and the BIBLIOGRAPHY, not the workbook.
EXCEL_SHEETS = (
    "READ FIRST", "Summary", "Fundamental Valuation", "Assumptions", "SOTP Bridge",
    "Segments", "Relative & Normalized", "DCF", "Income Statement", "Balance Sheet",
    "Cash Flow", "Summary Financials", "Monte Carlo", "Sensitivity",
    "Per-Share & Ratios", "Peer & Sector",
)
MIN_FORMULA_SHARE = 0.60   # of populated cells; the model report's workbook runs 0.83

# The standalone bibliography. The register is the study's own proof that no number is an
# orphan, so its floors are about COVERAGE, not length.
BIBLIOGRAPHY_CONTRACT = {
    "primary_documents_table": "The company's own documents — document, date, file held, and "
                               "what was taken from each; external documents in their own table.",
    "input_register": "EVERY input, four fields (input / value / date / source-and-construction), "
                      "GROUPED BY RESEARCH LAYER. The Step 2A sweep has four mandatory rings, so "
                      "a register with no industry-layer or global-layer input is showing an "
                      "unswept ring, not a simple business.",
    "required_layers": ("company", "country", "industry", "global"),
    "min_company_layer_inputs": 100,
    "judgements_table": "Each judgement with what the study took AND what would overturn it.",
    "negative_results_table": "What was searched for, when, and the outcome — including how the "
                              "study handled each gap.",
    "disagreement_table": "Where two readings of the same figure disagree: the other reading, the "
                          "one used, and why. Present with an explicit 'none found' row if none.",
    "calibration_evidence": "The window-by-window test behind the price map lives HERE, never as "
                            "an appendix in the study.",
}


# --------------------------------------------------------------------------------------
# Checkers — they read the delivered file. No python-docx dependency by design: the gate has
# to run wherever the build runs.
# --------------------------------------------------------------------------------------
_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
_M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

_HEAD_PATTERNS = (
    (r"^headline$", "headline"),
    (r"^valuation summary", "summary"),
    (r"^company overview", "overview"),
    (r"^1\s+fundamental valuation", "s1"),
    (r"^1\.1\b", "s1_1"), (r"^1\.2\b", "s1_2"), (r"^1\.3\b", "s1_3"),
    (r"^1\.4\b", "s1_4"), (r"^1\.5\b", "s1_5"), (r"^1\.6\b", "s1_6"),
    (r"^1\.7\b", "s1_7"), (r"^1\.8\b", "s1_8"), (r"^1\.9\b", "s1_9"),
    (r"^2\s+technical", "s2"), (r"^3\s+a probabilistic", "s3"),
    (r"^4\s+comparison", "s4"), (r"^5\s+catalysts", "s5"),
    (r"^6\s+reading", "s6"), (r"^7\s+caveats", "s7"),
    (r"^appendix\s+a\b", "appA"), (r"^appendix\s+b\b", "appB"), (r"^appendix\s+c\b", "appC"),
    (r"^about this series", "about"),
    (r"^disclosure", "disclosure"),
)


@dataclass
class ParsedSection:
    key: str
    heading: str
    paras: int = 0
    words: int = 0
    tables: list = field(default_factory=list)   # list[dict(rows, cols, text)]
    text: str = ""

    @property
    def n_tables(self) -> int:
        return len(self.tables)

    @property
    def n_table_rows(self) -> int:
        return sum(t["rows"] for t in self.tables)


def _para_text(p) -> str:
    return "".join(t.text or "" for t in p.iter(f"{{{_W}}}t"))


def _cells(row) -> list:
    return [
        " ".join(_para_text(p) for p in c.findall(f"{{{_W}}}p")).strip()
        for c in row.findall(f"{{{_W}}}tc")
    ]


def parse_study_docx(path: str) -> tuple:
    """Return (sections_by_key, figure_captions, forbidden_hits, all_text)."""
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(f"{{{_W}}}body")
    sections, order = {}, []
    cur = ParsedSection(key="front", heading="Masthead + READ FIRST")
    sections["front"] = cur
    order.append("front")
    forbidden, all_text = [], []

    for el in body:
        tag = el.tag.split("}")[1]
        if tag == "p":
            txt = _para_text(el).strip()
            if not txt:
                continue
            all_text.append(txt)
            low = txt.lower()
            hit = None
            if len(txt) < 130:
                for pat, key in _HEAD_PATTERNS:
                    if re.match(pat, low):
                        hit = key
                        break
                for bad in FORBIDDEN_SECTIONS:
                    if low.startswith(bad):
                        forbidden.append(txt)
            if hit:
                cur = sections.get(hit) or ParsedSection(key=hit, heading=txt)
                if hit not in sections:
                    sections[hit] = cur
                    order.append(hit)
                continue
            cur.paras += 1
            cur.words += len(txt.split())
            cur.text += " " + low
        elif tag == "tbl":
            rows = el.findall(f"{{{_W}}}tr")
            if not rows:
                continue
            hdr = _cells(rows[0])
            stubs = [(_cells(r) or [""])[0] for r in rows[1:]]
            body_words = 0
            for r in rows:
                for c in _cells(r):
                    body_words += len(c.split())
            ttext = " | ".join(hdr + stubs).lower()
            cur.tables.append({"rows": len(rows), "cols": len(hdr), "text": ttext})
            cur.words += body_words
            cur.text += " " + ttext
            all_text.append(ttext)

    figs = [t for t in all_text if re.match(r"^figure\s+\d", t.strip().lower())]
    n_img = len(list(root.iter(f"{{{_A}}}blip")))
    return sections, order, figs, n_img, forbidden, " ".join(all_text).lower()


def _table_matches(tbl: dict, req: RequiredTable) -> bool:
    if tbl["rows"] < req.min_rows or tbl["cols"] < req.min_cols:
        return False
    t = tbl["text"]
    if req.all_of and not all(term in t for term in req.all_of):
        return False
    if req.any_of and not any(term in t for term in req.any_of):
        return False
    return True


def check_study_docx(path: str) -> list:
    """Inspect a delivered study document against the model report's content contract.

    Returns a list of finding dicts: {section, item, status, detail}. status is PASS or FAIL.
    """
    sections, order, figs, n_img, forbidden, alltext = parse_study_docx(path)
    out = []

    for spec in SECTIONS:
        sec = sections.get(spec.key)
        if sec is None:
            out.append({"section": spec.title, "item": "present", "status": "FAIL",
                        "detail": "section not found in the delivered document"})
            continue
        if spec.min_words and sec.words < spec.min_words:
            out.append({"section": spec.title, "item": "substance floor", "status": "FAIL",
                        "detail": f"{sec.words} words against a floor of {spec.min_words} "
                                  f"(model report: {spec.model_actual})"})
        if spec.min_paras and sec.paras < spec.min_paras:
            out.append({"section": spec.title, "item": "paragraph floor", "status": "FAIL",
                        "detail": f"{sec.paras} paragraphs against a floor of {spec.min_paras}"})
        if spec.min_tables and sec.n_tables < spec.min_tables:
            out.append({"section": spec.title, "item": "tables", "status": "FAIL",
                        "detail": f"{sec.n_tables} tables against a floor of {spec.min_tables} — "
                                  f"a lens that shows no arithmetic is asserted, not built"})
        if spec.min_table_rows and sec.n_table_rows < spec.min_table_rows:
            out.append({"section": spec.title, "item": "table rows", "status": "FAIL",
                        "detail": f"{sec.n_table_rows} rows against a floor of {spec.min_table_rows}"})
        for req in spec.tables:
            if not any(_table_matches(t, req) for t in sec.tables):
                out.append({"section": spec.title, "item": f"table: {req.name}",
                            "status": "FAIL", "detail": req.why})
        for group in spec.prose_any:
            if not any(term in sec.text for term in group):
                out.append({"section": spec.title, "item": f"prose: {group[0]}",
                            "status": "FAIL",
                            "detail": f"none of {group} appears in the section"})

    for bad, why in FORBIDDEN_SECTIONS.items():
        if forbidden:
            out.append({"section": "document", "item": f"excluded section: {bad}",
                        "status": "FAIL", "detail": why})

    n_fig = max(len(figs), 0)
    if n_fig < MIN_FIGURES:
        out.append({"section": "document", "item": "figures", "status": "FAIL",
                    "detail": f"{n_fig} numbered figure captions against a floor of "
                              f"{MIN_FIGURES}; the model report carries "
                              f"{len(REQUIRED_FIGURES)}. Missing typically: the one-month and "
                              f"three-month outcome distributions."})
    if n_img < MIN_FIGURES:
        out.append({"section": "document", "item": "embedded images", "status": "FAIL",
                    "detail": f"{n_img} embedded images against a floor of {MIN_FIGURES}"})

    if not out:
        out.append({"section": "document", "item": "content contract", "status": "PASS",
                    "detail": "every section meets the model report's contract"})
    return out


def check_workbook(path: str) -> list:
    """16 sheets, exact names and order, and a real formula share."""
    z = zipfile.ZipFile(path)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels}
    names, out = [], []
    cells = forms = 0
    for s in wb.iter(f"{{{_M}}}sheet"):
        names.append(s.get("name"))
        tgt = rmap[s.get(f"{{{_R}}}id")].lstrip("/")
        if not tgt.startswith("xl/"):
            tgt = "xl/" + tgt
        sh = ET.fromstring(z.read(tgt))
        for c in sh.iter(f"{{{_M}}}c"):
            has_f = c.find(f"{{{_M}}}f") is not None
            if has_f or c.find(f"{{{_M}}}v") is not None:
                cells += 1
                forms += 1 if has_f else 0
    if tuple(names) != EXCEL_SHEETS:
        out.append({"section": "workbook", "item": "16 sheets, same names, same order",
                    "status": "FAIL", "detail": f"got {names}"})
    share = forms / cells if cells else 0.0
    if share < MIN_FORMULA_SHARE:
        out.append({"section": "workbook", "item": "formula share", "status": "FAIL",
                    "detail": f"{forms}/{cells} = {share:.0%} against a floor of "
                              f"{MIN_FORMULA_SHARE:.0%}; the workbook must CALCULATE"})
    if not out:
        out.append({"section": "workbook", "item": "structure", "status": "PASS",
                    "detail": f"16 sheets in order; {forms}/{cells} = {share:.0%} formula cells"})
    return out


def check_bibliography(path: str) -> list:
    """The standalone bibliography against its contract."""
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read(f"word/document.xml"))
    body = root.find(f"{{{_W}}}body")
    out, tables, headings = [], [], []
    last = ""
    for el in body:
        tag = el.tag.split("}")[1]
        if tag == "p":
            t = _para_text(el).strip()
            if t and len(t) < 120:
                last = t
            if t:
                headings.append(t.lower())
        elif tag == "tbl":
            rows = el.findall(f"{{{_W}}}tr")
            hdr = _cells(rows[0]) if rows else []
            tables.append({"rows": len(rows), "cols": len(hdr), "lead": last.lower(),
                           "hdr": " | ".join(hdr).lower()})
    alltext = " ".join(headings) + " " + " ".join(t["lead"] + " " + t["hdr"] for t in tables)

    def has(*terms, min_rows=2, min_cols=2):
        return any(t["rows"] >= min_rows and t["cols"] >= min_cols
                   and any(x in (t["lead"] + " " + t["hdr"]) for x in terms) for t in tables)

    if not has("document", "primary", min_rows=4, min_cols=3):
        out.append({"section": "bibliography", "item": "primary-documents table",
                    "status": "FAIL", "detail": BIBLIOGRAPHY_CONTRACT["primary_documents_table"]})
    reg = [t for t in tables if "source" in t["hdr"] and "value" in t["hdr"] and "date" in t["hdr"]]
    if not reg:
        out.append({"section": "bibliography", "item": "four-field input register",
                    "status": "FAIL", "detail": BIBLIOGRAPHY_CONTRACT["input_register"]})
    missing_layers = [l for l in BIBLIOGRAPHY_CONTRACT["required_layers"]
                      if not any(l in t["lead"] for t in reg)]
    if missing_layers:
        out.append({"section": "bibliography", "item": "research layers in the register",
                    "status": "FAIL",
                    "detail": f"no input registered in the {', '.join(missing_layers)} layer(s) — "
                              f"the sweep has four mandatory rings, so an empty ring is an "
                              f"unswept ring, not a simple business"})
    comp = max((t["rows"] - 1 for t in reg if "company" in t["lead"]), default=0)
    if comp < BIBLIOGRAPHY_CONTRACT["min_company_layer_inputs"]:
        out.append({"section": "bibliography", "item": "company-layer depth", "status": "FAIL",
                    "detail": f"{comp} company-layer inputs against a floor of "
                              f"{BIBLIOGRAPHY_CONTRACT['min_company_layer_inputs']}; the model "
                              f"report registers 582. A ground-up build consumes more of the "
                              f"filings than this."})
    if not has("judgement", "judgment", min_rows=4, min_cols=3) or "overturn" not in alltext:
        out.append({"section": "bibliography", "item": "judgements + what would overturn each",
                    "status": "FAIL", "detail": BIBLIOGRAPHY_CONTRACT["judgements_table"]})
    if not has("negative result", "not found", "could not be sourced", min_rows=3, min_cols=2):
        out.append({"section": "bibliography", "item": "negative-results table", "status": "FAIL",
                    "detail": BIBLIOGRAPHY_CONTRACT["negative_results_table"]})
    if not has("disagree", "discrepan", "two readings", "aggregator", min_rows=2, min_cols=3):
        out.append({"section": "bibliography", "item": "where two readings disagree",
                    "status": "FAIL", "detail": BIBLIOGRAPHY_CONTRACT["disagreement_table"]})
    if not out:
        out.append({"section": "bibliography", "item": "contract", "status": "PASS",
                    "detail": f"{len(tables)} tables; company layer {comp} inputs"})
    return out


def assert_model_report(findings: list) -> None:
    """Raise if any finding failed. A FAIL means DO NOT ISSUE."""
    fails = [f for f in findings if f["status"] == "FAIL"]
    if fails:
        lines = "\n".join(f"  - [{f['section']}] {f['item']}: {f['detail']}" for f in fails)
        raise AssertionError(
            f"MODEL-REPORT CONTRACT NOT MET — {len(fails)} unmet requirement(s). The study "
            f"must not be issued.\n{lines}\n"
            f"The bar is {MODEL_REPORT['reference']} ({MODEL_REPORT['path']}); the contract is "
            f"{MODEL_REPORT['spec_document']}."
        )


if __name__ == "__main__":
    # 16 sections in the reader's numbering; 25 addressable blocks here because §1's
    # nine subsections each carry their own contract.
    assert len(SECTIONS) == 25, "16 sections, of which §1 has nine contracted subsections"
    titles = [s.title for s in SECTIONS]
    assert titles[0].startswith("Masthead") and titles[-1].startswith("Disclosure")
    assert len(EXCEL_SHEETS) == 16, "16-sheet workbook, unchanged"
    assert set(MODEL_REPORT["lens_pattern_references"].values()) == {"ADNOCLS", "ADCB", "ALPHADHABI"}
    assert "what changed in these editions" in FORBIDDEN_SECTIONS
    assert MIN_FIGURES <= len(REQUIRED_FIGURES)
    n_req = sum(len(s.tables) for s in SECTIONS)
    print(f"model report spec loaded — {len(SECTIONS)} section specs, {n_req} required tables, "
          f"{len(REQUIRED_FIGURES)} named figures, reference {MODEL_REPORT['reference']}")
