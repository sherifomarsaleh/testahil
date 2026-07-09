# Testahil MC Engine v3 — Validation Results (10 Jul 2026)

**Design:** carry-anchored drift (ln(1+rf)−ln(1+q), MarketProfile schedule) + shrunk signal alpha (IC·σ_H·sign·clip(z), dead zone 0.5, clip ±2, cap ±0.5σ_H) · bias-corrected shrunk YZ-HAR width · fitted-ν Student-t shape (LONO cross-fitted) · benchmark = carry-anchored trailing-vol lognormal RW (same anchor, so skill isolates signal+width). Gate = pooled panel CRPS skill, calendar-block bootstrap 90% CI → PASS / PARITY / FAIL; pinball-0.5 and Winkler-90 skills co-reported.

## Ladder (Egypt panel: PHDC, TMGH, EMFD, OCDI, ORHD, GBCO — 98 pooled non-overlapping 60d windows · Alinma 18)

| Rung | Config | Egypt CRPS skill (90% CI) | Verdict | pin50 | wink90 | cov90 | Alinma CRPS |
|---|---|---|---|---|---|---|---|
| L0 | incumbent v2 (t5, no carry, secular mean on developers) | −0.044 [−0.172, +0.050] | PARITY | −0.145 | +0.092 | 0.88 | −0.001 PARITY |
| L1 | carry anchor both sides, mean drift killed | **+0.049 [+0.019, +0.088]** | **PASS** | −0.001 | +0.112 | 0.89 | −0.011 PARITY |
| L2 | + width fix (exp(s²/2) bias corr., 0.8/0.2 log-shrink) | +0.044 [+0.019, +0.075] | PASS | −0.001 | +0.102 | 0.90 | −0.007 PARITY |
| L3 | + fitted shape (ν=4 LONO, width_cal 0.98–1.06) | +0.044 [+0.017, +0.079] | PASS | −0.001 | +0.092 | 0.90 | −0.009 PARITY |
| L4 | + signal: Egypt rev_1m, IC 0.08 (SA off) | **+0.060 [+0.033, +0.102]** | **PASS** | **+0.026** | +0.085 | 0.89 | −0.009 PARITY |
| L4-alt | Egypt mom_12_1 (+) instead | +0.033 [−0.017, +0.077] | PARITY | −0.024 | — | 0.89 | — |

**Per-name L4:** PHDC +0.040 · TMGH +0.057 · EMFD +0.100 · OCDI +0.085 · ORHD +0.024 · GBCO −0.013 · ALINMA −0.009. Signal active in 31–69% of Egypt windows. Coverage essentially nominal (cov50/80/90 = 0.49/0.79/0.89).

## What the ladder proves
1. **The old drift mechanism was the failure, not the architecture.** Killing the raw expanding-mean drift and anchoring both engine and null to the policy-rate carry moves Egypt from PARITY (−0.044, pin50 −0.145) to PASS (+0.049) in one step. The old engine over-committed (PHDC +11.7%/quarter median) with no evidential basis.
2. **The reversal prior is confirmed, momentum rejected.** rev_1m (sign −1, IC 0.08 fixed a priori) lifts pooled skill to +0.060 and flips median-placement skill positive (+0.026); the momentum-sign alternative degrades both — consistent with the EGX-reversal literature. IC was not tuned; one fixed value, two pre-registered sign candidates, disclosed.
3. **Fitted ν = 4 (fatter than t5), not thinner.** EGX 60-day aggregates carry genuine jump risk (devaluations); the aggregational-Gaussianity prior does not hold on this panel. width_cal 0.98–1.06 → the old width was nearly unbiased.
4. **The pooled gate has the power the per-name gate lacked.** 98 windows resolve skill of ±0.03; 18 cannot. Per-name Step 0 becomes a diagnostic; the market-panel CI is the gate.
5. **Alinma is PARITY, permanently and honestly.** Carry ≈ 0 because rf (~4.25%) ≈ dividend yield (~4.2%): the bank pays its carry out as cash. Committed statement: total return ≈ +1.0%/quarter, ~all of it dividend, price ≈ flat ± band. Signal stays off until the Saudi panel reaches ~5 names.

## Live cards (v3 final config)
- **ALINMA** spot 24.00 (7 Jul): T+60 median 23.98 (−0.1%), IQR 22.80–25.23, 90% 20.73–27.81, P(up) 50%. Carry −0.04% (rf 4.25% est − q 4.17%).
- **PHDC** spot 16.19 (17 Jun data): T+60 median 16.55 (+2.2%) = carry +4.24% − reversal alpha 1.93% (z=+1.12 after the April rally), IQR 14.79–18.53, 90% 11.96–23.03 (≈10% narrower than v2's), P(up) 55%. v2 would have said +11.7%.

## Flags (unresolved, need decisions/actions)
- **SAR risk-free not directly sourced** — live anchor is a SAMA-repo-derived estimate (4.25%); replace with FTSE SAGBI / iBoxx Tadawul SAR sukuk yield before any Saudi publish (±50bp = ±0.12% on the median — immaterial but the sourcing rule stands). Egypt live anchor set at the CBE main-op rate 19.50% (sourced); fresh 3M T-bill quote flagged for first EGX publish.
- **Backtest carry schedules** are policy-rate-derived approximations — gate-neutral by construction (both sides carry them), documented in market_profiles.py.
- **PIT 0.587** (slightly right of 0.5, ≈3σ on n=98): realized prices ran modestly above the carry median — the equity risk premium we deliberately exclude (lens independence). Committed level still beats the null on CRPS and pinball; embedding ERP would breach §3/§1 separation.
- **GBCO per-name −0.013**: within parity; monitor as the panel grows.
- **Adoption not yet executed**: making v3 the standing engine requires a Standing_Research_Protocol edit (Step-0 gate → pooled three-way), Calibration Ledger annotation for KABO/QGTS/MAADEN re-scoring under the new null, and the ticker-page probability cards re-rendered with carry-anchored medians. Publishing remains a separate explicit step.
