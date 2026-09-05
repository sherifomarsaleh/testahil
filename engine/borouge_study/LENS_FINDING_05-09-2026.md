# BOROUGE — what its published central actually is, and it is not a valuation choice

Written 5 September 2026 while diagnosing why seven studies are invisible to the
valuation-gap gate. **This is a finding, not a rebuild.** The rebuild is the next pass's
first job on this name and its audit point should be declared before it starts, because
three corrections stack here and two of them are large.

## The published central is a counting artefact

`compute.py:721-722` builds the answer this way:

```
vals = list(lenses.values())
FAIR_LOW, FAIR_HIGH = float(min(vals)), float(max(vals))
FAIR_MID = float(np.median(vals))
```

Nine lens readings, and the middle one is published. **The nine are not nine independent
views of the company.** They are a 2×2 grid of two orthogonal framings — a beta choice
(own-stock against bottom-up sector) and a scenario choice (normalisation against
prolonged) — plus a framing-neutral relative multiple. Sorted:

| | value |
|---|---:|
| normalised earnings, sector beta | 1.3012 |
| DCF prolonged, sector beta | 1.3100 |
| book value, sector beta | 1.4388 |
| relative multiples | 1.4599 |
| **DCF normalisation, sector beta — THE PUBLISHED CENTRAL** | **1.4770** |
| normalised earnings, own beta | 2.3458 |
| DCF prolonged, own beta | 2.3481 |
| book value, own beta | 2.3898 |
| DCF normalisation, own beta | 2.5499 |

**The readings do not spread — they cluster in two blocks, one per beta**, 1.30–1.48 and
2.35–2.55, with the relative multiple sitting inside the lower block. So the median does
not average anything: it SELECTS ONE CELL of the grid, and which cell it selects is
decided by how many lenses happen to have been computed under each framing.

**Four sector readings plus the framing-neutral relative multiple make five below the
gap; four own-beta readings sit above it, so the fifth of nine lands at the top of the
lower block.** Compute one more lens under the own-stock beta and the median moves to
**1.9114**. Drop one sector lens and it moves to **1.9028**. Neither of those is a
different view of the company — **it is a different number of rows in a list.**

That is the [R-LENS-03] failure in an unusually clean form. The rule is written against a
typed weighted blend; this is not one, and it is caught for the same reason it gives: *"a
number produced by averaging several methods is not more robust than the best of them — it
is a NEW method with free parameters nobody tested."* Here the free parameter is not even a
weight somebody chose. It is a count.

## And the cell it selects is built on a tier-2 beta while a tier-1 beta exists and passes

This is the part that makes the finding material rather than tidy.

`beta_result.json` records an own-stock five-year weekly regression against the FTSE ADX
General Index, `engine/raw_indices/AE/FADGI.csv`: **beta 0.4153, R² 9.45%, n 215, SE
0.0881, `usable: true`, `gate_msg: "passes minimum usability gate"`.** It carries a
`weak: true` flag — R² below a 10% weak-instrument threshold, and a 90% interval of
[0.27, 0.56] spanning 0.70× the point estimate.

SIGCM clause 6 and the BETA hierarchy are a STRICT PREFERENCE ORDER: the own-stock
regression is first choice **whenever that much usable history exists and it passes the
gate**, and a same-country peer beta is tier 2, reached only when tier 1 is unavailable.
This one is available and passes. **So the study's published number is built on the tier-2
beta, and the tier-1 cell — 2.5499 on the normalisation scenario — is the one the hierarchy
points at.**

**The bottom-up sector beta is a defensible RESPONSE to a weak instrument and it is not the
sanctioned one.** [R-COC-01] names the sanctioned escape and it is different: *a noisy beta
may be Vasicek-shrunk toward its market-class prior, with the raw beta and the shrinkage
disclosed.* Shrinkage keeps the tier-1 instrument and states how far it was pulled;
substitution replaces it silently with a tier-2 one. On a petrochemical company a raw beta
of 0.42 is implausibly low and the study was right to be uncomfortable — **the discomfort
was correct and the remedy was not the one the rules hold.**

## What the rebuild has to do, and why it needs a declared audit point

Three corrections, and they do not point the same way:

1. **The lens architecture** — [R-LENS-03]: one class primary IS the central. BOROUGE is
   registered `petrochemical`, whose row is a DCF primary with EV/EBITDA on own history,
   replacement cost, a relative multiple and book beside it. **Normalised earnings appears
   in no row of the registry at all**, so those two readings come out entirely — the same
   thing EMPOWER's record found, and the rule working rather than a gap in it.
2. **The beta** — tier 1 restored, Vasicek-shrunk toward the sector prior if the weakness
   warrants it, with the raw beta, the prior and the shrinkage all disclosed. The sector
   read stays as a labelled cross-check, which is what it is.
3. **The scenario pair** — normalisation against prolonged is a genuine contested judgement
   about the world and is the study's real two-sidedness. Published as two branches, or as
   the ENVELOPE of the present-value reads on one clock; never averaged.

**On the current numbers, (1) and (2) together move the central from 1.4770 toward 2.5499,
+72.6%, against a spot of 2.40 that is itself a month stale.** That takes the study from
38% below the price to roughly 6% above it, which crosses [R-GAP-02]'s publication block in
the direction that releases it — and that is exactly why the audit point is declared BEFORE
the levers are applied rather than after. [R-REBUILD-01] exists for this shape.

**None of the three is discretionary and none was chosen for where it lands.** Each is a
standing rule applied to a study that predates it.
