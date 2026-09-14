# ELEC — fundamental walk-forward [R-FCAL-01]: pre-registration and SCOPE DECISION

**Electro Cable Egypt · EGX · market EG · 7 September 2026 · INTERNAL**

**THIS IS THE FUNDAMENTAL WALK-FORWARD.** Not the price-engine one
(`elec_study/backtest_rows.csv`, band coverage on the Monte Carlo cone) and not the
technical one (`engine/lab/ta_calibration/`). The three are different tests on different
machinery and none substitutes for another.

---

## 0 · SCOPE DECISION — decided first, and it is SKIP

> **walk-forward not run — insufficient sourceable history (4 years)**

Recorded in those words, per §0 of the protocol, in the study's register and its QC
table. A SKIP is a completed queue position, not a deferred one.

**Three independent grounds, any one of which is sufficient. They are stated in the
order of how much they turn on judgement — the last one turns on none at all.**

### (a) §1's absolute clause fails: the most recent three fiscal years are not obtainable

§1 admits no exception — *"the most recent 3 fiscal years and all current-year quarters
MUST come from the company's audited financial statements or its own website /
investor-relations documents."* For a run dated September 2026 those are **FY2023,
FY2024 and FY2025**. FY2023 is in hand. **FY2024 and FY2025 are not, and cannot be.**

Every route was **re-run on 7 September 2026** rather than taken from the record, because
a written outcome is a fact about the past and an empty probe is first evidence the probe
did not run [R-ENF-04]:

| route | outcome today |
|---|---|
| `www.ececables.com` homepage and financial-statements index | **HTTP 200** — reachable |
| the index, ENUMERATED | **61 linked statement files.** The index **ends at 30 September 2025**: no FY2025 annual, no FY2024 annual beyond a listing, no 2026 period at all |
| every one of the **19** statement PDFs on the live host | **HTTP 404, 19 of 19**, each returning the same 54,573-byte WordPress error page |
| the **42** files on the legacy host `ece.allmediaegypt.com` | **DNS does not resolve.** Every consolidated statement is on this host |
| `www.egx.com.eg`, `disclosure.egx.com.eg`, `mist.com.eg` | connect failed at the relay on all three |
| every live ref of this repository (258 refs) | four filings and nothing later |

The issuer **publishes an index it does not serve**. This is not an environment problem
and must not be recorded as one — that error stood in this study for a month and is
already corrected in `SOURCE_BLOCK_04-09-2026.md`.

### (b) Fewer than five fiscal years are sourceable on any one basis

What the four committed filings actually yield, every figure read off the rendered pixels
and every subtotal re-added against its own statement (`filed_record.py`, **zero
refusals**):

| basis | years obtainable | count |
|---|---|---|
| **consolidated** — the basis the delivered study models | FY2019, FY2020 | **2** |
| **standalone** — the parent entity only | FY2020, FY2021, FY2022, FY2023 | **4** |

Four is below the five §0 requires for even a LIGHT run. The two bases **may not be
chained into a single six-year series**: they are different reporting entities, and the
wedge between them is measured rather than assumed in `basis_breaks.md` — at the one
overlap year the group is **1.73x** the parent on revenue and **34.5x** on operating
profit.

### (c) The design admits ZERO valid origins — this ground involves no threshold at all

An origin must be projected FROM and scored AGAINST a later actual. The last sourceable
actual is **FY2023**, so the last possible origin is FY2022 at h=1. An origin also needs
five years of history behind it, so FY2022 needs FY2018–FY2022 — and FY2018 does not
exist on any basis in hand.

**Every candidate origin fails one of the two conditions. The count of scoreable
origins is zero, and no choice of threshold changes that.**

---

## 1 · What is pre-registered, and what will not be computed

**NO ERROR WILL BE COMPUTED.** There are no origins, so there is no forecast, no
horizon, no benchmark comparison and no bootstrap. The pre-registration below is
recorded so the decision is auditable — it states what the run WOULD have been, so that
a later reader can see the scope call was made against a fixed design rather than after
looking at what the numbers would have shown.

| item | what it would have been |
|---|---|
| origins | annual, each with five years of history to it |
| horizons | 1–3 (LIGHT) had five to seven years been sourceable; 1–5 at eight or more |
| drivers | tonnes despatched; realised price per tonne (copper-linked); conversion cost per tonne; overheads fixed + variable; D&A off a PP&E roll-forward; interest off **the borrowings that actually bear it**; tax by formula; capex; working capital off the disclosed cycle |
| naive benchmarks | **freeze** = every line flat at last actual; **trend** = trailing 3-year CAGR. Both, at every horizon |
| score | log error per driver per horizon; bias, MAE, block-bootstrap CI over origins, share over/under, sign at every cut the data admits |
| macro split | re-run on the knowable inflation path and on perfect foresight; volume drivers carry no inflation term and must return a zero macro share by construction |
| samples | the rolling record estimates corrections; the non-overlapping origins confirm them |

**Parameters would have been stated, never fitted.** No judgement driver would have been
admitted at a historical origin — the exercise tests the method, not the analyst.

---

## 2 · What IS committed, despite the SKIP

A SKIP does not mean nothing is written down. Three artefacts are committed because the
filings are open now and, on today's evidence, will not be obtainable again:

1. **`valuation_inputs.json`** — the valuation-input block [R-FCAL-01 AMENDED] for
   FY2021–FY2023 with FY2020 as the prior-year anchor: cash, interest-bearing debt, PP&E,
   D&A, the working-capital lines, disclosed capex, and the share count **footed against
   the par value its own note establishes**. The record declares in its own text that
   `walkforward_origins_tested` is empty.
2. **`engine/elec_study/useful_lives.json`** — route (1) FAILED (the policy note
   discloses spans, and a range is not a life); route (2) derived and labelled derived,
   **17.54–24.13 years**, with a prior-year control at 24.99.
3. **`basis_breaks.md`** — the consolidated/standalone break with its overlap year and
   its measured chain factors.

---

## 3 · What this run does NOT do, and why

**It does not rebuild the study and it does not move `fair{bear,base,full}`.** The
reason is [R-FCAL-01]'s own second clause read at the level of the whole panel: the
delivered study's historicals are consolidated vendor figures, and this run establishes
by arithmetic that they cannot be reconciled to any document the company has issued.
Rebuilding on that base — in either direction — would be building further on the thing
that is wrong. The finding is recorded, the answer is left where it stands, and the
reason is stated rather than implied.

Signed off before any figure below was computed against any forecast, because no
forecast was made.
