"""Negative control for the point-in-time macro archive's refusals.

The archive's whole claim is that it REFUSES rather than fills. A refusal nobody
has seen fire is not evidence, and this module's refusals are unusually easy to
believe in without testing, because the happy path looks identical either way:
a figure that should have been rejected simply sits there being a number.

Every case below is a defect the archive claims to catch, built in a temporary
directory, plus clean cases that must NOT fire.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import macro_history as MH  # noqa: E402


def good(**over):
    rec = {"value": 0.10, "source": "a named document, read on a stated date",
           "date": "2016-12-31", "tier": "Global", "revision_class": "observed"}
    rec.update(over)
    return rec


CASES = [
    ("a bare value with no source at all", {"erp": 0.10}, True),
    ("no value", good(value=None), True),
    ("no source", good(source=""), True),
    ("no date", good(date=""), True),
    ("no tier", good(tier=""), True),
    ("no revision class", good(revision_class=""), True),
    ("a tier that is not one of the four", good(tier="Vendor"), True),
    ("a revision class that is not one of the two", good(revision_class="final"), True),
    ("an ESTIMATED figure with no vintage named",
     good(revision_class="estimated"), True),
    ("an as-of date AFTER the origin it is filed under",
     good(date="2017-03-31"), True),
    ("published after the origin with no reason given",
     good(published="2017-06-01"), True),
    # ---- clean cases that must NOT fire -------------------------------------
    ("CLEAN — an observed figure dated at the origin", good(), False),
    ("CLEAN — an estimated figure naming its vintage",
     good(revision_class="estimated", vintage="ctryprem16.xls (Updated January 5, 2017)"),
     False),
    ("CLEAN — published just after the origin, WITH the reason recorded",
     good(published="2017-01-05",
          publication_lag_note="computed on data through this origin's year-end"),
     False),
]


def run_one(fig):
    tmp = tempfile.mkdtemp(prefix="mh-")
    old = MH.ARCHIVE_DIR
    try:
        MH.ARCHIVE_DIR = tmp
        json.dump({"market": "ZZ", "origins": [{"year": 2016, "figures": {"erp": fig}}]},
                  open(os.path.join(tmp, "ZZ.json"), "w"))
        try:
            MH.origin("ZZ", 2016)
            return False, ""
        except MH.VintageMissing as exc:
            return True, str(exc)[:90]
    finally:
        MH.ARCHIVE_DIR = old


def main():
    print("point-in-time macro archive — negative control")
    ok = []
    for name, fig, must_raise in CASES:
        raised, msg = run_one(fig)
        good_ = (raised == must_raise)
        ok.append(good_)
        print("  %-58s %s   %s" % (name[:58], "ok  " if good_ else "MISS",
                                   msg if raised else "(accepted)"))

    # The population guard: a real archive on disk must actually be readable, and
    # an archive that has stopped being fed must not read as clean. [R-ENF-04]
    rep = MH.report("EG")
    n_declared = len(rep["declared"])
    if n_declared == 0:
        print("\n  MISS — the EG archive declares zero origins. An empty archive is "
              "not a clean archive.")
        ok.append(False)
    else:
        print("\n  EG archive: %d declared, %d usable — the report is the only place "
              "to read this." % (n_declared, len(rep["usable"])))

    print()
    if all(ok):
        print("negative control OK — the archive refuses every injected defect and "
              "accepts every clean case")
        return 0
    print("NEGATIVE CONTROL FAILED — %d of %d cases came back wrong."
          % (sum(1 for r in ok if not r), len(ok)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
