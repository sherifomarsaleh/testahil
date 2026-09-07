"""Part E criterion 3, measured clause by clause instead of summarised in one line.

WHY THIS EXISTS. `acceptance.py` carried criterion 3 as a single sentence —
"the valuation calibration's pooled bias CI covering zero — its own scorer
returns a DATE until the first vintages mature, by design" — and that sentence
NAMES THE WRONG SCORE. [R-VCAL-01] fixes TWO series and `score.py` says so in
its own docstring: (i) CONTEMPORANEOUS AGREEMENT, log(FV/P) at every origin,
"measurable the moment a vintage exists"; (ii) GAP CLOSURE, whether that lean
predicts subsequent returns, which cannot mature before 2027-06-11.

Criterion 3 as WRITTEN in Part E opens on series (i):

    "The valuation calibration's pooled CONTEMPORANEOUS bias, log(FV/P) at
     every origin, has a 90% block-bootstrap CI that includes zero, is
     LONO-stable in sign, and holds in both eras; the gap-closure series shows
     whether any residual lean predicts returns; the method beats 'FV = price'
     and 'trailing P/E x EPS' on MAE; the decomposition attributes any residual
     bias to a named lever."

Read as one clock the criterion returns 2027-06-11 and every other clause is
invisible behind it. Read clause by clause, FOUR of the six are measurable
today and are NOT met for reasons that are work rather than waiting — which is
a different fact about the programme, and the one the reader actually needs.

THE FORWARD HALF CANNOT BE A PHASE 1 BLOCKER, AND THE ARGUMENT IS THE PLAN'S
OWN TEXT RATHER THAN A CONVENIENCE. Part D: "Phase 2 does not start until Phase
1's walk-forward record shows the method unbiased within its confidence
interval". Phase 2b acceptance: "the first forward cohort STRUCK AFTER 2a
CLOSED has matured". So a matured forward cohort requires Phase 2a closed,
which requires Phase 1 done. If Phase 1 required the forward reading, Phase 1
would require Phase 2a would require Phase 1. THE READING IS CIRCULAR AND SO
CANNOT BE THE INTENDED ONE. The forward half is already carried, in the same
words, by Phase 2b's own acceptance clause — where the plan also says its end
date "is a maturity date, not a throughput estimate, and must never be
published as one". It was published as one, to the principal, on 07-09-2026.

This module RE-READS the committed artefacts and re-runs their own scorers
[R-ENF-03]; it re-implements no arithmetic. An unmeasured clause is UNMEASURED,
never met [R-ENF-04], and a clause whose object does not exist says so.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
VCAL = os.path.join(ENGINE, "valuation_calibration")
if VCAL not in sys.path:
    sys.path.insert(0, VCAL)
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)

CASHFLOW_SCORES = os.path.join(VCAL, "SCORES_cashflow_06-09-2026.json")

# The criterion's own words, split at its semicolons. Not paraphrased: the
# clause list is what the instrument is held to.
CLAUSES = [
    ("A", "pooled contemporaneous bias, log(FV/P) at every origin, 90% "
          "block-bootstrap CI includes zero"),
    ("B", "LONO-stable in sign"),
    ("C", "holds in both eras"),
    ("D", "the gap-closure series shows whether any residual lean predicts "
          "returns"),
    ("E", "beats 'FV = price' and 'trailing P/E x EPS' on MAE"),
    ("F", "the decomposition attributes any residual bias to a named lever"),
]


def _cashflow():
    with open(CASHFLOW_SCORES, encoding="utf-8") as fh:
        return json.load(fh)


def _covers_zero(b):
    return b is not None and b.get("lo") is not None and b["lo"] <= 0.0 <= b["hi"]


def clause_a(dec):
    """Series (a), the mechanical lens — the only series struck at EVERY origin."""
    sc = dec["score"]
    n = sc["n"]
    boots = sc.get("bootstrap") or {}
    covering = {k: _covers_zero(v) for k, v in sorted(boots.items())}
    met = bool(covering) and all(covering.values())
    lines = [
        "cells %d / origins %d / names %d" % (n["cells"], n["origins"], n["names"]),
        "mean log(FV/P) %+.4f   median %+.4f   below price %d of %d"
        % (sc["mean"], sc["median"], sc["below"], sc["below"] + sc["above"]),
    ]
    for k, b in sorted(boots.items()):
        if b is None or b.get("lo") is None:
            lines.append("block %s: no interval (too few cells)" % k)
        else:
            lines.append("block %s: %+.4f to %+.4f   %s zero"
                         % (k, b["lo"], b["hi"],
                            "COVERS" if _covers_zero(b) else "EXCLUDES"))
    return met, lines


def clause_b(dec):
    l = dec["score"].get("lono") or {}
    usable = {k: v for k, v in l.items() if v.get("mean") is not None}
    if not usable:
        return None, ["undefined: %d name(s) in the panel, so leaving one out "
                      "leaves nothing to pool" % dec["score"]["n"]["names"]]
    signs = {(v["mean"] > 0) for v in usable.values()}
    return len(signs) == 1, ["%s: mean %+.4f on %d cells"
                             % (k, v["mean"], v["cells"])
                             for k, v in sorted(usable.items())]


def clause_c(dec):
    eras = dec["score"].get("eras") or {}
    live = {k: v for k, v in eras.items() if v.get("mean") is not None}
    lines = ["%-16s cells %3d  mean %s"
             % (k, v["cells"],
                "%+.4f" % v["mean"] if v.get("mean") is not None else "—")
             for k, v in sorted(eras.items())]
    if len(live) < 2:
        return None, lines + ["only %d era populated — 'both eras' has no "
                              "second side to hold in" % len(live)]
    signs = {(v["mean"] > 0) for v in live.values()}
    return len(signs) == 1, lines


def clause_d(today=None):
    import score as vscore  # [R-ENF-03]: the scorer's own refusal, not a copy
    t = vscore.maturity_table(today or dt.date.today())
    lines = ["vintages held %d" % t["vintages"]]
    for h, row in sorted(t["by_horizon"].items()):
        lines.append("horizon %dy: mature now %d, first scoreable %s (%d days)"
                     % (h, row["mature_now"], row["first_scoreable"],
                        row["days_away"]))
    lines.append("THE ONLY MATURITY-BOUND CLAUSE IN THIS CRITERION.")
    return None, lines


def clause_e():
    return None, [
        "'FV = price' has MAE 0 against log(FV/P) BY CONSTRUCTION, so this "
        "benchmark is unbeatable on the contemporaneous score and cannot be "
        "what the clause means.",
        "It is a benchmark on SUBSEQUENT RETURNS, i.e. clause D's series — "
        "maturity-bound with it.",
    ]


def clause_f(a_met):
    if a_met:
        return None, ["conditional: no residual bias to attribute while the "
                      "interval covers zero."]
    return None, ["a residual bias EXISTS (clause A red), so this clause bites "
                  "— and no decomposition to a named lever is committed."]


def cross_section():
    """Series (b), the delivered cross-section — reported BESIDE, never AS, clause A."""
    import delivered  # [R-ENF-03]
    rows, _nonpos, _unread, _two = delivered.read_book()
    xs = [r["log_gap"] for r in rows]
    if not xs:
        return ["cross-section unreadable — not clean, merely unmeasured [R-ENF-04]"]
    lo, hi = delivered.boot(xs)
    clo, chi = delivered.boot_clustered(rows)
    return [
        "n = %d readable single-central studies, ONE origin each" % len(xs),
        "mean %+.4f   median %+.4f" % (sum(xs) / len(xs),
                                       sorted(xs)[len(xs) // 2]),
        "95%% resampling NAMES   %+.4f to %+.4f   %s zero"
        % (lo, hi, "COVERS" if lo <= 0 <= hi else "EXCLUDES"),
        "95%% resampling MARKETS %+.4f to %+.4f   %s zero"
        % (clo, chi, "COVERS" if clo <= 0 <= chi else "EXCLUDES"),
        "NOT clause A's object: the criterion says AT EVERY ORIGIN and this is "
        "one origin per name. It is stated so the two are not confused, which "
        "is how a criterion gets reported met on the wrong series.",
    ]


def blocking(dec):
    """Why series (a) scores on one name — the taxonomy the drops already carry."""
    import collections
    c = collections.Counter()
    for r in dec.get("dropped", []):
        why = r["why"]
        for head in ("capex intensity needs",
                     "terminal refused: implied payout",
                     "terminal refused: terminal free cash flow",
                     "the projection runs to horizon"):
            if why.startswith(head):
                c[head] += 1
                break
        else:
            c[why[:56]] += 1
    return c


def main():
    today = dt.date.today()
    print("Part E criterion 3 — CLAUSE BY CLAUSE, printed not attested")
    print("read %s\n" % today.isoformat())
    print("  THE CRITERION OPENS ON THE **CONTEMPORANEOUS** SCORE. acceptance.py")
    print("  summarised it as the maturity-bound one and returned a 2027 date for")
    print("  the whole criterion. Four of its six clauses do not wait on a clock.\n")

    d = _cashflow()
    dec = d["DECLARED"]

    verdicts = {}
    print("=" * 74)
    a_met, lines = clause_a(dec)
    verdicts["A"] = a_met
    print("A  %s" % CLAUSES[0][1])
    print("   SERIES (a), the mechanical lens — struck at every origin")
    for l in lines:
        print("     " + l)
    print("   -> %s\n" % ("MET" if a_met else "NOT MET"))

    for tag, fn in (("B", lambda: clause_b(dec)), ("C", lambda: clause_c(dec))):
        met, lines = fn()
        verdicts[tag] = met
        print("%s  %s" % (tag, dict(CLAUSES)[tag]))
        for l in lines:
            print("     " + l)
        print("   -> %s\n" % ("MET" if met else
                              "NOT MET" if met is False else "UNMEASURED"))

    for tag, fn in (("D", clause_d), ("E", clause_e),
                    ("F", lambda: clause_f(a_met))):
        met, lines = fn()
        verdicts[tag] = met
        print("%s  %s" % (tag, dict(CLAUSES)[tag]))
        for l in lines:
            print("     " + l)
        print("   -> %s\n" % ("MET" if met else
                              "NOT MET" if met is False else "UNMEASURED"))

    print("=" * 74)
    print("BESIDE IT — series (b), the delivered cross-section")
    for l in cross_section():
        print("  " + l)

    print("\n" + "=" * 74)
    print("WHAT ACTUALLY BLOCKS A, B AND C — and none of it is a clock")
    tot = len(dec.get("dropped", []))
    print("  %d cells scored, %d dropped" % (dec["score"]["n"]["cells"], tot))
    for why, n in blocking(dec).most_common():
        print("    %3d  %s" % (n, why))
    print("  The largest class is a DATA-CARRY job: [R-FCAL-01 AMENDED "
          "03-Sep-2026]")
    print("  already requires the valuation-input block at every origin, and "
          "carrying")
    print("  it further back is a copy out of filings each run has parsed.")

    print("\n" + "=" * 74)
    print("VERDICT")
    print("  criterion 3 is NOT MET.")
    print("  It is not met because the mechanical series scores on ONE name,")
    print("  which is work with a rate — not because of the 2027 maturity date")
    print("  that clauses D and E carry and that acceptance.py reported for the")
    print("  whole criterion.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
