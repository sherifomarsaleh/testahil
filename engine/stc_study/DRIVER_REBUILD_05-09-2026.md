# STC — the driver rule, pre-registered before it is coded

**5 September 2026.** [R-FCAL-01] requires the MECHANICAL rule and its parameters to be
stated before any error is computed, and the same discipline applies to a rebuild: a driver
rule written after the answer is known is a rule fitted to the answer. This file is the
rule. The model does not yet implement it.

## What it replaces

The delivered study forecasts four typed arrays — `g_cbu`, `g_ebu`, `g_wc`, `g_sub` —
with **no source, date or layer on any of them**, over a taxonomy the filings do not use.
Their implied real growth wanders from 0.68% to 0.00% across five years with nothing saying
why, which is what makes a typed nominal rate unfalsifiable: nobody reading the page can
tell whether 3.0% meant inflation plus a point or inflation minus one.

**This is also why STC is still on the macro ratchet.** [R-MACRO-01] requires every growth
rate to be stored as (real, inflation-path id) and to recompute to its nominal. A typed
array cannot be converted without *choosing* a real rate, and choosing one to clear a
checker is the offence the protocol names in three places. The rate has to be **measured**,
and this file is where it is measured.

## The evidence: every disclosed segment's own real growth

Nominal growth is the two-year compound rate from the company's own note 9, on the
continuing-operations basis, three filed years. It is deflated by Saudi consumer-price
inflation for the two years it spans — **1.5% in 2024 and 2.0% in 2025** — from the
International Monetary Fund's World Economic Outlook database, series PCPIPCH, Saudi Arabia,
read live on 5 September 2026. That is the same database, the same series and the same
country row the house macro path's forward ladder comes from, so the history and the
forecast are one economy rather than two.

| segment | FY2023 | FY2025 | share of FY2025 | nominal CAGR | **real CAGR** | projectable |
|---|---:|---:|---:|---:|---:|---|
| stc | 49,218,179 | 51,119,024 | 65.7% | +1.91% | **+0.16%** | yes |
| Channels | 14,194,210 | 14,085,195 | 18.1% | -0.38% | **-2.10%** | yes |
| Solutions | 11,040,493 | 12,730,189 | 16.4% | +7.38% | **+5.53%** | yes |
| stc Kuwait | 3,986,034 | 4,179,842 | 5.4% | +2.40% | **+0.64%** | yes |
| stc Bahrain | 1,913,287 | 1,967,830 | 2.5% | +1.42% | **-0.33%** | yes |
| Center 3 | 1,089,218 | 1,961,666 | 2.5% | +34.20% | **+31.89%** | no — regrouped |
| stc Bank | 1,063,006 | 1,401,027 | 1.8% | +14.80% | **+12.83%** | yes |
| Sirar | 588,606 | 826,545 | 1.1% | +18.50% | **+16.46%** | yes |
| Specialized | 397,492 | 355,306 | 0.5% | -5.46% | **-7.08%** | yes |
| iot2 | 72,539 | 321,668 | 0.4% | +110.58% | **+106.96%** | no — regrouped |
| SCCC | 72,150 | 303,969 | 0.4% | +105.26% | **+101.73%** | no — regrouped |
| Other operating segments | 709,843 | 65,059 | 0.1% | -69.73% | **-70.25%** | no — regrouped |
| **group** | **71,777,161** | **77,818,675** | 100.0% | **+4.12%** | **+2.33%** | |

## The rule, and every clause of it is mechanical

1. **A segment's forward REAL growth is its own two-year trailing real rate**, from the
   table above. Nothing is chosen; every figure is the company's own disclosure divided by
   a published price index.

2. **It fades linearly to ZERO REAL by the last explicit year.** `real(t) = real0 x (1 - t/5)`.
   The fade is not a free parameter dressed up: the terminal already states real growth of
   zero, so a segment still growing in real terms in the last explicit year would be
   capitalised at a rate it never reached — which is the defect [R-MACRO-01] names about
   explicit windows, and [R-TERM-01] about terminals. Fading to the number the terminal
   already assumes is what makes the two halves of the model one model.

3. **A REGROUPED line takes the group's real growth, not its own.** Center 3, iot2, SCCC and
   Other operating segments each have a "growth rate" that is an artefact of a segment
   appearing, disappearing or being re-defined between filings. iot2 reads +107% real and
   Other reads -70%; neither is a growth rate, both are re-groupings, and projecting either
   would be projecting an accounting change.

4. **Nominal recomputes from real on the house ladder**: `nominal(t) = (1 + real(t)) x
   (1 + inflation(t)) - 1`, with inflation from `engine/macro_paths/SA.json` and never
   from anything this study holds of its own.

5. **Gross profit is built per segment at its own disclosed margin**, held at the FY2025
   rate where three years support it, because margin is an OUTPUT of a cost build and this
   panel discloses cost only as the residual. Where a segment's gross profit is negative in
   any filed year — SCCC in FY2023 and FY2024 — its margin is not defined and the line is
   held at its FY2025 absolute contribution rather than grown.

## What this rule does NOT claim

It does not claim to be a better forecast. Extrapolating a two-year trailing rate is a
crude driver and it is chosen because it is **mechanical and sourced**, not because it is
clever: the point of [R-MACRO-01] is that a rate can be checked from outside the study, and
a measured rate can be while a typed one cannot. Two years is short, and it is stated as
short rather than presented as a trend.

It also does not reach the finest level SIGCM clause 2 asks for. Revenue as **volume times
price** needs subscriber counts and average revenue per user, which this company does not
disclose by segment in its financial statements; its investor presentations may, and those
are not yet in this study's register. Building at the disclosed segment level and flagging
the gap is what the rule requires where the unit data stops, and the gap is flagged here.

## What is still owed, and it is named rather than implied

- **A Saudi macro-history archive.** `engine/macro_history/` holds Egypt and nothing else.
  The three inflation prints above are today's World Economic Outlook vintage, which is the
  right vintage for measuring a trailing rate in a forward study and is NOT the point-in-time
  archive [R-VCAL-01] specifies for grading past origins. Each is committed as a dated scalar
  with its source, and the archive itself is outstanding.
- **The investor-relations register**, which is where subscriber and revenue-per-user data
  would come from if this company publishes it.
