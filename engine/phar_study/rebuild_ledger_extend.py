#!/usr/bin/env python3
"""PHAR rebuild ledger [R-REBUILD-01] — EXTENDED, never restarted.

The five levers of 4 September 2026 stand exactly as recorded.  This pass appends
the sixth: the FUNDAMENTAL walk-forward [R-FCAL-01] of 7 September 2026.

AUDIT POINT, DECLARED BEFORE THE PASS BEGAN AND NOT AFTER IT: after the
walk-forward's corrections are dispositioned and BEFORE the price is consulted
for the gap review.  That is the same shape as the ledger's original audit point
— stop once the levers serving one rule are complete — and it is the place that
would have caught this study's own +45%-then-back-down route in September.

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
         "is consulted for the gap review.")


def build():
    old = json.load(open(LEDGER, encoding="utf-8"))
    led = RL.Ledger(ticker=old["ticker"], started_at=old["started_at"],
                    start_value=old["start_value"], start_spot=old["start_spot"],
                    audit_after=AUDIT)
    for lv in old["levers"]:
        led.apply(lv["name"], lv["rule"], lv["after"], lv.get("why", ""),
                  lv.get("evidence", ""))

    central = json.load(open(os.path.join(HERE, "study_numbers.json"),
                             encoding="utf-8"))["central_two_sided"]["branches"][0]["value"]
    assert abs(central - led.value) < 1e-6, (
        "the ledger's last lever must reach the answer the study publishes: %r vs %r"
        % (led.value, central))

    led.apply(
        "the fundamental walk-forward ran and adopted no correction",
        "R-FCAL-01",
        central,
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
