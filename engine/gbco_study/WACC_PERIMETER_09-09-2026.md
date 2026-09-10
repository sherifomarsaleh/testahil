# GBCO — one leg, two debt definitions, four lines apart

**09-09-2026 · internal · nothing published · no number changed**

## The inconsistency, verified in the study's own code

| line | what it uses | figure |
|---|---|---:|
| `compute.py:290` | **GROUP** gross debt, to build the WACC that discounts the **auto leg** | **42,476.0** |
| `compute.py:346` | **AUTO leg** debt, "on the COMPANY'S OWN definition", to bridge that leg's enterprise value to its equity | **24,068.7** gross · 14,623.7 net |

The same model levers the assembler with the whole group's borrowings when it sets the
discount rate, and then bridges with the assembler's own borrowings when it converts the
result to equity. **The difference is EGP 18,407.3mn, and it is GB Capital's funding
book** — a lender's borrowings.

## Why it flatters rather than merely differs

The captive lender's debt does not sit idle in the weights. Because after-tax cost of debt
(~19.1%) is **below** cost of equity (~27.97%), adding the lender's funding book to the
weights **lowers** the rate that discounts the assembler's cash flows. The debt weight is
57.45% on the group book against roughly 45.7% like-for-like.

**A lender's borrowings are its raw material; an assembler's are its working capital.** The
two are not the same kind of liability and this study knows it — it is why the bridge at
line 346 uses the auto leg's own definition, and why the cost-of-funds note at line 300
carefully pulls GB Capital's funding cost OUT of the group finance line to measure the
rate. The perimeter is drawn correctly in two places and not in the third.

## What it is worth

**−5.10 a share**, taking the carrying branch from 41.35 to 36.25 and the round branch
from 52.35 to 47.24. The direction is DOWN, toward the market, and under [R-GAP-04] that
changes nothing about how it is treated: a correction is not more welcome for closing a
gap, and this one is recorded exactly as PHAR's associates finding was, which points the
other way.

## Why it is NOT applied in this pass

The weights need a consistent PAIR and only one half is observable. The auto leg's debt is
disclosed; the auto leg's **equity market value is not** — the group's market capitalisation
of 31,458 contains GB Capital and the MNT-Halan stake, so pairing auto debt against group
market cap would replace one perimeter error with its mirror image.

Three routes exist and they are different studies:

1. **Auto debt against an auto equity value derived from the study's own sum-of-the-parts** —
   internally consistent, but circular: the discount rate would then depend on the answer
   it produces, which [R-COC-02] refuses outright for the terminal and which should not be
   let in through the weights either.
2. **Auto debt against group market cap less the study's own carrying value for the other
   two legs** — a stated approximation, and the least circular of the three.
3. **Discount the group and bridge the group**, abandoning the sum-of-the-parts for a
   single consolidated read — coherent, and a different study from the one delivered.

The cost of debt is a separate question inside the same perimeter: the 26.53% is measured
on group interest INCLUDING GB Capital's cost of funds over group borrowings, which is the
right rate for a group and the wrong one for an assembler alone. No disclosure separates
auto interest from auto borrowings, so an auto-only rate cannot be built from what this
repository holds.

**What would settle it:** a segmented cost-of-funds disclosure in a GB Corp release, or the
standalone GB Auto statements — which exist on the issuer's IR site
(`GB_Corp_Standalone_English_30_June-2026.pdf`) and are **not** in
`engine/gbco_study/src/`, though the 08-Sep gap review says the standalone statements were
"read and committed" there. That is a second, smaller finding: a review claiming a source
this repository does not hold.
