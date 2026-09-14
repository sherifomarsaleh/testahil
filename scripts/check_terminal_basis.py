#!/usr/bin/env python3
"""[R-TERM-01] — the terminal is fed on the LAST EXPLICIT YEAR'S basis, checked in the code.

engine/terminal_value.py states its contract in its own docstring and states the failure
in terms: the inputs are in the LAST EXPLICIT YEAR'S money, "the module grows the free
cash flow one year itself", and "Pass a NOPAT already grown by (1+g) and the terminal is
overstated by exactly (1+g) — a year-seven flow discounted at the year-five factor". The
field was renamed so that the NAME IS THE WARNING, after six of eight callers read it the
other way on 4 September 2026.

MEASURED 7 SEPTEMBER 2026, with twenty callers rather than eight: TWO STILL DO IT. SCEM
passes nopat[-1] * (1 + g_term) and dna_book = dna_f[-1] * (1 + g_term) at BOTH of its
call sites; PHAR passes a nopat_term defined as nopat[-1] * (1 + g_term) less a
depreciation catch-up, and dna[-1] * (1 + g_term), also at both. Priced through the module
on each study's own committed record: SCEM's terminal -8.64%, enterprise value -5.75%,
fair value -4.54%; PHAR's terminal -9.9% and -9.2% across its two frames, and because that
company is geared its EQUITY moves -18.4% and -13.9%.

WHY NOTHING SAW IT. check_terminal_floor tests the 1/g signature, check_terminal_record_
shape tests the record's FIELD SET, and both are satisfied by a record whose figures were
computed from an input on the wrong basis — the arithmetic is internally perfect and the
UNIT is wrong, which is [R-TERM-01]'s own general lesson arriving inside its own module.
A recalculation gate reconciles a model to itself.

WHY THIS READS THE CODE AND NOT THE RECORD. A first draft compared each record's committed
nopat against the study's own last explicit NOPAT and needed to FIND that series; two
matchers written the same afternoon gave two different answers on the same book — one
matched EGCH's base case against the halt case's rows and read 1.0096, the other matched
by path and read 1.1164, and neither was authoritative. That is [L-355]: a reader that
guesses a naming convention silently finds nothing and reports it as a result. The CALL
SITE is unambiguous and needs no convention at all.

WHAT IT MATCHES, AND WHY THAT IS NARROW ENOUGH TO GATE. Only a multiplication by a
parenthesised (1 + X) applied to the nopat or dna_book argument of a TerminalInputs call —
following one level of single assignment, because PHAR names the expression before passing
it. That shape cannot occur innocently in a call to a module whose contract says the
module grows the flow itself. It is the shape-matching argument already made for rule
identifiers and repository paths.

THREE CONSTRUCTIONS ARE LEGITIMATE AND ALL THREE STAY SILENT, verified against the book
rather than reasoned about:
  * EGCH DIVIDES by (1 + g), converting a terminal-year figure back to last-explicit-year
    money. That is the correction already applied, and a gate firing on it would be
    condemning the fix.
  * EMPOWER's two-stage terminal passes nopat['FY30'] * grow10 where grow10 = (1+g1)**10,
    compounding ten years to reach stage two's own starting point, whose terminal is then
    discounted by (1+wacc)**10. A named factor, not a one-year growth, and not matched.
  * A REPLAY of a committed record — TerminalInputs(**dict(r['inputs'])) — is rebuilding
    what a study already published and has no expression to inspect.

A STUDY MAY DELIBERATELY REBUILD THE RETIRED CONSTRUCTION, AND THAT IS NOT THIS DEFECT.
PHAR prices what the pre-grown basis was worth by building it through the same module and
committing the result — which is the honest way to show a correction's value rather than
typing it into a document, and nothing downstream discounts it. A gate firing on that
would be condemning the evidence for the fix.

THE RELEASE IS A DECLARATION WITH A REASON, NOT A NAMING CONVENTION. The call carries a
`TERMINAL-BASIS-EXCEPTION:` comment within the ten lines above it, followed by a reason,
and an EMPTY reason has switched the check off rather than declared it. Matching on a
variable spelled `_grown` or `_retired` instead would be exactly [L-355] — a reader
guessing a convention — and would let any study opt out by renaming a local.

AN UNREADABLE CALL SITE IS REPORTED, NEVER PASSED [R-ENF-04]. A caller that builds its
arguments as a dict and splats them (engine/valuation_calibration/cashflow_lens.py does
exactly this, correctly, with the last explicit year's NOPAT) is a shape this gate cannot
follow to the argument. Silently skipping it would make "we cannot read this" and "this is
clean" the same output, which is the failure mode this repository keeps paying for. Such a
call is listed as UNREADABLE and the run FAILS if a NEW one appears, so a study cannot
escape by restructuring its call.

POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: zero source files examined FAILS, and zero
TerminalInputs CALL SITES found across present files FAILS — a matcher that stopped
matching reads exactly like a book with no terminals in it.

RATCHETED [R-ENF-02] and the list may only ever SHORTEN.
"""
from __future__ import annotations

import ast
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit", "terminal_basis_outstanding.json")

FIELDS = ("nopat", "dna_book")


def _one_plus(n):
    """A (1 + X) growth factor, however X is spelled."""
    return (isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add)
            and isinstance(n.left, ast.Constant) and n.left.value == 1)


def _grows(node):
    return any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult)
               and (_one_plus(n.right) or _one_plus(n.left))
               for n in ast.walk(node))


def _divides(node):
    return any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div)
               and _one_plus(n.right) for n in ast.walk(node))



MARKER = "TERMINAL-BASIS-EXCEPTION:"


def _declared(path, call_line):
    """The stated reason for a deliberate pre-grown call, or '' if there is none.

    Read from the source lines ABOVE the call rather than from the syntax tree, because
    a comment is not a node — and a comment is the right shape here: it sits at the exact
    line the exception applies to, where the next reader of that call will see it, rather
    than in a declarations file somebody has to think to open.
    """
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except Exception:
        return ""
    lo = max(0, call_line - 11)
    for raw in lines[lo:call_line]:
        if MARKER in raw:
            return raw.split(MARKER, 1)[1].strip().lstrip("#").strip()
    return ""


def sources():
    """Every python file under engine/ that could construct a terminal."""
    out = []
    for pat in ("*_study/*.py", "*_walkforward/*.py", "*/*.py", "*.py"):
        out.extend(glob.glob(os.path.join(ENGINE, pat)))
    return sorted({p for p in out if "__pycache__" not in p
                   and os.path.basename(p) != "terminal_value.py"})


def audit():
    """(bad, unreadable, calls, files) over the whole book."""
    bad, unreadable, declared, calls, files = [], [], [], 0, 0
    for path in sources():
        try:
            tree = ast.parse(open(path, encoding="utf-8").read())
        except Exception:
            continue                      # not a defect of THIS rule
        files += 1
        assigns = {n.targets[0].id: n.value for n in ast.walk(tree)
                   if isinstance(n, ast.Assign) and len(n.targets) == 1
                   and isinstance(n.targets[0], ast.Name)}
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            fn = n.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", None)
            if name != "TerminalInputs":
                continue
            calls += 1
            rel = os.path.relpath(path, ROOT)
            named = {kw.arg for kw in n.keywords}
            if None in named:
                # **kwargs: the arguments are assembled elsewhere and this gate cannot
                # follow them to an expression. Reported, never passed [R-ENF-04].
                if not (named & set(FIELDS)):
                    why = _declared(path, n.lineno)
                    if why:
                        declared.append((rel, n.lineno, "**", why))
                    else:
                        unreadable.append((rel, n.lineno,
                                           "arguments are splatted from a mapping, so no "
                                           "expression for %s can be inspected here"
                                           % " or ".join(FIELDS)))
                    continue
            for kw in n.keywords:
                if kw.arg not in FIELDS:
                    continue
                expr, shown = kw.value, ast.unparse(kw.value)
                if isinstance(expr, ast.Name) and expr.id in assigns:
                    expr = assigns[expr.id]
                    shown = "%s = %s" % (kw.value.id, ast.unparse(expr))
                if _grows(expr) and not _divides(expr):
                    why = _declared(path, n.lineno)
                    if why:
                        declared.append((rel, kw.value.lineno, kw.arg, why))
                        continue
                    bad.append((rel, kw.value.lineno, kw.arg, shown[:150]))
    return bad, unreadable, declared, calls, files


def load():
    if not os.path.exists(OUTSTANDING):
        return {}
    try:
        return json.load(open(OUTSTANDING, encoding="utf-8")).get("outstanding", {})
    except Exception:
        return {}


def key(rel, field):
    return "%s::%s" % (rel, field)


def main(argv):
    prune = "--prune" in argv
    bad, unreadable, declared, calls, files = audit()

    if not files:
        print("FAIL — examined zero source files [R-ENF-04].")
        return 1
    if not calls:
        print("FAIL — read %d source file(s) and found ZERO TerminalInputs call sites. A "
              "matcher that stopped matching reads exactly like a book with no terminals "
              "in it [R-ENF-04]." % files)
        return 1

    known = load()
    print("[R-TERM-01] the terminal's inputs are on the LAST EXPLICIT YEAR'S basis")
    print("  source files read     : %d" % files)
    print("  TerminalInputs calls  : %d" % calls)
    print("  pre-grown arguments   : %d" % len(bad))
    print("  call sites unreadable : %d" % len(unreadable))
    print("  declared exceptions   : %d" % len(declared))
    for rel, line, field, why in sorted(declared):
        print("   [declared] %-40s :%-5d %-9s %s" % (rel, line, field, why[:60]))

    listed, fresh = [], []
    for rel, line, field, shown in bad:
        k = key(rel, field)
        (listed if k in known else fresh).append((rel, line, field, shown))
    for rel, line, why in unreadable:
        k = key(rel, "**")
        (listed if k in known else fresh).append((rel, line, "**", why))

    if listed:
        print("\nstill outstanding, allowed for now (%d):" % len(listed))
        for rel, line, field, shown in sorted(listed):
            print("   %-44s :%-5d %-9s %s" % (rel, line, field, shown[:70]))
    if fresh:
        print("\nFAIL — a terminal input pre-grown by (1+g), or a call site this gate "
              "cannot read, and not on the ratchet:")
        for rel, line, field, shown in sorted(fresh):
            print("   %-44s :%-5d %-9s %s" % (rel, line, field, shown[:70]))
        print("\nThe module grows the flow one year itself and values the terminal at the "
              "END OF THE LAST EXPLICIT YEAR, which is where every caller discounts it. A "
              "figure handed in already grown is a year-seven flow discounted at the "
              "year-five factor, and nothing in the arithmetic afterwards looks wrong.")
        return 1

    if prune:
        keep = {}
        cur = {key(r, f) for r, _l, f, _s in bad} | {key(r, "**") for r, _l, _w in unreadable}
        for k, v in known.items():
            if k in cur:
                keep[k] = v
        doc = {"rule": "R-TERM-01",
               "note": ("Call sites knowingly outstanding. The list may only ever SHORTEN "
                        "[R-ENF-02]; --prune rewrites it and never grows it."),
               "outstanding": keep}
        json.dump(doc, open(OUTSTANDING, "w", encoding="utf-8"), indent=1)
        print("\npruned: %d listed (was %d)" % (len(keep), len(known)))

    print("\nOK — every terminal is fed on the basis its own module specifies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
