# The seven studies invisible to the valuation-gap gate — what each one actually needs

Written 5 September 2026, **after two wrong guesses about this same population in one
night**, so the next session works from a measurement rather than from either of them.

## The wrong guesses, recorded first

1. *"The causes split three ways and the fixes are nothing like each other — a filename the
   reader does not try, a bear/base/bull dict where a scalar is expected, and a retired
   multi-lens blend."* Half right. The filename and the dict are real, and **neither is a
   sufficient cause**: fix STC's filename and it is still unreadable, because underneath it
   has no single central either.
2. *"AMR, and probably ADNOCDIST, ADNOCDRILL and BOROUGE, have no single central because
   they still carry the typed multi-lens blend."* Right for ADNOCDRILL, **wrong for
   ADNOCDIST and BOROUGE**, which carry dual FRAMINGS and a published range — legitimate
   constructions, not blends.

Both were stated before the files were opened. The correction below was five minutes' work
and should have come first.

## What is actually there

| study | where its answer lives | shape | what it needs |
|---|---|---|---|
| **ADNOCDIST** | `lenses.centre_A` 4.4113 and `centre_B` 4.5821; `meta.spot` 4.07 | **dual framing** — two centres, deliberately | commit a two-sided block in the shape `read_branches()` reads. No lens decision needed; the study already made it. |
| **ADNOCDRILL** | `fair_value.central` 4.9194, from a typed **25/25/20/15/15 five-lens blend**; spot at `market.spot_aed` | **retired blend** [R-LENS-03] | a lens decision: the class primary IS the central, the rest are cross-checks. A rebuild. |
| **BOROUGE** | `fair_low` 1.3012 / `fair_mid` 1.4770 / `fair_high` 2.5498; `spot_usd`, `spot_aed` | a range with a mid, across **two framings** (normalisation vs prolonged) | care: `fair_mid` looks like a scalar central and is a midpoint ACROSS scenarios, which [R-LENS-03] forbids publishing as an answer. Probably two-sided. |
| **ELEC** | `lenses.central` = {bear, base, bull}; `spot` 2.19 | bear/base/bull dict | decide whether `base` is the central or the study is two-sided, then expose it. |
| **GBCO** | same shape, **with weights** | dict + blend | lens decision, then expose. |
| **STC** | same shape with weights, in a file named `stc_study_numbers.json` | filename + dict + blend | all three; a bank, so the class primary is the dividend model. |
| **AMR** | `lenses.central` 0.5842, from a typed **50/20/20/10 four-lens blend**; `meta.spot` | **retired blend** | lens decision. Its DCF reads 0.6081. |

*(XPT is no longer here: it is exempt, and the exemption is now enforced rather than
declared.)*

## The finding, which is the opposite of the first guess

**None of the seven is plumbing.** Every one needs a decision about what this study's answer
IS — a single central, two branches, or a range — before anything can be exposed to a
shared reader. The filename and the dict shape are real and they are the *last* step, not
the first.

**And that is the right answer rather than a disappointing one.** A gate that could be
satisfied by re-keying a JSON file would be satisfiable by publishing a blend [R-LENS-03]
retired, or a midpoint across two scenarios nobody is proposing. The reason these studies
are invisible is that they have not had the lens decision applied — which is exactly what
the gate should be unable to paper over.

## The order to take them in

1. **ADNOCDIST** — the only one needing no valuation judgement at all. Its two centres are
   already decided and named; they need committing in the shape the gate reads.
2. **ELEC** — one decision (is `base` the answer, or is it two-sided?) and no blend to retire.
3. **BOROUGE** — one decision, and the trap named above is worth avoiding deliberately.
4. **AMR, ADNOCDRILL, GBCO, STC** — each a genuine [R-LENS-03] rebuild, and STC additionally
   predates the v2 cost-of-capital method, so it is a rebuild rather than a patch on two
   counts.
