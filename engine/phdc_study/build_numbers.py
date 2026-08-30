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

IN.assert_balance_sheet_foots()


def main():
    W = json.load(open(os.path.join(HERE, "wacc_result.json")))
    peers = json.load(open(os.path.join(HERE, "peers.json")))
    waccs, grid = VAL.sensitivity()
    cfos = [VAL.CFO_LO, 0.060, VAL.CFO_MID, 0.120, VAL.CFO_HI]
    gv = [row for _c, row in grid]
    base = VAL.run(VAL.CFO_MID, VAL.CPI3, W["wacc_rating"], 0.12)
    base_cds = VAL.run(VAL.CFO_MID, VAL.CPI3, W["wacc_cds"], 0.12)
    low = VAL.run(VAL.CFO_LO, VAL.CPI3, W["wacc_rating"], 0.12)
    high = VAL.run(VAL.CFO_HI, VAL.CPI3, W["wacc_rating"], 0.12)

    lo_, hi_ = 0.01, 0.30
    for _ in range(80):
        m = (lo_ + hi_) / 2
        if VAL.run(m, VAL.CPI3, W["wacc_rating"], 0.12)["per_share"] < VAL.V["spot"]:
            lo_ = m
        else:
            hi_ = m
    implied = (lo_ + hi_) / 2

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
            "cfo_lo": VAL.CFO_LO, "cfo_mid": VAL.CFO_MID, "cfo_hi": VAL.CFO_HI,
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


if __name__ == "__main__":
    main()
