# ARCC — critique adjudication register

**45 raised, 45 answered, 0 unaddressed.**

Source: the forensic audit of 18 September 2026 (`CRITIQUE_raw.md`), 45 rows in its Fail Table.
Plus **7 self-audit rows** found before the critique was read in detail, and **2 user-decision rows**.

**Status: REPORT ONLY. Nothing is implemented.** Procedure step 8.

Central under review **EGP 66.5300** against the latest known price of **EGP 76.60** (6 September 2026) — **-13.15%**.
1% of the central = **EGP 0.665**; the 5% escalation threshold = **EGP 3.327**.

| Bucket | All rows | Critique rows only |
|---|---:|---:|
| `accept-and-implement` | 40 | 34 |
| `accept-defect-reject-fix` | 7 | 7 |
| `unproven-go-research` | 0 | 0 |
| `reject-with-receipts` | 3 | 3 |
| `user-decision` | 4 | 1 |
| **Total** | **54** | **45** |

## How to read the price column

`price_egp` is the effect on the **published central** of adopting the finding's remedy against the
model as it stands today — `study_numbers.json` `central` = **EGP 66.5300405233**. Every non-zero price in
this register was produced by patching **this study's own `compute.py`** in an isolated sandbox,
asserting the patch landed before the run, and reading the central back; the patch and the result are
in each row's `evidence`. The sandbox reproduces the committed central to ten figures unpatched.

**A zero price is a measurement, not a dismissal.** 37 of the 45 rows price at 0.00 because this
critique is overwhelmingly about the *description* of a model whose arithmetic reconciles — which is
the audit's own conclusion and is correct. Every zero-priced row carries a `damage_note` saying what
it damages instead.

**Three prices in this register are the price of a BREACH rather than of a fix** — F-02, F-03 and
F-23 — and are labelled as such in their evidence. Adopting those remedies would de-anchor the
forecast from a reviewed filing or replace a house macro-path anchor with a study-local number.

`premise_verdict` and `conclusion_verdict` fail independently. **43 of the 45 rows are premise-RIGHT**,
which is the strongest thing that can be said about this critique: it is very rarely wrong about a
fact. 8 rows have a premise or a conclusion that is WRONG, and each carries its receipt.

**2 rows are flagged as duplicates of an earlier row.** None is merged away — a finding reached
twice is stronger evidence, not redundant evidence.

## The ten largest priced findings

| # | Row | Finding | Price EGP | % of central | Resulting gap | Bucket |
|---:|---|---|---:|---:|---:|---|
| 1 | `F-02` | Fail Table row 2 — FY2026 local price step | -14.1046 | -21.20% | -31.56% | `accept-defect-reject-fix` |
| 2 | `F-04` | Fail Table row 4 — Export price path | +13.0055 | +19.55% | +3.83% | `accept-defect-reject-fix` |
| 3 | `F-08` | Fail Table row 8 — The +12.0% beta alternative attributed to the wrong beta | +12.0072 | +18.05% | +2.53% | `accept-and-implement` |
| 4 | `F-03` | Fail Table row 3 — Four calibration multipliers absent from the register | -6.0080 | -9.03% | -20.99% | `accept-defect-reject-fix` |
| 5 | `SA-3` | The export dollar price declines 10.5% in nominal terms and the study never st | +3.1991 | +4.81% | -8.97% | `user-decision` |
| 6 | `UD-1` | USER DECISION — the export dollar price path | +3.1991 | +4.81% | -8.97% | `user-decision` |
| 7 | `F-25` | Fail Table row 25 — Terminal debt weight | -1.4904 | -2.24% | -15.09% | `user-decision` |
| 8 | `UD-2` | USER DECISION — the terminal debt weight of 20.0% | -1.4904 | -2.24% | -15.09% | `user-decision` |
| 9 | `F-32` | Fail Table row 32 — "Export clinker price — DERIVED" | -0.2202 | -0.33% | -13.43% | `accept-and-implement` |
| 10 | `F-20` | Fail Table row 20 — Debt book undated, does not reconcile with the bridge | +0.1929 | +0.29% | -12.89% | `accept-and-implement` |

Collapsed to **distinct things that are wrong** — the calibration rows F-02/F-03/F-04 are three
views of one construction, and SA-3 is the export half of F-04 measured separately:

| Distinct finding | Largest priced row | Price EGP | % |
|---|---|---:|---:|
| The four reviewed-half calibration multipliers are unregistered | `F-02` | -14.1046 | -21.20% |
| The beta choice contains the whole disagreement with the market | `F-08` | +12.0072 | +18.05% |
| The export dollar price path is an undisclosed real-terms decline | `SA-3` | +3.1991 | +4.81% |
| The terminal debt weight of 20.0% has no stated basis | `F-25` | -1.4904 | -2.24% |
| The terminal discount factor is misstated in the note AND the record | `SA-1` | +0.0000 | +0.00% |
| The cost-of-capital debt weight is struck on a superseded book | `F-20` | +0.1929 | +0.29% |
| The clinker export price is a typed ratio, not a derived price | `F-32` | -0.2202 | -0.33% |
| One cost of capital carries two tax bases | `F-22` | +0.0048 | +0.01% |

## The stack that matters

| | Central | Change | Gap to EGP 76.60 |
|---|---:|---:|---:|
| Published | 66.5300 | — | -13.15% |
| **The undisputed stack** — F-20 + F-22, the only accepted corrections that move the number | **66.7277** | **+0.30%** | **−12.89%** |
| Adding UD-1 branch B (export dollar price flat) | 69.9389 | +5.12% | −8.70% |

**THE UNDISPUTED STACK DOES NOT BRING ARCC INSIDE THE 10% BAND.** It moves the central by EGP 0.1977,
from −13.15% to −12.89%. This is the opposite of the AMOC result, and the reason is structural rather
than a matter of degree: AMOC's audit found four *modelling* errors the study did not dispute, while
this audit found — correctly, and it says so itself — that ARCC's arithmetic reconciles to ten
significant figures and what fails is the *description* of it. 37 of its 45 rows cannot move a
valuation at all, because they are about what the page says and not about what the model does.

**What would close the gap, and why none of it is in the undisputed stack:**

- **UD-1 branch B**, the export dollar price held flat: **+4.81%, gap −8.97%.** Refused by no assertion
  in the model, and it is the convention AMOC registers. It is a user-decision because the book's own
  remedy for this class is to NAME the real decline rather than change the path.
- **SA-1 / F-18**, making the model discount the terminal on the factor its own record and note both
  state: **+4.57%, gap −9.18%.** Rejected as a fix — the model is economically right and the record is
  wrong, so the fix is to correct the record at 0.00.
- **F-08**, the withdrawn basket beta of 0.628: **+18.05%, gap +2.53%**, a premium. Not a correction —
  it is the reverse read [R-ENF-05] requires the study to PUBLISH, and publishing it is accepted.

## Register

### `accept-and-implement` — 40 rows

| Row | Location | Finding | P | C | Price EGP | % | What it damages / what will be done |
|---|---|---|:-:|:-:|---:|---:|---|
| `F-08` | §1.5; §7; Table C2 | Fail Table row 8 — The +12.0% beta alternative attributed to the wrong beta | Y | Y | +12.0072 | +18.05% | Publish the reverse read: state the beta at which the lens meets the price, and attribute 74.54 to the 0.698 regression. |
| `F-32` | §1.2 Table 2 | Fail Table row 32 — "Export clinker price — DERIVED" | Y | Y | -0.2202 | -0.33% | Label 0.65 an input in the document and test only the clinker price against the clinker benchmark. |
| `F-20` | Table 5 | Fail Table row 20 — Debt book undated, does not reconcile with the bridge | Y | Y | +0.1929 | +0.29% | Date the table and strike the weight on the 30-Jun-2026 book. ACCEPTED AND IN THE UNDISPUTED STACK. |
| `F-22` | Table 6; DCF!C42 | Fail Table row 22 — Debt tax shield on the statutory rate, cash flows on the effective r | Y | Y | +0.0048 | +0.01% | Pick one basis and state it. ACCEPTED AND IN THE UNDISPUTED STACK. |
| `F-01` | §1.6; Table 3; Table 9 | Fail Table row 1 — Direction of the margin path | Y | Y | +0.0000 | +0.00% | The study's central stated judgement is the opposite of its own model's behaviour. §1.6 tells a reader the margin erodes while Table 9 prints it rising. |
| `F-05` | §1.8; Table 11 note; Table C2 | Fail Table row 5 — Stated mechanism for "growth destroys value" | Y | Y | +0.0000 | +0.00% | Describe the real-growth capital charge, which is what the model does. |
| `F-07` | §1.2; Segments!A83-84 | Fail Table row 7 — "It is not forced to" | Y | Y | +0.0000 | +0.00% | Delete the claim; the real test is the derived prices, as the workbook says. |
| `F-09` | §3; Table 18; §7 | Fail Table row 9 — Every calibration statistic for the price map | Y | Y | +0.0000 | +0.00% | Print the model's own 16 windows, its 100%/56.25% coverage and its too-wide conclusion. |
| `F-10` | §1.10 | Fail Table row 10 — Supporting paragraphs built against a superseded central | Y | Y | +0.0000 | +0.00% | Regenerate §1.10 against the published central, or withdraw it. |
| `F-11` | §1.2 physical constraint | Fail Table row 11 — Kiln headroom | Y | Y | +0.0000 | +0.00% | Print the workbook's clinker requirement; a tonne of exported clinker needs 1.0t of clinker. |
| `F-13` | Table 8; Table 13 beta row | Fail Table row 13 — Pasted beta re-runs carry the retired double-levering | Y | Y | +0.0000 | +0.00% | Regenerate the grid and the Table 13 alternative from the corrected formula. |
| `F-14` | Table 11 | Fail Table row 14 — Published growth grid inconsistent with the live formula | Y | Y | +0.0000 | +0.00% | Regenerate the grid from the live formula. |
| `F-15` | Sensitivity!A2; "About this series" | Fail Table row 15 — "A workbook that recalculates this study live" | Y | Y | +0.0000 | +0.00% | Recalculate and save the workbook before delivery; regenerate the two stale blocks. |
| `F-16` | Table A2; Table A3 | Fail Table row 16 — A deduction the model makes and the page does not print | Y | Y | +0.0000 | +0.00% | Print the FY2025 dividend as its own row in the FY2026 column. |
| `F-17` | Table C2 | Fail Table row 17 — DCF corners misquoted, direction word wrong | Y | Y | +0.0000 | +0.00% | Quote 67.08 / 24.61. |
| `F-19` | §1.8; §7; Table C2; DCF!B24 | Fail Table row 19 — Terminal return on capital | Y | Y | +0.0000 | +0.00% | Print the ratio the model computes, or change the cell. The 782bp gap becomes 708bp. |
| `F-24` | Table 6; DCF!C47 | Fail Table row 24 — Terminal beta construction not named | Y | Y | +0.0000 | +0.00% | Emit ke_terminal_construction='relevered' with its tax rate, and name the construction in the table. One field; it closes a ratchet entry. |
| `F-26` | §7 | Fail Table row 26 — Source dates do not support the figures used | Y | Y | +0.0000 | +0.00% | Name the H1-2026 review and its 13-Aug-2026 filing date in §7 and in the forecast_anchor record. |
| `F-27` | §7 | Fail Table row 27 — A false negative result about the study's own primary evidence | Y | Y | +0.0000 | +0.00% | Delete the stale caveat. |
| `F-28` | §7 | Fail Table row 28 — Treasury-share statement superseded | Y | Y | +0.0000 | +0.00% | Compute the count from the 30-Jun capital in the prose as the model already does in fact. |
| `F-29` | §1.10 | Fail Table row 29 — Risk-free instrument mislabelled | Y | Y | +0.0000 | +0.00% | Correct the label and show all three readings. |
| `F-31` | Register row 190 | Fail Table row 31 — This study's own figure attributed to EFG | Y | Y | +0.0000 | +0.00% | Re-attribute the figure to this study. |
| `F-33` | Table 19 | Fail Table row 33 — Three of four lens ranges are mechanical +/-10% bands | Y | Y | +0.0000 | +0.00% | Build every range on a driver, or label the bands as arbitrary. |
| `F-34` | Table 3 | Fail Table row 34 — "Range across the reads \| 45.65 - 65.57" | Y | Y | +0.0000 | +0.00% | Relabel "range across the cross-checks". |
| `F-35` | §1.11 vs headline | Fail Table row 35 — Two centrals | Y | Y | +0.0000 | +0.00% | Name one central — the published 66.53 — and withdraw the §1.11 sentence. |
| `F-36` | Table 16 | Fail Table row 36 — A scenario whose stated variation cannot move the metric shown | Y | Y | +0.0000 | +0.00% | Drop the row or report it on the lens it moves. |
| `F-37` | §B.2; Peer & Sector | Fail Table row 37 — Two incompatible characterisations of the same market | Y | Y | +0.0000 | +0.00% | Use one basis and compute utilisation on production. |
| `F-38` | Table B1; §4 | Fail Table row 38 — "A cement peer group trading at 6.2 times earnings" | Y | Y | +0.0000 | +0.00% | Source the peer financials, state n=2, and show the EV/EBITDA anchor the 4.5x rests on. |
| `F-39` | Assumptions!B10 | Fail Table row 39 — The beta cell is labelled as the construction the study rejects | Y | Y | +0.0000 | +0.00% | Relabel the cell and register the peer betas in the model. |
| `F-40` | SOTP Bridge!A19-20 | Fail Table row 40 — False statement about the live construction | Y | Y | +0.0000 | +0.00% | Delete the note. |
| `F-42` | Table 14 | Fail Table row 42 — "Bars sum to the gap exactly" | Y | Y | +0.0000 | +0.00% | Print bars that sum. |
| `F-43` | Assumptions!B5 | Fail Table row 43 — Stale date on the single most-cited input | Y | Y | +0.0000 | +0.00% | Fix the comment. |
| `F-44` | Monte Carlo!B14-B21 | Fail Table row 44 — Live formulas computing against the wrong anchor | Y | Y | +0.0000 | +0.00% | Anchor the memo cells on 59.00. |
| `F-45` | Summary!A8 | Fail Table row 45 — Role description contradicted by the document | Y | Y | +0.0000 | +0.00% | Correct the label. |
| `SA-1` | study_numbers.json cost_of_capital_record; c | The committed cost-of-capital record states a terminal discount factor the model does no | Y | Y | +0.0000 | +0.00% | Correct terminal_discount_factor to the applied 0.4155507 and declare the mid-period convention, which [R-COC-01 AMENDED] expressly permits. |
| `SA-2` | study_numbers.json forecast_anchor | The forecast-anchor record names FY2025 as the latest reviewed period while the model an | Y | Y | +0.0000 | +0.00% | Name the H1-2026 reviewed half, its 30-Jun-2026 date and its implied margin in the record. |
| `SA-4` | beta_result.json; docx_arcc.py:554-556; scri | ARCC quotes three testable beta diagnostics, names no estimator, and is invisible to the | Y | Y | +0.0000 | +0.00% | Emit the beta record into study_numbers.json and print beta_regression.estimator_note() beside the diagnostics. Separately, the gate should count records read against study directories rathe |
| `SA-5` | beta_result.json | beta_result.json pairs the adopted peer-median beta with the own-stock regression's diag | Y | Y | +0.0000 | +0.00% | Carry the tier-2 record's own dispersion, or mark the diagnostics as belonging to the rejected tier-1 attempt. |
| `SA-6` | engine/build_depth_audit/*.json | The study carries 15 open ratchet entries, and the two most valuation-relevant are the o | Y | Y | +0.0000 | +0.00% | No action in this pass; recorded so the debt is countable rather than remembered. |
| `SA-7` | engine/arcc_study/ (all records and builders | No deferral in this study cites the promotion guard as its reason — the [R-REBUILD-01 CL | Y | Y | +0.0000 | +0.00% | Nothing to fix. Reported because the instruction asked for it and a negative result that was actually run is worth stating. |

### `accept-defect-reject-fix` — 7 rows

| Row | Location | Finding | P | C | Price EGP | % | What it damages / what will be done |
|---|---|---|:-:|:-:|---:|---:|---|
| `F-02` | §1.6; §5; Assumptions!B142 | Fail Table row 2 — FY2026 local price step | Y | N | -14.1046 | -21.20% | Publish the charged step (+16.5%) and register the multiplier as a derived quantity. Do not change the driver. |
| `F-04` | §1.2 Table 2; §7 | Fail Table row 4 — Export price path | Y | ~ | +13.0055 | +19.55% | Disclose the dollar index and its basis. The path itself is a user-decision row (UD-1) priced separately. |
| `F-03` | Assumptions!B142-B145 | Fail Table row 3 — Four calibration multipliers absent from the register | Y | N | -6.0080 | -9.03% | Register all four as DERIVED quantities — reviewed H1-2026 statements as source, the scaling identity as construction, 13-Aug-2026 as date. Deleting them is refused. |
| `F-06` | §1.8; Table 6 note; DCF!B22 | Fail Table row 6 — "EGP 51,191mn, being 5.0Mt at USD 130 a tonne" | Y | N | +0.0000 | +0.00% | State the escalation in the note and use one stated FX convention per figure. The number does not move. |
| `F-18` | Table 7 note | Fail Table row 18 — "brought home on year five's own cumulative factor" | Y | Y | +0.0000 | +0.00% | State the convention, print the terminal FCFF (3,310) and TV (31,227), and correct cost_of_capital_record.terminal_discount_factor to the factor the model applies. |
| `F-30` | Register rows 203, 197; §1.4 | Fail Table row 30 — Terminal risk-free rate's stated derivation does not reproduce it | Y | N | +0.0000 | +0.00% | Reconcile the register note to the adopted figure: mark the 5% argument superseded. The number does not move. |
| `F-41` | §1.2; register | Fail Table row 41 — Basis mismatch between the volumes and the revenue divided by them | Y | N | +0.0000 | +0.00% | Disclose that the volumes are presentation-basis and the revenue audited, and that the calibration absorbs the difference. Do not re-base. |

### `reject-with-receipts` — 3 rows

| Row | Location | Finding | P | C | Price EGP | % | What it damages / what will be done |
|---|---|---|:-:|:-:|---:|---:|---|
| `F-12` | §1.2; §5 | Fail Table row 12 — 30% export cap tested on one leg only | Y | N | +0.0000 | +0.00% | Show both legs and state the basis the cap is tested on. The volumes do not change. |
| `F-21` | Table 5 | Fail Table row 21 — EUR balances imply EGP 48.0/EUR against EGP 50.30/USD | N | N | +0.0000 | +0.00% | No change to the model. Label the EUR column "facility drawn" rather than letting it read as a translated balance. |
| `F-23` | Table 6; Assumptions!B46 | Fail Table row 23 — Terminal cost of debt | N | N | +0.0000 | +0.00% | Print the pre-tax 15.00% and name the house macro path as its source. Do not re-derive it. |

### `user-decision` — 4 rows

| Row | Location | Finding | P | C | Price EGP | % | What it damages / what will be done |
|---|---|---|:-:|:-:|---:|---:|---|
| `SA-3` | compute.py:676 price_exp_path; macro_record. | The export dollar price declines 10.5% in nominal terms and the study never states it as | Y | Y | +3.1991 | +4.81% | Routed to UD-1. Whichever branch is taken, the real-terms decline must be NAMED, which is how the flat_nominal ratchet says an entry closes. |
| `UD-1` | compute.py:676 | USER DECISION — the export dollar price path | Y | ? | +3.1991 | +4.81% | RECOMMENDATION: BRANCH A. The book's own remedy for this class, recorded on the flat_nominal ratchet today, is that 'an entry closes by NAMING the real decline … It does NOT close by removin |
| `F-25` | Table 6; Assumptions!B49 | Fail Table row 25 — Terminal debt weight | Y | Y | -1.4904 | -2.24% | Routed to UD-2: this is a real judgement with EGP 1.49 at stake and no stated basis either way. |
| `UD-2` | compute.py:853 | USER DECISION — the terminal debt weight of 20.0% | Y | ? | -1.4904 | -2.24% | RECOMMENDATION: BRANCH A, with a stated basis. A terminal target structure above an observed weight is ordinary and defensible for a company expected to normalise leverage, and Branch B move |

## Count reconciliation

**45 findings raised, 45 answered, 0 unaddressed.** No row is grouped, batched or left parked:
this register carries no `unproven-go-research` bucket, because the three rows the audit itself
logged UNVERIFIABLE (F-12, F-21, F-38) were each resolved here against a primary record or an
internal coherence test rather than deferred.

*Nothing has been implemented; awaiting approval.*
