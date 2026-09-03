"""Point-in-time macro vintages — what was KNOWN at each historical origin.

WHY THIS IS A SEPARATE THING FROM `macro_path.py`. That module holds ONE dated
forward path per market: what the house believes today about the future. This
one holds what the house COULD have believed at each past year-end — the
sovereign yield actually quoted that month, the CPI print actually published, the
policy rate actually in force, the equity risk premium actually available in that
year's vintage. The valuation calibration [R-VCAL-01] rebuilds a fair value at
each origin and grades it, and a rebuild that reaches for today's numbers is not
a rebuild at all; it is the answer, wearing a date.

THE ONE RULE THIS MODULE ENFORCES, AND IT REFUSES RATHER THAN WARNS:

    A VINTAGE IS SOURCED OR IT DOES NOT EXIST.

Every figure carries a value, the institution that published it, the date it was
published or observed, and a tier. There is no interpolation between years, no
carrying a neighbouring year forward, and no "approximately". Where a vintage
cannot be sourced, `origin()` RAISES and the calibration drops that origin and
shortens its window — which the pre-registration fixes in advance, precisely so
that a thin archive shows up as fewer origins rather than as a fuller-looking
record built on filled-in cells. A fabricated input corrupts the very error it is
scored on, and unlike most defects it does so invisibly: the arithmetic still
reconciles.

TWO KINDS OF FIGURE, AND POINT-IN-TIME MEANS A DIFFERENT THING FOR EACH. This
distinction is the whole reason the archive can be built at all, and getting it
wrong in either direction is expensive:

  OBSERVED — a market close, an administered rate, an auction result. The number
  is FIXED AT ITS DATE. The overnight deposit rate in force on 31-Dec-2016 is the
  same number whether you read it that evening or ten years later, because no
  institution revises it. For these, point-in-time is satisfied by the OBSERVATION
  DATE, and today's database is a legitimate route to it.

  ESTIMATED — a price index, a national-accounts aggregate, a computed risk
  premium. The number is a MEASUREMENT THAT GETS REVISED, and it is rebased,
  re-weighted and restated for years afterwards. Egypt's 2013 CPI as reported
  today is not the figure any analyst had in 2013. For these, point-in-time
  requires the VINTAGE — the publication that existed at the origin — and this
  module REFUSES an estimated figure that does not name one.

A figure recorded in the wrong class is the quietest failure available here: it is
right in value, wrong in date, and nothing downstream can see it. So the class is
required on every figure, the vintage is required on every estimated one, and a
figure whose publication date falls AFTER its origin must say in its own record
why a study struck at that origin could legitimately have had it.

STATUS. The archive is assembled origin by origin and is DELIBERATELY INCOMPLETE
until each year's four figures have been read from their own source. `report()`
prints exactly which origins are usable and which are not, and the calibration
reads that rather than assuming a span. An origin appears here only when someone
has read its numbers off a document.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE_DIR = os.path.join(HERE, "macro_history")

# The four figures an origin needs before a fair value can be rebuilt on it.
# Fixed here rather than inferred from whatever a file happens to carry, so that
# a partially-filled year cannot pass by being quiet about what it lacks.
REQUIRED = ("sovereign_10y", "cpi_annual", "policy_rate", "erp")

# A fifth is required only where the model has a foreign-currency leg; it is
# checked when asked for, never silently defaulted.
OPTIONAL = ("fx_usd", "default_spread")

TIERS = {"Country", "Global", "Market", "House"}

# See the module docstring. The class is required on every figure because the two
# demand different evidence, and a figure filed in the wrong one is right in value
# and wrong in date, which is invisible afterwards.
REVISION_CLASSES = {"observed", "estimated"}

# Deliberately NOT a grace period in days. A cutoff would be a free parameter with
# no evidence behind it, which the promotion rule forbids; what is required
# instead is that a figure published after its own origin SAYS why a study struck
# at that origin could have had it. Damodaran's 1-January vintage, computed on data
# through the preceding 31 December, is the ordinary case and states exactly that.
LAG_NOTE_FIELD = "publication_lag_note"


class VintageMissing(KeyError):
    """Raised when an origin is asked for and cannot be served from sources.

    Deliberately an exception rather than a None: a caller that forgets to check
    a return value gets a stack trace, not a silently wrong fair value.
    """


@dataclass
class Vintage:
    year: int
    values: Dict[str, float]
    sources: Dict[str, str]
    dates: Dict[str, str]
    tiers: Dict[str, str]
    classes: Dict[str, str]
    vintages: Dict[str, str]
    extras: Dict[str, dict]

    def require(self, *fields) -> Dict[str, float]:
        missing = [f for f in (fields or REQUIRED) if f not in self.values]
        if missing:
            raise VintageMissing(
                "%d: %s not sourced. This origin is DROPPED rather than filled — "
                "an interpolated vintage corrupts the very error it would be "
                "scored on, and it does so invisibly."
                % (self.year, ", ".join(missing)))
        return {f: self.values[f] for f in (fields or REQUIRED)}


def _path(market: str) -> str:
    return os.path.join(ARCHIVE_DIR, "%s.json" % market.upper())


def load(market: str) -> dict:
    p = _path(market)
    if not os.path.exists(p):
        raise VintageMissing(
            "no macro history for %s. The valuation calibration cannot rebuild a "
            "fair value at a past origin without knowing what was published at "
            "it, and this module will not invent one. Assemble "
            "engine/macro_history/%s.json first." % (market.upper(), market.upper()))
    return json.load(open(p, encoding="utf-8"))


def _entry(blob, year):
    for o in blob.get("origins", []):
        if int(o.get("year", -1)) == int(year):
            return o
    return None


def origin(market: str, year: int) -> Vintage:
    """The vintage for one year-end, or RAISE.

    Never returns a partial vintage and never falls back to a neighbouring year:
    the whole point of a point-in-time archive is that the absence of a number is
    itself information about which origins the calibration may use.
    """
    blob = load(market)
    o = _entry(blob, year)
    if o is None:
        raise VintageMissing(
            "%s has no origin for %d. Origins are added when their figures have "
            "been read from a source, never when they are needed."
            % (market.upper(), year))
    vals, srcs, dates, tiers = {}, {}, {}, {}
    classes, vintages, extras = {}, {}, {}
    yearend = "%d-12-31" % int(year)
    for field, rec in (o.get("figures") or {}).items():
        if not isinstance(rec, dict):
            raise VintageMissing(
                "%s %d: %s is recorded as a bare value with no source. Four "
                "fields or it does not exist." % (market.upper(), year, field))
        for need in ("value", "source", "date", "tier", "revision_class"):
            if rec.get(need) in (None, ""):
                raise VintageMissing(
                    "%s %d: %s has no %s. Four fields plus its revision class, or "
                    "it does not exist." % (market.upper(), year, field, need))
        if rec["tier"] not in TIERS:
            raise VintageMissing("%s %d: %s carries tier %r, which is not one of %s"
                                 % (market.upper(), year, field, rec["tier"],
                                    ", ".join(sorted(TIERS))))
        rc = rec["revision_class"]
        if rc not in REVISION_CLASSES:
            raise VintageMissing(
                "%s %d: %s carries revision_class %r, which is not one of %s. The "
                "class decides what evidence the figure needs, so it cannot be "
                "left to the reader."
                % (market.upper(), year, field, rc, ", ".join(sorted(REVISION_CLASSES))))
        if rc == "estimated" and not rec.get("vintage"):
            raise VintageMissing(
                "%s %d: %s is an ESTIMATED figure with no vintage named. A price "
                "index or a computed premium is revised and rebased for years "
                "afterwards, so the number reported today is not the number the "
                "origin had. Name the publication that existed at the origin, or "
                "the figure does not exist here: right in value and wrong in date "
                "is the one error nothing downstream can see."
                % (market.upper(), year, field))
        # The as-of date may never sit after the origin it is filed under. This is
        # the plainest form of the whole rule and it is checked rather than trusted.
        if str(rec["date"]) > yearend:
            raise VintageMissing(
                "%s %d: %s is dated %s, which is AFTER the origin it is filed "
                "under. An origin sees only what the world had produced by its own "
                "year-end." % (market.upper(), year, field, rec["date"]))
        pub = rec.get("published")
        if pub and str(pub) > yearend and not rec.get(LAG_NOTE_FIELD):
            raise VintageMissing(
                "%s %d: %s was published %s, after this origin's year-end, and the "
                "record does not say why a study struck at that origin could have "
                "had it. There is no grace period here on purpose — a cutoff in "
                "days would be a free parameter nobody measured — so the record "
                "carries the reason instead."
                % (market.upper(), year, field, pub))
        vals[field] = float(rec["value"])
        srcs[field] = rec["source"]
        dates[field] = rec["date"]
        tiers[field] = rec["tier"]
        classes[field] = rc
        vintages[field] = rec.get("vintage", "")
        extras[field] = {k: v for k, v in rec.items()
                         if k not in ("value", "source", "date", "tier",
                                      "revision_class", "vintage")}
    return Vintage(year=int(year), values=vals, sources=srcs, dates=dates,
                   tiers=tiers, classes=classes, vintages=vintages, extras=extras)


def usable_origins(market: str, fields=REQUIRED) -> List[int]:
    """The origins the calibration may actually use — measured, never assumed."""
    try:
        blob = load(market)
    except VintageMissing:
        return []
    out = []
    for o in blob.get("origins", []):
        try:
            origin(market, int(o["year"])).require(*fields)
            out.append(int(o["year"]))
        except VintageMissing:
            continue
    return sorted(out)


def report(market: str = "EG") -> dict:
    """Print what is sourced and what is not. The calibration reads THIS rather
    than assuming a span, so a thin archive shows up as fewer origins."""
    try:
        blob = load(market)
    except VintageMissing as exc:
        print("%s: %s" % (market.upper(), exc))
        return {"market": market.upper(), "usable": [], "declared": []}
    declared = sorted(int(o["year"]) for o in blob.get("origins", []))
    usable = usable_origins(market)
    print("macro history — %s" % market.upper())
    print("  declared origins : %s" % (", ".join(map(str, declared)) or "none"))
    print("  USABLE origins   : %s" % (", ".join(map(str, usable)) or "none"))
    if declared and len(usable) < len(declared):
        print("  incomplete       : %s"
              % ", ".join(str(y) for y in declared if y not in usable))
    for y in declared:
        if y in usable:
            continue
        try:
            origin(market, y).require()
        except VintageMissing as exc:
            print("     %d — %s" % (y, str(exc)[:150]))
    print("  target span      : %s" % blob.get("target_span", "not stated"))

    # Per-FIELD coverage, because "eleven origins, none usable" does not say what
    # would unlock them and the whole point of the report is to be actionable.
    # A field held by every origin but one is a very different problem from a
    # field nobody has, and the two look identical in an origin-by-origin list.
    print("\n  coverage by field (of %d declared origins):" % len(declared))
    for f in REQUIRED:
        have = []
        for y in declared:
            try:
                origin(market, y).require(f)
                have.append(y)
            except VintageMissing:
                pass
        gap = [y for y in declared if y not in have]
        print("     %-16s %2d/%2d%s" % (f, len(have), len(declared),
              ("   missing: " + ", ".join(map(str, gap))) if gap else "   complete"))
    # A FIGURE NOBODY COULD CHECK IS NOT THE SAME EVIDENCE AS ONE THAT WAS
    # CHECKED, and a report that prints only "usable" hides the difference.
    # Every origin leaning on an uncorroborated figure is named here, so a pooled
    # result built on them cannot be read without seeing what it rests on.
    uncorr = {}
    for o in blob.get("origins", []):
        for f in (o.get("uncorroborated_figures") or []):
            uncorr.setdefault(f, []).append(int(o["year"]))
    if uncorr:
        print("\n  UNCORROBORATED — recorded, and no second source exists here:")
        for f, yrs in sorted(uncorr.items()):
            print("     %-16s %d origin(s): %s"
                  % (f, len(yrs), ", ".join(map(str, yrs))))
        print("     These are usable and they are NOT equal evidence. A calibration")
        print("     that leans on them says so, or excludes them and shortens.")

    compromised = [int(o["year"]) for o in blob.get("origins", [])
                   if o.get("point_in_time_compromised")]
    if compromised:
        print("\n  point-in-time COMPROMISED (usable only with the caveat read): %s"
              % ", ".join(map(str, compromised)))
    uns = blob.get("unsourced") or {}
    if uns.get("fields"):
        print("  unsourced by record: %s" % ", ".join(uns["fields"]))
    print("\n  An origin is USABLE when all four of %s are sourced. Anything else "
          "is dropped, never filled." % ", ".join(REQUIRED))
    return {"market": market.upper(), "usable": usable, "declared": declared,
            "compromised": compromised, "uncorroborated": uncorr}


if __name__ == "__main__":
    import sys
    report(sys.argv[1] if len(sys.argv) > 1 else "EG")
