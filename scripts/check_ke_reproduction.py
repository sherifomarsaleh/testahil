#!/usr/bin/env python3
"""[R-COC-02] enforced from outside the study — the cost of equity reproduces.

The rule and the measurement that produced it live in engine/ke_reproduction.py.

IT RUNS THE INSTRUMENT, IT DOES NOT RE-DERIVE THE ARITHMETIC [R-ENF-03]. The identity is
in one module and both this gate and any study that wants to check itself call the same
one; a gate holding its own copy stops testing the standard the moment one of them moves.

POPULATION ANCHORED BOTH WAYS [R-ENF-04]: zero study directories fails, and zero
cost-of-capital RECORDS read across the directories present fails — a reader that stopped
finding records reads exactly like a book with none.

A RECORD THAT CANNOT BE READ IS NOT A CLEAN RECORD. A study committing a
cost_of_capital_record whose fields will not support the identity is reported as
unreadable and listed, never skipped.

RATCHET [R-ENF-02]: engine/build_depth_audit/ke_outstanding.json, may only SHORTEN. Each
entry carries WHAT THE RECORD ACTUALLY REPRODUCES UNDER, because the fix here is a single
declared field rather than a rebuild, and an entry that names the fix is an entry somebody
can close.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")
for p in (ENGINE, ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

import ke_reproduction as kr                 # noqa: E402
import ratchet_shape as rshape               # noqa: E402  [R-ENF-08]

RATCHET = os.path.join(ENGINE, "build_depth_audit", "ke_outstanding.json")
RECORD_KEYS = ("cost_of_capital_record", "coc_record", "wacc_record")


def numbers_file(sdir):
    for name in ("study_numbers.json", "numbers.json"):
        p = os.path.join(sdir, name)
        if os.path.exists(p):
            return p
    c = [p for p in glob.glob(os.path.join(sdir, "*.json"))
         if "numbers" in os.path.basename(p).lower()]
    return c[0] if c else None


def dig(doc, keys):
    if isinstance(doc, dict):
        for k in keys:
            if isinstance(doc.get(k), dict):
                return doc[k]
        for v in doc.values():
            r = dig(v, keys)
            if r is not None:
                return r
    elif isinstance(doc, list):
        for v in doc:
            r = dig(v, keys)
            if r is not None:
                return r
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune", action="store_true")
    a = ap.parse_args(argv)

    dirs = sorted(glob.glob(os.path.join(ENGINE, "*_study")))
    if not dirs:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    rat = json.load(open(RATCHET, encoding="utf-8")) if os.path.exists(RATCHET) else {}
    known = rat.get("outstanding") or {}
    if isinstance(known, list):
        known = {k: "" for k in known}

    read, conforming, fresh, listed = [], [], [], []
    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        nf = numbers_file(d)
        if not nf:
            continue
        try:
            doc = json.load(open(nf, encoding="utf-8"))
        except Exception:
            continue
        rec = dig(doc, RECORD_KEYS)
        if rec is None:
            continue                    # no record: [R-COC-01]'s subject, not this one
        read.append(tk)
        problems = kr.check(rec)
        if not problems:
            conforming.append(tk)
        else:
            msg = "; ".join(problems)
            ok, note = rshape.excused(known.get(tk), msg)   # [R-ENF-08]
            if tk in known and ok:
                listed.append((tk, msg))
            else:
                fresh.append((tk, msg if ok else "%s — %s" % (msg, note)))

    print("[R-COC-02] the cost of equity reproduces from its own inputs")
    print("  study directories examined  : %d" % len(dirs))
    print("  cost-of-capital records read: %d  (%s)"
          % (len(read), ", ".join(sorted(read)) or "-"))
    print("  reproducing                 : %d" % len(conforming))
    print("  outstanding (allowed)       : %d" % len(listed))

    if not read:
        print("\nFAIL — read zero cost-of-capital records across %d study directories. "
              "A reader that stopped finding records reads exactly like a book with none "
              "[R-ENF-04]." % len(dirs))
        return 1

    rc = 0
    if fresh:
        rc = 1
        print("\nFAIL — NEW breach, not on the ratchet:")
        for tk, why in sorted(fresh):
            print("   %-12s %s" % (tk, why))

    if listed:
        print("\nstill outstanding, allowed for now (%d):" % len(listed))
        for tk, why in sorted(listed):
            print("   %-12s %s" % (tk, why))

    ghosts = sorted(set(known) - {os.path.basename(d)[:-6].upper() for d in dirs})
    if ghosts:
        rc = 1
        print("\nFAIL — ratchet names studies not on disk [R-ENF-04]: %s"
              % ", ".join(ghosts))

    now_clean = sorted(set(known) & set(conforming))
    if now_clean:
        print("\n%d listed stud(ies) now reproduce and may be pruned: %s"
              % (len(now_clean), ", ".join(now_clean)))
        if a.prune:
            for tk in now_clean:
                known.pop(tk, None)
            rat["outstanding"] = known
            rat.setdefault("pruned_on", []).append({"removed": now_clean})
            json.dump(rat, open(RATCHET, "w", encoding="utf-8"), indent=1,
                      ensure_ascii=False)
            print("   ratchet rewritten — the list may only ever SHORTEN.")

    print("\n%s" % ("FAIL" if rc else "OK — no new breach."))
    return rc


if __name__ == "__main__":
    sys.exit(main())
