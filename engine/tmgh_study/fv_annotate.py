"""Annotate the TMGH movement record: what the second rebuild changed, and why.

Kept as a script rather than typed into the store by hand, so the reasoning is
committed beside the numbers it explains and a later session can see how the
record came to say what it says.
"""

import json
import os

STORE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "fv_movement.json")

NOTE = (
    "Second rebuild, after the first was rejected as well. FIVE further "
    "structural errors, each one masking the next, and every one of them making "
    "the company shrink. "
    "(1) NEW SALES HELD FLAT IN NOMINAL TERMS while hospitality grew at 20% and "
    "other recurring at 22% — an 84% REAL decline across the window that nobody "
    "decided on. It was the 15% fade again, wearing inflation instead of a "
    "parameter. "
    "(2) TERMINAL GROWTH OF 15% against nominal growth near 20% — a perpetual "
    "real decline, also undecided. "
    "(3) THE CRUX WAS THE WRONG QUESTION. 'How long does a static book take to "
    "convert' forced deliveries to a fraction of a book that kept growing. It is "
    "now HOW FAST TMG CAN BUILD, anchored on the company's own 28.5% compound "
    "delivery growth from 2019 to 2025, with contracted sales as the balancing "
    "item that holds the book at cover — because a company selling ten times what "
    "it delivers is bounded by construction, not by demand. "
    "(4) THE TERMINAL TREATED THE COMPANY AS A PIPELINE EMPTYING OUT. A level "
    "annuity on the residual book valued EGP 1.6 TRILLION of contracted, "
    "already-sold backlog at about EGP 9bn, because at 35.79% an annuity starting "
    "in year eleven is worth almost nothing. It is now a going concern with a "
    "two-stage fade from the crux rate to the economy's rate. "
    "(5) ADVANCES WERE TIED TO THE ORDER BOOK AND LAGGED FOUR YEARS, so growth "
    "CONSUMED cash — contradicted by a balance sheet holding EGP 47bn of cash and "
    "deposits against EGP 17bn of borrowings while deliveries grew 28.5% a year. "
    "Advances are 90.3% of work in progress at the balance-sheet date and now "
    "track it in-year. "
    "THE TELL THAT THE MODEL WAS FINALLY COHERENT: building FASTER is now worth "
    "MORE — the faster reading is EGP 54.08 against the slower one's EGP 43.94. "
    "It had been the other way round, which is what a broken cash-flow "
    "construction looks like from the outside.")

OPEN_QUESTION = (
    "The discount rate is the whole of the residual gap and it is NOT resolved "
    "here. On the house method (WACC 35.79%) the range is EGP 43.94–54.08; on the "
    "CDS premium basis (32.37%) EGP 54.39–69.95; and counting country risk ONCE "
    "rather than multiplying it by a beta measured against EGX30 — the standard "
    "treatment for an issuer whose revenues are all domestic — the WACC is 31.57% "
    "and the range EGP 57.76–75.18. The market implies 23.09%; reaching the "
    "market price needs roughly 23–25%. Whether a 1.4718 price beta should lever "
    "a 9.71% country risk premium is a change to the STANDING cost-of-capital "
    "method and not a study decision, so all three are computed and published and "
    "none is adopted unilaterally.")


def main():
    d = json.load(open(STORE, encoding="utf-8"))
    e = d["entries"]["TMGH"]
    for i in (0, 1):
        e["editions"][i]["superseded_by"] = "edition 3"
    e["editions"][2]["note"] = NOTE
    e["editions"][2]["open_question"] = OPEN_QUESTION
    json.dump(d, open(STORE, "w", encoding="utf-8"), indent=1, sort_keys=True)
    open(STORE, "a", encoding="utf-8").write("\n")
    print("TMGH edition 3 annotated; editions 1 and 2 marked superseded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
