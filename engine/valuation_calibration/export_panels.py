"""Commit what each walk-forward already knows, so a later job can use it.

THE DEFECT THIS CLOSES. AMOC, ARCC and EGCH ran their statement walk-forwards
against real filings and scored them properly — and left nothing in the repository
a later job can rebuild from. Their as-reported figures live in a module-level dict
inside each run's own panel.py, and the filings behind it are gitignored. PHDC and
TMGH wrote a year-keyed JSON; these three did not, so the valuation calibration
cannot touch them however good the original run was.

That is a REPRODUCIBILITY gap, not a data one: the numbers exist, they just did not
survive the run. This module imports each run's own panel module and writes the
year-keyed panel it already holds — no re-parsing, no re-derivation, nothing new
asserted. What is committed is exactly what that run computed, which is the only
thing that makes it evidence rather than a second opinion.

It writes `panel_export.json` beside each run and never touches the run's own
files.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)

# The dict on each run's panel module that holds the as-reported income statement,
# and any companions worth carrying with it. Named per run rather than guessed,
# because a wrong guess would export something that is not the statement and
# nothing downstream would notice.
SOURCES = {
    "AMOC": ["IS", "OTHER_REVENUE", "COST_STACK", "PRODUCTS", "COMMON"],
    "ARCC": ["IS", "REV", "COST", "OTHER", "DEBT", "PHYS"],
    "EGCH": ["IS"],
}


def _load(run):
    d = os.path.join(ENGINE, "%s_walkforward" % run.lower())
    p = os.path.join(d, "panel.py")
    if not os.path.exists(p):
        return None, None
    cwd = os.getcwd()
    sys.path.insert(0, d)
    try:
        os.chdir(d)
        spec = importlib.util.spec_from_file_location("panel_%s" % run.lower(), p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m, d
    finally:
        os.chdir(cwd)
        if d in sys.path:
            sys.path.remove(d)


def _year(k):
    m = re.match(r"^(?:FY)?((?:19|20)\d{2})$", str(k))
    return int(m.group(1)) if m else None


def export(run):
    m, d = _load(run)
    if m is None:
        return None, "no panel.py in this run"
    out, keyed = {}, 0
    for name in SOURCES.get(run.upper(), ["IS"]):
        src = getattr(m, name, None)
        if not isinstance(src, dict):
            continue
        for k, v in src.items():
            y = _year(k)
            if y is None:
                continue
            out.setdefault(str(y), {})
            if isinstance(v, dict):
                for f, val in v.items():
                    out[str(y)]["%s.%s" % (name.lower(), f)] = val
            else:
                out[str(y)][name.lower()] = v
            keyed += 1
    if not out:
        return None, "the run's panel module holds no year-keyed dict among %s" \
                     % ", ".join(SOURCES.get(run.upper(), []))
    blob = {
        "_": ("As-reported figures EXPORTED from this run's own panel.py, so a later "
              "job can rebuild at a past origin from something committed. Nothing "
              "here is re-parsed or re-derived — it is exactly what the run "
              "computed, which is the only thing that makes it evidence."),
        "run": run.upper(),
        "exported_by": "engine/valuation_calibration/export_panels.py",
        "sources": SOURCES.get(run.upper(), []),
        "years": sorted(int(y) for y in out),
    }
    blob.update(out)
    p = os.path.join(d, "panel_export.json")
    json.dump(blob, open(p, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False, default=float)
    return p, "%d year(s), %d source-year pairs" % (len(out), keyed)


def main(argv):
    runs = [a.upper() for a in argv] or sorted(SOURCES)
    for r in runs:
        p, why = export(r)
        if p:
            print("  %-6s %s  -> %s" % (r, why, os.path.relpath(p, os.path.dirname(ENGINE))))
        else:
            print("  %-6s NOT EXPORTED — %s" % (r, why))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
