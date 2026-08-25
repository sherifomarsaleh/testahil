"""GBCO beta — re-derived against the EGX's PUBLISHED index, replacing an assumed 1.0.

WHY THIS FILE EXISTS. The delivered study set beta = 1.0 and recorded why:

    "assumed_1.0 -- n=5 annual GBCO-vs-EGX30 regression gave beta=-0.15, R2=0.008
     (unusable); higher-frequency EGX30 data inaccessible via available tools;
     house rule default applied"

Tier 3 is the LAST resort in the standing preference order, reachable only when neither a
2-5yr own-stock regression nor a same-country peer set is available. What was actually
attempted was an n=5 ANNUAL regression -- not one of the tiers at all. The binding tier 1 is
a 2-5yr WEEKLY or monthly regression against the published index of the exchange the stock
is listed on, and EGX30 has been registered in this repo since 10-Aug-2026. So tier 1 was
available and was never run: the study fell three tiers on the strength of a test the rule
does not recognise.

The regressor is NOT this file's choice. beta_regression.own_stock_beta() resolves it
through wacc_builder.market_index_path(market, exchange) -- GBCO is EGX-listed, which the
site records as the code prefix "EGX:" in assets/data.js and which this file passes
explicitly rather than inferring from the raw_ohlc/EG/ folder (market codes group by
country; EG happens to be single-exchange, AE does not, and reading the folder would be the
habit that breaks on the first dual-exchange market).

NO REGRESSION IS HAND-ROLLED HERE. Every study in this repo once wrote its own and every
one of them regressed against an equal-weight composite of the covered names; on FERTIGLB
that understated beta ~40% and overstated the centre 21.6%. own_stock_beta is the only
sanctioned route: it runs Step 0.0 on both series, matches the weekly grid to the exchange's
real trading week, and returns provenance with the number.

WHAT THIS FILE DOES NOT DO. It does not re-issue the WACC. That needs Egypt's own sovereign
default spread on both the rating and CDS bases, read fresh from Damodaran's original
ctryprem.html -- volatile, per-sovereign figures the protocol forbids reconstructing from
memory. The study's published WACC additionally predates the v2 method (it passes `rf=`,
which the current WaccInputs rejects outright), so a re-issue is a rebuild, not a patch.
What is computed below is the one thing that needs no new sourcing: the effect of the
corrected beta on Ke at the study's OWN recorded ERP. Ke = rf* + beta x ERP, so the delta is
exact and carries no assumption about rf*.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from beta_regression import own_stock_beta                      # noqa: E402
from research_protocol import assert_beta_provenance            # noqa: E402

MARKET, EXCHANGE, TICKER = 'EG', 'EGX', 'GBCO'

# Verbatim from engine/gbco_study/compute.py, the delivered study.
SUPERSEDED_BETA = 1.0
SUPERSEDED_SOURCE = ("assumed_1.0 -- n=5 annual GBCO-vs-EGX30 regression gave beta=-0.15, "
                     "R2=0.008 (unusable); higher-frequency EGX30 data inaccessible via "
                     "available tools; house rule default applied")
STUDY_ERP_RATING, STUDY_ERP_CDS = 0.1394, 0.0941      # Damodaran Egypt row, Jan-2026, per the study

rec = own_stock_beta(TICKER, MARKET, EXCHANGE)
assert_beta_provenance(rec)                            # [R-BETA-04] gate, on the record itself

# A number stated in prose must be COMPUTED, not typed.
d_beta = rec['beta'] - SUPERSEDED_BETA
ke_delta = {'rating_basis_pp': round(100 * d_beta * STUDY_ERP_RATING, 3),
            'cds_basis_pp': round(100 * d_beta * STUDY_ERP_CDS, 3)}

out = dict(rec)
out.update({
    'superseded_beta': SUPERSEDED_BETA,
    'superseded_beta_source': SUPERSEDED_SOURCE,
    'superseded_tier': 3,
    'tier': 1,
    'delta_beta': round(d_beta, 6),
    'ke_delta_at_study_erp': ke_delta,
    'study_erp_rating': STUDY_ERP_RATING,
    'study_erp_cds': STUDY_ERP_CDS,
    'wacc_reissue_blocked_on': (
        "Egypt's own sovereign default spread, rating basis and CDS basis, read fresh from "
        "Damodaran's original ctryprem.html. The v2 method normalises rf* = local govt-bond "
        "yield - that sovereign's OWN default spread, so country risk enters once via the CRP "
        "inside the ERP; the delivered study passes the raw local yield to a field the current "
        "WaccInputs does not accept. Not reconstructed from memory: stop and inform."),
})

path = os.path.join(HERE, 'beta_result.json')
with open(path, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=1)

print(f"{TICKER}: tier-1 beta {rec['beta']:.4f} vs {rec['index_file']} "
      f"(n={rec['n']} {rec['frequency']}, R2={rec['r2']:.3f}, SE={rec['se']:.3f}, "
      f"{rec['gate_msg']})")
print(f"  supersedes assumed {SUPERSEDED_BETA} (tier 3) -> delta {d_beta:+.4f}")
print(f"  Ke effect at the study's own ERP: {ke_delta['rating_basis_pp']:+.3f}pp rating basis, "
      f"{ke_delta['cds_basis_pp']:+.3f}pp CDS basis")
print(f"  wrote {os.path.relpath(path, os.path.join(HERE, '..', '..'))}")
