"""PHDC — the three standing gates, filled honestly.

This study is NOT ISSUABLE at this build date and this file is what says so in
code rather than in prose. The analytical core is complete and sourced; the
delivered artefacts required by the model-report depth bar are not built, and
the cash leg of the forecast sits at the coarsest level on the ground-up ladder
because the company does not disclose its collection schedule.

Running this module prints the gate results. assert_model_study() is EXPECTED to
raise; that is the correct outcome, not a bug, and PHDC is registered in
engine/build_depth_audit/outstanding.json for exactly that reason.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, HERE)

import research_protocol as RP
import beta_regression as BR
import inputs as IN

STANDARD_BUILT_AGAINST = RP.STANDARD_VERSION


def beta_gate():
    rec = BR.own_stock_beta("PHDC", "EG", "EGX")
    RP.assert_beta_provenance(rec)          # raises unless the regressor is published
    return rec


def ground_up_record():
    """Per revenue line: physical unit, disclosure, price basis, cost basis.

    PHDC runs one revenue line — residential and commercial property sold
    off-plan and recognised on completion. It is recorded at SEGMENT level, not
    unit, and the gap note says why: the company discloses new sales, units sold
    and units delivered in aggregate and by region, but publishes no per-project
    unit mix, average unit area, price per square metre or construction cost per
    square metre. The 11-Jun-2026 edition carried a full table of those figures;
    they are not sourced to any company document and are not reused here.
    """
    DL = RP.DriverLine
    return [DL(
        name="Property development (residential and commercial)",
        share_of_revenue=1.0,
        level="segment",
        unit="EGP of contracted value recognised on completion",
        unit_source=("PHD results releases disclose new sales in EGP and units sold, "
                     "total and by region, and units delivered; PHD consolidated "
                     "statements disclose revenue, cost of revenue and work in "
                     "progress. FY2011-FY2025 assembled in engine/phdc_walkforward."),
        price_basis=("Realised revenue per period from the audited statements; gross "
                     "margin is an OUTPUT of price against cost on the same completion "
                     "clock, never an input."),
        cost_basis=("Cost of revenue from the audited statements, recognised on the "
                    "SAME completion schedule as revenue — the correction the "
                    "walk-forward training run earned on this company's history."),
        gap_note=("SEGMENT, not unit. No per-project unit mix, unit area, price per "
                  "sqm or construction cost per sqm is disclosed anywhere by the "
                  "company, so unit economics cannot be built without inventing them. "
                  "Separately, the CASH leg is coarser still — TOPDOWN — because the "
                  "collection schedule (down payment, instalment tenor, post-handover "
                  "tail) is undisclosed; cash conversion is measured from three years "
                  "of disclosed cash-flow statements instead, and it is the study's "
                  "crux."),
    )]


def sigcm_checklist():
    return RP.SIGCMChecklist(
        historicals_official_only=True,
        forecast_ground_up=True,        # attested on the record above, not on this flag
        debt_lc_fx_split=True,
        asset_conversion_cycle=True,
        competitors=False,
        formula_based_model=True,
        beta_own_history_vs_egx30=True,
        flags_raised_before_issue=True,
        stop_and_inform_honoured=True,
        na_reasons={},
    )


def model_study_checklist():
    return RP.ModelStudyChecklist(
        provenance_four_field=True,
        numeric_traceability=True,
        structure_matches_model=False,
        bibliography_document=False,
        external_reader_scrub=False,
        figure_discipline=False,
        table_discipline=False,
        expert_appendix_max_detail=False,
        contested_judgement_both_ways=True,
        na_reasons={},
    )


def main():
    out = {"standard_version": STANDARD_BUILT_AGAINST, "gates": {}}

    rec = beta_gate()
    out["gates"]["assert_beta_provenance"] = {
        "result": "PASS",
        "evidence": ("beta %.4f against %s (as-of %s), R^2 %.1f%%, SE %.4f, n=%d "
                     "weekly, usable=%s, conforming=%s"
                     % (rec["beta"], rec["index_file"], rec["index_asof"],
                        rec["r2"] * 100, rec["se"], rec["n"], rec["usable"],
                        rec["conforming"]))}

    gu = RP.assert_ground_up(ground_up_record(), ticker="PHDC")
    out["gates"]["assert_ground_up"] = {"result": "PASS", "evidence": gu}

    try:
        RP.assert_sigcm(sigcm_checklist())
        out["gates"]["assert_sigcm"] = {"result": "PASS"}
    except AssertionError as e:
        out["gates"]["assert_sigcm"] = {"result": "FAIL", "detail": str(e)}

    try:
        RP.assert_model_study(model_study_checklist())
        out["gates"]["assert_model_study"] = {"result": "PASS"}
    except AssertionError as e:
        out["gates"]["assert_model_study"] = {
            "result": "FAIL — EXPECTED AT THIS BUILD DATE", "detail": str(e)}

    out["issuable"] = all(g["result"] == "PASS" for g in out["gates"].values())
    json.dump(out, open(os.path.join(HERE, "gate_result.json"), "w"), indent=1,
              default=str)
    for k, v in out["gates"].items():
        print("%-28s %s" % (k, str(v["result"])[:60]))
        if "detail" in v:
            print("      %s" % v["detail"][:300])
    print("\nISSUABLE: %s" % out["issuable"])
    if not out["issuable"]:
        print("This study must NOT be issued. The analytical core is complete and "
              "sourced;\nthe delivered artefacts the depth bar requires are not built.")
    return out


if __name__ == "__main__":
    main()
