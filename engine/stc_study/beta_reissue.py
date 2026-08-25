"""STC beta — re-derived against TASI, replacing a daily 9-week stopgap.

WHY THIS FILE EXISTS. The delivered study set beta = 0.48 from this attempt, recorded
verbatim in stc_compute.py:

    "Genuine daily STC-vs-TASI regression, n=40 paired sessions (5-May->7-Jul-2026,
     investing.com TASI closes) ... Flag: 9-week window (longer TASI history not
     programmatically accessible); beta sensitivity grid published."

The study flagged it honestly and the flag was the right call at the time. But the standing
rule is explicit that this is not a tier: "A daily/short-window regression is NOT one of
these tiers -- if ever used as a stopgap, flag it as interim and replace with tier (1)
before a study is audit-clean." The replacement condition has been met since 10-Aug-2026,
when TASI was supplied and registered, and the instruction adopting it said so in terms:
"STC and every other Tadawul beta must be re-derived against it." That re-derivation is
what this file is.

The regressor is resolved, not chosen: own_stock_beta() goes through
wacc_builder.market_index_path(market, exchange). STC is Tadawul-listed -- assets/data.js
records its code as "TADAWUL:7010", a NUMERIC code whose raw library file is SA/STC.csv.
That mismatch is the trap that caught ALRAJHI (code TADAWUL:1120, file RAJHI) on the day
the per-name calibration builder landed, so the ticker passed here is the library stem and
the exchange is passed explicitly.

NO REGRESSION IS HAND-ROLLED HERE, and the study directory still carries
stc_tasi_daily_for_beta.csv -- the 40-session extract behind the superseded number. It is
left in place as the evidence for what was superseded, not as an input: nothing in this file
reads it.

WHAT THIS FILE DOES NOT DO. It does not re-issue the WACC. That needs Saudi Arabia's own
sovereign default spread on both bases from Damodaran's original ctryprem.html, which the
protocol forbids reconstructing from memory. The delivered study also predates the v2 method
(it passes `rf=`, which the current WaccInputs rejects) and imports mc_v2, which is no longer
in the repo -- so a re-issue is a rebuild, not a patch. What is computed below needs no new
sourcing: Ke = rf* + beta x ERP, so the beta delta's effect on Ke at the study's OWN recorded
ERP is exact and assumes nothing about rf*.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from beta_regression import own_stock_beta                      # noqa: E402
from research_protocol import assert_beta_provenance            # noqa: E402

MARKET, EXCHANGE, TICKER = 'SA', 'TADAWUL', 'STC'

# Verbatim from engine/stc_study/stc_compute.py, the delivered study.
SUPERSEDED_BETA = 0.48                 # BETA = round(reg.beta, 2), reg.beta = 0.4753
SUPERSEDED_RAW = 0.4753
SUPERSEDED_SOURCE = ("Genuine daily STC-vs-TASI regression, n=40 paired sessions "
                     "(5-May->7-Jul-2026, investing.com TASI closes); flagged as a 9-week "
                     "window, longer TASI history not programmatically accessible at the time")
STUDY_ERP_RATING, STUDY_ERP_CDS = 0.0501, 0.0572   # Damodaran Saudi row, 5-Jan-2026, per the study

rec = own_stock_beta(TICKER, MARKET, EXCHANGE)
assert_beta_provenance(rec)                         # [R-BETA-04] gate, on the record itself

d_beta = rec['beta'] - SUPERSEDED_BETA
ke_delta = {'rating_basis_pp': round(100 * d_beta * STUDY_ERP_RATING, 3),
            'cds_basis_pp': round(100 * d_beta * STUDY_ERP_CDS, 3)}

out = dict(rec)
out.update({
    'superseded_beta': SUPERSEDED_BETA,
    'superseded_beta_raw': SUPERSEDED_RAW,
    'superseded_beta_source': SUPERSEDED_SOURCE,
    'superseded_tier': 'none — a daily short-window stopgap, which the rule states is not a tier',
    'tier': 1,
    'delta_beta': round(d_beta, 6),
    'ke_delta_at_study_erp': ke_delta,
    'study_erp_rating': STUDY_ERP_RATING,
    'study_erp_cds': STUDY_ERP_CDS,
    'wacc_reissue_blocked_on': (
        "Saudi Arabia's own sovereign default spread, rating basis and CDS basis, read fresh "
        "from Damodaran's original ctryprem.html. Not reconstructed from memory: stop and "
        "inform. The study additionally imports mc_v2, which is not in the repo."),
})

path = os.path.join(HERE, 'beta_result.json')
with open(path, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1)

print(f"{TICKER}: tier-1 beta {rec['beta']:.4f} vs {rec['index_file']} "
      f"(n={rec['n']} {rec['frequency']}, R2={rec['r2']:.3f}, SE={rec['se']:.3f}, "
      f"{rec['gate_msg']})")
print(f"  supersedes {SUPERSEDED_BETA} (daily n=40 stopgap) -> delta {d_beta:+.4f}")
print(f"  Ke effect at the study's own ERP: {ke_delta['rating_basis_pp']:+.3f}pp rating basis, "
      f"{ke_delta['cds_basis_pp']:+.3f}pp CDS basis")
print(f"  wrote {os.path.relpath(path, os.path.join(HERE, '..', '..'))}")
