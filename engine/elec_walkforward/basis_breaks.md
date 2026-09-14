# ELEC — basis-break register

**7 September 2026 · INTERNAL.** Built before any modelling, per §1 of the protocol.
Every figure is read off the rendered pixels of the company's own audited statements
and re-added against its own subtotal; `filed_record.py` reproduces the checks and
returns zero refusals.

## Break 1 — CONSOLIDATED to STANDALONE, and it is not chainable

| | |
|---|---|
| what changed | the reporting ENTITY, not a policy |
| last consolidated statement issued | **FY2020** (31-Dec-2020), auditor UHY United |
| every statement from mid-2021 onward | **standalone** (`المستقلة`) |
| overlap year | **FY2020** — it exists on both bases, which is what makes the wedge measurable rather than assumable |
| treatment | **NOT CHAINED.** The two series are reported separately and a driver is scored only inside its own definition window. |

### The chain factor, measured at the overlap

| line | consolidated FY2020 | standalone FY2020 | factor |
|---|---:|---:|---:|
| revenue | 1,740,090,697 | 1,003,350,740 | **1.73x** |
| gross profit | 211,697,261 | 59,145,112 | **3.58x** |
| operating profit | 121,562,003 | 3,524,172 | **34.49x** |
| net profit | 133,506,537 | 65,409,824 | **2.04x** |

Non-controlling interests in the consolidated FY2020 profit are **EGP 44** — the
subsidiaries are all but wholly owned, so the wedge is not a minority effect. It is
simply that the parent company on its own is a fraction of the group.

**The factor is wildly unstable down the statement — 1.73x on revenue and 34.5x on
operating profit — because the standalone parent's FY2020 operating profit was almost
nil (EGP 3.5mn on EGP 1,003mn of revenue). No single ratio restates one basis onto the
other, which is precisely why chaining is refused rather than attempted.**

### Why this break is the study's problem and not a technicality

Note 5 of the FY2023 standalone accounts discloses a **99.99%** holding in Giza Power
for Industry (EGP 299,999,800), 75.00% of Giza Egyptian for Transport and Distribution,
and 35.00% of OMS for Cable Manufacturing. The company therefore HAS subsidiaries to
consolidate and has published no consolidated statement for five years. The delivered
study models consolidated figures. **So the study's entire historical panel sits on a
basis for which the issuer has released nothing since FY2020, and the standalone
accounts are not a substitute — they are a smaller, different entity.**

## Break 2 — the share split, and it is fully documented

| | |
|---|---|
| resolution | EGM of 2 December 2020 approved a 1:5 split, par EGP 1.00 to EGP 0.20 |
| ratified | listing committee, 24 January 2021 — **after** the FY2020 balance-sheet date |
| effect | 711,447,385 shares become 3,557,236,925 |
| treatment | the FY2020 count is the **pre-split** one; FY2021 onward is post-split. No count is carried back [R-FCAL-01 AMENDED (ii)]. |
| foots | 711,447,385 / 0.20 = 3,557,236,925, the count the note itself states |

## Break 3 — IFRS 16 right-of-use assets first appear in FY2021

An office-headquarters right-of-use asset of EGP 10,425,929 gross appears in FY2021 and
is absent from FY2020, with amortisation of EGP 1,149,348 a year thereafter. D&A is
therefore reported here as fixed-asset depreciation PLUS right-of-use amortisation, so
that the series means the same thing in every year.

## Break 4 — a capital reduction between FY2022 and FY2023

Committed capital falls from EGP 711,447,385 to EGP 680,928,642, with treasury shares
moving from EGP 56,348,727 to EGP 52,265,165. The FY2023 capital note (note 12) sits
**past the point at which the committed PDF is truncated**, so the resolution behind it
cannot be read. The count is therefore taken as that year's own committed capital over
the par the FY2021 recital establishes — 680,928,642 / 0.20 = 3,404,643,210, which is
integral, itself a control on the par being unchanged. **Recorded as a break with what
is missing named, rather than passed over.**
