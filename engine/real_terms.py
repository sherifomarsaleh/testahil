"""What a price path does in REAL terms, measured against the house inflation ladder.

ADOPTED 18-09-2026 on four studies audited the same night, all four carrying the same
defect in four costumes. A revenue line that does not move with inflation while the cost
lines do manufactures a margin collapse, and the model then reports the collapse as a
finding:

    PHAR   domestic drug price 5.0 / 8.0 / 7.5 / 6.5 / 5.5% against a house ladder of
           16 / 12 / 9 / 7.5 / 7 -- a 15.9% REAL fall over the window, under a driver
           note reading "tracks domestic inflation ... with no real price gain"
    EGCH   export price pinned at US$530 for five years while the pound falls 25%
    AMOC   crude held flat in dollars, costs escalating at full domestic inflation
    ARCC   export dollar price declining 10.5% nominal, sourced by nothing

NONE OF THESE IS NECESSARILY WRONG, and that is the whole shape of this instrument.
Egyptian medicine prices ARE set administratively and do lag inflation; a traded
commodity held flat in hard currency IS a declared convention rather than a slip. What
none of them may do is go UNSAID. A gate can prove a price falls in real terms; it
cannot prove that is a mistake -- so what is caught here is SILENCE, and a human decides
what the silence was hiding.

WHY A NOMINAL PATH CANNOT BE READ. "5% in year one" is unfalsifiable: nobody can tell
whether it means a real gain, a real hold, or an eleven-point real cut, and the reader of
a driver note cannot tell either, which is why PHAR's note survived every review. The
same figure written as "-9.5% real" is read correctly by everybody at a glance. That is
[R-MACRO-01]'s own argument -- growth stored as (real, inflation-path id) and the nominal
RECOMPUTED -- applied to the price lines that rule does not reach, because it binds what a
study DECLARES as an inflation input and a revenue price is not declared as one.

TWO STUDIES IN THIS BOOK ALREADY DO IT THE RIGHT WAY and the pattern is read off them
rather than invented: STC commits `segment_real_growth_path` beside its own
`inflation_ladder`, and SWDY commits `cables_real_growth`. Both name the real rate and let
the nominal follow.

THE COMPARISON DEPENDS ON THE CURRENCY THE PRICE IS SET IN, and getting that wrong would
condemn correct work. A price in local currency is measured against the DOMESTIC ladder. A
price in hard currency is measured against LONG-RUN FOREIGN inflation -- because the house
currency path is derived by purchasing-power parity from the inflation differential, so a
dollar price held flat translates into local currency growing at roughly the differential,
and the real squeeze it causes locally is about the FOREIGN rate rather than the domestic
one. Measuring a dollar price against a 16% domestic ladder would report a 14-point real
collapse where the model suffers about two.

MATERIALITY IS REUSED, NEVER MINTED: 5% is the line this house already applies to a
contested judgement and which [R-ANCHOR-01] already reused for exactly this kind of
question. A cumulative real change beyond it over the explicit window must be named.
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import macro_path as MP       # noqa: E402

# The line this house already draws round a material judgement. Reused rather than minted.
MATERIAL = 0.05

# CLOSED, for [R-COC-01 AMENDED]'s reason: an open list lets any study opt out by
# inventing a mechanism, and "the path looked right" is not one. Adding to it is a rule
# amendment, which is the point -- each of these names a fact about the world that can be
# checked against a filing, not a preference about the model.
MECHANISMS = (
    "administered_price",                       # a regulator sets it and adjusts in steps
    "traded_commodity_flat_in_hard_currency",   # the declared no-forecast convention
    "contractual_escalator",                    # a contract fixes the path
    "regulated_tariff_glide",                   # a published tariff schedule
    "competitive_erosion_measured_in_own_history",   # measured, not asserted
)

# FIVE KINDS, and the split is between SHAPE (a rate or a level) and BASIS (the
# currency the price is set in). The first draft carried four and compared a dollar
# GROWTH RATE against the domestic ladder, which reported a 35.5% real collapse on a path
# running +1% a year in dollars -- condemning correct work on an instrument built to stop
# exactly that. A rate needs its currency named as much as a level does.
KINDS = ("nominal_rate", "nominal_rate_hard_currency", "real_rate",
         "level_local", "level_hard_currency")

# A FLOOR ON THE CANDIDATE SET, NOT ITS DEFINITION. The study's own declaration is what
# says which inputs are price-class; this catches the obvious omissions, exactly as the
# delivered-vocabulary check is a floor under each study's own scrub. A word list cannot
# be complete and is not asked to be -- what it must not do is sweep in work that is
# right, so it matches PRICE tokens only and never volume, margin or utilisation.
PRICE_TOKEN = re.compile(
    r"(?:^|[._])(?:price|prices|asp|tariff|arpu|realis|realiz|"
    r"per_pack|per_t\b|per_tonne|per_unit|usd_t|egp_t|ppp|day_rate|charter_rate)",
    re.I)


class RealTermsError(ValueError):
    pass


def ladder(market: str):
    """The house domestic inflation ladder. A market with no sourced path RAISES."""
    return list(MP.load(market).inflation_path)


def foreign_inflation(market: str):
    """The long-run foreign rate a hard-currency price is held against."""
    v = getattr(MP.load(market), "us_inflation_lt", None)
    if v is None:
        raise RealTermsError("this market's path carries no long-run foreign inflation, "
                             "so a hard-currency price has nothing to be measured against")
    return float(v)


def _cum(rates):
    f = 1.0
    for r in rates:
        f *= 1.0 + float(r)
    return f


def real_drift(values, kind: str, market: str):
    """Cumulative REAL change of a path over its own window.

    Returns (drift, detail) or (None, reason). Positive is a real gain.
    """
    if kind not in KINDS:
        return None, "kind %r is not one of %s" % (kind, ", ".join(KINDS))
    vals = [float(x) for x in values if isinstance(x, (int, float))]
    if len(vals) != len(values) or len(vals) < 2:
        return None, "a path needs at least two numeric years"

    if kind == "real_rate":
        # Real by construction: the drift IS the path, compounded. Nothing to compare it
        # against, and the gate's job on this kind is to check the nominal was COMPUTED.
        return _cum(vals) - 1.0, {"basis": "the path is already real", "years": len(vals)}

    if kind == "nominal_rate_hard_currency":
        n = len(vals)
        f = foreign_inflation(market)
        nom, pi = _cum(vals), (1.0 + f) ** n
        return nom / pi - 1.0, {"basis": "hard-currency growth against long-run foreign "
                                         "inflation", "nominal_factor": nom,
                                "foreign_rate": f, "inflation_factor": pi, "years": n}

    infl = ladder(market)
    if kind == "nominal_rate":
        n = len(vals)
        if n > len(infl):
            return None, ("the path runs %d years and this market's ladder publishes %d; "
                          "extending the ladder here would invent it" % (n, len(infl)))
        nom, pi = _cum(vals), _cum(infl[:n])
        return nom / pi - 1.0, {"basis": "nominal growth against the domestic ladder",
                                "nominal_factor": nom, "inflation_factor": pi,
                                "years": n}
    # LEVELS: the path's own growth from its first year to its last, over n-1 years.
    n = len(vals) - 1
    if vals[0] == 0:
        return None, "the path opens at zero, so its own growth is undefined"
    grew = vals[-1] / vals[0]
    if kind == "level_local":
        if n > len(infl):
            return None, ("the path spans %d years of growth and the ladder publishes %d"
                          % (n, len(infl)))
        pi = _cum(infl[:n])
        return grew / pi - 1.0, {"basis": "a local-currency level against the domestic "
                                          "ladder", "level_factor": grew,
                                 "inflation_factor": pi, "years": n}
    f = foreign_inflation(market)
    pi = (1.0 + f) ** n
    return grew / pi - 1.0, {"basis": "a hard-currency level against long-run foreign "
                                      "inflation", "level_factor": grew,
                             "foreign_rate": f, "inflation_factor": pi, "years": n}


def candidates(numbers: dict):
    """Inputs whose NAME marks them a price and whose value is a numeric path.

    Read off the four-field input register, which is the one artefact every study in this
    book commits and the only place all of these paths actually live -- the builders keep
    some and the numbers file keeps others, and a reader taught one location finds a
    fraction [L-355].
    """
    reg = numbers.get("inputs")
    if not isinstance(reg, dict):
        return None, "this study commits no four-field input register to read"
    out = {}
    for name, rec in reg.items():
        if not isinstance(rec, dict):
            continue
        v = rec.get("value")
        if not (isinstance(v, list) and 2 <= len(v) <= 12
                and all(isinstance(x, (int, float)) for x in v)):
            continue
        if PRICE_TOKEN.search(name):
            out[name] = v
    return out, None


def infer_kind(name: str, values):
    """A REPORTING aid, never the gate's authority.

    The study declares the kind. This is what the report prints beside an UNDECLARED
    candidate so a reader can see what it probably is without the gate deciding — and it
    is deliberately conservative: a path of small numbers is a rate, a path of large ones
    a level, and a dollar level only where the NAME says the currency, because guessing a
    currency is how a check condemns correct work.
    """
    hard = bool(re.search(r"usd|\$|dollar|_fx\b", name, re.I))
    if all(abs(float(x)) < 1.0 for x in values):
        return "nominal_rate_hard_currency" if hard else "nominal_rate"
    return "level_hard_currency" if hard else "level_local"


def nominal_from_real(real_rates, market: str):
    """The INPUT side: give a real path, get the nominal one the model should run.

    This is the half that makes the defect unwritable rather than merely detectable. A
    study calling this cannot type a nominal rate at all — it states what it believes in
    real terms and the house ladder supplies the rest, so "5% nominal" becomes "-9.5%
    real" on the page, which nobody writes by accident.
    """
    infl = ladder(market)
    if len(real_rates) > len(infl):
        raise RealTermsError("a %d-year path against a %d-year ladder would extend it"
                             % (len(real_rates), len(infl)))
    return [(1.0 + float(r)) * (1.0 + infl[i]) - 1.0 for i, r in enumerate(real_rates)]


def assess(numbers: dict, market: str):
    """Every price-class path in a study, with its real drift and whether it is declared."""
    cands, why = candidates(numbers)
    if cands is None:
        return None, why
    block = numbers.get("real_terms_block")
    declared = {}
    if isinstance(block, dict):
        declared = {k: v for k, v in (block.get("paths") or {}).items()}
    excluded = set((block or {}).get("not_price_class") or {}) if isinstance(block, dict) else set()
    rows = []
    for name, vals in sorted(cands.items()):
        d = declared.get(name)
        kind = (d or {}).get("kind") or infer_kind(name, vals)
        drift, detail = real_drift(vals, kind, market)
        rows.append({"input": name, "values": vals, "kind": kind, "declared": bool(d),
                     "excluded": name in excluded, "real_drift": drift,
                     "detail": detail, "entry": d,
                     "material": (drift is not None and abs(drift) >= MATERIAL)})
    return {"rows": rows, "block_present": isinstance(block, dict),
            "declared_count": len(declared), "excluded_count": len(excluded)}, None
