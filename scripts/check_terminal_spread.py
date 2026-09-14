#!/usr/bin/env python3
"""[R-TERM-01] — A TERMINAL THAT REINVESTS BELOW ITS OWN COST OF CAPITAL SAYS SO.

WHY THIS EXISTS. [R-GAP-02]'s first run found the defect BY HAND, on ARCC, and recorded it
in this project's own words: the terminal charges replacement-cost invested capital, "a
terminal return on capital of 11.26% against a terminal cost of capital of 18.34%, and
then reinvests 62% of profits at that destroying spread in perpetuity to buy 7% nominal
growth", while the company's own filed accounts show returns on book capital of 43.9%,
44.3% and 60.6%. Moving only that return took the central from 53.22 to 79.27.

NOTHING IN THE STUDY WAS LOOKING AT IT, because the reinvestment rate is an OUTPUT of the
return and the growth rate and both were individually defensible — and nothing OUTSIDE the
study has looked at it since either. The finding was written into a rule as evidence and
never became an instrument, which is the shape [R-MACRO-01] names: a lesson that binds
nothing is advice.

WHAT IT CHECKS, and none of it is a threshold.

(1) THE SIGN OF THE SPREAD, WHERE THE TERMINAL REINVESTS. A terminal return beneath the
    terminal cost of capital is a legitimate finding — [R-TERM-01] says so in terms, and
    records that building capacity in that market destroys value and the model should take
    none. What is NOT ordinary is reinvesting INTO it for ever: that is a claim that the
    company will keep funding projects it knows lose money, in perpetuity, and a claim that
    strong is declared or it is an oversight. The test is the SIGN of return minus cost,
    with reinvestment strictly positive. There is no distance to argue about.

    MEASURED ON ADOPTION DAY, three studies reinvest at a negative spread and none declares
    it: ARCC 11.26% against 18.34% (-707bp), PHAR 12.73% against 15.03% (-230bp) while
    reinvesting 54.99% of terminal profit, MODON 8.50% against 11.92% (-342bp).

(2) A REINVESTMENT RATE THAT IS NOT A RATE. ARCC commits -191.8806. A share of profit
    reinvested lies in [0,1]; a figure outside it is a unit or sign error, not a policy,
    and it is reported as the different finding it is rather than swept into (1).

(3) A TERMINAL THAT REINVESTS AND COMMITS NO RETURN CANNOT BE CHECKED, so it is UNREADABLE
    and ratcheted, never silently clean [R-ENF-04]. That is the escape this gate would
    otherwise leave wide open: commit less and pass.

THE NAMES ARE TAKEN FROM WHAT THE BOOK CONTAINS, NOT FROM WHAT IT OUGHT TO. The terminal
return is committed as roic_term, roic_terminal, terminal_roic or terminal_return; the cost
as wacc_term or wacc_terminal; the reinvestment under five spellings. A reader that knew
one of them would have found four studies and reported that as a result — [L-355], which
this repository has now met three times in one day, twice inside gates written to catch
this very class.

WHAT IT DELIBERATELY DOES NOT DO. It does not test whether the terminal return is RIGHT —
that is [R-TERM-01]'s disclosed-life question and terminal_value.build() owns it. It does
not compare the terminal return against the company's filed history, which is a judgement
about comparability that a gate cannot make. It asks one thing: where the model keeps
investing for ever, does it earn more than the money costs, and if not, does the study say
so.

RATCHET [R-ENF-02] in TWO GROUPS that are not interchangeable [R-TERM-01]: one excuses a
declared-nowhere negative spread, the other a terminal that cannot be read. A study moving
between them goes red until the move is recorded. Both may only SHORTEN.
POPULATION-ANCHORED [R-ENF-04] BOTH WAYS.

USAGE
    python3 scripts/check_terminal_spread.py            # gate
    python3 scripts/check_terminal_spread.py --prune    # rewrite the ratchets SHORTER
"""
from __future__ import annotations

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit", "terminal_spread_outstanding.json")

RETURN_KEYS = ("roic_term", "roic_terminal", "terminal_roic", "terminal_return")
COST_KEYS = ("wacc_terminal", "wacc_term")
REINVEST_KEYS = ("reinvest", "reinvestment", "reinvest_rate", "reinvestment_rate",
                 "reinvest_term", "terminal_reinvestment")
# A study may say the spread is deliberate. An EMPTY reason has switched the check off
# rather than declared it, which is the release discipline every gate here uses.
DECLARE_KEY = "terminal_spread_reason"


def _find(doc, names):
    """(key, value) for the first committed figure under any of these names, at any depth."""
    hit = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lower() in names:
                    val = v.get("value") if isinstance(v, dict) else v
                    if isinstance(val, (int, float)):
                        hit.append((k, float(val)))
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(doc)
    return hit[0] if hit else (None, None)


def studies(engine=ENGINE):
    out = {}
    for d in sorted(glob.glob(os.path.join(engine, "*_study"))):
        tk = os.path.basename(d)[:-6].upper()
        g = ([p for p in (os.path.join(d, n) for n in
                          ("study_numbers.json", "numbers.json")) if os.path.exists(p)]
             or sorted(glob.glob(os.path.join(d, "*numbers*.json"))))
        if g:
            out.setdefault(tk, g[0])
    return out


def load():
    if not os.path.exists(OUTSTANDING):
        return set(), set()
    try:
        d = json.load(open(OUTSTANDING, encoding="utf-8"))
    except Exception:
        return set(), set()
    return set(d.get("outstanding", [])), set(d.get("unreadable", []))


def measure():
    """(bad, unreadable, read) — bad: {ticker: why}."""
    bad, unreadable, read = {}, {}, 0
    for tk, path in sorted(studies().items()):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception as exc:
            unreadable[tk] = "numbers file will not parse: %s" % exc
            continue
        rk, rv = _find(doc, REINVEST_KEYS)
        if rk is None:
            continue                       # a terminal that reinvests nothing is not in scope
        read += 1

        if not (0.0 <= rv <= 1.0):
            bad[tk] = ("%s is committed as %.4f. A share of terminal profit reinvested "
                       "lies in [0,1]; this is a unit or sign error rather than a policy"
                       % (rk, rv))
            continue
        if rv == 0.0:
            continue                       # nothing is reinvested, so no spread is earned

        ck, cv = _find(doc, RETURN_KEYS)
        wk, wv = _find(doc, COST_KEYS)
        if ck is None or wk is None:
            unreadable[tk] = ("reinvests %.4f of terminal profit and commits %s, so the "
                              "spread it reinvests at cannot be read"
                              % (rv, "no terminal return" if ck is None
                                 else "no terminal cost of capital"))
            continue
        if cv < wv and not (doc.get(DECLARE_KEY) or "").strip():
            bad[tk] = ("terminal return %s %.4f sits BELOW terminal cost of capital %s "
                       "%.4f (%.0fbp) while %s reinvests %.1f%% of terminal profit — value "
                       "destroyed in perpetuity to buy growth, and no %s declares it"
                       % (ck, cv, wk, wv, (cv - wv) * 10000, rk, rv * 100, DECLARE_KEY))
    return bad, unreadable, read


def main(argv):
    prune = "--prune" in argv
    all_studies = studies()
    if not all_studies:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    bad, unreadable, read = measure()
    if read == 0:
        print("FAIL — %d study directories on disk and ZERO terminals that reinvest were "
              "read. A reader that stopped matching reads exactly like a book with none "
              "[R-ENF-04]." % len(all_studies))
        return 1

    known_bad, known_unread = load()

    if prune:
        still_bad = sorted(bad)
        still_un = sorted(unreadable)
        json.dump({"rule": "R-TERM-01 — the spread a terminal reinvests at",
                   "note": "Two groups, NOT interchangeable: one excuses an undeclared "
                           "negative spread, the other a terminal that cannot be read. "
                           "Both may only SHORTEN.",
                   "outstanding": still_bad, "unreadable": still_un},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1)
        print("pruned: undeclared %d -> %d, unreadable %d -> %d"
              % (len(known_bad), len(still_bad), len(known_unread), len(still_un)))
        return 0

    print("[R-TERM-01] the spread a terminal reinvests at")
    print("  study directories examined : %d" % len(all_studies))
    print("  terminals that reinvest    : %d" % read)
    print("  spread earned or declared  : %d" % (read - len(bad) - len(unreadable)))

    new = sorted(set(bad) - known_bad)
    new_un = sorted(set(unreadable) - known_unread)
    moved = sorted((set(bad) & known_unread) | (set(unreadable) & known_bad))

    for tk in sorted(bad):
        print("  %-6s %-12s %s" % ("NEW" if tk in new else "known", tk, bad[tk]))
    for tk in sorted(unreadable):
        print("  %-6s %-12s %s" % ("NEW" if tk in new_un else "known", tk, unreadable[tk]))

    rc = 0
    if new:
        print("\nFAIL — %d terminal(s) reinvest below their own cost of capital with "
              "nothing declaring it: %s" % (len(new), ", ".join(new)))
        print("   Declare %s with the mechanism, or correct the terminal. Never move the "
              "return to close the spread." % DECLARE_KEY)
        rc = 1
    if new_un:
        print("\nFAIL — %d terminal(s) newly UNREADABLE: %s" % (len(new_un),
                                                                ", ".join(new_un)))
        print("   An absent answer is not a clean one [R-ENF-04].")
        rc = 1
    if moved:
        print("\nFAIL — %d study/studies MOVED between the groups: %s"
              % (len(moved), ", ".join(moved)))
        rc = 1
    if rc:
        return rc

    print("\nOK — every terminal that reinvests either earns more than its capital costs "
          "or says why it does not.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
