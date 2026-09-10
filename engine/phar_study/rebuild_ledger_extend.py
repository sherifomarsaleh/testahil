#!/usr/bin/env python3
"""PHAR rebuild ledger [R-REBUILD-01] — EXTENDED, never restarted.

The five levers of 4 September 2026 stand exactly as recorded.  7 September 2026
appends two: the FUNDAMENTAL walk-forward [R-FCAL-01], which moved nothing, and the
TERMINAL BASIS correction [R-TERM-01], which moved the answer -9.94% on Frame A and
-8.41% on Frame B.

AUDIT POINT, DECLARED BEFORE THE PASS BEGAN AND NOT AFTER IT: after the
walk-forward's corrections are dispositioned and BEFORE the price is consulted
for the gap review.  That is the same shape as the ledger's original audit point
— stop once the levers serving one rule are complete — and it is the place that
would have caught this study's own +45%-then-back-down route in September.

THE SEVENTH LEVER IS A BASIS CORRECTION AND NOT A JUDGEMENT.  engine/terminal_value.py
takes its flows in the LAST EXPLICIT YEAR'S money and grows the free cash flow one year
itself; both of this study's call sites handed it flows already grown by (1+g), so the
module grew them a second time.  Rebuilding the superseded construction through the SAME
module reproduces the previous edition's published pair to the fourth decimal, which is
how this pass knows it moved one thing and not several.  It moves the answer FURTHER FROM
the market price, and that is not a reason to reconsider it.

THE SIXTH LEVER MOVES NOTHING AND THAT IS THE RECORD, NOT AN ABSENCE OF ONE.
The run dispositioned seven primitive drivers and adopted no correction: six are
UNTESTABLE under the cut-invariance clause because a LIGHT run at three horizons
yields nine cells and the clause needs ten, and the seventh flips sign at the one
admissible cut.  Untestable is not stable.  So the walk-forward's finding is a
measurement of the method, not a change to the answer, and a lever recording
before == after with its reason is how that is made countable rather than
invisible.
"""
from __future__ import annotations
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
sys.path.insert(0, ENG)
import rebuild_ledger as RL  # noqa: E402

LEDGER = os.path.join(HERE, "rebuild_ledger.json")
AUDIT = ("the levers serving [R-MACRO-01] are complete — the house inflation ladder, the "
         "currency derived from it and the terminal risk-free derived from it are ONE rule "
         "in three places, and the natural place to stop and look is when that rule has "
         "finished moving the answer. RE-DECLARED FOR THE 07-09-2026 PASS, IN ADVANCE: stop "
         "again once the walk-forward's corrections are dispositioned and BEFORE the price "
         "is consulted for the gap review. RE-DECLARED AGAIN FOR THE TERMINAL-BASIS PASS OF "
         "THE SAME DAY, BEFORE THE LEVER WAS BUILT: that audit point was REACHED AND PASSED "
         "at the sixth lever, so this pass declares its own — stop once the single lever "
         "serving [R-TERM-01] is in and BEFORE the gap review is written, and record that "
         "the cumulative move has crossed the previously declared point. It has: the route "
         "from the 4 September starting answer now runs through +45% and back down past the "
         "level the earlier audit point stopped at, and the eighth heading of the gap review "
         "is where that is answered rather than here.")


WF_LEVER = "the fundamental walk-forward ran and adopted no correction"
TERM_LEVER = "the terminal fed on the last explicit year's money, not a year already grown"
BETA_LEVER = "the beta re-derived against the published index of its own exchange"


def build():
    old = json.load(open(LEDGER, encoding="utf-8"))
    # IDEMPOTENT, AND IT WAS NOT ON ITS FIRST RUN. A generator that appends every
    # time it is invoked does not reproduce its own committed output, which is the
    # drift a committed record is checked against — running it twice added the same
    # lever twice, with a zero move, and the ledger still WALKED, so nothing would
    # have caught it. The append is now keyed on the lever's own name.
    # THE TERMINAL LEVER'S OWN LANDING IS A HISTORICAL FACT AND IS READ BACK, NOT
    # RECOMPUTED. It was applied on 7 September and it landed on EGP 32.9975 with the
    # beta this study then carried. A later lever changed that beta, so recomputing
    # this lever from today's model would silently re-date it and the sequence would
    # describe an order that never happened. [R-REBUILD-01] records levers IN THE
    # ORDER APPLIED, so the earlier lever keeps the answer it actually reached and the
    # beta lever walks on from there.
    _prior_term = [lv for lv in old["levers"] if lv["name"] == TERM_LEVER]
    TERM_LANDED = _prior_term[0]["after"] if _prior_term else None
    old["levers"] = [lv for lv in old["levers"]
                     if lv["name"] not in (WF_LEVER, TERM_LEVER, BETA_LEVER)]
    led = RL.Ledger(ticker=old["ticker"], started_at=old["started_at"],
                    start_value=old["start_value"], start_spot=old["start_spot"],
                    audit_after=AUDIT)
    for lv in old["levers"]:
        led.apply(lv["name"], lv["rule"], lv["after"], lv.get("why", ""),
                  lv.get("evidence", ""))

    NUM = json.load(open(os.path.join(HERE, "study_numbers.json"), encoding="utf-8"))
    central = NUM["central_two_sided"]["branches"][0]["value"]
    A, Bf = NUM["dcf"]["frame_A"], NUM["dcf"]["frame_B"]
    # THE ANSWER THIS PASS STARTED FROM, READ RATHER THAN TYPED. The superseded terminal is
    # rebuilt through the same sanctioned module inside compute.py, so the value the ledger
    # must walk from is a COMPUTED figure and not a remembered one; it reproduces the answer
    # the previous edition published, which is how this pass knows the correction is
    # isolated to the basis and moved nothing else.
    # AND THE SAME APPLIES TO WHERE THIS PASS STARTED FROM. per_share_superseded_grown_basis
    # is Frame A under the SUPERSEDED terminal construction as today's model computes it —
    # which is a different number once a later lever has moved the discount rate. Comparing
    # a recomputed quantity against a historical chain is exactly the vintage mismatch this
    # ledger exists to make visible, so where the terminal lever has already been recorded
    # its OWN opening value is what the earlier levers must reach.
    before_term = (_prior_term[0]["before"] if _prior_term
                   else A["per_share_superseded_grown_basis"])
    assert abs(before_term - led.value) < 1e-6, (
        "the ledger's last lever must reach the answer this pass started from: %r vs %r"
        % (led.value, before_term))

    led.apply(
        WF_LEVER,
        "R-FCAL-01",
        before_term,
        why=("the LIGHT run's five origins at horizons one to three give nine cells on every "
             "primitive driver and twelve on the aggregates. The cut-invariance clause needs "
             "a boundary leaving five cells each side, so NO primitive driver admits a single "
             "cut and none can be shown sign-stable; the one driver with twelve cells that is "
             "not an aggregate, the associates-and-interest-income block, FLIPS at the one cut "
             "it admits. Every candidate is therefore DECLINED and the answer does not move."),
        evidence=("scores.json and corrections_log.json of 07-09-2026, built through the HOUSE "
                  "cut instrument (engine/valuation_calibration/boundary_sensitivity.cuts_for) "
                  "rather than a copy of it. Pooled bias: revenue -0.310, cost of sales -0.294, "
                  "net profit -0.553, compounding -0.157 -> -0.387 -> -0.693 across the three "
                  "horizons — the scale is systematically under-forecast and the margin is "
                  "roughly right, which is this house's own pooled census arriving on this "
                  "name's own history."))

    # SEVENTH LEVER — [R-TERM-01]. The sanctioned terminal module takes its flows in the
    # LAST EXPLICIT YEAR'S money and grows the free cash flow one year itself; both of this
    # study's call sites handed it a NOPAT, a book depreciation charge and a working-capital
    # level already grown by (1+g), so the module grew them a second time and the terminal
    # capitalised a year-seven flow at the year-five discount factor.
    led.apply(
        TERM_LEVER,
        "R-TERM-01",
        TERM_LANDED if TERM_LANDED is not None else central,
        why=("engine/terminal_value.py states the basis in its own contract and says what "
             "breaking it costs: 'Pass a NOPAT already grown by (1+g) and the terminal is "
             "overstated by exactly (1+g) — a year-seven flow discounted at the year-five "
             "factor.' Both call sites did it, on nopat, on dna_book and on working_capital. "
             "The parked-construction depreciation catch-up deducted beside the NOPAT is "
             "cip[-1] x dep_rate, a FY2030E balance at the annual rate, so it is ALREADY on "
             "the last-explicit-year basis and is deducted at full value rather than "
             "deflated — the correction is the removal of a growth factor, not the division "
             "of an expression."),
        evidence=("rebuilt through the same sanctioned module: terminal value %.1f -> %.1f "
                  "(%+.2f%%) on Frame A and %.1f -> %.1f (%+.2f%%) on Frame B; value per "
                  "share %.4f -> %.4f (%+.2f%%) and %.4f -> %.4f (%+.2f%%). The share effect "
                  "exceeds the terminal effect because the bridge is geared — net debt %.1f "
                  "against equity %.1f on Frame A. The superseded construction, rebuilt "
                  "through the module, reproduces the previous edition's published pair "
                  "exactly, which is the evidence that this pass moved one thing."
                  % (A["terminal_record"]["superseded_grown_basis"]["tv"], A["tv"],
                     100 * (A["tv"] / A["terminal_record"]["superseded_grown_basis"]["tv"] - 1),
                     Bf["terminal_record"]["superseded_grown_basis"]["tv"], Bf["tv"],
                     100 * (Bf["tv"] / Bf["terminal_record"]["superseded_grown_basis"]["tv"] - 1),
                     A["per_share_superseded_grown_basis"], A["per_share"],
                     100 * (A["per_share"] / A["per_share_superseded_grown_basis"] - 1),
                     Bf["per_share_superseded_grown_basis"], Bf["per_share"],
                     100 * (Bf["per_share"] / Bf["per_share_superseded_grown_basis"] - 1),
                     A["net_debt"], A["equity"])))
    # EIGHTH LEVER — SIGCM clause 6. Two defects in one input line, and the second is
    # why the first survived.
    if abs(led.value - central) > 1e-9:
        led.apply(
            BETA_LEVER,
            "SIGCM-6",
            central,
            why=("the beta was regressed against an EQUAL-WEIGHT COMPOSITE of 36 covered "
                 "Egyptian names, and the study said so in its own source field. A "
                 "constituent composite is not a weaker tier: it changes whenever a stock "
                 "is posted and it shares constituents with the panel it prices, so it is "
                 "a coverage artefact rather than a market, which is why SIGCM clause 6 "
                 "calls it a hard fail. AND THE NUMBER WAS TYPED — the input carried a "
                 "literal 0.629, so re-running the regression to any answer at all would "
                 "have left the model discounting at the old one. Running it first and "
                 "watching the valuation not move is how that was found. The correction "
                 "moves both frames FURTHER BELOW a price they already sit far below."),
            evidence=("beta_regression.own_stock_beta('PHAR','EG','EGX') against "
                      "raw_indices/EG/EGX30.csv as at 2026-09-08: beta 0.6658, R-squared "
                      "0.143, n 256, standard error 0.1355, 90%% interval [0.443, 0.889], "
                      "Dimson-corrected and matched to the exchange's own trading week. "
                      "THE WITHDRAWN COMPOSITE FIT BETTER — 0.6295 at an R-squared of "
                      "0.235 — and that is recorded rather than left out: a basket sharing "
                      "constituents with the panel it prices will track a member of that "
                      "panel more closely than a blue-chip index does, and a better fit "
                      "against the wrong regressor is not evidence for the wrong "
                      "regressor. Frame A %.4f -> %.4f, Frame B %.4f -> %.4f."
                      % (TERM_LANDED if TERM_LANDED is not None else central, central,
                         49.678879191581700, NUM["central_two_sided"]["branches"][1]["value"])))

    assert abs(led.value - central) < 1e-9, (
        "the ledger's last lever must reach the answer the study publishes: %r vs %r"
        % (led.value, central))
    return led


if __name__ == "__main__":
    led = build()
    rec = led.record()
    RL.assert_rebuild(rec, "PHAR")
    json.dump(rec, open(LEDGER, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("PHAR rebuild ledger — %d levers, %d distinct rules" %
          (len(rec["levers"]), rec["distinct_rules"]))
    for lv in rec["levers"]:
        print("  %-58s %-12s %9.4f -> %9.4f  %+6.1f%%"
              % (lv["name"][:58], lv["rule"], lv["before"], lv["after"], 100 * lv["move"]))
    print("  cumulative %+.1f%%   answer %.6f" % (100 * rec["cumulative_move"], rec["value"]))
