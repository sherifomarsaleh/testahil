"""Does a driver's bias survive where somebody drew the line?

[R-FCAL-01] permits a correction only where the bias HOLDS ITS SIGN ACROSS ERAS,
and says in terms that a bias which changes sign between eras is not a bias --
report the instability, never correct for it. Every stability claim in this book
has been made at ONE boundary, chosen for the MARKET: the year its currency moved.

THAT BOUNDARY IS NOT EVERY DRIVER'S BREAK, AND ASSUMING IT IS COST A CONCLUSION.
TMGH's depreciation reads -0.397 before 2023 and -0.342 after, which is exactly
the shape a correctable bias has, and it was written up as the one correctable
driver in that run. Its own break is a YEAR LATER -- realised depreciation over
property, plant and equipment rose from 0.0378 to 0.0761 and then COLLAPSED to
0.0141 as the asset base jumped elevenfold in 2024. Cut at 2025 the same driver
reads -0.516 and +0.364: A SIGN FLIP, and the conclusion was withdrawn.

SO THE STABILITY TEST IS RUN AT EVERY CUT POINT THE DATA ADMITS, not at one. A
driver whose sign survives every cut is stable in a way that means something; one
whose sign depends on the cut is telling you where the line was drawn.

WHAT THIS DOES NOT DO. It does not choose a boundary, and it must not: picking
the cut that makes a bias look stable is the selection this method forbids, and
picking the one that makes it look unstable is the same offence facing the other
way. It reports EVERY cut and lets the pattern speak. Nor does it claim a
sign-stable driver is correctable -- that needs [R-FCAL-01]'s whole procedure,
of which this is one clause.

Read live: python3 engine/valuation_calibration/boundary_sensitivity.py
"""
import os, sys, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
MIN_SIDE = 5          # a side with fewer cells than this is not an era

RUNS = {
    "ARCC": ("arcc_walkforward", "driver", "log_error", "setting", "asknown", "year"),
    "AMOC": ("amoc_walkforward", "driver", "log_error", "setting", "asknown", "year"),
    "EGCH": ("egch_walkforward", "driver", "log_error", "setting", "asknown", "year"),
    "TMGH": ("tmgh_walkforward", "driver", "log_error", "setting", "asknown", "year"),
    "PHDC": ("phdc_walkforward", "field", "e", "setting", "as_known", "target"),
}


def _yr(v):
    d = "".join(c for c in str(v) if c.isdigit())
    return int(d[-4:]) if len(d) >= 4 else None


def load(name):
    d, dk, ek, sk, sv, yk = RUNS[name]
    path = os.path.join(ENG, d, "error_cells.json")
    if not os.path.exists(path):
        return None
    raw = json.load(open(path))
    rows = (sum(([r for r in v] for k, v in raw.items() if k == sv), [])
            if isinstance(raw, dict) else [r for r in raw if r.get(sk) == sv])
    out = collections.defaultdict(list)
    for r in rows:
        e, y = r.get(ek), _yr(r.get(yk))
        if e is None or y is None:
            continue
        out[str(r.get(dk))].append((y, float(e)))
    return out or None


def cuts_for(cells):
    """Every admissible cut for one driver, and the ones where the sign flips.

    Exposed so a GATE can hold an adopted correction to this exact arithmetic
    instead of reimplementing it — a checker that models the measurement is
    checking a different measurement [R-ENF-03].

    Returns (cuts, flipped) where each is a list of (boundary, mean_before,
    mean_after); `cuts` is empty where no boundary leaves MIN_SIDE cells on both
    sides, which is a driver too thin to test rather than a stable one.
    """
    mean = lambda v: sum(v) / len(v) if v else None
    years = sorted({y for y, _ in cells})
    cuts = []
    for b in years[1:]:
        pre = [e for y, e in cells if y < b]
        post = [e for y, e in cells if y >= b]
        if len(pre) < MIN_SIDE or len(post) < MIN_SIDE:
            continue
        cuts.append((b, mean(pre), mean(post)))
    flipped = [(b, a, c) for b, a, c in cuts if (a > 0) != (c > 0)]
    return cuts, flipped


def main():
    flips, stable, thin, missing = [], [], [], []
    for name in sorted(RUNS):
        got = load(name)
        if got is None:
            missing.append(name)
            continue
        for drv, cells in sorted(got.items()):
            cuts, flipped = cuts_for(cells)
            if not cuts:
                thin.append((name, drv, len(cells)))
                continue
            (flips if flipped else stable).append((name, drv, cuts, flipped))

    if not (flips or stable):
        raise SystemExit("FAIL: no driver had two eras of at least %d cells" % MIN_SIDE)

    print("Boundary sensitivity — does the sign survive where the line is drawn?")
    print("Cuts requiring at least %d cells each side.\n" % MIN_SIDE)
    print("SIGN FLIPS AT SOME CUT (%d driver(s)) — not a bias, an instability:" % len(flips))
    for name, drv, cuts, flipped in flips:
        print("  %-6s %-24s" % (name, drv))
        for b, a, c in cuts:
            mark = "  <-- FLIPS" if (a > 0) != (c > 0) else ""
            print("        cut %d   before %+.3f   after %+.3f%s" % (b, a, c, mark))
    print("\nSIGN SURVIVES EVERY CUT (%d driver(s)):" % len(stable))
    for name, drv, cuts, _ in stable:
        lo = min(min(a, c) for _, a, c in cuts)
        hi = max(max(a, c) for _, a, c in cuts)
        print("  %-6s %-24s %d cut(s), range %+.3f to %+.3f"
              % (name, drv, len(cuts), lo, hi))
    if thin:
        print("\nTOO FEW CELLS TO CUT (%d) — reported, not counted as stable:" % len(thin))
        for name, drv, n in thin[:12]:
            print("  %-6s %-24s %d cell(s)" % (name, drv, n))
    for name in missing:
        print("\n%-6s NOT READ — no per-cell file" % name)
    print("\nA sign that survives every cut means something. One that does not is")
    print("telling you where the line was drawn, and a correction adopted on it is")
    print("fitted to that line.")
    json.dump({"flips": [[n, d] for n, d, _, _ in flips],
               "stable": [[n, d] for n, d, _, _ in stable],
               "uncuttable": [[n, d, c] for n, d, c in thin],
               "min_side": MIN_SIDE},
              open(os.path.join(HERE, "boundary_sensitivity.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
