#!/usr/bin/env python3
"""Negative control for [R-CAL-02]'s gate: prove it catches the real defect.

A check nobody has seen fail is not evidence. This reinjects the exact text the
site carried on 24-Aug-2026 -- and a band record deliberately disagreeing with
its panel -- into throwaway copies, and asserts the gate goes red on each. If any
case passes, the gate is asleep and this exits nonzero.

It copies only what the gate READS. The first cut did shutil.copytree of the whole
repository once per case -- 1,627 files and 319 MB each, five times, 33 s per copy
on a cold CI checkout -- to mutate one file, while the gate opens 211 files and
7.7 MB. engine/*_study/ and engine/raw_ohlc/ were copied five times and never
opened. Hence the --root argument on the gate.

Also carries a CLEAN arm: legitimate text that must NOT be flagged, following
check_protocol_text_negative_control.py. Without it a gate that flagged
everything would pass this control.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CASES = [
    ("the FAIL banner", "legacy/ledger.html",
     lambda s: s.replace("</body>",
                         '<p>⚠ INDICATIVE ONLY · FAILED CALIBRATION TEST</p></body>', 1)),
    ("a PARITY verdict in a thesis", "assets/coverage.js",
     lambda s: s.replace("const COVERAGE_EN = [",
                         'const X = "\\u00a73 The calibration is PARITY, not skill.";\n'
                         'const COVERAGE_EN = [', 1)),
    ("a matches-benchmark chip", "method.html",
     lambda s: s.replace("</body>", "<p>◆ Indicative · matches benchmark</p></body>", 1)),
    ("CRPS beside a company", "legacy/savola.html",
     lambda s: s.replace("</body>", "<p>SAVOLA scored +0.9% CRPS skill.</p></body>", 1)),
    ("a band record that disagrees with its panel", "assets/data.js",
     lambda s: re.sub(r'(  SAVOLA: \{mkt:"SA", n:)\d+', r'\g<1>999', s, count=1)),
    ("a hand-edited coverage figure", "assets/data.js",
     lambda s: re.sub(r'(  SAVOLA: \{mkt:"SA", n:\d+, hits:)\d+', r'\g<1>58', s, count=1)),
    ("a span naming no record", "legacy/savola.html",
     lambda s: s.replace('data-band-record="SAVOLA"', 'data-band-record="NOSUCHNAME"', 1)),
    # The figures are images; only their caption TEMPLATE is readable, and this
    # arm is live only because the ratchet is now empty. It is the one that would
    # catch the verdict creeping back into 93 pictures no text check can read.
    ("the verdict back in the figure caption", "engine/metal_backtest.py",
     lambda s: s.replace('    h2 = ("{cov90} of {n} windows',
                         '    h2 = ("PARITY  \u00b7  {cov90} of {n} windows', 1)),
]

# Text that must NOT trip the gate. A check that flags everything is not a check:
# lowercase "parity" is an ordinary word in this book, and CRPS is taught on the
# methodology page on purpose.
CLEAN = [
    ("a currency peg", "legacy/savola.html",
     lambda s: s.replace("</body>", "<p>the riyal's fixed parity to the dollar</p></body>", 1)),
    ("export parity pricing", "legacy/savola.html",
     lambda s: s.replace("</body>", "<p>subsidised vs. export parity feedstock</p></body>", 1)),
    ("CRPS where the rule is taught", "method.html",
     lambda s: s.replace("</body>", "<p>Forecasts are graded with CRPS.</p></body>", 1)),
]

# Only what the gate opens.
COPY = ["*.html", "legacy/*.html", "assets/*.js", "engine/band_record.py", "engine/panels/*_3m.csv",
        "engine/panel_refresh.py", "engine/mc_v3.py", "engine/primitives.py",
        "engine/market_profiles.py", "engine/fv_overlay.py", "engine/__init__.py",
        "engine/build_depth_audit/band_outstanding.json", "engine/metal_backtest.py",
        "engine/primitives.py",
        "scripts/build_market_registry.py", "scripts/build_band_records.py",
        "scripts/check_band_vocabulary.py"]


def stage(dst):
    """Copy only the paths the gate reads, preserving layout."""
    import glob as _g
    n = 0
    for pat in COPY:
        for src in _g.glob(os.path.join(ROOT, pat)):
            rel = os.path.relpath(src, ROOT)
            out = os.path.join(dst, rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copy2(src, out)
            n += 1
    return n


def run_case(label, rel, mutate, must_fail):
    with tempfile.TemporaryDirectory() as tmp:
        work = os.path.join(tmp, "repo")
        stage(work)
        path = os.path.join(work, rel)
        src = open(path, encoding="utf-8").read()
        out = mutate(src)
        if out == src:
            return f"{label}: could not inject into {rel} — control is stale"
        open(path, "w", encoding="utf-8").write(out)
        r = subprocess.run([sys.executable,
                            os.path.join(ROOT, "scripts", "check_band_vocabulary.py"),
                            "--root", work], capture_output=True, text=True)
        red = r.returncode != 0
        if red != must_fail:
            what = "PASSED on an injected defect" if must_fail else "FAILED on legitimate text"
            return f"{label}: gate {what} in {rel}"
        print(f"  {'caught' if must_fail else 'allowed'}: {label}  ({rel})")
        return None


def main():
    failures = [f for f in
                [run_case(*c, must_fail=True) for c in CASES] +
                [run_case(*c, must_fail=False) for c in CLEAN]
                if f]
    if failures:
        print("NEGATIVE CONTROL FAILED:")
        for f in failures:
            print("  " + f)
        return 1
    print(f"negative control OK — {len(CASES)} defects caught, "
          f"{len(CLEAN)} legitimate cases allowed through")
    return 0


if __name__ == "__main__":
    sys.exit(main())
