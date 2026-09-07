#!/usr/bin/env python3
"""[R-LENS-03] — THE RELATIONSHIP BETWEEN A STUDY'S OWN PUBLISHED FIGURES.

WHY THIS EXISTS. Every instrument in this repository asks how a figure was BUILT — its
provenance, its arithmetic, whether it reproduces from the model. None asks whether the
figures a study publishes are consistent WITH EACH OTHER, which is the question a reader
asks first and the only one they can ask without the model. That is the table-footing
lesson one level up: a defect can live entirely in the relationship between two figures,
each individually computed and individually correct, and nothing inspecting figures one at
a time can see it.

TWO CLAIMS, BOTH THRESHOLD-FREE, BOTH WITH A LIVE BREACH ON THE DAY THIS WAS WRITTEN.

(1) A CENTRAL BELOW THE STUDY'S OWN PUBLISHED FLOOR. [R-LENS-03] names book value a
    DISCLOSED FLOOR, published as such and never weighted. A study that publishes a book
    cross-check, calls it a floor in its own note, and then publishes a central beneath it
    has contradicted itself on the page — and the two commonest drags are an over-charged
    discount rate and a compressed margin path, which is the principal's own complaint.
    MEASURED: AIRARABIA publishes a central of 4.7459 against a book cross-check of 5.2046
    whose committed note reads "a disclosed FLOOR, published as such and never weighted" —
    8.8% below its own floor, through every gate in the repository.

    THERE IS NO TOLERANCE TO ARGUE ABOUT: below is below. What the rule does NOT do is
    require the central to exceed the floor — it requires the study to SAY SO when it does
    not, in a field, with a reason. A developer carrying land at historical cost in a
    currency that has halved can be worth less than book and that is a finding; a study
    that publishes it silently while calling the number a floor is a contradiction.

(2) A CROSS-CHECK VALUE THAT DOES NOT REPRODUCE FROM ITS OWN COMMITTED OPERANDS. The
    relative-multiple lens commits a circularity block — spot, shares, net debt, metric —
    so that assert_lens_design can show the adopted multiple is not the traded one. Those
    same four operands run the other way give the lens's own value:

        value = (multiple x metric_value - net_debt) / shares

    MEASURED ACROSS THE BOOK: eight of fourteen do not reproduce, and the failures are two
    different kinds. AIRARABIA at 0.887 and EGCH at 0.889 are REAL ADJUSTMENTS — a fee
    stream added, a haircut applied — which the identity cannot see and which are perfectly
    legitimate work. ADNOCLS, THE MODEL REPORT ITSELF, is at 330.7: its net debt and metric
    are in thousands while spot x shares is in millions, so the traded multiple its own
    circularity block computes is 0.991x, and assert_lens_design then compared the adopted
    11.1037x against a number that means nothing AND PASSED IT. An absent answer in a clean
    answer's clothes [R-ENF-04].

    SO THE CHECK IS NOT THE IDENTITY [R-COC-01]. A gate demanding reproduction would fire
    on AIRARABIA and EGCH, which are right, and widening it until they passed would let
    ADNOCLS through — the free parameter this house forbids, choosing between two correct
    answers and one broken one by how far apart they happen to sit. WHAT SEPARATES THEM IS
    NOT A DISTANCE, IT IS WHETHER THE DIFFERENCE IS DECLARED. A record that reproduces is
    clean; a record that does not must NAME the adjustment in a field. A note in prose is
    not a declaration a reader can use — that is the reciprocal-orientation lesson verbatim.

WHAT IT DELIBERATELY DOES NOT DO. It does not test the envelope's low leg against net cash
per share, which is the third claim in this family and is NOT YET TESTABLE: net cash per
share needs the circularity block's money unit, and (2) is what establishes that a study
has declared one. It is named here rather than dropped, because a claim silently left out
is indistinguishable from one nobody thought of.

RATCHET [R-ENF-02] with each entry carrying its MEASURED ratio [R-ENF-08], so a record
that drifts further from its own operands is a NEW breach rather than an excused one. The
list may only SHORTEN. POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: zero study directories
fails, and so does zero LENS RECORDS read across present directories.

USAGE
    python3 scripts/check_output_sanity.py            # gate
    python3 scripts/check_output_sanity.py --prune    # rewrite the ratchet SHORTER
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit", "output_sanity_outstanding.json")

# The study calling its own cross-check a floor. A cross-check of kind book_value is a
# floor by [R-LENS-03] whatever its note says; the note is read as well so a study that
# spells the claim differently is still held to it.
FLOOR_KINDS = ("book_value",)
FLOOR_WORD = re.compile(r"\bfloor\b", re.I)

# TOLERANCE IS DERIVED FROM THE OPERANDS' OWN PRECISION, NEVER CHOSEN. The first draft
# demanded agreement to double precision and flagged ARCC, which is RIGHT: its multiple is
# committed as 4.5, a half-unit of 0.05, and 0.05 of a multiple on EGP 3,650.6mn of metric
# over 374.9mn shares is 0.487 a share — three orders of magnitude more than the 0.0006 by
# which it misses. A record cannot reproduce more precisely than the coarsest number it
# was written with. So the allowance is propagated from the printed decimals of the four
# committed operands, which is arithmetic ABOUT THE RECORD rather than a free parameter —
# the table-footing precedent verbatim — and per [R-COC-01] this is re-pointing a check
# that fired on correct work, not widening it: ARCC and PHDC clear by wide margins and
# twelve records stay red, several of them by three orders of magnitude.
def _half_unit(x):
    """Half of the last printed decimal place of a committed figure."""
    s = repr(float(x))
    if "e" in s or "E" in s:
        return 0.0
    d = len(s.split(".")[1]) if "." in s else 0
    return 0.5 * 10 ** -d


def reproduction_tolerance(mult, metric, net_debt, shares):
    """value = (m.M - D)/S, so the allowance propagates through that expression."""
    dm, dM, dD, dS = (_half_unit(v) for v in (mult, metric, net_debt, shares))
    val = (mult * metric - net_debt) / shares
    return (abs(dm * metric) + abs(mult * dM) + dD) / abs(shares) \
        + abs(val) * dS / abs(shares)


def numbers_files(engine=ENGINE):
    out = {}
    for d in sorted(glob.glob(os.path.join(engine, "*_study"))):
        tk = os.path.basename(d)[:-6].upper()
        for n in ("study_numbers.json", "numbers.json"):
            p = os.path.join(d, n)
            if os.path.exists(p):
                out.setdefault(tk, p)
                break
        else:
            g = sorted(glob.glob(os.path.join(d, "*numbers*.json")))
            if g:
                out.setdefault(tk, g[0])
    return out


def lens_record(path):
    try:
        doc = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    return doc.get("lens_record") if isinstance(doc, dict) else None


def central_of(lr):
    c = lr.get("central")
    if isinstance(c, dict):
        c = c.get("value")
    if isinstance(c, (int, float)):
        return float(c)
    p = lr.get("primary") or {}
    v = p.get("value")
    return float(v) if isinstance(v, (int, float)) else None


def floors(lr):
    """[(value, note)] — every cross-check this study publishes as a floor."""
    out = []
    for c in (lr.get("cross_checks") or []):
        if not isinstance(c, dict):
            continue
        note = c.get("note") or ""
        if c.get("kind") in FLOOR_KINDS or FLOOR_WORD.search(note):
            v = c.get("value")
            if isinstance(v, (int, float)):
                out.append((float(v), note))
    return out


# RE-POINTED 07-09-2026 ON THE EXEMPLAR, TWICE, AND BOTH RE-POINTINGS ARE THE SAME LESSON.
# The identity above — value = (multiple x metric - net debt) / shares — is what a simple
# relative lens does, and this gate condemned ADNOCLS at 330.7x for two reasons that were
# both the INSTRUMENT rather than the study.
#
#   (i) UNITS. The operands are USD thousands and the published figure is AED per share, so
#       the comparison crossed a currency and a scale. That is the identical defect this
#       repository found in check_bridge_reaches_answer the same morning, where the
#       exemplar's bridge was reported as the largest disagreement in the book and the two
#       figures were the same number either side of a 3.6725 peg.
#
#  (ii) CONSTRUCTION. Even in one currency it does not reproduce, because THIS RELATIVE LENS
#       IS NOT ONE ROUTE. It is 70 per cent of an enterprise multiple carried through the
#       full bridge — net debt, the perpetual securities and the minority — and 30 per cent
#       of an earnings multiple on profit after the hybrid coupon. Both routes are ordinary,
#       both are published, and NEITHER is the single-operand identity.
#
# WHY A DECLARED CONSTRUCTION IS NOT A WAY OUT. Same argument as the capital-structure
# tranches: a declared ROUTE carries a weight and a value, so declaring one has to be paid
# for twice — the weights must sum to one, and the weighted routes must still reproduce the
# published figure. A study cannot buy slack by naming a route. THE ARITHMETIC IS THE
# CLOSURE, and what is still refused is a published figure that reproduces from nothing.

def _fx_of(c):
    """The conversion between the operands' currency and the published one, or 1.0.

    A study reporting in one currency and publishing in another is ordinary — a pegged
    market makes it near-universal — and a gate that cannot read the declaration reports
    the peg as an error.
    """
    u = c.get("units") or (c.get("construction") or {}).get("units") or {}
    if not isinstance(u, dict):
        return 1.0
    op, pub, fx = u.get("operand_currency"), u.get("currency"), u.get("fx")
    if isinstance(op, str) and isinstance(pub, str) and op != pub \
            and isinstance(fx, (int, float)) and fx > 0:
        return float(fx)
    return 1.0


def _from_routes(c):
    """(reproduced, tolerance, failures) for a declared multi-route construction."""
    con = c.get("construction") or {}
    routes = con.get("routes")
    if not isinstance(routes, list) or not routes:
        return None
    bad, tot_w, acc, tol = [], 0.0, 0.0, 0.0
    for i, r in enumerate(routes):
        if not isinstance(r, dict):
            bad.append("route %d is not a record" % (i + 1))
            continue
        nm, w, v = r.get("name"), r.get("weight"), r.get("value")
        if not str(nm or "").strip():
            bad.append("route %d names nothing" % (i + 1))
        if not isinstance(w, (int, float)) or not isinstance(v, (int, float)):
            bad.append("route %r carries no weight and value to be blended"
                       % (nm or i + 1))
            continue
        tot_w += float(w)
        acc += float(w) * float(v)
        tol += abs(float(w)) * _half_unit(float(v))
    if abs(tot_w - 1.0) > 1e-6:
        bad.append("the declared route weights sum to %.6f, not one — a blend over "
                   "weights that do not sum to one is not a blend of anything" % tot_w)
    return (acc, max(tol, 1e-9), bad)


def reproduction(lr):
    """(committed, reproduced, declared_adjustment, tolerance) for the relative lens."""
    for c in (lr.get("cross_checks") or []):
        if not isinstance(c, dict) or c.get("kind") != "relative_multiple":
            continue
        val = c.get("value")
        if not isinstance(val, (int, float)):
            return None

        routed = _from_routes(c)
        if routed is not None:
            rep, tol, bad = routed
            if bad:
                return (float(val), float("nan"), None, 0.0, bad)
            return (float(val), rep, c.get("value_adjustment"), tol, [])

        circ = c.get("circularity") or {}
        mult = c.get("multiple")
        if not isinstance(mult, (int, float)):
            return None
        try:
            m, mv = float(mult), float(circ["metric_value"])
            nd, sh = float(circ["net_debt"]), float(circ["shares"])
            fx = _fx_of(c)
            rep = (m * mv - nd) / sh * fx
            tol = reproduction_tolerance(m, mv, nd, sh) * fx
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            return None
        return (float(val), rep, c.get("value_adjustment"), tol, [])
    return None


def load_outstanding():
    if not os.path.exists(OUTSTANDING):
        return {}
    try:
        return json.load(open(OUTSTANDING, encoding="utf-8")).get("outstanding", {})
    except Exception:
        return {}


def measure():
    """{ticker: {claim: detail}} — every relationship that does not hold."""
    found = {}
    for tk, path in sorted(numbers_files().items()):
        lr = lens_record(path)
        if not isinstance(lr, dict):
            continue
        bad = {}

        cen = central_of(lr)
        if cen is not None:
            for v, note in floors(lr):
                if cen < v and not lr.get("below_floor_reason"):
                    bad["floor"] = {
                        "central": cen, "floor": v,
                        "ratio": (cen / v) if v else None,
                        "note": note[:120],
                        "why": ("the central %.4f sits BELOW a cross-check this study "
                                "itself publishes as a floor (%.4f), and no "
                                "below_floor_reason is declared" % (cen, v))}
                    break

        rp = reproduction(lr)
        if rp:
            val, rep, declared, tol, broken = rp
            if broken:
                # A DECLARED CONSTRUCTION THAT CANNOT BE READ IS NOT A CONSTRUCTION. It
                # fails on its own terms rather than falling back to the simple identity,
                # because falling back would let a study switch the check off by declaring
                # a route badly [R-ENF-04].
                bad["reproduce"] = {
                    "committed": val, "reproduced": None, "ratio": None,
                    "why": ("the relative lens declares a construction that cannot be "
                            "read: %s" % "; ".join(broken))}
            elif val and abs(rep - val) > tol and not declared:
                bad["reproduce"] = {
                    "committed": val, "reproduced": rep, "ratio": (rep / val),
                    "why": ("the relative lens publishes %.4f; its own committed operands "
                            "give %.4f (%.3fx, against %.4f allowed by their own printed "
                            "precision), and no value_adjustment names the difference"
                            % (val, rep, rep / val, tol))}
        if bad:
            found[tk] = bad
    return found


def main(argv):
    prune = "--prune" in argv
    files = numbers_files()
    if not files:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1
    records = {tk: p for tk, p in files.items() if isinstance(lens_record(p), dict)}
    if not records:
        print("FAIL — %d study directories on disk and ZERO lens records read. A reader "
              "that stopped finding them reads exactly like a book with none [R-ENF-04]."
              % len(files))
        return 1

    found = measure()
    outstanding = load_outstanding()

    if prune:
        keep = {}
        for tk, bad in found.items():
            old = outstanding.get(tk, {})
            keep[tk] = {"claims": {k: {"ratio": v.get("ratio"), "why": v["why"]}
                                   for k, v in bad.items()},
                        "reason": old.get("reason",
                                          "measured on adoption day; the fix is the "
                                          "study's own record, at its next re-issue")}
        dropped = sorted(set(outstanding) - set(keep))
        json.dump({"rule": "R-LENS-03 — the relationship between a study's own figures",
                   "note": "May only SHORTEN. An entry excuses the claims and the RATIOS "
                           "it records; a ratio that grows is a NEW breach [R-ENF-08].",
                   "outstanding": keep},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print("pruned: %d listed (was %d); %d came off%s"
              % (len(keep), len(outstanding), len(dropped),
                 (": " + ", ".join(dropped)) if dropped else ""))
        return 0

    print("[R-LENS-03] the relationship between a study's own published figures")
    print("  study directories examined : %d" % len(files))
    print("  lens records read          : %d" % len(records))
    print("  relationships that hold    : %d" % (len(records) - len(found)))

    new, worse = [], []
    for tk, bad in sorted(found.items()):
        entry = outstanding.get(tk)
        if entry is None:
            new.append((tk, bad))
            continue
        excused = (entry.get("claims") or {})
        for claim, det in bad.items():
            if claim not in excused:
                new.append((tk, {claim: det}))
                continue
            rec, now = excused[claim].get("ratio"), det.get("ratio")
            # A ratio DRIFTING FURTHER FROM 1.0 is a worse breach; nearer is progress.
            if isinstance(rec, (int, float)) and isinstance(now, (int, float)):
                if abs(now - 1.0) > abs(rec - 1.0) + 1e-9:
                    worse.append((tk, claim, rec, now))

    if new or worse:
        for tk, bad in new:
            for claim, det in bad.items():
                print("  NEW   %-12s %-10s %s" % (tk, claim, det["why"]))
        for tk, claim, rec, now in worse:
            print("  WORSE %-12s %-10s excused at %.4fx, now %.4fx — further from its own "
                  "operands than the ratchet records [R-ENF-08]" % (tk, claim, rec, now))
        print("\nFAIL — a study publishes figures that contradict each other. The fix is "
              "the study's own record: declare the reason, or correct the construction. "
              "Never move a figure to close a gap.")
        return 1

    print("\nOK — no study publishes a central beneath its own floor, and every relative "
          "lens either reproduces from its own operands or names what separates them.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
