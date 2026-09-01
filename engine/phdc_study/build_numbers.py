"""Assemble study_numbers.json — the single numeric source every builder reads.

Numeric traceability: the document builder and the workbook builder read this
file and nothing else. No financial numeral is typed into either of them, so a
figure in the delivered study can always be traced to the registry entry it came
from, and an independent recalculation has one place to check.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import inputs as IN
import valuation as VAL
import bottom_up_model as BU
import valuation_v2 as V2
import statements as ST

IN.assert_balance_sheet_foots()


def main():
    W = json.load(open(os.path.join(HERE, "wacc_result.json")))
    peers = json.load(open(os.path.join(HERE, "peers.json")))
    # ONE MODEL. Cases, the sensitivity grid, the implied rate and every lens
    # all come from the bottom-up units-and-prices forecast. The study used to
    # take these four from a separate ten-year capacity-ratio model while the
    # lens tables and the bridge came from the bottom-up one, so the same
    # document published two different fundamental ranges — EGP 9.17 to 38.74
    # in the headline against EGP 2.85 to 38.75 in the summary table two pages
    # later. The independent recalculation of the delivered workbook caught it.
    CF = V2.lenses()["cfo"]
    waccs, grid = V2.sensitivity()
    cfos = [CF["lo"], 0.060, CF["mid"], 0.120, CF["hi"]]
    gv = [row for _c, row in grid]
    base = V2.run(CF["mid"], W["wacc_rating"])
    base_cds = V2.run(CF["mid"], W["wacc_cds"])
    low = V2.run(CF["lo"], W["wacc_rating"])
    high = V2.run(CF["hi"], W["wacc_rating"])
    implied = V2.implied_conversion(V2.SPOT, W["wacc_rating"])

    gross_debt = sum(r["value"] for r in IN.DEBT_FY25.values())
    out = {
        "meta": {
            "ticker": "PHDC", "name": "Palm Hills Developments",
            "exchange": "EGX", "market": "EG", "currency": "EGP",
            "edition": "2026-08-30", "prior_edition": "2026-06-11",
            "base_year": 2025, "information_set_ends": "1Q2026",
        },
        "registry": {k: v for g in (IN.ACTUALS, IN.BALANCE_SHEET_FY25, IN.DEBT_FY25,
                                    IN.OPERATING, IN.MARKET) for k, v in g.items()},
        "balance_sheet_fy24": IN.BALANCE_SHEET_FY24,
        "balance_sheet_subtotals": IN.BALANCE_SHEET_SUBTOTALS,
        "historical_is": IN.HISTORICAL_IS,
        "fy24_cogs_basis": {"as_reported": IN.FY24_COGS_AS_REPORTED,
                            "fy25_comparative": IN.FY24_COGS_FY25_BASIS},
        "gaps": IN.GAPS,
        "wacc": W,
        "derived": {
            "gross_debt": gross_debt,
            "net_debt": gross_debt - VAL.V["cash"],
            "shares_mn": VAL.SHARES_MN,
            "book_equity_per_share": VAL.V["total_equity"] / VAL.SHARES_MN,
            "gross_margin_fy25": VAL.GM_FY25,
            "gross_margin_1q26": VAL.GM_1Q26,
            "sga_ratio_fy25": VAL.SGA_RATIO,
            "cfo_margins": VAL.CFO_MARGINS,
            "cfo_lo": CF["lo"], "cfo_mid": CF["mid"], "cfo_hi": CF["hi"],
            "cpi_trailing3": VAL.CPI3,
            "target_backlog_multiple": VAL.TARGET_BACKLOG_MULT,
            "market_implied_cash_conversion": implied,
            "prior_edition_wacc": 0.18,
            "prior_edition_fair": {"bear": 7.62, "base": 15.89, "full": 24.92},
        },
        "cases": {"low_conversion": low, "base": base,
                  "base_cds_erp": base_cds, "high_conversion": high},
        "sensitivity": {"waccs": waccs, "cfos": cfos, "grid": gv},
        "peers": peers,
        # published price engine output, read from the live site data, not re-derived
        "price_map": {
            "spot": 15.20, "spot_date": "close 23 Aug 2026",
            "dist": {"m1": {"p5": 13.08, "p25": 14.67, "p50": 15.64,
                            "p75": 16.68, "p95": 18.71, "resolve": "2026-09-23"},
                     "m3": {"p5": 11.98, "p25": 14.61, "p50": 16.34,
                            "p75": 18.27, "p95": 22.26, "resolve": "2026-11-23"}},
            "touch": [[20.00, 3, 19], [18.50, 9, 35], [17.50, 20, 51],
                      [16.50, 43, 71], [15.55, 80, 90]],
            "band_record": {"n": 57, "hits": 52, "c50": 0.5088, "c80": 0.8596,
                            "c90": 0.9123, "width": 1.469, "strength": "long",
                            "flag": None},
            "asof": {"mc_data": "2026-08-23", "mc_computed": "2026-08-24",
                     "tech_data": "2026-08-23", "tech_computed": "2026-08-25"},
        },
        "technical": {
            "levels": {"res": [15.38, 15.73, 16.08], "sup": [14.99, 14.40, 13.01]},
            "close": 15.20, "sma20": 15.15, "sma50": 15.10, "sma200": 10.95,
        },
        "bottom_up": {
            "regions": {nm: {"units_base": d["units_base"],
                             "asp_base": d["asp_base"],
                             "history": BU.REGION_HISTORY[nm]}
                        for nm, d in BU.build()["regions"].items()},
            "rows": BU.build()["rows"],
            "anchors": BU.build()["anchors"],
        },
        "lenses": V2.lenses()["rows"],
        "lens_weighted": V2.lenses()["weighted"],
        "bridge": [list(x) for x in V2.bridge(V2.lenses()["dcf"]["base"])],
        "ranged_revenue": V2.ranged_revenue(),
        "dcf_cases": {k: {kk: vv for kk, vv in v.items()}
                      for k, v in V2.lenses()["dcf"].items()},
        "statements": {
            "cycle_measured": {"dso_fy25": ST.DSO25, "dso_fy24": ST.DSO24,
                               "dio_fy25": ST.DIO25, "dio_fy24": ST.DIO24,
                               "dpo_fy25": ST.DPO25, "dpo_fy24": ST.DPO24,
                               "adv_of_backlog_fy25": ST.ADV25,
                               "adv_of_backlog_fy24": ST.ADV24,
                               "operating_assets_fy25": ST.WA25,
                               "operating_assets_fy24": ST.WA24,
                               "operating_liabs_fy25": ST.WL25,
                               "operating_liabs_fy24": ST.WL24,
                               "nwc_fy25": ST.NWC25, "nwc_fy24": ST.NWC24,
                               "nwc_over_revenue_fy25": ST.NWC25 / ST.R25,
                               "nwc_over_revenue_fy24": ST.NWC24 / ST.R24},
            "wedge": {"d_wc_book_fy25": ST.DWC_BOOK_25,
                      "d_wc_cash_fy25": ST.DWC_CASH_25,
                      "wedge_fy25": ST.WEDGE_25,
                      "wedge_over_revenue": ST.WEDGE_RATIO,
                      "audited_rounding": ST.AUDITED_ROUNDING},
            "cash_conversion": {**ST.CONV, "mean": ST.CONV_MID,
                                "low": ST.CONV_LO, "high": ST.CONV_HI},
            "framing_a": ST.project("cycle"),
            "framing_b": ST.project("conversion"),
            "dcf_a": ST.bridge(ST.project("cycle"), W["wacc_rating"], V2.TG,
                               "cycle"),
            "dcf_b": ST.bridge(ST.project("conversion"), W["wacc_rating"],
                               V2.TG, "conversion"),
            "capex_ratio": ST.CAPEX_RATIO, "dividend": ST.DIVIDEND,
            "min_cash": ST.MIN_CASH, "other_assets": ST.OTHER_ASSETS,
            "other_liabs": ST.OTHER_LIABS,
            "checks": [{"name": n, "pass": bool(pp), "note": t}
                       for n, pp, t in ST.verify()],
        },
        "walkforward": {
            "origins": 10, "horizons": "1-5y",
            "revenue_bias": 0.105, "revenue_mae": 0.425,
            "net_profit_bias": 1.116, "net_profit_mae": 1.117,
            "net_profit_share_over": 0.97,
            "gross_profit_bias": 0.540, "gross_profit_share_over": 0.86,
            "units_sold_bias": -0.215, "macro_share_revenue": 0.215,
            "macro_share_net_profit": 0.039,
            "bridge_residual_all_drivers_correct": 0.130,
        },
    }
    json.dump(out, open(os.path.join(HERE, "study_numbers.json"), "w"),
              indent=1, default=str)
    n = sum(1 for _ in json.dumps(out))
    print("study_numbers.json written (%d chars)" % n)
    print("  registry entries : %d" % len(out["registry"]))
    print("  gaps             : %d" % len(out["gaps"]))
    print("  cases            : %s" % ", ".join(out["cases"]))
    print("  fair value range : EGP %.2f - %.2f  (spot %.2f)"
          % (min(c["per_share"] for c in out["cases"].values()),
             max(c["per_share"] for c in out["cases"].values()),
             out["price_map"]["spot"]))
    print("  implied conversion at spot : %.2f%%" % (implied * 100))
    lw = out["lens_weighted"]
    print("  weighted lenses  : bear %.2f / base %.2f / full %.2f"
          % (lw["bear"], lw["base"], lw["full"]))
    print("  bottom-up FY2026 revenue   : %.0f (anchored on the reported quarter)"
          % out["bottom_up"]["rows"][0]["revenue"])


if __name__ == "__main__":
    main()
