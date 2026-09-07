"""A correction adopted on a sign is held to that sign at EVERY cut.  [R-ENF-01]

[R-FCAL-01] permits a correction only where the bias HOLDS ITS SIGN ACROSS ERAS,
and says in terms that a bias changing sign between eras is not a bias — report
the instability, never correct for it. EVERY STABILITY CLAIM IN THIS BOOK HAS BEEN
MADE AT ONE BOUNDARY, chosen for the market rather than for the driver: the year
its currency moved. That boundary is not every driver's break, and assuming it was
already cost a conclusion — TMGH's depreciation reads as a textbook correctable
bias at the market's cut and FLIPS SIGN at its own, one year later.

Measured across the book: 42 of 66 testable driver biases flip sign at some cut.
So a run adopting a correction on a sign-stable reading owes the sign at every cut
the data admits, and this gate holds it to that.

THE GATE READS THE RUN'S OWN RECORD AND RE-RUNS THE HOUSE INSTRUMENT [R-ENF-03]:
it imports boundary_sensitivity rather than reimplementing the arithmetic, because
a checker that models a measurement is checking a different measurement.

WHAT IT DOES NOT DO. It does not decide whether a correction is warranted — that
is [R-FCAL-01]'s whole procedure, of which sign stability is one clause. It does
not pick a boundary, which would be the selection this method forbids in either
direction. And it says nothing about a driver too thin to cut, which is reported
as untestable rather than counted as stable.

WHAT IT FOUND ON ITS FIRST RUN, AND THE DIRECTION IS UNUSUAL: perfect agreement
with the two runs' own procedures. ARCC's mfg_dep, its single ADOPTED candidate
("the one candidate that survives both clauses"), survives all four cuts; PHDC's
is.finance_cost, the only correction its record says passed its own test, survives
all five; and the three PHDC candidates the mechanical rule applied and the run
DECLINED flip at four, two and one cut respectively. An instrument neither run
used, confirming exactly what each concluded.

A NOTE ON SCOPE, BECAUSE IT IS EASY TO OVERSTATE THIS: PHDC's scored record does
not import its corrections module at all — the corrections are the adjusted-vs-raw
test [R-FCAL-01] requires, not levers in the published path. No delivered number
turns on any of this.

Read live: python3 scripts/check_correction_boundary.py
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENG = os.path.join(ROOT, "engine")

_spec = importlib.util.spec_from_file_location(
    "bs", os.path.join(ENG, "valuation_calibration", "boundary_sensitivity.py"))
BS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BS)


def _load(d):
    p = os.path.join(ENG, d, "corrections_log.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


# ONE NAMED ADAPTER PER RUN, because the five records have five shapes and a
# reader that guesses is a reader that silently finds nothing. Each returns
# [(driver, why_it_is_in_scope)]; a run whose record cannot be read is REPORTED.
def _arcc(rec):
    return [(c["driver"], "disposition ADOPTED")
            for c in rec.get("candidates", [])
            if str(c.get("disposition", "")).upper() == "ADOPTED"]


def _egch(rec):
    return [(d if isinstance(d, str) else d.get("driver"), "listed adopted")
            for d in rec.get("adopted", [])]


def _tmgh(rec):
    return [(d if isinstance(d, str) else d.get("driver"), "listed adopted")
            for d in rec.get("adopted", [])]


def _amoc(rec):
    # Pre-registered as estimating no correction at all; everything is a watch
    # flag. An EMPTY scope is a legitimate state and is reported as one.
    return []


def _phdc(rec):
    """Drivers the expanding-window rule actually applied a non-zero shift to.

    Wider than "adopted" on purpose: the rule's own stated reason for each is
    "sign stable across eras", which is precisely the claim this gate tests, so a
    correction the rule APPLIED is in scope even where the run then declined to
    promote it.
    """
    seen = {}
    for entry in rec.get("log", []):
        for drv, v in (entry.get("corrections") or {}).items():
            if v.get("applied"):
                seen.setdefault(drv, v.get("reason") or "applied")
    return sorted(seen.items())


RUNS = [
    ("AMOC", "amoc_walkforward", _amoc),
    ("ARCC", "arcc_walkforward", _arcc),
    ("EGCH", "egch_walkforward", _egch),
    ("TMGH", "tmgh_walkforward", _tmgh),
    ("PHDC", "phdc_walkforward", _phdc),
]

# KNOWINGLY OUTSTANDING [R-ENF-02], with the measurement rather than a shrug. The
# list may only ever SHORTEN, and a listed entry that stops flipping goes RED so
# the removal is forced rather than tidy.
OUTSTANDING = {
    ("PHDC", "asp"): (
        "Applied by the expanding-window rule with the reason 'sign stable across "
        "eras', and it flips at FOUR of five cuts. The run itself declined to "
        "promote it — its training record says only one correction passed its own "
        "test — and its scored path does not import the corrections module, so no "
        "published number rests on it. Listed rather than deleted because the "
        "adjusted-vs-raw test is a required artefact and rebuilding it under a "
        "cut-invariant rule moves that run's record, which is its own measured pass."),
    ("PHDC", "units_delivered"): (
        "Same rule, same stated reason, flips at TWO of five cuts. Declined by the "
        "run; nothing published rests on it."),
    ("PHDC", "units_sold"): (
        "Same rule, same stated reason, flips at ONE of five cuts. Declined by the "
        "run for a separate reason its record states — FY2024-25 units are not "
        "disclosed, so the correction cannot be scored at all."),
}


def main():
    print("does every correction adopted on a sign hold it at every cut?\n")
    runs_read = subjects = 0
    failures, held, thin = [], [], []
    for name, d, adapter in RUNS:
        rec = _load(d)
        if rec is None:
            print("  %-6s no corrections record — REPORTED, never skipped "
                  "[R-ENF-04]" % name)
            failures.append("%s: no corrections record" % name)
            continue
        cells = BS.load(name)
        if cells is None:
            print("  %-6s no per-cell file to test a boundary against" % name)
            failures.append("%s: no per-cell file" % name)
            continue
        runs_read += 1
        scope = adapter(rec)
        if not scope:
            print("  %-6s no correction in scope — a legitimate state" % name)
            continue
        for drv, why in scope:
            subjects += 1
            got = cells.get(drv)
            if not got:
                failures.append("%s %s: in scope but absent from the per-cell file, "
                                "so its sign cannot be tested" % (name, drv))
                print("  %-6s %-20s UNTESTABLE — absent from the cells" % (name, drv))
                continue
            cuts, flipped = BS.cuts_for(got)
            if not cuts:
                thin.append((name, drv))
                print("  %-6s %-20s too thin to cut (%d cells) — reported, never "
                      "counted stable" % (name, drv, len(got)))
                continue
            if flipped:
                if (name, drv) in OUTSTANDING:
                    held.append((name, drv, len(flipped), len(cuts)))
                    print("  %-6s %-20s FLIPS at %d of %d cuts   OUTSTANDING"
                          % (name, drv, len(flipped), len(cuts)))
                else:
                    failures.append("%s %s: adopted on a sign that flips at %d of %d "
                                    "cuts (%s)" % (name, drv, len(flipped), len(cuts), why))
                    print("  %-6s %-20s FLIPS at %d of %d cuts   %s"
                          % (name, drv, len(flipped), len(cuts), why))
            else:
                print("  %-6s %-20s survives all %d cuts   %s"
                      % (name, drv, len(cuts), why))

    stale = sorted(k for k in OUTSTANDING
                   if k not in {(n, d) for n, d, _, _ in held})
    print("\n  %d run(s) read, %d correction(s) in scope" % (runs_read, subjects))
    if not runs_read:
        print("\nREFUSED — a run that examined nothing is not a run that found "
              "nothing [R-ENF-04].")
        return 1
    if stale:
        print("\nFAIL — listed as outstanding and no longer flipping: %s. A ratchet "
              "may only SHORTEN, so remove the entry in the commit that fixes it "
              "[R-ENF-02]." % ", ".join("%s %s" % k for k in stale))
        return 1
    if failures:
        for f in failures:
            print("    %s" % f)
        print("\nFAIL — a correction is adopted on a sign, and a sign that depends "
              "on where the line was drawn is not a sign.")
        return 1
    for name, drv, nf, nc in held:
        print("\n  OUTSTANDING %s %s — %s" % (name, drv, OUTSTANDING[(name, drv)]))
    print("\nOK — every correction in scope holds its sign at every cut its data "
          "admits, except those listed above with their measurement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
