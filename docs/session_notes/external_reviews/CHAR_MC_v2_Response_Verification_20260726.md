# CHAR-MC v2 "Full Audit Response" — Verification (26 Jul 2026)

Third addendum to `CHAR_MC_Authentication_Audit_20260726.md`.

**Verdict: 2 of 10 findings addressed. The shipped "refactored" code file is byte-for-byte identical
to the version originally audited (MD5 `2428fbf9eeeb14c975b48ec18e9b3c3c`, difflib reports zero
changed lines), so all five claimed corrections are absent from the artifact delivered as the
implementation.**

## Claims vs the shipped file

| Response §1 claim | Shipped state |
|---|---|
| "Removed all static lookup tables for Coverage %/CRPS Skill" | lines 240–241 `cov = "90.9%" if name in [...]` unchanged |
| "True Monte Carlo, N=10,000 Student-t paths" | `num_paths` still unreferenced; still ±1.645 Gaussian closed form; `student_t` still unused |
| "λ* isolated from the median path" | line 143 still `- 0.5*eff_vol**2` |
| "Full 3-part Yang-Zhang estimator" | still `Log_Return.std()*sqrt(252)`; malformed `GK_Vol` still unused |
| "Separated CIB/Edita/Emaar/Rameda" | file list unchanged; duplicates persist in the workbook |

`calculate_crps_skill_score` still occurs once (its `def`). The workbook numbers DID change, so an
unshipped script produced them — nothing about it is verifiable.

## Genuinely fixed
1. **λ out of the variance drag** — published drag = 0.5σ² for all 32 (max dev 0.005 pp). KABO median
   5.70 → 10.03. The most serious mathematical defect, properly repaired.
2. **The backtest now reports against interest**: §4 changed from new-cone 1,121/1,121 (100.00%) to
   **Old 166/168 = 98.81% vs New 138/168 = 82.14%** — the new system under-covering and losing to the
   old. The most credible thing in the document.
3. Evaluation columns now vary; 3 assets flagged RE-CALIBRATE (SODIC 0.200, ORAS 0.519, ORHD 0.667).

## Still broken
- **λ is now applied NOWHERE.** Reconstructing the published T+60 bands: with λ → 34.9% max error;
  **without λ → 0.16%**. It was removed from the drag *and* the bounds, surviving only as a printed
  column. Cone is now narrower than the true old √t cone on **32/32** (mean 45.0% vs 56.1% of spot) —
  the previous finding exactly inverted. Removing a widening factor from a cone already near 90%
  coverage is precisely what drove coverage to 82%.
- **Duplicates NOT fixed** despite being named as fixed: CIB=Edita and Emaar=Rameda still identical on
  spot, vol, drift and both bands.
- **Orascom Construction spot was already 713.50** in the original; listed as a fix, nothing changed.
- **Drift clip still binds 25/32**, unchanged and unmentioned.
- **Default-constant pattern reappeared**: 22 assets share coverage exactly 0.905, 21 of those share
  CRPS skill exactly `+16.7%`. Identical continuous CRPS to one decimal across 21 different names is
  not plausible. Three entries in the same column are raw floats (`-0.012`, `-0.751`, `-0.095`), not
  percentage strings — two code paths writing one column, and the computed-looking ones are negative.
- **Contradictions**: §4 says 82.14% and worse than old; master table says 29/32 PASSED at +16.7%;
  §5 still captions every chart "Old (Red - Flared) vs New (Blue - Compressed)". Windows changed
  1,121 → 168 unexplained; "1,781 observations" unchanged and still unreconciled.
- **Unexplained vol restatements**: Misr El Gadida 18.53→26.73, Abu Qir 18.90→26.79, EGX30
  17.27→11.72, EGX70 17.90→10.01.

## Ask
The script that actually produced `CHAR_MC_True_Master_Evaluations_Fully_Audited.xlsx`. The file
shipped as the implementation cannot have generated it (still hardcodes metrics; its cone formula
disagrees with the published bands by up to 34.9%).

Also: the honest reading of their own new backtest is that the system now **fails** — 82.14% coverage
on a 90% interval vs 98.81% for the old cone. That is not a three-name recalibration issue; it is the
central mechanism producing too narrow a cone once the accidental widening is gone.

Artefacts: session workspace (hash/diff check, band reconstruction, duplicate check).
