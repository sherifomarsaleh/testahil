# Selection engine — data, scripts, and record (27-Jul-2026)

This commit does three things:

1. **Replaces `engine/raw_ohlc/AE/` and `engine/raw_ohlc/SA/` with the long-history
   libraries** (AE 18 names, ten ≥15.5 yrs; SA 11 names, six ≥15.5 yrs), gated clean
   on 27-Jul-2026 — see the two Export Gate docs in the project (overlap-verified
   price-identical to the previous 5.5-yr files on every common date). SA files are
   staged with the 2026-07-27 export-day rows dropped per the SA gate's recorded
   rule; AE files end 2026-07-24 (complete session), verbatim vendor exports.
2. **Adds the pooled test pipeline** (`build_cohorts_pooled.py` → `factors_pooled.py`
   → `significance_pooled.py`), the F5 forensic scripts, and the shadow-cohort
   scorer. Path constants (`RAW_BASE`, `OUT`) sit at the top of each script — the
   only edit needed to re-run anywhere. Requires numpy/pandas/scipy plus this repo's
   `engine/` on `sys.path` (`data_quality.clean_ohlc`, `primitives.yz_variance_proxy`).
3. **Snapshots the key records** in `docs/`: the full-power pre-registered test
   result (no adoption; F6 one rule short), the F5 forensic determination
   (UNTESTABLE — retired), the shadow-cohort ledger as filed, and `STATE.md`
   (standing orders for the autonomous monthly cycle).

The living documents — signed pre-registration, interim run, gate docs, and the
append-only shadow ledger — live in the "Selection engine" Claude project; the
copies here are point-in-time snapshots for reproducibility. Verification chain for
everything in this commit: the EG scripts reproduce the 27-Jul exploratory pass
exactly; the pooled scripts reproduce the recorded interim run exactly; the
full-power run was executed on precisely these staged files.
