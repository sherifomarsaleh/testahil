"""AIRARABIA study — formal attestations: ModelStudyChecklist + SIGCMChecklist,
asserted (a raise here means DO NOT ISSUE), plus verify-by-import of every
engine module this study touched."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

# verify-by-import (never by parse)
import market_profiles, research_protocol, wacc_builder, adaptive_width, research_sweep
import technicals, apply_technicals, ta_chart, rollforward_one, data_quality, mc_v3
p = market_profiles.PROFILES['AE']
assert (p.nu, p.width_cal) == (8.0, 0.979), (p.nu, p.width_cal)
print('verify-by-import OK — market_profiles (AE nu=8.0/0.979), research_protocol, '
      'wacc_builder, adaptive_width, research_sweep, technicals, apply_technicals, '
      'ta_chart, rollforward_one, data_quality, mc_v3 all import')

from research_protocol import (ModelStudyChecklist, assert_model_study,
                               SIGCMChecklist, assert_sigcm)

m = ModelStudyChecklist(
    structure_matches_model=True,        # 16-section Word + 16-sheet Excel, asserted in builder
    bibliography_document=True,          # AIRARABIA_Bibliography_09-08-2026 (docx+pdf)
    provenance_four_field=True,          # every INPUT four-field, asserted in compute.py
    numeric_traceability=True,           # builders read study_numbers.json only; recalc.py 644/644
    external_reader_scrub=True,          # qc_checks.py: 0 hits, both documents
    figure_discipline=True,              # qc_checks.py: 8/8 opaque light canvases; PDFs inspected
    table_discipline=True,               # qc_checks.py: 31 tables, 0 over/starved/bloated
    expert_appendix_max_detail=True,     # C.1-C.6 with worked tables, falsifiers, divergence
    contested_judgement_both_ways=True,  # JV network book vs capitalised, everywhere; fuel dual too
)
assert_model_study(m)
print('MODEL-STUDY BAR: PASS —', 'all 9 standards attested')

# The beta clause is attested against the RESOLVER, not against a string typed here: the
# regressor is whatever the exchange-keyed rule returns for this stock's exchange, and the
# study's committed regression must have been run on that exact file.
import json as _json
from wacc_builder import market_index_path as _mip, index_interim_note as _iin
_BETA_IDX = os.path.basename(_mip('AE', 'DFM'))
_BR = _json.load(open(os.path.join(HERE, 'beta_result.json')))
assert _BR['index_file'] == _BETA_IDX, (
    f"the committed beta was regressed on {_BR['index_file']!r} but the rule resolves "
    f"{_BETA_IDX!r} for (AE, DFM)")
assert _BR.get('interim_note') == _iin('AE', 'DFM'), \
    'an interim regressor must carry its disclosure note verbatim in beta_result.json'
assert _BR['usable'], 'the resolved regressor must clear the usability gate'

s = SIGCMChecklist(
    historicals_official_only=True,      # audited FS FY2022-25 + reviewed Q1-2026, company IR only
    forecast_ground_up=True,             # pax x fare, cost per pax, one escalator per class
    debt_lc_fx_split=True,               # all debt AED-denominated (leases+borrowings); stated
    asset_conversion_cycle=True,         # deferred income/payables/provisions cycle measured, projected
    competitors=True,                    # peer KPIs+multiples in and outside the UAE, cross-check only
    # own-stock 5y weekly vs the index the exchange-keyed rule RESOLVES for (AE, DFM):
    # FADGI, under the registered interim substitution. Asserted against the resolver
    # below rather than asserted in a comment.
    beta_own_history_vs_egx30=True,
    formula_based_model=True,            # 644 formula cells, driver test 24/24, zero dead inputs
    flags_raised_before_issue=True,      # seat/ASK gap, hedge ratios, capex split — all flagged
    stop_and_inform_honoured=True,       # no blocking gap was hit: primary sources were reachable
    na_reasons={},
)
assert_sigcm(s)
print('SIGCM: PASS — all clauses attested (beta clause: own history vs the stock\'s own '
      f'local index -- {_BETA_IDX}, resolved by market_index_path("AE", "DFM"), '
      f'interim-substitution note carried in the report)')
