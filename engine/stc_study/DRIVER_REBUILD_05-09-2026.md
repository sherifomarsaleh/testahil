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

## The audit point for this stage, declared before the rule is coded

**AFTER THE WHOLE DRIVER REBUILD, AND NOT INSIDE IT.** The seven levers of
`REBUILD_PLAN_05-09-2026.md` are landed; this is a new stage and it gets its own declared
stop rather than borrowing that plan's. It is ONE rule applied in one place — the revenue
and margin build moves from four typed arrays to eleven disclosed segments — so there is no
intermediate state worth auditing: half the segments on measured rates and half on typed
ones is a model this study would never publish, and a look taken there would audit a
chimera. The rebuild lands as one lever serving [R-MACRO-01] and [R-SIGCM-02] together.

**The size is NOT known in advance and that is stated rather than discovered.** Group real
growth of +2.33% trailing is close to what the delivered arrays imply in aggregate, so the
headline may barely move — but the *composition* changes completely, because the four
aggregates do not map onto the eleven segments at all, and a segment growing at its own
rate compounds differently from a blend growing at an average of them. Whether that is worth
a percent or ten is not predicted here.

## Margins become outputs in the same pass, because the panel makes it possible

The delivered model types an EBITDA margin path of 31.8% rising to 32.5%. A margin set as an
input is a fail wherever the filings disclose enough to build the cost side instead, and
they do: the panel carries **gross profit per segment**, and the gap from group gross profit
to group EBITDA is one line — selling, general and administrative cost — which runs

| | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| gross profit | 34,740,066 | 37,325,924 | 37,699,689 |
| EBITDA | 22,445,389 | 23,951,115 | 24,469,435 |
| **the residual** | **12,294,677** | **13,374,809** | **13,230,254** |
| as a share of revenue | 17.13% | 17.62% | 17.00% |

so EBITDA is built as gross profit less that cost at its three-year average share of
revenue, and the EBITDA margin becomes an **output** of two sourced lines rather than an
assumption typed above them.
