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
import research_protocol as RP

IN.assert_balance_sheet_foots()
BS26_FOOT = IN.assert_balance_sheet_1q26_foots()


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
    # THE CDS BASIS IS THE HOUSE DEFAULT AND PHDC WAS THE SECOND STUDY NOT USING IT
    # [corrected 03-Sep-2026]. [R-COC-01] names the swap basis as central -- the
    # market's own live pricing of the sovereign's credit against an agency judgement
    # updated in steps -- and AMOC, ARCC and (as of today) EGCH all follow it. Both
    # bases stay published; only which one is CENTRAL moves.
#
    # THE REASON THIS IS DONE HERE AND NOT DEFERRED IS WORTH WRITING DOWN. The switch
    # moves PHDC from 17.46 to 17.85, +2.2%, which carries it FURTHER above the traded
    # price -- 21.2% to 23.9% -- while the same switch on EGCH moved that study TOWARD
    # the market. Correcting the one that helps and deferring the one that hurts is
    # precisely the lean [R-ENF-05]'s sign test exists to measure, and a basis chosen
    # by which way it moves the answer is not a basis at all. The convention is a house
    # convention; it does not get decided per study by its consequences.
    S = V2.SCHEDULES["cds"]
    base = V2.run(CF["mid"], S)
    base_cds = V2.run(CF["mid"], V2.SCHEDULES["rating"])   # the published ALTERNATIVE now
    low = V2.run(CF["lo"], S)
    high = V2.run(CF["hi"], S)
    implied = V2.implied_conversion(V2.SPOT, S)

    gross_debt = sum(r["value"] for r in IN.DEBT_FY25.values())
    out = {
        "meta": {
            "ticker": "PHDC", "name": "Palm Hills Developments",
            "exchange": "EGX", "market": "EG", "currency": "EGP",
            "edition": "2026-09-02", "prior_edition": "2026-08-30",
            "edition_note": ("interim edition applying the three corrections of the "
                             "01-Sep-2026 valuation review: bridge, book lens and debt "
                             "stack on the 31-Mar-2026 reviewed balance sheet; minority "
                             "interests deducted at their share of value; normalised "
                             "earnings capitalised at cost of equity less growth. The "
                             "discount rate and the lens weights are unchanged."),
            "base_year": 2025, "information_set_ends": "1Q2026",
            "bridge_balance_sheet": IN.BRIDGE_BS_DATE,
            "standard_version": RP.STANDARD_VERSION,
            "spot": 14.40, "spot_date": "close 3 Sep 2026",
        },
        "registry": {**{k: v for g in (IN.ACTUALS, IN.BALANCE_SHEET_FY25, IN.DEBT_FY25,
                                       IN.OPERATING, IN.MARKET) for k, v in g.items()},
                     **{k + "_1q26": v for k, v in IN.BALANCE_SHEET_1Q26.items()}},
        "balance_sheet_fy24": IN.BALANCE_SHEET_FY24,
        "balance_sheet_1q26": IN.BALANCE_SHEET_1Q26,
        "balance_sheet_1q26_foot": BS26_FOOT,
        "balance_sheet_subtotals": IN.BALANCE_SHEET_SUBTOTALS,
        "historical_is": IN.HISTORICAL_IS,
        "fy24_cogs_basis": {"as_reported": IN.FY24_COGS_AS_REPORTED,
                            "fy25_comparative": IN.FY24_COGS_FY25_BASIS},
        "gaps": IN.GAPS,
        "wacc": W,
        "derived": {
            "gross_debt": gross_debt,                       # FY2025, the projection's base year
            "net_debt": gross_debt - VAL.V["cash"],         # FY2025, for the projected statements
            "gross_debt_bridge": BU.GROSS_DEBT_BRIDGE,      # 31-Mar-2026, what the bridge deducts
            "cash_bridge": BU.BS_BRIDGE["cash"],
            "net_debt_bridge": BU.NET_DEBT_BRIDGE,
            "bridge_balance_sheet": BU.BRIDGE_BS_DATE,
            "nci_value_share": BU.NCI_VALUE_SHARE,
            "nci_profit_share_3y": BU.NCI_PROFIT_SHARE_3Y,
            "nci_book_1q26": BU.NCI_BOOK_1Q26,
            "nci_book_share_1q26": BU.NCI_BOOK_SHARE_1Q26,
            "nci_basis": BU.NCI_BASIS,
            "shares_mn": VAL.SHARES_MN,
            "book_equity_per_share": BU.BS_BRIDGE["equity_parent"] / VAL.SHARES_MN,
            "book_equity_per_share_basis": "equity attributable to the parent, 31 March 2026, over parent shares",
            "book_equity_per_share_30aug_edition": VAL.V["total_equity"] / VAL.SHARES_MN,
            "gross_margin_fy25": VAL.GM_FY25,
            "gross_margin_1q26": VAL.GM_1Q26,
            "sga_ratio_fy25": VAL.SGA_RATIO,
            "cfo_margins": VAL.CFO_MARGINS,
            "cfo_lo": CF["lo"], "cfo_mid": CF["mid"], "cfo_hi": CF["hi"],
            "cpi_trailing3": VAL.CPI3,
            "target_backlog_multiple": VAL.TARGET_BACKLOG_MULT,
            "market_implied_cash_conversion": implied,
            "edition_11jun_wacc": 0.18,      # the 11-Jun-2026 edition's typed rate, kept for the narrative
            "prior_edition_fair": {"bear": 4.5998, "base": 10.9412, "full": 23.3342},   # 30-Aug-2026 edition
            "prior_edition_lenses": {"dcf_base": 14.86, "book": 6.56, "nep_base": 5.17},
        },
        "cases": {"low_conversion": low, "base": base,
                  "base_cds_erp": base_cds, "high_conversion": high},
        "sensitivity": {"waccs": waccs, "cfos": cfos, "grid": gv},
        "peers": peers,
        # published price engine output, read from the live site data, not re-derived
        "price_map": {
            "spot": 14.40, "spot_date": "close 3 Sep 2026",
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
        # [R-BRIDGE-01] the bridge as a RECORD, so the standing rules are checked
        # from outside the study rather than trusted inside it
        "bridge_record": {
            "market": "EG",
            "balance_sheet_date": IN.BRIDGE_BS_DATE,
            "latest_disclosed_date": IN.BRIDGE_BS_DATE,
            "latest_disclosed_source": (
                "PHD consolidated financial statements for the three months ended 31 March 2026 "
                "(limited review report attached), downloaded 01-Sep-2026 from the company's own "
                "result centre; registered line by line in bs_1q2026.json and accepted only "
                "because its own subtotals foot. The company had published no later statement at "
                "this edition's date — the half-year 2026 filing was not out."),
            # the ADDITIVE lines only: the waterfall's own components, not the
            # subtotals it prints beside them, so the record foots by construction
            "lines": [{"label": lbl, "value": val} for lbl, val in
                      V2.bridge(V2.lenses()["dcf"]["base"])
                      if lbl.startswith(("Present value", "less", "plus"))],
            "nci": {
                "basis": "value_share",
                "deduction": V2.lenses()["dcf"]["base"]["nci_deduction"],
                "applied_to": "equity_value",
                "proxy_source": (
                    "the minority's filed share of FY2025 profit after tax "
                    "(EGP 207.2mn of 4,423.8mn) — the company does not disclose the "
                    "subsidiaries carrying the minority with their own economics, so their "
                    "value cannot be built directly"),
                "book": BU.NCI_BOOK_1Q26,
                "profit_share": BU.NCI_VALUE_SHARE,
                "proportional": BU.NCI_BOOK_SHARE_1Q26,
            },
            "cash": {
                "treatment": "inside_the_flow",
                "weights_basis": "gross",
                "note": ("Cash is inside net debt, which is deducted once; the discount-rate "
                         "weights stand on GROSS debt, so no balance is netted twice. The "
                         "company is net DEBT, so the net-cash pathology cannot arise here."),
            },
            "associates": {"basis": "book", "listed": False,
                           "note": "no associate of this company is separately listed"},
            "dividend": {"deducted": False,
                         "note": "the company has not paid a cash dividend"},
            "equity_value": V2.lenses()["dcf"]["base"]["equity"],
            "shares_mn": VAL.SHARES_MN,
            "per_share": V2.lenses()["dcf"]["base"]["per_share"],
        },
        "lenses": V2.lenses()["rows"],
        "lens_weighted": V2.lenses()["weighted"],
        "lens_detail": {k: V2.lenses()[k] for k in ("normalised_inputs", "book_reference")},
        # [R-LENS-03] the architecture as a record the outside gate reads
        "lens_record": {
            "class": "real-estate developer, off-plan, percentage-of-completion",
            "primary": {"kind": "dcf", "value": V2.lenses()["primary"]["value"],
                        "range": {"low": V2.lenses()["rows"][0][1],
                                  "high": V2.lenses()["rows"][0][3]},
                        "range_note": ("the cash-flow lens across the full observed range of "
                                       "the crux — cash conversion — with the whole schedule "
                                       "shifted rather than flattened"),
                        "note": ("the cash-flow lens on the company's own units and prices, "
                                 "discounted on the cost-of-capital schedule over a window "
                                 "that runs until growth has converged on the terminal"),
                        # THIS BLOCK WAS PATCHED INTO study_numbers.json AND NOT INTO
                        # THE THING THAT WRITES IT [folded back 03-Sep-2026]. The
                        # committed artefact carried a range_basis; this generator did
                        # not emit one, so the first honest rebuild dropped it and the
                        # lens gate went red on a study that had been conforming. The
                        # standing rule is that post-delivery corrections fold back
                        # into the build scripts and not just the delivered file, and
                        # this is what it looks like when they do not: the correction
                        # survives exactly until somebody re-runs the builder.
                        "range_basis": {
                            "driver": ("cash conversion — the rate at which contracted "
                                       "sales become operating cash"),
                            "low": 0.039375934839767424,
                            "high": 0.17870012846326283,
                            "units": ("fraction of contracted sales converting to "
                                      "operating cash in the year"),
                            "evidence": (
                                "the full observed span of that rate in the company's own "
                                "filed cash-flow statements, recorded in this study's "
                                "diagnostics as study_value_range against a forecast of "
                                "0.0871. Not a chosen percentage band: the low and the "
                                "high are values this company has actually printed."),
                            "macro_held": True,
                            "macro_note": (
                                "one inflation path, one currency path, one cost-of-capital "
                                "schedule across all three reads — the schedule is shifted "
                                "whole rather than flattened, so no read discounts a year "
                                "at a rate another read does not recognise."),
                        }},
            "cross_checks": [
                # THE INGREDIENTS, NOT THE SENTENCE [added 03-Sep-2026]. This
                # lens was already non-circular -- 9x FY2026E earnings, from the
                # 6x-14x band PHDC's own shares have carried -- but the gate that
                # said so was reading this prose. AMOC's record used the same
                # reassuring words while its code divided the MARKET CAP by
                # base-year EBITDA, so the claim is now arithmetic everywhere.
                # net_debt is 0 because this is an EQUITY multiple: the comparator
                # is the traded price-to-earnings ratio on the same earnings.
                {"kind": "relative_multiple", "value": V2.lenses()["relative"]["base"],
                 "multiple": 9.0,
                 "circularity": {"spot": 14.40,
                                 "shares": float(V2.SHARES),
                                 "net_debt": 0.0,
                                 "metric_value": float(V2.ROWS[0]["npat"])},
                 "multiple_source": ("the multiples PHDC's own shares have carried over five "
                                     "years of its own history, 6x to 14x trailing earnings")},
                {"kind": "book_value", "value": V2.lenses()["book"], "present_value": False,
                 "note": ("shareholders' funds attributable to the parent at 31 March 2026, "
                          "per share: a disclosed floor, published as such and carrying no "
                          "weight")},
            ],
            "retired_lenses": [
                {"kind": "normalised_earnings",
                 "why": ("not a lens for this class. A developer recognising revenue on "
                         "completion reports earnings that are an accident of which project "
                         "completed in which year, and capitalising a mid-cycle figure treats "
                         "that schedule as a steady state. It was this study's lowest read and "
                         "carried a fifth of the retired blend's weight; the working is kept "
                         "as a disclosed diagnostic and carries no value claim.")},
            ],
            "envelope": V2.lenses()["envelope"],
            "central": V2.lenses()["primary"]["value"],
        },
        # [R-MACRO-01] every growth rate, stored so it recomputes
        "macro_record": {
            "market": "EG",
            "path_as_of": V2.PATH.as_of,
            "growth_lines": [
                {"name": "selling price and cost per delivered unit",
                 "years": [r["year"] for r in BU.build()["rows"]],
                 "nominal": [round(BU.price_growth(r["year"]), 6)
                             for r in BU.build()["rows"]],
                 "real": 0.0,
                 "basis": ("the house inflation path, zero real: price and cost escalate "
                           "together so the margin is an OUTPUT")},
                {"name": "units delivered",
                 "years": [r["year"] for r in BU.build()["rows"]],
                 "nominal": [round(BU.delivery_growth(i), 6)
                             for i in range(1, len(BU.build()["rows"]) + 1)],
                 "exempt_reason": ("a physical handover rate, not a price: the company's own "
                                   "disclosed 15% run, faded to nothing over ten years "
                                   "because it is limited by what it can build and its order "
                                   "book is finite")},
            ],
            # [R-MACRO-01], clause added 03-Sep-2026 after EGCH: every inflation-class
            # INPUT, not only the declared growth lines. THIS STUDY CARRIES ONE AND THE
            # CLAUSE FOUND IT ON ITS FIRST RUN HERE. bottom_up_model.CPI = 25.20% is the
            # World Bank Egyptian CPI averaged over 2023-25, and it escalates FY2024's
            # revenue per delivered unit forward ONE year to FY2025 so the implied FY2025
            # delivery count can be read off the disclosed revenue.
            #
            # It is a HISTORICAL step, so the forward ladder does not govern it — but a
            # THREE-YEAR MEAN is not the right figure for a one-year step either, and the
            # right figure is the 2025 print as published at the time. engine/macro_history
            # holds no sourced Egyptian CPI vintage yet (every origin reports unusable,
            # deliberately: a revised or rebased figure is fabricated in vintage even when
            # right in value), so it cannot be supplied here without inventing it.
            # Registered rather than quietly kept [SIGCM clause 8], and the effect is
            # bounded: it moves the implied unit COUNT and the price/cost pair together,
            # against a disclosed FY2025 revenue that does not move at all.
            "inflation_inputs": [
                {"key": "bottom_up_model.CPI", "mapping": "observed", "values": 0.2520,
                 "date": "2025-12-31",
                 "note": ("World Bank Egyptian CPI, mean of 2023-2025, applied as a "
                          "one-year escalator across a HISTORICAL step (FY2024 -> FY2025). "
                          "A mean over three years is not the published rate for one of "
                          "them; the correct figure is the 2025 print at its own vintage, "
                          "which engine/macro_history does not yet carry. OUTSTANDING. "
                          "PRICED 03-Sep-2026 so the open item carries its own size "
                          "rather than only its reason: this escalator moves the "
                          "NORMALISED-EARNINGS CROSS-CHECK and nothing else, and across "
                          "every candidate figure the lens spans EGP 6.17 to 7.09 a share "
                          "against 6.66 as built \u2014 at the IMF's current-vintage "
                          "Egyptian CPI for 2025 (20.4%) it is 6.41, -3.8%; at 2024's "
                          "33.3% it is 7.09; on the house forward ladder for 2026 (16.0%) "
                          "it is 6.17. The central is the cash-flow lens at 17.85 and is "
                          "untouched by any of them. IT STAYS OUTSTANDING: the figures "
                          "above are CURRENT-VINTAGE prints and [R-VCAL-01] refuses a "
                          "revised estimate without naming the publication that existed "
                          "at the origin, so none of them is the point-in-time number "
                          "this note asks for \u2014 they bound the item, they do not "
                          "close it.")},
            ],
            "terminal": {"g_nominal": V2.TG, "real": V2.TERMINAL_REAL_GROWTH,
                         "rf": V2.SCHEDULES["rating"].rf_terminal,
                         "inflation_in_rf": V2.PATH.terminal_inflation},
            "explicit_years": len(BU.build()["rows"]),
            "growth_at_horizon_end": round(
                BU.build()["rows"][-1]["revenue"] / BU.build()["rows"][-2]["revenue"] - 1, 6),
        },
        # [R-COC-01] the schedule, on this study's CENTRAL basis
        "cost_of_capital_record": W["cost_of_capital_record"],
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
            "dcf_a": ST.bridge(ST.project("cycle"), S, V2.TG,
                               "cycle"),
            "dcf_b": ST.bridge(ST.project("conversion"), S,
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
    # ---- THE FORECAST ANCHOR: THE LATEST REVIEWED PERIOD, AND THE PATH -------
    # PHDC IS THE SHAPE THE RULE ASKS FOR, AND IT DID NOT START THERE. The forward
    # gross margin IS the latest reviewed period's rate: bottom_up_model sets the
    # forward margin equal to the 1Q2026 margin and solves cost per delivered unit
    # from it, so the opening forecast year and the latest reviewed period are the
    # same number by construction and the path is flat across the whole explicit
    # window. Neither clause fires and no mechanism is owed. The record is committed
    # anyway, because it is printed for every study whether or not it fires -- which
    # is how the shape of a forecast becomes visible rather than merely not-red.
    #
    # NOTHING BELOW IS TYPED. Every figure in the record and in its note is computed
    # from this file's own registry, historical statements and projected rows, so a
    # rebuild moves the record with the model instead of leaving prose behind it.
    _FB = out["statements"]["framing_b"]
    _GMP = [float(r["gross_margin"]) for r in _FB]
    _HIS = out["historical_is"]

    def _gm_hist(y):
        return _HIS[y]["gross_profit"]["value"] / _HIS[y]["revenue"]["value"]

    _REV1Q = out["registry"]["revenue_1q26"]["value"]
    _GP1Q = out["registry"]["gross_profit_1q26"]["value"]
    _GM1Q = _GP1Q / _REV1Q
    _GM25 = _gm_hist("2025")
    _CONV = out["statements"]["cash_conversion"]
    _CONVF = float(_FB[0]["cash_conversion"])
    _CS = out["cases"]
    # the drift the two filed periods measure, and what carrying it would cost --
    # computed here so the record states arithmetic rather than quoting a comment
    _COSTDRIFT = ((1 - _GM1Q) / (1 - _GM25)) - 1.0
    _c4 = (1 - _GM1Q) * (1 + _COSTDRIFT) ** 4
    _c5 = (1 - _GM1Q) * (1 + _COSTDRIFT) ** 5
    out["forecast_anchor"] = dict(
        rate_name="gross margin",
        latest_reviewed_period="1Q2026, three months ended 31 March 2026",
        latest_reviewed_date="2026-03-31",
        latest_reviewed_rate=float(_GM1Q),
        first_forecast_rate=float(_GMP[0]),
        forecast_path=_GMP,
        note=(
            "NEITHER CLAUSE FIRES AND THE ANCHOR IS EXACT. The forecast gross margin IS "
            "the latest reviewed period's rate, %.4f%%, and it is held there for every "
            "one of the %d explicit years: the model sets the forward margin equal to the "
            "1Q2026 margin and solves cost per delivered unit from it, so the opening year "
            "and the latest reviewed period are the same number by construction and the "
            "path is flat. THE LATEST REVIEWED PERIOD IS THE NEWEST DISCLOSURE OF ANY "
            "KIND: this study's own gap register records that no second-quarter or "
            "half-year 2026 statements or release were posted to the company's result "
            "centre at this build, so the information set ends at 1Q2026. The two figures "
            "forming the rate are the company's own 1Q2026 earnings release of 20 May "
            "2026 -- revenue EGP %s mn and gross profit EGP %s mn, the release itself "
            "stating the margin as %.0f%% -- and the consolidated "
            "statements for those same three months, which carry a limited review report, "
            "are what the balance sheet in the bridge stands on. Nothing here is "
            "estimated, interpolated or inferred. "
            "WHAT THE RECORD MAKES VISIBLE, AND WHICH NO SENTENCE IN THE STUDY SAYS: "
            "against the audited FULL YEAR the forecast sits %.2f%% relatively BELOW -- "
            "FY2025 %.2f%% against a forecast %.2f%% -- and had the anchor been that full "
            "year the opening-year clause would have fired and a mechanism would have "
            "been owed. It is not the anchor precisely because the standing rule says a "
            "near-term reviewed actual outranks a stale full-year rate, and this study "
            "averaged the two until 03-Sep-2026, which took neither. The audited record "
            "is FY2023 %.2f%%, FY2024 %.2f%%, FY2025 %.2f%%, so the forecast sits above "
            "the first two audited years and below the third. "
            "THE DRIFT THAT IS MEASURED AND NOT CARRIED, recorded rather than left out. "
            "The FY2025-to-1Q2026 pair moves cost per unit of revenue from %.3f%% to "
            "%.3f%%, a rise of %.2f%% -- a like-for-like direction that would support an "
            "input-cost mechanism if a drift were being claimed. None is claimed: price "
            "and cost escalate on the same path, so the margin neither rises nor falls, "
            "and declining to extrapolate a drift is not a decline away from the anchor. "
            "The model states why it is not extrapolated -- one quarter against one "
            "audited year is a single observation on a developer whose margin moves with "
            "which project happens to hand over. What carrying it would cost is arithmetic on "
            "those two filed periods and is stated rather than asserted: cost per unit of "
            "revenue compounding at that rate reaches %.2f%% of revenue after four years, "
            "a gross margin of %.2f%%, and passes 100%% in the fifth -- a margin of %.2f%%, "
            "which is a loss on every delivered unit. A rate that takes a company to a "
            "loss inside its own explicit window on the strength of one quarterly print is "
            "an extrapolation, not an anchor. "
            "THE OTHER CANDIDATE RATE IS NAMED HERE BECAUSE IT IS THE ONE THAT CARRIES "
            "THE VALUE. The published central does not stand on the gross margin. It "
            "stands on the framing in which operating cash is set at a fixed share of "
            "revenue and working capital is the derived line, and that share is %.3f%% -- "
            "the MEAN of the company's three published years, FY2023 %.2f%%, FY2024 "
            "%.2f%%, FY2025 %.2f%% -- held flat across the window. It sits %.1f%% "
            "relatively ABOVE the latest disclosed year rather than below it, so no "
            "clause of this rule reaches it: a rate above the latest period is what the "
            "two-sided gap trigger and the sign test audit. It is recorded because the "
            "same standing sentence the gross-margin anchor obeys -- a near-term actual "
            "outranks a stale full-year rate, hold everything flat INCLUDING observed "
            "improvements -- read on this rate would point at FY2025's %.2f%% and not at "
            "a three-year mean, and the study's own grid prices the difference: EGP %.2f "
            "a share at the FY2025 rate, EGP %.2f at the mean and EGP %.2f at the FY2024 "
            "rate, on one discount schedule, with the rate the traded price implies, "
            "%.2f%%, sitting between the first two. NO REVIEWED COMPARATOR FOR THIS RATE "
            "CAN BE FORMED FROM WHAT THIS STUDY HOLDS -- 1Q2026 discloses revenue, gross "
            "profit and net profit and no cash-flow statement -- and none is estimated to "
            "fill the gap. The same model with the collection cycle held instead of the "
            "conversion yields a NEGATIVE EGP %.2f a share and is published as a funding "
            "statement rather than as a value, which is the disagreement this record sits "
            "inside."
            % (100 * _GMP[0], len(_GMP),
               "{:,.0f}".format(_REV1Q), "{:,.0f}".format(_GP1Q), 100 * _GM1Q,
               100 * (_GM25 - _GMP[0]) / _GM25, 100 * _GM25, 100 * _GMP[0],
               100 * _gm_hist("2023"), 100 * _gm_hist("2024"), 100 * _GM25,
               100 * (1 - _GM25), 100 * (1 - _GM1Q),
               100 * _COSTDRIFT,
               100 * _c4, 100 * (1 - _c4), 100 * (1 - _c5),
               100 * _CONVF,
               100 * _CONV["FY2023"], 100 * _CONV["FY2024"], 100 * _CONV["FY2025"],
               100 * (_CONVF - _CONV["FY2025"]) / _CONV["FY2025"],
               100 * _CONV["FY2025"],
               _CS["low_conversion"]["per_share"], _CS["base"]["per_share"],
               _CS["high_conversion"]["per_share"],
               100 * out["derived"]["market_implied_cash_conversion"],
               abs(out["statements"]["dcf_a"]["per_share"]))))

    # [R-LENS-03] the central IS the class primary, not a blend of lenses
    out["central"] = out["lens_record"]["primary"]["value"]
    out["standard_version"] = RP.STANDARD_VERSION   # read by campaign_queue.py; never typed
    out["spot"] = 14.40
    out["meta"]["central"] = out["central"]
    out["meta"]["gap_vs_spot"] = out["central"] / out["spot"] - 1
    out["meta"]["central_note"] = (
        "the cash-flow lens — the class primary — which IS the central under the lens "
        "architecture of 02-Sep-2026. The cross-checks are published beside it and define "
        "the range; nothing is averaged. Written by the builder, never by hand.")
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
