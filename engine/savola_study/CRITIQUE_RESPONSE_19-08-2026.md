# SAVOLA — critique response and second edition (19-Aug-2026)

Four external critiques of the 18-Aug-2026 first edition were worked under
`engine/Critique_Response_Prompt.md` v2: a self-audit first (recorded before reading three of
the four documents; the fourth was auto-loaded on attachment and that anchoring is disclosed),
then a one-row-per-finding ledger, every finding priced through the study's own `compute.py`
before any verdict, premise split from conclusion, rejections with receipts, and findings above
5% of the central re-derived from primary sources. **82 findings raised (Claude Cowork 37,
Claude Code 19, Gemini research 16, Gemini think 10), 82 answered, 0 unaddressed.** The full
row-by-row ledger was delivered in the session record; this file is the permanent summary and
the implementation proof. The pricing harness (`price_findings.py` / `price_runs.py`, pinned to
the first edition at commit c0ba9bb8) reproduces the delivered base to ten decimals and carries
every priced run.

## The verdict that survived verification

All four critiques' arithmetic reproductions of the study agreed with the study — the machinery
was sound; the failures sat in one FCFF convention, the input layer, the lens bases and the
Expert 3 appendix. The second edition corrects them **through the model**: the weighted central
moves **SAR 28.02 → SAR 27.24 (−2.8%)** against the **settled SAR 25.40** close (**+7.3%**,
from the first edition's claimed +11% against a stale 25.30 print).

## Findings accepted and implemented (master list, priced at the first edition's central 28.0166)

| Finding | Price | Receipt | Fix |
|---|---|---|---|
| FCFF charged lease renewals only while the lease book grew 3,952→4,808 (Cowork #3; **the largest accepted finding**) | **−2.47 DCF / −1.11 central (−3.97%)** — reproduced exactly | The study's own balance-sheet walk: additions 756–787/yr vs the 559–647 charged; the growth rode free while only the opening liability was deducted | FCFF charges the FULL additions in every framing and scenario; the lease walk is single-sourced |
| Terminal ROIC 10.5% input above every year the model produces (Cowork #12 = CC-implied; GR/GT warnings) | −0.44 (−1.58%) at their 9.66% | Model's own ROIC path 9.2→9.7% on the first edition's capital base | Terminal return **COMPUTED** (year-5 NOPAT / opening capital = 10.07% on the consistently carved base); 10.5% retired to a labelled variant (SAR 25.49) |
| Tiryaki 274.6 receivable ON the 31-Dec-2025 balance sheet, excluded on a wrong rationale (CC #2; **escalated, re-derived**) | +0.44 central (+1.57%) bridge; ≈+1.0 with the WC ratio | FY2025 FS notes 14/22 verbatim; Q2-2026 interims show the share settlement | Bridge asset + WC ratio ex-receivable (4.11%) + balance-sheet reclass to investments (the critic's fix as stated would have booked a phantom 274.6 release — repaired) |
| Book lens on a "+15% first-half-evidenced" base its own engine contradicted at +35% (CC #3) | +0.69 (+2.47%) | Engine FY2026E recurring 729.8 vs 539.1×1.15 | One FY2026 base across lenses; book on 30-Jun-2026 reviewed equity |
| Trailing peer multiple on forward EPS (Cowork #22) | −0.89 (−3.19%) rel; −0.36 norm | Double-counts the peers' growth | Relative rebuilt trailing-on-trailing (TTM recurring 645.1, all three legs company-disclosed); normalized moved to FY2026E; forward variant published |
| Spot 25.30 was an intraday print; settled close 25.40 (Cowork #1, GT; also self-audit — third occurrence of the house settled-print class) | comparison basis +11%→+10.3%; model −0.02% | Argaam prior-close on 19-Aug; O/H/L/vol reconciled across three feeds | Library row corrected; cone restruck (seed 42); technical read recomputed; every peer quote settled-verified (Herfy 15.50 confirmed, GT's 15.66 rejected) |
| Al Othaim 19.4x was a pre-announcement window (Cowork #2) | +0.075 (+0.27%) | 11-Aug-2026 H1 loss 53.5mn → TTM ~79mn → ~57x | n/m, like Herfy; retail leg = BinDawood at the settled 20.20 |
| rf construction mixed a market spread with a rating spread (Cowork #18 premise; their rf*=4.68% fix rejected) | adopted fix +0.15 (+0.54%); their fix would have been +0.95 | FTSE SAGBI factsheet 31-Jul-2026: 7-10y **5.52%** — the published curve sits 84bp above their proposal and 1bp below the study's proxy | rf OBSERVED on the published curve; July-2026 Damodaran rating legs (0.48/4.94); CDS legs Jan-flagged; iBoxx corroboration cited (Cowork #19) |
| WACC weights mixed an 18-Aug numerator with 31-Dec debt (Cowork #25, CC #15) | +0.11 (+0.40%) | 30-Jun-2026 reviewed interims: loans 2,664.5, leases 3,716.8 | Freshest observable per leg, labelled |
| Per-share divisor (Cowork #13 premise; their 300mn fix improved on) | +0.19 (+0.66%) | Q2-2026 EPS note: weighted treasury 3,318,046 → **296.682mn** | Every per-share value on the company's own latest ex-treasury divisor |
| Mehbaj "no disclosure anywhere" was false (Cowork #9, CC #7) | −0.01 (deducted 11.4) | Q2-2026 interims note 19: SR 11.4mn (5.4+6.0) | Consideration consumed in bridge + nuts note; five study statements corrected; sourcing failure (unfetched filed interims) acknowledged in the register |
| Kinan/Herfy legs accreted though anchor-dated (Cowork #26 premise; their ±75mn price corrected to the net +9.2mn) | −0.03 DCF | (650−511)×6.47% | Three anchor-dated legs (Kinan, Herfy NCI, Mehbaj) held outside the roll, shown line-by-line |
| E3's bridge failed the accounting identity by ~648mn; its EP series detached from the model's capital; its "no-tail low" printed ABOVE base (Cowork #4/5/6, CC #1/12) | nil on central; panel median 19.82→21.96 | Mechanism found in code: double-deducted items already inside IC0, dropped Kinan, and `e3_lo` omitted `other_net_liab` — the cause neither critic reached | E3 rebuilt on the identity with a build-time reconciliation assert; lo < base < hi asserted |
| E1 deducted 100% consolidated liabilities against a 49%-at-market Herfy leg (CC #11, GT half-accepted) | E1 +2.6 (appendix only) | Note 20: Herfy liabilities 728.9 | Carve-out from the audited aggregates, its two constructed splits flagged |
| Ke-sensitivities froze the Kinan leg (CC #4) | interval ends ±0.3–0.5 | Reproduced | Every Ke-dependent leg re-runs in every grid; grid base-row asserts added |
| Herfy margin 18.5 vs the disclosed 18.7 held flat (Cowork #14, CC #14a) | +0.05 | Q2 deck 18.7%; the 20bp haircut had no measured mechanism | 18.7 held flat |
| Mix weight 55% "the group's own EBITDA mix" wasn't (Cowork #24) | +0.08 | Model's own split 53.5/46.5 | Weight computed from the segment sheet |
| Pasta FY25 volume derived when disclosed (the residual of Cowork #7 after its rejection) | nil | Deck p17: 263k t | Rebased to the disclosed volume (derived 268 was within 2%) |
| sps −7.1% quoted as measured on an unpublished store count (Cowork #29); the 213 literal unregistered (self-audit) | −0.40/+0.02 band | June-2025 count in no reachable disclosure | Derivation published as a range (−7.1/−6.0); 213 a registered ASSUMPTION; build opens at −6% |
| Store path: run-rate variant demanded (Cowork #28 variant accepted; its "four-fold acceleration" premise unprovable either way) | variant −3.18 central at full severity (my engine; their −1.85 understated it) | H1 +4 vs guidance "20+"; FY25 delivered +18 net with an undisclosed half-split | Guidance base kept; +8/yr variant priced (SAR 19.53) with lease growth scaled to cadence; named the near watch |
| Framing B description vs computation; two "measured" figures (CC #5) | nil (their 23.42 verified) | −6% then −3% is what computes | Path stated exactly everywhere |
| Bear/bull levers unpublished (CC #16) | nil | Their reconstruction guessed a pasta cut that doesn't exist | Every lever value in print |
| Labels/narrative: Almarai 21.1bn-at-settlement vs 12.75bn dividend leg (CC #6 governs over Cowork #11's circular figure); zakat trio reconciled (Cowork #27, CC #8); pasta +3.1%; IS/CF row labels; loans relabelled currencies-constructed (Cowork #8); DDM crosswalk published (Cowork #23/CC #13: "not derivable" rejected — the two-stage construction computes 8.18x — "not published" accepted, Gordon 6.95x and E2-implied 7.73x beside it); MACD 3dp + §2 conventions (Cowork #30/35/36); beta pack + citations (Cowork #31/32/33); MC spec line (CC #17); FY23 citations (CC #18); nuts step-down stated with its H1 anchor (CC #19); margins-status disclosure — Herfy/Kabeer margin-pinned at the finest disclosed level (Cowork #15); FY25 GP footing row in the workbook (Cowork #16's ask; its "does not hold" recompute rejected — it mixed FY26 rates with FY25 volumes on swapped pasta roles) | each ≤0.5% or nil | per the session ledger | all implemented |

## Rejected, with receipts

| Claim | Receipt |
|---|---|
| Gemini think fatal #1: "lease double-count — remove the charge entirely"; corrected DCF 34.48, central 31.74 (**+13.8%, escalated and re-derived**) | Removing the charge leaves store occupancy in neither opex (post-IFRS16 EBITDA) nor capital charge — the estate becomes free forever while only the Dec-2025 lease stock is deducted. The real defect ran the OTHER way (under-charged growth). Premise right, conclusion inverted; their figure is the size of their own error |
| Gemini think fatal #4: Herfy NCI must be at book 434.6 | Book is a carrying value, not a claim measure; the 18-Aug market price of the listed minority is observable and MORE conservative here (their fix raises the valuation +0.44%). Mixed-basis disclosure added instead |
| Gemini think (half of fatal #2): E1 must carry the 20% holdco discount | E1's stated worldview is a straight segment SOTP; the conglomerate discount lives in the relative lens and the divergence table exists to isolate exactly that difference |
| Gemini think fatal #3 / self-audit item (d): investment property +158.2 is a double-count | **Accepted at step 8, REVERSED at implementation with a better receipt**: the audited segment note 33 shows the Investments segment's 28,978 revenue is INTER-SEGMENT only (external zero, eliminated); the model's group EBITDA excludes the property's income (the unalloc line is an independent HQ-cost estimate, not a residual), so the asset belongs in the bridge. The study text that miscalled it "revenue…noise" was fixed instead |
| Cowork #7: "disclosed pasta volume 445k t, GP/tonne 263" | Deck p17 layout: 232→263 under "Volume (MT '000)", 440→445 under "Gross Profit / Ton (SAR)"; 117.2/263=445 and 102/232=440 exactly; the Q2 deck's "+3.1%" volume growth matches 135→139k t and cannot cohere with a 527k-t H1 |
| Cowork #10: "no source carries the 11,554.7 Almarai gain" | Audited FY2024 statements, segment note: gain on distribution 11,554,662 (the critic's extraction stopped at p39) |
| Cowork #17: "no Investments segment exists" | Audited FY2025 segment note 33 lists it (28,978); the deck's five-segment view nets it into Others/Eliminations — their own footing (−443.2+29.0=−414.3) confirms |
| CC #10: "54.1 months holds at most 18 windows" | Fencepost: 19 origins = 18 three-month gaps; 54.07/3.0025 = 18.01 gaps; their own integer-consistency check (10/15/16 **of 19**) confirms n=19; origin list in `backtest_rows.csv` |
| Gemini research: spot 25.30 "validated as a highly accurate closing mark"; lease mechanics "flawless"; WACC "hybrid tax shielding, highly accurate"; "zero critical failures"; "affirmed at 28.00" | Settled close 25.40; the lease under-charge was −4.0% of central; the code applies the FULL 19.5% shield on both legs (their own sibling reproduced 7.9668% exactly on that basis — the "hybrid mechanic" rationalized their arithmetic slop); five proven defects; corrected central 27.24. A mirror-image calibration failure to Gemini think's: one document invented defects, the other cleared them |
| Gemini think: Herfy 15.66 | Argaam prior-close 19-Aug: Herfy settled 15.50 on 18-Aug (15.39 intraday 19-Aug) |

## What the rebuild's own gates surfaced (step-9 disclosure)

1. **The GT-4/invprop reversal above** — a finding this response had ACCEPTED at step 8 was
   overturned during implementation by the audited segment note; the honest price of the
   reversal (+0.25 central vs the step-8 candidate) is inside the final 27.24.
2. **CC #2's fix as stated books a phantom working-capital release**: re-basing the prepay
   ratio without re-basing opening NWC releases the 274.6 into year-1 cash. The balance-sheet
   foot assert caught it at exactly −274.619; the receivable is reclassified to investments.
3. **The final computed terminal return is 10.07%, not the 9.66–9.75% quoted at step 8**: with
   the Tiryaki receivable and the investment property carved out of operating invested capital
   (their income is outside NOPAT), the base is smaller and the return correspondingly higher —
   the definition is now consistent on both sides of the ratio. The 10.5% variant sits 43bp above.
4. **Framing B and the bear now carry per-scenario computed terminal returns**, so both fell
   further than a naive restatement would suggest (B 22.10→19.63; bear 15.02→10.75): a world of
   permanent density erosion is a world of structurally lower returns on capital. Stated in the
   study rather than smoothed.
5. **The first edition's technical read had no committed producer** — `tech_run.py` now
   regenerates `tech_read.json` from the library through `engine/technicals.py`.
6. **Terminal-value share rose to 79%** (from 76%) because the corrected lease charge back-loads
   the explicit years — the duration-risk warning all four critiques carried got STRONGER, and
   the study now says so in three places.
7. Four rendered-page defects were caught and fixed in-pass at the reading gate (an unfixed
   overview sentence, a bridge subtotal whose label mentioned a roll the value didn't show, a
   flat −7.1% claim in the crux, an unnarrated SMA-100 line in the price chart), plus three
   clipped workbook labels.

## Before → after (all gates re-run on the delivered files)

| | First edition (18-Aug) | Second edition (19-Aug) |
|---|---|---|
| Weighted central | 28.02 (+11% vs 25.30 print) | **27.24 (+7.3% vs settled 25.40)** |
| DCF / Relative / Normalised / Book | 26.20 / 30.90 / 36.39 / 20.27 | 24.99 / 28.22 / 35.12 / 24.49 |
| WACC explicit → terminal | 7.97% → 8.46% | 7.82% → 8.42% (SAGBI rf; July Damodaran; 30-Jun weights) |
| Terminal ROIC / TV share | 10.5% input / 76% | **10.07% computed** (10.5% variant = 25.49) / 79% |
| Framing A / B | 26.20 / 22.10 | 24.99 / 19.63 (per-scenario computed terminals) |
| DCF bear / bull | 15.02 / 32.29 | 10.75 / 32.59 (mechanism disclosed) |
| Judgement variants | — | stores run-rate 19.53 · sps −7.1/−6.0 24.34/25.01 · CDS 23.27 |
| Experts (E1/E2/E3 → median) | 34.79 / 18.22 / 19.82 → 19.82 (E3 irreproducible) | 37.44 / 18.52 / 21.96 → 21.96 (**E3 identity-asserted**) |
| Per-share divisor | 298.589 FY25 weighted | 296.682 ex-treasury (Q2-2026 EPS note) |
| Workbook | 786 formulas; terminal an input; Othaim in; forward-EPS relative | **802 formulas, 802/802 recalc agreements; live computed terminal; 49 driver direction-tests** |
| Cone (settled spot) | struck on 25.30 | restruck on 25.40: 1M p50 25.47 · 3M p50 25.68 (seed 42) |
| Study | 18pp | 21pp with the revision note and every derivation published |

Deliverables rebuilt end-to-end and read as rendered pages: study PDF 21pp (every page
inspected), model PDF 23pp landscape with 802 baked values, bibliography 15pp (196-input
register). Every rerun artifact (`step0`, `backtest_5y`, `strike`, `tech_read` via the new
`tech_run.py`) and the pricing harness are committed alongside.

Not published: no site page, ticker page or ledger cohort exists or was touched; publication
remains a separate, explicit request.
