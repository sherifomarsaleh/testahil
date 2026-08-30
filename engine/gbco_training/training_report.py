#!/usr/bin/env python3
"""GBCO walk-forward training — report generator.

Reads the scored cells (errors_by_line.csv), the panel, and corrections_test.json;
writes PANEL_SUMMARY.md, guidance_ledger.md, decompositions.csv, np_ex table, and
assembles the driver-level summary used by TRAINING_RECORD.md. Pure reporting —
no model logic here; bottom_up.py owns every forecast.
"""
import csv
import json
import math
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))

# B7 one-offs (EGP mn, effect ON reported NP; sign = what to REMOVE)
ONE_OFFS_NP = {2022: +8207.309,   # MNT-Halan deconsolidation/sale gain (essentially untaxed)
               2023: -522.0}      # Algeria full impairment (pre-tax; conservative: no tax shield)


def load_rows():
    with open(os.path.join(HERE, "errors_by_line.csv")) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("origin", "fy", "h", "crosses_B4"):
            r[k] = int(r[k])
        for k in ("forecast", "actual", "log_err", "scaled_err", "freeze_err",
                  "trend_err", "log_err_realized_macro"):
            r[k] = float(r[k]) if r[k] not in ("", None) else None
    return rows


def np_ex_table(rows):
    """NP scored with registered one-offs removed from the actual (model never
    forecasts one-offs, so the forecast side is already ex-one-off)."""
    out = []
    for r in rows:
        if r["line"] != "np":
            continue
        adj = ONE_OFFS_NP.get(r["fy"], 0.0)
        a_ex = (r["actual"] - adj) if r["actual"] is not None else None
        e = None
        if r["forecast"] and a_ex and r["forecast"] > 0 and a_ex > 0:
            e = math.log(r["forecast"] / a_ex)
        out.append({"origin": r["origin"], "fy": r["fy"], "h": r["h"],
                    "np_forecast": r["forecast"], "np_actual_reported": r["actual"],
                    "np_actual_ex_oneoff": a_ex, "log_err_reported": r["log_err"],
                    "log_err_ex_oneoff": e})
    return out


def decompositions(rows):
    """Revenue and NP error bridges at h1 per origin (level differences)."""
    by = {}
    for r in rows:
        by[(r["origin"], r["fy"], r["line"])] = r
    out = []
    for Y in sorted({r["origin"] for r in rows}):
        fy = Y  # h1
        def d(line):
            r = by.get((Y, fy, line))
            if r and r["forecast"] is not None and r["actual"] is not None:
                return r["forecast"] - r["actual"]
            return None
        rev_d = d("rev")
        comp = {c: d(c) for c in ("pc_rev", "m3w_rev", "cv_rev", "fin_rev", "resid_rev")}
        np_d = d("np")
        np_bridge = {"gp": d("gp"),
                     "sga": (-d("sga")) if d("sga") is not None else None,
                     "fin": d("fin"),
                     "assoc": (by.get((Y, fy, "assoc")) or {}).get("forecast"),
                     "tax": d("tax")}
        out.append({"origin": Y, "h1_fy": fy, "rev_gap": rev_d, **{f"rev_gap_{k}": v for k, v in comp.items()},
                    "np_gap": np_d, **{f"np_gap_{k}": v for k, v in np_bridge.items() if k != "assoc"}})
    return out


def guidance_ledger(pj):
    """Management guidance vs outcome. Quantitative items graded from the panel;
    qualitative items listed ungraded. Sources: AR/ER outlook sections captured
    verbatim in the extraction JSONs (see panel guidance fields)."""
    mkt = {int(k): v for k, v in pj["exog"]["egypt_pc_market_units"]["values"].items()}
    items = [
        {"stated": "AR2013 outlook: continued growth expected in 2014 across lines (verbatim quotes in panel FY2013.guidance)",
         "vintage": 2013, "for": 2014, "outcome": f"market {mkt[2014]:,} (+55.5%); GB revenue +35.0%", "verdict": "directionally right"},
        {"stated": "AR2017: PC market to hit 120,000 units in 2018; GB share at least 30%",
         "vintage": 2017, "for": 2018,
         "outcome": f"market {mkt[2018]:,} (beat 120k); GB share 25.4% (AR2018)", "verdict": "market BEAT / share MISS"},
        {"stated": "AR2018 outlook for 2019 (7 quotes in panel): further recovery expected",
         "vintage": 2018, "for": 2019,
         "outcome": f"market {mkt[2019]:,} (−12.6%); GB Egypt PC volumes −27% (26,887)", "verdict": "MISS (market fell)"},
        {"stated": "AR2019 outlook for 2020 (8 quotes): growth momentum expected",
         "vintage": 2019, "for": 2020,
         "outcome": f"market {mkt[2020]:,} (+31.7%) despite COVID; GB PC volumes +10.3%", "verdict": "directionally right"},
        {"stated": "AR2020: 'exploring strategic options regards to our financing businesses'",
         "vintage": 2020, "for": 2021,
         "outcome": "MNT/Halan restructuring executed 2021-2022 (B4)", "verdict": "delivered"},
        {"stated": "ER 4Q24: Sadat factory fully operational by 4Q25, first assembly online 2Q25",
         "vintage": 2024, "for": 2025,
         "outcome": "ER 4Q25: Sadat entered a SOFT LAUNCH phase in 4Q25", "verdict": "partial — later than guided"},
        {"stated": "ER 4Q24: FY25 securitization target — exceed 13 deals, EGP 30bn total bond size",
         "vintage": 2024, "for": 2025,
         "outcome": "ER 4Q25: 17 deals, EGP 33bn, 36% market share", "verdict": "BEAT"},
        {"stated": "ER 4Q25 (for 2026): supportive macro (stabilizing FX, easing inflation, declining rates); gradual regional relief H2-26 subject to GSO enforcement; Jordan drag to subside from Q4",
         "vintage": 2025, "for": 2026,
         "outcome": "OPEN — H1-26: group revenue +35.2% y-o-y; regional still weak (NCI loss −206.4 EGP mn H1)", "verdict": "open"},
    ]
    bias_note = ("Directional record 2013-2025 from the graded items: management market-direction "
                 "calls were right in expansions and missed both contractions (2019 vintage; 2018 "
                 "share target). Capacity/product guidance (Sadat) landed late by about one "
                 "quarter-to-two; financing-business guidance (securitization, MNT strategic "
                 "options) delivered or beat. Treat management volume guidance as mildly "
                 "over-optimistic at cycle turns; treat GB Capital operational guidance as reliable.")
    return items, bias_note


def main():
    pj = json.load(open(os.path.join(HERE, "gbco_panel.json")))
    rows = load_rows()

    npx = np_ex_table(rows)
    with open(os.path.join(HERE, "np_ex_oneoffs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(npx[0].keys()))
        w.writeheader()
        w.writerows(npx)
    # summary comparison
    for h in (1, 3, 5):
        rep = [r["log_err_reported"] for r in npx if r["h"] == h and r["log_err_reported"] is not None]
        ex = [r["log_err_ex_oneoff"] for r in npx if r["h"] == h and r["log_err_ex_oneoff"] is not None]
        if rep and ex:
            print(f"np h{h}: reported bias {st.mean(rep):+.3f} (n={len(rep)}) | "
                  f"ex-one-off bias {st.mean(ex):+.3f} (n={len(ex)})")

    dec = decompositions(rows)
    with open(os.path.join(HERE, "decompositions.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(dec[0].keys()))
        w.writeheader()
        w.writerows(dec)

    items, bias_note = guidance_ledger(pj)
    with open(os.path.join(HERE, "guidance_ledger.md"), "w") as f:
        f.write("# GBCO — guidance ledger (management guidance vs outcome)\n\n")
        f.write("Sources: outlook/CEO-letter quotes captured verbatim in the extraction "
                "JSONs referenced by gbco_panel.json (panel[FY].guidance), graded against "
                "the panel actuals. Never used as a driver at historical origins.\n\n")
        f.write("| vintage | for | guidance | outcome | verdict |\n|---|---|---|---|---|\n")
        for it in items:
            f.write(f"| {it['vintage']} | {it['for']} | {it['stated']} | {it['outcome']} | {it['verdict']} |\n")
        f.write(f"\n{bias_note}\n")

    # panel summary (human-readable)
    with open(os.path.join(HERE, "PANEL_SUMMARY.md"), "w") as f:
        f.write("# GBCO panel summary (EGP mn; consolidated, as originally reported)\n\n")
        f.write("Full provenance per figure in gbco_panel.json (value, source document/URL, "
                "date, tier; DERIVED formulas in bottom_up.py SEG_NOTES + exog block). "
                "All company figures tier A (company's own documents).\n\n")
        f.write("| FY | revenue | gross profit | SG&A | net finance | PBT | tax | NP total | NP parent | source |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")
        P = pj["panel"]
        for fy in pj["fiscal_years"]:
            i = P[f"FY{fy}"]["is"]
            k = 1e-3
            def m(key, alt=None):
                v = i.get(key, i.get(alt) if alt else None)
                return f"{v*k:,.0f}" if isinstance(v, (int, float)) else "−"
            sga = None
            if "sm_exp" in i and "ga_exp" in i:
                sga = -(i["sm_exp"] + i["ga_exp"]) * k
            elif "distribution_exp" in i and "admin_exp" in i:
                sga = (abs(i["distribution_exp"]) + abs(i["admin_exp"])) * k
            fin = i.get("finance_cost_net", i.get("finance_cost"))
            f.write(f"| {fy} | {m('revenue')} | {m('gross_profit')} | "
                    f"{sga:,.0f} | {fin*k:,.0f} | {m('pbt')} | {m('tax','income_tax')} | "
                    f"{m('np_total')} | {m('np_parent')} | "
                    f"{P[f'FY{fy}'].get('source_doc','')} |\n")
        f.write("\n2026 interims (EGP mn): Q1 revenue 21,571 / NP 320; H1 revenue 48,474 / NP 1,056 "
                "(parent 1,262, NCI −206) — see panel interims_2026 block.\n")
    print("wrote np_ex_oneoffs.csv, decompositions.csv, guidance_ledger.md, PANEL_SUMMARY.md")


if __name__ == "__main__":
    main()
