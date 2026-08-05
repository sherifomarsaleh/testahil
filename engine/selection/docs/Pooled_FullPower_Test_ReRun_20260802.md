# SELECTION ENGINE — POOLED EG+AE+SA RE-RUN (02-Aug-2026)

**Status: reproduction / freshness check, NOT a new binding run.** This re-executes the
frozen pooled pipeline (`build_cohorts_pooled.py` → `factors_pooled.py` →
`significance_pooled.py`) against the current repo `main` data, to close out the
monthly autonomous cycle's step 3 for the 01-Aug-2026 firing. Same scripts, same seeds
(H₀ 42, bootstrap 0, power 7), same B (30,000 / 5,000 / 8,000); critical values
re-simulated at the run's real dimensions. The only script change since the binding
27-Jul run is a comment-only naming edit in `factors_pooled.py` (docstring "60 sessions"
→ "3-month window"; the estimator definition is byte-identical). Survivorship-bias
caveat applies as in every run: the universe is today's listed names.

## Why this run adds no new evidence

The step-3 gate ("≥60 EG majority-quorum sessions after the 2026-04-20 last full-power
anchor, AND long AE/SA on `main`") is numerically satisfied — 60 EG sessions fall in
(2026-04-20, 2026-07-22], and the long AE/SA libraries (2011→2026) have been on `main`
since 28-Jul-2026 (commit `108ab4f`). **But the libraries have not been rolled forward
past their 27-Jul anchors** (EG 2026-07-22 · AE 2026-07-24 · SA 2026-07-26), so the
EG master grid still ends at the **same last anchor, 2026-04-20**. A genuinely new
resolvable anchor requires ~60 further forward sessions (data through ~mid-Oct 2026).
The re-run therefore reproduces the 27-Jul full-power test rather than extending it.

## Dimensions (real, re-simulated) — identical to 27-Jul

- Reference calendars: EG 3,744 sessions (2011-01-02 → 2026-07-22, quorum ≥15/30);
  AE 3,754 (2011-01-02 → 2026-07-24, ≥9/18); SA 3,881 (2011-01-01 → 2026-07-26, ≥6/11).
- EG master grid: **58 anchors** (2012-03-25 → 2026-04-20), **41** for F3.
- AE + SA mappable and forward-resolvable at **58 of 58** EG anchors (AE 40/41 for F3,
  SA 41/41).

## Results — re-run vs 27-Jul binding run

| Factor | Re-run pooled IC | 27-Jul IC | Crit Bonf (IC) | §6 rules 1·2·3·4·5 | Verdict |
|---|---|---|---|---|---|
| F1 momentum (+)   | +0.0317 | +0.0318 | +0.0499 | ✗ ✗ ✓ ✓ ✓ | not detected |
| F2 ST-reversal (−)| +0.0138 | +0.0137 | −0.0490 | ✗ ✗ ✗ ✓ ✗ | WRONG SIGN |
| F3 LT-reversal (−)| −0.0251 | −0.0249 | −0.0619 | ✗ ✗ ✓ ✓ ✗ | not detected |
| F4 low-vol (+)    | +0.0329 | +0.0332 | +0.0509 | ✗ ✗ ✓ ✓ ✗ | not detected |
| F5 Amihud (+)     | +0.0098 | +0.0104 | +0.0503 | — retired (UNTESTABLE) | BLOCKED (volume DQ) |
| F6 52w-high (+)   | **+0.0462** | +0.0460 | +0.0499 | ✗ ✓ ✓ ✓ ✓ | single-only |

**Headline: no factor ADOPTED — unchanged from 27-Jul.** F6 remains the lead: it clears
the Bonferroni tercile-spread bar (+0.1197 vs +0.1187) and rules 3–5, and misses only
the Bonferroni IC bar, by **0.0037** (+0.0462 vs +0.0499). F5 stays retired (its IC is
not quoted as evidence; shown for reproduction only). Residual 4th-decimal differences
vs 27-Jul are numpy/BLAS version noise and do not move any rule outcome. NOT DETECTED at
this power — not "no signal."

## Reproduction notes

- Path constants (`RAW_BASE`, `OUT`, `sys.path`) are the only edits needed to re-run
  anywhere, per the pipeline README; no other lines were touched.
- Environment: numpy 2.4.6 / pandas 3.0.5 / scipy 1.17.1. Significance stage wall time
  ~5 min (30k H₀ + true drop-one-name jackknife + power at four ρ).
- Estimator-mirror asserts (vectorised H₀ path ≡ stored per-cohort Spearman) pass at
  <1e-9 on ten cohorts per factor.

## Bottom line for the cycle

Step 3 for the 01-Aug firing is complete: the re-run is valid and reproduces the binding
verdict; there is no new cohort and nothing to adopt. The next run that can change the
answer is the one after the libraries roll forward far enough to resolve a new anchor
(~mid-Oct 2026), which also aligns with Shadow Cohort #1's first maturity.
