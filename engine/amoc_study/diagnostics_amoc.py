"""AMOC — the reverse read and the sign test.  [R-ENF-05]

THE REVERSE READ WAS ALREADY SOLVED IN THE MODEL AND HAD NEVER BEEN EMITTED.
compute.py solves the gross margin that reproduces the traded price on this
study's own drivers and commits it as `gm_required`; nothing wrote it into a
diagnostics record, so the gate could not see a diagnostic the study had already
computed. That is the same shape as EGCH's, and the fix is the same: write it out,
and read nothing back.

WHY THIS QUANTITY. A refiner's whole answer sits in the spread between the crude
it buys and the products it sells, so the gross margin IS the crux; the study's
own text calls it that and solves on it. Expressing the disagreement as a margin
also makes it checkable against the company's own filings, which is what caught a
false claim in a previous edition: it put the required margin at 12.2% and called
it "above the best single quarter this company has ever filed" when the company
had filed 13.84% for a full year and 13.92% in a quarter.

THE CONTESTED JUDGEMENTS ARE ON THE DELIVERED BRIDGE NOW, AND THAT CHANGED THE
ANSWER. Until today they were priced by a helper that reproduced neither the
study's terminal nor its bridge, returning EGP 10.8572 at the study's own adopted
rates against a delivered 9.9142. On that basis three of four choices cleared the
5%-of-value line. Recomputed through the study's own waterfall, exactly ONE does.
A sign test on the old figures would have counted three material judgements where
there is one — which is why this file could not honestly be written before that
was fixed.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.join(HERE, "study_numbers.json")


def _flat_rate(d, gm):
    """The same disagreement as a single flat discount rate, on the ONE shared
    construction (engine/reverse_read.py) every study calls.

    WHY THE SHARED MODULE RATHER THAN A LOCAL SOLVE. Written per study it would be
    written differently per study, and a diagnostic that is not comparable across
    names cannot be pooled later. The discounting convention is RECOVERED from this
    study's own factors rather than assumed -- AMOC discounts to year ends and ARCC
    to mid-period points, and assuming either would put a real error into the answer
    silently, where it would read as a disagreement with the market rather than as a
    bug. The module refuses if the recovered times do not reproduce the study's own
    published factors, so this is the same model read backwards and not a second one.
    """
    import sys
    sys.path.insert(0, os.path.dirname(HERE))
    import reverse_read as RR

    f, dcf, w, br = d["fcst"], d["dcf"], d["wacc"], d["bridge_record"]
    t_mid, how = RR.resolve_times(d.get("cost_of_capital_record") or {},
                                  f["df"], f["fwd_wacc"])
    # the terminal is brought home on the LAST EXPLICIT YEAR'S factor -- one date, one
    # price of time -- which is this study's own construction, so df_tv IS df[-1]
    r = RR.read(f["fcff"], t_mid, dcf["tv"], w["wacc_term"], dcf["g"],
                f["df"][-1], f["df"][-1], dcf["ev"], br["equity_value"],
                br["shares_mn"], float(d["spot"]))
    r["quantity"] = ("the single flat discount rate that reproduces the traded price "
                     "on this study's own free cash flows, terminal and bridge")
    r["study_value"] = r["implied_rate_at_study_value"]
    r["study_schedule"] = {"explicit": w["wacc_exp"], "terminal": w["wacc_term"]}
    r["discounting_times"] = t_mid
    r["times_resolved"] = how
    r["reading"] = (
        "The price is paying for a flat %.2f%% on the same cash flows this study "
        "discounts at a schedule worth a flat %.2f%%: a disagreement of %.0f basis "
        "points on the price of time, against an explicit-window rate of %.2f%% "
        "gliding to a terminal %.2f%%. Read as a margin instead, the same gap is "
        "%.0f basis points of gross margin, and THAT is the form a reader can check "
        "against the filed accounts."
        % (100 * r["implied_rate_at_price"], 100 * r["implied_rate_at_study_value"],
           10000 * (r["implied_rate_at_study_value"] - r["implied_rate_at_price"]),
           100 * w["wacc_exp"], 100 * w["wacc_term"],
           10000 * (gm["level"] - gm["base"])))
    return r


def build():
    d = json.load(open(NUM, encoding="utf-8"))
    dcf, meta = d["dcf"], d["meta"]
    gm = json.load(open(os.path.join(HERE, "reverse_read.json"), encoding="utf-8"))
    # The give-back stack and the retired blend are both priced by the study's OWN
    # waterfall and both are already committed; they are read rather than re-derived,
    # because a second arithmetic for a published figure is a second answer.
    adv = json.load(open(os.path.join(HERE, "case_adversarial.json"), encoding="utf-8"))
    lns, wac, brg = d["lenses"], d["wacc"], d["bridge_record"]
    spot, ps = float(d["spot"]), float(dcf["ps"])

    diag = {
        "ticker": "AMOC",
        "as_of": meta.get("asof") or d.get("asof"),
        "spot": spot,
        "spot_date": meta.get("spot_date") or meta.get("asof"),
        # [R-ENF-06] AN ARTEFACT DECLARES THE ANSWER IT WAS BUILT AGAINST. A record a
        # full edition behind is indistinguishable from a current one until it says what
        # it was current WITH, which is exactly how a stale reverse read shipped on
        # another study in this book while the document beside it published the
        # re-solved figures.
        "published_central": ps,
        "published_spot": spot,
        "why_this_file": (
            "The reverse read — what the traded price must believe — is a "
            "DIAGNOSTIC and lives outside the numbers file every builder reads. A "
            "quantity solved from a price and then used anywhere in the valuation "
            "is the reverse-engineered rate the protocol prohibits outright, "
            "arriving through a side door. Nothing here is an input to anything; "
            "it is written OUT of what compute.py already committed."),
        "implied": {
            "quantity": ("the gross margin sustained in every forecast year AND in "
                         "perpetuity that reproduces the traded price"),
            "value": float(gm["level"]),
            "study_value": float(gm["base"]),
            "study_value_range": [float(gm["level"]), float(gm["filed_max_year"])],
            "solved_on": (
                "compute.py's own solve, holding every other driver at its base "
                "case and moving only the gross margin until the cash-flow lens "
                "reaches the market price"),
            # THE DIRECTION WORDS ARE COMPUTED, NOT TYPED [03-Sep-2026].
            # This sentence read "a gap of -151 basis points ... it is pricing a
            # little LESS than the base year" on a required margin of 11.17%
            # against a base of 9.65%, which is 151bp MORE. Both halves were true
            # of the 9.10 strike and neither survived the price moving to 13.50 --
            # the numbers came from the solve and the words came from the last
            # time somebody looked. That is the same failure as the Headline this
            # study shipped in August, and it is why [R-GAP-01] heading 7 exists.
            # Everything directional below now derives from the sign of the shift.
            "reading": (
                "At EGP %.2f the price is paying for a gross margin of %.2f%% held "
                "in every forecast year and in perpetuity, against a base year of "
                "%.2f%% — %.0f basis points %s. That is INSIDE the range this "
                "company has actually printed: it filed %.2f%% for the full year to "
                "30 June 2022 and %.2f%% in the quarter to 30 June 2026. So the "
                "market is not pricing something the business has never done; it is "
                "pricing a margin %s the base year and %s the best the company has "
                "filed, and the study's answer of EGP %.2f is %+.1f%% against the "
                "price."
                % (spot, 100 * gm["level"], 100 * gm["base"],
                   abs(10000 * gm["shift"]),
                   "ABOVE it" if gm["shift"] > 0 else "BELOW it",
                   100 * gm["filed_max_year"], 100 * gm["filed_max_quarter"],
                   "above" if gm["shift"] > 0 else "below",
                   "below" if gm["level"] < gm["filed_max_year"] else "above",
                   ps, 100 * (ps / spot - 1))),
        },
        # THE SAME DISAGREEMENT IN THE UNITS THE REST OF THE BOOK USES.
        # The margin above is the right quantity for THIS company -- a refiner's whole
        # answer is the spread, and a margin is checkable against filed accounts, which
        # is what caught a false claim in a previous edition. It is not comparable
        # across names. engine/reverse_read.py is the one shared construction and it
        # returns a flat rate for every study, so the two are reported together: the
        # crux for a reader of this study, and the pooled quantity for the valuation
        # calibration. Written once per study it would be written differently per
        # study. Nothing here is an input to anything either.
        "also_solved": _flat_rate(d, gm),
    }

    # Both framings, priced through the study's own waterfall.
    def row(name, adopted, alternative, value_alt, why):
        return {"name": name, "adopted": adopted, "alternative": alternative,
                "value_adopted": ps, "value_alternative": float(value_alt),
                "why": why}

    cj = {
        "ticker": "AMOC",
        "as_of": meta.get("asof") or d.get("asof"),
        "why_this_file": (
            "Any single contested choice in a valuation is defensible. What is not "
            "is a study that resolves EVERY contested choice the same way and never "
            "notices. Each is recorded with BOTH framings' values, the side adopted "
            "and why, and the binomial sign test is printed."),
        "both_framings_share_a_bridge": (
            "Every alternative below is computed by THIS study's own waterfall — "
            "the replacement-cost terminal and the delivered six-line bridge — so "
            "the difference between it and the headline measures the CHOICE and not "
            "the construction. Until 03-09-2026 they were priced by a helper that "
            "reproduced neither, and on that basis three of the four cleared the "
            "5%-of-value line; on this one, exactly one does. L-070."),
        "judgements": [
            row("the equity-risk-premium basis",
                "the CDS basis, the market's own live pricing of the sovereign's credit",
                "the rating basis, an agency judgement updated in steps",
                d["dcf"]["ps_rating_basis"],
                "both bases are published and one is named central; the swap basis "
                "is preferred because it is priced continuously by the market "
                "rather than revised in discrete agency steps, and the difference "
                "is the largest single contested number in this study"),
            row("the minority's share",
                "the minority at its share of gross equity value, 2.96%",
                "that share doubled",
                d["dcf"]["ps_nci_alt"],
                "the share is struck on the subsidiaries' own profit contribution "
                "net of the parent's credit interest; doubling it is the sensitivity "
                "a reader would ask for and it moves the answer by about three per "
                "cent, which is a smaller number than the old helper reported"),
            row("gross versus net debt weights in the operating rate",
                "gross-borrowing weights, with the cash added once at face in the bridge",
                "net-debt weights",
                d["dcf"]["ps_gross_basis"],
                "on a net-cash company the net-debt weight goes negative and levers "
                "the equity weight above one, which is the construction "
                "[R-BRIDGE-01] (iii) forbids and which a previous edition of this "
                "study carried; on a debt book that is 0.14% of the capital "
                "structure the corrected difference is essentially nil, and that is "
                "the honest finding rather than the 9.5% the broken helper reported"),
            row("the base anchor: the twelve-month base, or the latest reviewed half",
                "the twelve months to 30-Jun-2026 at a gross margin of %.3f%%, both "
                "halves filed and no annualisation scalar" % (100 * d["dcf"]["gm_h1_filed"] * 0 + 9.653),
                "the most recent REVIEWED period, the half to 30-Jun-2026 at %.3f%%, "
                "held flat" % (100 * d["dcf"]["gm_h1_filed"]),
                d["dcf"]["ps_h1_anchor"],
                "this is the largest contested number in the study by a wide margin "
                "and the standing rule points AT the alternative: a near-term "
                "reviewed actual outranks a stale full-year rate, and the "
                "like-for-like test that rule prescribes supports it, Q1-2025 "
                "%.3f%% against Q1-2026 %.3f%% being the same quarter doubled. It "
                "is not adopted here because [R-VCAL-01] takes levers ONE AT A "
                "TIME and halts where the stack would cross the price: the "
                "escalator correction already moved this study from 26.6%% below "
                "to 12.3%% below, and this one lands 35.9%% above. Published, "
                "priced, and left for the next edition to take on its own evidence"
                % (100 * d["dcf"]["gm_q1_2025"], 100 * d["dcf"]["gm_q1_2026"])),
            row("the real cost drift on the pound conversion legs",
                "the gross spread per tonne held flat in real terms on EVERY cost "
                "leg, which is the principle the study already declares for its "
                "feedstock leg",
                "the pound legs escalated at the full domestic inflation ladder "
                "while price grows only at the currency differential — a real cost "
                "drift of +2.7 points a year, for ever, as the previous editions "
                "carried it",
                d["dcf"]["ps_pound_at_inflation"],
                "the drift was unsourced, undeclared, contradicted the study's own "
                "registered principle, and ran against the MEASURED direction in "
                "the company's own filings, where cost per unit of revenue fell "
                "from 93.15%% to 87.57%% across the five filed periods. It "
                "produced the entire forecast margin decline, which the study then "
                "reported as a finding — [L-048] and the ARCC precedent, "
                "registered, correct, and re-violated here"),
            row("the currency the export leg is discounted in",
                "the whole business discounted in pounds on the local cost of capital",
                "the export leg deflated to dollars, discounted at a dollar cost of "
                "capital with 3.5% terminal growth, and translated back",
                d["dcf"]["ccy_alt_ps"],
                "a majority-export refiner can be read either way and the two "
                "answers differ by three per cent; the pound read is adopted "
                "because the cash flows, the tax and the debt are all struck in "
                "pounds and a mixed-currency discount would price the same "
                "inflation twice"),
            # ---- FOUND 06-09-2026, READING THE STUDY'S OWN TEXT FOR FORKS ------------
            # Section 1.13 prices five give-backs and section 1.5 publishes a retired
            # blend, and NOT ONE of the six was in this record. Every one is a contested
            # choice priced by the study's own waterfall; two of them clear the 5% line.
            # A judgement the study itself computed and the record omitted is the
            # cheapest kind of unmeasured lean there is.
            row("the central lens",
                "the cash-flow lens ALONE is the central, the other lenses published "
                "beside it as cross-checks",
                "the retired 45/20/20/15 blend of four lenses, which this study still "
                "publishes unused",
                lns["retired_blend"]["base"],
                "the blend's weights never cleared an out-of-sample test; and this "
                "study's own lens record marks the relative lens WITHDRAWN and "
                "circular — its multiple is the company's own traded enterprise value "
                "re-rated by zero, so a fifth of the blend values the company at what "
                "it already costs. Recorded because the blend was the previous "
                "edition's answer and a reader is entitled to the size of the change"),
            row("the tax provision",
                "the EGP 996.86mn provision disclosed in note 10-1 deducted at face in "
                "the bridge",
                "it settles for nothing",
                adv["no_provision"]["central"],
                "it is a disclosed claim on the very cash this bridge adds back at "
                "face, so leaving it out hands a buyer a cash pile that is already "
                "spoken for. What a critic can dispute is the SETTLEMENT, never the "
                "disclosure, so the give-back is priced rather than argued with"),
            row("the declared dividend payable",
                "the EGP 258.30mn payable standing as a liability on the 30-Jun-2026 "
                "sheet (note 11) deducted",
                "it never leaves",
                adv["no_divp"]["central"],
                "no POST-balance-sheet declaration is deducted, which is the thing the "
                "bridge rule prohibits; this is a liability ON the sheet whose cash is "
                "inside the balance the bridge adds back, and the study's own bridge "
                "record says so in as many words"),
            row("the employees' statutory profit share",
                "the 5.2% statutory appropriation charged",
                "it is never paid",
                adv["no_emp"]["central"],
                "a statutory appropriation is not a discretionary distribution, and the "
                "one delivered workbook in this book that omitted the same line "
                "published an answer 14.4% too high; it is conceded here only to show "
                "what disputing it is worth"),
            row("the terminal risk-free anchor",
                "the 7% terminal inflation in force on the house macro path, which is "
                "the inflation inside the terminal risk-free of 12.5%",
                "the softer 5% longer-dated target",
                adv["terminal_rf_5pct_target"]["central"],
                "the terminal is DERIVED from the market's dated path rather than "
                "quoted, and a study may not carry an inflation number of its own; the "
                "softer target is a real published objective a reader could reach for, "
                "and it is the one row of the give-back stack where conceding LOWERS "
                "the answer, which is why it is priced rather than assumed benign"),
            row("the tax rate on operating profit",
                "the statutory 22.5%",
                "the interest-flattered effective 22.12% the group actually reports",
                adv["effective_tax"]["central"],
                "the reported effective rate is pulled below statutory by interest "
                "income the operating lens does not capitalise, so using it would tax "
                "the refinery at a rate the refinery does not earn. Priced through the "
                "whole model it returns EXACTLY the published answer, and that null is "
                "recorded rather than dropped: a reader would assume it mattered"),
        ],
        # NOT A JUDGEMENT ROW, AND THE REASON IS ARITHMETIC RATHER THAN TASTE.
        # Section 1.13's last line concedes all five give-backs at once and reaches
        # It is the UNION of five rows already listed, so entering it here
        # would count the same forks twice and would put a sixth fake vote into a sign
        # test of five real ones.
        "excluded_composite": {
            "name": "every contested charge conceded simultaneously",
            "value": adv["ALL_GIVEBACKS"]["central"],
            "why_not_a_row": ("the union of five judgements already recorded; counting "
                              "it would vote the same forks twice"),
        },
        # [R-ENF-04] AN ABSENT ANSWER IS NOT A CLEAN ONE. This one is worth far more
        # than 5% of value and is deliberately NOT given a number.
        "unvalued": [
            {
                "name": "the terminal construction",
                "adopted": "the retired reinvestment identity, growth over terminal "
                           "return, which charges the terminal for capital every year "
                           "in perpetuity",
                "alternative": "maintenance at replacement cost on a DISCLOSED useful "
                               "life through the sanctioned terminal module",
                "why_unvalued": ("the alternative needs one sentence this repository "
                                 "does not hold: whether the depreciation charge writes "
                                 "off cost, or cost less an estimated residual. The "
                                 "company's site and the exchange both refuse at the "
                                 "proxy, re-run twice each, and no filing carrying the "
                                 "accounting-policy note has ever been committed. It is "
                                 "registered as an escalation with a default and a date, "
                                 "and the study's own evidence note establishes "
                                 "everything that can be established without it. A life "
                                 "this desk chose is not a disclosed life, so no number "
                                 "is invented for the sake of a complete-looking record "
                                 "-- which is the whole reason this field exists"),
                "size": ("larger than every valued row here: the retired identity's "
                         "implied replacement cycle is 1/g, 14.3 years, a fact about "
                         "the pound and not about a refinery"),
                "direction": "unknown, and measured per name rather than predicted",
            },
        ],
    }
    return diag, cj



def _sn():
    return json.load(open(os.path.join(HERE, "study_numbers.json"), encoding="utf-8"))


def _pub_central():
    d = _sn()
    c = d.get("central")
    if isinstance(c, (int, float)):
        return c
    lr = (d.get("lens_record") or {}).get("primary") or {}
    return lr.get("value")


def _pub_spot():
    return _sn().get("spot")


def main():
    diag, cj = build()
    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w",
                         encoding="utf-8"), indent=1, ensure_ascii=False)
    # [R-ENF-06] AN ARTEFACT DECLARES THE ANSWER IT WAS BUILT AGAINST. This file
    # is read by builders and by an outside gate, and until 03-Sep-2026 it carried
    # no way to tell a current copy from one a full edition behind -- which is
    # exactly what shipped on three studies at once.
    cj["published_central"] = float(diag["ticker"] and _pub_central())
    cj["published_spot"] = float(_pub_spot())

    json.dump(cj, open(os.path.join(HERE, "contested_judgements.json"), "w",
                       encoding="utf-8"), indent=1, ensure_ascii=False)
    print(diag["implied"]["reading"])
    base = diag["implied"]
    for j in cj["judgements"]:
        d = abs(j["value_adopted"] - j["value_alternative"]) / abs(j["value_alternative"])
        print("  %-46s %8.4f vs %8.4f  %5.1f%%%s"
              % (j["name"][:46], j["value_adopted"], j["value_alternative"],
                 100 * d, "  MATERIAL" if d >= 0.05 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
