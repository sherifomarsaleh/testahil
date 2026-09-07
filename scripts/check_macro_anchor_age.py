"""A STUDY MAY NOT BE STRUCK LONG AFTER THE ANCHOR ITS CURRENCY PATH DERIVES FROM.

Enforced per [R-ENF-01]. The rule it enforces is an extension of [R-MACRO-01] and is
recorded with its arithmetic in engine/method_reassessment/MACRO_ANCHOR_DATE_06-09-2026.md.

WHY THIS EXISTS
    [R-GAP-01 AMENDED] requires every study to be delivered against the LATEST KNOWN price.
    [R-MACRO-01] pins the currency to one house path per market, whose forward path is
    DERIVED by relative purchasing-power parity from a spot ANCHOR carried in the path file
    with its own date. Nothing held those two dates to each other.

    Found by reading PHAR's rebuild ledger — the route rather than the arrival, which is
    what [R-REBUILD-01] exists for. Its fifth lever, worth -25.4% and the largest in that
    ledger, records in its own words that "the house derivation does not admit a leading-year
    anchor for a currency and the study conforms rather than inventing one", with the evidence
    "the tension in the house path's first year is registered, not resolved".

    The tension is not PHAR's. Measured 6 September 2026: engine/macro_paths/EG.json is
    stamped 2026-09-02 and its fx.spot anchor is dated 2026-08-06 — twenty-seven days apart
    INSIDE ONE FILE — while AMOC, ARCC, PHAR and SCEM were struck on 2 and 3 September, 27
    and 28 days after it. Four of the six Egyptian studies that commit a strike date. A study
    obeying both rules runs TWO DATES FOR ONE ECONOMY, which is [L-048]'s own complaint
    quoted in that path's own `derivation` field, arriving where nobody looked.

FLOATING MARKETS ONLY, AND THAT IS THE HALF THAT KEEPS THIS HONEST
    A stale currency anchor on a HARD PEG is the same number today by construction — the
    dirham at 3.6725, the riyals at 3.75 and 3.64. Seven of the eleven studies the census
    flags are pegged, and counting them would overstate this by a factor of three. It is the
    [R-TERM-01 CLAUSE TWO] error exactly: a defect measured on one side of a sign change
    presented as a finding about the sign. So the gate reads the path's own `regime` and
    holds only transition and mature markets to the bound.

THE BOUND IS BORROWED, NOT MINTED
    [R-COC-01] already refuses a sovereign quote older than 14 days, allows it to be accepted
    deliberately, and requires the staleness to be DISCLOSED in the record. This reuses that
    shape and that number rather than inventing a second cutoff for a second input, because a
    threshold chosen here would be the free parameter the PROMOTION RULE forbids and the
    honest justification for a number is that the house already uses it for the same job.

    A study past the bound is NOT simply refused: it may declare `anchor_staleness_accepted`
    with a REASON, exactly as a stale sovereign quote may be. An empty reason has switched
    the check off rather than declared it, and fails.

Population-anchored [R-ENF-04] BOTH ways: every listed ticker must resolve on disk, and a run
that read ZERO strike dates across present study directories fails rather than reporting clean.
Ratcheted [R-ENF-02]; the list may only ever get SHORTER (--prune).

    python3 scripts/check_macro_anchor_age.py
    python3 scripts/check_macro_anchor_age.py --prune
"""
import datetime as dt
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING_FILE = os.path.join(ENGINE, "build_depth_audit", "anchor_age_outstanding.json")

# BORROWED FROM [R-COC-01], NOT CHOSEN HERE.
MAX_AGE_DAYS = 14
PEGGED = "pegged"
CURRENCY_MARKET = {"EGP": "EG", "AED": "AE", "SAR": "SA", "QAR": "QA",
                   "INR": "IN", "KRW": "KR", "USD": "US"}


def _date(x):
    try:
        return dt.date.fromisoformat(str(x)[:10])
    except Exception:                                                   # noqa: BLE001
        return None


def paths(engine=ENGINE):
    out = {}
    for p in sorted(glob.glob(os.path.join(engine, "macro_paths", "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:                                               # noqa: BLE001
            continue
        fx = (d.get("fx") or {}).get("spot") or {}
        out[d.get("market") or os.path.basename(p)[:-5]] = dict(
            regime=d.get("regime"), fx_date=_date(fx.get("date")))
    return out


def studies(engine=ENGINE):
    """(ticker, strike date, market, declared currency, acceptance record)."""
    out = []
    for dd in sorted(glob.glob(os.path.join(engine, "*_study"))):
        tk = os.path.basename(dd)[:-6].upper()
        p = os.path.join(dd, "study_numbers.json")
        if not os.path.exists(p):
            out.append((tk, None, None, None, None))
            continue
        try:
            n = json.load(open(p, encoding="utf-8"))
        except Exception:                                               # noqa: BLE001
            out.append((tk, None, None, None, None))
            continue
        meta = n.get("meta") or {}
        sd = _date(meta.get("spot_date")
                   or ((n.get("inputs") or {}).get("spot") or {}).get("date"))
        # A CURRENCY THIS GATE GUESSED IS NOT A CURRENCY THE STUDY DECLARED. An earlier
        # draft of the census inferred the market by searching the file for "EGP" and swept
        # in an AED study and a SAR one, because both quote an Egyptian figure somewhere.
        cur = str(meta.get("currency") or n.get("currency") or "").upper() or None
        acc = ((n.get("macro_record") or {}).get("anchor_staleness_accepted")
               or n.get("anchor_staleness_accepted"))
        out.append((tk, sd, CURRENCY_MARKET.get(cur), cur, acc))
    return out


def evaluate(engine=ENGINE):
    """(breaches, read_count) — a breach is (ticker, market, days, reason)."""
    P, breaches, read = paths(engine), [], 0
    for tk, sd, mkt, cur, acc in studies(engine):
        if not (sd and mkt):
            continue
        rec = P.get(mkt)
        if not (rec and rec["fx_date"]):
            continue
        read += 1
        if rec["regime"] == PEGGED:
            continue                       # the anchor IS the peg
        age = (sd - rec["fx_date"]).days
        if age <= MAX_AGE_DAYS:
            continue
        if isinstance(acc, dict) and str(acc.get("reason") or "").strip():
            continue                       # deliberately accepted AND disclosed
        why = ("declares acceptance with no reason — an empty reason switches the check off"
               if acc is not None else
               "struck %d days after the %s currency anchor it derives from" % (age, mkt))
        breaches.append((tk, mkt, age, why))
    return breaches, read


def main(argv=()):
    engine = ENGINE
    for a in argv:
        if a.startswith("--engine="):
            engine = a.split("=", 1)[1]
    listed = {}
    if os.path.exists(OUTSTANDING_FILE):
        listed = (json.load(open(OUTSTANDING_FILE, encoding="utf-8")) or {}).get(
            "outstanding", {})

    dirs = sorted(os.path.basename(d)[:-6].upper()
                  for d in glob.glob(os.path.join(engine, "*_study")))
    if not dirs:
        print("REFUSED — examined ZERO study directories. An empty population is not a "
              "clean one [R-ENF-04].")
        return 1
    ghosts = sorted(set(listed) - set(dirs))
    if ghosts:
        print("REFUSED — the ratchet names %d study(ies) that do not resolve on disk: %s"
              % (len(ghosts), ", ".join(ghosts)))
        return 1

    breaches, read = evaluate(engine)
    if read == 0:
        print("REFUSED — %d study directories are present and NOT ONE paired a strike date "
              "with a currency anchor. A run that read nothing is not a run that found "
              "nothing [R-ENF-04]." % len(dirs))
        return 1

    if "--prune" in argv:
        keep = {t: listed[t] for t, _, _, _ in breaches if t in listed}
        json.dump({"why": "[R-MACRO-01] extension with the ratchet of [R-ENF-02]. The list "
                          "may only ever get SHORTER.",
                   "bound_days": MAX_AGE_DAYS, "outstanding": keep},
                  open(OUTSTANDING_FILE, "w", encoding="utf-8"), indent=1)
        print("pruned — %d of %d entries kept" % (len(keep), len(listed)))
        return 0

    new = [b for b in breaches if b[0] not in listed]
    print("CURRENCY ANCHOR AGE — floating markets held to the %d-day bound [R-COC-01]'s\n"
          "  %d studies paired a strike date with an anchor; %d breach, %d of them NEW"
          % (MAX_AGE_DAYS, read, len(breaches), len(new)))
    for tk, mkt, age, why in sorted(breaches, key=lambda b: -b[2]):
        print("   %-6s %-13s %-4s %s" % ("NEW" if tk not in listed else "listed",
                                         tk, mkt, why))
    if new:
        print("\nFAIL — %d study(ies) struck past the bound with no accepted, reasoned "
              "declaration." % len(new))
        return 1
    print("\nOK — no study newly breaches the bound.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
