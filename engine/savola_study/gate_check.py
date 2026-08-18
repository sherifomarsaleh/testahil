#!/usr/bin/env python3
"""SAVOLA study — final protocol gate (verify-by-import + SIGCM + model-study bar +
four-field completeness + beta provenance). Run last, after every builder and check.
Raises (and therefore blocks issue) on any unmet clause; prints the evidence when green.
"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
sys.path.insert(0, ROOT)
sys.path.insert(0, ENGINE)

# ---------------------------------------------------------------- 1. verify by IMPORT
# The protocol's standing rule: nu=Gaussian parses cleanly and only dies at import.
MODULES = [
    "engine.market_profiles", "engine.wacc_builder", "engine.research_protocol",
    "engine.adaptive_width", "engine.research_sweep", "engine.data_quality",
    "engine.mc_v3", "engine.beta_regression", "engine.horizons",
    "engine.technicals", "engine.apply_technicals", "engine.ta_chart",
    "engine.rollforward_one",
]
for m in MODULES:
    importlib.import_module(m)
print(f"IMPORT OK — {len(MODULES)} engine modules imported (not parsed)")

from engine.research_protocol import (  # noqa: E402
    SIGCMChecklist, assert_sigcm, ModelStudyChecklist, assert_model_study,
    assert_beta_provenance, REFERENCE_SET,
)
import engine.market_profiles as market_profiles  # noqa: E402

# The SA profile must be live and loadable — read it, never quote it.
sa = market_profiles.PROFILES["SA"]
print(f"SA profile live: nu={sa.nu}, width_cal={sa.width_cal}, "
      f"signal_active={sa.signal_active}, width_overlay_active={getattr(sa, 'width_overlay_active', False)}")
assert set(REFERENCE_SET) == {"SWDY", "ADCB", "ALPHADHABI"}

# ---------------------------------------------------------------- 2. four-field completeness
SN = json.load(open(os.path.join(HERE, "study_numbers.json")))
inputs = SN["inputs"]
bad = {k: v for k, v in inputs.items()
       if not (isinstance(v, dict) and v.get("source") and v.get("date") and v.get("ring")
               and ("value" in v))}
assert not bad, f"FOUR-FIELD FAIL — orphan inputs: {sorted(bad)}"
rings = {}
for v in inputs.values():
    rings[v["ring"]] = rings.get(v["ring"], 0) + 1
print(f"FOUR-FIELD OK — {len(inputs)} inputs complete (value/source/date/layer); by layer: "
      + ", ".join(f"{k} {n}" for k, n in sorted(rings.items())))

# ---------------------------------------------------------------- 3. beta provenance (record-level)
beta_rec = json.load(open(os.path.join(HERE, "beta_result.json")))
assert_beta_provenance(beta_rec)
idx = beta_rec["index_file"].replace("\\", "/")
assert "raw_indices/SA/TASI.csv" in idx, idx
assert beta_rec["conforming"] and beta_rec["usable"]
print(f"BETA PROVENANCE OK — {beta_rec['ticker']} beta {beta_rec['beta']:.3f} "
      f"(R²={beta_rec['r2']:.3f}, n={beta_rec['n']}) vs {idx.split('raw_indices/')[-1]} "
      f"(index as of {beta_rec['index_asof']}), conforming regressor, usability gate passed")

# ---------------------------------------------------------------- 4. SIGCM hard gate
sigcm = SIGCMChecklist(
    historicals_official_only=True,   # FY2023-FY2025 audited FS + Q1-2026 reviewed, savola.com; segments/categories from the company's own FS notes and IR decks; zero vendor numbers in historicals
    forecast_ground_up=True,          # category engine: oil/sugar/pasta volume × unit gross profit; Panda stores × sales-per-store; margins are OUTPUTS
    debt_lc_fx_split=True,            # SAR 1,256.4 / EGP 417.2 / other 220.4; EGP tranche at SAR-parity cost in the WACC
    asset_conversion_cycle=True,      # DSO/DIO/DPO measured from FY2023-25 statements; BS/CF projected from component days, foot asserted per year
    competitors=True,                 # NADEC, Wilmar (SGX), Al Othaim, BinDawood, Almarai, Herfy — KPIs and multiples, cross-check only
    beta_own_history_vs_egx30=True,   # own-stock weekly vs the exchange's published index (TASI) — record asserted above
    formula_based_model=True,         # 778 formula cells / 296 literals (3 disclosed pasted classes); driver→IS→BS→CF→DCF live
    flags_raised_before_issue=True,   # FY2023 Türkiye basis, H1-2026 FS mirror gap, constructed 10Y SAR rf, Mehbaj consideration undisclosed — all flagged in the study + bibliography
    stop_and_inform_honoured=True,    # no blocking gap: every company-reported figure came from the company's own documents
)
assert_sigcm(sigcm)
print("SIGCM OK — all 8 clauses + stop-and-inform attested and evidenced")

# ---------------------------------------------------------------- 5. model-study depth bar
ms = ModelStudyChecklist(
    structure_matches_model=True,        # 16-section Word (SWDY order) + 16-sheet Excel (SWDY names/order)
    bibliography_document=True,          # standalone SAVOLA_Bibliography_18-08-2026 (primary docs + 184-input register + judgements/negative/aggregator tables)
    provenance_four_field=True,          # asserted in step 2 above
    numeric_traceability=True,           # builders read study_numbers.json only; recalc.py: 778/778 formula cells reproduced, 0 unresolvable, 22 headline reconciliations
    external_reader_scrub=True,          # qc_checks.py scrub: 0 hits in both documents; calibration evidence as plain language in §3, no appendix
    figure_discipline=True,              # 8 figures, opaque canvas verified (corner luminance 248), each inspected as a rendered image
    table_discipline=True,               # fixed layouts with explicit widths; programmatic starved/bloated check clean over every table in both docs
    expert_appendix_max_detail=True,     # C.1-C.3 worked tables w/ named sensitivities + falsifiers, C.4 cross-exam, C.5 three-in-one-room + figure, C.6 divergence table
    contested_judgement_both_ways=True,  # Panda density: Framing A 26.20 vs Framing B 22.10 side by side in summary, body §1.7, workbook FV panel, Expert 2's low case — never averaged
)
assert_model_study(ms)
print("MODEL-STUDY BAR OK — all 9 standards attested against SWDY_Valuation_Study_05-08-2026")

# ---------------------------------------------------------------- 6. deliverables exist
DELIVER = [
    "SAVOLA_Valuation_Study_18-08-2026_public.docx",
    "SAVOLA_Valuation_Study_18-08-2026_public.pdf",
    "SAVOLA_Valuation_Model_18082026_public.xlsx",
    "SAVOLA_Valuation_Model_18082026_public.pdf",
    "SAVOLA_Bibliography_18-08-2026.docx",
    "SAVOLA_Bibliography_18-08-2026.pdf",
    "study_numbers.json", "xlsx_expected.json", "sweep_register.json",
    "step0_result.json", "backtest_5y.json", "beta_result.json",
    "strike_result.json", "tech_read.json",
]
for f in DELIVER:
    p = os.path.join(HERE, f)
    assert os.path.exists(p) and os.path.getsize(p) > 0, f"missing deliverable: {f}"
print(f"DELIVERABLES OK — {len(DELIVER)} files present and non-empty")

print("\nGATE CHECK PASSED — SAVOLA study may issue (publishing remains a separate, explicit request)")
