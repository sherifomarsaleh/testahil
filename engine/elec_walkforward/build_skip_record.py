#!/usr/bin/env python3
"""ELEC — the SKIP record: what a run that scored nothing nonetheless measured.

A SKIP is one of [R-FCAL-01]'s three scopes and a completed queue position, not a
deferred one. It still MEASURES things — how much history the archive holds, whether
the issuer serves it, whether the study's own panel reconciles to it — and those
measurements are what a lesson can legitimately be harvested from. They are written
here, mechanically, from filed_record.py, so nothing in a lesson's evidence clause is
typed by hand.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import filed_record as F                                          # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
STUDY = json.load(open(os.path.join(ROOT, "engine/elec_study/study_numbers.json"),
                       encoding="utf-8"))
OUT = os.path.join(HERE, "skip_record.json")
YS = ("FY2020", "FY2021", "FY2022", "FY2023")


def main():
    hs = STUDY["hist_is"]
    f23 = F.IS[("FY2023", "standalone")]
    w = F.consolidation_wedge()
    ul = F.implied_useful_life()
    foot = F.footing_report()
    margins = {y: F.ebitda(y) / F.IS[(y, "standalone")]["rev"] for y in YS}
    study_margins = {y: hs[y]["ebitda"] / hs[y]["rev"] for y in ("FY23", "FY24", "FY25")}

    rec = {
        "ticker": "ELEC", "built": "2026-09-07", "scope": "skip",
        "scope_words": "walk-forward not run — insufficient sourceable history (4 years)",

        "sourceable_years": {
            "consolidated": 2, "standalone": 4, "required_for_light": 5,
            "scoreable_origins": 0,
            "why_zero_origins": "the last sourceable actual is FY2023, so the last "
                                "possible origin is FY2022 at h=1, and FY2022 needs "
                                "five years of history to it (FY2018-FY2022) which do "
                                "not exist on any basis in hand",
        },

        # RE-PROBED 09-09-2026 AND ONE FIELD OF THE FIRST PROBE WAS WRONG.
        #
        # The 07-09 probe recorded dead_host_resolves False and stopped there. The host
        # RESOLVES — https://www.ececables.com answers 200 with a rebuilt WordPress site.
        # What is dead is the UPLOADS: every statement URL the old index pointed at now
        # 404s against a page of HTML, which is the failure that reads as a dead host to
        # anything checking a status code and not a content type. Correcting it matters
        # because the wrong reason is the recoverable one, and a later session reading
        # "dead host" would try the archive, find statements, and think the skip was
        # premature. It is not, and the paragraph below is why.
        #
        # THE ARCHIVE ROUTE WAS THEN WALKED TO ITS END RATHER THAN SAMPLED. All 926
        # unique ececables.com URLs the Wayback CDX index holds were enumerated, not the
        # 61 the issuer's own index listed. The result is decisive in both directions:
        #   * ZERO consolidated statements were ever archived, at any date. Every
        #     recoverable statement is standalone (القوائم المالية المستقلة). The
        #     consolidation wedge below is therefore not closable from any public source
        #     — 1.73x revenue and 34.5x operating profit at the FY2020 overlap.
        #   * ZERO filings of ANY basis exist for 2018, 2019 or 2020. The archive holds
        #     2013-2017 on the retired /download/ path and 2021-2023 under wp-content,
        #     with a three-year hole between them.
        # The hole falls exactly where the origins would be. FY2022 at h=1 needs
        # FY2018-FY2022, so the missing years are not a thinner sample, they are the
        # reason the sample is empty. THE SKIP IS NOT A SOURCING EFFORT NOT YET MADE;
        # it is a sourcing effort completed with a negative result [R-ENF-04].
        "issuer_archive": {
            "probed": "2026-09-07", "reprobed": "2026-09-09", "index_http": 200,
            "statement_files_listed": 61,
            "on_live_host": 19, "fetchable_on_live_host": 0,
            "on_dead_host": 42,
            "dead_host_resolves": True,
            "dead_host_correction": "the host resolves; the uploads 404 into HTML. The "
                                    "07-09 field was wrong and the wrong reason was the "
                                    "recoverable one.",
            "index_last_period": "2025-09-30",
            "consolidated_files_all_on_dead_host": True,
            "last_consolidated_statement_issued": "FY2020",
            "wayback_urls_enumerated": 926,
            "wayback_consolidated_statements": 0,
            "wayback_filings_2018_2019_2020": 0,
            "wayback_recoverable_basis": "standalone only, 2013-2017 and 2021-2023",
            "recovery_route_closed": True,
        },

        "footing": {"checks": len(foot),
                    "refusals": sum(1 for _, c, p in foot
                                    if abs(c - p) > max(1.0, abs(p) * 1e-9)),
                    "route": "OCR/pixel off the rendered pages; no filing carries a "
                             "usable text layer and three of four are truncated"},

        "consolidation_wedge_at_overlap": {
            "year": w["year"],
            "revenue": w["revenue"]["factor"],
            "operating_profit": w["operating_profit"]["factor"],
            "net_profit": w["net_profit"]["factor"],
        },

        "study_panel_vs_filed_FY2023": {
            "revenue": hs["FY23"]["rev"] * 1e6 / f23["rev"],
            "ebitda": hs["FY23"]["ebitda"] * 1e6 / F.ebitda("FY2023"),
            "net_profit": hs["FY23"]["np"] * 1e6 / f23["np"],
            "revenue_consistent_with_wedge": abs(
                hs["FY23"]["rev"] * 1e6 / f23["rev"] - w["revenue"]["factor"]) < 0.15,
            "profit_beyond_wedge_by": (hs["FY23"]["np"] * 1e6 / f23["np"])
                                      / w["net_profit"]["factor"],
        },

        "claimed_filed_record": {
            "claimed_range": [min(study_margins.values()), max(study_margins.values())],
            "claimed_source_in_audit": "this company's own reconstructed filed record",
            "actual_source": "the study's own committed hist_is, which is vendor data; "
                             "no filing exists for FY2024 or FY2025 at all",
            "true_filed_range_standalone": [min(margins.values()), max(margins.values())],
            "study_terminal_forecast": 0.1230,
            "terminal_inside_true_filed_range":
                min(margins.values()) <= 0.1230 <= max(margins.values()),
            "premise_withdrawn": True,
            "reverse_read_implied": 0.2717,
            "reverse_read_over_highest_filed": 0.2717 / max(margins.values()),
        },

        "useful_life": {
            "route_1_succeeded": False,
            "route_1_outcome": "spans only (10-50, 4-25, 5-20, 5-20, 5, 5-10); no "
                               "dominant class, no weighting",
            "route_2_years_band": [ul["years_excluding_fully_depreciated"],
                                   ul["years_on_full_base"]],
            "route_2_prior_year_control": ul["prior_year_control"],
            "fully_depreciated_share_of_base":
                F.FIXED_ASSET_NOTE_FY2023["fully_depreciated_still_in_use"]
                / ul["depreciable_gross_cost"],
        },

        "trap_i": {y: F.borrowing_rate_check(y)
                   for y in ("FY2021", "FY2022", "FY2023")},
        "trap_i_broad_denominator_below_sovereign_years": sum(
            1 for y in ("FY2021", "FY2022", "FY2023")
            if F.borrowing_rate_check(y)["rate_on_total_liabilities"] < 0.09),

        "filings_truncated": 3, "filings_held": 4,
        "study_share_count_mn": STUDY["shares"],
        "filed_share_count_mn": F.shares("FY2023") / 1e6,
    }
    json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", OUT)
    return rec


if __name__ == "__main__":
    r = main()
    print("  sourceable standalone years : %d (need %d)"
          % (r["sourceable_years"]["standalone"],
             r["sourceable_years"]["required_for_light"]))
    print("  scoreable origins           : %d" % r["sourceable_years"]["scoreable_origins"])
    print("  footing refusals            : %d of %d"
          % (r["footing"]["refusals"], r["footing"]["checks"]))
    print("  terminal inside filed range : %s"
          % r["claimed_filed_record"]["terminal_inside_true_filed_range"])
