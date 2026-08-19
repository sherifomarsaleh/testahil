#!/usr/bin/env python3
"""Critique-response pricing harness — SAVOLA second-edition response (19-Aug-2026).

Prices every material critique finding through the study's own compute.py, one
override set per finding, against the delivered base (central 28.0166, DCF
26.2042). Same pattern as the RIYADHCABLE response harness: exec the CALC
section only (truncated before EMIT), with `V.update(_OVR)` injected right
after the V dict is built, plus optional source patches for findings that
change code paths rather than input values.
"""
import io, json, re, sys, contextlib
from pathlib import Path

HERE = Path(__file__).parent
SRC = (HERE / 'compute.py').read_text()
SRC = SRC[:SRC.index('# ============================ EMIT')]
ANCHOR = "V = {k: r['value'] for k, r in INP.items()}"
assert ANCHOR in SRC
SRC = SRC.replace(ANCHOR, ANCHOR + "\nV.update(_OVR)")

BASE_CENTRAL = 28.016591405896726
BASE_DCF = 26.204159458590066


def run(ovr=None, patches=None):
    """Run the CALC section with value overrides and/or source patches."""
    src = SRC
    for old, new in (patches or []):
        assert old in src, f"patch target not found: {old[:80]}"
        src = src.replace(old, new)
    ns = {'_OVR': ovr or {}, '__file__': str(HERE / 'compute.py')}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, 'compute_calc', 'exec'), ns)
    return ns


def price(name, ns):
    c, d = ns['CENTRAL'], ns['PS_A']
    print(f"{name:58s} central {c:8.4f} ({c - BASE_CENTRAL:+7.4f}, "
          f"{(c / BASE_CENTRAL - 1) * 100:+6.2f}%) | DCF {d:8.4f} ({d - BASE_DCF:+7.4f})")
    return c, d


if __name__ == '__main__':
    ns = run()
    c, d = ns['CENTRAL'], ns['PS_A']
    print(f"BASE reproduce: central {c:.10f} (delta {c - BASE_CENTRAL:+.2e}) | "
          f"DCF {d:.10f} (delta {d - BASE_DCF:+.2e})")
    assert abs(c - BASE_CENTRAL) < 1e-9 and abs(d - BASE_DCF) < 1e-9
    print("base OK — 4dp+ reproduction of the delivered study")
