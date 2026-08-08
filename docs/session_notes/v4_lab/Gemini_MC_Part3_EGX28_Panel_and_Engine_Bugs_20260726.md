# Gemini MC proposal — PART 3: Ali Nabil's 28-series Egyptian panel (26-Jul-2026)

Parts 1 and 2: `Gemini_ACI_HARQ_SkewT_REJECTED_20260726.md`,
`Gemini_MC_Part2_Repaired_Retested_20260726.md`.

Tested on the requested set: **26 EGX stocks + EGX30 + EGX70 EWI**, history extended
to Jan-2011 (vs the library's ~2021), **1,293 non-overlapping 60-day windows**, 2012–2026.
Series: ABUK ADIB BTFH CCAP CLHO DSCW EFID EFIH EGAL EGX30 EGX70 EMFD ETEL FWRY GBCO
HELI HRHO ISPH JUFO LCSW OCDI ORAS ORHD ORWE PHDC RAYA RMDA TMGH.
Four files named in the first batch never arrived (PRDC, KABO, COMI, OIH) — not tested.

---

## THE HEADLINE: three defects found in OUR OWN engine, not the proposal's

The extended history reached back past 2021 for the first time, and it broke things
that the short library had never exercised. **These are production findings and they
matter more than the Gemini verdict.**

### FINDING 1 — `data_quality.py` corrupts series containing a zero close (HARD BUG)

The vendor writes `Price = 0.00` on some sessions with valid Open/High/Low (a
missing-close artifact). `clean_ohlc` does `np.log(0) = -inf`, reads it as an infinite
one-day move, and computes `factor = p[i+1]/p[i] = inf` (or `0.0`) — then multiplies
**every prior row** by that factor. These rows survive the placeholder filter because
they carry real volume and a real High≠Low range.

Measured: **17 such rows across 6 of 28 series** (ABUK 13, CCAP, HRHO, OCDI, ORWE, LCSW,
TMGH — 2011–2013). On OCDI it rescales 536 rows of history to zero. Five series came out
of the current gate with non-finite or non-positive prices.

### FINDING 2 — spike-and-revert bad prints mis-repaired as corporate actions

A one-session bad print is not a corporate action; a corporate action is one-way and
permanent. The iterative back-adjust treats each leg separately and applies two
rescalings that do **not** cancel:

| name | date | sequence | back-adjust | net distortion on prior rows |
|---|---|---|---|---|
| BTFH | 2016-03 | 4.638 → **16.390** → 5.006 | ×3.5339 then ×0.3054 | **+7.9% on 952 rows** |
| BTFH | 2016-05 | 4.041 → **12.500** → 4.041 | ×3.0933 then ×0.2971 | **−8.1% on 989 rows** |
| HELI | 2012-02 | 0.330 → **12.080** → 0.340 | ×36.606 then ×0.0281 | **+2.9% on 228 rows** |
| DSCW | 2022-08 | 0.253 → **0.365** → 0.247 | (same pattern) | — |

and the bad print itself stays in the series.

**Both fixed** in `dq_patch.py` (proposed patch, not pushed): drop non-finite/non-positive
closes before the jump scan; guard against a non-finite back-adjust factor; and before
treating a breach as a corporate action, scan forward up to 5 sessions for a reversal —
if the move reverts, drop the bad-print block and rescale nothing. Conservative by
construction: it only ever removes rows the exchange could not have traded, and it
strictly reduces the number of back-adjustments. After the patch all 28 series pass at
max |log move| ≤ 0.241, comfortably inside the 0.290 EGX threshold, and only **two**
genuine corporate actions survive (EFIH 3:2 May-2025, OCDI Aug-2025).

### FINDING 3 — price-space CRPS is not a convergent estimator (AFFECTS THE LIVE GATE)

The engine draws `spot·exp(drift + z·mix·σ_h)` with `mix` from a Student-t. **A Student-t
has no moment generating function, so E[exp(σ·T)] is infinite for every σ>0.** The
lognormal-t terminal price has no finite mean, and sample CRPS in price space does not
converge — it is dominated by the largest of N draws and grows without bound in N.

Measured on **production's own `simulate_terminal_v3` at the live ν=4.0**: RAYA
2012-09-17 (spot EGP 0.090, σ_h = 1.15) drew a terminal price **1.35 × 10¹³ × spot** and
carried **99.45% of the entire panel's CRPS**. Panel skill printed as −2,009.

It stays invisible at the median σ_h ≈ 0.256 and only detonates on high-σ_h, low-priced
windows — which is precisely what extending EGX history to 2012 introduces. The
scale-normalization fix (crps/spot) does not touch this: it solved cross-name *price*
weighting, not the non-existence of the moment.

**Fix used here: score CRPS in log space** — finite for a t, scale-free by construction,
and already house precedent (the Round 8 shadow-cohort protocol grades "CRPS (log-space)").
Worst single-window share drops from **99.45% → 0.80%**. Every number below is log-space.

---

## Results

### A. Post-break sample (2022-03-21 on, protocol calibration window) — 461 windows

| arm | ν | cal | skill | 90% CI | verdict | cov90 | D |
|---|---|---|---|---|---|---|---|
| PROD YZ-HAR (production) | 4.0 | 1.007 | +0.0128 | [+0.0054,+0.0205] | PASS | 0.894 | PASS |
| **R2 YZ-HARQ log-space** | 4.0 | 1.000 | **+0.0136** | [+0.0062,+0.0213] | PASS | 0.889 | PASS |
| R4 PROD + online ACI width | 5.0 | 0.951 | +0.0118 | [+0.0048,+0.0189] | PASS | 0.898 | PASS |
| R7 Gemini fully repaired | 5.0 | 0.951 | +0.0112 | [+0.0040,+0.0189] | PASS | 0.907 | PASS |
| **GEM as submitted** | 5.0 | n/a | **−0.0977** | [−0.1174,−0.0762] | **FAIL** | **0.807** | **FAIL** |

GEM as submitted has **negative skill in 27 of 28 series** (only CCAP positive, +0.017).
Its two worst are the indices: EGX70 −0.326, EGX30 −0.245.

### B. Full sample 2012–2026 — 1,293 windows

| arm | skill | 90% CI | verdict | cov90 | D |
|---|---|---|---|---|---|
| PROD YZ-HAR | −0.0023 | [−0.0097,+0.0048] | **PARITY** | 0.896 | PASS |
| R2 YZ-HARQ | −0.0021 | [−0.0095,+0.0051] | PARITY | 0.896 | PASS |
| R7 Gemini repaired | −0.0031 | [−0.0087,+0.0026] | PARITY | 0.902 | PASS |
| GEM as submitted | −0.0570 | [−0.0668,−0.0470] | **FAIL** | 0.767 | **FAIL** |

Stocks only (1,214 windows): PROD +0.0003 PARITY, R2 +0.0005 PARITY, GEM −0.0535 FAIL
(negative in **28 of 28** series).

**This is the uncomfortable one: production's edge does not survive extension to 15 years.**
+0.0128 PASS on the post-2022 window becomes −0.0023 PARITY over 2012–2026. That is not
a Gemini result — it is a statement about our own engine, and it deserves its own
investigation rather than a footnote. Two readings, both plausible and not yet separated:
the break cut at 2022-03-21 is doing real work (the pre-2022 regime genuinely differs),
or the post-break PASS is partly a favourable-sample artifact. The honest position is
that we do not currently know which.

### C. Indices — EGX30 + EGX70, 79 windows

| arm | skill | 90% CI | verdict | cov90 | D |
|---|---|---|---|---|---|
| **PROD YZ-HAR** | **−0.0234** | [−0.0381,−0.0007] | **FAIL** | **0.772** | **FAIL** |
| R2 YZ-HARQ | −0.0234 | [−0.0381,−0.0007] | FAIL | 0.772 | FAIL |
| R4 PROD + online ACI width | −0.0119 | [−0.0299,+0.0099] | PARITY | 0.886 | PASS |
| R7 Gemini repaired | −0.0073 | [−0.0262,+0.0156] | PARITY | 0.873 | FAIL |
| GEM as submitted | −0.1432 | [−0.2040,−0.0815] | FAIL | 0.709 | FAIL |

**Production FAILs on Egyptian indices** and misses criterion D by 11 points (77.2% vs an
88% floor). This is the first index-class instrument the engine has ever been scored on
and it does not transfer from the single-stock fit.

**Confounded, and I will not call a verdict until it is resolved:** I ran `q_annual = 0`
for every series, which is gate-neutral for a *stock* comparison (engine and benchmark
carry the same anchor) but is **not innocuous for coverage** — the EGX30 is a PRICE index
and its constituents' aggregate dividend yield is material, so a q=0 anchor systematically
mis-centres the index cone. Sourcing a real EGX30/EGX70 dividend yield is a prerequisite
before any index verdict is recorded. What is *not* confounded is the ordering: the two
arms carrying an adaptive width multiplier are the only ones that get index coverage near
target, which points at width, not only at drift.

Also note the indices are the one place where the ACI/adaptive-width layer *helps* —
the opposite of its effect on single stocks. An index's realized vol sits well below the
single-stock panel average, so a pooled market width over-narrows it. Same mechanism the
`adaptive_width.py` note identified, in the opposite direction.

---

## Verdict on the four acceptance criteria, this panel

| | GEM as submitted | GEM fully repaired |
|---|---|---|
| **1. Personalized drift per stock** | **No** — Hurst gate closed 86% of windows; all series share drift = 0 | **No** — carry is market-level; drift differs across series in **0 of 1,293 windows** |
| **2. Optimized cone width per stock** | **No** — per-stock but biased ~46% low | **Partial** — per-stock variance yes; per-stock *multiplier* hurts stocks (−0.0010 to −0.0022), helps indices |
| **3. cov90 in 88–92%** | **No** — 80.7% post-break, 76.7% full sample | **Yes** — 90.7% post-break, 90.2% full sample |
| **4. Beats the dumb yardstick** | **No** — FAIL everywhere; negative in 28/28 series | **Post-break yes** (+0.0112 PASS); **full sample no** (PARITY); **indices no** (PARITY) |

**All four at once: no, for either version.**

## Disposition

1. **`dq_patch.py` should become a PR against `engine/data_quality.py`.** This is the
   highest-value output of the session and it is independent of the Gemini question. Until
   it merges, **do not drop these extended-history files into `engine/raw_ohlc/EG/`** — the
   unattended loop would ingest six corrupted series and refit the whole EG market on them.
2. **Log-space CRPS should be evaluated as the panel-scoring basis.** Price-space CRPS is
   not merely noisy on a lognormal-t, it is non-convergent. Needs its own PR and a
   re-verification that existing verdicts are unchanged on the current short panels.
3. **The full-sample PARITY result on production needs its own investigation** — is the
   2022-03-21 break carrying the PASS, or is the PASS sample-specific?
4. **Indices need an index profile**: sourced dividend yield, an index-appropriate
   Step 0.0 threshold (an index has no single-stock limit; the EGX market-wide breaker is
   the right basis), and their own (ν, width_cal) fit. Do not publish an index cone off the
   single-stock fit.
5. Gemini as submitted: **REJECTED**, now on 28 series and 1,293 windows. Repaired: passes
   D and beats the yardstick post-break, still does not beat production.
6. Nothing pushed. Any push needs a fresh PAT at that moment.
