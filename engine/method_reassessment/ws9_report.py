"""WS9 — what the new construction standard costs the rest of the book.

The reassessment adopted four construction rules and re-issued five studies under
them. This asks the obvious next question mechanically: OF EVERY OTHER NAME, WHICH
WOULD FAIL, AND ON WHAT? It is a REPORT and a queue, never a rebuild — the campaign
wrapper's order and hard stop stand.

IT IS BUILT FROM THE RATCHETS RATHER THAN BY RE-RUNNING THE GATES, on purpose. Each
gate already records exactly which studies it is letting through and why; reading
those lists is reading the gates' own verdicts, while re-implementing the checks
here would grade something other than what ships [R-ENF-03].

THE FIRST THING IT SAYS IS ABOUT ITS OWN POPULATION, and that is the finding. The
gates glob engine/*_study/. Most published fair values have no study directory at
all, so for those names there is nothing for any gate to open — they are not
passing, they are UNEXAMINED, and a queue that listed only the failures would
describe the smaller problem.
"""
from __future__ import annotations

import glob
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
AUDIT = os.path.join(ENGINE, "build_depth_audit")

# gate label -> (ratchet file, key holding the outstanding tickers)
GATES = [
    ("macro path      [R-MACRO-01]", "macro_outstanding.json", "outstanding"),
    ("cost of capital [R-COC-01]", "coc_outstanding.json", "outstanding"),
    ("lens design     [R-LENS-03]", "lens_outstanding.json", "outstanding"),
    ("bridge          [R-BRIDGE-01]", "bridge_outstanding.json", "outstanding"),
    ("output records  [R-ENF-05]", "output_outstanding.json", "outstanding"),
    ("gap review      [R-GAP-01]", "gap_outstanding.json", "breach_no_review"),
    ("answer readable [R-GAP-01]", "gap_outstanding.json", "unreadable"),
    ("walk-forward    [R-FCAL-01]", "actuation_outstanding.json", "outstanding"),
    # Adopted 03-09-2026. The first is a ratchet over RUNS rather than studies, so
    # its count is read against the walk-forward directories, not the study ones;
    # it is listed here anyway because a ratchet nobody prints is a ratchet nobody
    # shortens.
    ("valuation inputs [R-FCAL-01]", "valuation_inputs_outstanding.json", "runs"),
    ("deliverables    [R-FCAL-01]", "deliverables_outstanding.json", "outstanding"),
    ("lens in the document [R-LENS-03]", "lens_vocabulary_outstanding.json",
     "outstanding"),
]


def _list(fn, key):
    p = os.path.join(AUDIT, fn)
    if not os.path.exists(p):
        return None
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
    v = d.get(key)
    if isinstance(v, list):
        return [str(x).upper() for x in v]
    # A RATCHET MAY BE A MAPPING OF TICKER TO REASON RATHER THAN A BARE LIST, and
    # three adopted on 03-09-2026 are. Returning None for those reported them as
    # UNREADABLE, which the status reader escalates to a refusal — the right
    # behaviour for a ratchet nobody can read, and the wrong answer for one that
    # simply carries its reasons beside its names. The names are the keys.
    if isinstance(v, dict):
        return [str(k).upper() for k in v]
    return None


def report():
    studies = sorted(os.path.basename(d).replace("_study", "").upper()
                     for d in glob.glob(os.path.join(ENGINE, "*_study")))
    arch_path = os.path.join(ENGINE, "fv_vintages.json")
    published = {}
    if os.path.exists(arch_path):
        for name, entries in json.load(open(arch_path, encoding="utf-8")
                                       ).get("series", {}).items():
            e = entries[-1]
            fv = (e.get("fair") or {}).get("base")
            sp = e.get("spot")
            published[name] = (math.log(fv / sp) if sp and fv and fv > 0 else None)

    print("WS9 — the new standard against the rest of the book\n")
    print("  published fair values      %d" % len(published))
    print("  with a study directory     %d   (the only names any gate can open)"
          % len(set(published) & set(studies)))
    print("  UNEXAMINED, no directory   %d   — not passing; nothing to open"
          % len(set(published) - set(studies)))
    print("  study directories in all   %d" % len(studies))

    rows, missing_gates = {}, []
    for label, fn, key in GATES:
        lst = _list(fn, key)
        if lst is None:
            missing_gates.append(label)
            continue
        for tk in lst:
            rows.setdefault(tk, []).append(label)
    if missing_gates:
        # A gate whose ratchet cannot be read is not a gate everyone passes.
        print("\n  RATCHET UNREADABLE for %d gate(s) — reported, never assumed clean: %s"
              % (len(missing_gates), "; ".join(missing_gates)))

    print("\n  studies outstanding on at least one gate, worst first")
    print("  %-12s %-6s %8s   %s" % ("ticker", "gates", "vs price", "outstanding on"))
    for tk in sorted(rows, key=lambda t: (-len(rows[t]), t)):
        lg = published.get(tk)
        gap = ("%+7.1f%%" % ((math.exp(lg) - 1) * 100)) if lg is not None else "      —"
        print("  %-12s %-6d %8s   %s"
              % (tk, len(rows[tk]), gap,
                 ", ".join(g.split()[0] for g in rows[tk])))

    clean = sorted(set(studies) - set(rows))
    print("\n  studies outstanding on NOTHING (%d): %s"
          % (len(clean), ", ".join(clean) or "none"))
    print("\n  THE QUEUE THIS IMPLIES IS NOT THE ORDER THE CAMPAIGN RUNS IN, and")
    print("  nothing here changes that order. The campaign wrapper's market order")
    print("  and its hard stop after EGX stand; this is a REPORT of what the new")
    print("  standard costs, and the names with no study directory are the larger")
    print("  half of it — they clear only by being built, not by being re-gated.")
    return {"rows": rows, "clean": clean, "published": published,
            "studies": studies}


if __name__ == "__main__":
    report()
