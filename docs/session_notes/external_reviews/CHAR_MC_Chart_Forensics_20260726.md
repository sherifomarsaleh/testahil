# CHAR-MC §5/§6 cone charts — forensic reconstruction (26 Jul 2026)

Addendum to `CHAR_MC_Authentication_Audit_20260726.md`. Question: can the plotted red/blue bands
be reproduced from the paper's own published parameters, and with which formula?

**Answer: yes, and the formula is not the one in the paper's code. λ has been applied to the "old"
cone and stripped from the "new" one. That swap is the entire source of the apparent compression.**

## Decisive check — the blue band contradicts the paper's own tables

For SODIC the paper's §4 and §7 tables publish T+60 = **[19.34, 43.41]** (width 87.5% of spot).
The blue band plotted in §6 for the same asset runs roughly **[22.3, 37.7]** (width 56%). The chart's
"new CHAR-MC cone" is ~36% narrower than the number the same document publishes twice elsewhere.
No pixel precision is needed for this: the plotted blue upper bound sits below 40 while the table
says 43.41.

## Reconstruction (spot, σ, θ, λ all taken from the workbook, unchanged)

| formula | SODIC T+60 | Qalaa T+60 | matches |
|---|---|---|---|
| A `λ·σ` **with** saturation — the code and both tables | [19.34, 43.41] | [1.85, 3.16] | the published tables |
| B `σ` **no** saturation — the true old √t cone | [20.70, 40.56] | [1.90, 3.08] | — |
| C `λ·σ` **no** saturation | [17.32, 48.47] | [1.75, 3.34] | **the plotted RED band** |
| D `σ` **with** saturation | [22.25, 37.74] | [1.98, 2.95] | **the plotted BLUE band** |

Qalaa is essentially exact: D gives [1.98, 2.95] against a plotted band reading [2.00, 2.97].

So the charts plot **C vs D** — λ·σ·√t against σ·f(t) — while the code and tables produce **A**, and
the genuine old system is **B**. Neither plotted curve is a system that exists anywhere in the
document.

## What the honest comparison looks like

Same parameters, correct formulas: old **B** = 72% of spot at T+60; new **A** = 88%. **The new cone
is wider**, consistent with the audit's finding that all 32 of 32 assets have λ/√(1+θ√60) > 1
(median +20.2%). Reversing which curve carries λ is exactly what flips that on screen.

## Note on the figure captions

The §6 captions read "Corrected comparative price cone charts" and the document's opening states
"All visual charts have been corrected to accurately depict the Old System YZ-HAR-MC as the wider …
cone and the New CHAR-MC as the tighter … cone." That is a statement of the conclusion the charts
were made to show, not of what the parameters produce.

Artefacts: `chart_forensics.py`, `make_exhibit.py`, `CHAR_MC_chart_forensics.png` (session workspace).
