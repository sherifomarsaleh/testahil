"""TMGH — the study's single committed numbers file.

NUMERIC TRACEABILITY. Every builder in this study reads `study_numbers.json`
and nothing else; no financial numeral is typed into a document builder, a
workbook builder or a figure. That is depth-bar item 3, and it is what lets an
independent evaluator recalculate the delivered workbook against a file that
was produced by the model rather than transcribed from it.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ENGINE)
import inputs as IN
import model as M
import valuation as VAL
import statements as ST
import lenses as LN
import wacc as WC


def _v(d, k):
    return d[k]["value"]


def build():
    w = json.load(open(os.path.join(HERE, "wacc.json")))
    val = json.load(open(os.path.join(HERE, "valuation.json")))
    lens = json.load(open(os.path.join(HERE, "lenses.json")))
    stm = ST.build()
    wf = json.load(open(os.path.join(ENGINE, "tmgh_walkforward",
                                     "corrections_log.json")))
    fr = json.load(open(os.path.join(ENGINE, "tmgh_walkforward",
                                     "forward_ranges.json")))
    scores = json.load(open(os.path.join(ENGINE, "tmgh_walkforward", "scores.json")))

    spot = WC.SPOT
    sh = _v(IN.KPI, "shares_outstanding")
    cases = {k: val[k] for k in val if "|" in k}
    per_share = {k: v["per_share_nci_book"] for k, v in cases.items()}
    ps_prop = {k: v["per_share_nci_proportional"] for k, v in cases.items()}

    lo = min(list(per_share.values()) + list(ps_prop.values()))
    hi = max(list(per_share.values()) + list(ps_prop.values()))

    return {
        "meta": {
            "instrument": "Talaat Moustafa Group Holding", "ticker": "TMGH",
            "exchange": "EGX", "market": "EG", "currency": "EGP",
            "edition_date": "2026-09-01",
            "spot": spot, "spot_source": WC.SPOT_SOURCE,
            "shares_mn": sh,
            "market_cap": spot * sh,
            "class": "real-estate developer, off-plan — point-in-time on handover",
        },
        "inputs": {"IS": IN.IS, "H1_26": IN.H1_26, "BS": IN.BS, "KPI": IN.KPI,
                   "GAPS": IN.GAPS},
        "wacc": w,
        "ratios": M.ratios(),
        "model_parameters": val["parameters"],
        "valuation_cases": cases,
        "per_share_nci_book": per_share,
        "per_share_nci_proportional": ps_prop,
        "fair_value_range": {"low": lo, "high": hi,
                             "note": ("the envelope of four published cases — two ERP "
                                      "bases x two readings of the crux — on the "
                                      "minority framed both ways. It is a range, not a "
                                      "target, and the cases are never averaged")},
        "statements": stm,
        "lenses": lens,
        "walkforward": {
            "adopted_corrections": wf["adopted"],
            "watch_flags": wf["watch_flags"],
            "refused": wf["refused"],
            "forward_ranges": fr["projection"],
            "guidance_ledger": fr["guidance_ledger"],
            "driver_scores": {k: {"bias": v["bias"], "mae": v["mae"], "n": v["n"],
                                  "robust": v["robust_sign"],
                                  "eras": v["by_era"]}
                              for k, v in scores.items() if k.endswith("|all")
                              and k.startswith("asknown|")},
        },
    }


def main():
    d = build()
    p = os.path.join(HERE, "study_numbers.json")
    json.dump(d, open(p, "w"), indent=1)
    print("wrote %s (%d bytes)" % (p, os.path.getsize(p)))
    print("fair-value envelope %.2f - %.2f against spot %.2f"
          % (d["fair_value_range"]["low"], d["fair_value_range"]["high"],
             d["meta"]["spot"]))
    print("cases:")
    for k in sorted(d["per_share_nci_book"]):
        print("   %-20s NCI at book %7.2f   proportional %7.2f"
              % (k, d["per_share_nci_book"][k], d["per_share_nci_proportional"][k]))


if __name__ == "__main__":
    main()
