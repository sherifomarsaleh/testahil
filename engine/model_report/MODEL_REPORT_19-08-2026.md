# THE MODEL REPORT

**Adopted 19-Aug-2026, per instruction.** The reference is **ADNOC Logistics & Services,
`ADNOCLS_Valuation_Study_09-08-2026`**, minus one section. It displaces SWDY as the model
study under the standing one-in-one-out rule.

Three files make up the model:

| | |
|---|---|
| **The document** | `engine/model_report/MODEL_REPORT_09-08-2026.docx` — the exemplar with the excluded section removed. Open it beside the study you are writing. |
| **The contract** | `engine/model_report/model_report_spec.py` — the same standard, machine-readable, per section. |
| **The gate** | `engine/model_report/check_model_report.py` — reads a *delivered* file and counts what is in it. Run it before issue. |

Supporting evidence lives in `engine/adnocls_study/` — the workbook, the standalone
bibliography, `QC_GATE_09-08-2026.md`, and the critique adjudication behind the second edition.

---

## Why this exists

Two studies built nine days apart both reported `[model-study bar] PASS — all depth standards
met`, and differ by a factor of seven in delivered substance:

| Delivered study | Words | Tables | Table rows | Figures | Workbook cells |
|---|---:|---:|---:|---:|---:|
| **ADNOCLS 09-Aug-2026** — the model | 29,989 | 51 | 473 | 9 | 2,605 (83% formulas) |
| SWDY 05-Aug-2026 — the displaced model | 12,416 | 36 | 290 | 8 | 924 (64% formulas) |
| RIYADHCABLE 18-Aug-2026 | 4,408 | 12 | 80 | 7 | 771 (72% formulas) |

All three carry the 16-section skeleton and the 16-sheet workbook in the right order. **A
skeleton check cannot tell them apart**, so the previous bar — a list of self-attested
booleans in `ModelStudyChecklist` — could not either.

What the third one actually delivered, against a contract it certified it had met:

- **Twelve sections carry no table at all**: 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.9, 2, 4, 5, 6, 7.
  Four valuation lenses state their answers in 61–97 words each. A lens that shows no
  arithmetic has been asserted, not built.
- **The level-touch ladder is absent** from §3 — an element the protocol names explicitly.
  The word "touch" appears once in the whole document.
- **The balance sheet is history-only** (three actual years, no forecast columns), so the
  asset-conversion cycle SIGCM requires it to project from cannot be shown.
- **No expert shows a worked valuation.** Appendix C has zero tables; no cross-examination
  table, no divergence table.
- **No beta diagnostics table and no cost-of-debt evidence table** in §1.8 — one WACC
  component table, with the cost of debt as a single asserted after-tax rate.
- **Bibliography**: 105 inputs against the model's 618, no global-ring input at all, no
  aggregator-discrepancy table.

This is the same failure `assert_beta_provenance()` was written to close, in a different
organ: *a checklist boolean cannot see the work it is attesting to.* Every study in the repo
set `beta_own_history_vs_egx30 = True` while regressing on a composite. The fix there was to
inspect the record instead of trusting the flag. The fix here is the same — the gate parses
the delivered `.docx`, `.xlsx` and bibliography and counts.

**It is negative-controlled**, the same discipline as `check_ta_chart_overlay.js`:
`--self-test` requires the model report to PASS and the 18-Aug delivery to FAIL. Today that
reads **0 unmet / 100 unmet**. Run against the displaced SWDY study it reports 27 unmet across
10 sections — the bar has genuinely moved, and that is the point.

---

## What is excluded from the model

**"What changed in these editions, and why."** Present in the exemplar, **not part of the
model** [per instruction, 19-Aug-2026]. The edition-by-edition correction record is internal
QC evidence: it belongs in the study's QC gate file and its critique adjudication, not in a
document an external reader receives. `FORBIDDEN_SECTIONS` in the spec enforces its absence,
and the gate fails a study that carries it.

Removing the section forced three consequential edits, all made by
`build_model_report_docx.py` and all asserted:

1. **One paragraph was rescued out of it before the cut.** The note that the desk's
   sanctioned beta routine now returns 1.103 on 159 weekly observations, where every table in
   the study carries the adopted 1.085, is not edition history — it is a live discrepancy
   between an adopted number and the routine meant to produce it. That is a **caveat**, and it
   now sits in §7 with the others.
2. **The READ FIRST box lost its edition paragraph** ("This is a twice-corrected edition…"),
   which was the same content class in the front matter and closed by pointing at the section.
3. **"About this series" was repaired.** It promised the reader the full correction list
   "under 'What changed in these editions, and why', immediately after the caveats". The
   correction *rule* stays; the mechanism is now stated as what the document actually does —
   the correction is made at the point it bears on, with the superseded construction reprinted
   beside the new one at full size.

**Not removed:** the inline "an earlier edition of this study…" passages in 1.2, 1.7, 1.8 and
7. Those are not edition history — each prices a live construction against the superseded one
*at the point the number is used*, which is the dual-framing rule doing its job.

---

## The reference set

Closed at three, unchanged in size:

| Class | Reference |
|---|---|
| Operating company — **and the model report** | **ADNOCLS** |
| Bank | ADCB |
| Holding company | ALPHADHABI |

SWDY is **removed from the reference layer outright**, not carried as a retired entry — a
study named as "the old template" is still a name a future build can reach for. `REFERENCE_SET`
in `engine/research_protocol.py` asserts on exactly these three at import.

Class adapts **the lens and the indicator set**, never the structure or the depth. A class
that fits none of the three adapts the nearest pattern's lens inside this skeleton and says
which and why — it does not go looking for a fourth exemplar.

---

## The contract, section by section

Floors below are **backstops, not targets**: they sit far under what the model report carries
and exist to catch a section that was asserted rather than built. The binding requirements are
the **named tables** and the **prose beats** — a section can clear every floor and still fail,
which is correct.

### Front matter — masthead + READ FIRST
Identity, class, exchange, reporting vs trading currency, the anchor close **and its date**,
and the balance-sheet date the model is built at. Then a READ FIRST box: what the document is,
what a fair value is not, the currency structure, and how the market is measured.
*Model: 2 boxes, 683 words.*

### Headline — ≥400 words, ≥4 paragraphs
The whole argument in prose before any table: what the business is, what moves it, **which
single judgement decides the answer**, and why the conclusion is stronger or weaker than it
looks. Written so a reader who stops here has the thesis *and its main weakness*.
*Model: 6 paragraphs, 1,214 words.*

### Valuation summary — every read at a glance
**Required table 1 — every read.** Four lenses + weighted central + market price, each with
bear/base/bull and its weight. ≥8 rows, ≥4 columns.
**Required table 2 — alternative readings.** The contested judgement, **both ways, carrying
numbers**, excluded from the weighting and shown so the reader can price it. *A prose box
saying a judgement is contested does not satisfy this.*
*Model: 11 rows × 5 columns including four alternative-reading rows, 806 words.*

### Company overview — ≥1 table, ≥12 rows
An at-a-glance fact table — listing and parent, what it does, physical scale, how much is
contracted vs exposed, currencies, shares, market capitalisation, net debt, hybrids,
distribution policy, tax — then the two or three structural facts that govern everything
downstream. *Model: 15 rows, 891 words.*

### 1.1 The cash-flow model — ≥3 tables, ≥35 rows, ≥800 words
1. **The full FCFF waterfall**, inline: revenue → operating cost → EBITDA → D&A → EBIT → tax →
   NOPAT → +D&A → −capex → −ΔWC → FCFF → discount factor → PV. **Stopping at FCFF is a hard
   fail.**
2. **The EV→equity bridge**, every claim between enterprise value and the ordinary share
   counted once and named, with **terminal value as a share of EV on its own row**.
3. **The capital-intensity evidence table** — the two or three lines a reviewer will challenge
   (the depreciation rate, receivable days) with the evidence behind each, not left as
   assumptions inside the waterfall.
*Model: 4 tables / 50 rows, 2,255 words.*

### 1.2 Book value and sustainable return — ≥2 tables, ≥400 words
A **return schedule** (opening book, return on it, cost of equity charged against it, the
residual, discounted) and a **value build** from book per share to fair value per share with
the memorandum lines that let a reader check it against the market. Residual income rather
than a justified-multiple assertion wherever the distribution policy breaks the steady-state
assumption. *Model: 2 tables / 20 rows, 1,492 words.*

### 1.3 Relative multiples — ≥2 tables, ≥400 words
A **peer frame** — named comparators with market, business model and multiples, the subject on
the same basis — and an **applied-multiple build** showing which multiple goes on what, at what
weight, arriving at a value per share. Where no clean comparable exists, say so and build the
construction that stands in for one. *Model: 4 tables / 31 rows including a sum-of-the-parts on
the same multiples, 1,504 words.*

### 1.4 Normalised earnings power — ≥1 table, ≥6 rows
The mid-cycle build line by line, measured against both the last reported year and the
current-year build. *Model: 1 table / 10 rows, 402 words.*

### 1.5 Synthesis — four lenses, one field — ≥1 table, ≥6 rows
Bear / base / bull / weight / **contribution** per lens, contributions adding to the weighted
central exactly. Both constructions of any contested input get their own weighted-central row.
**The weakness in the weighting is told to the reader**, not left to be found.
*Model: 1 table / 8 rows, 810 words.*

### 1.6 The drivers — ≥3 tables, ≥20 rows, ≥600 words
1. **Every disclosed unit, historically** — its own revenue, its own margin, from the filings.
2. **The driver map** — one row per unit naming the physical driver it is grown on. This is
   where volume × price and cost-per-unit are shown to exist.
3. **The built output, margins as OUTPUTS.** A margin set as an input where the filings
   disclose enough to build cost per unit is a QC fail on its own.

Where management publishes guidance, **reconcile the build against it and state the gap
plainly** — including the arithmetic that converts guidance onto the model's own basis.
*Model: 5 tables / 46 rows including the guidance reconciliation, 1,836 words.*

### 1.7 The crux — ≥2 tables, ≥500 words
The single question the answer turns on, isolated, quantified **in real observable units**, and
the reversion-or-persistence judgement supported by evidence **that is not this study's own
construction**. *Model: 3 tables / 24 rows — the disclosed contract table and the
outside-evidence table — 1,886 words.*

### 1.8 Macro and country — the sourced cost of capital — ≥4 tables, ≥25 rows, ≥700 words
1. **Components with source and construction in their own column**: observed risk-free, less
   the sovereign's *own* default spread, adjusted risk-free, beta, ERP, cost of equity, pre-
   and after-tax cost of debt, hybrid cost, the weights, the cost of capital and its glide.
2. **Beta diagnostics** — the regressor named, its span, observation count, beta, standard
   error, R², the confidence interval, and the same regression on the alternative series so
   the reader sees what the choice of market is worth. *A beta quoted without its diagnostics
   is not sourced.*
3. **Cost-of-debt evidence** — the instruments actually visible in the statements, each with
   its basis and its rate, and the adopted marginal rate read off them. *A single disclosed
   range is not evidence of what a company pays.*
4. **Contested constructions, priced** — each arguable convention with the alternative, **the
   value on the alternative**, and why this one was taken.
*Model: 4 tables / 43 rows, 2,420 words.*

### 1.9 Sensitivity — ≥2 tables, ≥8 rows
A **two-way grid** over the two inputs that move the answer most, with the adopted cell
identified, and **ranked single-driver swings** — every driver varied independently around its
own base, ranked, so the reader sees which one input dominates.
*Model: 2 tables / 13 rows, 572 words.*

### 2 Technical and price structure — ≥1 table, ≥10 rows
The computed marker table: last close, 20/50/200 averages with slope, nearest resistance and
support, 52-week range, RSI(14), ATR(14), crossover recency, annualised volatility. Every
clause of the narrative selected by one of these numbers. **No fundamental assertion in this
section.** *Model: 1 table / 12 rows, 450 words.*

### 3 A probabilistic price map — ≥2 tables, ≥350 words
The **percentile map** at one and three calendar months with the check dates stated as calendar
dates, and the **level-touch ladder** — touch probabilities, distinct from finish probabilities,
because a path can visit a level and come back. Calibration evidence in plain language with the
statistics inline; **no calibration appendix**; never blended with the fundamental work.
*Model: 2 tables / 8 rows + two outcome-distribution figures, 670 words.*

### 4 Comparison of the lenses — ≥1 table, ≥6 rows
Every read, **what it says**, and **what it assumes** — including the price map and the market
itself as reads — closing with an explicit statement that no recommendation and no price
forecast is expressed. *Model: 1 table / 10 rows, 605 words.*

### 5 Catalysts to watch — ≥1 table, ≥6 rows
Catalyst · why it matters · **what to watch** — each tied to a mechanism and to an observable a
reader can actually check. *Model: 1 table / 9 rows, 387 words.*

### 6 Reading the probability zones — ≥1 table, ≥6 rows
The zones of the three-month distribution with **where each lens's central sits inside them**,
so the reader can locate the fundamental work on the price map without the two being blended.
*Model: 1 table / 10 rows, 342 words.*

### 7 Caveats and what would change our mind — ≥8 paragraphs, ≥600 words
Every material weakness **as its own paragraph**: the input that dominates, the terminal-value
share, where the build sits against guidance, what the model does that the company will not
allow, the lens that is missing and why, every solved-rather-than-sourced input. Closing with
**"what would change our mind, specifically"**, in both directions.
*Model: 16 substantive paragraphs, 2,226 words.*

### Appendix A Financial statements — 3 tables, ≥30 rows
- **A.1 Income statement** — 3 reported + 5 forecast years, ≥9 columns. House derivations
  labelled.
- **A.2 Balance sheet** — **3 reported + 5 forecast, ≥9 columns.** The balance sheet is
  forecast too. A cash-flow model whose balance sheet does not roll forward cannot show the
  asset-conversion cycle SIGCM requires it to project from.
- **A.3 Forecast balance-sheet and cash-flow markers** — capex, ΔWC, FCFF, interest,
  distributions, payout, gross and net debt, leverage, invested capital, ROIC, the cost of
  capital that year, and the spread.
*Model: 3 tables / 55 rows, 1,216 words.*

### Appendix B Peers, risk register, research register — 3 tables, ≥15 rows
Peers with **why relevant and why imperfect**; risks each with a **mechanism and a rough
valuation impact**; sources by research layer with what each provided — followed by the
**negative results**: what was looked for, not found, and how the study handled the gap.
*Model: 3 tables / 26 rows + 6 negative results, 1,480 words.*

### Appendix C The expert panel — ≥5 tables, ≥30 rows, ≥1,200 words
Three genuinely different methods, labelled **Expert 1/2/3, cast by method, never by persona
name**. Each carries: worldview · when it works / when it fails · **a worked valuation table
with every intermediate line** · a named sensitivity with numbers · **a falsifier stated in
advance**. Then **C.4 cross-examination** (each challenge explicitly conceded or rejected),
**C.5 the three in one room** with the ranges figure, and **C.6 the divergence table** isolating
which assumption drives which gap — so the reader is told to *decide between premises*, not to
average three numbers. *Model: 6 tables / 51 rows, 2,900 words.*

### About this series · Disclosure
What the series is, the both-ways rule, the correction policy, and how the price map is tested
before it is allowed to publish a range. Then: educational analysis, not advice. **No rating
and no price target anywhere in any deliverable.**

---

## Figures — ≥8, the named set

1. Valuation football field — every lens's span against the market price
2. The driver build — earnings by disclosed unit, reported and forecast, with the group margin
3. The crux, made visible in its own observable units
4. Sensitivity across the two inputs that move the answer most
5. Price against the 20/50/200 moving averages with the computed support and resistance ladder
6. The forward price cone to three months, with the fundamental centrals marked
7. The one-month outcome distribution
8. The three-month outcome distribution
9. The three experts' ranges with the panel centre

Solid light canvas, zero transparency verified programmatically, **every figure inspected as a
rendered image**, label collisions fixed in-pass.

---

## The workbook — unchanged

16 sheets, same names, same order: READ FIRST · Summary · Fundamental Valuation · Assumptions ·
SOTP Bridge · Segments · Relative & Normalized · DCF · Income Statement · Balance Sheet · Cash
Flow · Summary Financials · Monte Carlo · Sensitivity · Per-Share & Ratios · Peer & Sector.
Blue = input, black = formula, green = cross-sheet link. **Formula share ≥60% of populated
cells** — the model report's workbook runs 83%.

The 18-Aug failure was in the **document and the bibliography**, not the workbook; its workbook
passes this check. Nothing here is relaxed and nothing is added.

---

## The standalone bibliography

- **Primary-documents table** — the company's own documents (document, date, file held, what
  was taken from each), external documents in their own table.
- **The full input register**, four fields — input / value / date / source-and-construction —
  **grouped by research layer**. The sweep has four mandatory rings, so **a register with no
  industry-layer or global-layer input is showing an unswept ring**, not a simple business.
  Company-layer floor: **100 inputs** (the model registers 582).
- **Judgements**, each with **what would overturn it**.
- **Negative results** — what was searched for, when, the outcome, and how the study handled it.
- **Where two readings of the same figure disagree** — the other reading, the one used, and
  why. Present with an explicit "none found" row if none.
- **The window-by-window calibration evidence** lives here, never as an appendix in the study.

---

## Running the gate

```bash
# before issue, on the delivered files
python3 engine/model_report/check_model_report.py \
    --study  engine/xxx_study/XXX_Valuation_Study_DD-MM-YYYY_public.docx \
    --xlsx   engine/xxx_study/XXX_Valuation_Model_DDMMYYYY_public.xlsx \
    --biblio engine/xxx_study/XXX_Bibliography_DD-MM-YYYY.docx

# the negative control: model report must PASS, the 18-Aug delivery must FAIL
python3 engine/model_report/check_model_report.py --self-test

# rebuild the model report document from its exemplar
python3 engine/model_report/build_model_report_docx.py
python3 engine/model_report/build_model_report_docx.py --check
```

Exit code is non-zero on any FAIL. **Paste the output into the study's QC gate file against
item (a)** — that item is no longer satisfiable by attestation. `assert_model_report(findings)`
raises for a build that wants to fail hard in-process.

A FAIL means **do not issue**. Depth below the model report is a defect, not a style choice and
not a noted limitation.

### What the gate cannot see

It counts structure. It cannot tell you whether a margin is an output or an input dressed as
one, whether the outside evidence in §1.7 is real, or whether the four-field register is
truthful. Those stay with SIGCM, the sweep register and the QC gate. **Passing this gate is
necessary, never sufficient** — the same relationship a clean recalc has to a correct workbook.

---

## Rendering

`MODEL_REPORT_09-08-2026.docx` is committed. Its PDF is produced with the standing command
wherever the LibreOffice import filters are installed:

```bash
python3 engine/make_pdf.py engine/model_report/MODEL_REPORT_09-08-2026.docx
```

It has **not** been rendered in this container: `libreoffice-writer` / `libreoffice-calc` are
absent here, so `make_pdf.py` fails loudly rather than emitting a broken file — which is the
behaviour that script was written to have.
