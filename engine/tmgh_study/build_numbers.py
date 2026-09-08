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
        # ---- the records the outside gates read ------------------------------
        # (the count is deliberately not written here: a comment carrying a
        # tally goes stale the first time a gate is added, which is what a
        # sixth record arriving beside a comment reading "four" would have done)
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
        # [R-ANCHOR-01] the rate this forecast is anchored on, the reviewed
        # actual it is anchored ON, and the whole explicit path
        "forecast_anchor": _forecast_anchor(),
        # [R-FCAL-01] THE SCOPE DECISION, TRANSCRIBED FROM THIS NAME'S OWN
        # WALK-FORWARD PRE-REGISTRATION RATHER THAN RE-DECIDED HERE. The rule
        # requires the decision to be stated in the study; the run stated it in
        # section 0 and it was never carried across, which is [R-ENF-01]'s founding
        # observation. `sourceable` is a claim about the ARCHIVE, not the panel, so
        # the count is the pre-registration's and never the number of origins used.
        "walkforward_scope": {
            "rule": "R-FCAL-01",
            "scope": "FULL",
            "sourceable_fiscal_years": 16,
            "earliest_sourceable": "FY2009",
            "basis": ("this name's own walk-forward pre-registration, section 0: "
                      "\"FULL run. The panel holds 16 sourceable fiscal years — "
                      "FY2009 and FY2011-FY2025\". The run built origins 2015-2024 "
                      "on that archive"),
            "status": "run",
            "note": ("The fundamental walk-forward HAS been run on this name "
                     "(engine/tmgh_walkforward/, 01-09-2026): 10 origins, 2015-2024, "
                     "466 scored cells on the as-known macro setting. Its adopted "
                     "list is empty — every candidate is a watch flag."),
        },
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
            # a walk-forward that scored nothing is a walk-forward that did not run
            "_driver_scores_nonempty": bool(scores.get("by_driver")),
            # THIS COMPREHENSION MATCHED NOTHING AND PRODUCED AN EMPTY DICT, SILENTLY.
            # It looked for keys shaped "asknown|<driver>|all" at the TOP LEVEL of
            # scores.json, and this file's top level is by_driver / by_horizon /
            # macro_split / by_era / sign_cases / detail — the driver keys sit one level
            # down and are plain names. Nothing raised, because an empty comprehension is
            # a valid dict; the delivered document then printed the walk-forward results
            # table with its headers, its caption and NO ROWS, under prose describing what
            # the testing found. [R-ENF-04]: an empty result is not a clean result, and
            # here the emptiness reached a reader.
            "driver_scores": {k: {"bias": v["bias"], "mae": v["mae"], "n": v["n"],
                                  "robust": v["robust_sign"],
                                  "eras": scores["by_era"].get(k, {})}
                              for k, v in scores["by_driver"].items()},
        },
    }


def _forecast_anchor():
    """[R-ANCHOR-01]. The rate the forecast is anchored on, and the whole path.

    A near-term reviewed actual outranks a stale full-year rate, and this model
    obeys that by construction rather than by assertion: every cost line is a
    disclosed ratio of its own segment's revenue taken from the reviewed half
    just filed, so each SEGMENT margin is held at its 30-June-2026 actual for the
    whole explicit window and no segment rate drifts anywhere.

    The rate recorded here is therefore the GROUP gross margin, not one of the
    three segment rates, and that choice is the point. The segment rates cannot
    move — recording one of them would be a true statement about an object that
    is constant by construction, which is the safest place a claim can hide from
    a checker. The group rate is the one a reader is shown in the projected
    income statement, and it is the one that moves: it moves on MIX, as the
    lowest-margin leg takes a different share of revenue.

    THE PATH COMMITTED IS THE STEEPER OF THE TWO THIS STUDY PUBLISHES. The crux
    is how fast the order book converts and it is computed both ways and never
    averaged, so there is no single path to commit. Choosing the flatter reading
    would satisfy clause two on a shape the study does not solely claim; the
    steeper one is selected mechanically below, so if it clears, both do.

    Nothing is typed here. Every figure is read from the reviewed statements in
    the input registry or computed from the model's own projection.
    """
    h = IN.H1_26
    rev_h1 = sum(_v(h, k) for k in ("dev_revenue", "hosp_revenue", "other_revenue"))
    gp_h1 = _v(h, "gross_profit")
    # THE DISCLOSED GROSS PROFIT MUST FOOT TO THE THREE SEGMENT LINES. Arithmetic
    # is the arbiter: an anchor standing on a figure the statement's own segments
    # do not reproduce is an anchor standing on a transcription.
    seg = sum(_v(h, r) - _v(h, c)
              for r, c in (("dev_revenue", "dev_cost"),
                           ("hosp_revenue", "hosp_cost"),
                           ("other_revenue", "other_cost")))
    assert abs(seg - gp_h1) < 1e-6, "H1-2026 gross profit does not foot to its segments"
    latest = gp_h1 / rev_h1

    paths, years = {}, {}
    for m in ("capacity", "recovery"):
        rows = M.project(m)["rows"]
        paths[m] = [r["gross_margin"] for r in rows]
        years[m] = [r["year"] for r in rows]
    # the two readings share their first year: FY2026 is anchored on the reviewed
    # half in both, so the opening rate is not a function of the crux
    assert paths["capacity"][0] == paths["recovery"][0]
    first = paths["capacity"][0]
    drop = {m: (min(paths[m]) - paths[m][0]) / paths[m][0] for m in paths}
    steep = min(drop, key=drop.get)
    flat = "capacity" if steep == "recovery" else "recovery"

    # the group rate is a revenue-weighted mean of three CONSTANT segment rates,
    # so the whole movement — into the first forecast year and along the path —
    # is mix and nothing else. Asserted rather than asserted-in-prose.
    r = M.ratios()
    gm = (r["gm_dev_h1_26"], r["gm_hosp_h1_26"], r["gm_other_h1_26"])
    w_h1 = tuple(_v(h, k) / rev_h1 for k in
                 ("dev_revenue", "hosp_revenue", "other_revenue"))
    row0 = M.project("capacity")["rows"][0]
    w_f = tuple(row0[k] / row0["revenue"] for k in
                ("dev_revenue", "hosp_revenue", "other_revenue"))
    assert abs(sum(a * b for a, b in zip(w_h1, gm)) - latest) < 1e-12
    assert abs(sum(a * b for a, b in zip(w_f, gm)) - first) < 1e-12

    rep = ST.build()["reported"]

    def _gm(y, restated=False):
        v = rep[y]
        rv = v["dev_revenue"] + v["hosp_revenue"] + v["other_revenue"]
        return (v["restated"]["gross_profit"] if restated else v["gross_profit"]) / rv

    return {
        "rate_name": "group gross margin",
        "latest_reviewed_period": "H1 2026, six months to 30 June, reviewed",
        # the date the input registry carries on the figure itself, never typed
        # here — the record and the source cannot then disagree about the vintage
        "latest_reviewed_date": h["gross_profit"]["date"],
        "latest_reviewed_rate": latest,
        "first_forecast_rate": first,
        "forecast_path": paths[steep],
        "note": (
            "No margin in this model is an input. Each cost line is a disclosed ratio of "
            "its own segment's revenue taken from the reviewed half just filed, so the "
            "three segment rates are held at their 30-June-2026 actuals for the whole "
            "explicit window and none of them drifts: development %.2f%%, hospitality "
            "%.2f%%, other recurring %.2f%%. The group rate is a revenue-weighted mean of "
            "those three constants, so every movement in it is MIX and nothing else. It "
            "opens at %.2f%% against the reviewed half's %.2f%%, %.2f%% relative below it, "
            "because development — the lowest-margin leg — is %.1f%% of the first forecast "
            "year's revenue against %.1f%% of the reviewed half's. The filed group record "
            "is FY2023 %.2f%%, FY2024 %.2f%% as first reported and %.2f%% restated, FY2025 "
            "%.2f%%, and the reviewed H1 2026 %.2f%%; the forecast opens below all of them "
            "but FY2023. The path recorded here is the slower-conversion reading of the "
            "crux, the steeper of the two this study publishes and never averages: it "
            "falls to %.2f%% in %d, %.2f%% relative below its own opening year. The faster "
            "reading falls only to %.2f%%, %.2f%% relative below its own. Both movements are "
            "the same "
            "mix effect — handovers grow faster than the two recurring legs, so the "
            "lowest-margin business takes share. Neither the opening year nor either path "
            "reaches the materiality line, so no mechanism is claimed; the steeper reading "
            "sits inside it rather than clear of it, and this record says so rather than "
            "reporting a pass."
            % (100 * gm[0], 100 * gm[1], 100 * gm[2],
               100 * first, 100 * latest, abs(100 * (first - latest) / latest),
               100 * w_f[0], 100 * w_h1[0],
               100 * _gm("2023"), 100 * _gm("2024"), 100 * _gm("2024", True),
               100 * _gm("2025"), 100 * latest,
               100 * min(paths[steep]), years[steep][paths[steep].index(min(paths[steep]))],
               abs(100 * drop[steep]), 100 * min(paths[flat]), abs(100 * drop[flat]))),
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
    # cases, never averaged — so the exposed figure is the MEDIAN of the four cases on the
    # ADOPTED basis, labelled a summary statistic. Written by the builder, never by hand.
    #
    # THE COMMENT AND THE NOTE BOTH SAID "book-minority" AND THE CODE ONE LINE BELOW READS
    # per_share_nci_value_share. The number was right and the two sentences describing it
    # were wrong, which is the more dangerous way round: a wrong number gets checked and a
    # wrong description gets believed. The note also asserted that "every case sits below
    # the price", which two of the four have not done for as long as it has been written.
    # It is now built from the cases themselves and cannot say either thing again.
    cases = sorted(d["per_share_nci_value_share"].values())
    med = (cases[len(cases) // 2 - 1] + cases[len(cases) // 2]) / 2 if len(cases) % 2 == 0 else cases[len(cases) // 2]
    d["central"] = med
    d["standard_version"] = RP.STANDARD_VERSION   # read by campaign_queue.py; never typed
    d["spot"] = d["meta"]["spot"]
    d["meta"]["central"] = med
    d["meta"]["gap_vs_spot"] = med / d["spot"] - 1
    _above = sum(1 for c in cases if c > d["spot"])
    d["meta"]["central_note"] = (
        "THIS STUDY DELIBERATELY PUBLISHES NO CENTRAL — the four cases are never "
        "averaged. The figure is the median of the four cases on the adopted "
        "minority basis (its share of value), exposed only so [R-GAP-01]'s gate can "
        "read the answer; %d of the four sit above the price and %d below."
        % (_above, len(cases) - _above))
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
