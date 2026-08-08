# TESTAHIL — Source-Integrity & Ground-Up Construction Mandate (SIGCM)

Adopted at Sherif's instruction, 21-Jul-2026. Standing hard gate — QC gate item (r) in
Standing_Research_Protocol.md's own internal numbering. Applies to EVERY study and EVERY
update, every ticker, every market, with no carve-out.

This is the canonical prose. The machine-readable form and enforcement gate live in
`engine/research_protocol.py` — `SIGCM_CLAUSES` for the text of each clause,
`SIGCMChecklist` for the per-study attestation, and `assert_sigcm()` for the hard-fail
gate itself. The two must never diverge: if this file's wording changes, the clause text
inside `SIGCM_CLAUSES` changes in the same commit, and `assert_sigcm()` is verified by
IMPORT — not by parsing — before anything relying on it is trusted, the same discipline
`market_profiles.py` and `wacc_builder.py` already carry.

This mandate does not replace any other standing procedure. It makes explicit and
enforceable what the sourcing, Step 2A, driver-discipline and code-first rules already
imply, and adds the formula-based-model requirement on top. **A violation of any clause
is a HARD FAIL — the report must not issue.**

---

## The eight clauses

**1. Historicals — official sources only.**
Build the past income statement, balance sheet and cash flow statement using ONLY the
company's own issued financial statements and full disclosures. No data vendors, no
brokers, no press coverage used as a numbers source, no third-party estimates, for the
subject's own reported historicals. The Step 2A sweep's Global/Country/Industry rings
remain valid for external context and forecast drivers — never as the source of the
company's own reported numbers. If required official data is inaccessible, STOP AND
INFORM. Never substitute unofficial data. Never issue a report built on unofficial
company information.

**2. Forecast from the ground up.**
Product-by-product / service-by-service wherever segments are disclosed. Revenue is
built as volume × price; cost as cost-per-unit; growth is projected in BOTH volume and
price, never as a single blended revenue-growth assumption when the unit economics are
available. Where unit- or segment-level data is not disclosed, drop to the finest sourced
level that is available and FLAG the gap as a Driver Ledger row — do not silently default
to a top-down blend.

**3. Debt and FX.**
Study balance-sheet debt in full. Split local-currency from foreign-currency tranches.
Carry FX-denominated debt at its local-equivalent cost (coupon plus expected local
depreciation) — never a raw FX coupon dropped into a local-nominal WACC. Consistent with
the WACC standing procedure's Kd-integrity gate and the v2 cost-of-capital method.

**4. Asset-conversion cycle drives the balance sheet and cash flow.**
Study DSO, DIO, DPO and the cash-conversion cycle from the statements, and PROJECT the
balance-sheet and cash-flow items from them. No unexplained plugs where the drivers
themselves are disclosed. Reinforces the cross-sheet-integrity requirement — Δcash on the
cash-flow statement must equal Δcash on the balance sheet, every year, by construction of
how both are built, not by a reconciling plug bolted on afterward.

**5. Competitors.**
Study peers within and outside the country for operating KPIs and valuation multiples.
Cross-check and relative-multiples use only — competitor data is never a source for the
subject company's own historicals, no matter how well-disclosed the peer is.

**6. Beta.**
From the stock's own price history, regressed against its own local index (EGX30 for
EGX-listed names, and the equivalent local benchmark elsewhere) — the SAME beta the
standing BETA procedure and the `wacc_builder.py` usability gate produce. Not a second,
independently-run method that could quietly disagree with the WACC block's own number.

**7. Formula-based, always.**
Every constructed financial statement is a live formula model: driver → income statement
→ balance sheet → cash flow → DCF. Blue cells are inputs, black cells are formulas. Fair
value must recompute when a driver changes. A statement built from hardcoded, pasted
values is not an acceptable deliverable, no matter how correct the numbers look on
delivery day. Sits alongside the code-first rule: `compute.py` owns the arithmetic, and
the delivered Excel is itself a live model, never a values-dump of `study_numbers.json`.

**8. Flag before issue; stop when blocked.**
Flag any missing input BEFORE the report is issued — never discover a gap after delivery
that should have been disclosed on day one. If the company's website or its disclosed
statements cannot be read, and that blocks a properly ground-up build, STOP AND INFORM.
Do not proceed on assumptions or on unofficial substitutes standing in for what should
have been sourced directly.

---

## Why this exists

Adopted the same day as a direct instruction, after the pattern it closes had already
reached delivered work more than once: a study reads as buildable and internally
consistent while quietly resting on a vendor's restated number, a press summary of a
filing, or a hardcoded value dressed up as a formula. None of those failures show up in a
clean recalc or a passing cell-by-cell diff — the arithmetic is fine; the foundation is
not. SIGCM exists to make the foundation itself an assertable, checkable thing rather than
a claim taken on trust.

## QC consequence

New gate item **(r)** in Standing_Research_Protocol.md's own internal lettering: SIGCM
attested, with evidence per clause, output as a filled table — never self-certified.
Absence of any clause's evidence is a QC FAIL. The engine guard list (verified by IMPORT,
not by parsing) reads: `market_profiles.py`, `wacc_builder.py`, `research_protocol.py`,
`adaptive_width.py`, `research_sweep.py`, `technicals.py`, `apply_technicals.py`,
`ta_chart.py`, `rollforward_one.py`.

## Related, extended by later procedures

- **[07-Aug-2026] PRIMARY-SOURCE FINANCIAL RESEARCH** (Standing_Research_Protocol.md)
  extends clause 1 specifically for the Company ring: the company's own website /
  investor-relations page is the first channel attempted, logged whether it succeeds or
  fails, before any secondary source; a minimum of two (target four) complete audited
  fiscal years; every quarter of the study year already disclosed swept in before the
  build; investor-relations presentations and call transcripts tagged distinctly
  (`COMPANY_IR`) as a mandatory source in their own right.
