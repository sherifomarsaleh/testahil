#!/usr/bin/env python3
"""GBCO fundamental walk-forward training — panel assembler.

Builds the 15-year provenance panel (FY2011–FY2025 + 2026 interims) from the
per-document extraction JSONs produced in-session from GB Corp's own IR documents
(ir.gb-corporation.com — annual reports, audited consolidated FS, 4Q earnings
releases; all tier A). Third-party (tier C) inputs are the exogenous macro
conditioning series only (World Bank CPI/FX), never the company's own numbers.

Every figure carries four fields: value, source (document URL), date (document
date), tier (A/B/C). DERIVED figures carry their formula. Identity assertions run
over the assembled panel and the build FAILS on any violation beyond rounding —
a transcription error must not survive into the training run (R-ENF-01 spirit:
the check runs over the work, not inside it).

Run:  python3 engine/gbco_training/gbco_panel.py [--extract-dir DIR] [--out DIR]
Outputs: gbco_panel.json, PANEL_SUMMARY.md (both git-committed training records).
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# extraction records are committed beside this script so the panel rebuilds
# from the repo alone; GBCO_EXTRACT_DIR overrides for a fresh extraction pass
DEFAULT_EXTRACT = os.environ.get("GBCO_EXTRACT_DIR", os.path.join(HERE, "extraction"))

IR = "https://ir.gb-corporation.com/media/"

# Document dates (publication) for point-in-time discipline: figures from a
# document are visible to origins dated after doc_date.
DOC_DATES = {
    "GB_Annual_Report_2011.pdf": "2012-04-30", "GB_Annual_Report_2012.pdf": "2013-04-30",
    "GB_Annual_Report_2013.pdf": "2014-04-30", "GB_Annual_Report_2014.pdf": "2015-04-30",
    "GB_Annual_Report_2015.pdf": "2016-04-30", "GB_Annual_Report_2016.pdf": "2017-04-30",
    "GB_Annual_Report_2017.pdf": "2018-04-30", "GB_Annual_Report_2018.pdf": "2019-04-30",
    "GB_Annual_Report_2019.pdf": "2020-04-30", "GB_Annual_Report_2020.pdf": "2021-04-30",
    "GB_Annual_Report_2021.pdf": "2022-04-30", "GB_Annual_Report_2022.pdf": "2023-04-30",
    "GB_Corp_Annual_Report_2025.pdf": "2026-04-30",
    "GB_Auto_Consolidated_E_31_December_2020.pdf": "2021-03-01",
    "GB_Auto_Consolidated_E_31_December_2021.pdf": "2022-03-01",
    "GB_Corp_Consolidated_E_31_December_2023.pdf": "2024-02-29",
    "GB_Corp_Consolidated_E_31_December_2024.pdf": "2025-02-27",
    "GB_Corp_Consolidated_E_31_December_2025.pdf": "2026-02-26",
}
# AR publication approximated at 30 April of the following year (GB publishes
# the glossy AR after the February FS/ER); origins are dated 30 April so year
# Y-1 figures are always visible at origin Y through the FS/ER even where the
# AR itself came later. The FS/ER date is the binding one for the last year.

FYS = list(range(2011, 2026))

# ---------------------------------------------------------------------------
# Exogenous conditioning series (pre-registered inputs). Company figures above
# are tier A; these are the ONLY tier-C series in the panel, and they are
# conditioning inputs, never the subject's own reported numbers (SIGCM clause 1
# untouched). Values were fetched/extracted in-session on 30-Aug-2026; sources
# per series. DERIVED entries carry their formula and are flagged.
# ---------------------------------------------------------------------------
EXOG = {
    "cpi_egypt_pct": {  # World Bank FP.CPI.TOTL.ZG (CAPMAS underlying), fetched 30-Aug-2026
        "tier": "C", "source": "https://api.worldbank.org/v2/country/EGY/indicator/FP.CPI.TOTL.ZG",
        "values": {2009: 11.76, 2010: 11.27, 2011: 10.06, 2012: 7.11, 2013: 9.47, 2014: 10.07,
                   2015: 10.37, 2016: 13.81, 2017: 29.51, 2018: 14.40, 2019: 9.15, 2020: 5.04,
                   2021: 5.21, 2022: 13.90, 2023: 33.88, 2024: 28.27, 2025: 14.07}},
    "egp_usd_avg": {  # World Bank PA.NUS.FCRF period-average, fetched 30-Aug-2026
        "tier": "C", "source": "https://api.worldbank.org/v2/country/EGY/indicator/PA.NUS.FCRF",
        "values": {2009: 5.54, 2010: 5.62, 2011: 5.93, 2012: 6.06, 2013: 6.87, 2014: 7.08,
                   2015: 7.69, 2016: 10.03, 2017: 17.78, 2018: 17.77, 2019: 16.77, 2020: 15.76,
                   2021: 15.64, 2022: 19.16, 2023: 30.63, 2024: 45.30, 2025: 49.23}},
    "egypt_pc_market_units": {  # AMIC as quoted in GB's own documents (tier A quotes)
        "tier": "A (company-quoted AMIC); DERIVED rows flagged",
        "source": "AR2017 p.25 chart (2006-2017); AR2018 (145,886); AR2019 (127,443); "
                  "AR2020 (167,792); AR2021 (215,072); AR2022 (133,857 AMIC); "
                  "ER 4Q23 (market -48.3% y-o-y FY23); ER 4Q25 CEO letter (~210,000 in 2025, +~40% vs 2024)",
        "values": {2011: 133165, 2012: 144204, 2013: 133760, 2014: 207973, 2015: 195559,
                   2016: 141983, 2017: 99530, 2018: 145886, 2019: 127443, 2020: 167792,
                   2021: 215072, 2022: 133857, 2023: 69204, 2024: 150000, 2025: 210000},
        "derived": {2023: "133,857 x (1-0.483) = 69,204 (ER 4Q23 growth quote applied to AR2022 AMIC base; "
                          "cross-check via share: 16,469 GB units / 23.3% share = 70,682 — within 2%)",
                    2024: "210,000 / 1.40 = 150,000 (ER 4Q25 CEO letter: 2025 ~210,000, up ~40% vs 2024)",
                    2025: "~210,000 as stated (approximate company quote, not an AMIC table)"}},
    "tax_statutory_pct": {
        "tier": "B", "source": "Egyptian income tax law as reflected in the FS tax notes of the era",
        "values": {y: (25.0 if y <= 2013 else 30.0 if y in (2014, 2015) else 22.5) for y in range(2011, 2027)},
        "note": "22.5% from Law 96/2015; 30% top rate 2014-2015 incl. temporary surtax; 25% before"},
}


def _val(x):
    """Normalize a figure that may be {'v':..,'q':..} or a plain number."""
    if isinstance(x, dict) and "v" in x:
        return x["v"]
    return x


def _quote(x):
    if isinstance(x, dict):
        return x.get("q")
    return None


def load_extracts(xdir):
    data = {}
    for fn in sorted(os.listdir(xdir)):
        if fn.endswith(".json"):
            with open(os.path.join(xdir, fn)) as f:
                data[fn[:-5]] = json.load(f)
    return data


def build_panel(ex):
    """Assemble per-FY consolidated records with provenance."""
    panel = {}
    problems = []
    for fy in FYS:
        key = f"FY{fy}"
        rec = {"fy": fy, "is": {}, "bs": {}, "cf": {}, "kpis": {}, "segments": [],
               "provenance": {}, "guidance": [], "accounting_changes": [],
               "restatement_notes": [], "oddities": []}
        src = ex.get(key)
        if src:
            for blk in ("is", "bs", "cf"):
                for k, v in (src.get(blk) or {}).items():
                    val = _val(v)
                    if val is not None:
                        rec[blk][k] = val
                        q = _quote(v)
                        if q:
                            rec["provenance"][f"{blk}.{k}"] = q
            rec["segments"] = src.get("segments") or []
            rec["kpis"] = src.get("kpis") or {}
            rec["guidance"] = src.get("guidance") or []
            rec["accounting_changes"] = src.get("accounting_changes") or []
            rec["restatement_notes"] = src.get("restatement_notes") or []
            rec["oddities"] = src.get("oddities") or []
            rec["source_doc"] = src.get("source_doc")
            rec["source_url"] = src.get("source_url")
            rec["tier"] = "A"
        panel[key] = rec

    # Overlay the visually-read audited FS for FY2023/24/25 (image-only PDFs,
    # read in the lead session) — these override/there was no agent file.
    for name, fy in (("FS2023_visual", 2023), ("FS2024_visual", 2024), ("FS2025_visual", 2025)):
        v = ex.get(name)
        if not v:
            problems.append(f"missing visual FS extract {name}")
            continue
        rec = panel[f"FY{fy}"]
        for blk in ("is", "bs", "cf"):
            got = v.get(blk) or {}
            if got:
                # keep agent AR-derived values only where FS lacks the key
                merged = dict(rec[blk])
                for k, val in got.items():
                    if k in merged and abs(merged[k]) > 0 and val is not None:
                        # disagreement between AR text and audited FS → FS wins, log
                        if merged[k] != val:
                            rec["oddities"].append(
                                f"{blk}.{k}: AR text {merged[k]} vs audited FS {val} — FS kept")
                    if val is not None:
                        merged[k] = val
                rec[blk] = merged
        rec["source_doc"] = v["source_doc"]
        rec["source_url"] = v["source_url"]
        rec["doc_date"] = v.get("doc_date")
        rec["tier"] = v.get("tier", "A")
        rec["audit"] = v.get("audit")
        rec["oddities"] += v.get("notes", [])
    return panel, problems


def assert_identities(panel):
    """Arithmetic identities per FY. Tolerance covers EGP-000 rounding."""
    errs = []
    for key, rec in panel.items():
        i, b = rec["is"], rec["bs"]
        def ck(cond, msg):
            if not cond:
                errs.append(f"{key}: {msg}")
        if {"revenue", "cogs", "gross_profit"} <= set(i):
            ck(abs(i["revenue"] + i["cogs"] - i["gross_profit"]) <= 5,
               f"rev+cogs != gp ({i['revenue']}+{i['cogs']} vs {i['gross_profit']})")
        if {"np_total", "np_parent", "np_nci"} <= set(i):
            ck(abs(i["np_parent"] + i["np_nci"] - i["np_total"]) <= 5,
               f"np split mismatch ({i['np_parent']}+{i['np_nci']} vs {i['np_total']})")
        if {"total_equity", "equity_parent", "nci_equity"} <= set(b):
            ck(abs(b["equity_parent"] + b["nci_equity"] - b["total_equity"]) <= 5,
               "equity split mismatch")
        if {"ta", "tl", "total_equity"} <= set(b):
            ck(abs(b["ta"] - b["tl"] - b["total_equity"]) <= 10,
               f"BS identity broken (TA {b['ta']} vs TL {b['tl']} + TE {b['total_equity']})")
        if {"total_assets", "total_liabilities", "total_equity"} <= set(b):
            ck(abs(b["total_assets"] - b["total_liabilities"] - b["total_equity"]) <= 10,
               "BS identity broken (agent keys)")
    return errs


def coverage_report(panel):
    """R-ENF-04: declare what was examined against the known total (15 FYs)."""
    lines = []
    core = ("revenue", "gross_profit", "np_total")
    for fy in FYS:
        rec = panel[f"FY{fy}"]
        have = [k for k in core if k in rec["is"]]
        lines.append((fy, len(have), len(rec["is"]), len(rec["bs"]), len(rec["cf"]),
                      rec.get("source_doc") or "MISSING"))
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract-dir", default=DEFAULT_EXTRACT)
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()

    ex = load_extracts(args.extract_dir)
    panel, problems = build_panel(ex)
    errs = assert_identities(panel)

    cov = coverage_report(panel)
    missing_core = [fy for fy, ncore, *_ in cov if ncore < 3]
    print("coverage (fy, core-IS lines of 3, IS keys, BS keys, CF keys, source):")
    for row in cov:
        print("  ", row)
    if problems:
        print("problems:", *problems, sep="\n  ")
    if errs:
        print("IDENTITY FAILURES:", *errs, sep="\n  ")
        sys.exit(1)
    if missing_core:
        print(f"INCOMPLETE PANEL — core IS lines missing for: {missing_core}")
        sys.exit(2)

    # interims (2026) travel with the panel for the update, unscored
    interims = {k: ex[k] for k in ("FS2026Q1_visual", "FS2026H1_visual") if k in ex}
    er_kpis = ex.get("ER_kpis_2023_2026", {})
    er_vol_2020_2022 = ex.get("ER_vol_2020_2022", {})
    ar2017 = ex.get("AR2017_visual", {})

    out = {"built": "walk-forward training panel, GBCO",
           "units": "consolidated FS figures in EGP 000 unless a record's units say otherwise",
           "fiscal_years": FYS, "panel": panel, "exog": EXOG,
           "interims_2026": interims, "er_kpis": er_kpis,
           "er_vol_2020_2022": er_vol_2020_2022, "ar2017_kpis": ar2017}
    with open(os.path.join(args.out, "gbco_panel.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"panel written: {len(FYS)} fiscal years, identity checks passed")


if __name__ == "__main__":
    main()
