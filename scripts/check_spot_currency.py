#!/usr/bin/env python3
"""[R-GAP-01] THE PRICE A STUDY IS STRUCK AT IS THE LATEST ONE, AND IT CARRIES ITS DATE.

WHY THIS EXISTS. [R-GAP-01 AMENDED] has said since 03-Sep-2026 that no study is
delivered against a stale price, and since 08-09-2026 that the study is struck against
THE LATEST COMMITTED SUPPLIED PRICE, "with its date stated and its age disclosed". Two
halves, and NOTHING WAS CHECKING EITHER. What existed was check_valuation_gap, which
reads each study's OWN committed spot and audits the gap against it — the right
question for whether a study was audited before it shipped, and a question that is
satisfied just as happily by a price four weeks old as by today's.

MEASURED ON THE BOOK 08-09-2026, BEFORE A LINE OF THIS GATE EXISTED: of 24 study
directories, TWELVE commit no spot date of any kind, ONE is struck on a price a month
stale, and SIX of the undated twelve also carry a price that is not the latest
supplied — between 0.4% and 7.2% away from it. Half the book could not say when its
comparison was taken.

THE TWO CHECKS ARE SEPARATE AND BOTH BIND, because they fail differently and are
repaired differently:

  (1) THE DATE. A price with no date is a comparison a reader cannot use and a claim
      nobody can age. It is also the cheaper half: where the price already matches the
      latest supplied figure, adding its date moves no number and is a record fix.

  (2) THE PRICE. A study struck on a superseded quote is audited against its own past.
      Repairing it is a RE-STRIKE, which moves the gap and can move a gap review out of
      its own tolerance, so it is a study act rather than a record fix — which is why
      the two are reported apart rather than as one count.

WHAT IT DELIBERATELY DOES NOT DO. It does not require the date to equal the supplied
file's date: a study may legitimately be struck on an earlier session and say so, and
the AGE is what [R-GAP-01] asks to be disclosed rather than abolished. What it refuses
is a date that is ABSENT, a date that is not a date, and a price that is not the latest
one this repository holds for that name.

THE PRICES ARE READ LIVE from engine/prices/ through gap_today.latest_price_per_ticker(),
never from a figure in this file — the merge is on each price's own date, so a file
naming one name adds it without dropping the rest.

    python3 scripts/check_spot_currency.py            report
    python3 scripts/check_spot_currency.py --prune    shorten the ratchet
"""
import argparse, datetime, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
sys.path.insert(0, ENGINE)
sys.path.insert(0, os.path.join(ENGINE, "prices"))

import gap_today as GT                                       # noqa: E402
import ratchet_shape as rshape                               # noqa: E402  [R-ENF-08]

RATCHET = os.path.join(ENGINE, "build_depth_audit", "spot_currency_outstanding.json")

# Several spellings, because the book already uses several and a reader that guesses one
# silently finds nothing [L-355]. PHDC writes its date as prose ("close 3 Sep 2026"),
# which is a DATE a human can read and a machine cannot age, so it is accepted only if a
# date can actually be parsed out of it.
DATE_KEYS = ("spot_date", "spotDate", "spot_as_of", "spot_asof", "price_date")
SPOT_KEYS = ("spot",)

# The site publishes FERTIGLB; the study directory is FERTIGLOBE. An alias is NAMED here
# and asserted to resolve, never inferred, because a resolver that guesses reports a
# clean book when it has simply failed to look [L-355].
TICKER_ALIAS = {"FERTIGLOBE": "FERTIGLB"}

_ISO = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")
_MONTHS = {m.lower(): i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
_PROSE = re.compile(r"(\d{1,2})\s+([A-Za-z]{3,9})\s+(20\d\d)")


def parse_date(v):
    """A date, or None. Prose is accepted where a date can be READ out of it."""
    if not isinstance(v, str):
        return None
    m = _ISO.search(v)
    if m:
        try:
            return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = _PROSE.search(v)
    if m:
        mon = _MONTHS.get(m.group(2)[:3].lower())
        if mon:
            try:
                return datetime.date(int(m.group(3)), mon, int(m.group(1)))
            except ValueError:
                return None
    return None


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


def numbers_file(sdir):
    for name in ("study_numbers.json", "numbers.json"):
        p = os.path.join(sdir, name)
        if os.path.exists(p):
            return p
    c = [p for p in glob.glob(os.path.join(sdir, "*.json"))
         if "numbers" in os.path.basename(p).lower()]
    return c[0] if c else None


def load_ratchet():
    if not os.path.exists(RATCHET):
        return {"why": "", "outstanding": {}, "pruned_on": []}
    return json.load(open(RATCHET, encoding="utf-8"))


def audit(sdir, latest):
    """(state, message) for one study. An unreadable study is NOT a clean one."""
    tk = os.path.basename(sdir)[:-len("_study")].upper()
    nf = numbers_file(sdir)
    if not nf:
        return tk, "unreadable", "no committed numbers file"
    try:
        doc = json.load(open(nf, encoding="utf-8"))
    except Exception as e:                                          # noqa: BLE001
        return tk, "unreadable", "%s will not parse: %s" % (os.path.basename(nf), e)

    spot = dig(doc, SPOT_KEYS)
    raw_date = dig(doc, DATE_KEYS)
    day = parse_date(raw_date)
    L = latest.get(TICKER_ALIAS.get(tk, tk)) or latest.get(tk) or {}
    lp, ld = L.get("price"), L.get("date")

    if spot is None:
        return tk, "unreadable", "commits no spot at all"
    if lp is None:
        # A name this repository holds no supplied price for cannot be held to one. It
        # is reported rather than skipped, because "no price on file" and "price checked
        # and current" must never read the same [R-ENF-04].
        return tk, "no_supplied_price", ("commits %s but no supplied price is held for "
                                         "this name, so currency cannot be tested" % spot)
    if day is None:
        return tk, "no_date", ("commits a spot of %s and NO READABLE DATE (%r). The "
                               "latest supplied price is %s of %s."
                               % (spot, raw_date, lp, ld))
    if abs(float(spot) - float(lp)) > 1e-9:
        return tk, "stale_price", ("struck at %s (%s) against a latest supplied %s of "
                                   "%s — %+.1f%% away, so this study is audited against "
                                   "its own past"
                                   % (spot, day.isoformat(), lp, ld,
                                      100 * (float(spot) / float(lp) - 1)))
    return tk, "ok", "%s as at %s, the latest supplied price" % (spot, day.isoformat())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune", action="store_true",
                    help="rewrite the ratchet with the studies that now conform removed")
    a = ap.parse_args(argv)

    # THE ALIASES ARE ASSERTED, NOT TRUSTED.
    latest = GT.latest_price_per_ticker()
    if not latest:
        print("FAIL — read ZERO supplied prices. A price file that stopped being read "
              "looks exactly like a book with no prices in it [R-ENF-04].")
        return 1
    for src, dst in TICKER_ALIAS.items():
        if dst not in latest:
            print("FAIL — the alias %s -> %s resolves to no supplied price. An alias "
                  "that does not resolve is a reader guessing." % (src, dst))
            return 1

    dirs = sorted(glob.glob(os.path.join(ENGINE, "*_study")))
    if not dirs:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    rat = load_ratchet()
    known = rat.get("outstanding") or {}
    if isinstance(known, list):
        known = {k: "" for k in known}

    results, fresh, listed, now_ok = [], [], [], []
    for sd in dirs:
        tk, state, msg = audit(sd, latest)
        results.append((tk, state, msg))
        if state == "ok" or state == "no_supplied_price":
            if tk in known:
                now_ok.append(tk)
            continue
        entry = known.get(tk)
        if entry is None:
            fresh.append((tk, state, msg))
        elif rshape.excused(entry, msg):
            listed.append((tk, state, msg))
        else:
            fresh.append((tk, state, msg + "   [on the ratchet for a DIFFERENT failure: %s]"
                          % rshape.signature_of(entry)))

    print("[R-GAP-01] the struck price is the latest one, and it carries its date")
    print("  study directories examined : %d" % len(dirs))
    print("  supplied prices read       : %d" % len(latest))
    print("  conforming                 : %d" % sum(1 for _, s, _ in results if s == "ok"))
    print("  outstanding (allowed)      : %d" % len(listed))
    print()
    for tk, state, msg in sorted(results):
        if state == "ok":
            print("   %-12s %s" % (tk, msg))
    if listed:
        print()
        print("still outstanding, allowed for now (%d):" % len(listed))
        for tk, state, msg in sorted(listed):
            print("   %-12s [%s] %s" % (tk, state, msg))
    if now_ok:
        print()
        print("%d listed stud(ies) now conform and may be pruned: %s"
              % (len(now_ok), ", ".join(sorted(now_ok))))
    if a.prune:
        for tk in now_ok:
            known.pop(tk, None)
        rat["outstanding"] = known
        rat.setdefault("pruned_on", []).append({"removed": sorted(now_ok)})
        json.dump(rat, open(RATCHET, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("pruned — now %d entries" % len(known))
        return 0
    if fresh:
        print()
        print("FAIL — %d new violation(s):" % len(fresh))
        for tk, state, msg in sorted(fresh):
            print("   %-12s [%s] %s" % (tk, state, msg))
        print()
        print("A price with no date is a comparison a reader cannot age; a price that is "
              "not the latest is a study audited against its own past.")
        return 1
    print()
    print("OK — every study states the date of the price it was struck at, and every "
          "price is the latest this repository holds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
