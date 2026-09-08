"""[R-ASSET-01] — the operating asset base is as at the latest disclosure the study read.

THE DEFECT THIS CLOSES, IN THE PRINCIPAL'S OWN WORDS: a study that "takes into
consideration current landbank of a developer but does not account for new land added to
the developer landbank".

WHY NO EXISTING GATE SEES IT. [R-BRIDGE-01] requires the enterprise-to-equity bridge to
stand on the LATEST DISCLOSED BALANCE SHEET and check_bridge.py enforces it. Nothing says
the same of the OPERATING ASSET BASE — the land, the fleet, the kilns, the keys, the
installed capacity — which on an asset-based lens is what the value actually rests on. The
rule was written about one statement and the quantity that matters here sits beside it.
Measured 07-09-2026: "landbank", in any of five spellings, occurs in ZERO gate files and
ZERO governing documents; the only occurrence anywhere in the tree is a fixture string
inside a negative control, which is a defect being reproduced rather than a check for it.

WHAT IT COST, on the day it was found: PHDC commits land_bank_sqm_mn = 33.0 dated
2024-12-31 and sourced to the FY2024 earnings release, inside a study edition-dated
2026-09-02 whose information set ends 1Q2026 and whose bridge stands on the 31-March-2026
balance sheet. Every other input in that study is held to a freshness discipline. The land
base is not, and it is printed to the delivered workbook.

THE TEST IS AN ORDERING, NOT A THRESHOLD, and that is deliberate. A cutoff in days would
be a free parameter the PROMOTION RULE forbids, and it would be the wrong shape anyway: an
asset base is restated when the company discloses it, not on a clock. So the test is that
the asset base is as at, or later than, the end of the information set the study itself
claims to have read. A study that read 1Q2026 may not value the company on an FY2024 land
bank without saying so.

THE RELEASE IS REAL AND CANNOT BE GAMED. Companies do not restate every quantity every
quarter, and a study whose asset base is genuinely the latest disclosure of it is correct
however old that disclosure is. So a study may declare `not_restated_since` — but it must
name the LATER DISCLOSURES IT CHECKED and give a REASON, because a declaration with an
empty reason has switched the check off rather than declared it. That is the shape every
release in this repository takes.

A CLASS THAT DOES NOT RESOLVE IS A FAILURE, NEVER A SKIP [R-ENF-04]. The scope is derived
from research_protocol.LENS_REGISTRY — the classes whose lens set contains an asset-based
lens — and never from a list typed here, so a class added to the registry is in scope
without anyone remembering. TMGH was the case that forced this: it commits its class as
"real-estate developer, off-plan — point-in-time on handover" with an em dash where the
registry key carries a comma, so a gate that looked the string up and moved on when it
missed would SILENTLY SKIP A DEVELOPER. That is exactly the failure this project has
registered as L-355 — a reader that guesses a naming convention finds nothing and reports
it as a result — so the class is normalised before lookup and an unresolved class FAILS.
"""
from __future__ import annotations

import re
import unicodedata

# The lenses that value a company on a physical asset base. A class carrying any of these
# is in scope. Read from the registry rather than listed by name, so the scope follows the
# taxonomy instead of drifting from it.
ASSET_BASED_LENSES = ("rnav", "replacement_cost", "ev_per_tonne")

REQUIRED = ("quantity", "unit", "value", "as_at", "disclosure")


class AssetBaseError(Exception):
    pass


def normalise_class(s):
    """Fold the punctuation a class string is written with, never its words.

    An em dash, an en dash and a comma are the same separator to a reader and three
    different strings to a dict lookup. Folding them is safe; folding WORDS would let a
    study opt into a different class by rewording, which is the offence this repo calls
    moving a finding's ring to satisfy a checker.
    """
    if not isinstance(s, str):
        return ""
    t = unicodedata.normalize("NFKD", s)
    t = t.replace("—", ",").replace("–", ",").replace("-", " ")
    t = re.sub(r"[,\s]+", " ", t).strip().lower()
    return t


def in_scope_classes(registry):
    """The registry classes whose lens set contains an asset-based lens."""
    out = {}
    for cls, lenses in registry.items():
        flat = []
        for item in (lenses if isinstance(lenses, (list, tuple)) else [lenses]):
            flat.extend(item if isinstance(item, (list, tuple)) else [item])
        if any(l in ASSET_BASED_LENSES for l in flat):
            out[normalise_class(cls)] = cls
    return out


def period_end(s):
    """Resolve a date or a period label to the calendar date it ENDS on.

    Studies write an information set as '1Q2026', 'H1 2026', 'FY2025' or a plain date;
    all four are ordinary and all four have to compare. An unparseable value RAISES
    rather than returning a default, because a period that silently became 1-Jan would
    make every asset base look fresh.
    """
    if not isinstance(s, str) or not s.strip():
        raise AssetBaseError("empty period")
    t = s.strip().upper().replace("_", " ")
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", t)
    if m:
        return tuple(int(g) for g in m.groups())
    m = re.fullmatch(r"([1-4])Q\s?(\d{4})", t) or re.fullmatch(r"Q([1-4])\s?(\d{4})", t)
    if m:
        q, y = int(m.group(1)), int(m.group(2))
        return (y, q * 3, (31, 30, 30, 31)[q - 1] if q != 1 else 31)
    m = re.fullmatch(r"H([12])\s?(\d{4})", t)
    if m:
        h, y = int(m.group(1)), int(m.group(2))
        return (y, 6 if h == 1 else 12, 30 if h == 1 else 31)
    m = re.fullmatch(r"(?:FY)?\s?(\d{4})", t)
    if m:
        return (int(m.group(1)), 12, 31)
    raise AssetBaseError("unparseable period %r" % s)


def check(record, information_set_ends):
    """Return a list of failure strings. Empty means the record holds.

    Everything here is about the RECORD, never about the number: this gate makes no claim
    that a land bank of 33 million square metres is right or wrong, only that the study
    says when it was true and that the date is not behind the study's own reading.
    """
    fails = []
    if not isinstance(record, dict):
        return ["no asset_base_record committed"]

    for f in REQUIRED:
        if record.get(f) in (None, "", []):
            fails.append("asset_base_record is missing %s" % f)
    if fails:
        return fails

    try:
        base = period_end(str(record["as_at"]))
    except AssetBaseError as e:
        return ["as_at %s" % e]
    try:
        read_to = period_end(str(information_set_ends))
    except AssetBaseError as e:
        return ["information_set_ends %s" % e]

    if base >= read_to:
        return []

    rel = record.get("not_restated_since")
    if not isinstance(rel, dict):
        return ["asset base as at %s is BEHIND the information set ending %s, and the "
                "study declares no not_restated_since"
                % (record["as_at"], information_set_ends)]

    reason = (rel.get("reason") or "").strip()
    checked = rel.get("disclosures_checked") or []
    if not reason:
        fails.append("not_restated_since carries an EMPTY reason — that switches the "
                     "check off rather than declaring it")
    if not isinstance(checked, (list, tuple)) or not checked:
        fails.append("not_restated_since names no later disclosure it actually checked")
    return fails
