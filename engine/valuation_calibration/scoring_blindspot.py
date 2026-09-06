"""What the log score does not score, and which way the omission runs.

EVERY DRIVER BIAS THIS HOUSE PUBLISHES IS A LOG ERROR, and a log error needs both
the projection and the actual to be POSITIVE. That is not a rounding detail on a
profit line: a cell where the model projected a loss, or where the company made
one, is dropped -- silently, from a mean everyone then reads as the driver's bias.

THE EXCLUSION IS NOT RANDOM: it removes exactly the cells where a loss appears on
one side or the other. WHAT IT IS NOT is one-signed. Measured on this book, 13 of
28 drivers lose cells, and of those only 5 show a larger bias on the full sample
-- the other 8 show a larger one on the taken subset. A first draft of this file
asserted the flattering direction and the measurement refused it.

THAT IS THE WORSE OF THE TWO OUTCOMES AND IT IS WHY THIS MATTERS. A known lean
can be corrected for. A published figure that differs from the full sample by up
to five times in EITHER direction cannot, and nothing on the page says which way
this one went. What IS consistent is WHERE it happens: revenue and cost are
always positive and lose nothing, so the distortion falls entirely on the
bottom-line drivers a valuation depends on.

MEASURED, ON THE RUNS' OWN COMMITTED PROJECTIONS. For each driver: how many cells
exist, how many the log score takes, and the bias on ALL cells against the bias on
the taken subset -- BOTH IN THE SAME METRIC, relative error, so the comparison is
about the SAMPLE and not about the scale. Comparing a log figure with a relative
one would be the ratio-of-two-different-quantities mistake this repository has
already paid for.

RELATIVE ERROR IS USED HERE AND IS NOT PROPOSED AS A REPLACEMENT. It has its own
faults -- it is unbounded below and asymmetric -- and swapping the house score on
the strength of this file would be exactly the selection this method forbids.
What it is used for is to hold the two SAMPLES against each other in one metric,
which is a narrower claim and the one the numbers support.

Read live: python3 engine/valuation_calibration/scoring_blindspot.py
"""
import os, sys, math, json

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)

# (name, directory, adapter, the drivers to inspect)
RUNS = [
    ("EGCH", "egch_walkforward", "module",
     ["revenue", "cost_of_sales", "gross_profit", "selling", "provisions",
      "other_bucket", "fx", "debit_interest", "pbt", "tax_current", "net"]),
    ("AMOC", "amoc_walkforward", "module",
     ["net_sales", "cost_of_sales", "gross_profit", "operating_profit",
      "claims_provision", "other_revenues", "pbt", "income_tax", "npat", "majority"]),
    ("ARCC", "arcc_walkforward", "module",
     ["revenue", "cogs", "gross_profit", "pbt", "tax", "pat", "majority"]),
]


def cells(d, drivers):
    p = os.path.join(ENG, d)
    sys.path.insert(0, p)
    for m in ("bottom_up", "panel", "score", "macro"):
        sys.modules.pop(m, None)
    try:
        import bottom_up as B
        P = None
        try:
            import panel as P
        except Exception:
            pass
        act = getattr(B, "actual", None) or getattr(P, "actual")
        out = {k: [] for k in drivers}
        for o, h, t in B.cells():
            pr, a = B.project(o, h), act(t)
            for k in drivers:
                pv, av = pr.get(k), a.get(k)
                if pv is None or av is None or av == 0:
                    continue
                log = math.log(pv / av) if (pv > 0 and av > 0) else None
                out[k].append((log, (pv - av) / abs(av)))
        return out
    finally:
        sys.path.remove(p)


def main():
    mean = lambda v: (sum(v) / len(v)) if v else None
    rows, notes = [], []
    print("What the log score does not score\n")
    print("%-6s %-18s %5s %5s %6s %11s %11s %8s" %
          ("name", "driver", "cells", "taken", "%", "bias ALL", "bias TAKEN", "factor"))
    for name, d, _adapter, drivers in RUNS:
        if not os.path.isdir(os.path.join(ENG, d)):
            notes.append((name, "no run directory on disk"))
            continue
        try:
            got = cells(d, drivers)
        except Exception as e:
            notes.append((name, str(e)[:70]))
            continue
        for k in drivers:
            v = got.get(k) or []
            if not v:
                continue
            taken = [x for x in v if x[0] is not None]
            b_all = mean([r for _, r in v])
            b_tak = mean([r for l, r in taken])
            factor = (abs(b_all) / abs(b_tak)) if (b_tak not in (None, 0)) else None
            rows.append({"name": name, "driver": k, "cells": len(v),
                         "taken": len(taken), "bias_all": b_all, "bias_taken": b_tak,
                         "factor": factor})
            print("%-6s %-18s %5d %5d %5.0f%% %+11.3f %11s %8s" %
                  (name, k, len(v), len(taken), 100 * len(taken) / len(v), b_all,
                   ("%+.3f" % b_tak) if b_tak is not None else "not scored",
                   ("%.1fx" % factor) if factor else "-"))
    for name, why in notes:
        print("%-6s NOT MEASURED -- %s" % (name, why))
    if not rows:
        raise SystemExit("FAIL: no driver measured -- that is not a clean result")

    partial = [r for r in rows if r["taken"] < r["cells"]]
    understated = [r for r in partial
                   if r["bias_taken"] is not None and r["bias_all"] is not None
                   and abs(r["bias_all"]) > abs(r["bias_taken"])]
    print("\n%d of %d drivers lose cells to the log score, and where it happens the two"
          % (len(partial), len(rows)))
    print("samples disagree by a lot -- up to %.1fx on this book."
          % max(r["factor"] for r in partial if r["factor"]))
    print("\nTHE OMISSION IS NOT ONE-SIGNED, AND SAYING SO IS THE FINDING RATHER THAN A")
    print("CAVEAT ON IT. Of the %d drivers that lose cells, %d show a LARGER bias on the"
          % (len(partial), len(understated)))
    print("full sample and %d show a SMALLER one. So the published figure is not"
          % (len(partial) - len(understated)))
    print("systematically flattering -- it is unreliable in an unknown direction, which is")
    print("the worse of the two: a known lean can be corrected for and this cannot.")
    print("A first draft of this file asserted the flattering direction on five of thirteen")
    print("cases and is corrected here rather than quietly rephrased.")
    print("\nWhat IS one-signed is the size. Where the samples disagree they disagree")
    print("materially, and the biggest gaps sit on the BOTTOM-LINE drivers a valuation")
    print("depends on -- not on revenue and cost, which are always positive and lose nothing.")
    unscored = [r for r in rows if r["taken"] == 0]
    for r in unscored:
        print("\n%s %s is scored on NONE of its %d cells; its bias on all of them is %+.3f."
              % (r["name"], r["driver"], r["cells"], r["bias_all"]))
        print("It appears in no table this house publishes.")
    json.dump(rows, open(os.path.join(HERE, "scoring_blindspot.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
