#!/usr/bin/env python3
"""[R-STD-02] — a study's standard version is a CLAIM, and a rebuild may not re-assert it.

WHAT THE STAMP MEANS, from research_protocol.STANDARD_VERSION_NOTE's own text: it
enumerates what a study at that version DOES — a v2 cost of capital, a conforming beta, a
ground-up forecast, the three gates called in its own code, a dated gap review, and since
today an asset_base_record and a declared terminal construction. So a study stamped
2026.09.07 is asserting it does all of those. The stamp is a CONFORMANCE CLAIM, not a
build timestamp.

AND SIX STUDIES STAMP IT FROM THE LIVE CONSTANT. They import research_protocol and write
research_protocol.STANDARD_VERSION into their committed numbers, so every rebuild
re-asserts conformance to whatever standard happens to be current — silently, with nobody
deciding. One study's attestation goes further and REQUIRES it: it asserts the committed
stamp equals the live constant, so a rebuild cannot decline to make the claim.

THIS IS A DEFECT THIS REPOSITORY HAS ALREADY FOUND ONCE, IN ANOTHER FIELD. [R-ENF-01
EXTENDED 07-09-2026] found a generator that "stamped its study date with the clock rather
than with a fact, SO REBUILDING THE STUDY RESTAMPED A DELIVERED DOCUMENT'S ACCOUNT OF WHEN
THE WORK WAS DONE", and froze it to the date the document already carried. This is the same
shape one field over: a claim about the study, taken from a constant that moves on its own.

IT IS LATENT RATHER THAN LIVE TODAY, and saying which matters. All seven studies carrying a
stamp read 2026.09.01 against a live 2026.09.07, so none over-claims — because none has
been rebuilt since the bump. THE NEXT REBUILD OF ANY OF THEM CREATES THE OVER-CLAIM BY
CONSTRUCTION. The repair loop caught exactly this on PHDC and TMGH and reverted, but only
because it happened to be running; nothing made it a rule.

THE TEST: a study may not claim a standard version whose requirements it is RATCHETED
AGAINST. The ratchets are the repository's own record of what a study does not yet do, so
this needs no new bookkeeping — it reads what is already written and asks whether the claim
agrees with it.

WHAT IT DELIBERATELY DOES NOT DO: it does not require a study to be at the current version.
Being behind is the ordinary state and [R-STD-01] already reports it. What is forbidden is
claiming a version you are listed as not meeting.
"""
from __future__ import annotations

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")
AUDIT = os.path.join(ENGINE, "build_depth_audit")
for p in (ENGINE, ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

# WHAT EACH VERSION REQUIRES, keyed to the ratchet that records who does not do it. Kept
# here rather than derived from the NOTE's prose because a sentence is not a mapping; the
# entries are added by whoever bumps the version, in the same commit, which is [R-ENF-02]'s
# discipline applied to a claim instead of to a debt.
REQUIREMENTS = {
    "2026.09.01": [("[R-GAP-01] a dated gap review", "gap_outstanding.json")],
    "2026.09.07": [("[R-ASSET-01] an asset-base record", "asset_base_outstanding.json"),
                   ("[R-COC-02] a declared terminal construction", "ke_outstanding.json")],
}


def dig(doc, key):
    if isinstance(doc, dict):
        if isinstance(doc.get(key), str):
            return doc[key]
        for v in doc.values():
            r = dig(v, key)
            if r:
                return r
    elif isinstance(doc, list):
        for v in doc:
            r = dig(v, key)
            if r:
                return r
    return None


def ratcheted(fname):
    p = os.path.join(AUDIT, fname)
    if not os.path.exists(p):
        return None                       # a named ratchet that is gone is not "nobody"
    d = json.load(open(p, encoding="utf-8"))
    out = set()
    for k, v in d.items():
        if k == "pruned_on":
            continue
        if isinstance(v, dict):
            out |= set(v)
        elif isinstance(v, list):
            out |= {x for x in v if isinstance(x, str)}
    return out


def main(argv=None):
    dirs = sorted(glob.glob(os.path.join(ENGINE, "*_study")))
    if not dirs:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    # Every named ratchet must resolve, or this gate is measuring against nothing.
    for _ver, reqs in REQUIREMENTS.items():
        for label, f in reqs:
            if ratcheted(f) is None:
                print("FAIL — %s names ratchet %s, which is not on disk. This gate would "
                      "silently stop testing that requirement [R-ENF-04]." % (label, f))
                return 1

    claims, over, unread = {}, [], []
    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        nf = None
        for n in ("study_numbers.json", "numbers.json"):
            if os.path.exists(os.path.join(d, n)):
                nf = os.path.join(d, n)
                break
        if not nf:
            continue
        try:
            v = dig(json.load(open(nf, encoding="utf-8")), "standard_version")
        except Exception:
            unread.append(tk)
            continue
        if not v:
            continue
        claims[tk] = v
        broken = [label for ver, reqs in REQUIREMENTS.items() if v >= ver
                  for label, f in reqs if tk in (ratcheted(f) or set())]
        if broken:
            over.append((tk, v, broken))

    print("[R-STD-02] a standard version is a claim, not a build timestamp")
    print("  study directories examined : %d" % len(dirs))
    print("  studies carrying a claim   : %d" % len(claims))
    print("  requirements mapped        : %d across %d version(s)"
          % (sum(len(r) for r in REQUIREMENTS.values()), len(REQUIREMENTS)))
    for tk, v in sorted(claims.items()):
        print("     %-13s %s" % (tk, v))

    if not claims:
        print("\nFAIL — read zero standard-version claims across %d study directories. A "
              "reader that stopped finding them reads exactly like a book with none "
              "[R-ENF-04]." % len(dirs))
        return 1

    if unread:
        print("\n  numbers file would not parse: %s" % ", ".join(sorted(unread)))

    if over:
        print("\nFAIL — a study claims a standard whose requirements it is listed as not "
              "meeting:")
        for tk, v, broken in sorted(over):
            print("   %-13s claims %s but is ratcheted against: %s"
                  % (tk, v, "; ".join(broken)))
        print("\n   A stamp taken from the live constant re-asserts this on every rebuild, "
              "with nobody\n   deciding. Freeze the study's claim to a version it meets, or "
              "meet the requirement.")
        return 1

    print("\nOK — no study claims a standard it is listed as not meeting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
