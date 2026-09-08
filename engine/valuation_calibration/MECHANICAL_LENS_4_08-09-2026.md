# Mechanical lens, declaration 4 — the terminal is a growing perpetuity on the last forecast year's cash flow

**Sealed and committed BEFORE any figure under it was computed.** That is the whole of
this document's claim on credibility, and it is a fact about commit order rather than an
assurance — the commit that introduces this file must be an ancestor of the commit
introducing any score computed under it, and that is checkable from outside.

This supersedes declaration 3 (`MECHANICAL_LENS_3_06-09-2026.md`) **in the terminal and
in nothing else.** Every other element of declaration 3 — the origins, the projections,
the cost of capital, the bridge, the point-in-time discipline, the two naive benchmarks,
the block bootstrap, the leave-one-name-out and era tests — stands exactly as written
there and is not restated here. A rule restated in two places is the drift this project
already closes elsewhere.

---

## 1. Why declaration 3's terminal is replaced

Declaration 3 charged perpetual upkeep at the trailing three-year median capital
spend. **At a past origin that window is frequently not a steady state**, and the
construction then produces an answer the module is right to refuse:

- a company mid-construction reads as needing many times its own depreciation for ever;
- a company in a spending lull reads as needing less than half of it;
- a company carrying a large working-capital base is charged inflation on all of it in
  perpetuity, which on one developer removed 42% of terminal profit.

Measured on the declared series before this declaration was written: **17 of 32 blocked
answers are blocked by that construction.** A terminal that refuses half the sample is
not a conservative terminal, it is a terminal that does not work at these origins.

**The principal's challenge, which this declaration accepts:** a perpetuity does not need
a separate model of perpetual capital spending. The last forecast year's free cash flow
already has that year's capital spending inside it. Growing that figure is the ordinary
construction and it makes one assumption where declaration 3 made a chain of them.

**What is NOT reinstated is the construction retired before declaration 3**, and this
document is explicit so nobody restores it by accident. That construction charged
`g x invested capital` every year for ever through the reinvestment identity, which makes
the implied asset replacement cycle `1/g` — the implied asset life becomes the reciprocal
of the *inflation rate*, 14.3 years at 7% and 6.7 years at 15%. An asset's life is not a
fact about a currency. That construction stays retired, permanently.

---

## 2. The terminal

For each origin, with the projection and the cost-of-capital schedule exactly as
declaration 3 builds them:

```
TV = FCF_N x (1 + g) / (WACC_terminal - g)
```

- **`FCF_N`** is the free cash flow of the **last explicit forecast year**, as that
  origin's own projection produces it — the same figure the explicit window discounts,
  taken without adjustment, re-derivation or normalisation. It already contains that
  year's capital spending and working-capital movement.
- **`WACC_terminal`** is the terminal rate the cost-of-capital schedule returns, unchanged
  from declaration 3.
- **`g`** is defined in §3.

**No separate maintenance charge, no separate growth-capital charge, no separate
working-capital charge, and no disclosed useful life is used or invented.** All three
belonged to the construction being replaced. The `disclosed_life` basis is likewise not
used: this declaration does not choose between declaration 3's two bases, it replaces the
question.

---

## 3. Terminal growth is real growth on the house inflation path, never a typed nominal rate

```
g = terminal_inflation(market) + real_growth
```

- **`terminal_inflation(market)`** comes from the house macro path and from nowhere else.
  It is not quoted here, because a number written into a document is a number that goes
  stale; it is read live at every run.
- **`real_growth` is 0.0 for every name in this declaration**, stated rather than
  defaulted silently. Zero real growth in perpetuity is the conservative standard reading
  and it is what the house macro path already returns for every terminal it builds.
- **A typed nominal rate is prohibited.** Nobody can tell whether a typed 5% meant
  inflation plus one point or inflation minus two, and in a market whose terminal
  inflation is 7% a typed 5% is a **permanent real decline of about 1.9% a year** that
  nothing in the filings supports. This project has already shipped that defect once and
  registered it.
- The growth rate and the discount rate therefore sit on **the same sourced inflation
  path**, so they cannot drift apart. That coherence is the reason for the construction,
  not a side effect of it.

Changing `real_growth` away from zero for any name is an amendment to this declaration,
made before the figures it affects are computed, with the evidence for that name's real
growth stated. It is not a per-name dial.

---

## 4. What still refuses, and what no longer does

**Refuses, and the origin is dropped:**

1. `g >= WACC_terminal`. The perpetuity does not converge; there is no value to compute.
2. `FCF_N <= 0`. A company whose last forecast year consumes cash cannot be capitalised
   as a growing perpetuity — that is a liquidation, and this lens does not value one.

**No longer refuses, because the quantities no longer exist in the construction:** the
implied-payout test, the terminal-free-cash-flow test as declaration 3 posed it, the
maintenance-versus-book-depreciation comparison, and every refusal that rested on a
disclosed or derived asset life.

**A terminal this declaration refuses drops the origin. It is not floored, not retried on
another basis, and not rebuilt by hand.** That sentence is inherited verbatim from
declaration 3 and it binds here exactly as it bound there — it is the sentence that stops
anyone shopping for a construction after seeing which answers fail, and replacing a
construction through a sealed declaration written in advance is the *only* sanctioned way
to change it.

---

## 5. What this construction gives up, stated now rather than discovered later

**The last forecast year must be a steady state, and this declaration does not test that
it is.** If an origin's final forecast year carries unusually heavy or unusually light
capital spending, the perpetuity inherits it and compounds it for ever. Declaration 3's
construction existed to defend against exactly that and paid for the defence by refusing
half the sample.

The defence given up is real and the exposure runs **both ways** — a light final year
overstates the terminal, a heavy one understates it — so it is not a conservatism and
must not be described as one. It is one visible assumption in place of a chain of derived
ones, and a reader can inspect the final forecast year directly, which is what makes it
the better trade at these origins.

**The direction is not predicted here.** Declaration 3's construction under-valued some
names and over-valued others, and nobody may claim in advance which way this one moves a
given answer. That is measured after this file is committed, never before.

---

## 6. Falsifier

If the answers this construction produces do not resemble the answers the house actually
delivers in its live studies — once that record is long enough to compare — then this
calibration is grading a method the house does not use, and every finding under it must
be withdrawn. Inherited from the standing valuation-calibration design and stated here
because a test with no falsifier is a habit.

---

## 7. Scope

Series (a) of the valuation calibration, on the markets the house macro path has sourced.
The delivered studies are not rebuilt by this document and no published fair value moves
because of it. Whether this construction should also govern the studies the house issues
is a separate question, decided separately, on evidence this declaration is written to
produce.
