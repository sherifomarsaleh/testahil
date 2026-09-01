# ARCC — fundamental walk-forward training record
### Arabian Cement Company (EGX: ARCC) · 01-Sep-2026 · **INTERNAL, never shown to a reader**

**Which walk-forward this is.** The FUNDAMENTAL one [R-FCAL-01]: the driver model
rebuilt as it stood at each past origin, projected forward, and scored against
what the company actually reported. It is not the price-engine walk-forward
(band coverage on the Monte Carlo cone) and it is not the technical walk-forward
(the shipped read replayed on a 5/10/21-session clock). The three are different
tests on different machinery and none substitutes for another.

**Campaign position 2 of 90.** The second name ever put through this method.
Everything below is PROVISIONAL for that reason [R-LESSON-01].

---

## 1 · Scope, and the documents behind it

**FULL run.** Twelve sourceable fiscal years, FY2014–FY2025, plus both disclosed
2026 quarters. Threshold for a full run is eight.

Thirty-four documents were retrieved from **arabiancementcompany.com**, the
company's own site — eleven audited consolidated filings, both 2026 interim
filings, ten earnings releases and eleven investor presentations. Every URL,
timestamp, HTTP status, byte count and sha256 is in `fetch_attempts.json`.
**No aggregator, broker or press report appears anywhere in this chain**
(SIGCM clause 1).

That the site was reachable at all is worth recording: `CLAUDE.md` carried
`arabiancementcompany.com` as `connect_rejected` from an earlier session, and it
answered 200 on the day this run was made. The block was re-probed rather than
believed — the rule that came out of that is [R-CAMP-01].

**Every audited filing is a pure scan.** Eleven fiscal years, zero characters of
text layer between them. The statements were rendered at 300dpi and read off the
pixels, and the route each figure came by is recorded in `panel.py`.

**Arithmetic is the arbiter, and it earned its keep on the first pass.** FY2016
income tax OCR'd as 224,683,515. The statement would not foot: 369,699,646 −
224,683,515 = 145,016,131 against a printed net profit of 245,016,131. The
footing forced 124,683,515, and the FY2017 filing's own comparative column then
confirmed it. **Nothing about that page looked broken.**

---

## 2 · The finding that changes how this name is modelled

**The earnings releases and the audited statements report different things, and
neither is wrong.**

| FY2024 | EGP |
|---|---|
| Earnings release, "Total Revenues" | 8,585,000,000 |
| Audited consolidated net sales | 8,729,782,821 |
| difference | 144,782,821 |

Note 36 (operating segments) resolves it to the pound: revenue from external
customers, **cement production segment = 8,585,462,048**, with ready-mix concrete
and alternative fuels making up the remainder. The release reports the cement
segment; the statements report the group. The gap is real revenue from a real
business, and it runs 0.9% to 3.5% of sales across the whole window.

**Consequence, and it is a prohibition, not a note.** Volumes and per-tonne
metrics describe the CEMENT SEGMENT. Group sales describe the GROUP. Dividing one
by the other to obtain "revenue per tonne" would inflate the price driver by one
to three and a half per cent, and no downstream diagnostic could separate that
from a genuine price move. The panel refuses the construction; §D2 of the
pre-registration uses segment revenue against segment volume throughout.

This is L-010 in a new costume — a value divided by a quantity that does not
describe it — and it was found by making the two sources foot against each other,
not by inspecting either one alone.

---

## 3 · Pre-registration and one amendment

`PRE_REGISTRATION_01-09-2026.md`, written before a single error was computed.
Seven origins (FY2018–FY2024), horizons 1–5 truncated at FY2025, **25 graded
cells per driver**, ten drivers with a stated mechanical rule each, two naive
benchmarks, log error, moving-block bootstrap over origins at {2,3,4}.

**Amendment A-1** was made before scoring and for a sourcing reason: ARCC reports
the national cement market as domestic + export up to FY2020 and as domestic only
from FY2021, so a consistent total-market series does not exist across the window
while a domestic one does. The volume anchor became *national domestic market ×
ACC domestic share*, with the export leg held flat.

The amendment carries its own check: the computed share **reproduces the ratio
ARCC itself publishes** — FY2019 8.14% against a printed 8.1%, FY2021 5.58%
against 5.6%, FY2022 6.29% against 6.3%. Including local clinker in the numerator
breaks the reproduction (FY2022 6.95% against 6.3%), which is how the right
numerator was identified rather than assumed.

---

## 4 · Results

### 4.1 Per-driver error

| driver | n | bias | MAE | over | sign cases | robust | era-stable |
|---|---|---|---|---|---|---|---|
| volume | 25 | −0.124 | 0.196 | 24% | 0 | YES | **NO** |
| revenue/tonne | 25 | −0.276 | 0.396 | 32% | 0 | YES | **NO** |
| cash cost/tonne | 25 | −0.315 | 0.406 | 28% | 0 | YES | yes |
| segment revenue | 25 | −0.400 | 0.545 | 36% | 0 | YES | **NO** |
| other revenue | 25 | +0.162 | 0.341 | 72% | 0 | no | yes |
| group sales | 25 | −0.385 | 0.533 | 36% | 0 | YES | **NO** |
| cash cost | 25 | −0.439 | 0.551 | 32% | 0 | YES | **NO** |
| G&A | 25 | −0.318 | 0.476 | 32% | 0 | YES | **NO** |
| finance costs | 14 | −0.545 | 0.813 | 36% | **11** | YES | yes |
| gross profit | 25 | +0.028 | 1.159 | 40% | 0 | no | **NO** |
| profit before tax | 23 | −0.002 | 1.122 | 35% | 2 | no | **NO** |
| **net profit** | 23 | **+0.059** | **1.144** | 39% | 2 | no | **NO** |

**Every operating driver is biased low.** The model under-forecast volume, price,
cost and revenue at essentially every origin. §4.3 says why, and it is not a
modelling failure.

### 4.2 Skill against the two naive benchmarks

**A METHOD THAT CANNOT BEAT "NO CHANGE" HAS NOT EARNED THE PRECISION IT DISPLAYS.**

| driver | n | build MAE | freeze | trend | verdict |
|---|---|---|---|---|---|
| volume | 25 | 0.196 | 0.157 | 0.227 | beats trend only |
| revenue/tonne | 25 | 0.396 | 0.550 | 0.448 | **beats both** |
| cash cost/tonne | 25 | 0.406 | 0.417 | 0.307 | beats freeze only |
| segment revenue | 25 | 0.545 | 0.665 | 0.597 | **beats both** |
| group sales | 25 | 0.533 | 0.653 | 0.586 | **beats both** |
| cash cost | 25 | 0.551 | 0.539 | 0.515 | **LOSES TO BOTH** |
| G&A | 25 | 0.476 | 0.574 | 0.580 | **beats both** |
| gross profit | 25 | 1.159 | 1.943 | 2.690 | **beats both** |
| **net profit** | 18 | **1.180** | 2.004 | 2.687 | **beats both** |

**On net profit the build beats freeze by 41% and trend by 56% on MAE. This is
the opposite of the PHDC result**, where the method could not beat "no change" on
net profit at any horizon. Two names is not a pattern, and this is recorded as an
observation about ARCC rather than a rehabilitation of the method.

**And two drivers lose.** Volume loses to freeze (0.196 against 0.157): ARCC's
own last-year volume beat an exogenous market-share build, because ACC's share
moved more than the market did — from 8.1% to 5.4% across the window as the
company pivoted to exports. Cash cost loses to both. Neither is explained away
below; both are named as weaknesses in §7.

### 4.3 Macro against company

| driver | knowable MAE | foresight MAE | macro share |
|---|---|---|---|
| volume | 0.196 | 0.196 | **0%** ← negative control |
| revenue/tonne | 0.396 | 0.192 | 51% |
| cash cost/tonne | 0.406 | 0.120 | **71%** |
| group sales | 0.533 | 0.345 | 35% |
| cash cost | 0.551 | 0.186 | 66% |
| gross profit | 1.094 | 1.293 | **−18%** |
| net profit | 1.106 | 1.504 | **−36%** |

**The negative control passed exactly.** Volume has no inflation and no FX term
in its rule, so its macro share must be zero by construction; it is zero to
machine precision, and `score.py` refuses to publish the decomposition otherwise.

**Two-thirds to three-quarters of the cost error is macro.** The pound went from
15.64 to 49.23 between 2021 and 2025. No origin could have known that, and the
knowable path — last year's move carried flat — was the only honest thing to give
the model.

**And the profit macro share is NEGATIVE, which is the most interesting number in
this record.** Perfect macro foresight makes the profit forecast **worse**
(−18% on gross profit, −36% on net profit). The reason is offsetting errors: the
knowable path under-escalates revenue and cost simultaneously, and the two misses
partly cancel in the margin. Correcting both breaks the cancellation, because the
cost escalator carries 79% weight on FX while the revenue escalator carries only
the export share, around 30–48%.

**So the model's profit accuracy under the knowable path is partly luck.** That
is worth saying plainly, because the headline in §4.2 — "beats both benchmarks on
net profit" — would otherwise read as more skill than the record supports.

### 4.4 The revenue error is a price error, not a volume error

The decomposition is an identity, ln(vol·rpt / vol*·rpt*) = ln(vol/vol*) +
ln(rpt/rpt*), and it closes to 4.4e−16.

    pooled segment-revenue error   −0.400
      from volume                  −0.124
      from price                   −0.276

**Price is 69% of it.** A cement model that spends its effort on volume and
treats price as an escalator has put its effort in the wrong place on this name.

### 4.5 The margin bias changes sign between eras — so it is not a bias

| origin | era | margin miss (pp, projected − actual) |
|---|---|---|
| 2018 | E2 post-float | +18.4, +30.5, +30.7, +24.0, +26.6 |
| 2019 | E2 post-float | +18.3, +19.5, +13.7, +17.2, +19.8 |
| 2020 | E2→E3 | +4.6, −1.5, +1.7, +4.1, −8.0 |
| 2021 | E3 devaluation | −3.6, −2.8, −2.5, −16.4 |
| 2022 | E3 devaluation | −1.6, −6.9, −26.5 |
| 2023 | E3 devaluation | −4.2, −25.8 |
| 2024 | E3 devaluation | −16.9 |

Origins before the devaluation over-forecast margin by 13 to 31 points. Origins
inside it under-forecast by up to 26. **The average of those two regimes was true
in neither** [L-029]. This is reported as instability and is not corrected for.

---

## 5 · Corrections — nothing promoted

Two drivers passed clause 1 (robust across all three block lengths **and**
sign-stable by era): **cash cost per tonne** and **finance costs**. Both were
refused at clause 2.

**cash cost per tonne — WATCH FLAG.** 71% of its error disappears under perfect
macro foresight. The driver is not biased; the macro path it was given was wrong.
Scaling cost per tonne up 16% at every origin would be correcting for an
unforecastable currency collapse and would be flatly wrong in a stable-currency
era, which is most of this book. Every other cement and heavy-industrial study
builds cost per tonne from a disclosed cost stack escalated per driver class,
with no name-level multiplier anywhere.

**finance costs — WATCH FLAG, and it names a SPECIFICATION DEFECT.** Eleven of
25 cells project a finance charge of exactly zero against a real one. The
pre-registered debt path amortises at the trailing average repayment and never
re-borrows, so once ARCC settled its entire debt in FY2023 the rule had the
company debt-free in perpetuity — and it then signed a EUR 25mn EBRD facility in
2025. **A multiplier on zero is still zero.** This is L-002 exactly: fix the
wiring, do not reach for a factor. The defect is named here for the next edition.

**The mechanical test corroborates both refusals rather than merely being
overridden by them**: on the adjusted-versus-raw comparison by origin, cash cost
per tonne improves in only 1 of 4 origins and finance costs in 2 of 3. Clause 1's
"pass" was already fragile on the data before clause 2 was consulted.

**PROMOTED INTO THE LIVE DRIVERS: NOTHING.**

---

## 6 · Years 3–5 as ranges

The measured log-error distribution on group sales:

| horizon | n | p10 | p50 | p90 |
|---|---|---|---|---|
| 1 | 7 | −0.308 | +0.002 | +0.193 |
| 2 | 6 | −0.741 | −0.145 | +0.385 |
| 3 | 5 | −1.066 | −0.508 | +0.225 |
| 4 | 4 | −1.430 | −0.913 | −0.134 |
| 5 | 3 | −1.483 | −0.892 | −0.267 |

At five years the spread is a factor of **3.4× on the level**. A point estimate
at that distance is a fiction, which is why the delivered study publishes years
3–5 as ranges and not as points.

**How the range must be read, and it is not a forecast of the company.** It is
the measured record of how wrong *this method* has been at this distance, and
that record is dominated by one unrepeatable event. The median error is negative
because no origin could foresee the pound. Carrying the width forward assumes
another shock of that size is as likely as not — a statement nobody has evidence
for. The range is published with that caveat attached, and **the bias inside it
is not promoted into the drivers**: clause 2 refused exactly that correction, and
re-centring the range would have smuggled it back in.

---

## 7 · The honest limits of this record

- **Two names.** ARCC is the second company ever put through this method. Every
  lesson below is PROVISIONAL and the code refuses to write one as adopted.
- **25 cells, not independent.** Horizons share origins and origins overlap. The
  intervals come from a block bootstrap over origins for that reason, and they
  are still wide.
- **One regime dominates.** Four of seven origins forecast into the 2022–2025
  devaluation. The record is a record of that event as much as of the method.
- **Volume loses to freeze.** The exogenous market-share anchor is worse than
  ARCC's own last-year volume, because ACC's share moved further than the market
  did. This is a weakness of the anchor on this name and it is not explained away.
- **Cash cost loses to both benchmarks.** Named, not softened.
- **Finance costs carry a specification defect**, described in §5 and not patched
  in this edition.
- **Fuel is not separately disclosed**, so the cost driver is `derived`, not
  `unit` [R-SIGCM-02]. The escalator rests on a composition assumption, stated in
  the study rather than implied away.
- **The profit skill is partly offsetting errors**, per §4.3, and the record says
  so beside the headline rather than underneath it.
