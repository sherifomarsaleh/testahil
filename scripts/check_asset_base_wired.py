#!/usr/bin/env python3
"""[R-ASSET-02] — the asset base must be READ BY ARITHMETIC, not merely recorded and printed.

THIS CORRECTS A CLAIM I MADE THIS MORNING. [R-ASSET-01] and check_asset_base.py were built
against the principal's words — a study that "takes into consideration current landbank of a
developer but does not account for new land added" — and I reported the error caught. It is
caught FOR VINTAGE. engine/asset_base.py says so in its own docstring, which is the right
way to write a gate and the wrong thing to have overlooked when summarising it:

    "Everything here is about the RECORD, never about the number: this gate makes no claim
     that a land bank of 33 million square metres is right or wrong, only that the study
     says when it was true and that the date is not behind the study's own reading."

WHAT THE CENSUS FOUND, AND IT IS WORSE THAN THE PRINCIPAL'S DESCRIPTION. The land bank is
not merely stale in these studies — IT IS CONSUMED BY NO ARITHMETIC AT ALL. Verified by
hand on both developers on the book:

  PHDC  land_bank_sqm_mn  registered at inputs.py:138, committed to study_numbers.json,
        and printed as a workbook row at build_xlsx_phdc.py:336. THREE SITES, NONE OF THEM
        A CALCULATION.
  TMGH  landbank_msqm     registered at inputs.py:194, committed, printed at
        docx_tmgh.py:296, printed inside a gap-review calculation's output, and bound at
        experts.py:150 — where it is used at line 166 solely as a "%" FORMAT ARGUMENT in a
        sentence. That expert's net asset value is built from balance-sheet totals and
        never from land.

SO NEW LAND RAISES THE VALUE BY ZERO AND EXHAUSTED LAND LOWERS IT BY ZERO. A developer's
terminal is capitalised on a finite land bank with nothing objecting. And the figure is
PRINTED to the delivered workbook and the delivered prose, where a reader will reasonably
read it as a constraint that is doing work — which makes it worse than an absent input,
because an absent input does not mislead.

WHY A STATIC TEST RATHER THAN A PERTURBATION. The obvious instrument is
check_frozen_escalator's: change the quantity, re-run the generator, require the answer to
move. That is the stronger test and it is also the slower and more fragile one — it needs
every study's generator to run, and this morning's repair loop demonstrated that
re-running a generator moves fields nobody asked it to. THE CHEAP TEST FINDS EXACTLY WHAT
THE EXPENSIVE ONE WOULD HERE: a quantity read only by a document builder and a format
string cannot be in the arithmetic, and that is decidable by reading. A perturbation probe
remains the right next instrument for the cases this cannot decide, and saying so is not a
substitute for building it.

A PRESENTATION SITE IS NAMED BY WHAT IT IS, NOT GUESSED AT. A document or workbook builder
is presentation; a line where the name appears only as an argument to a format operator is
presentation; everything else is a candidate computation and this gate lets it pass. That
asymmetry is deliberate — the gate refuses only when it can see that EVERY site is
presentational, so a genuine computation it fails to recognise costs nothing.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")
RATCHET = os.path.join(ENGINE, "build_depth_audit", "asset_wired_outstanding.json")

# How this book names an asset-base quantity. Several spellings, because a reader that
# guesses one silently finds nothing [L-355].
QUANTITY_RX = re.compile(
    r"\b(land_?bank\w*|landbank\w*|\w*_msqm|\w*_sqm_mn|fleet_\w+|vessels?_count|"
    r"capacity_\w*t(?:pa|onnes)?|keys_\w+|installed_\w+)\b", re.I)

PRESENTATION_FILE_RX = re.compile(r"(^|/)(docx_|build_xlsx|build_docx|_docx|report_|"
                                  r"figures?|charts?)", re.I)


def logical_lines(lines):
    """Physical lines joined into logical ones, so a call split across lines is one site.

    TMGH prints its land bank inside a p(...) whose format operator sits two physical
    lines above the argument — so a per-PHYSICAL-line test sees only `KPI["landbank_msqm"]))`
    and calls it arithmetic. Brackets are counted outside string literals, which is why the
    scanner below exists; this is not a parser and does not need to be, because a
    mis-joined line only makes the gate more lenient, the direction it already errs in.
    """
    out, buf, depth = [], [], 0
    for ln in lines:
        buf.append(ln)
        in_q, q, i = False, "", 0
        while i < len(ln):
            c = ln[i]
            if in_q:
                if c == "\\":
                    i += 2
                    continue
                if c == q:
                    in_q = False
            elif c in "\"'":
                in_q, q = True, c
            elif c in "([{":
                depth += 1
            elif c in ")]}":
                depth -= 1
            i += 1
        if depth <= 0:
            out.append(" ".join(x.strip() for x in buf))
            buf, depth = [], 0
    if buf:
        out.append(" ".join(x.strip() for x in buf))
    return out


def uses_outside_strings(line, ident):
    """Occurrences of `ident` as CODE, not inside a quoted string.

    Needed because following a binding is defeated by prose: TMGH's experts.py mentions
    the word "landbank" inside an English sentence sixteen lines above the binding, and a
    plain substring search counts that as a use and calls the quantity wired. A one-line
    scanner is enough here — this is not a parser and does not need to be, since a false
    "in code" only makes the gate more lenient, which is the direction it already errs in.
    """
    out, in_q, q = [], False, ""
    i = 0
    while i < len(line):
        c = line[i]
        if in_q:
            if c == "\\":
                i += 2
                continue
            if c == q:
                in_q = False
        elif c in "\"'":
            in_q, q = True, c
        elif not in_q and line.startswith(ident, i) and \
                (i == 0 or not (line[i-1].isalnum() or line[i-1] == "_")) and \
                (i + len(ident) >= len(line) or
                 not (line[i+len(ident)].isalnum() or line[i+len(ident)] == "_")):
            out.append(i)
        i += 1
    return out


def _strings(line):
    """(start, end, body) for each quoted literal on a logical line."""
    out, i, n = [], 0, len(line)
    while i < n:
        c = line[i]
        if c in "\"'":
            q, j = c, i + 1
            while j < n:
                if line[j] == "\\":
                    j += 2
                    continue
                if line[j] == q:
                    break
                j += 1
            out.append((i, j, line[i + 1:j]))
            i = j + 1
            continue
        i += 1
    return out


def name_is_code(line, name):
    """Does `name` appear as CODE on this line, rather than only inside prose?

    A STRING IS NOT AUTOMATICALLY PROSE AND THIS IS THE DISTINCTION THE GATE TURNS ON.
    V["land_bank_sqm_mn"] is a dictionary lookup — the name is inside quotes and the line
    is arithmetic. "a live land_bank_sqm_mn is worth something" is a sentence that happens
    to contain the identifier. So the test is not whether the occurrence sits inside a
    string but whether THE STRING IS THE NAME: a bare key is code, a name embedded in a
    longer sentence is not. The gate's own negative control caught the first draft calling
    an English sentence a calculation.
    """
    lits = _strings(line)
    for a, b, body in lits:
        if body.strip() == name:
            return True                     # a bare key: V["name"], get("name")
    # any occurrence outside every literal is code
    for pos in uses_outside_strings(line, name):
        if not any(a < pos < b for a, b, _ in lits):
            return True
    return False


def is_presentation_line(line, name):
    """A site where the quantity can only be shown, never used."""
    s = line.strip()
    if s.startswith("#"):
        return True
    n = re.escape(name)
    # PATTERNS BUILT BY CONCATENATION, NEVER BY % INTERPOLATION. These patterns are
    # looking for a format operator, so they contain a literal per-cent sign — and
    # interpolating a name into them makes Python read the pattern's own "%" as a
    # conversion specifier. The first draft did exactly that and raised before it
    # checked anything, which is the loud kind of failure and the lucky one.
    if re.search("%" + r"\s*[\(\w]*" + n + r"\b", s):
        return True                       # an argument to a format operator
    if re.search("%" + r"\s*" + n + r"\s*\)?\s*$", s):
        return True
    if re.match(r"^(print|p)\s*\(", s):
        return True                       # inside a print
    if re.search(r"""\(\s*["'][^"']+["']\s*,\s*["']""" + n + r"""["']""", s):
        return True                       # a table-row tuple: ("Label", "key", fmt, "")
    if re.search(r"""["']""" + n + r"""["']\s*:""", s):
        return True                       # a registration: "key": I(...)
    return False


def main(argv=None):
    dirs = sorted(glob.glob(os.path.join(ENGINE, "*_study")))
    if not dirs:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    rat = json.load(open(RATCHET, encoding="utf-8")) if os.path.exists(RATCHET) else {}
    known = rat.get("outstanding") or {}
    if isinstance(known, list):
        known = {k: "" for k in known}

    examined, wired, fresh, listed = 0, [], [], []
    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        # the quantities this study COMMITS
        names = set()
        for nf in glob.glob(os.path.join(d, "*numbers*.json")):
            try:
                txt = open(nf, encoding="utf-8").read()
            except Exception:
                continue
            names |= {m.group(1) for m in QUANTITY_RX.finditer(txt)}
        if not names:
            continue
        examined += 1

        for name in sorted(names):
            comp_sites = []
            for p in sorted(glob.glob(os.path.join(d, "*.py"))):
                base = os.path.basename(p)
                try:
                    lines = logical_lines(
                        open(p, encoding="utf-8").read().splitlines())
                except Exception:
                    continue
                if PRESENTATION_FILE_RX.search(base):
                    continue
                for ln in lines:
                    if name not in ln:
                        continue
                    if not name_is_code(ln, name):
                        continue          # the name occurs only inside prose
                    if is_presentation_line(ln, name):
                        continue
                    # THE BINDING IS NOT THE USE, and the first draft stopped at the
                    # binding. TMGH does `landbank = _v(kpi, "landbank_msqm")` and then
                    # uses `landbank` sixteen lines later as a "%" format argument in a
                    # sentence — so the quantity is decorative and a reader of the
                    # ASSIGNMENT alone would call it wired. Where a line only BINDS the
                    # quantity to a local name, the local name is followed: if every one
                    # of ITS uses is presentational too, the site is presentational.
                    bind = re.match(r"^(\w+)\s*=\s*[^=]", ln.strip())
                    if bind:
                        local = bind.group(1)
                        uses = [l for l in lines
                                if uses_outside_strings(l, local)
                                and l.strip() != ln.strip()]
                        if uses and all(is_presentation_line(u, local) for u in uses):
                            continue
                    comp_sites.append("%s: %s" % (base, ln.strip()[:70]))
            if comp_sites:
                wired.append((tk, name, comp_sites[0]))
            else:
                why = ("%s is registered, committed and printed, and read by no arithmetic "
                       "— new asset raises the value by zero and exhausted asset lowers it "
                       "by zero" % name)
                (listed if tk in known else fresh).append((tk, why))

    print("[R-ASSET-02] the asset base is read by arithmetic, not only recorded and printed")
    print("  studies committing an asset quantity : %d" % examined)
    print("  quantities WIRED into a calculation  : %d" % len(wired))
    print("  outstanding (allowed)                : %d" % len(listed))
    for tk, name, site in sorted(wired)[:8]:
        print("     %-13s %-22s %s" % (tk, name, site))

    if not examined:
        print("\nFAIL — read zero asset quantities across %d study directories. A reader "
              "that stopped matching reads exactly like a book with none [R-ENF-04]."
              % len(dirs))
        return 1

    rc = 0
    if fresh:
        rc = 1
        print("\nFAIL — an asset quantity that no arithmetic reads:")
        for tk, why in sorted(fresh):
            print("   %-13s %s" % (tk, why))
    if listed:
        print("\nstill outstanding, allowed for now (%d):" % len(listed))
        for tk, why in sorted(listed):
            print("   %-13s %s" % (tk, why))

    ghosts = sorted(set(known) - {os.path.basename(d)[:-6].upper() for d in dirs})
    if ghosts:
        rc = 1
        print("\nFAIL — ratchet names studies not on disk [R-ENF-04]: %s"
              % ", ".join(ghosts))

    print("\n%s" % ("FAIL" if rc else "OK — no new decorative asset quantity."))
    return rc


if __name__ == "__main__":
    sys.exit(main())
