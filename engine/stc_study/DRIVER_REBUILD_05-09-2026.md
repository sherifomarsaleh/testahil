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

## Addendum, same day — the unit data exists, and it says the growth is volume

The rule above sits at the disclosed segment level and flags that **volume times price** was
out of reach because the financial statements carry no subscriber counts. **They do not; the
earnings presentations do**, and those are now registered — see `src/SOURCES.md` for the
route and for the correction that got there, which is that four failed URL guesses had been
recorded as evidence the investor-relations channel no longer resolved.

From the FY2025 presentation, KSA, and **every column foots to its own stated total**:

| | Q4 2024 | Q4 2025 | growth |
|---|---:|---:|---:|
| prepaid mobile | 21.1 | 22.2 | |
| postpaid mobile | 6.2 | 6.5 | |
| machine-to-machine | 1.0 | 1.3 | |
| **mobile subscribers, millions** | **28.3** | **30.0** | **+6.01%** |
| fixed telephone lines | 3.9 | 4.1 | |
| fixed-wired broadband | 1.3 | 1.4 | |
| fixed-wireless broadband | 0.5 | 0.5 | |
| **fixed subscribers, millions** | **5.7** | **6.0** | **+5.26%** |

The components sum to the stated totals in both years and both computed growth rates
reproduce the presentation's own stated 5.9% and 5.0% to the rounding of its chart labels.
These are chart figures rather than a table, which is exactly where a text layer can be
trusted least — so arithmetic is the arbiter, and it agrees.

**And it changes what the segment rule is measuring.** The `stc` segment's revenue grew
**2.97%** in FY2025 while the subscriber base it serves grew about **6%**. Revenue per
subscriber therefore fell about **2.9%** — 1,754 riyals a year to 1,704 on mobile alone,
1,460 to 1,420 across mobile and fixed together.

So the +0.16% real growth this rule extrapolates for two thirds of the business is the NET
of a volume line growing strongly and a price line falling. Extrapolating the net is not
wrong, and it is what the rule does; but it hides the two forces inside it, and a build that
projected them separately could say which one it expects to continue. **That is the next
refinement of this rule and it is now sourced rather than blocked.**

**One caution, recorded before anyone builds on it.** These are KSA subscriber counts and
the `stc` segment is the KSA operating business, so the two line up — but the presentation's
counts are explicitly *not audited*, they are read off a chart, and they are period-end
stocks against a full-year revenue flow. Each of those is a reason to treat the derived
revenue per subscriber as an INDICATOR rather than as a driver until the same figures are
found in a table.


---

## The cost side, decomposed and priced

The rule is that a gross margin set as an input is a fail wherever the filings disclose
enough to build cost instead, and note 35 breaks cost of revenues into seven lines by
nature. The model holds each **segment's** margin flat, so every line already sits on the
revenue of the segment it belongs to — which is the right base for most of the stack, and
is not the single blended index the cost-stack rule forbids. What it does not do is put the
lines whose driver is something *other* than revenue onto that other thing.

Four lines have a base the filings actually name. Each is priced against the model's own
final forecast year, in SR million:

| line | held at a share of revenue | on the base the filings name | difference |
|---|---:|---:|---:|
| Commercial service provisioning fees | 5,254.3 | 5,149.3 | -105.0 |
| License fees | 534.4 | 536.1 | +1.7 |
| Repairs and maintenance | 2,243.5 | 2,323.7 | +80.2 |
| Amortisation and impairment of contract costs | 216.3 | 281.4 | +65.1 |
| **net** | | | **+41.9** |

That is **-0.0473 points of margin** and, through the study's own
committed sensitivity grid, **37.1640 → 37.0521**, or
**-0.301%** of the central.

**The offsets run both ways and that is the finding.** The levy and the licence fee fall
against a group growing faster than the Saudi segment they are charged on; maintenance and
subscriber-acquisition costs rise against it; the two nearly cancel. The blended
construction is not hiding a mix effect here — which is worth establishing rather than
assuming, because the same test on another name in this book found one worth seventeen per
cent. Three tenths of one per cent does not justify adding four escalators, two of which
would rest on two observations apiece, so **the model is not rewired and the measurement is
what is committed.**

### Four lines are deliberately not priced

Inventing a driver to complete a table is worse than the gap it closes.

| line | share of FY2025 revenue | why not |
|---|---:|---|
| Network access charges | 12.97% | no disclosed unit rate |
| Employees costs | 7.12% | no headcount anywhere in the filings — searched, absent |
| Others | 3.48% | a residual of three unrelated things |
| Frequency spectrum fees | 0.34% | lumpy, and the first Saudi licence expiry falls **inside** the explicit window with no renewal cost disclosed |

The spectrum line is the one to watch rather than to model. It ran
361,932 then
137,427 then
265,470 across the three filed years — a
swing of roughly a hundred per cent in each direction — and escalating a three-year mean at
consumer-price inflation would dress a guess as a construction. It is named as a gap.

### Two things the sub-notes settle that nobody had

**The 724 million reversal is placed by arithmetic, not by inference.** The FY2024 filing's
footnote puts a non-recurring provision reversal of that size inside FY2023 government
charges and does not say which sub-line. Three of the four sub-lines are each *smaller than
the reversal* — License fees at 444,266,
Frequency spectrum fees at 361,932 and Others at
77,329 — so it cannot sit in any of them. It belongs to the commercial service
provisioning fee, and placing it there tightens that levy's own ratio against the Saudi
segment from a two-point step to
8.964% / 9.473% / 9.015%. The tightening is corroboration; the
deduction stands on the sizes alone, and `check()` fails if a restatement ever makes a
second sub-line large enough to carry it.

**The device line is not device cost of sales, and the split is unidentified.** The line
costs more than the devices sell for in every filed year — by 1,953,454,
2,186,801 and 1,561,502 — so it carries equipment and software consumed in operations as
well as handsets resold. Solving `cost = k x device revenue + e x revenue` across every
available period pair gives a device ratio ranging from **-1.08 to 5.86**,
two of the three pairs economically impossible. That is a split *demonstrated* unidentified
rather than asserted to be, and it is left alone rather than filled with an imported ratio.
