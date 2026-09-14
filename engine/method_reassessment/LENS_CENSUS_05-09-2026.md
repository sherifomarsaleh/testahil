# The lens architecture, censused across the whole book

**Dated 5 September 2026.** Twenty-five studies tested against [R-LENS-03] — the twenty-four
directories under `engine/*_study/` plus **CLHO**, which has a published fair value and a
delivered workbook and no study directory at all.

**This is a census of an architecture, not a calibration of it.** Nothing here is corrected.
Retiring a blend moves a delivered number, which makes it a re-issue with a rebuild ledger
[R-REBUILD-01] and not a line in a census.

**AS OF.** Every figure below was read from the repository and recomputed on **6 September
2026**; the filename carries the date the census was commissioned. Each is arithmetic on a
study's own committed record, re-verified against disk after the tables were written — twenty-
seven load-bearing figures, all stable. That re-verification is not a formality: [R-TERM-01]
work on the terminal was landing in this repository while the census was being taken (PHAR's
numbers file gained `average_age_years` and `maintenance_escalator` fields mid-run), so **any
name whose terminal is rebuilt after this date moves its primary and therefore its correction,
while its blend weights and its residual do not move.** Re-read the primaries before quoting a
correction from this file; the architecture findings stand on their own.

---

## The test, and why it is identity rather than search

[R-LENS-03] states it in one sentence: **ONE class primary IS the central.** So the test is
whether the published central **equals one of the study's own lens reads** to floating-point
tolerance. A central matching no read is, by construction, something other than a lens's own
answer — and only then is there a weight vector to find.

The weights were **solved, never searched**. In all nine cases below they are committed in the
record or typed in the builder; no brute-force sweep over weight combinations was run, and none
was needed. That matters, because with several lens reads straddling a central, *some* convex
combination almost always reproduces *some* number — a reproduction found by search would be
evidence of arithmetic rather than of architecture.

---

## 1. Nine studies still publish a blend

Every reproduction below is exact. The residual is the recomputed weighted sum minus the
published figure, in double precision.

| study | weights | residual | published central | class primary alone | book weighted |
|---|---|---|---|---|---|
| **ADNOCDIST** | 40 cash flow / 25 normalised / 20 relative / **15 book** | **+8.88e-16** | 4.411292110312444 (Frame A) | 4.783957863288807 | **yes, 15% = 11.41% of the answer** |
| **ADNOCDRILL** | 25 dcf A / 25 dcf B / 20 relative / **15 book** / 15 normalised | **0.0** | 4.919425418226855 | 6.208275510273871 | **yes, 15% = 14.41%** |
| **AMR** | 50 cash flow / 20 relative / 20 normalised / **10 book** | **0.0** | 0.5842075318817193 USD → 2.1455021608356137 AED | 2.2333080177520155 AED | **yes, 10% = 4.84%** |
| **CLHO** | 40 cash flow / 25 relative / 20 normalised / 15 EV-per-bed | **−1.24e-14** | 9.20515811305707 | 7.16903572416875 | no (no book lens) |
| **ELEC** | 40 cash flow / 20 relative / 20 normalised / **20 book** | **0.0** | 0.3357186228503667 | 0.01 *(floored)* | **yes, 20% = 54.17%** |
| **EMPOWER** | 50 cash flow / 20 relative / 15 normalised / **15 book** | **0.0** on all four branches | 1.835329801482165 (recovery, 9% CT) | 2.0996608323641923 | **yes, 15% = 13.32%** |
| **GBCO** | 40 SOTP / 15 pre-discount NAV / 20 relative / 25 normalised | **0.0** on bear, base and bull | 35.74687012834619 | 38.38008105397857 | no (no book lens) |
| **SAVOLA** | 45 cash flow / 25 relative / 15 normalised / **15 book** | **0.0** | 26.64244605169207 | 23.596156479763444 | **yes, 15% = 13.89%** |
| **XPT** | 30 ratio / 30 consensus / 20 balance / 20 cost | **−0.003** (2dp rounding at publication) | 1634.33 | 1831.09 | no issuer, no book — **but the cost-curve floor carries 20% = 15.91%** |

**Six of the nine weight book value**, which [R-LENS-03] forbids *separately from and in
addition to* the blend itself: book is a **disclosed floor, published as such and never
weighted**. A seventh, XPT, weights a floor by another name — its `cost` lens is described in
the study's own words as the *"deep-bear bound"* and carries a fifth of the answer.

Two details worth stating rather than flattening into the table:

- **AMR's blend runs through the dirham peg.** Its lens block is in dollars and its central in
  dirhams; 0.5842075318817193 × 3.6725 = 2.1455021608356137, the published figure to the last
  digit. A resolver comparing the two directly sees no relationship at all.
- **EMPOWER publishes four centrals** — two tax framings × two consumption cases — and *all
  four* sit on the same four weights, residual 0.0 throughout. The two continuation branches are
  written in the builder as a delta off the recovery branch, which is algebraically the same
  blend because the cash-flow weight is exactly 0.50.

---

## 2. What is unreadable, and exactly what was missing

**An unreadable study is not a clean one** [R-ENF-04], and putting it in the same column as a
conforming one is the defect this house has paid for before. Nothing below is reported as
conforming.

### Unreadable to a gate, readable to this census

| study | what is missing | consequence |
|---|---|---|
| **GBCO** | no top-level `central`/`spot` pair — the answer lives at `lenses.central.base` | `check_valuation_gap.py` prints *"study_numbers.json carries no central/spot pair"* and lists it under ANSWER NOT READABLE. It is the only such entry. Its blend nevertheless reproduces here to 0.0 on all three legs, from its own committed `lenses.weights`. |
| **XPT** | its numbers file is `study_numbers_xpt.json`, not `study_numbers.json` | invisible to the gap gate's glob; carried instead as an explicit exemption (*"metals study — no issuer, no equity fair value of this shape"*). The exemption is legitimate and the blend inside it is not visible through it. |
| **CLHO** | **no study directory exists at all** | already on `coverage_outstanding.json` as *"published fair value, no study directory"*. Every lens gate globs `engine/*_study`, so **no instrument in this repository examines CLHO**. Its blend was resolved from the delivered workbook (`files/CLHO_Valuation_Model_13072026_public.xlsx`, `Summary` rows 4–8, cached values), where `Summary!C8` is a live `SUMPRODUCT` of the lens bases and the declared weights at `Assumptions` row 56. |

### Unreadable to the rule's own gate, by construction

This is the finding under the finding, and it explains how nine blends survived a gate written
to catch exactly this. Measured live across all twenty-four directories:

| state | count | studies |
|---|---|---|
| **no `lens_record` at all** | **8** | ADNOCDIST, ADNOCDRILL, AMR, ELEC, EMPOWER, GBCO, SAVOLA, XPT |
| has a record but **exposes no `central`** — `assert_lens_design`'s identity clause reads `r.get("central")` and skips the whole block when it is absent | **9** | AMOC, ARCC, DU, EGCH, FERTIGLOBE, MODON, PHAR, RIYADHCABLE, SWDY |
| record **and** central — the clause named for the rule actually executes | **7** | ADNOCLS, AIRARABIA, BOROUGE, PHDC, SCEM, STC, TMGH |

**Seven of twenty-four studies are held to "the primary IS the central" by the gate.** The
eight with no record are on `lens_outstanding.json`'s ratchet and allowed to fail, which is the
ratchet working as designed — but **every one of the eight that still publishes a blend is in
that group**, so the blends and the blind spot are the same set. `check_lens_design.py` reports
*"24 examined, 15 conforming, 9 outstanding — OK, no new violations"* while nine studies publish
a weighted central.

The nine that skip the clause are a *different* hole and a quieter one: those records look
complete, pass the gate, and are simply never asked the question. None of them is currently a
blend — verified individually — so the hole is unexploited rather than harmless.

---

## 3. What the correction is worth, name by name

The central on the class primary, and what that does to the gap against the **latest known
price** (`engine/prices/SUPPLIED_03-09-2026.json`, supplied 3 September 2026; XPT against its own
struck 1608.37, no supplied platinum quote).

| study | blend | on the primary | correction | gap now | gap corrected | move |
|---|---|---|---|---|---|---|
| ADNOCDRILL | 4.9194 | 6.2083 | **+26.20%** | −15.2% | +7.0% | +22.2 pp |
| EMPOWER | 1.8353 | 2.0997 | **+14.40%** | +16.9% | +33.7% | +16.8 pp |
| XPT | 1634.33 | 1831.09 | **+12.04%** | +1.6% | +13.8% | +12.2 pp |
| ADNOCDIST | 4.4113 | 4.7840 | **+8.45%** | +9.7% | +19.0% | +9.3 pp |
| GBCO | 35.7469 | 38.3801 | **+7.37%** | +23.4% | +32.4% | +9.1 pp |
| AMR | 2.1455 | 2.2333 | **+4.09%** | −10.2% | −6.6% | +3.7 pp |
| SAVOLA | 26.6424 | 23.5962 | **−11.43%** | −12.1% | −22.1% | −10.1 pp |
| CLHO | 9.2052 | 7.1690 | **−22.12%** | −48.5% | −59.9% | −11.4 pp |
| ELEC | 0.3357 | 0.01 | **−97.02%** | −83.9% | −99.5% | −15.7 pp |

Second framings, where a study publishes two: **ADNOCDIST** Frame B 4.5821 → 5.1007 (+11.32%,
gap +14.0% → +26.9%); **ADNOCDRILL** on its framing B 4.9194 → 5.3970 (+9.71%, gap −15.2% →
−6.9%); **EMPOWER** on the 15% top-up branch 1.7220 → 1.9443 (+12.91%, gap +9.7% → +23.8%),
which crosses [R-GAP-01]'s band from inside to outside.

**ELEC's −97% is a floor artefact and must not be read as a number.** Its cash-flow lens is
clamped by `max(..., 0.01)`; unfloored it reads **−1.8082 a share**, because the base enterprise
value of 3,813mn does not cover net debt of 9,805mn. Three of ELEC's four weighted inputs are
bounds rather than valuations — the cash-flow clamp, a relative multiple clamped at 0.05 in
bear, base *and* bull, and book, which the rule itself names a floor. **A weighted mean of three
floors and one valuation is neither a floor nor a valuation.** The honest statement of ELEC's
correction is not that the value falls 97%; it is that the cash-flow lens says the equity is
worth less than nothing and the blend was holding a floor in front of it.

**Three of the nine cross [R-GAP-01]'s band from inside to outside on the correction** —
ADNOCDIST Frame A (+9.7% → +19.0%), EMPOWER's 15% branch (+9.7% → +23.8%) and XPT (+1.6% →
+13.8%) — and a fourth, GBCO, moves from +23.4% to +32.4%. On those names the blend is not
merely producing a different answer: it is **suppressing an audit obligation**, because the gate
fires on the size of the gap and the blend is what keeps the gap small.

---

## 4. The distribution of the corrections

**Sample A — the nine that still carry a blend:**

> **6 raise the value, 3 lower it.** Mean **−6.45%**, median **+7.37%**, mean absolute move
> **22.57%**. Two-sided sign test **p = 0.508** — no lean.
> Excluding ELEC's floored primary: 6 up, 2 down, mean **+4.87%**, median **+7.91%**, mean
> absolute move **13.26%**, p = 0.289.

The mean and the median disagree in sign because ELEC's −97% carries the mean on its own. The
median is the honest central figure here, and the mean absolute move is the one that matters.

**Sample B — the thirteen that have already retired a blend and commit its value.** Eleven are
single-valued:

| BOROUGE | MODON | DU | SCEM | RIYADHCABLE | ARCC | AMOC | AIRARABIA | ADNOCLS | SWDY | EGCH |
|---|---|---|---|---|---|---|---|---|---|---|
| +72.80% | +46.25% | +30.08% | +28.46% | +15.65% | +13.61% | +9.68% | +8.64% | −16.79% | −22.08% | −31.22% |

> **8 up, 3 down.** Mean **+14.10%**, median **+13.61%**, mean absolute move **26.84%**, p = 0.227.

**The other two are two-sided, and both split in opposite directions across their own branches.**
This is the sharpest evidence in the census that the direction is not a property of the
architecture, because here the *same* retired blend on the *same* company corrects both ways:

| study | retired blend | branch A | branch B |
|---|---|---|---|
| **FERTIGLOBE** | 2.1730 | 1.8105 — **−16.68%** | 2.6846 — **+23.55%** |
| **PHAR** | 42.9171 (Frame A) / 51.7184 (Frame B) | 36.6395 — **−14.63%** | 54.2420 — **+4.88%** |

FERTIGLOBE's own record names the mechanism: the blend *"averaged the primary's own two framings"*
— it was damping precisely the disagreement a two-sided answer exists to publish, which is a
worse failure than a wrong point estimate and is invisible in any single-figure comparison.

**Both samples independently: no lean, and the two-sided pair splits.** Combined across the
twenty single-valued architecture corrections in the book — **14 up, 6 down, mean +4.85%,
median +9.16%, mean absolute move 24.92%, sign test p = 0.115** (ex-ELEC: 14 up, 5 down,
mean +10.21%, median +9.68%, p = 0.064).

**The finding is the magnitude and the unpredictability, not a direction.** Retiring a blend
moves the answer by roughly a quarter, and *which way it moves is a fact about where the
discarded lenses happened to sit on that company* — not a property of the architecture. That is
precisely what an untested free parameter does, and it is a worse result for the blend than a
systematic bias would be: a bias can be corrected for, a coin-flip of twenty-five per cent
cannot.

**This sample was nearly read the other way, and the near-miss is recorded rather than
buried.** An earlier pass measured only the three blends it had then found, saw all three
sitting below their primaries, and drew a direction from them. That reading was withdrawn the
same day on a larger sample. The sample of *still-carrying* studies is selected on **not yet
corrected**, and the studies conformed first were conformed for reasons that sorted the
population before anybody measured it. This is [R-TERM-01 CLAUSE TWO]'s own lesson —
**a defect measured only where it hurts looks like a bias with a direction** — arriving inside
this reassessment's own work within hours of that clause being written.

---

## 5. PHDC's precedent, and the sharper replication

[R-LENS-03] was adopted on PHDC: its published central was a blend of four lenses at typed
weights, **three of which value a developer on reported accounting earnings and historical-cost
book** — a floor, not a value, for a company whose worth sits in an undelivered EGP 263bn order
book. **The cash-flow lens landed within 2.2% of the market; the blend landed 28% below.**
Nothing in that study was wrong except its architecture.

**ADNOCDRILL is the same case and sharper.** Its two cash-flow framings read 6.20828 and
5.39701. Their midpoint is **5.80264** against a latest known price of **5.80** — a gap of
**0.046%**, and the price sits near the middle of the study's own framing envelope. The published
blend is **4.91943, 15.2% below**.

**The entire discount is the blend.** There was never a market disagreement on this name to
explain, and the study's `GAP_REVIEW_05-09-2026.md` audits a −15.2% gap that its own cash-flow
work does not produce.

**CLHO is the same shape pointing the other way, and is the reason no direction may be claimed.**
Its cash-flow lens reads 7.169 against a blend of 9.205; there the discarded lenses sat *above*
the primary, the relative multiple at 13.21 carrying a quarter of the weight. Same architecture,
same defect, opposite sign.

---

## 6. Adjacent breaches of the same rule that are not blends

[R-LENS-03] has more than one clause, and three studies whose **central** is correctly the class
primary breach it elsewhere. These are named because a census reporting only `is_blend` would
report them clean.

- **DU** — envelope. The record attests `range_basis.macro_held = true` with the evidence
  sentence *"the macro path, the cost of capital and terminal growth held still"*; the builder
  moves the discount rate in both corners and terminal growth in the bull. Re-run with those
  dials actually held, the range is 13.20–18.87 against a published **10.57–27.67**: the two
  macro dials supply **66.9% of the published width**. The central does not move. The published
  bear sits *below* the spot; held properly it sits above it. The gate passes it because
  `macro_held` is a self-attested boolean and its other clause scans the `driver` prose for macro
  words that DU's string does not contain — [R-MACRO-01]'s own lesson one level up.
- **PHAR** — envelope. The field a reader is shown runs 36.64–56.78, and its upper bound is the
  **normalised-earnings read that the study's own `lens_record.lenses_excluded` carries** at
  56.78243923512581, with the reason *"not a permitted lens for any class in the registry ... it
  does not enter either centre"*. The record's own `lens_record.envelope`
  conforms; the delivered document does not use it. Separately, delivered §1.5 tells a reader the
  central is built at *"cash flow 50% … book value against sustainable return at 20%, relative
  15%, normalised 15%"* — the construction the rule forbids outright, asserted in prose, and
  attributing to it the DCF-only figures. **The record already carries those exact weights under
  `lens_record.retired_blend`, with its own values of 42.9171 and 51.7184** — so the model retired
  the blend and the delivered document still tells a reader the answer is built from it, at
  figures the weights do not produce. Model right, sentence false.
- **XPT** — envelope, in addition to its blend. The published field 1310.0–2138.6 is the *blend*
  re-run on each anchor's corners, not the range of the reads (1006–2400). §1.5 attributes each
  edge to a named lens — *"the bear edge is a cost-curve world … the bull edge is the stale
  consensus"* — and **neither edge is that lens's read**: cost bear is 1006 against a published
  1310, consensus bull is 2222 against a published 2138.6.
- **ADNOCLS** — the exemplar, whose central conforms and whose **delivered workbook still
  performs the retired arithmetic on the answer's own row**: `Summary` column F computes
  `F5..F8 = value × weight` and `F9 = SUM(F5:F8) = 6.7363`, printed in the row labelled *"CENTRAL
  — THE CASH-FLOW LENS, NOT A BLEND"*, whose answer cell reads 5.6054. A reader adding the printed
  column reaches the retired blend. Under [R-ENF-01 EXTENDED 04-Sep-2026] the exemplar is held to
  the standard the exemplar defines, and a new study built by opening it beside the work inherits
  that scaffolding looking exactly like the house standard.

**TMGH was tested and is not a blend.** Its resolved `central` of 91.8306 is the median of two
**cases of one lens** — the CDS and rating premium bases that [R-COC-01] requires published, and
which `research_protocol.py` names by name as the legitimate construction. It is printed in no
delivered document, no workbook cell and not on the live site; it exists so [R-GAP-01]'s gate can
read an answer. That is not averaging several *methods*. It carries a real defect of another
kind — a two-sided disagreement spanning +22.7% to −34.1% reads through that field as a single
−4.9% — which belongs to whatever consumes `central`, not to the lens architecture.

---

## 7. The other surface: what a reader is actually shown

The census above measures **studies**. `assets/data.js` is a different object and it has its own
answer for each name. Measured through a real JavaScript parse [R-ENF-03], **the live site
publishes the retired architecture for names whose studies have already retired it**:

- **FERTIGLOBE** — `fair {bear 1.27, base 2.15, full 2.79}`. The file's own committed comment
  names the weights: *"cash flow 45% / relative 20% / normalised 20% / book 15%"*, and they
  reproduce to −0.004 on the two-decimal legs it prints. Book carries 15%; the bear **is** the
  book floor; the bull **is** the normalised-earnings lens the delivered study withdraws in terms
  (*"it is left out because the multiple behind it was chosen rather than sourced"*). The study
  itself conforms and is two-sided at 1.8105 / 2.6846.
- **BOROUGE** — `fair {bear 1.30, base 1.48, full 2.55}` = {min, median, max} of the nine lens
  readings, base being `fair_mid_retired` exactly. The study publishes 2.3524 / 2.5543.
- **RIYADHCABLE** — `fair base 109.35`, reproducing as 45/20/20/**15 book** on the *pre-rebuild*
  lens reads. The study publishes 124.8948.
- **STC** — `fair base 47.11` = the retired 35/25/20/20, of which DDM and normalised earnings
  carry 45% between them and neither is a permitted cross-check for its class. The file links
  point at the 09-07-2026 edition, so the entire delivered set a reader currently reaches is the
  pre-rebuild blend.
- **SWDY**, **AIRARABIA**, **SCEM**, **ARCC**, **AMR**, **ELEC**, **CLHO** and others carry the
  same shape on stale payloads.

**Publishing is a separate, explicitly-requested step**, and under [R-GAP-02 CLAUSE THREE] the
whole book is held while Phase 1 proof is open — so a lagging site is expected and is not a
finding against any study. **What is a finding is that only five of twenty-four entries say so.**
AMOC, ARCC, EGCH, PHDC and TMGH carry *"PRE-CALIBRATION. HELD BACK FROM THE SITE,
DELIBERATELY."* The rest present a superseded weighted central as current, several of them
spelling out the retired weights in their own committed comment, with nothing marking them
superseded.

**No instrument compares `fair{}` against the lens architecture of the study behind it.**
`check_lens_design` reads the committed record; `check_lens_vocabulary`'s population is the
delivered documents; `check_valuation_gap` reads `study_numbers.json`; `check_fv_vintages` holds
`fair{}` to *having* a vintage, never to being the study's own answer. Closing that class rather
than the instance — the gap gate's own resolver already recovers a central, or a branch set, from
every study, and holding `data.js` to that resolution is the same instrument pointed at the
surface a reader reads.

---

## 8. What this does NOT establish

**This is a census of an architecture, not a calibration of it.** Every figure above is
arithmetic on committed records. Nothing here measures whether any of these answers is *right*.

- **It does not show that a blend is worse than its primary out of sample.** That is
  [R-VCAL-01]'s question and only [R-VCAL-01] can answer it, on vintages that have not matured.
  **Until it answers, the typed blend is retired** — the promotion rule applied to an
  architecture rather than a parameter. The objection to a blend has never rested on any
  measurement of its accuracy: **a number produced by averaging several methods is a new method
  with free parameters nobody tested**, and these particular weights were chosen, written down
  and inherited without ever clearing an out-of-sample test.
- **It does not establish a direction.** Fourteen up, six down, p = 0.115. Any sentence drawing
  a systematic lean from these twenty corrections is unsupported, and the version of that
  sentence written earlier in this reassessment was withdrawn on a larger sample within hours.
- **It does not price the corrections as *improvements*.** The correction column says what the
  central becomes on the class primary, nothing more. **Seven of the nine move the answer
  further from the market** (EMPOWER, XPT, ADNOCDIST, GBCO, SAVOLA, CLHO, ELEC) and two move it
  closer (ADNOCDRILL, AMR); four move the gap by more than ten percentage points. That is
  reported as measured. **A correction that moves the answer away from the price is not a reason
  to reconsider the correction** — and, equally, one that moves it toward the price is not
  evidence for it. ADNOCDRILL's correction happens to land on the traded price and CLHO's moves
  away; neither fact is evidence about the architecture, and reading the first as confirmation
  would be fitting to the market through the front door.
- **It does not clear the studies it does not name.** Sixteen directories carry no blend that
  this test could resolve, and that is not the same as the gate having cleared them: **seventeen
  of the twenty-four expose no field for `assert_lens_design`'s identity clause to read** — eight
  with no lens record at all, nine with a record carrying no `central`. Every one of them was
  resolved here by hand, one at a time, against its own committed arithmetic. What clears a study
  is the gate holding the quantity, and on seventeen of twenty-four it currently does not.
- **It does not repair anything.** No driver, weight, fair value, builder, artefact or delivered
  document was touched in producing this file. Each correction above is a **re-issue with a
  rebuild ledger** [R-REBUILD-01], recording the levers in the order applied, each naming the rule
  it serves, with an audit point declared in advance — and several of these names would take the
  lens lever alongside others, which is exactly the stacking that ledger exists to make visible.

---

## The general lesson, which is not about lenses

**A rule that names a construction is not enforced by a gate that reads a declaration.**
[R-LENS-03] has been in force since 2 September, its gate has run in CI since the day it was
adopted, it reports fifteen of twenty-four conforming and no new violations — and nine studies
publish a weighted central, six of them weighting a disclosed floor. The gate is not wrong: it
tests the primary's *kind*, its permitted cross-checks, whether a multiple is circular. **The one
thing it did not test until 5 September is the sentence the rule is named for**, and where it
now does, seventeen of twenty-four studies expose no field for it to test.

Where a rule governs a **quantity**, hold the quantity — and then check how many of the things
it governs actually expose one.
