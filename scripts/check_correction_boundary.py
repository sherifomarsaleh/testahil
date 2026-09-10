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
direction. A driver too thin to cut is REFUSED where a correction rests on
it, not merely noted: an adoption is a claim the sign is stable, and a driver with
no admissible cut carries no evidence of stability at all. Untestable is not
stable, which is [R-ENF-04]'s clause and the stronger objection rather than the
weaker one.

AN ACT AT AN ORIGIN IS JUDGED ON WHAT THAT ORIGIN COULD SEE. A correction applied
by an expanding-window rule is tested on the resolved history available at that
origin — the run's own definition, reconstructed from its committed cells and
verified against the counts the run itself recorded — while a claim about a DRIVER
(an adopted disposition) is tested on the whole record. The whole-record reading is
printed beside every act as information and never gates, because condemning a
method for not knowing the future is what point-in-time discipline forbids.

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
    # An ADOPTED disposition is a claim about the DRIVER rather than an act at one
    # origin, so it carries no origin and is judged on the whole record.
    return [(c["driver"], "disposition ADOPTED", None)
            for c in rec.get("candidates", [])
            if str(c.get("disposition", "")).upper() == "ADOPTED"]


def _egch(rec):
    return [(d if isinstance(d, str) else d.get("driver"), "listed adopted", None)
            for d in rec.get("adopted", [])]


def _tmgh(rec):
    return [(d if isinstance(d, str) else d.get("driver"), "listed adopted", None)
            for d in rec.get("adopted", [])]


def _amoc(rec):
    # Pre-registered as estimating no correction at all; everything is a watch
    # flag. An EMPTY scope is a legitimate state and is reported as one.
    return []


def _phdc(rec):
    """Drivers the expanding-window rule applied a non-zero shift to, WITH THE ORIGIN.

    Wider than "adopted" on purpose: the rule's own stated reason for each is a
    sign-stability claim, which is precisely what this gate tests, so a correction
    the rule APPLIED is in scope even where the run then declined to promote it.

    THE ORIGIN TRAVELS WITH THE DRIVER AND THAT IS THE WHOLE CORRECTION [07-09-2026].
    The first version returned the driver alone and the gate then judged it against
    the FULL panel — a question the method was never allowed to answer, because an
    expanding window at an early origin cannot see a flip the later record reveals.
    Measured when a rebuild was attempted: a correction applied at one origin on two
    admissible cuts, neither flipping, sits on a driver that flips at SIX OF SIX cuts
    of the whole record. Judging it on the whole record condemns the method for not
    knowing the future, which point-in-time discipline forbids.
    """
    seen = {}
    for entry in rec.get("log", []):
        o = entry.get("origin")
        for drv, v in (entry.get("corrections") or {}).items():
            if v.get("applied"):
                seen.setdefault((drv, o), v.get("reason") or "applied")
    return [(drv, why, o) for (drv, o), why in sorted(seen.items())]


def origin_window(name, driver, origin):
    """The resolved history a correction at `origin` was allowed to see.

    THE RUN'S OWN DEFINITION, RECONSTRUCTED FROM ITS COMMITTED CELLS: every scored
    cell whose ORIGIN and whose TARGET both fall strictly before the correcting
    origin — which is the expanding window the corrections module documents as
    "the whole information set a correction may use". Verified rather than assumed:
    all 50 (origin, driver) windows this reproduces match the counts the run itself
    recorded, so the gate is reading the same window the rule used.

    Returns [(year, error)] in boundary_sensitivity's shape, or None where the run
    has no per-cell file to reconstruct from.
    """
    d = dict((n, dd) for n, dd, _a in RUNS)[name]
    p = os.path.join(ENG, d, "error_cells.json")
    if not os.path.exists(p):
        return None
    raw = json.load(open(p, encoding="utf-8"))
    if isinstance(raw, dict):
        rows = raw.get("as_known", []) or raw.get("asknown", [])
        dk, ek, yk, ok_ = "field", "e", "target", "origin"
    else:
        rows = [r for r in raw if r.get("setting") == "asknown"]
        dk, ek, yk, ok_ = "driver", "log_error", "year", "origin"
    out = []
    for r in rows:
        if str(r.get(dk)) != driver or r.get(ek) is None:
            continue
        y, o = BS._yr(r.get(yk)), BS._yr(r.get(ok_))
        if y is None or o is None or y >= origin or o >= origin:
            continue
        out.append((y, float(r[ek])))
    return out


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
    # ("PHDC", "units_delivered") CAME OFF 07-09-2026, the same day it went on, and
    # the reason is the rework rather than a fix to the run. Judged on the whole
    # record it flips at two of five cuts; judged on what origin 2023 could actually
    # see — the only question point-in-time discipline allows of an act at an origin
    # — it survives all four. The act was sound on its own information and the
    # driver is unstable in hindsight, which are two different findings, and the
    # first draft of this gate could only express the second. The whole-record
    # reading is still printed beside it, because it is worth knowing and is not a
    # verdict on the method.
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
        for drv, why, origin in scope:
            subjects += 1
            full = cells.get(drv)
            if not full:
                failures.append("%s %s: in scope but absent from the per-cell file, "
                                "so its sign cannot be tested" % (name, drv))
                print("  %-6s %-20s UNTESTABLE — absent from the cells" % (name, drv))
                continue
            # AN ACT AT AN ORIGIN IS JUDGED ON WHAT THAT ORIGIN COULD SEE; a claim
            # about the driver is judged on the whole record. The other reading is
            # reported beside it and never gates.
            if origin is None:
                got, vantage = full, "whole record"
                aside = ""
            else:
                got = origin_window(name, drv, origin)
                vantage = "as at %s" % origin
                fc, ff = BS.cuts_for(full)
                aside = ("   [whole record: %d of %d cuts flip]" % (len(ff), len(fc))
                         if fc else "   [whole record: too thin to cut]")
            if got is None:
                failures.append("%s %s: no per-cell file to rebuild the %s window"
                                % (name, drv, vantage))
                continue
            label = "%s %s" % (drv, vantage) if origin is not None else drv
            cuts, flipped = BS.cuts_for(got)
            if not cuts:
                # UNTESTABLE IS NOT STABLE. A correction applied on a window too
                # short to cut has no sign-stability evidence behind it at all,
                # which is a stronger objection than a flip, not a weaker one.
                key = (name, drv)
                if key in OUTSTANDING:
                    held.append((name, drv, label, 0, 0))
                    print("  %-6s %-28s too thin to cut (%d cells)   OUTSTANDING%s"
                          % (name, label, len(got), aside))
                else:
                    failures.append("%s %s: applied on a window too short to cut "
                                    "(%d cells) — untestable is not stable [R-ENF-04]"
                                    % (name, label, len(got)))
                    print("  %-6s %-28s too thin to cut (%d cells)%s"
                          % (name, label, len(got), aside))
                thin.append((name, drv))
                continue
            if flipped:
                if (name, drv) in OUTSTANDING:
                    held.append((name, drv, label, len(flipped), len(cuts)))
                    print("  %-6s %-28s FLIPS at %d of %d cuts   OUTSTANDING%s"
                          % (name, label, len(flipped), len(cuts), aside))
                else:
                    failures.append("%s %s: adopted on a sign that flips at %d of %d "
                                    "cuts (%s)" % (name, label, len(flipped), len(cuts), why))
                    print("  %-6s %-28s FLIPS at %d of %d cuts   %s%s"
                          % (name, label, len(flipped), len(cuts), why, aside))
            else:
                print("  %-6s %-28s survives all %d cuts%s"
                      % (name, label, len(cuts), aside))

    stale = sorted(k for k in OUTSTANDING
                   if k not in {(n, d) for n, d, _l, _f, _c in held})
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
    for name, drv, label, nf, nc in held:
        print("\n  OUTSTANDING %s %s — %s" % (name, label, OUTSTANDING[(name, drv)]))
    print("\nOK — every correction in scope holds its sign at every cut its data "
          "admits, except those listed above with their measurement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
