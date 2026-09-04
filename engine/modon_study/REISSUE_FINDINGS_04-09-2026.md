# MODON — what the next rebuild must do, and what is now on disk to do it with

**04-Sep-2026 · internal · this study is not re-issued in this pass**

The study was delivered 09-Aug-2026 with a central of AED 3.542 against a spot of 2.83
(+25.2%). Nothing here changes it. What changed is that **three of the company's own
audited filings are now in the repository**, where before there were none, and two
defects are located precisely enough to be fixed rather than described.

## What arrived

| File | What it is |
|---|---|
| `sources/FS_FY2025.pdf` | Board of Directors' report and consolidated financial statements, 31 December 2025 |
| `sources/FS_FY2024.pdf` | Consolidated financial statements, 31 December 2024 |
| `sources/FS_H1_2026.pdf` | **Review report and interim condensed consolidated financial statements, 30 June 2026** |

All three from `modon.com/investor-relations?inv_tab=financial-information` — the
company's own site, reachable, serving its own documents. The study cited the FY2025
statements correctly and did not hold them; it holds them now.

## 1. A REVIEWED HALF-YEAR EXISTS AND THE STUDY DOES NOT USE IT

The 30-June-2026 interim is on the company's own investor-relations page. The study was
struck on 9 August 2026. `[R-BRIDGE-01]` clause (i) requires the bridge to stand on the
**latest disclosed balance sheet**, and this study carries no `bridge_record` at all, so
which sheet it stands on is not committed anywhere — which is the second finding and the
reason the first one could not be checked from outside.

**The next rebuild reads the half, re-bases the bridge on 30 June 2026, and commits a
bridge record.** Whether that moves the answer is not predicted here.

## 2. THE TERMINAL IS BELOW ITS OWN FLOOR, AND THE FIX IS BLOCKED BY A DISCLOSURE GAP

MODON's terminal is the retired reinvestment identity, and it is the only name in the
book whose terminal is worth **less than not investing at all** — 8.4% below the
no-growth perpetuity at book depreciation. Correcting it is worth at least **+6.2%**
(3.54 → 3.76 at the floor alone) and the sanctioned construction would be higher.

It cannot be built today, and the reason is recorded rather than worked around.
`[R-TERM-01]` needs a **disclosed** useful life; MODON discloses eight of them, and the
property note's own columns make them impossible to weight:

- **Land and buildings are ONE COLUMN** — AED 12,438,392 thousand, **73% of gross cost** —
  and **land is not depreciated at all** while buildings run 2 to 50 years. The
  depreciable base inside the largest class is unknown.
- **Plant (40 years) shares a column with machinery and equipment (3 to 4 years)** — a
  more than tenfold spread on AED 883,217 thousand.

**The charge-implied route is closed too, and for a reason worth recording.** FY2025
carried AED 832,492 thousand of assets acquired through business combinations, most of it
into the plant column, so a full-year charge over an average base measures the timing of
an acquisition rather than a life: the implied figures come out at **20.7 years on a
class disclosed at 3 to 4**, and **12.4 years on one disclosed at 2 to 5**.

A life this desk chose is not a disclosed life. MODON stays on the terminal ratchet **with
this reason**, the same disposition as ADNOCLS and for the same kind of gap. Recorded in
`engine/valuation_calibration/disclosed_lives.json`.

*The coincidence is worth naming so nobody mistakes it for a derivation: `1/g` at the
study's 2.5% is 40.0 years, which happens to equal the disclosed life of **plant alone**
while the rest of the base runs 2 to 5 years. That is an accident of two unrelated
numbers, not a validation.*

## 3. TERMINAL GROWTH IS TYPED AND ITS JUSTIFICATION IS THE WHOLE SENTENCE "Terminal growth 2.5%"

Against the AE house terminal inflation of 2.0% that is **+0.49% real growth in
perpetuity**, and the study argues for none. The house default is zero real, so the next
rebuild stores zero and derives 2.0% nominal — unless a real rate is argued for, in which
case it is argued for and stored. Either way the rate stops being unfalsifiable.

This is deliberately **not** done in isolation. Changing the growth rate inside the
retired terminal moves two terms in opposite directions on a construction the house has
retired, and `[R-REBUILD-01]` exists precisely to stop levers being applied one at a time
without the route being recorded. **The growth storage and the terminal rebuild are one
pass**, and that pass begins when the weighted life can be sourced.
