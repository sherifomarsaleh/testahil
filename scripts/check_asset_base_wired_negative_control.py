#!/usr/bin/env python3
"""Negative control for [R-ASSET-02]. Four of its cases are the gate's own misses.

The gate decides whether a quantity is READ BY ARITHMETIC or only shown, and its whole
value is in the cases it nearly got wrong: a binding is not a use, a prose mention of a
word is not a use, and a format operator two physical lines above its argument is still a
format operator. Each of those let a real decorative land bank read as wired.

Nothing is written into the real tree.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DECLARED_CASES = 11

spec = importlib.util.spec_from_file_location(
    "abw", os.path.join(HERE, "check_asset_base_wired.py"))
abw = importlib.util.module_from_spec(spec)
src = open(spec.origin, encoding="utf-8").read().replace("sys.exit(main())", "pass")
exec(compile(src, spec.origin, "exec"), abw.__dict__)


def wired(body, name="land_bank_sqm_mn"):
    """Does the gate's own logic call this body a computation site?"""
    lines = abw.logical_lines(body.splitlines())
    for ln in lines:
        if name not in ln:
            continue
        if not abw.name_is_code(ln, name):
            continue
        if abw.is_presentation_line(ln, name):
            continue
        import re
        b = re.match(r"^(\w+)\s*=\s*[^=]", ln.strip())
        if b:
            local = b.group(1)
            uses = [l for l in lines
                    if abw.uses_outside_strings(l, local) and l.strip() != ln.strip()]
            if uses and all(abw.is_presentation_line(u, local) for u in uses):
                continue
        return True
    return False


CASES = []
def case(name, body, expect_wired, note=""):
    CASES.append((name, body, expect_wired, note))


# ---- NOT wired: the gate must see these as decorative -------------------
case("PHDC's shape — a printed workbook row",
     '("Land bank (mn sqm)", "land_bank_sqm_mn", "#,##0.0", ""),', False)
case("a registration only",
     '"land_bank_sqm_mn": I(33.0, "FY2024 release", "2024-12-31", "A"),', False)
case("TMGH's shape — bound, then used only as a format argument",
     'landbank = _v(kpi, "land_bank_sqm_mn")\n'
     'out = ("be earned on the book." % landbank)', False,
     "the binding is not the use")
case("a prose mention of the word does not make it wired",
     '# a business with a live land_bank_sqm_mn is undervalued\n'
     'x = "a live land_bank_sqm_mn is worth something"', False,
     "inside a string literal")
case("a format operator TWO PHYSICAL LINES above its argument",
     'p("  land bank "\n'
     '  "%.0f mn sqm" % (KPI["land_bank_sqm_mn"],\n'
     '                   OTHER["x"]))', False,
     "the logical line is what carries the operator")
case("a comment",
     '# land_bank_sqm_mn is 33.0 per the release', False)

# ---- WIRED: the gate must NOT refuse these ------------------------------
case("multiplied into a value",
     'gav = V["land_bank_sqm_mn"] * price_per_sqm', True)
case("bounding an absorption schedule",
     'remaining = V["land_bank_sqm_mn"] - cumulative_delivered', True)
case("bound, then used in arithmetic",
     'lb = V["land_bank_sqm_mn"]\nnav = lb * rate - debt', True,
     "the binding IS a use when the local name is computed with")
case("passed to a function that is not a printer",
     'rnav = absorb(V["land_bank_sqm_mn"], years=8)', True)
case("compared against a projection",
     'assert cum_area <= V["land_bank_sqm_mn"], "over-delivers the land bank"', True)


def main():
    print("[R-ASSET-02] negative control — a binding is not a use, and prose is not "
          "arithmetic\n")
    assert len(CASES) == DECLARED_CASES, (
        "case count moved: %d present, %d declared" % (len(CASES), DECLARED_CASES))
    bad = 0
    for name, body, expect, note in CASES:
        assert "land_bank_sqm_mn" in body, "CONDITION NOT INJECTED in %r" % name
        got = wired(body)
        ok = (got == expect)
        print("  %-6s [%s] %-58s %s"
              % ("ok" if ok else "WRONG", "WIRED " if expect else "SHOWN ", name[:58],
                 note))
        if not ok:
            bad += 1
    print("\n%d case(s): %d must read as WIRED, %d as SHOWN ONLY"
          % (len(CASES), sum(1 for c in CASES if c[2]),
             sum(1 for c in CASES if not c[2])))
    if bad:
        print("FAIL — %d case(s) did not behave as declared." % bad)
        return 1
    print("OK — tells a calculation from a caption.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
