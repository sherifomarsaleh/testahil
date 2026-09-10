#!/usr/bin/env python3
"""Negative control for the terminal-basis gate.

A gate nobody has seen fail is not evidence. Every condition below is either a defect
the gate claims to catch or a legitimate construction it must stay silent on, injected
into an isolated copy of the tree — and EVERY MUTATION ASSERTS THAT IT LANDED before the
gate runs, because this project has caught a control passing a fixture that never
injected its condition five times.

THE CLEAN HALF IS THE HALF THAT MATTERS HERE. Three real constructions in this book look
like the defect and are not: EGCH DIVIDES by (1 + g), converting a terminal-year figure
back to last-explicit-year money — that is the correction already applied, and a gate
firing on it would condemn the fix; EMPOWER's two-stage terminal multiplies by a named
ten-year factor to reach stage two's own starting point; and PHAR deliberately rebuilds
the retired pre-grown construction to price what the defect was worth.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "check_terminal_basis.py")

CALL = """
import terminal_value as TV
t = TV.build(TV.TerminalInputs(%s))
"""


def sandbox():
    d = tempfile.mkdtemp(prefix="tbasis-")
    dst = os.path.join(d, "repo")
    shutil.copytree(ROOT, dst, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", ".git", "*.pyc"))
    return d, dst


def run(dst):
    r = subprocess.run([sys.executable, os.path.join(dst, "scripts",
                                                     "check_terminal_basis.py")],
                       capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout + r.stderr


def plant(dst, body):
    """Write a synthetic caller into a study directory and assert it landed."""
    d = os.path.join(dst, "engine", "planted_study")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "compute.py")
    open(p, "w", encoding="utf-8").write(body)
    got = open(p, encoding="utf-8").read()
    assert "TerminalInputs" in got, "fixture did not land: no call written"
    return p


def main():
    print("terminal-basis gate — negative control")
    out = []

    def case(name, body, must_fail, expect=None):
        d, dst = sandbox()
        try:
            if body is not None:
                plant(dst, body)
                if expect:
                    src = open(os.path.join(dst, "engine", "planted_study",
                                            "compute.py"), encoding="utf-8").read()
                    assert expect in src, "fixture did not land: %r absent" % expect
            rc, txt = run(dst)
            red = rc != 0
            ok = (red == must_fail)
            if must_fail and red and body is not None:
                ok = "planted_study" in txt          # red for the RIGHT subject
            out.append((name, ok))
            print("  %-4s %-64s exit %d" % ("ok" if ok else "FAIL", name[:64], rc))
            if not ok:
                for line in txt.strip().splitlines()[-6:]:
                    print("        " + line[:150])
        finally:
            shutil.rmtree(d, ignore_errors=True)

    # ---- must go RED ---------------------------------------------------------
    case("a NOPAT pre-grown by (1+g)",
         CALL % "nopat=n[-1] * (1 + g), wacc=w, inflation=pi", True,
         expect="(1 + g)")

    case("a book D&A pre-grown by (1+g)",
         CALL % "nopat=n[-1], dna_book=d[-1] * (1 + g), wacc=w", True,
         expect="d[-1] * (1 + g)")

    case("the growth factor written the other way round",
         CALL % "nopat=(1 + g) * n[-1], wacc=w", True,
         expect="(1 + g) * n[-1]")

    case("a splatted call nobody declared",
         "\nimport terminal_value as TV\nti = dict(nopat=1.0)\n"
         "t = TV.build(TV.TerminalInputs(**ti))\n", True,
         expect="**ti")

    case("a declaration with an EMPTY reason switches the check off",
         "\nimport terminal_value as TV\n# TERMINAL-BASIS-EXCEPTION:\n"
         "t = TV.build(TV.TerminalInputs(nopat=n[-1] * (1 + g), wacc=w))\n", True,
         expect="TERMINAL-BASIS-EXCEPTION:")

    # ---- must stay GREEN -----------------------------------------------------
    case("EGCH's construction — DIVIDING by (1+g) is the CORRECTION",
         CALL % "nopat=nopat_T / (1 + g), wacc=w, inflation=pi", False,
         expect="/ (1 + g)")

    case("EMPOWER's two-stage — a NAMED ten-year factor, not one year",
         CALL % "nopat=n['FY30'] * grow10, dna_book=d['FY30'] * grow10, wacc=w", False,
         expect="* grow10")

    case("a pre-grown call DECLARED with a real reason",
         "\nimport terminal_value as TV\n"
         "# TERMINAL-BASIS-EXCEPTION: prices the retired construction; nothing\n"
         "# downstream discounts this terminal.\n"
         "t = TV.build(TV.TerminalInputs(nopat=n[-1] * (1 + g), wacc=w))\n", False,
         expect="prices the retired construction")

    case("a plain last-explicit-year call",
         CALL % "nopat=n[-1], dna_book=d[-1], wacc=w, inflation=pi", False,
         expect="nopat=n[-1]")

    case("the repository as it stands must stay GREEN", None, False)

    print()
    bad = [n for n, ok in out if not ok]
    if not bad:
        print("negative control OK — %d/%d conditions behaved as required" % (len(out), len(out)))
        return 0
    print("NEGATIVE CONTROL FAILED — %d of %d wrong: %s"
          % (len(bad), len(out), ", ".join(bad)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
