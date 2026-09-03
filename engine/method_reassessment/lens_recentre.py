"""What the book's centrals would be if the class primary WERE the central.

[R-LENS-03] retired the typed multi-lens blend on 02-09-2026: one class primary IS
the central, the other lenses are cross-checks published beside it. The evidence
that prompted it was one name — PHDC, whose cash-flow lens landed within 2.2% of
the market while its 45/15/20/20 blend landed 28% below, because three of its four
lenses value a developer on reported earnings and historical-cost book.

ONE NAME IS NOT A PATTERN. This measures the same thing across every study that
commits its per-lens values, and asks the question the reassessment is actually
about: DID THE BLEND PULL THE HOUSE'S CENTRALS DOWN, and by how much?

WHAT IT IS AND IS NOT. It is a measurement over committed numbers, not a
re-valuation: it reads each study's own lens block and its own spot, and takes the
class primary's BASE read as the central the rule now requires. It does not
re-derive a lens, re-run a model, or move a delivered number — every study that
needs its central changed needs a re-issue, and this only says how large that
change is and which way it runs.

THE PRIMARY IS NOT GUESSED. LENS_REGISTRY names one primary per class — ddm for a
bank, sotp for a holding company, dcf for everything else — and this resolves in
that order over the lenses a study actually commits. A study whose block carries
no primary is REPORTED AS UNREADABLE rather than skipped: an unreadable answer is
not a clean answer [R-ENF-04].
"""
from __future__ import annotations

import glob
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
sys.path.insert(0, ENGINE)

# In LENS_REGISTRY's own order of primaries.
PRIMARY_ORDER = ("ddm", "sotp", "dcf")


def _num(x):
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x)
    return None


def _base(entry):
    """The base read of one lens, whatever shape the study wrote it in."""
    if isinstance(entry, dict):
        for k in ("base", "central", "value", "mid"):
            v = _num(entry.get(k))
            if v is not None:
                return v
        return None
    return _num(entry)


PRIMARY_WORDS = {"ddm": ("ddm", "dividend discount"),
                 "sotp": ("sotp", "sum of the parts", "sum-of-the-parts", "nav"),
                 "dcf": ("dcf", "discounted cash flow", "cash flow", "cash-flow")}


def _match(name, loose=False):
    """Which class primary a key or lens name denotes, if any.

    SUBSTRING MATCHING IS ONLY SAFE ON SOMETHING LENS-SHAPED. PHAR's numbers file
    carries `w_dcf = 0.5` — the DCF's WEIGHT — beside its lens lists, and a
    substring rule read that 0.5 as a fair value of EGP 0.50 against a spot of
    130.05, producing a tidy, plausible-looking -99.6% that was pure nonsense.
    So a bare number must match a primary word EXACTLY, and the loose match is
    allowed only where the entry itself carries a bear/base/bull shape or a name.
    """
    low = str(name).lower().strip()
    if "alt" in low or "diagnostic" in low or "retired" in low:
        # an ALTERNATIVE reading of the primary is not the primary
        return None
    for kind in PRIMARY_ORDER:
        for w in PRIMARY_WORDS[kind]:
            if low == w or low == w.replace(" ", "_"):
                return kind
            if loose and (low.startswith(w + " ") or low.startswith(w + "_")
                          or (" " + w) in low or low.startswith(w)):
                return kind
    return None


def _lens_shaped(e):
    """A dict carrying a base (or bear/bull) read — the shape a lens is written in."""
    return isinstance(e, dict) and any(k in e for k in ("base", "bear", "bull",
                                                        "central", "value"))


def primary_of(d):
    """(kind, value, where) of the class primary, or (None, None, reason).

    FIVE SHAPES, because the studies genuinely wrote five. The order is not
    arbitrary: the [R-LENS-03] lens RECORD is asked first because it is the
    artefact the rule is about and the one a gate already validates; a heuristic
    over a lens block is a reconstruction and is used only where there is no
    record to read. That is the same order the reverse read uses for a
    discounting convention, and for the same reason.
    """
    lr = d.get("lens_record") or {}
    prim = lr.get("primary") or {}
    v = _num(prim.get("value"))
    if v is not None:
        return (prim.get("kind") or "primary"), v, "lens_record"
    # A PRIMARY PUBLISHED AS A RANGE IS NOT A MISSING PRIMARY. TMGH's record
    # carries a low and a high and says in its own words that the four cases
    # behind them are never averaged into a headline; reporting that as "no class
    # primary" reads like a defect where the construction is deliberate, and
    # [R-LENS-03] positively permits an envelope of present-value reads. The
    # difference matters because this measurement is about a BLEND, and a study
    # that refuses to collapse its own cases has no blend to measure.
    rng = prim.get("range") or {}
    if _num(rng.get("low")) is not None and _num(rng.get("high")) is not None:
        return None, None, ("the primary is published as a range (%.2f-%.2f) and "
                            "the study says its cases are never averaged"
                            % (_num(rng["low"]), _num(rng["high"])))

    lenses = d.get("lenses")
    if isinstance(lenses, dict):
        named = lenses.get("primary")
        vals = lenses.get("values")
        if isinstance(named, str) and isinstance(vals, dict) and named in vals:
            v = _num(vals[named])
            if v is not None:
                return (_match(named) or "primary"), v, "lenses.primary"
        for k in lenses:
            kind = _match(k, loose=_lens_shaped(lenses[k]))
            if kind:
                v = _base(lenses[k])
                if v is not None:
                    return kind, v, "lenses[%s]" % k
        # A study that frames its primary TWO WAYS has two primaries, and picking
        # one here would make the choice it deliberately published both sides of.
        if any(str(k).lower().startswith("items_") for k in lenses):
            return None, None, ("the primary is published in two framings and this "
                                "measurement will not pick one")
        return None, None, "no class primary in the committed lens block"

    if isinstance(lenses, list):
        # [name, bear, base, bull, weight] — PHDC's shape.
        for row in lenses:
            if isinstance(row, (list, tuple)) and len(row) >= 3:
                kind = _match(row[0], loose=True)
                if kind:
                    v = _num(row[2])
                    if v is not None:
                        return kind, v, "lenses[] row %r" % str(row[0])[:28]
        return None, None, "no class primary among the committed lens rows"

    return None, None, "no committed lens block"


def floored(d, kind_value):
    """True where the primary's BASE equals its own BEAR — a floored read.

    Not a threshold and not a judgement: it is a structural fact about the
    study's own numbers. ELEC's cash-flow lens carries bear 0.01 and base 0.01
    against a spot of 2.19, which is a floor rather than a central, and letting
    one such cell into a pooled mean would let a floor decide the book's answer.
    It is REPORTED, never dropped silently.
    """
    lenses = d.get("lenses")
    if not isinstance(lenses, dict):
        return False
    for k, e in lenses.items():
        if _match(k) and isinstance(e, dict):
            b, base = _num(e.get("bear")), _num(e.get("base"))
            if b is not None and base is not None and abs(b - base) < 1e-12:
                return True
    return False


def spot_of(d):
    v = _num(d.get("spot"))
    if v is not None:
        return v
    return _num((d.get("meta") or {}).get("spot"))


def central_of(d):
    v = _num(d.get("central"))
    if v is not None:
        return v
    v = _num((d.get("meta") or {}).get("central"))
    if v is not None:
        return v
    # ELEC writes its blended central INSIDE the lens block, beside the lenses it
    # blends. Reading only the top level reported it as having no central at all.
    lenses = d.get("lenses")
    if isinstance(lenses, dict):
        return _base(lenses.get("central"))
    return None


def rows():
    out = []
    for sd in sorted(glob.glob(os.path.join(ENGINE, "*_study"))):
        tk = os.path.basename(sd).replace("_study", "").upper()
        p = os.path.join(sd, "study_numbers.json")
        if not os.path.exists(p):
            out.append({"ticker": tk, "unreadable": "no committed numbers file"})
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            out.append({"ticker": tk, "unreadable": "numbers file will not parse: %s" % e})
            continue
        kind, prim, where = primary_of(d)
        central, spot = central_of(d), spot_of(d)
        if prim is None:
            out.append({"ticker": tk, "unreadable": where})
            continue
        if spot is None:
            out.append({"ticker": tk,
                        "unreadable": "no spot in the committed numbers"})
            continue
        row = {"ticker": tk, "primary_lens": kind, "primary": prim,
               "primary_from": where, "central": central, "spot": spot,
               "floored": floored(d, prim),
               "primary_vs_spot": prim / spot - 1.0}
        if central is not None:
            row["central_vs_spot"] = central / spot - 1.0
            row["blend_cost"] = row["central_vs_spot"] - row["primary_vs_spot"]
        out.append(row)
    return out


def report():
    rs = rows()
    if not rs:
        raise SystemExit("REFUSED: no studies were examined [R-ENF-04].")
    good = [r for r in rs if "unreadable" not in r and "blend_cost" in r
            and not r.get("floored")]
    floors = [r for r in rs if r.get("floored")]
    print("what the centrals would be if the class primary WERE the central\n")
    print("  a measurement over committed numbers. No delivered number moves here;")
    print("  a study whose central would change needs a re-issue, and this says")
    print("  how large that change is and which way it runs.\n")
    print("  %-12s %-10s %10s %10s %9s %9s %9s"
          % ("ticker", "primary", "primary", "central", "spot", "prim/spot", "cent/spot"))
    print("  " + "-" * 76)
    for r in sorted(rs, key=lambda x: x["ticker"]):
        if "unreadable" in r:
            print("  %-12s %s" % (r["ticker"], r["unreadable"]))
            continue
        c = r.get("central")
        print("  %-12s %-10s %10.2f %10s %9.2f %8.1f%% %8s"
              % (r["ticker"], r["primary_lens"][:10], r["primary"],
                 ("%10.2f" % c) if c is not None else "         —",
                 r["spot"], 100 * r["primary_vs_spot"],
                 ("%.1f%%" % (100 * r["central_vs_spot"]))
                 if "central_vs_spot" in r else "—"))
    if not good:
        print("\n  no study commits both a class primary and a central — nothing to "
              "compare, and that is the finding rather than a clean result.")
        return rs
    costs = [r["blend_cost"] for r in good]
    below = [r for r in good if r["blend_cost"] < 0]
    print("\n  on the %d studies committing BOTH a class primary and a central:" % len(good))
    print("    the central sits BELOW the primary on %d of %d" % (len(below), len(good)))
    print("    median difference  %+.1f pp of spot" % (100 * statistics.median(costs)))
    print("    mean   difference  %+.1f pp of spot" % (100 * statistics.mean(costs)))
    print("    range              %+.1f pp to %+.1f pp"
          % (100 * min(costs), 100 * max(costs)))
    # A STUDY WHOSE CENTRAL ALREADY IS ITS PRIMARY CONTRIBUTES A ZERO, AND A ZERO
    # IS NOT EVIDENCE ABOUT A BLEND. Three of the eleven were migrated by hand in
    # WS3/WS8, so their difference is zero by construction; leaving them in drags
    # the median toward nothing and makes the blend look harmless. Both figures
    # are printed rather than one being chosen.
    blended = [r for r in good if abs(r["blend_cost"]) > 1e-9]
    if blended:
        bc = [r["blend_cost"] for r in blended]
        down = [r for r in blended if r["blend_cost"] < 0]
        print("\n  on the %d that actually carry a blend (the other %d already have"
              % (len(blended), len(good) - len(blended)))
        print("  the primary as their central, so their difference is zero by")
        print("  construction and is not evidence either way):")
        print("    the central sits BELOW the primary on %d of %d"
              % (len(down), len(blended)))
        print("    median %+.1f pp · mean %+.1f pp · range %+.1f to %+.1f pp"
              % (100 * statistics.median(bc), 100 * statistics.mean(bc),
                 100 * min(bc), 100 * max(bc)))
        worst = sorted(blended, key=lambda r: r["blend_cost"])[:3]
        print("    furthest down: %s"
              % ", ".join("%s %+.1f pp" % (r["ticker"], 100 * r["blend_cost"])
                          for r in worst))
        up = sorted(blended, key=lambda r: -r["blend_cost"])[:2]
        print("    and the other way: %s"
              % ", ".join("%s %+.1f pp" % (r["ticker"], 100 * r["blend_cost"])
                          for r in up))

    if floors:
        print("\n  excluded from the pooled figures, and reported rather than "
              "dropped: %s" % ", ".join(r["ticker"] for r in floors))
        print("    the primary's base EQUALS its own bear — a floored read, not a")
        print("    central, and one floor should not decide the book's answer.")
    print("\n  A NEGATIVE number means the published central sits BELOW the class")
    print("  primary — the blend pulling the answer down. That is the direction")
    print("  [R-LENS-03] was adopted on, measured on one name; this is the book.")
    return rs


if __name__ == "__main__":
    report()
