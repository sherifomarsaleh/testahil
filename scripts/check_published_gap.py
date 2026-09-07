#!/usr/bin/env python3
"""[R-GAP-03] — the gap A READER SEES is audited, not only the gap the study was struck at.

WHY THIS IS NOT check_valuation_gap AGAIN, and the protocol says so in its own words:

    "the gap a READER sees and the gap the gate reports are two different numbers, each
     honest about a different thing, and refreshing a spot moves the reader's and not
     the gate's."

[R-GAP-01] audits a STUDY against the price it was STRUCK at — the right question for
whether an answer was audited before it shipped, and deliberately kept that way. It reads
each study's own committed numbers, so its subject is the 22 names that commit an answer.

THE SITE PUBLISHES NINETY. assets/data.js carries fair{bear,base,full} and a spot for every
one of them, and a reader divides one by the other without knowing or caring whether a
study directory exists. MEASURED 07-09-2026 through a real JavaScript load: all 90 gaps are
computable, and 58 OF THEM EXCEED TEN PER CENT EITHER WAY. Twenty-two are audited. The
other thirty-six are not, because the gates that audit an answer take a study directory as
their subject and those names have none — so a published fair value of 2.39 against a spot
of 9.12 is examined by nothing at all.

THE PROTOCOL ALREADY NAMED THIS HOLE AND GAVE IT NO INSTRUMENT, saying it "closes when the
campaign publishes the book together". That is a plan, not a check: it cannot go red, it
cannot shorten, and nothing would notice if it grew. A number in a status note is a number
that rots [R-DOC-02].

WHAT IT CHECKS
    1. every published name's gap is computable from data.js — an unreadable answer is not
       a clean answer [R-ENF-04]
    2. a gap beyond the trigger owes a GAP_REVIEW auditing the CURRENTLY PUBLISHED central
       and the CURRENT gap, on [R-GAP-01 AMENDED]'s own markers
    3. the population is the site, and a run reading zero names FAILS

THE TRIGGER IS BORROWED, NEVER MINTED: ten per cent either way, [R-GAP-01]'s own audit
trigger, and the five-point staleness tolerance on an audited gap is [R-GAP-01 AMENDED]'s.
Inventing a second cutoff for the same question would be the free parameter the PROMOTION
RULE forbids and would let the two gates disagree about what a large gap is.

IT IMPORTS [R-GAP-01]'S OWN READERS rather than re-implementing them [R-ENF-03]: a checker
that models another checker's parser is checking a different file from the one that ships.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")
for p in (HERE, ENGINE, ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

import check_valuation_gap as vg             # noqa: E402  [R-ENF-03]
import ratchet_shape as rshape              # noqa: E402  [R-ENF-08]

DATA_JS = os.path.join(ROOT, "assets", "data.js")
RATCHET = os.path.join(ENGINE, "build_depth_audit", "published_gap_outstanding.json")

TRIGGER = vg.TRIGGER if hasattr(vg, "TRIGGER") else 0.10
GAP_STALE = 0.05          # [R-GAP-01 AMENDED]: half the trigger, borrowed not minted


def published_book():
    """Every name the site publishes, through a real JavaScript load [R-ENF-03]."""
    prog = (
        "const fs=require('fs');const s=fs.readFileSync(%r,'utf8');"
        "eval(s.replace(/^\\s*(const|let|var)\\s+/gm,'globalThis.'));"
        "const T=globalThis.TICKERS||{};const out={};"
        "for(const [n,t] of Object.entries(T)){"
        "  out[n]={fair:(t.fair||null), spot:(t.spot==null?null:t.spot),"
        "          spotDate:(t.spotDate||null), code:(t.code||'')};}"
        "console.log(JSON.stringify(out));" % DATA_JS)
    r = subprocess.run(["node", "-e", prog], capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or not (r.stdout or "").strip():
        raise RuntimeError("could not load assets/data.js: %s"
                           % ((r.stderr or "")[:300]))
    return json.loads(r.stdout)


def study_dir(ticker):
    d = os.path.join(ENGINE, "%s_study" % ticker.lower())
    return d if os.path.isdir(d) else None


def load_ratchet():
    if not os.path.exists(RATCHET):
        return {"outstanding": {}, "pruned_on": []}
    return json.load(open(RATCHET, encoding="utf-8"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune", action="store_true")
    ap.add_argument("--list", action="store_true",
                    help="print every breaching name and its gap, audited or not")
    a = ap.parse_args(argv)

    try:
        book = published_book()
    except Exception as e:
        print("FAIL — %s" % e)
        return 1
    if not book:
        print("FAIL — read zero published names from assets/data.js [R-ENF-04]. A gate "
              "reporting a clean book having examined nothing is the failure this rule "
              "exists to prevent.")
        return 1

    rat = load_ratchet()
    known = rat.get("outstanding") or {}
    if isinstance(known, list):
        known = {k: "" for k in known}

    unreadable, breaching, audited, fresh, listed = [], [], [], [], []

    for tk in sorted(book):
        rec = book[tk]
        fair, spot = rec.get("fair") or {}, rec.get("spot")
        base = fair.get("base") if isinstance(fair, dict) else None
        if not isinstance(base, (int, float)) or not isinstance(spot, (int, float)) \
                or spot <= 0:
            unreadable.append(tk)
            continue
        gap = base / spot - 1.0
        if abs(gap) <= TRIGGER:
            continue
        breaching.append((tk, gap, base, spot))

        sdir = study_dir(tk)
        if not sdir:
            why = "no study directory, so nothing can carry a review"
            worse, note = rshape.worsened(known.get(tk), gap, GAP_STALE)
            if tk in known and not worse:
                listed.append((tk, gap, why))
            else:
                fresh.append((tk, gap, why if not worse else "%s — %s" % (why, note)))
            continue
        name, covered, ac, acs, ag = vg.read_review(sdir)
        if not name:
            why = "study directory but no GAP_REVIEW"
        elif ac is None:
            why = "review %s states no audited central" % name
        elif not any(abs(v - base) <= max(0.005, abs(base) * 0.002) for v in (acs or [ac])):
            why = ("review %s audits %s; the site publishes %s"
                   % (name, ac, base))
        elif ag is None:
            why = "review %s states no audited gap" % name
        elif abs(ag - gap) > GAP_STALE:
            why = ("review %s audited a gap of %+.1f%%; the site now shows %+.1f%%"
                   % (name, ag * 100, gap * 100))
        else:
            audited.append(tk)
            continue
        worse, note = rshape.worsened(known.get(tk), gap, GAP_STALE)
        if tk in known and not worse:
            listed.append((tk, gap, why))
        else:
            fresh.append((tk, gap, why if not worse else "%s — %s" % (why, note)))

    print("[R-GAP-03] the gap a READER sees, audited")
    print("  published names read        : %d" % len(book))
    print("  unreadable answers          : %d%s"
          % (len(unreadable), ("  " + ", ".join(unreadable)) if unreadable else ""))
    print("  beyond %.0f%% either way      : %d" % (TRIGGER * 100, len(breaching)))
    print("  of those, audited currently : %d" % len(audited))
    print("  outstanding (allowed)       : %d" % len(listed))

    if a.list:
        print("\n  every breaching name, worst first:")
        for tk, gap, base, spot in sorted(breaching, key=lambda r: r[1]):
            mark = "audited" if tk in audited else ("listed" if tk in known else "NEW")
            print("     %-12s %+7.1f%%   fair %-10s spot %-10s %s"
                  % (tk, gap * 100, base, spot, mark))

    rc = 0
    if unreadable:
        # An unreadable answer is not a clean one, and it is not this gate's job to
        # decide it is harmless: a name the site publishes and nobody can read is
        # exactly the state that reads as clean.
        rc = 1
        print("\nFAIL — %d published name(s) expose no readable fair value and spot."
              % len(unreadable))

    if fresh:
        rc = 1
        print("\nFAIL — NEW breach with no current audit, not on the ratchet:")
        for tk, gap, why in sorted(fresh, key=lambda r: r[1]):
            print("   %-12s %+7.1f%%   %s" % (tk, gap * 100, why))

    if listed:
        print("\nstill outstanding, allowed for now (%d):" % len(listed))
        for tk, gap, why in sorted(listed, key=lambda r: r[1])[:12]:
            print("   %-12s %+7.1f%%   %s" % (tk, gap * 100, why))
        if len(listed) > 12:
            print("   ... and %d more; --list prints them all" % (len(listed) - 12))

    ghosts = sorted(set(known) - set(book))
    if ghosts:
        rc = 1
        print("\nFAIL — ratchet names studies the site does not publish [R-ENF-04]: %s"
              % ", ".join(ghosts))

    now_clean = sorted(set(known) - {t for t, _, _ in listed})
    now_clean = [t for t in now_clean if t in book]
    if now_clean:
        print("\n%d listed name(s) no longer breach or are now audited: %s"
              % (len(now_clean), ", ".join(now_clean)))
        if a.prune:
            for tk in now_clean:
                known.pop(tk, None)
            rat["outstanding"] = known
            rat.setdefault("pruned_on", []).append({"removed": now_clean})
            json.dump(rat, open(RATCHET, "w", encoding="utf-8"), indent=1,
                      ensure_ascii=False)
            print("   ratchet rewritten — the list may only ever SHORTEN.")

    print("\n%s" % ("FAIL" if rc else "OK — no new unaudited breach."))
    return rc


if __name__ == "__main__":
    sys.exit(main())
