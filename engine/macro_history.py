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
    for field, rec in (o.get("figures") or {}).items():
        if not isinstance(rec, dict):
            raise VintageMissing(
                "%s %d: %s is recorded as a bare value with no source. Four "
                "fields or it does not exist." % (market.upper(), year, field))
        for need in ("value", "source", "date", "tier"):
            if rec.get(need) in (None, ""):
                raise VintageMissing(
                    "%s %d: %s has no %s. Four fields or it does not exist."
                    % (market.upper(), year, field, need))
        if rec["tier"] not in TIERS:
            raise VintageMissing("%s %d: %s carries tier %r, which is not one of %s"
                                 % (market.upper(), year, field, rec["tier"],
                                    ", ".join(sorted(TIERS))))
        vals[field] = float(rec["value"])
        srcs[field] = rec["source"]
        dates[field] = rec["date"]
        tiers[field] = rec["tier"]
    return Vintage(year=int(year), values=vals, sources=srcs, dates=dates, tiers=tiers)


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
    print("\n  An origin is USABLE when all four of %s are sourced. Anything else "
          "is dropped, never filled." % ", ".join(REQUIRED))
    return {"market": market.upper(), "usable": usable, "declared": declared}


if __name__ == "__main__":
    import sys
    report(sys.argv[1] if len(sys.argv) > 1 else "EG")
