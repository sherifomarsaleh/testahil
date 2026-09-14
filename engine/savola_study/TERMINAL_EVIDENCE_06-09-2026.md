# SAVOLA — sourcing the disclosed useful life, and why it stops at a refusal

**Status: REFUSED on the weighted life, 6 September 2026.** No published number moves. The
disclosure was found, read twice by two routes, footed where it can be footed, weighted by
the note's own carrying amounts — and the weighting determines nothing. Written so the next
session does not re-derive a closed route.

## 1. The accounting-policies note, quoted as it stands

Audited consolidated financial statements for the year ended 31 December 2025 (Deloitte and
Touche & Co., unmodified opinion), note 4.8, PDF page 32 (printed page 30):

> *"Depreciation represents the systematic allocation of the depreciable amount of an asset
> over its estimated useful life. **Depreciable amount represents cost of an asset, or other
> amount substituted for cost, less its residual value.**"*
>
> *"Depreciation is charged to the profit or loss on a straight-line basis over the estimated
> useful lives of individual items of property, plant and equipment. Leased assets are
> depreciated over the shorter of the lease term and their useful lives. **Land is not
> depreciated.**"*
>
> *"The estimated useful lives of assets for current and comparative year is as follow:"*

| | Years |
|---|---:|
| Buildings | 5 - 50 |
| Leasehold improvements | 3 - 33 |
| Plant and equipment | 3 – 40 |
| Furniture and office equipment | 1 – 10 |
| Vehicles | 2 - 15 |

> *"Depreciation methods, useful lives and residual values are reviewed at least annually and
> adjusted prospectively if required."*

Construction work in progress does not depreciate until the asset is available for use
(note 4.9), so it leaves the depreciable base alongside land.

## 2. The route, and what the arithmetic could and could not arbitrate

**A life table carries no arithmetic and cannot be footed.** It was therefore read twice: the
text layer via `pdftotext -layout`, and off the rendered pixels at 200 dpi via `pdftoppm`. The
two agree character for character. A footing page beside an unfootable table does not certify
the unfootable table, which is why the pixels were required here rather than optional.

**What can be footed is note 6, the movement schedule that supplies the weights, and it does:
82 checks, zero failures** — every movement row summing across the seven classes to its printed
total, every class column rolling opening-plus-movements to its printed close, and net book
value reproducing as cost less accumulated depreciation by class and in total, in **both**
years. The text layer of note 6 is corroborated by its own arithmetic and needed no OCR.

## 3. The weights the note does disclose

Note 6, 31 December 2025, SR thousands:

| class | gross cost | accumulated | net book value | the year's charge | written down |
|---|---:|---:|---:|---:|---:|
| Buildings | 2,824,359 | 1,420,808 | 1,403,551 | 106,229 | 50.3% |
| Leasehold improvements | 2,133,648 | 1,320,733 | 812,915 | 138,025 | 61.9% |
| Plant and equipment | 2,563,647 | 1,448,812 | 1,114,835 | 133,349 | 56.5% |
| Furniture and office equipment | 3,011,907 | 2,291,773 | 720,134 | 217,297 | 76.1% |
| Vehicles | 446,993 | 381,577 | 65,416 | 14,033 | 85.4% |
| **depreciable base** | **10,980,554** | **6,863,703** | **4,116,851** | **608,933** | **62.5%** |

## 4. The weighting, and the refusal

Maintenance is the sum of each class's capital over its own life, so the aggregate life is the
capital-weighted **harmonic** mean, not the arithmetic one.

| weighting | every class at its LONGEST | every class at its SHORTEST | factor |
|---|---:|---:|---:|
| gross cost (10,980,554) | 21.27 y | 2.05 y | 10.4x |
| net book value (4,116,851) | 26.23 y | 2.46 y | 10.7x |

The implied maintenance charge on the gross base spans **SR 516mn to SR 5,366mn**. That is not
a life; it is the width of the disclosure. **Picking a figure out of it is this desk choosing a
life under cover of a citation, which is what [R-TERM-01] refuses outright (SIGCM clause 1),
so none is recorded.**

**This is the mirror image of the exemplar's refusal.** ADNOCLS discloses the lives and not the
composition — 97.85% of depreciable net book value in one column spanning six lives. SAVOLA
discloses the composition and not the lives: the weighting can actually be performed here, and
the bands it weights are so wide that performing it settles nothing. Both stop in the same
place for opposite reasons.

## 5. Three further things the accounts say, each of which would close the route on its own

**(i) Residual values, disclosed in terms.** The depreciable amount is cost *less its residual
value*, so the charge is (cost − residual)/life. Both identities off this note are therefore
**overstatements rather than measurements** — gross cost over the charge overstates the LIFE,
and accumulated depreciation over the charge overstates the AGE — and **no residual percentage
is quantified anywhere**, so neither can be corrected. This is [L-328] condition (i), and it is
the condition `terminal_value.py` already names this company for.

**(ii) The bands moved, and the note says they did not.** Four of the five classes are disclosed
differently in FY2025 than in the FY2024, FY2023 and FY2020 audited filings:

| class | FY2020 / FY2023 / FY2024 | FY2025 | |
|---|---|---|---|
| Buildings | 12.5 - 50 | 5 - 50 | changed |
| Leasehold improvements | 3 - 33 | 3 - 33 | unchanged |
| Plant and equipment | 3 - 30 | 3 - 40 | changed |
| Furniture and office equipment | 3 - 16 | 1 - 10 | changed |
| Vehicles | 4 - 10 | 2 - 15 | changed |

Both filings introduce the table with the same sentence — *"for current and comparative year"* —
so the FY2025 note asserts these bands describe 2024 as well, and the FY2024 audited filing's own
table for 2024 says otherwise. **No change in accounting estimate is quantified** anywhere in
FY2025. **Both tables were read off the rendered pixels**, so neither reading is an extraction
artefact; whether this is a re-description of the bands or a reassessment whose effect is
undisclosed is not decidable from outside, and it is [L-328] condition (ii) either way.

**(iii) The arithmetic contradicts the note on a third of the base.** Gross cost over each
class's own charge: buildings 26.59 y (inside 5-50), leasehold improvements 15.46 y (inside
3-33), plant and equipment 19.23 y (inside 3-40), **furniture and office equipment 13.86 y
against a disclosed maximum of 10**, and **vehicles 31.85 y against a disclosed maximum of 15**
— 2.1x it. Those two classes are **31.5% of depreciable gross cost**, and their bases are 76.1%
and 85.4% written down. The prior year does the same: on the FY2024 columns against the FY2024
bands, vehicles implies 26.15 y against a maximum of 10.

## 6. What the study commits today, and what the band would do to it

The study commits **18.03 years, derived by identity** (10,980,554 / 608,933) and labelled as
derived, cross-checked against FY2024's columns at 17.05. Both figures reproduce exactly and
**the cross-check is circular** — the same identity one year apart. The note is the test; the
arithmetic is a corroborator that here passes at 0.0% while the note closes the route.

**What the 18.03 actually does in that terminal is set an escalation window, not a divisor.**
Maintenance is built on `book_dna_escalated` over half the life — 9.015 years at 2% terminal
inflation, escalator 1.1954, maintenance 884.6 — because the model commits no replacement-cost
capital base. So the life stands in for an **age**, and a *shorter* life *lowers* maintenance and
*raises* the terminal, the opposite of what the word suggests. Anyone reading a life off this
record without reading the basis beside it will get the sign wrong.

Priced through the sanctioned module with everything else held exactly as committed, and with
the committed case reproduced bit-for-bit first (maintenance 884.6321, TV 14392.07381, identical
to the study's own record, which is what makes the rest comparable):

| life fed to the escalation window | maintenance | TV | vs committed |
|---|---:|---:|---:|
| committed 18.03 (identity) | 884.6 | 14,392.1 | — |
| gross-cost weighted, all classes LONGEST — 21.27 y | 913.5 | 13,872.8 | −3.61% |
| gross-cost weighted, all classes SHORTEST — 2.05 y | 755.2 | 16,723.0 | +16.20% |
| net-book weighted, LONGEST — 26.23 y | 959.5 | 13,044.9 | −9.36% |
| net-book weighted, SHORTEST — 2.46 y | 758.2 | 16,667.7 | +15.81% |
| FY2024 bands, gross-cost weighted, LONGEST — 24.97 y | 947.6 | 13,259.1 | −7.87% |
| FY2024 bands, gross-cost weighted, SHORTEST — 3.82 y | 768.5 | 16,482.6 | +14.53% |

**A 17.0% span on the terminal, and nothing here is applied.** This is the size of the
indeterminacy, not a correction, and no direction is claimed for a rebuild that has not run
[R-TERM-01 CLAUSE TWO CORRECTED].

## 7. Negative searches actually run

- **Residual value percentages** — not quantified anywhere in FY2025; only the policy sentence
  and critical-estimates note 2(a).
- **Maintenance / sustaining capex** — no such disclosure in any filing this study holds.
- **Depreciation rates by class** — none; this company discloses lives, not rates, so the route
  that pins EGCH's life at 3.95% → 25.3 years does not exist here.
- **AR2025 annual report** — carries no useful-life disclosure at all.

Any one of these would close the refusal. None is disclosed.

## 8. Two by-products, recorded rather than fixed

- **The earlier registry entry read the FY2024 filing** on a vintage note saying no FY2025 annual
  was listed on the company's investor-relations page. **The FY2025 annual audited statements were
  in this study's own `filings/` directory the whole time** (113 pages, full text layer, committed
  31 August 2026). [R-IND-01]'s ladder says open the artefact; that pass reasoned about a web page
  instead of listing a directory. Registry entry now superseded.
- **The committed `terminal_record.inputs` cannot be replayed verbatim** through
  `TerminalInputs(**inputs)` — it carries a `nominal_growth` key the dataclass rejects, since the
  module derives nominal growth and will not accept it. `terminal_correction_price.py` reports
  SAVOLA (with DU and MODON) as "its own committed inputs no longer build" for exactly this
  reason. Harmless to the record, and it means a replay must filter the key — as the pricing in
  section 6 did. Not fixed in this pass.
