#!/usr/bin/env python3
"""Every calibrated name ships a report, a workbook and the papers that go with them.

[R-FCAL-01] already requires it — *"EVERY RUN PRODUCES TWO DOCUMENTS AND A RUN THAT
PRODUCES ONE IS NOT FINISHED: (1) THE UPDATED FUNDAMENTAL ANALYSIS at full
model-report depth (16-section Word, 16-sheet Excel, standalone bibliography, QC
gate); (2) THE UPDATED LESSONS-LEARNT DOCUMENT"* — and NOTHING CHECKED IT. That is
the [R-ENF-01] species exactly: a rule that was written, agreed and unenforced,
which is the state every defect this repository has paid for was found in.

It matters now rather than later because the campaign has most of a book still to
run. A missing deliverable on one name is an afternoon; the same omission repeated
across eighty is the difference between a research programme and a pile of scripts.

WHAT IT ASSERTS, per calibrated name — the population being the walk-forward run
directories on disk, so it grows by itself as the campaign runs:

  a study directory            engine/{ticker}_study/
  a Word report                *Valuation_Study*.docx
  its PDF                      the same stem, .pdf — the rendered document is a
                               GATE in this house, not a convenience, and it
                               cannot be read if it was never produced
  a workbook                   *Valuation_Model*.xlsx (its SHEETS are
                               check_workbook_structure.py's job, not this one's)
  a standalone bibliography    *Bibliography*.docx or *Sources*.docx — TMGH names
                               its Sources and PHDC names its Bibliography, and a
                               gate that knew only one name would have reported a
                               conforming study as short
  a QC gate                    QC_GATE_{DD-MM-YYYY}.md

AND THAT THE EDITION AGREES WITH ITSELF. The report, the workbook, the
bibliography and the QC gate must all carry the SAME latest date. A study whose
newest report sits beside last edition's workbook is the L-066/L-067 defect —
a check pointed at a superseded file reports on something nobody receives — and
it is invisible to every gate that opens "the latest" of each artefact
separately.

RATCHET [R-ENF-02] · POPULATION ANCHORED [R-ENF-04]: as everywhere else. A run
that examined zero names REFUSES rather than reporting clean.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit",
                           "deliverables_outstanding.json")

DATE = re.compile(r"(\d{2})[-_]?(\d{2})[-_]?(\d{4})")


def _date(name):
    """The DD-MM-YYYY or DDMMYYYY stamp in a filename, as a sortable tuple."""
    m = DATE.search(name)
    if not m:
        return None
    d, mo, y = (int(x) for x in m.groups())
    if not (1 <= d <= 31 and 1 <= mo <= 12 and 2000 <= y <= 2100):
        return None
    return (y, mo, d)


def _latest(sdir, *patterns):
    """(path, date) of the newest file matching any pattern, or (None, None)."""
    best = (None, None)
    for pat in patterns:
        for p in glob.glob(os.path.join(sdir, pat)):
            dt = _date(os.path.basename(p))
            if dt and (best[1] is None or dt > best[1]):
                best = (p, dt)
    return best


def runs(engine=ENGINE):
    out = {}
    for d in sorted(glob.glob(os.path.join(engine, "*_walkforward"))):
        out[os.path.basename(d).replace("_walkforward", "").upper()] = d
    return out


REQUIRED = (
    ("report",       ("*Valuation_Study*.docx",)),
    ("report PDF",   ("*Valuation_Study*.pdf",)),
    ("workbook",     ("*Valuation_Model*.xlsx",)),
    ("bibliography", ("*Bibliograph*.docx", "*Sources*.docx", "*Biblio*.docx")),
    ("QC gate",      ("QC_GATE_*.md",)),
)


def check_study(sdir):
    """([] , {}) if the edition is complete and self-consistent, else the reasons."""
    if not os.path.isdir(sdir):
        return ["no study directory at %s" % os.path.relpath(sdir, ROOT)], {}
    bad, dates = [], {}
    for label, pats in REQUIRED:
        p, dt = _latest(sdir, *pats)
        if not p:
            bad.append("no %s (%s)" % (label, " or ".join(pats)))
            continue
        dates[label] = (os.path.basename(p), dt)
    if bad:
        return bad, dates
    newest = max(dt for _, dt in dates.values())
    behind = {k: v for k, v in dates.items() if v[1] != newest}
    if behind:
        stamp = "%04d-%02d-%02d" % newest
        for k, (fn, dt) in sorted(behind.items()):
            bad.append("the %s is dated %04d-%02d-%02d while the edition is %s (%s)"
                       % (k, dt[0], dt[1], dt[2], stamp, fn))
    return bad, dates


def load_outstanding():
    if not os.path.exists(OUTSTANDING):
        return {}
    try:
        return json.load(open(OUTSTANDING, encoding="utf-8")).get("outstanding", {})
    except Exception:
        return {}


def main(argv):
    prune = "--prune" in argv
    engine = ENGINE
    for a in argv:
        if a.startswith("--engine="):
            engine = a.split("=", 1)[1]
    found = runs(engine)
    if not found:
        print("REFUSED: no calibrated names were examined. An empty population is "
              "not a clean result [R-ENF-04].")
        return 2

    outstanding = load_outstanding()
    stale = [tk for tk in outstanding if tk not in found]
    ok, failed = [], {}
    for tk in sorted(found):
        sdir = os.path.join(engine, "%s_study" % tk.lower())
        bad, dates = check_study(sdir)
        if bad:
            failed[tk] = bad
        else:
            ok.append((tk, "%04d-%02d-%02d" % max(dt for _, dt in dates.values())))

    print("calibration deliverables [R-FCAL-01]\n")
    print("  calibrated names on disk  %d   %s"
          % (len(found), ", ".join(sorted(found))))
    print("  complete and self-consistent  %d" % len(ok))
    for tk, stamp in ok:
        print("     %-6s edition %s" % (tk, stamp))
    new = {tk: why for tk, why in failed.items() if tk not in outstanding}
    waived = {tk: why for tk, why in failed.items() if tk in outstanding}
    if waived:
        print("  waived on the ratchet  %d" % len(waived))
        for tk, why in sorted(waived.items()):
            print("     %-6s %s" % (tk, why[0]))
    if new:
        print("  NEW failures  %d" % len(new))
        for tk, why in sorted(new.items()):
            for w in why:
                print("     %-6s %s" % (tk, w))
    if stale:
        print("\n  REFUSED: the ratchet names names that are not calibrated: %s"
              % ", ".join(sorted(stale)))
        return 2

    if prune:
        keep = {tk: outstanding[tk] for tk in outstanding if tk in failed}
        json.dump({"_": ("Calibrated names whose delivered edition is incomplete or "
                         "inconsistent, allowed to fail. THE LIST MAY ONLY SHORTEN "
                         "[R-ENF-02]."),
                   "outstanding": keep},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        print("\n  pruned: %d name(s) remain outstanding" % len(keep))

    if new:
        print("\nFAILED — a calibrated name ships a report, its PDF, a workbook, a "
              "standalone bibliography and a QC gate, all of one edition.")
        return 1
    print("\nOK — every calibrated name ships a complete, self-consistent edition, "
          "or is a listed outstanding one.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
