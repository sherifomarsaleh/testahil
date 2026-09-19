"""Every price path a study commits says what it does in REAL terms.  [R-REAL-01]

A revenue line that does not move with inflation while the cost lines do manufactures a
margin collapse, and the model then reports the collapse as a finding. Four studies
audited on 18-09-2026 carried it in four costumes, and the sentence describing each one
was reassuring: PHAR's driver note says its price "tracks domestic inflation ... with no
real price gain" over a path that falls 15.9% in real terms.

WHAT THIS GATE DOES NOT DO is decide that a real decline is wrong. Egyptian medicine
prices are set administratively and do lag inflation; a commodity held flat in hard
currency is a declared convention. The gate catches SILENCE: the claim must be stated,
with its measured magnitude and a mechanism from a closed list, and then a human rules.

THE QUANTITY IS CHECKED, NOT THE DECLARATION -- [R-MACRO-01 AMENDED]'s own lesson, learned
when a study declared a perfectly TRUE exemption about a line that was not doing the work
while the input that drove the currency was named nowhere. So a study cannot opt out by
declaring nothing: the register is scanned for price-class paths and an undeclared
material one is red. The scan is a FLOOR under the study's own declaration rather than its
definition, on the delivered-vocabulary precedent, and it matches PRICE tokens only --
never volume, margin or utilisation, because a check that condemns correct work gets
switched off.

MATERIALITY IS REUSED, NEVER MINTED: 5% cumulative, the line this house already draws
round a contested judgement and which [R-ANCHOR-01] already reused for this same question.

Ratcheted [R-ENF-02] with each entry carrying its MEASUREMENT [R-ENF-08]; the list may
only ever SHORTEN, and an entry closes by NAMING the real change -- never by deleting the
figure and never by changing the path, because what is wrong is the claim and not the
construction. Population-anchored [R-ENF-04] BOTH ways: zero study directories fails, and
so does zero INPUTS read across the directories present, because a reader that stopped
finding registers reads exactly like a book with no price paths in it.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))

import real_terms as RT       # noqa: E402

RATCHET = os.path.join(ROOT, "engine", "build_depth_audit", "real_terms_outstanding.json")


_SITE = {}


def _site_markets():
    """Ticker -> market, from the ONE place this protocol says records an exchange.

    "THE EXCHANGE OF A COVERED NAME IS RECORDED IN assets/data.js AS THE code PREFIX" --
    so the market is read from there through a real JavaScript parse [R-ENF-03], never
    guessed from a study's own fields. The first draft searched four plausible keys inside
    each numbers file and returned nothing for FOURTEEN of twenty-four studies, which read
    exactly like a book with no price paths in it. That is [L-355] landing on the
    instrument written to close it, and it was caught by the count rather than by reading.
    """
    if _SITE:
        return _SITE
    import site_data
    tick = site_data.read_object("TICKERS")
    pref = {"EGX": "EG", "ADX": "AE", "DFM": "AE", "TADAWUL": "SA", "QSE": "QA",
            "KRX": "KR", "NSE": "IN", "NASDAQ": "US"}
    for tk, rec in (tick or {}).items():
        code = (rec or {}).get("code") or ""
        if ":" in code:
            m = pref.get(code.split(":", 1)[0].upper())
            if m:
                _SITE[tk.upper()] = m
    return _SITE


def market_of(numbers, tk):
    """The market for this study. The site is the authority; the record is the fallback."""
    try:
        m = _site_markets().get(tk.upper())
        if m:
            return m
    except Exception:
        pass
    for k in ("market", "exchange_market"):
        v = numbers.get(k)
        if isinstance(v, str) and v:
            return v.upper()
    for path in (("beta_record", "market"), ("macro_record", "market"),
                 ("wacc", "beta_record", "market"), ("cost_of_capital_record", "market")):
        cur = numbers
        for p in path:
            cur = cur.get(p) if isinstance(cur, dict) else None
            if cur is None:
                break
        if isinstance(cur, str) and cur:
            return cur.upper()
    return None


def study_dirs():
    import glob
    return sorted(glob.glob(os.path.join(ROOT, "engine", "*_study")))


def main(argv=None):
    argv = argv or sys.argv[1:]
    measure = "--measure" in argv
    dirs = study_dirs()
    if not dirs:
        print("FAIL - zero study directories examined. The population resolver is broken, "
              "not the book. [R-ENF-04]")
        return 1

    ratchet = {}
    if os.path.exists(RATCHET):
        try:
            ratchet = (json.load(open(RATCHET, encoding="utf-8")).get("measurements") or {})
        except Exception as exc:
            print("FAIL - the ratchet will not parse (%s)" % exc)
            return 1

    read_inputs = 0
    breaches, listed, clean, unreadable = [], [], [], []
    for d in dirs:
        tk = os.path.basename(d).replace("_study", "").upper()
        nj = os.path.join(d, "study_numbers.json")
        if not os.path.exists(nj):
            continue
        try:
            numbers = json.load(open(nj, encoding="utf-8"))
        except Exception as exc:
            unreadable.append((tk, "numbers file will not parse: %s" % exc))
            continue
        reg = numbers.get("inputs")
        if not isinstance(reg, dict):
            unreadable.append((tk, "commits no four-field input register"))
            continue
        read_inputs += len(reg)
        mkt = market_of(numbers, tk)
        if mkt is None:
            unreadable.append((tk, "names no market, so no ladder resolves"))
            continue
        try:
            rep, why = RT.assess(numbers, mkt)
        except Exception as exc:
            unreadable.append((tk, "%s: %s" % (mkt, str(exc)[:90])))
            continue
        if rep is None:
            unreadable.append((tk, why))
            continue
        bad = []
        for r in rep["rows"]:
            if r["real_drift"] is None:
                continue
            e = r["entry"]
            if not r["material"]:
                continue
            if r["excluded"] and not (r["entry"] or {}).get("reason", "").strip():
                bad.append("%s is excluded from the block with no reason - an empty "
                           "reason has switched the check off, not declared it" % r["input"])
                continue
            if not e:
                bad.append("%s moves %+.1f%% in REAL terms over its window (%s) and the "
                           "study declares nothing about it"
                           % (r["input"], 100 * r["real_drift"],
                              (r["detail"] or {}).get("basis", "")))
                continue
            stated = e.get("real_change")
            if not isinstance(stated, (int, float)):
                bad.append("%s is declared and states no measured real_change" % r["input"])
            elif abs(float(stated) - r["real_drift"]) > 0.005:
                bad.append("%s states a real change of %+.1f%% and its own path against "
                           "the house ladder gives %+.1f%% - the arithmetic is the arbiter"
                           % (r["input"], 100 * float(stated), 100 * r["real_drift"]))
            m = e.get("mechanism")
            if m not in RT.MECHANISMS:
                bad.append("%s names mechanism %r, which is not on the closed list"
                           % (r["input"], m))
            elif not str(e.get("disclosure") or "").strip():
                bad.append("%s names a mechanism with no disclosure establishing it from "
                           "the filings" % r["input"])
        if bad:
            (listed if tk in ratchet else breaches).append((tk, bad))
        else:
            clean.append((tk, len([r for r in rep["rows"] if r["material"]]),
                          len(rep["rows"])))

    print("[R-REAL-01] price paths declare what they do in REAL terms")
    print("  study directories examined : %d" % len(dirs))
    print("  register inputs read       : %d" % read_inputs)
    print("  studies clean              : %d" % len(clean))
    print("  studies on the ratchet     : %d" % len(listed))
    print("  studies unreadable         : %d" % len(unreadable))
    if read_inputs == 0:
        print("\nFAIL - zero register inputs read across %d directories. A reader that "
              "stopped finding registers reads exactly like a book with no price paths "
              "in it [R-ENF-04]." % len(dirs))
        return 1

    # A STUDY CLEAN BY ABSENCE IS NOT A STUDY CLEAN BY DECLARATION, and printing them
    # alike would hide which is which — twelve studies passed the first run and every one
    # of them passed because the register carries no price-class path at all, which says
    # nothing about the gate and everything about the register.
    none_at_all = [t for t, _m, n in clean if not n]
    for tk, n_mat, n_all in sorted(clean):
        if n_all:
            print("   ok    %-12s %d price path(s), %d material and declared"
                  % (tk, n_all, n_mat))
    if none_at_all:
        print("   none  %-12s carry no price-class path in their register: %s"
              % ("", ", ".join(sorted(none_at_all))))
    for tk, bad in sorted(listed):
        print("   known %-12s %s" % (tk, ratchet.get(tk, "")[:100]))
    for tk, why in sorted(unreadable):
        print("   unread %-11s %s" % (tk, why[:90]))

    stale = sorted(set(ratchet) - {t for t, _ in listed})
    if breaches:
        print()
        for tk, bad in sorted(breaches):
            for b in bad:
                print("  FAIL  %-12s %s" % (tk, b))
        print("\nFAIL - a price path that moves materially in real terms and says so "
              "nowhere. It closes by NAMING the real change, never by deleting the figure "
              "and never by changing the path.")
        return 0 if measure else 1
    if stale:
        print("\nFAIL - listed as outstanding and no longer breaching: %s. A ratchet may "
              "only SHORTEN, so remove the entry in the commit that fixes it [R-ENF-02]."
              % ", ".join(stale))
        return 0 if measure else 1
    print("\nOK - every material real move is declared with its measurement, or is on the "
          "ratchet, which may only ever SHORTEN.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
