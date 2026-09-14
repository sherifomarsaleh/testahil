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

# WHICH PHASE EACH CLAUSE BELONGS TO [CORRECTED 07-09-2026, per instruction — "we chose
# backtesting for that particular purpose. We back test and in the future we calibrate and
# enhance as we go along and compare our predictions now with what the future unfolds. So
# as far as my rule is concerned. We backtest."]
#
# THE PLAN ALREADY SAID THIS AND CRITERION 3 WAS WRITTEN AS THOUGH IT DID NOT. Part D
# separates the phases in terms: Phase 1 and 2a are the BACKTEST — "it is finished when its
# names are also backtested" — while Phase 2b is "the live test, going forward: from the
# day 2a closes, every fair value the house publishes is a dated claim graded against what
# actually happens". Clauses D and E score exactly that forward series, and criterion 3
# gated PHASE 1 on it.
#
# THE ARGUMENT IS STRONGER THAN THE INSTRUCTION AND IT IS THE PLAN'S OWN. 2b says in terms
# that it "grades ONLY claims struck after 2a closed", and gives the reason: "no claim
# inside 2b was made by a method that had not already passed its historical test, so a 2b
# result cannot be explained away as the old method's residue." EVERY ONE OF THE 103
# VINTAGES NOW HELD WAS STRUCK BEFORE 2a — so clause D, read as a Phase 1 gate, demands
# evidence the programme's own design declares INADMISSIBLE. It was not merely early; it
# was asking the wrong question of the wrong sample.
#
# WHAT THIS DOES NOT DO, STATED RATHER THAN DISCOVERED LATER: Phase 1 now closes with NO
# evidence that this house's lean is INFORMATION rather than merely a lean. That is a real
# loss and it is not softened here — it is precisely what Phase 2b exists to supply, on a
# sample that can actually answer it, and [R-VCAL-01]'s promotion guard stays symmetric in
# the meantime. D and E are REPORTED at every run with their maturity date, so the debt is
# visible rather than dropped; what changes is that they no longer hold the book.
# [R-VCAL-02] is the rule this map implements.
PHASE = {"A": 1, "B": 1, "C": 1, "F": 1, "D": "2b", "E": "2b"}
GATING = [c for c in "GBCF"]   # [R-VCAL-02 CLAUSE THREE]: G replaces A


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
    # THE KEY IS THE NAME LEFT OUT, NOT THE NAME MEASURED, and printing it bare read
    # as the opposite: with PHDC holding six cells and TMGH one, the line "PHDC: mean
    # -0.3478 on 1 cells" states TMGH's figure under PHDC's name. The scorer is right
    # and the rendering was the defect, so the label says WITHOUT.
    return len(signs) == 1, ["without %-6s the remaining %d cell(s) mean %+.4f"
                             % (k, v["cells"], v["mean"])
                             for k, v in sorted(usable.items())]


def clause_c(dec):
    """Does the sign hold in both eras — where an era is thick enough to be a side.

    A POPULATED ERA IS NOT THE SAME THING AS A SIDE, and reading it as one made this
    clause report MET on a single observation the first time a second era was
    populated at all: six cells against one, signs agreeing, verdict MET. This book
    already refuses exactly that reading in [R-FCAL-01 AMENDED 07-09-2026] — a cut is
    admitted only where it leaves at least five cells each side, and a quantity too
    thin to cut is UNTESTABLE, never counted stable, because an absence of contrary
    evidence is not evidence [R-ENF-04].

    THE THRESHOLD IS BORROWED AND NOT MINTED, which is the only honest justification
    for a number: boundary_sensitivity.MIN_SIDE is the bound this house already uses
    for this exact question, IMPORTED rather than retyped so the two cannot drift
    [R-ENF-03]. Fewer than two sides survive it and the clause is UNTESTABLE — which
    is what it was before, and is a weaker claim than MET rather than a stronger one.
    """
    sys.path.insert(0, VCAL)
    from boundary_sensitivity import MIN_SIDE  # noqa: E402

    eras = dec["score"].get("eras") or {}
    live = {k: v for k, v in eras.items() if v.get("mean") is not None}
    sides = {k: v for k, v in live.items() if v["cells"] >= MIN_SIDE}
    lines = ["%-16s cells %3d  mean %s%s"
             % (k, v["cells"],
                "%+.4f" % v["mean"] if v.get("mean") is not None else "—",
                "" if v["cells"] >= MIN_SIDE else
                "   TOO THIN TO BE A SIDE (needs %d)" % MIN_SIDE)
             for k, v in sorted(eras.items())]
    if len(sides) < 2:
        return None, lines + [
            "%d era(s) populated and %d thick enough to be a side at %d cells — "
            "'both eras' has no second side to hold in, and an era of one "
            "observation is untestable rather than agreeing"
            % (len(live), len(sides), MIN_SIDE)]
    signs = {(v["mean"] > 0) for v in sides.values()}
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
    """READ, never asserted [R-ENF-01].

    This clause returned a hardcoded sentence and consulted nothing, so it could
    never have gone green however much work was done — which is a claim about the
    checker rather than about the book. It now reads the committed decomposition,
    and an UNREADABLE one is reported as unreadable rather than as absent [R-ENF-04].
    """
    if a_met:
        return None, ["conditional: no residual bias to attribute while the "
                      "interval covers zero."]
    p = os.path.join(ENGINE, "valuation_calibration",
                     "CLAUSE_F_DECOMPOSITION_08-09-2026.json")
    if not os.path.exists(p):
        return None, ["a residual bias EXISTS (clause A red), so this clause bites "
                      "— and no decomposition to a named lever is committed."]
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as exc:
        return None, ["the committed decomposition will not parse (%s) — "
                      "unreadable is not absent and is not clean"
                      % type(exc).__name__]
    need = ("the_lever", "pooled_bias", "pooled_bias_held_to_filed_peak",
            "attributed_share", "n_breaching", "cells")
    miss = [k for k in need if d.get(k) is None]
    if miss:
        return None, ["the committed decomposition is missing %s" % ", ".join(miss)]
    return True, [
        "the lever is NAMED and carries a standing rule: [R-ANCHOR-01 CLAUSE "
        "THREE], a forecast rate climbing past everything the company has FILED.",
        "a mechanical lens cannot name a mechanism for such a rise — it is "
        "forbidden judgement drivers by construction — so the rise is a claim "
        "nothing in the lens is entitled to make.",
        "pooled bias %+.4f; held to each name's filed peak AS AT ITS ORIGIN, "
        "%+.4f" % (d["pooled_bias"], d["pooled_bias_held_to_filed_peak"]),
        "ATTRIBUTES %.1f%% of the residual, on %d of %d cells"
        % (100 * d["attributed_share"], d["n_breaching"], len(d["cells"])),
        "the attribution is CONCENTRATED and that is reported rather than "
        "smoothed: one cell carries most of it.",
        "AN ATTRIBUTION, NEVER A PROMOTED LEVER — no published fair value moves.",
    ]


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


def _market_census():
    """Which market each completed walk-forward run belongs to.

    ANCHORED ON THE RUN DIRECTORIES ON DISK per [R-ENF-04], never on a written
    list: a market list in a document goes stale the moment a run is added, which
    is the same reason the stale-library list was retired. The resolver is
    panel.find_market(), imported rather than reimplemented [R-ENF-03].
    """
    import glob
    sys.path.insert(0, VCAL)
    import panel as _P  # noqa: E402
    out = {}
    for d in sorted(glob.glob(os.path.join(ENGINE, "*_walkforward"))):
        tk = os.path.basename(d).split("_")[0].upper()
        out.setdefault(_P.find_market(tk) or "unresolved", set()).add(tk)
    return out


AUDIT_BAR = 0.10          # [R-GAP-01]'s own audit trigger, BORROWED never minted:
#                           a second cutoff for the same question would be the free
#                           parameter the PROMOTION RULE forbids.
AUDIT_GLOB = "EXPENSIVE_CALLS_AUDIT_*.md"


def _audit_path():
    """Resolve the audit BY PATTERN, exactly one, or fail loudly.

    It was a dated filename typed into this file. That is a second copy of a fact
    that moves: the audit is re-issued on the day it is rewritten, and the clause
    would then stop finding it and report that none is committed — a true sentence
    about the wrong file. The digest resolver already works this way for the same
    reason, and the rule is the same: exactly one file on the pattern, or say so.
    TWO audits are refused rather than the newest taken, because a criterion that
    silently picks among candidates is choosing its own evidence.
    """
    import glob as _g
    hits = sorted(_g.glob(os.path.join(ENGINE, "valuation_calibration", AUDIT_GLOB)))
    if len(hits) == 1:
        return hits[0], None
    if not hits:
        return None, "no committed audit on %s" % AUDIT_GLOB
    return None, ("%d audits match %s and a criterion may not choose among them: %s"
                  % (len(hits), AUDIT_GLOB,
                     ", ".join(os.path.basename(h) for h in hits)))


def clause_g(dec):
    """[R-VCAL-02 CLAUSE THREE] — the bar that REPLACES clause A for Phase 1.

    Per instruction: "I am not worried if we say something is cheap. Because some
    markets and some companies are genuinely cheap. I am concerned if we say a
    company is expensive by more than 10%." NO COMPANY IS CALLED EXPENSIVE BY MORE
    THAN TEN PER CENT WITHOUT AN AUDIT BEHIND IT.

    READ, NEVER ASSERTED [R-ENF-01]. The population comes from the SCORE — every
    cell more than the bar below the price it was struck against — and each one
    must be NAMED in the committed audit. A cell the audit does not name is a
    breach; an audit naming a cell that no longer breaches is not an error, since
    a fixed cell is exactly what the audit is for. AN UNREADABLE AUDIT IS NOT A
    CLEAN ONE [R-ENF-04].
    """
    rows = dec.get("cells") or []
    if not rows:
        return None, ["no scored cell to hold to the bar — a run that read nothing "
                      "is not a run that found nothing [R-ENF-04]"]
    breach = [r for r in rows
              if r.get("price") and r["fv"] / r["price"] - 1.0 < -AUDIT_BAR]
    p, why = _audit_path()
    if p is None:
        return None, ["%d cell(s) call a company expensive by more than %.0f%%: %s"
                      % (len(breach), 100 * AUDIT_BAR, why)]
    try:
        txt = open(p, encoding="utf-8").read()
    except Exception as exc:
        return None, ["the committed audit will not read (%s) — unreadable is not "
                      "clean" % type(exc).__name__]
    missing = [r for r in breach
               if ("%s %d" % (r["ticker"], r["origin"])) not in txt]
    lines = ["THE BAR IS ONE-SIDED BY INSTRUCTION and its cost is recorded in the "
             "rule: an acceptance criterion that fires one way is the shape "
             "[R-GAP-01 AMENDED] refused for a delivery gate.",
             "%d of %d cell(s) sit more than %.0f%% BELOW the price they were "
             "struck against" % (len(breach), len(rows), 100 * AUDIT_BAR)]
    for r in sorted(breach, key=lambda x: x["fv"] / x["price"]):
        named = ("%s %d" % (r["ticker"], r["origin"])) in txt
        lines.append("  %-6s %d  %+7.1f%%   %s"
                     % (r["ticker"], r["origin"],
                        100 * (r["fv"] / r["price"] - 1.0),
                        "audited" if named else "NOT NAMED IN THE AUDIT"))
    if missing:
        lines.append("%d cell(s) are not named in the committed audit." % len(missing))
        return None, lines
    lines.append("every one is named in %s, with its cause established by "
                 "measurement." % os.path.basename(p))
    return True, lines


def verdicts():
    """The Phase 1 clause verdicts, as a dict, WITHOUT printing anything.

    Exists so nothing downstream has to keep its own copy of what Phase 1 is.
    [R-VCAL-02] requires the publish block and this criterion to agree, and the
    only safe way to write a standard twice is for the second copy to be a CALL
    rather than a transcription -- progress.acceptance() carried criterion 3 as a
    hardcoded BLOCKED and went on saying so after the clauses had moved, which is
    a check holding its own copy of a standard and is what [R-ENF-03] refuses.

    The cross-section, the market census and the drop census are NOT computed
    here: they are reporting, they are slow, and a caller asking "is Phase 1 met"
    should not pay for them.
    """
    d = _cashflow()
    dec = d["DECLARED"]
    out = {}
    out["G"], _ = clause_g(dec)
    out["A"], _ = clause_a(dec)
    out["B"], _ = clause_b(dec)
    out["C"], _ = clause_c(dec)
    out["F"], _ = clause_f(out["A"])
    out["_gating"] = list(GATING)
    out["_met"] = all(out.get(c) is True for c in GATING)
    return out


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
    g_met, glines = clause_g(dec)
    verdicts["G"] = g_met
    print("G  no company called expensive by more than 10% without an audit behind it")
    print("   [R-VCAL-02 CLAUSE THREE] — GATES Phase 1 IN PLACE OF CLAUSE A")
    for l in glines:
        print("     %s" % l)
    print("   -> %s\n" % ("MET" if g_met else "NOT MET"))

    a_met, lines = clause_a(dec)
    verdicts["A"] = a_met
    print("A  %s" % CLAUSES[0][1])
    print("   SERIES (a), the mechanical lens — struck at every origin")
    for l in lines:
        print("     " + l)
    print("   -> %s   [REPORTED, no longer gating — see clause G]\n"
          % ("MET" if a_met else "NOT MET"))

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
    print("PHASE — WHICH CLAUSES GATE PHASE 1 AND WHICH BELONG TO 2b")
    print("  GATING (Phase 1, the BACKTEST): %s" % ", ".join(GATING))
    print("  REPORTED, no longer gating: A — [R-VCAL-02 CLAUSE THREE] replaced the")
    print("  symmetric zero-bias test with the one-sided audit bar, per instruction.")
    print("  A SYMMETRIC ZERO-BIAS TEST PENALISES A METHOD FOR DOING THE THING IT IS")
    print("  FOR, and this house exists to find companies that are cheap. The COST is")
    print("  that Phase 1 no longer bounds how cheap the method may lean; what guards")
    print("  it is that [R-GAP-01]'s delivery audit stays TWO-SIDED, [R-VCAL-01]'s")
    print("  promotion guard stays SYMMETRIC, and 2b remains the only thing that can")
    print("  say whether a lean is information.")
    print("  REPORTED (Phase 2b, the LIVE forward record): D, E")
    print("  Part D of the plan separates these in terms and 2b grades ONLY claims")
    print("  struck after 2a closed. All 103 vintages held were struck BEFORE it, so")
    print("  clause D as a Phase 1 gate asks for evidence 2b itself declares")
    print("  inadmissible. Reported here with their date; they no longer hold the book.")
    print("  THE COST IS STATED: Phase 1 closes with no evidence that the house lean is")
    print("  INFORMATION rather than merely a lean. That is what 2b supplies.")

    print("\n" + "=" * 74)
    print("MARKET COVERAGE — WHAT THIS BACKTEST HAS AND HAS NOT SEEN")
    _mk = _market_census()
    for m, names in sorted(_mk.items()):
        print("  %-3s  %2d run(s): %s" % (m, len(names), ", ".join(sorted(names))))
    print("  THE SERIES IS SCORED ON ONE MARKET AND THAT IS THE CAMPAIGN'S OWN ORDER,")
    print("  NOT AN UNMEASURED GAP [per instruction 08-09-2026 — 'We adopt the")
    print("  framework. Apply it to EGX, then UAE, etc.']. campaign_queue.py fixes the")
    print("  order EGX -> UAE -> KSA -> Qatar -> India -> Korea -> USA with a HARD STOP")
    print("  after EGX, so every completed run is Egyptian by design and the exemplar")
    print("  ADNOCLS, an AE name, sits behind that stop with no run at all.")
    print("  THE COST IS STATED RATHER THAN DISCOVERED LATER, and this book has already")
    print("  paid it once: [R-TERM-01 CLAUSE TWO] was adopted BECAUSE every correction")
    print("  had come from one market and the terminal defect REVERSES SIGN in a pegged")
    print("  one — 1/g starves a kiln at 15% inflation and flatters a fleet at 2%. So a")
    print("  clause passing here is evidence about EGX, and the UAE leg is where it is")
    print("  tested rather than assumed. A finding measured on one side of a sign change")
    print("  is not a finding about the sign.")
    print("  WHAT THIS DOES NOT DO: it holds nothing. The gating clauses are G, B, C, F")
    print("  exactly as [R-VCAL-02 CLAUSE TWO] states them, and market coverage is not")
    print("  an adoption condition — it is reported so adoption happens with the limit")
    print("  on the page instead of in somebody's memory.")

    print("\n" + "=" * 74)
    print("VERDICT")
    gating_met = [verdicts.get(c) for c in GATING]
    if all(v is True for v in gating_met):
        print("  criterion 3 is MET on its Phase 1 clauses (%s)." % ", ".join(GATING))
        print("  D and E stay OPEN as Phase 2b's subject, with their maturity date.")
    else:
        bad = [c for c in GATING if verdicts.get(c) is not True]
        print("  criterion 3 is NOT MET on its Phase 1 clauses: %s." % ", ".join(bad))
        print("  It is not met because the mechanical series scores on ONE name,")
        print("  which is WORK WITH A RATE — not because of the 2027 maturity date")
        print("  that D and E carry and that acceptance.py once reported for the")
        print("  whole criterion. That date is now recorded where it belongs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
