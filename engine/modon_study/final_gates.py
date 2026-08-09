"""MODON study — the two standing hard gates, run as the last scripted step.

SIGCM (source integrity & ground-up construction) and the model-study depth bar.
A failure raises: the study must not issue."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_protocol import (SIGCMChecklist, assert_sigcm,
                               ModelStudyChecklist, assert_model_study)

sig = SIGCMChecklist(
    historicals_official_only=True,     # FY2023/24/25 + H1-2026 from the company's own filings
    forecast_ground_up=True,            # segment build, backlog roll, unit anchors; gap flagged
    debt_lc_fx_split=True,              # note 29 tranche table: AED vs USD/EUR/GBP/SAR, carried
    asset_conversion_cycle=True,        # NWC studied (inventory/DWIP/receivables/escrow) and
                                        # BS/CF projected from a stated release schedule
    competitors=True,                   # Aldar/Emaar/EmaarDev (in-country) from own releases
    beta_own_history_vs_egx30=False,    # tier-3 fallback — index unobtainable, 7 attempts logged
    formula_based_model=True,           # 537 formula cells; recalc + driver test green
    flags_raised_before_issue=True,     # beta interim flag, segment-level gap, EIBOR mirror
    stop_and_inform_honoured=True,      # nothing official was inaccessible for the build itself
    na_reasons={'beta_own_history_vs_egx30':
                'Own-stock regression impossible: no FTSE ADX General Index history obtainable '
                '(seven sources attempted, all logged in the bibliography); same-country peer '
                'betas need the same index. Tier-3 fallback beta=1.0 applied per the strict '
                'preference order, FLAGGED INTERIM, sensitised 0.8-1.2 in the study and priced '
                'as its own sensitivity strip. House precedent: EAND, TWOPOINTZERO.'})
assert_sigcm(sig)
print('SIGCM gate: PASS (beta tier-3 exception documented, not silent)')

chk = ModelStudyChecklist(
    structure_matches_model=True,        # 16 sections, 16 sheets, same order
    bibliography_document=True,          # standalone: primary docs, 176-input register,
                                         # judgements+overturns, negatives, discrepancies
    provenance_four_field=True,          # every input value/source/date/ring, asserted
    numeric_traceability=True,           # builders read study_numbers.json only; recalc 537/537
    external_reader_scrub=True,          # programmatic scrub, zero hits
    figure_discipline=True,              # opaque light canvases verified; rendered-image pass
    table_discipline=True,               # fixed layouts; width check across both documents
    expert_appendix_max_detail=True,     # worked tables, sensitivities, falsifiers, C.4-C.6
    contested_judgement_both_ways=True)  # sales path base vs run-off, side by side everywhere
assert_model_study(chk)
print('Model-study depth bar: PASS (all eight standards attested with evidence)')
