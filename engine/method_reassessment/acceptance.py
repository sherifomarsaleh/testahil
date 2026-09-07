"""Part E's acceptance criteria, PRINTED rather than attested.

The criteria say in their own first line that the plan is complete "when all of the
following hold AND ARE PRINTED BY THE GATES, NOT ATTESTED". Nothing printed them.
Measured 07-09-2026, the document that says when this work is finished was the
least-checked prose in the project: criterion 1 names seven gates and one of them,
check_corrections_applied, HAD NEVER BEEN WRITTEN — for five days, including days
on which the list was read to decide what to do next.

THIS IS AN INSTRUMENT, NOT A GATE, AND THE DISTINCTION IS DELIBERATE. A check that
is red until the programme finishes is the permanently-red check [R-ENF-02] forbids;
what is useful is a page that says where the criteria actually stand, so the answer
comes from arithmetic rather than from anyone's memory of it. It exits 0 whatever it
finds, and it REFUSES to report on what it cannot measure rather than passing it.

READ IT LIVE — python3 engine/method_reassessment/acceptance.py.
"""
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
ROOT = os.path.dirname(ENG)

# The five re-issued names, read from the plan's own text rather than typed from
# memory: they are the studies WS1-WS7 rebuild and the ones every criterion means.
FIVE = ["AMOC", "ARCC", "EGCH", "PHDC", "TMGH"]

CRITERION_1_GATES = [
    "check_cost_of_capital", "check_macro_coherence", "check_lens_design",
    "check_bridge", "check_walkforward_actuation", "check_corrections_applied",
    "check_valuation_calibration",
]

PATH_KEY = re.compile(r'engine/([a-z0-9]+)_(?:study|walkforward)/', re.I)


def _ticker_of_key(k):
    """The ticker a ratchet KEY names — bare, prefixed, or a repository path.

    BOTH SHAPES OR NEITHER. A first probe matched the ticker anywhere in the file
    and counted prose in a `_why` field; a second matched only ticker-shaped keys
    and missed the ratchets keyed by document PATH. They disagreed by two lists in
    opposite directions, and only reading both shapes gives the number.
    """
    s = str(k)
    m = PATH_KEY.search(s)
    if m and m.group(1).upper() in FIVE:
        return m.group(1).upper()
    head = s.upper().split(":")[0].split("/")[0].strip()
    if head in FIVE:
        return head
    if head.endswith("_STUDY") and head[:-6] in FIVE:
        return head[:-6]
    return None


def _entries(o):
    out = set()
    if isinstance(o, dict):
        for k, v in o.items():
            t = _ticker_of_key(k)
            if t:
                out.add(t)
            if isinstance(v, (dict, list)):
                out |= _entries(v)
    elif isinstance(o, list):
        for v in o:
            if isinstance(v, str):
                t = _ticker_of_key(v)
                if t:
                    out.add(t)
            elif isinstance(v, dict):
                for kk in ("ticker", "study", "name", "id", "path", "file"):
                    if kk in v:
                        t = _ticker_of_key(v[kk])
                        if t:
                            out.add(t)
                out |= _entries(v)
    return out


def criterion_1():
    print("CRITERION 1 — the seven gates green with negative controls, and the "
          "ratchet\n              lists carrying only names NOT yet re-issued.\n")
    missing, red, green = [], [], []
    for g in CRITERION_1_GATES:
        p = os.path.join(ROOT, "scripts", "%s.py" % g)
        nc = os.path.join(ROOT, "scripts", "%s_negative_control.py" % g)
        if not os.path.exists(p):
            missing.append(g)
            print("  %-32s ABSENT" % g)
            continue
        r = subprocess.run([sys.executable, p], capture_output=True, text=True,
                           timeout=900)
        ok = r.returncode == 0
        (green if ok else red).append(g)
        print("  %-32s %-6s  negative control %s"
              % (g, "GREEN" if ok else "RED",
                 "present" if os.path.exists(nc) else "ABSENT"))
    print("\n  %d green, %d red, %d absent" % (len(green), len(red), len(missing)))

    lists = sorted(glob.glob(os.path.join(ENG, "build_depth_audit",
                                          "*outstanding*.json")))
    per = {t: [] for t in FIVE}
    for f in lists:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            print("  RATCHET UNREADABLE: %s — unreadable is not clean [R-ENF-04]"
                  % os.path.basename(f))
            continue
        for t in _entries(d):
            per[t].append(os.path.basename(f).replace("_outstanding.json", ""))
    print("\n  ratchet debt on the five re-issued names, over %d lists:" % len(lists))
    for t in FIVE:
        n = len(per[t])
        print("    %-6s %2d list(s)%s" % (t, n, "  " + ", ".join(sorted(per[t]))
                                          if n else "   — clear"))
    total = sum(len(v) for v in per.values())
    held = (not missing and not red and total == 0)
    print("\n  CRITERION 1: %s" % ("MET" if held else "NOT MET"))
    if missing:
        print("    - %d of the seven gates do not exist: %s"
              % (len(missing), ", ".join(missing)))
    if red:
        print("    - red: %s" % ", ".join(red))
    if total:
        print("    - the criterion requires the ratchets to carry ONLY names not "
              "yet re-issued;\n      the five carry %d entries between them" % total)
    return held


def main():
    print("Part E acceptance criteria — printed, not attested\n")
    print("=" * 74)
    criterion_1()
    print("=" * 74)
    print("\nCRITERIA 2, 3, 5 and 6 ARE NOT MEASURED HERE AND ARE NOT REPORTED AS "
          "MET.\n"
          "  2  forward drivers inside each name's own walk-forward p10-p90, or a\n"
          "     priced exception — needs a per-name driver comparison this file does\n"
          "     not build; its second half (claimed corrections reconcile) IS gated.\n"
          "  3  the valuation calibration's pooled bias CI covering zero — its own\n"
          "     scorer returns a DATE until the first vintages mature, by design.\n"
          "  5  the two-sided gap gate firing on nothing among the five, or every\n"
          "     firing carrying a complete review — check_valuation_gap holds this.\n"
          "  6  the publish queue holding four files per name, each OPENED AND READ\n"
          "     — the reading is a human act and no script may attest it.\n"
          "\nAn unmeasured criterion is UNMEASURED, never met [R-ENF-04].")
    return 0


if __name__ == "__main__":
    sys.exit(main())
