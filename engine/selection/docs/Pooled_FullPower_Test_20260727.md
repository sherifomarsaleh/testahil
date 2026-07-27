# SELECTION ENGINE — POOLED EG+AE+SA PRE-REGISTERED TEST (FULL POWER)

**Status: BINDING full-power run of the SIGNED pre-registration**
(`Selection_Engine_PreRegistration_v1`, §11 signed 27-Jul-2026), executed the same day
the long AE/SA exports landed and gated clean. This is the run pre-declared in
Sign-off Record item (g), reported side by side with the interim run
(`claude/Pooled_Interim_Test_20260727.md`) per the standing both-specs discipline.
Same scripts as the interim run — the only diff is the two data-path constants
(`RAW_BASE`, `OUT`); same seeds (H₀ 42, bootstrap 0, power 7); same B (30,000 / 5,000 /
8,000); critical values re-simulated at the new real dimensions.

**Headline: no factor is ADOPTED — and the full history reshuffled the candidates.**
F6 (52w-high proximity) is now the lead: it passes four of the five adoption rules,
including the Bonferroni *tercile-spread* threshold, and fails only the Bonferroni IC
bar — by 0.0040. F4 (low volatility), the interim favourite, weakened: the long SA
history flipped SA's sign against it and it now fails three rules. F1 (momentum)
flipped from wrong-signed to sign-correct as Gulf history extended, but sits below
even the single-factor bar. F3 got its first genuine three-market test. F2 is
wrong-signed again. F5 stays blocked.

---

## Data (all 59 series through Step 0.0, all PASS)

- **EG**: public repo `cd68546`, 15-yr library, 30 names (unchanged from EG pass).
  Gate notes 30; 15/30 volume-flagged.
- **AE**: 18-name long export, gated 27-Jul (`claude/AE_Export_Gate_20260727.md`) —
  ten names ≥15.5 yrs, perfect price identity vs the repo files on all 23,405 overlap
  dates. Gate notes 6 (benign stale-row drops); 6/18 volume-flagged, all pre-2021.
- **SA**: 11-name long export re-uploaded and verified **line-by-line identical** to
  the morning gate (`claude/SA_Export_Gate_20260727.md`); export-day (2026-07-27)
  rows dropped at staging per its recorded rule. Gate notes 3; 0/11 volume-flagged.

## Dimensions (real, re-simulated)

- Reference calendars: EG 3,744 sessions (2011-01-02 → 2026-07-22, quorum ≥15/30);
  AE 3,754 (2011-01-02 → 2026-07-24, ≥9/18); SA 3,881 (2011-01-01 → 2026-07-26, ≥6/11).
- EG master grid unchanged: **58 anchors** (2012-03-25 → 2026-04-20), **41** for F3.
- AE and SA anchors mappable **and** forward-resolvable at **58 of 58** EG anchors
  (own-calendar anchor steps: AE 47–69 sessions, SA 57–66). AE blocks enter all 58
  cohorts (**40 of 41** for F3); SA all 58 (**41 of 41** for F3). Interim was 17
  (21 for F2, 1 for F3) each.
- Pooled cohort sizes: min 31 / median 45 / max 59 names (252d factors); F3 24/41/48.
  The thin early cohorts are why simulated critical values sit above naive
  59-name arithmetic, same lesson as the interim run.

## Verification chain (before trusting anything)

1. The three EG scripts, unmodified, reproduce the 27-Jul exploratory pass **exactly**
   in this environment (all six mean ICs, spreads, critical values, jackknife flip
   lists).
2. The pooled scripts on the repo's 5.5-yr AE/SA reproduce the recorded interim run
   **exactly** — every pooled IC, critical value, per-market mean, jackknife flip
   (EG:KABO on F1; EG:COMI/EG:LCSW on F5), boundary note and power figure.
3. Estimator-mirror asserts (vectorised H₀ path ≡ stored per-cohort Spearman) pass at
   <1e-9 on ten cohorts per factor.
4. The full-power per-market EG means equal the EG pass values exactly — the pooled
   estimator reduces to the EG estimator on the EG blocks by construction.
5. **F6 threshold stability check** (its rule-2 margin is thin): re-simulated at
   100,000 reps with a fresh seed (123): Bonferroni IC threshold +0.0500 (30k: +0.0499)
   — rule-1 **fail stands**; Bonferroni spread threshold +0.1184 (30k: +0.1187) vs
   empirical +0.1190 — rule-2 **pass stands**, margin +0.0005, recorded as
   threshold-noise-marginal at 30k but stable at 100k.

## Results — pooled, full power vs interim (seeds 42/0/7; B=30,000 / 8,000)

| Factor | Cohorts (AE/SA in) | Pooled IC | *(interim)* | Spread (z) | *(interim)* | Crit single | Crit Bonf | Verdict | *(interim)* |
|---|---|---|---|---|---|---|---|---|---|
| F1 Momentum (+) | 58 (58/58) | **+0.0318** | *(−0.0095)* | +0.0738 | *(+0.0176)* | +0.0346 | +0.0499 | **not detected** | *(WRONG SIGN)* |
| F2 ST reversal (−) | 58 (58/58) | **+0.0137** | *(+0.0196)* | +0.0491 | *(+0.0442)* | −0.0337 | −0.0490 | **WRONG SIGN** | *(WRONG SIGN)* |
| F3 LT reversal (−) | 41 (40/41) | −0.0249 | *(−0.0202)* | −0.0255 | *(+0.0001)* | −0.0429 | −0.0619 | not detected | *(not detected)* |
| F4 Low volatility (+) | 58 (58/58) | +0.0332 | *(+0.0547)* | +0.0312 | *(+0.0722)* | +0.0359 | +0.0509 | **not detected** | *(single-only)* |
| F5 Amihud (+) | 58 (58/58) | +0.0104 | *(−0.0086)* | +0.0633 | *(+0.0440)* | +0.0346 | +0.0503 | **BLOCKED (volume DQ)** | *(BLOCKED)* |
| F6 52w-high (+) | 58 (58/58) | **+0.0460** | *(+0.0454)* | **+0.1190** | *(+0.0975)* | +0.0346 | +0.0499 | **single-only** | *(single-only)* |

Per-market mean within-market ICs, full power *(interim)*:

| Factor | EG 58/41 | AE 58 (F3 40) | SA 58 (F3 41) | Markets w/ expected sign |
|---|---|---|---|---|
| F1 (+) | −0.0349 | +0.1335 *(+0.2502 on 17)* | +0.0672 *(+0.0345 on 17)* | **2/3** |
| F2 (−) | +0.0053 | +0.0519 | −0.0130 | 1/3 |
| F3 (−) | −0.0187 | **−0.0710** *(1 cohort at interim)* | +0.0215 *(1 cohort)* | **2/3** |
| F4 (+) | +0.0481 | +0.0534 *(+0.1187)* | **−0.0231** *(+0.0371)* | **2/3** *(was 3/3)* |
| F5 (+) | +0.0014 | +0.0196 | +0.0196 *(−0.0863)* | 3/3 — blocked |
| F6 (+) | +0.0303 | +0.1224 *(+0.2230)* | −0.0024 *(+0.0055)* | **2/3** |

§6 five-part checklist (1 IC>Bonf · 2 spread>Bonf · 3 ≥2/3 markets · 4 jackknife · 5 ≤25% share):

- **F6: ✗ ✓ ✓ ✓ ✓ — one rule short of adoption.** Misses the Bonferroni IC bar by
  0.0040 (+0.0460 vs +0.0499); **clears the Bonferroni spread threshold** (+0.1190 vs
  +0.1187; margin stable at 100k reps); 2/3 markets (SA −0.0024, essentially zero);
  jackknife range +0.0378…+0.0550, no flips; max cohort share 0.18 (interim's 0.24
  watch item eased). Block bootstrap 90% CI excludes zero at **all three** block sizes
  (b2[+0.0105,+0.0791] b3[+0.0157,+0.0794] b4[+0.0186,+0.0767]) — at interim only b4 did.
- **F1: ✗ ✗ ✓ ✓ ✓** — below even the single bar, but block-boot excludes zero at all
  three block sizes (b2[+0.0036,+0.0644] b3[+0.0090,+0.0652] b4[+0.0081,+0.0621]);
  jackknife +0.0198…+0.0380, no flips (interim's EG:KABO fragility is gone — the mean
  no longer sits on zero).
- **F4: ✗ ✗ ✓ ✓ ✗** — max cohort share **0.26 breaches the 25% cap**; SA sign flipped
  against it; jackknife +0.0223…+0.0393, no flips.
- F3: ✗ ✗ ✓ ✓ ✗ (max share 0.41 — small-mean caveat: share is unstable when the mean
  is far from the bar); jackknife −0.0345…−0.0112, robust.
- F5: blocked; jackknife flips on SA:SABIC (to −0.0000); 3/3 signs are noted and
  inadmissible until the forensic pass.
- F2: ✗ ✗ ✗ ✓ ✗.

## Power at full dimensions (Bonferroni bar, pre-registered direction)

| True Spearman IC | F1 | F2 | F3 | F4 | F5 | F6 |
|---|---|---|---|---|---|---|
| 0.03 | 15% | 16% | 9% | 14% | 15% | 15% |
| 0.05 | 44% | 46% | 28% | 41% | 43% | 45% |
| 0.08 | 88% | 90% | 68% | 87% | 88% | 88% |
| 0.10 | 98% | 99% | 88% | 98% | 98% | 98% |

Up from 25–32% (ρ=0.05, 252d factors) at interim, still below the pre-reg §7
illustrative 67% — that table assumed ~62 uniformly full-size cohorts; the real panel's
early cohorts run thin (pooled minimum 31 names). **The cross-market expansion is now
exhausted: further power comes only from time** (each ~60 EG sessions adds one cohort)
or from adding markets, which would be a §10 amendment.

## Reading this, per §7

**F6 is the lead candidate and the record should say exactly how close it came:** it
cleared the single bar pooled, cleared the Bonferroni spread threshold, agreed in sign
in EG and AE, survived all 59 drop-one-name jackknifes, spread its mean across cohorts,
and its bootstrap CI excludes zero at every block size. It failed the one bar that
adoption hangs on, by 0.0040. Under the signed rule that is **`single-only — NOT
DETECTED at the Bonferroni bar at 45% power against a true IC of 0.05`**, not an
adoption, and not a near-adoption to be rounded up later. The standing caveat applies:
under a global null the chance that at least one of six factors clears its single bar
is ~26%; what distinguishes F6 from a lucky draw is the *convergence* of independent
checks, and none of that convergence substitutes for rule 1.

**F4's interim case was a regime artifact, partially.** The interim run strengthened
F4 on 17 recent AE/SA cohorts (post-2021 — the low-vol-friendly regime); the full
15-yr SA history flips SA to −0.0231 and drags the pooled mean to +0.0332, below the
single bar, with rule 5 now breached (0.26). EG remains F4's best market (+0.0481,
unchanged — same data). `NOT DETECTED at this power`, demoted from lead, not discarded.

**F1 momentum is the sharpest lesson of the day.** Interim (Gulf = 17 recent cohorts):
pooled wrong-signed, recorded as a hypothesis failure. Full power (Gulf = 58 cohorts):
pooled +0.0318, sign-correct, bootstrap-stable at all block sizes, yet below the single
bar. Both records stand as written at their own dimensions. The EG-vs-Gulf split is
now measured on equal footing: EG −0.0349 / AE +0.1335 / SA +0.0672 over 15 years.
Egypt is momentum-negative; the Gulf is momentum-positive. Any action on that split —
per-market signs, market-specific factors — is a **§10 amendment discussion**,
explicitly not exercised here.

**F3 finally had its test** — the one the 15-yr exports existed for. Pooled −0.0249
right-signed; AE agrees over 40 cohorts (−0.0710); SA disagrees (+0.0215). At 28%
power against a true IC of 0.05: `NOT DETECTED at this power`. F3's grid also grows
fastest with time (41 → more as the calendar extends past the 1260d burn-in).

**F2 short-term reversal is now 0-for-3** (exploratory, interim, full power — wrong
sign or zero every time, 1/3 markets here). Egypt's `rev_1m` prior was already
refuted; nothing in the Gulf rescues the contrarian sign. It stays in the six —
removing it now would be the result-driven amendment §10 prohibits — but it is the
obvious candidate if a seventh factor ever forces a §10 swap.

**F5 stays BLOCKED and earns a footnote:** +0.0104 pooled with 3/3 sign agreement is
the most sign-consistent reading F5 has produced, and it is inadmissible — the number
means nothing until the volume forensic pass, and the jackknife's SA:SABIC flip (to
−0.0000) shows how little is holding it up. The forensic queue is now: EG first
(EFID 176 jump-days, JUFO 129, GBCO 91, ABUK 52, LCSW 49), then AE pre-2021 (AGTHIA 64,
ENBD 38, IHC 35, ADCB 13, FAB 11, ADIB 7). SA volume is near-pristine (≤2 jump-days).

**Survivorship bias applies to every number above** (§8): currently-covered names
only, in all three markets, and the long Gulf histories inherit it in full.

## What this run does NOT do

- Does not adopt any factor (F6 fails rule 1; every other factor fails more).
- Does not change the factor list, signs, thresholds, or cohort construction.
- Does not retire the interim run — it stands on record; this run supersedes its
  *power*, not its honesty.
- Does not touch `market_profiles.py`, the MC engine, ticker pages, or the live site.

## Next steps (proposals — none binding until Sherif signs off)

1. **F5 volume forensic pass**, EG queue first, AE pre-2021 queue second. F5 is the
   only factor whose verdict can change without new data.
2. **Standing re-run trigger (proposed):** re-run this exact pipeline when the EG
   calendar has added 4 new resolved cohorts (~1 year) **or** when F5 unblocks,
   whichever comes first. More data on a frozen spec needs no §10; adopting the
   *trigger* itself should be recorded.
3. **Commit the long AE/SA libraries + the pooled scripts to the public repo** —
   reproduction of this run currently depends on the staged exports documented in the
   two gate docs; the repo still carries 5.5-yr AE/SA.
4. The **EG-vs-Gulf momentum split**: park it as a recorded observation; any
   exploitation is §10.
5. **Shadow Cohort #1 grading trigger** (pre-reg §9): still cancelled, still cheap to
   reverse, first maturity mid-Oct-2026.

## Reproduction

Same three pooled scripts as the interim run (`claude/build_cohorts_pooled.py`,
`claude/factors_pooled.py`, `claude/significance_pooled.py`) with only `RAW_BASE`
(→ staged long AE/SA + repo EG) and `OUT` changed; Python 3 + numpy/pandas/scipy;
engine imports (`data_quality.clean_ohlc`, `mc_v2.yz_variance_proxy`) at `cd68546`.
Seeds 42/0/7; B_H₀=30,000, B_boot=5,000, B_power=8,000; F6 stability check at
B=100,000, seed 123. Data provenance: EG = repo `cd68546`; AE/SA = 27-Jul long
exports per the two gate docs (AE files end 2026-07-24 complete; SA staged with
2026-07-27 export-day rows dropped, last complete session 2026-07-26).
