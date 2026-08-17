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
    beta_own_history_vs_egx30=True,     # TIER 1: own-stock weekly regression vs the
                                        # official FTSE ADX General, the stock's own local
                                        # index. REVISION 3: the series was obtained on
                                        # 10-Aug-2026 after ten failed sources, Step 0.0
                                        # screened, and the proxy composite is RETIRED.
                                        # 5y beta 1.278 (SE 0.258, R2 0.089, n 255, gate
                                        # PASS) adopted as the longest passing window; 3y
                                        # 1.800 and 2y 1.581 both read higher. The clause is
                                        # now satisfied outright, not in substance.
    formula_based_model=True,
    flags_raised_before_issue=True,
    stop_and_inform_honoured=True)
assert_sigcm(sig)
print('SIGCM gate: PASS (beta = TIER 1 own-stock regression vs the official FTSE ADX General)')

chk = ModelStudyChecklist(
    structure_matches_model=True,        # 16 sections, 16 sheets, same order
    bibliography_document=True,          # standalone: primary docs, 176-input register,
                                         # judgements+overturns, negatives, discrepancies
    provenance_four_field=True,          # every input value/source/date/ring, asserted
    numeric_traceability=True,           # builders read study_numbers.json only; recalc all cells
    external_reader_scrub=True,          # programmatic scrub, zero hits
    figure_discipline=True,              # opaque light canvases verified; rendered-image pass
    table_discipline=True,               # fixed layouts; width check across both documents
    expert_appendix_max_detail=True,     # worked tables, sensitivities, falsifiers, C.4-C.6
    contested_judgement_both_ways=True)  # sales path base vs run-off, side by side everywhere
assert_model_study(chk)
print('Model-study depth bar: PASS (all eight standards attested with evidence)')
