"""SCEM — every figure the gap review quotes, computed from the study's own record.

[R-ENF-06] AN ARTEFACT EVERY BUILDER READS AND NOTHING WRITES IS A NUMBER FROZEN AT THE
DATE SOMEBODY LAST TYPED IT. gap_review_numbers.json existed for a full edition with no
generator anywhere in this repository — read by the review, written by nothing — which is
the exact shape that rule was adopted on, and it went undetected because the artefact-
currency gate could not read this study's answer at all and therefore skipped it.

Nothing here is typed. Every figure resolves from study_numbers.json, and the file
declares the central and spot it was generated against so a later edition cannot leave it
behind silently.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def build():
    d = json.load(open(os.path.join(HERE, "study_numbers.json"), encoding="utf-8"))
    meta, dcf, f, h = d["meta"], d["dcf"], d["forecast"], d["history"]
    coc, lens = d["cost_of_capital_record"], d["lens_record"]
    central, spot, sh = meta["central"], meta["spot"], meta["shares_mn"]
    mktcap = spot * sh
    nc = dcf["net_cash"]
    ev_fair = central * sh - nc + d["inputs"]["nci"]["value"]
    ev_mkt = mktcap - nc + d["inputs"]["nci"]["value"]
    eb25, pat25 = h["ebitda"][2], h["pat"][2]
    eb26 = f["ebitda"][0]
    # the earnings the multiples are struck on: this study's own forecast, taxed
    pat26 = f["pat"][0]
    return {
        "published_central": float(central),
        "published_spot": float(spot),
        "why_this_file": (
            "Every figure the eight-heading gap review quotes, resolved from "
            "study_numbers.json rather than typed. The review is an audit of an answer, "
            "so an audit quoting a stale figure audits nothing."),
        "central": float(central),
        "spot": float(spot),
        "spot_date": meta.get("spot_date"),
        "gap": float(central / spot - 1.0),
        "net_cash": float(nc),
        "net_cash_per_share": float(nc / sh),
        "net_cash_share_of_answer": float((nc / sh) / central),
        "net_cash_share_mktcap": float(nc / mktcap),
        "ev_fair": float(ev_fair),
        "ev_mkt": float(ev_mkt),
        "ev_ebitda_fair_25": float(ev_fair / eb25),
        "ev_ebitda_mkt_25": float(ev_mkt / eb25),
        "ev_ebitda_fair_26": float(ev_fair / eb26),
        "ev_ebitda_mkt_26": float(ev_mkt / eb26),
        "pe_fair_25": float(central * sh / pat25),
        "pe_mkt_25": float(mktcap / pat25),
        "pe_fair_26": float(central * sh / pat26),
        "pe_mkt_26": float(mktcap / pat26),
        "just_evebitda": float(d["inputs"]["ev_ebitda_just"]["value"]),
        "margins": [float(m) for m in f["margin"]],
        "filed_margins": [float(x) for x in
                          (h["ebitda"][i] / h["revenue"][i] for i in range(3))],
        "filed_margin_25": float(h["ebitda"][2] / h["revenue"][2]),
        "utilisation_filed": [float(u) for u in h["utilisation"]],
        "utilisation_forecast": [float(u) for u in
                                 d["inputs"]["kiln_util"]["value"][1:]],
        "tv_share": float(dcf["tv_share"]),
        "life": float(dcf["term_life_years"]),
        "term_fcff": float(dcf["term_fcff"]),
        "term_floor": float(dcf["term_floor"]),
        "term_maintenance": float(dcf["term_maintenance"]),
        "capex": [float(c) for c in f["capex"]],
        "maintenance_at_current_cost": float(dcf["term_maintenance"]),
        "wacc_exp": float(coc["wacc_exp"]),
        "wacc_term": float(coc["wacc_terminal"]),
        "wd_exp": float(coc["weight_debt"]),
        "lens": dict(d["lenses"]["values"]),
        "primary": float(lens["primary"]["value"]),
        "envelope": [float(lens["envelope"]["low"]), float(lens["envelope"]["high"])],
        "retired_blend_value": float(lens["retired"]["blend"] and
                                     lens["retired"]["blend_value"]),
        "contested": [{"choice": c["choice"], "effect": float(c["effect"]),
                       "adopted_value": float(c["fv_adopted"]),
                       "alternative_value": float(c["fv_alternative"])}
                      for c in d["contested"]],
    }


if __name__ == "__main__":
    out = build()
    json.dump(out, open(os.path.join(HERE, "gap_review_numbers.json"), "w"), indent=1,
              default=float)
    print("gap_review_numbers.json: central %.4f, spot %.2f, gap %+.1f%%"
          % (out["central"], out["spot"], 100 * out["gap"]))
