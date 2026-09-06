"""Every study's committed central against the LATEST KNOWN price, computed now.

WHY THIS IS NOT scripts/check_valuation_gap.py. That gate audits a study against
the price it was STRUCK at, which is the right question for the study: it asks
whether the answer was audited before it shipped. This asks the other question,
and [R-GAP-01] is written on it — *"where the central sits more than 10% below the
LATEST KNOWN price"*. A study struck a month ago is not retroactively in breach,
but the gap it now carries is a fact about the book, and the price is the only
instrument in the room that measures it.

THE PRICES ARE READ FROM THE MOST RECENT SUPPLIED FILE, never typed here, and the
file records who supplied it and when. A figure that arrives in a conversation
binds nothing: the container is rebuilt from the repository and a session that
cannot see it will ask for it again [R-IND-01].

WHAT IT REFUSES. A study whose numbers expose no central is REPORTED as unreadable
rather than skipped — an unreadable answer is not a clean answer — and a name with
no supplied price is named too, rather than dropped silently. A run that read zero
studies raises [R-ENF-04].
"""
from __future__ import annotations

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)

# The ledger and the price file do not always spell a name the same way. Named
# rather than fuzzy-matched: a wrong pairing is a plausible number against the
# wrong company, which is the failure mode this whole file exists to catch.
ALIAS = {"FERTIGLOBE": "FERTIGLB"}

TRIGGER = 0.10          # [R-GAP-01], both sides since 02-09-2026


def _supplied_files():
    files = glob.glob(os.path.join(HERE, "SUPPLIED_*.json"))
    if not files:
        raise SystemExit("REFUSED: no supplied price file under engine/prices/. An "
                         "empty population is not a clean result [R-ENF-04].")
    return files


def latest_price_per_ticker():
    """The freshest price held for each name, merged across EVERY supplied file.

    PRICES ARRIVE BY HAND, SO THEY ARRIVE WITH LAGS AND GAPS, and one file is not
    the state of the book: a name priced on Tuesday and absent from Thursday's
    file is still priced on Tuesday, and reading only the newest file would drop
    it. Each entry therefore carries the DATE OF THE PRICE ITSELF and the file it
    came from, so a reader is told how old the number is rather than being left
    to assume it is today's.

    Returns {ticker: {"price": float, "date": "YYYY-MM-DD", "file": str}}.
    """
    out = {}
    for f in sorted(_supplied_files()):
        d = json.load(open(f, encoding="utf-8"))
        base = os.path.basename(f)
        for tk, row in (d.get("prices") or {}).items():
            px, when = row.get("price"), row.get("date") or d.get("supplied")
            if px is None or not when:
                continue
            prev = out.get(tk)
            if prev is None or when > prev["date"]:
                out[tk] = {"price": float(px), "date": when, "file": base}
    return out


def latest_prices():
    """Back-compatible view: the merged map, plus the newest file's provenance."""
    files = sorted(_supplied_files())
    d = json.load(open(files[-1], encoding="utf-8"))
    merged = latest_price_per_ticker()
    return ({tk: {"price": v["price"], "date": v["date"]} for tk, v in merged.items()},
            os.path.basename(files[-1]), d.get("supplied"))


def _num(x):
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, dict):
        for k in ("base", "central", "value", "mid"):
            v = x.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return float(v)
    return None


def read_study(sdir):
    """(central, spot_at_strike, note)."""
    p = os.path.join(sdir, "study_numbers.json")
    if not os.path.exists(p):
        return None, None, "no committed numbers file"
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return None, None, "numbers file will not parse: %s" % e
    m = d.get("meta") or {}
    c = _num(d.get("central"))
    if c is None:
        c = _num(m.get("central"))
    note = None
    if c is None:
        ts = d.get("central_two_sided") or {}
        br = ts.get("branches") or []
        if br:
            c = _num(br[0])
            note = ("two-sided: this is the first branch, %s"
                    % str(br[0].get("label"))[:60])
    spot = _num(d.get("spot")) or _num(m.get("spot"))
    if c is None:
        return None, spot, "no central in the committed numbers"
    return c, spot, note


def rows():
    prices, src, when = latest_prices()
    out = []
    for sd in sorted(glob.glob(os.path.join(ENGINE, "*_study"))):
        tk = os.path.basename(sd).replace("_study", "").upper()
        c, spot, note = read_study(sd)
        px = (prices.get(ALIAS.get(tk, tk)) or {}).get("price")
        pxd = (prices.get(ALIAS.get(tk, tk)) or {}).get("date")
        out.append({"ticker": tk, "central": c, "spot_at_strike": spot,
                    "price_now": px, "price_date": pxd, "note": note,
                    "gap_at_strike": (c / spot - 1) if (c and spot) else None,
                    "gap_now": (c / px - 1) if (c and px) else None})
    return out, src, when


def report():
    rs, src, when = rows()
    if not rs:
        raise SystemExit("REFUSED: no study directories examined [R-ENF-04].")
    print("committed centrals against the latest known price\n")
    print("  prices: %s, supplied %s\n" % (src, when))
    print("  %-12s %10s %9s %8s %10s %9s  %s"
          % ("ticker", "central", "at strike", "now", "vs strike", "vs now", "[R-GAP-01]"))
    print("  " + "-" * 86)
    breach, unread, nopx = [], [], []
    for r in sorted(rs, key=lambda x: x["ticker"]):
        if r["central"] is None:
            unread.append(r["ticker"])
            print("  %-12s %s" % (r["ticker"], r["note"]))
            continue
        if r["price_now"] is None:
            nopx.append(r["ticker"])
        f = ""
        if r["gap_now"] is not None and abs(r["gap_now"]) > TRIGGER:
            f = "BREACH"
            breach.append(r)
        print("  %-12s %10.4g %9s %8s %10s %9s  %s"
              % (r["ticker"], r["central"],
                 ("%.2f" % r["spot_at_strike"]) if r["spot_at_strike"] else "—",
                 ("%.2f" % r["price_now"]) if r["price_now"] else "not supplied",
                 ("%+.1f%%" % (100 * r["gap_at_strike"])) if r["gap_at_strike"] is not None else "—",
                 ("%+.1f%%" % (100 * r["gap_now"])) if r["gap_now"] is not None else "—", f))
    print("\n  breaching the %.0f%% trigger against today's price: %d"
          % (100 * TRIGGER, len(breach)))
    for r in sorted(breach, key=lambda x: x["gap_now"]):
        was = (r["gap_at_strike"] is not None and abs(r["gap_at_strike"]) > TRIGGER)
        print("    %-12s %+7.1f%%   %s" % (r["ticker"], 100 * r["gap_now"],
              "already breaching at its own strike"
              if was else "NEW — it was inside the band when struck"))
    if unread:
        print("\n  unreadable, reported rather than skipped (%d): %s"
              % (len(unread), ", ".join(unread)))
    if nopx:
        print("  no price supplied for (%d): %s" % (len(nopx), ", ".join(nopx)))
    return rs


if __name__ == "__main__":
    report()
