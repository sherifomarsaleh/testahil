#!/usr/bin/env python3
"""[R-ASSET-01] enforced from outside the study — the operating asset base's vintage.

The rule and the reasoning live in engine/asset_base.py; this runs it over the book.

SCOPE IS DERIVED, NOT TYPED. A study is in scope when the class it commits carries an
asset-based lens in research_protocol.LENS_REGISTRY. Importing the registry rather than
keeping a copy of it is [R-ENF-03]: a check holding its own copy of a standard stops
testing the standard the moment one of them moves.

A CLASS THAT DOES NOT RESOLVE IS RED, NEVER SKIPPED. That is the clause this gate exists
around as much as the vintage test: TMGH writes its class with an em dash where the
registry uses a comma, and a gate that looked it up and moved on when it missed would
silently exempt a developer — an absent answer wearing a clean answer's clothes [R-ENF-04].

POPULATION ANCHORED BOTH WAYS [R-ENF-04]: zero study directories fails, zero IN-SCOPE
classes resolved from the registry fails (the registry read broke rather than the book
being clear), and every ticker on the ratchet must resolve to a directory on disk.

RATCHET [R-ENF-02]: studies predating the rule are listed in
engine/build_depth_audit/asset_base_outstanding.json WITH THEIR MEASUREMENT where one
exists, so the debt is countable rather than remembered. The list may only ever SHORTEN
(--prune). The build breaks on a NEW in-scope study with no entry either way.
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

import asset_base as ab                      # noqa: E402
import research_protocol as rp               # noqa: E402

RATCHET = os.path.join(ENGINE, "build_depth_audit", "asset_base_outstanding.json")

# Where a study writes the two things this gate reads. Several spellings, because the book
# already uses several and a reader that guesses one silently finds nothing [L-355].
CLASS_KEYS = ("class", "lens_class", "study_class")
INFOSET_KEYS = ("information_set_ends", "information_set", "info_set_ends",
                "data_through", "disclosure_through")
RECORD_KEYS = ("asset_base_record", "asset_base")


def numbers_file(sdir):
    for name in ("study_numbers.json", "numbers.json"):
        p = os.path.join(sdir, name)
        if os.path.exists(p):
            return p
    c = [p for p in glob.glob(os.path.join(sdir, "*.json"))
         if "numbers" in os.path.basename(p).lower()]
    return c[0] if c else None


def dig(doc, keys):
    """First value under any of `keys`, at any depth. Depth-first, deterministic."""
    if isinstance(doc, dict):
        for k in keys:
            if k in doc and doc[k] not in (None, ""):
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


def load_ratchet():
    if not os.path.exists(RATCHET):
        return {"why": "", "outstanding": {}, "pruned_on": []}
    return json.load(open(RATCHET, encoding="utf-8"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune", action="store_true",
                    help="rewrite the ratchet with the studies that now conform removed")
    a = ap.parse_args(argv)

    scope = ab.in_scope_classes(rp.LENS_REGISTRY)
    if not scope:
        print("FAIL — no asset-based class resolved from LENS_REGISTRY. The registry read "
              "broke; this is not a book with no asset-based companies in it.")
        return 1

    dirs = sorted(glob.glob(os.path.join(ENGINE, "*_study")))
    if not dirs:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    rat = load_ratchet()
    known = rat.get("outstanding") or {}
    if isinstance(known, list):                     # tolerate the plain-list shape
        known = {k: "" for k in known}

    examined, in_scope, conforming, fresh_fail, listed_fail, unresolved = [], [], [], [], [], []

    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        examined.append(tk)
        nf = numbers_file(d)
        if not nf:
            continue
        try:
            doc = json.load(open(nf, encoding="utf-8"))
        except Exception as e:
            listed_fail.append((tk, "numbers file will not parse: %s" % e))
            continue

        cls = dig(doc, CLASS_KEYS)
        if not isinstance(cls, str) or not cls.strip():
            continue                                # no class committed: not this gate's subject
        norm = ab.normalise_class(cls)
        if norm not in scope:
            # Is it a registry class at all? An unregistered class is [R-LENS-03]'s
            # business; a class that IS in the registry but not asset-based is simply
            # out of scope here. Anything else is a string nobody can resolve.
            allknown = {ab.normalise_class(k) for k in rp.LENS_REGISTRY}
            if norm not in allknown:
                unresolved.append((tk, cls))
            continue

        in_scope.append(tk)
        rec = dig(doc, RECORD_KEYS)
        infoset = dig(doc, INFOSET_KEYS)
        if infoset in (None, ""):
            problems = ["the study states no information-set end date, so its asset base "
                        "cannot be held to anything"]
        else:
            problems = ab.check(rec, infoset)

        if not problems:
            conforming.append(tk)
        elif tk in known:
            listed_fail.append((tk, "; ".join(problems)))
        else:
            fresh_fail.append((tk, "; ".join(problems)))

    print("[R-ASSET-01] the operating asset base's vintage, checked from outside")
    print("  study directories examined : %d" % len(examined))
    print("  asset-based classes in the registry : %d" % len(scope))
    print("  studies IN SCOPE           : %d  (%s)"
          % (len(in_scope), ", ".join(sorted(in_scope)) or "-"))
    print("  conforming                 : %d" % len(conforming))
    print("  outstanding (allowed)      : %d" % len(listed_fail))

    if not in_scope:
        print("\nFAIL — zero studies resolved into scope across %d directories. The book "
              "holds developers, cement and shipping names; a run finding none of them "
              "read nothing [R-ENF-04]." % len(examined))
        return 1

    rc = 0
    if unresolved:
        rc = 1
        print("\nFAIL — a committed class that resolves to NOTHING in LENS_REGISTRY. This "
              "is red rather than skipped, because a name nobody can resolve is silently "
              "exempt from every class-scoped rule:")
        for tk, cls in sorted(unresolved):
            print("   %-12s %r" % (tk, cls))

    if fresh_fail:
        rc = 1
        print("\nFAIL — NEW breach, not on the ratchet:")
        for tk, why in sorted(fresh_fail):
            print("   %-12s %s" % (tk, why))

    if listed_fail:
        print("\nstill outstanding, allowed for now (%d):" % len(listed_fail))
        for tk, why in sorted(listed_fail):
            note = known.get(tk) or ""
            print("   %-12s %s" % (tk, why))
            if note:
                print("   %-12s   reason on the ratchet: %s" % ("", note))

    ghosts = sorted(set(known) - set(examined))
    if ghosts:
        rc = 1
        print("\nFAIL — ratchet names studies that do not exist on disk [R-ENF-04]: %s"
              % ", ".join(ghosts))

    now_clean = sorted(set(known) & set(conforming))
    if now_clean:
        print("\n%d listed stud(ies) now conform and may be pruned: %s"
              % (len(now_clean), ", ".join(now_clean)))
        if a.prune:
            for tk in now_clean:
                known.pop(tk, None)
            rat["outstanding"] = known
            rat.setdefault("pruned_on", []).append(
                {"removed": now_clean})
            json.dump(rat, open(RATCHET, "w", encoding="utf-8"),
                      indent=1, ensure_ascii=False)
            print("   ratchet rewritten — the list may only ever SHORTEN.")

    print("\n%s" % ("FAIL" if rc else "OK — no new breach."))
    return rc


if __name__ == "__main__":
    sys.exit(main())
