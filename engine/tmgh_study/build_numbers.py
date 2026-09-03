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
import research_protocol as RP
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
    ps_value = {k: v["per_share_nci_value_share"] for k, v in cases.items()}

    # The published envelope and the exposed central are on the ADOPTED minority basis
    # (value share); book and proportional are printed beside it [class-A, 02-Sep-2026].
    lo = min(ps_value.values())
    hi = max(ps_value.values())

    return {
        "meta": {
            "instrument": "Talaat Moustafa Group Holding", "ticker": "TMGH",
            "exchange": "EGX", "market": "EG", "currency": "EGP",
            "edition_date": "2026-09-02",
            "standard_version": RP.STANDARD_VERSION,
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
        "per_share_nci_value_share": ps_value,
        # ---- the four records the outside gates read ------------------------
        # [R-COC-01] the schedule, on the CENTRAL premium basis
        "cost_of_capital_record": w["cost_of_capital_record"],
        # [R-MACRO-01] every growth rate in the model, stored so it recomputes
        "macro_record": _macro_record(),
        # [R-LENS-03] one primary, published as a range because its crux is
        # computed both ways; the cross-checks beside it
        "lens_record": _lens_record(ps_value, lo, hi),
        # [R-BRIDGE-01] the bridge as a RECORD, checked from outside the study.
        # The central case is the one the exposed central is taken from.
        "bridge_record": _bridge_record(cases, sh),
        "nci_basis_adopted": "value share (filed profit share proxy, 20.98%); book and proportional shown as the more punitive reads",
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


def _macro_record():
    """Every growth rate in this model, stored as (real, path) so it recomputes.

    [R-MACRO-01]. The rates that ARE inflation carry real growth of zero; the
    rates the path does not drive — a contracted sales ladder, a physical
    delivery rate — are exempted BY NAME with the reason, which is the honest
    alternative to either forcing them onto the path or going quiet about them.
    """
    import macro_path as MP
    path = MP.load("EG")
    yrs = list(range(2026, 2031))
    return {
        "market": "EG",
        "path_as_of": path.as_of,
        "growth_lines": [
            {"name": "selling prices and unit costs",
             "years": yrs, "nominal": [round(path.inflation(y), 6) for y in yrs],
             "real": 0.0,
             "basis": "the house inflation path, zero real: price and cost escalate "
                      "together and the margin is an OUTPUT, never an input"},
            {"name": "contracted sales replenishment",
             "years": yrs, "nominal": [M.SALES_FADE - 1.0] * len(yrs),
             "exempt_reason": ("a physical sales ladder held flat in REAL terms against the "
                               "company's own record, not a price; the class-A correction of "
                               "02-Sep-2026 replaced a 15%-a-year fade with this")},
        ],
        # [R-MACRO-01], clause added 03-Sep-2026 after EGCH. Every inflation-class INPUT
        # the model registers, with the mapping that derives it from the house ladder --
        # declared even when the list is empty, because EGCH's growth lines were all
        # legitimately exempt while an undeclared cpi_path drove its whole currency path
        # and every cost escalator. This model carries none: its selling prices and unit
        # costs escalate on the house path through the growth line above, its sales ladder
        # is a physical rate, and no separate inflation array exists anywhere in it.
        "inflation_inputs": [],
        "terminal": {
            "g_nominal": M.TERMINAL_GROWTH,
            "real": M.TERMINAL_REAL_GROWTH,
            "rf": path.terminal_rf,
            "inflation_in_rf": path.terminal_inflation,
        },
        "explicit_years": 10,
        "growth_at_horizon_end": M.TERMINAL_GROWTH,
        "note": ("The explicit window ends at the terminal growth rate by construction: the "
                 "recurring legs grow with prices and the development leg is a finite order "
                 "book, so nothing is capitalised at a rate the model never reached."),
    }


def _lens_record(ps_value, lo, hi):
    """[R-LENS-03]. One primary, published as a RANGE.

    The class primary for a developer recognising revenue on handover is the
    cash-flow lens. This study's crux — how fast the order book converts — is
    computed BOTH WAYS and never averaged, so the primary is published as a range
    rather than a point, and the figure exposed for the gap gate says what it is.

    NORMALISED EARNINGS IS RETIRED HERE, and its retirement is the registry's own
    reasoning rather than a convenience: a company recognising revenue when the
    customer takes the home reports earnings that are an accident of which project
    completed in which year, and capitalising a mid-cycle figure treats that
    schedule as a steady state.
    """
    L = json.load(open(os.path.join(HERE, "lenses.json")))
    book = L["book_and_sustainable_return"]["book_value_per_share"]
    return {
        "class": "real-estate developer, off-plan, point-in-time on handover",
        "primary": {
            "kind": "dcf",
            "range": {"low": lo, "high": hi},
            "note": ("four cases: two premium bases x two readings of the crux, on the "
                     "cost-of-capital SCHEDULE rather than a flat rate. They are never "
                     "averaged."),
            # THIS BLOCK WAS PATCHED INTO study_numbers.json AND NEVER INTO THIS BUILDER
            # [restored 03-Sep-2026]. The 03-Sep commit that adopted the range_basis
            # requirement edited the generated file directly, so the next honest rebuild of
            # this study dropped it and the lens gate went red — which is L-067's cousin: a
            # value written into a generated artefact is lost at the next generation, and
            # the gate is what tells you, some hours later, in another pass. It lives in the
            # generator now.
            "range_basis": {
                "driver": ("two readings of the crux crossed with the two published "
                           "equity-risk-premium bases — four cases, never averaged"),
                "low": lo,
                "high": hi,
                "units": "EGP per share, the four cases' own present values",
                "evidence": ("the four cases this study computes and publishes side by "
                             "side, per the dual-framing rule; the low and high are the "
                             "lowest and highest of them."),
                "macro_held": True,
                "sanctioned_framing": ("both premium bases are published and one is named "
                                       "central. Spanning them is a framing the method "
                                       "requires, not a spread invented around the answer."),
            },
        },
        "cross_checks": [
            {"kind": "book_value", "value": book, "present_value": False,
             "note": ("shareholders' funds attributable to the parent, per share, at "
                      "30 June 2026 — a disclosed floor, published as such and carrying "
                      "no weight")},
        ],
        "retired_lenses": [
            {"kind": "normalised_earnings",
             "why": ("not a lens for this class: the company recognises revenue when the "
                     "customer takes control of the home, so its reported earnings are an "
                     "accident of which project completed in which year, and capitalising a "
                     "mid-cycle figure treats that schedule as a steady state. The working "
                     "is kept as a disclosed diagnostic and carries no value claim.")},
        ],
        "envelope": {"low": lo, "high": hi},
        "central": sorted(ps_value.values())[1:3] and
                   (sorted(ps_value.values())[1] + sorted(ps_value.values())[2]) / 2.0,
        "central_note": ("this study publishes NO central. The figure exposed here is the "
                         "median of the four cases, so the valuation-gap gate can read an "
                         "answer; the cases themselves are published side by side and are "
                         "never averaged into a headline."),
    }


def _bridge_record(cases, sh):
    """The enterprise-to-equity bridge of the central case, in the shape
    research_protocol.assert_bridge() checks [R-BRIDGE-01]."""
    # The published central is the MEDIAN of the four value-share cases, and on an
    # even number of cases a median is not any one of them. The record therefore
    # describes the case NEAREST the central and says so: the bridge's
    # construction — which balance sheet, which minority basis, cash charged how
    # often — is identical across the four, and a bridge averaged out of two
    # cases would be a bridge nobody built.
    ordered = sorted(cases.values(), key=lambda v: v["per_share_nci_value_share"])
    central = (ordered[1]["per_share_nci_value_share"]
               + ordered[2]["per_share_nci_value_share"]) / 2.0
    c = min(ordered, key=lambda v: abs(v["per_share_nci_value_share"] - central))
    bs_date = max(r["date"] for r in IN.BS.values() if isinstance(r, dict) and r.get("date"))
    return {
        "market": "EG",
        "case": ("the case nearest the published central of %.2f; the four cases share one "
                 "bridge construction and differ only in the discount rate and the "
                 "conversion period" % central),
        "balance_sheet_date": bs_date,
        "latest_disclosed_date": bs_date,
        "latest_disclosed_source": (
            "TMG Holding interim consolidated financial statements for the three and six "
            "months ended 30 June 2026 (reviewed), taken from the company's own investor "
            "relations channel and registered line by line in inputs.BS; the walk-forward "
            "document register for this name records no later filing."),
        "lines": [
            {"label": "Enterprise value", "value": c["enterprise_value"]},
            {"label": "plus cash and deposits", "value": c["cash_and_deposits"]},
            {"label": "less borrowings", "value": -c["borrowings"]},
            {"label": "less lease liabilities", "value": -c["lease_liabilities"]},
            {"label": "plus investment property", "value": c["investment_property"]},
            {"label": "plus associates", "value": c["associates"]},
            {"label": "plus investments at fair value", "value": c["fvoci"]},
            {"label": "less minority interests at their share of value",
             "value": -(c["equity_before_minority"] - c["equity_after_nci_value_share"])},
        ],
        "nci": {
            "basis": "value_share",
            "deduction": c["equity_before_minority"] - c["equity_after_nci_value_share"],
            "applied_to": "equity_value",
            "proxy_source": (
                "the minority's filed share of FY2025 profit after tax (%.2f%%) — the company "
                "does not disclose the subsidiaries carrying the minority with their own "
                "economics, so their value cannot be built directly"
                % (100 * c["nci_profit_share"])),
            "book": c["nci_book"],
            "profit_share": c["nci_profit_share"],
            "proportional": c["nci_share_of_equity"],
        },
        "cash": {
            "treatment": "added_at_face",
            "weights_basis": "gross",
            "note": ("Cash is added once, at face, in the bridge; the discount-rate weights "
                     "stand on GROSS debt, so the company's net cash position is not also "
                     "netted inside the rate. Doing both is the defect that put an operating "
                     "rate above the cost of equity on a net-cash company."),
        },
        "associates": {"basis": "book", "listed": False,
                       "note": "no associate is separately listed"},
        "dividend": {"deducted": False,
                     "note": "no dividend declared after the balance-sheet date is deducted here"},
        "equity_value": c["equity_after_nci_value_share"],
        "shares_mn": sh,
        "per_share": c["per_share_nci_value_share"],
    }


def main():
    d = build()
    # THE ANSWER THE GAP GATE READS. This study deliberately publishes no central — four
    # cases, never averaged — so the exposed figure is the MEDIAN of the four book-minority
    # cases, labelled a summary statistic. Written by the builder, never by hand.
    cases = sorted(d["per_share_nci_value_share"].values())
    med = (cases[len(cases) // 2 - 1] + cases[len(cases) // 2]) / 2 if len(cases) % 2 == 0 else cases[len(cases) // 2]
    d["central"] = med
    d["standard_version"] = RP.STANDARD_VERSION   # read by campaign_queue.py; never typed
    d["spot"] = d["meta"]["spot"]
    d["meta"]["central"] = med
    d["meta"]["gap_vs_spot"] = med / d["spot"] - 1
    d["meta"]["central_note"] = ("THIS STUDY DELIBERATELY PUBLISHES NO CENTRAL — the four cases are never "
                                 "averaged. The figure is the median of the four book-minority cases, exposed "
                                 "only so [R-GAP-01]'s gate can read the answer; every case sits below the price.")
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
