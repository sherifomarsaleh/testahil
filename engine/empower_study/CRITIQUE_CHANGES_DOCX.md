# Word-document change list — critique implementation, 17-Aug-2026
(Instructions for the docx builder update. Every number comes from the UPDATED
study_numbers.json; this file lists the TEXT/structure changes. The external
facts cited here are verified in critique_facts.json.)

## Macro / war (Headline, §1.8, §5, §7, catalysts) — the biggest text change
The old framing ("a ceasefire has held — fraying — since 8 April"; bear = "war
re-escalation") was stale at publication. Verified timeline: Iran struck
Fujairah 4-May-2026; Hormuz clashes 4-7 May; the US declared the ceasefire
"over" on 8-Jul; the Strait of Hormuz was CLOSED from 11-Jul (US blockade
14-Jul) and remained closed at the 7-Aug anchor; an ADNOC tanker was attacked
at sea on 8-Aug; no strikes on UAE soil after 8-Jul. As of this revision
(17-Aug): ADNOC vessels hit 12 & 14 Aug, an Iran-Oman reopening agreement was
announced 17-Aug and the ceasefire formally ended 17-Aug.
REWRITE: (1) Headline/overview states the conflict facts as of the anchor
plainly (strait closed, ceasefire declared over a month earlier, tanker attack
the day after the anchor); (2) the base case is relabelled "de-escalation case"
and its condition stated honestly: it requires a de-escalation that HAD NOT
occurred at the anchor date — the bear ("continuation") case describes the
world as it stood on the published facts; (3) §5 catalysts: watch tempo of
attacks on shipping/UAE soil and the Iran-Oman reopening track, not "truce
durability"; (4) a dated postscript box "As of this 17-Aug revision" with the
newest facts. Do NOT re-weight the lenses by fiat — the field (bear 1.558 /
central 1.959-1.836 / bull 2.351) plus this honest labelling is the deliverable.
Also add CBUAE's own 2027 rebound forecast (9.8%, "temporary moderation",
June-2026 QER) wherever the 1.7% cut is cited — cite both legs.

## Regulation (§overview Table 4, §1.8, §5, §7, B.2)
- Tariff approval: RSB assesses and RECOMMENDS; the Dubai Supreme Council of
  Energy APPROVES (RD10 under ECR 6/2021; ECR 87/2025 fines unapproved
  tariffs). Fix everywhere RSB is named as the approver; §5 watch-item points
  to DSCE/SCE decisions with RSB consultations as the leading indicator.
- Add RD10 v1.3 (17-Sep-2025; v1.4 Feb-2026): explicit tariff caps
  (0.643 AED/TRh consumption-with-capacity incl. fuel surcharge; 0.075 fuel
  surcharge; AED 30/mo billing fee; 120% excess-demand fee) and the verbatim
  rule that "indexation or escalation of Capacity Charges will not be
  approved". Present it as BOTH: (a) it hardens the model's flat-nominal-tariff
  assumption from a conservative choice into a regulatory constraint, and (b)
  it removes any tariff-escalation upside — terminal growth must be volume-only.
- ECR 87/2025 (18-Nov-2025): AED 1.55/RT/annum service fee — ~AED 2.7m/yr on
  the connected base, ~0.005/share capitalised, stated and expensed in words
  (immaterial, with the number), plus the AED 100k fine schedule as enforcement
  evidence.

## Terminal growth (§1.9, Assumptions discussion)
Drop the label "long-run UAE nominal-GDP-consistent" (UAE nominal GDP CAGR
2024-29 ≈ 5.7%; 2.5% is roughly half of it — the label was wrong in the
conservative direction). Re-justify 2.5% as a VOLUME-ONLY perpetual growth
bound under the RD10 no-indexation regime: Dubai 2040 build-out, the contracted
backlog and the 163-186 new contracts/yr signing run-rate — and state the
tension honestly (2.5% volume growth forever doubles the connected base in ~28
years; the grid now extends to 0% so the reader sees the flat-everything end:
g=0 ≈ 1.68/share on the primary lens).

## Cost of capital (§1.8)
- The rf paragraph: the Jan-2031 T-Bond (4.50-year tenor — fix "4.4", which was
  the auction's bid-to-cover) is the most RECENT AED sovereign print (30-Jul
  tap), not the longest: a Feb-2033 T-Sukuk exists (first 7-yr AED tranche,
  AED 1,650m, ISIN AED01889C262) whose last print was 4.13% in the April tap —
  pre-escalation and stale in a repriced market, which is why the on-the-run
  4.48% remains the anchor; both stated.
- Kd: relabel "the company's own disclosed all-in borrowing cost (the IAS 23
  capitalisation rate on general borrowings — an average, not a marginal
  print)" and keep it as the anchor because it is the top of the
  EIBOR-plus-implied-margin band. EIBOR: "3M EIBOR ~3.9% in August 2026
  (3.66% at end-March)" — fix the stale figure. REFINANCING: only ONE AED
  2.75bn tranche was extended (to Feb-2028); the other still matures Sep-2027
  (H1-2026 borrowings note) — fix every "both facilities refinanced" claim and
  add the Kd sensitivity sentence: the Sep-2027 roll reprices half the book at
  then-current EIBOR + market margin.
- The 15% framing keeps the 9% interest shield (Pillar-Two top-up is a
  minimum-ETR charge, not a higher statutory rate) — both framings discount at
  7.61%; state it.
- ADD a "WACC constructions — all priced" table: base target-net 7.61% (company
  net-debt policy ~2x EBITDA; payout ≈ FCFE so surplus cash is transient),
  gross-weights 7.23% → DCF 2.507, negative-carry net 7.79% → 2.227, and the
  DFM-index beta 6.77% → 2.792 (the index basis is an explicit client
  instruction; the listing-venue regression 0.652 is priced in full, not
  parenthetical). State that the published field is bounded by scenarios while
  these CONSTRUCTIONS span 2.23-2.79 — wider than the scenario field — and the
  beta's own 90% interval spans roughly 1.8-3.0 on the primary lens; a reader
  should treat the printed field as scenario risk, and construction risk as
  additional and larger.

## Clean receivable treatment (§1.1, bridge, §1.6, A.2)
- The "airport-concession receivable" is renamed: related-party acquisition
  receivables (Note 8: AED 1,005.0m Dubai Aviation City re DXB CoolCo 2023 +
  AED 289.4m Nakheel re Empower Snow 2021 = 1,294.4m at 30-Jun-2026).
- New treatment stated: interest excluded from operating EBITDA/FCFF; asset
  added at BOOK in the bridge (new bridge row); excluded from terminal
  invested capital. FY2025 identity: operating EBITDA ex interest 1,583.9 +
  interest 58.3 = audited-derived 1,642.2.
- A.2 row must show the FULL carrying value in all four columns (1,343.9 FY23 /
  1,324.8 FY24 / 1,304.8 FY25 / 1,294.4 Jun-26 — non-current + current summed);
  the old row printed the current portion in three columns.

## Valuation clock (§1.1, bridge caption, A.3)
Bridge and cash-flow clock now BOTH sit at 30-Jun-2026: FY2026 contributes its
second half only (stub at t=0.5), year-ends at 1.5-4.5, TV at 4.5. Replace the
"no accretion roll" caption with the stub-convention statement and note the old
convention double-counted H1-2026 cash (~AED 200m).

## Company facts
- DXB CoolCo: 85%-owned (H1-2026 subsidiary note "85% 85%"), minorities 15% —
  fix "70%/30%" everywhere; the NCI charge (profit share) is unchanged.
- Listing date: 15 November 2022 (Dubai Media Office), not 16.
- H1-2026 results: statements dated 5-Aug, released/covered 6-Aug — say
  "released 5-6 August"; the share fall ran 4→7 Aug (1.60→1.50).
- "Roughly 80% of Dubai's market" — date-stamp as the company's 2022
  IPO-era disclosure, not restated since.
- H1-2026 profit lines ADDED wherever H1 is cited: PBT 514.0m (+16.2%), net
  profit 468m (+16.2%), EBITDA 773m (+7.5%) — the shock half produced record
  profits, which SUPPORTS the pass-through crux; also state the FY2026E build
  implies H2 EBITDA roughly flat y/y (conservative vs the H1 run-rate).
- Margin narrative (§1.6): the margin RISES in the shock year (48.6%, the
  highest forecast year) because the lost revenue is mostly pass-through cost;
  the dip is FY2027 — fix the backwards sentence. Margin band since 2021: keep
  47.6-50.5% but add the basis note "derived as audited operating profit plus
  depreciation and amortisation (FY2021 50.5%); the company's own reported
  EBITDA figures differ slightly in definition".
- §1.1 "of which" rows: add the pipes line so the disaggregation foots.
- Bull case description: connections 110/110/100/90/80k RT (the actual path).
- Consumption shock attribution: hospitality-occupancy-led (~80% per company
  attribution), weather minor — align any wording.
- Mix reconciliation sentence (§1.6): the auditor-KAM basis puts FY2025
  consumption at 56.3% of revenue vs the deck's H1 49% — H2 carries the summer
  peak; the pass-through ratio (76.3%) is computed on the KAM basis.
- Appendix C.2 FCFE coverage table: use the model's own forecast finance line
  (167.6, coverage 1.01x in FY26), not the FY2025 actual 154.1.
- A.3 note: "GROSS borrowings held flat; NET debt falls as retained cash
  builds" + both rolls from 30-Jun-2026.
- Relative lens (§1.3): peers restruck at the anchor (Tabreed 2.46 on
  6/7-Aug: 10.1x EV/EBITDA, 15.0x P/E; was 10.7x/16.6x on 22-Jun marks) —
  trailing multiple on trailing operating EBITDA, like-for-like; Tabreed
  revenue 2,456. Fix any "discount to Tabreed on EV/EBITDA" claim (it is a
  premium on EV/EBITDA; the discount is on P/E).
- Normalised lens: forward justified P/E (no (1+g)); both tax framings.
- Book lens: both tax framings (ROE re-taxed under 15%).
- §3/§6 cone-vs-centrals: make the comparison COMPUTED, never asserted — with
  the new centrals (1.959/1.836) vs the 3M p95 (1.92): 1.959 sits just ABOVE,
  1.836 BELOW — write conditional text generated from the numbers.
- §3 calibration language: downgrade to the workbook's own wording — the
  record is 10 windows, too short to establish skill either way; 10-of-10
  inside the 80% band is itself evidence of over-width; keep the plain-language
  statistics, drop "calibrated rather than assumed" absolutism.
- "No price target" disclosure: keep the no-target/no-rating statement but
  drop absolutism: centrals printed to 2dp in the summary, the field labelled
  scenario range, and the construction range (2.23-2.79 on the primary lens)
  plus beta-interval width stated beside it.
- READ FIRST: add "Revised 17-Aug-2026 following an external audit; the
  changes and their prices are catalogued in the accompanying critique-response
  note", and update the conventions (stub clock, operating-EBITDA definition,
  receivable at book).
- Research register (B.3): add RSB RD10 v1.3/v1.4 + ECR 87/2025 rows (primary,
  dated), the MoF outstanding-securities table (2033 sukuk), and re-date the
  index rows.
- Bibliography document: update the affected input rows (receivable, tenor
  wording, EIBOR, peer marks, refinancing scope, DXB 85%, listing date), the
  judgements table (valuation clock; receivable treatment; WACC construction
  now dual-framed; g relabelled), and the discrepancy table (add: study's own
  first edition vs audit — ceasefire status, RD10 instruments missed).
