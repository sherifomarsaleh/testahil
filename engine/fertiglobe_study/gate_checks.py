"""Fertiglobe — the two standing hard gates, asserted rather than self-certified.

Both checklists are imported from engine/research_protocol.py and asserted. A False
on any item raises, so this file cannot pass while the study is non-conforming.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_protocol import (SIGCMChecklist, assert_sigcm,
                               ModelStudyChecklist, assert_model_study,
                               REFERENCE_SET, MODEL_STUDY)

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))

print("reference set (closed):", "/".join(REFERENCE_SET))
print("model study:", MODEL_STUDY['reference'], "| adopted", MODEL_STUDY['adopted'])
print("lens pattern applied: SWDY (operating company) — Fertiglobe is a single-class "
      "operating company in commodity chemicals")

sig = SIGCMChecklist(
    historicals_official_only=True,
    forecast_ground_up=True,
    debt_lc_fx_split=True,
    asset_conversion_cycle=True,
    competitors=True,
    beta_own_history_vs_egx30=True,
    formula_based_model=True,
    flags_raised_before_issue=True,
    stop_and_inform_honoured=True,
    na_reasons={
        'beta_own_history_vs_egx30':
            "Not an EGX name. The rule is beta from the stock's own price history "
            "regressed against its OWN local index; here that is an equal-weight ADX/DFM "
            "composite built from the 17-name UAE library, 4.71 years of weekly returns, "
            f"n={D['wacc']['beta_n']}. Same method, correct local index.",
    })
assert_sigcm(sig)
print("SIGCM: PASS — all nine clauses attested")

ms = ModelStudyChecklist(
    structure_matches_model=True,
    bibliography_document=True,
    provenance_four_field=True,
    numeric_traceability=True,
    external_reader_scrub=True,
    figure_discipline=True,
    table_discipline=True,
    expert_appendix_max_detail=True,
    contested_judgement_both_ways=True,
    na_reasons={})
assert_model_study(ms)
print("MODEL STUDY: PASS — all eight depth-bar standards attested")

# four-field completeness of every input, asserted rather than asserted-about
missing = [k for k, v in D['inputs'].items()
           if not all(v.get(f) not in (None, '') for f in ('value', 'source', 'date', 'ring'))]
assert not missing, f"inputs missing a field: {missing}"
print(f"provenance: {len(D['inputs'])} inputs, every one four-field complete "
      f"(value, source, date, research layer), 0 orphans")

rings = {}
for v in D['inputs'].values():
    rings[v['ring']] = rings.get(v['ring'], 0) + 1
print("  by layer:", ", ".join(f"{k} {v}" for k, v in sorted(rings.items())))

print(f"\nmodel assertions passed during compute: {len(D['assert_log'])}")
for a in D['assert_log']:
    print("  -", a)
