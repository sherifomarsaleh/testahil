#!/usr/bin/env python3
"""[R-ENF-01] for L-353: a driver wired to NOTHING must say so.

L-353, registered 06-09-2026 on three runs' own history: holding a price or a
cost still is the worst thing a forecast can do with it. Freezing was the worst
of four knowable rules on every name that could be measured -- mean absolute log
error 0.346 on PHDC, 0.236 on AMOC, 0.364 on TMGH -- and one of those models
freezes its main driver by construction, worth 0.52 log points of its bias on its
own. [R-MACRO-01]'s own lesson is that a lesson binding nothing is advice and
loses to the next deadline. This makes it arithmetic.

WHAT IS TESTED IS CONNECTIVITY, NOT MAGNITUDE, AND THE DISTINCTION IS THE WHOLE
DESIGN. The clock test (engine/valuation_calibration/clock_test.py) went through
an ELASTICITY draft that was abandoned: bumping inflation by a point and reading
the local slope cannot see a level held still, so it reported a frozen model as
healthy. That instrument was wrong for THAT question and is exactly right for
THIS one. Asking "does this line respond AT ALL to the inflation path the model
itself carries" is a question about wiring, and the answer is a bit rather than a
number:

    project the run at its own inflation, then again with every inflation RATE
    the run carries doubled AT ITS SOURCE. A line whose projected value is
    IDENTICAL is wired to none of them.

Zero is not a threshold, so no free parameter enters -- which the promotion rule
would forbid. The bump is deliberately large (x2) so that no line is called
frozen through floating-point noise; a line genuinely wired to the path moves by
tens of per cent under it.

A FROZEN LINE IS NOT AUTOMATICALLY A DEFECT AND THE GATE SAYS SO. A price fixed
by contract, a line denominated in a foreign currency and wired to the currency
path instead, a pure volume driver with no price component -- each is a real
construction. What is forbidden is freezing a line and going quiet about it, so
the run DECLARES its frozen lines with a reason from a CLOSED list, in
frozen_escalators.json in its own directory. The list is closed for
[R-COC-01 AMENDED]'s reason: an open one lets any run opt out by inventing a
reason, and "we could not forecast it" is not a construction.

RATCHETED [R-ENF-02]: engine/build_depth_audit/frozen_outstanding.json carries
the runs already frozen on adoption day, allowed to fail, and the list may only
ever SHORTEN. POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: zero run directories
FAILS, and directories present with zero lines actually PROBED also FAILS,
because a run that could not be driven is not a run that came back clean.

    python3 scripts/check_frozen_escalator.py
    python3 scripts/check_frozen_escalator.py --prune
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENG = os.path.join(ROOT, "engine")
RATCHET = os.path.join(ENG, "build_depth_audit", "frozen_outstanding.json")

REASONS = {
    "contractually_fixed",
    "foreign_currency_wired_to_the_currency_path",
    "volume_driver_with_no_price_component",
    "benchmark_line_not_a_forecast",
}

# (ticker, directory, the module attribute holding the cumulative inflation path,
#  the lines to probe)
RUNS = [
    ("AMOC", "amoc_walkforward", "cpi_path", ["net_sales", "cost_of_sales"]),
    ("EGCH", "egch_walkforward", "cpi_path", ["revenue", "cost_of_sales"]),
    ("ARCC", "arcc_walkforward", None, ["revenue", "cogs"]),
]


def probe(d, attr, lines, horizon=3):
    """Returns {line: is_frozen}. Raises where the run cannot be driven -- a run
    that cannot be probed is reported, never silently passed.

    THE BUMP IS APPLIED AT THE SOURCE, NOT TO ONE DERIVED PATH, AND THAT WAS
    LEARNED BY GETTING IT WRONG. The first draft doubled a named function
    (cpi_path) and flagged EGCH's revenue as frozen. EGCH's revenue is urea
    tonnes times a pound price, and that price moves through fx_level, which
    derives the currency from the CPI DIFFERENTIAL read straight off the run's
    own fiscal-year table -- so it never touches cpi_path and the gate was firing
    on work that is right. Per [R-COC-01]: when a check fires on work that is
    right, re-point it. Every inflation RATE the run carries is doubled at its
    source, so every path derived from any of them moves.
    """
    p = os.path.join(ENG, d)
    sys.path.insert(0, p)
    for m in ("bottom_up", "panel", "score", "macro"):
        sys.modules.pop(m, None)
    try:
        import bottom_up as B
        cells = [(o, h, t) for o, h, t in B.cells() if h == horizon]
        if not cells:
            raise RuntimeError("no cell at horizon %d" % horizon)
        base = {(o, h): B.project(o, h) for o, h, _ in cells}

        # Every inflation rate the run carries, found BY SHAPE in its own
        # fiscal-year table: a key naming cpi or inflation, holding a number.
        # Two table SHAPES are in use across this book and both are searched.
        # A run holding neither is reported, never assumed clean.
        touched, saved = 0, []

        def _bump(rec):
            n = 0
            for k, v in list(rec.items()):
                kl = k.lower()
                if ("cpi" in kl or "inflation" in kl) and isinstance(v, (int, float)):
                    saved.append((rec, k, v))
                    rec[k] = v * 2.0   # rates here are PERCENT; the RATE doubles
                    n += 1
            return n

        # shape one: {fiscal year: {field: value}}
        table = getattr(B, "FY", None)
        if isinstance(table, dict):
            for _fy, rec in table.items():
                if isinstance(rec, dict):
                    touched += _bump(rec)
        # shape two: {field: {"values": {year: value}}}. Here the FIELD name is on
        # the outer key and the inner keys are years, so every year's value moves.
        # THE FACTOR RISES WITH THE YEAR, deliberately: some of these series are a
        # cpi INDEX rather than a rate, and a model using an index reads RATIOS of
        # it -- scaling every year by the same constant would leave every ratio
        # unchanged and make a line wired only to the index look frozen. That is
        # the false negative this shape invites, and it is closed by construction
        # rather than by hoping no run uses an index.
        macro = getattr(B, "MACRO", None)
        if isinstance(macro, dict):
            for k, rec in macro.items():
                kl = k.lower()
                if ("cpi" in kl or "inflation" in kl) and isinstance(rec, dict):
                    vals = rec.get("values")
                    if isinstance(vals, dict):
                        for i, y in enumerate(sorted(vals, key=str)):
                            v = vals[y]
                            if isinstance(v, (int, float)):
                                saved.append((vals, y, v))
                                vals[y] = v * (1.0 + 0.5 * (i + 1))
                                touched += 1
        if not touched:
            raise RuntimeError("no inflation rate found in this run's own tables")
        try:
            bumped = {(o, h): B.project(o, h) for o, h, _ in cells}
        finally:
            for rec, k, v in saved:
                rec[k] = v

        out = {}
        for ln in lines:
            moved, probed = False, 0
            for k in base:
                a, b = base[k].get(ln), bumped[k].get(ln)
                if a is None or b is None:
                    continue
                probed += 1
                if a != b:
                    moved = True
            if probed == 0:
                raise RuntimeError("line %r present in no cell" % ln)
            out[ln] = not moved
        return out
    finally:
        sys.path.remove(p)


def declared(d):
    f = os.path.join(ENG, d, "frozen_escalators.json")
    if not os.path.exists(f):
        return {}
    return json.load(open(f)).get("frozen", {})


def main(argv):
    prune = "--prune" in argv
    ratchet = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {"outstanding": []}
    allowed = set(ratchet.get("outstanding", []))

    on_disk = [t for t, d, _, _ in RUNS if os.path.isdir(os.path.join(ENG, d))]
    if not on_disk:
        print("FAIL: no walk-forward directory on disk — the resolver is broken,")
        print("      not the book. An empty population is never a clean result.")
        return 1

    probed_lines, failures, still = 0, [], []
    for ticker, d, attr, lines in RUNS:
        if not os.path.isdir(os.path.join(ENG, d)):
            continue
        try:
            res = probe(d, attr, lines)
        except Exception as e:
            failures.append("%s: could not be probed — %s" % (ticker, str(e)[:80]))
            continue
        probed_lines += len(res)
        dec = declared(d)
        frozen = [ln for ln, f in res.items() if f]
        undeclared = []
        for ln in frozen:
            why = dec.get(ln)
            if not why:
                undeclared.append("%s (no declaration)" % ln)
            elif why not in REASONS:
                undeclared.append("%s (reason %r not in the closed list)" % (ln, why))
        print("%-6s probed %d line(s); frozen: %s"
              % (ticker, len(res), ", ".join(frozen) if frozen else "none"))
        if undeclared:
            msg = "%s: frozen and undeclared — %s" % (ticker, "; ".join(undeclared))
            (still if ticker in allowed else failures).append(msg)

    if probed_lines == 0:
        print("\nFAIL: %d run directories present and ZERO lines probed." % len(on_disk))
        print("      A run that could not be driven is not a run that came back clean.")
        return 1

    for m in still:
        print("  (on the ratchet) %s" % m)
    if prune:
        cleared = sorted(allowed - {m.split(":")[0] for m in still})
        ratchet["outstanding"] = sorted({m.split(":")[0] for m in still})
        json.dump(ratchet, open(RATCHET, "w"), indent=1)
        print("\npruned: %s" % (", ".join(cleared) if cleared else "nothing to clear"))
        return 0

    if failures:
        print("\nRED — %d finding(s):" % len(failures))
        for m in failures:
            print("  %s" % m)
        return 1
    # A ratcheted run is NOT a declared one and the closing line must not say it
    # is. An allowance for known-outstanding work that reports itself as clean is
    # how a ratchet quietly becomes an exemption.
    if still:
        print("\nOK — %d line(s) probed across %d run(s); no NEW frozen line. "
              "%d run(s) still outstanding on the ratchet: %s."
              % (probed_lines, len(on_disk), len(still),
                 ", ".join(sorted({m.split(":")[0] for m in still}))))
    else:
        print("\nOK — %d line(s) probed across %d run(s); every frozen line is declared."
              % (probed_lines, len(on_disk)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
