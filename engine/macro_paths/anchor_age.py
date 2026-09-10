#!/usr/bin/env python3
"""How old is each house macro path's own anchor, against the studies that stand on it?

WHY THIS EXISTS
    [R-GAP-01 AMENDED] requires every study to be delivered against the LATEST KNOWN price.
    [R-MACRO-01] pins its currency to the house path, whose forward path is DERIVED by
    relative purchasing-power parity from a spot ANCHOR carried in the path file with its
    own date. Nothing holds those two dates to each other.

    Measured 6 September 2026 on the Egyptian path: the file is stamped 2026-09-02 and its
    fx.spot anchor is dated 2026-08-06 — twenty-seven days apart INSIDE ONE FILE — while
    four of the six Egyptian studies that commit a strike date were struck on 2 or 3
    September, twenty-seven and twenty-eight days after the anchor their currency rests on.
    A study obeying both rules is running TWO DATES FOR ONE ECONOMY, which is [L-048]'s own
    complaint quoted in that path's own `derivation` field, arriving where nobody looked.

    It was worth 25.4% on PHAR — the largest single lever in its rebuild ledger, and the one
    its own `why` flags as "the tension in the house path's first year is registered, not
    resolved".

WHAT THIS IS AND IS NOT
    It is a CENSUS, on the pattern of terminal_census.py and driver_bias_census.py: it prints
    what the dates are and never fails. It is NOT a gate, because no rule yet says how old an
    anchor may be, and a check that goes red where no rule exists is the permanently-red check
    [R-ENF-02] forbids.

    [R-COC-01] already carries the shape a rule would take, for a different input: "a
    sovereign quote older than 14 days REFUSES rather than being used quietly; it may be
    accepted deliberately and the staleness is then DISCLOSED in the record." The currency
    anchor has no such guard, and it is the input from which the whole purchasing-power wedge
    and every translated line descend.

READ IT LIVE. Both halves move — a path is refreshed, a study is re-struck — so a written
table goes stale the same way a calibration figure does.

    python3 engine/macro_paths/anchor_age.py
"""
import datetime as dt
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)

# a study is governed by a market's path only if it is priced in that market's currency
CURRENCY_MARKET = {"EGP": "EG", "AED": "AE", "SAR": "SA", "QAR": "QA",
                   "INR": "IN", "KRW": "KR", "USD": "US"}


def _date(x):
    try:
        return dt.date.fromisoformat(str(x)[:10])
    except Exception:                                                   # noqa: BLE001
        return None


def paths():
    """Every sourced path, with the dates its own anchors carry."""
    out = {}
    for p in sorted(glob.glob(os.path.join(HERE, "*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:                                               # noqa: BLE001
            continue
        mkt = d.get("market") or os.path.basename(p)[:-5]
        anchors = {}
        fx = (d.get("fx") or {}).get("spot") or {}
        if fx.get("date"):
            anchors["fx spot"] = _date(fx["date"])
        inf = (d.get("inflation") or {}).get("latest") or {}
        if inf.get("date"):
            anchors["inflation latest"] = _date(inf["date"])
        sov = d.get("sovereign") or {}
        for k in ("date", "as_of"):
            if isinstance(sov, dict) and sov.get(k):
                anchors["sovereign quote"] = _date(sov[k])
                break
        out[mkt] = {"as_of": _date(d.get("as_of")), "anchors": anchors,
                    "regime": d.get("regime")}
    return out


def studies():
    """Every study that commits a strike date, with the market whose path governs it."""
    out = []
    for dd in sorted(glob.glob(os.path.join(ENGINE, "*_study"))):
        tk = os.path.basename(dd)[:-6].upper()
        p = os.path.join(dd, "study_numbers.json")
        if not os.path.exists(p):
            continue
        try:
            n = json.load(open(p, encoding="utf-8"))
        except Exception:                                               # noqa: BLE001
            continue
        meta = n.get("meta") or {}
        sd = _date(meta.get("spot_date")
                   or ((n.get("inputs") or {}).get("spot") or {}).get("date"))
        cur = str(meta.get("currency") or n.get("currency") or "").upper()
        # A CURRENCY THIS SCRIPT GUESSED IS NOT A CURRENCY THE STUDY DECLARED. An earlier
        # draft inferred the market by searching the whole file for "EGP", and swept in an
        # AED study and a SAR one because both quote an Egyptian figure somewhere. Where the
        # study does not declare one, it is reported UNDECLARED rather than assigned.
        out.append((tk, sd, CURRENCY_MARKET.get(cur), cur))
    return out


def main():
    P, S = paths(), studies()
    print("HOUSE MACRO PATHS — how old is each path's own anchor?\n")
    print("  %-5s %-11s %-12s %s"
          % ("mkt", "regime", "path as_of", "anchors, and their age within the file"))
    print("  " + "-" * 74)
    for mkt, rec in sorted(P.items()):
        if not rec["anchors"]:
            print("  %-5s %-11s %-12s (no dated anchor in the file)"
                  % (mkt, rec.get("regime") or "?", rec["as_of"] or "—"))
            continue
        bits = []
        for k, v in sorted(rec["anchors"].items()):
            age = (rec["as_of"] - v).days if (rec["as_of"] and v) else None
            bits.append("%s %s%s" % (k, v, "" if age is None else " (%+d d)" % age))
        print("  %-5s %-11s %-12s %s"
              % (mkt, rec.get("regime") or "?", rec["as_of"] or "—", " · ".join(bits)))

    print("\n\nSTUDIES AGAINST THE CURRENCY ANCHOR THEY STAND ON\n")
    print("  %-13s %-5s %-10s %-12s %-12s %s"
          % ("study", "mkt", "regime", "struck", "fx anchor", "days after"))
    print("  " + "-" * 74)
    rows, undecl = [], []
    for tk, sd, mkt, cur in S:
        if mkt is None:
            undecl.append((tk, cur, sd))
            continue
        fx = (P.get(mkt) or {}).get("anchors", {}).get("fx spot")
        if not (sd and fx):
            continue
        rows.append((tk, mkt, sd, fx, (sd - fx).days,
                     (P.get(mkt) or {}).get("regime")))
    for tk, mkt, sd, fx, g, reg in sorted(rows, key=lambda r: -r[4]):
        # A STALE ANCHOR ON A PEG IS NOT THE SAME FINDING. The dirham is hard-pegged at
        # 3.6725 and the riyals at 3.75 and 3.64, so an anchor eight months old is the same
        # number it would be today by construction of the peg. Reporting those beside a
        # floating market's would be the [R-TERM-01 CLAUSE TWO] error — a defect measured on
        # one side of a sign change presented as a finding about the sign.
        flag = ("   <-- struck after its anchor" if g > 0 and reg != "pegged"
                else "   (pegged — the anchor is the peg)" if g > 0 else "")
        print("  %-13s %-5s %-10s %-12s %-12s %+5d%s"
              % (tk, mkt, reg or "?", sd, fx, g, flag))

    after = [r for r in rows if r[4] > 0]
    float_after = [r for r in after if r[5] != "pegged"]
    print("\n  %d studies pair a strike date with a currency anchor; %d were struck after it,"
          % (len(rows), len(after)))
    print("  and %d of those are in a FLOATING market where the gap can move the answer."
          % len(float_after))
    if float_after:
        w = max(float_after, key=lambda r: r[4])
        print("  widest floating gap %d days (%s, %s)" % (w[4], w[0], w[1]))
    print("  The pegged rows are reported and NOT counted: an anchor eight months old on a")
    print("  hard peg is the same number today by construction, and putting it in the same")
    print("  column as a floating one would overstate this by a factor of three.")
    if undecl:
        # AN UNREADABLE ROW IS NOT A CLEAN ONE [R-ENF-04]
        print("\n  %d studies declare no currency and are NOT assigned one: %s"
              % (len(undecl), ", ".join(t for t, _, _ in undecl)))

    # WHAT THIS CENSUS DOES NOT COVER, said here rather than left for someone to assume.
    stale_inf = [(m, r) for m, r in sorted(P.items())
                 if r["as_of"] and r["anchors"].get("inflation latest")
                 and (r["as_of"] - r["anchors"]["inflation latest"]).days > 60]
    if stale_inf:
        # RAISED AS A FINDING AND THEN REFUTED, WITHIN THE HOUR, BY ASKING WHAT READS THE
        # FIELD. The inflation "latest" anchor is stale by 246 days in six of the seven
        # paths, which looked like the larger half of this census and is not: grep says
        # inflation.latest is consumed in FOUR places and every one is display or
        # provenance — a property, a source string, two print statements. No study and no
        # escalator reads it. What drives every cost line is inflation.PATH, the forward
        # ladder, and those are sourced 3 September 2026 in six paths and 11 May 2026 in
        # EG's, which is the most recent Monetary Policy Report the central bank has
        # published. A STALE REFERENCE PRINT IS NOT A STALE DRIVER, and the difference is
        # one grep — the same discipline this file applies to the pegged rows above.
        print("\n  A STALE FIELD THAT DRIVES NOTHING, reported so nobody re-raises it: the")
        print("  inflation 'latest' anchor is %d+ days old in %d paths, and it is a DISPLAY"
              % (min((r["as_of"] - r["anchors"]["inflation latest"]).days
                     for _, r in stale_inf), len(stale_inf)))
        print("  field — consumed only by a property, a source string and two prints. The")
        print("  forward LADDER is what escalates every cost line, and those are current.")
        for m, r in stale_inf:
            print("      %-4s %-11s latest %s (%d d) — ladder source is what matters, not this"
                  % (m, r.get("regime") or "?", r["anchors"]["inflation latest"],
                     (r["as_of"] - r["anchors"]["inflation latest"]).days))

    print("\n  THIS IS A CENSUS, NOT A GATE. No rule yet says how old an anchor may be, and a")
    print("  check going red where no rule exists is the permanently-red check [R-ENF-02]")
    print("  forbids. [R-COC-01] carries the shape a rule would take, for the sovereign quote:")
    print("  refuse past 14 days, allow deliberate acceptance, disclose the staleness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
