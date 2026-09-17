"""The calibration panel — what a mechanical rebuild at each past origin can stand on.

[R-VCAL-01] scores a fair value rebuilt at each historical origin. Before any
value can be rebuilt, four things must exist FOR THAT ORIGIN and be readable
without reaching for anything published after it:

  MACRO      what the world knew — engine/macro_history/, four required figures
  STATEMENTS the company's own numbers AS REPORTED then — the statement
             walk-forward's panel, which is the only place in this repository
             holding as-reported figures rather than restated ones
  DRIVERS    the projection the mechanical method makes at that origin — the
             walk-forward's own forward record, so no judgement enters
  PRICE      the close at the origin, from the persistent OHLC library

This module ASSEMBLES those and reports, cell by cell, which are present. It
deliberately does not value anything: the readiness matrix is the thing every
later step reads, and a cell that is missing here is an origin the scorer must
drop rather than fill. A panel that quietly substituted a neighbouring year's
statement, or today's macro, would produce a fuller-looking record and a corrupted
error — and the arithmetic would still reconcile.

WHAT IT IS HONEST ABOUT. The price series is a market close and needs no vintage.
The statements are as-reported and carry the walk-forward's own provenance. The
macro carries its revision class and, where a figure could not be corroborated,
says so. Nothing here upgrades the evidence a figure arrived with.
"""
from __future__ import annotations

import csv
import datetime as dt
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
sys.path.insert(0, ENGINE)

import macro_history as MH  # noqa: E402


def _shares():
    """Point-in-time share counts, per name, from the committed OCR records."""
    out = {}
    for p in sorted(glob.glob(os.path.join(HERE, "shares_*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        tk = (d.get("ticker") or "").upper()
        if not tk:
            continue
        out[tk] = {y: rec.get("shares_mn")
                   for y, rec in (d.get("shares_mn") or {}).items()
                   if rec.get("shares_mn")}
    return out


def _block_shares():
    """The FOOTED counts from the valuation-input blocks [R-FCAL-01 AMENDED].

    The amendment requires the count to be committed WITH the par value it was
    footed against — issued capital over par must reproduce the count the same
    document states — which is a stricter record than the OCR files above, and it
    is committed by the run rather than assembled beside it. So it is read FIRST.

    A record carrying a count and no par value is NOT read, and that refusal is
    the amendment's own clause (ii): the count is footed or it is not recorded.
    A block that says `missing` is not a count either; recording the absence is
    what makes it visible and crediting it would undo that.
    """
    out = {}
    for d in sorted(glob.glob(os.path.join(ENGINE, "*_walkforward"))):
        tk = os.path.basename(d).replace("_walkforward", "").upper()
        p = os.path.join(d, "valuation_inputs.json")
        if not os.path.exists(p):
            continue
        try:
            doc = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        for key, block in (doc.get("origins") or {}).items():
            rec = (block or {}).get("shares")
            if not isinstance(rec, dict) or "missing" in rec:
                continue
            v, cap, par = (rec.get("value"), rec.get("issued_capital"),
                           rec.get("par_value"))
            if not (isinstance(v, (int, float)) and v > 0):
                continue
            if not (isinstance(cap, (int, float)) and isinstance(par, (int, float))
                    and par > 0):
                continue
            # The footing is RE-RUN here rather than trusted: a record that states
            # a check is not a record that passes one, and this costs one division.
            if abs(cap / par - v) > max(1.0, 1e-6 * v):
                continue
            digits = "".join(ch for ch in str(key) if ch.isdigit())
            if len(digits) == 4:
                out.setdefault(tk, {})[digits] = float(v)
    return out


SHARES = _shares()
BLOCK_SHARES = _block_shares()

# ticker -> the artefact that answered for its panel, or a SKIPPED/UNREADABLE sentinel
PANEL_SOURCE = {}

OHLC = os.path.join(ENGINE, "raw_ohlc")


def runs():
    out = {}
    for d in sorted(glob.glob(os.path.join(ENGINE, "*_walkforward"))):
        out[os.path.basename(d).replace("_walkforward", "").upper()] = d
    return out


# ONE NAMED ADAPTER PER RUN, BECAUSE A READER THAT GUESSES A SHAPE FINDS NOTHING AND
# REPORTS THAT AS A RESULT [L-355].
#
# WHAT THE GUESSING COST, MEASURED 17-09-2026. The search below used to be "by SHAPE" —
# try six filenames, accept the first whose TOP LEVEL is keyed by four-digit years — and
# it reported FIVE runs as having committed no as-reported panel at all. FOUR OF THE FIVE
# COMMIT ONE. GBCO and SWDY nest theirs one level down under `years`; SCEM and PHAR key
# theirs "FY2021" under `income_statement`. Every one of those files was on disk, tracked,
# and full of footed figures with their sources.
#
# AND THE TOOL DID NOT GO QUIET ABOUT IT — IT EXPLAINED. It printed that their statements
# "came from engine/*_walkforward/filings/, which is gitignored", which is a specific,
# confident and WRONG account of why a number was zero, and it is the reason nobody looked
# for three weeks: an absence with a plausible story attached stops being a question.
#
# So the route is NAMED per run rather than inferred. A run this table does not name and
# whose file is not top-level year-keyed is REPORTED as unreadable [R-ENF-04] — never
# silently empty, which is the state this whole comment is about.
def _years_top(d):
    """{year: cell} where the years ARE the top-level keys — PHDC, TMGH."""
    return {int(k): v for k, v in d.items() if k.isdigit() and len(k) == 4}


def _years_nested(key):
    """{year: cell} from a dict nested one level under `key` — GBCO, SWDY."""
    def read(d):
        inner = d.get(key) or {}
        return {int(k): v for k, v in inner.items()
                if isinstance(k, str) and k.isdigit() and len(k) == 4}
    return read


def _years_fy(key):
    """{year: cell} from FY-prefixed keys under `key` — SCEM, PHAR."""
    def read(d):
        inner = d.get(key) or {}
        out = {}
        for k, v in inner.items():
            digits = "".join(ch for ch in str(k) if ch.isdigit())
            if len(digits) == 4:
                out[int(digits)] = v
        return out
    return read


PANEL_ADAPTER = {
    "PHDC": ("panel.json", _years_top),
    "TMGH": ("panel_annual.json", _years_top),
    "GBCO": ("panel.json", _years_nested("years")),
    "SWDY": ("panel.json", _years_nested("years")),
    "SCEM": ("panel_export.json", _years_fy("income_statement")),
    "PHAR": ("panel_export.json", _years_fy("income_statement")),
}


def _skip_reason(rundir):
    """The run's own recorded reason for not running, or None.

    A SKIP IS NOT A MISSING PANEL AND MUST NOT BE COUNTED AS ONE. ELEC records
    "walk-forward not run — insufficient sourceable history (4 years)" in the words
    [R-FCAL-01] prescribes; reporting that as an absent artefact would turn a correct
    refusal into an outstanding debt, which is how a clean result gets manufactured in
    the other direction.
    """
    p = os.path.join(rundir, "skip_record.json")
    if not os.path.exists(p):
        return None
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        return "skip_record.json will not parse"
    return d.get("scope_words") or "recorded as skipped"


def _panel(rundir):
    """The walk-forward's as-reported panel, keyed by year, or {}.

    Returns (panel, source) where source is the filename that answered, or one of
    the sentinels "SKIPPED: ..." / "UNREADABLE: ..." so a caller can tell a run that
    correctly did not run from one this reader cannot open.
    """
    tk = os.path.basename(rundir.rstrip(os.sep)).replace("_walkforward", "").upper()
    skip = _skip_reason(rundir)
    if skip:
        return {}, "SKIPPED: %s" % skip
    named = PANEL_ADAPTER.get(tk)
    if named:
        fn, route = named
        p = os.path.join(rundir, fn)
        if not os.path.exists(p):
            return {}, "UNREADABLE: %s names %s and it is not on disk" % (tk, fn)
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            return {}, "UNREADABLE: %s will not parse (%s)" % (fn, e)
        got = route(d) if isinstance(d, dict) else {}
        if not got:
            return {}, ("UNREADABLE: %s adapter found no year-keyed cells in %s — the "
                        "shape moved and the adapter did not" % (tk, fn))
        return got, fn
    # No named adapter: the top-level convention is still accepted, and anything else
    # is reported rather than returned empty.
    for fn in ("panel.json", "panel_annual.json", "panel_export.json",
               "panel_kpi_verified.json", "bottom_up.json", "fs_parsed.json"):
        p = os.path.join(rundir, fn)
        if not os.path.exists(p):
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and any(k.isdigit() and len(k) == 4 for k in d):
            return {int(k): v for k, v in d.items() if k.isdigit()}, fn
    return {}, ("UNREADABLE: %s commits no panel this reader is taught to read — add a "
                "named adapter rather than letting the name drop out" % tk)


def _forward(rundir):
    p = os.path.join(rundir, "forward_ranges.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def find_market(ticker):
    for m in sorted(os.listdir(OHLC)) if os.path.isdir(OHLC) else []:
        if os.path.exists(os.path.join(OHLC, m, "%s.csv" % ticker)):
            return m
    return None


def close_at(ticker, year):
    """The last close on or before 31 December of `year`, with its date.

    A market close needs no vintage — it is fixed at its date — but it does need
    to be the close of a session that had actually happened by the origin, so the
    search runs BACKWARD from the year end and never forward into the next year.
    """
    m = find_market(ticker)
    if not m:
        return None, None
    p = os.path.join(OHLC, m, "%s.csv" % ticker)
    cutoff = dt.date(year, 12, 31)
    best = None
    with open(p, encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            raw = (row.get("Date") or "").strip().strip('"')
            try:
                d = dt.datetime.strptime(raw, "%m/%d/%Y").date()
            except ValueError:
                continue
            if d > cutoff:
                continue
            if best is None or d > best[0]:
                try:
                    px = float((row.get("Price") or "").replace(",", ""))
                except ValueError:
                    continue
                best = (d, px)
    return (best[1], best[0].isoformat()) if best else (None, None)


def build(market="EG"):
    usable = set(MH.usable_origins(market))
    declared = [int(o["year"]) for o in MH.load(market).get("origins", [])]
    # WHICH ARTEFACT ANSWERED, PER NAME, so the report can say WHY a name is empty
    # instead of offering one explanation for three different facts. Module-level rather
    # than a fifth return value: build() has ten callers and changing its arity to carry
    # a diagnostic would be a breaking change for a message.
    PANEL_SOURCE.clear()
    cells, names = {}, runs()
    for tk, rundir in names.items():
        panel, panel_src = _panel(rundir)
        PANEL_SOURCE[tk] = panel_src
        fwd = _forward(rundir)
        for y in declared:
            px, pxdate = close_at(tk, y)
            # THE SHARE COUNT IS THE FIFTH INPUT AND IT IS THE ONE NOBODY
            # COMMITTED. A model equity value cannot be compared with a share
            # price without it, and today's count is NOT a substitute: share
            # counts change on capital increases, so carrying the current one
            # back to a 2013 origin is right only by luck — fabricated in
            # vintage, invisible afterwards, and the exact error the macro
            # archive was built to refuse. It is read from the panel where the
            # panel has it and is otherwise missing.
            # First the committed share record, which is the point-in-time count
            # read off that year's own filing and footed against it. Only if it
            # has nothing for this year does the panel look inside the run's own
            # artefacts — and today's count is never a fallback.
            sh = BLOCK_SHARES.get(tk, {}).get(str(y))
            sh_src = "valuation_inputs.json" if sh else None
            if sh is None:
                sh = SHARES.get(tk, {}).get(str(y))
                sh_src = "shares_%s.json" % tk.lower() if sh else None
            if sh is None and y in panel:
                rec = panel[y]
                cell = rec.get("cells") if isinstance(rec, dict) else None
                for src in (rec, cell):
                    if not isinstance(src, dict):
                        continue
                    for k in ("shares", "shares_mn", "share_count",
                              "bs.shares", "is.shares"):
                        v = src.get(k)
                        v = v.get("value") if isinstance(v, dict) else v
                        if isinstance(v, (int, float)) and v > 0:
                            sh = float(v)
                            break
                    if sh:
                        break
            if sh and sh_src is None:
                sh_src = panel_src
            cells[(tk, y)] = {
                "shares": sh,
                "shares_source": sh_src,
                "macro": y in usable,
                "statements": y in panel,
                "statements_source": panel_src,
                "drivers": fwd is not None,
                "price": px,
                "price_date": pxdate,
                "ready": bool(y in usable and y in panel and fwd is not None
                              and px and sh),
            }
    return cells, sorted(names), declared, usable


def report(market="EG"):
    cells, names, declared, usable = build(market)
    print("valuation-calibration panel — %s\n" % market)
    print("  a cell is READY when all four exist for that origin: macro, "
          "as-reported statements, the mechanical drivers, and a price.\n")
    head = "  %-8s " % "origin" + " ".join("%-7s" % n[:7] for n in names)
    print(head)
    print("  " + "-" * (len(head) - 2))
    for y in declared:
        row = []
        for tk in names:
            c = cells[(tk, y)]
            if c["ready"]:
                row.append("READY  ")
            else:
                missing = ([k for k in ("macro", "statements", "drivers")
                            if not c[k]]
                           + ([] if c["price"] else ["price"])
                           + ([] if c["shares"] else ["shares"]))
                row.append("%-7s" % ("-" + missing[0][:6] if missing else "?"))
        print("  %-8d " % y + " ".join(row))

    ready = [(t, y) for (t, y), c in cells.items() if c["ready"]]
    print("\n  READY cells: %d of %d" % (len(ready), len(cells)))
    by_name = {}
    for t, y in ready:
        by_name.setdefault(t, []).append(y)
    for t in names:
        ys = sorted(by_name.get(t, []))
        print("     %-10s %d origin(s)%s"
              % (t, len(ys), ("  " + ", ".join(map(str, ys))) if ys else ""))

    short = {}
    for (t, y), c in cells.items():
        if c["ready"]:
            continue
        for k in ("macro", "statements", "drivers"):
            if not c[k]:
                short.setdefault(k, 0)
                short[k] += 1
        if not c["price"]:
            short.setdefault("price", 0)
            short["price"] += 1
        if not c["shares"]:
            short.setdefault("shares", 0)
            short["shares"] += 1
    if short:
        print("\n  what is short, across all unready cells:")
        for k, n in sorted(short.items(), key=lambda kv: -kv[1]):
            print("     %-12s %d cell(s)" % (k, n))
    # WHY A NAME HAS NO STATEMENTS AT ALL IS A DIFFERENT FACT FROM A THIN PANEL,
    # and it is one this repository can act on. Say it separately.
    nostate = [t for t in names
               if not any(cells[(t, y)]["statements"] for y in declared)]
    if nostate:
        # A NAME WITH NO STATEMENTS IS THREE DIFFERENT FACTS AND THIS PRINTED ONE
        # EXPLANATION FOR ALL OF THEM [corrected 17-09-2026]. It said their statements
        # "came from engine/*_walkforward/filings/, which is gitignored" — true of
        # nobody, as it turned out. Each name now says which of the three it is, read
        # off the source sentinel _panel returned rather than assumed.
        print("\n  NO USABLE AS-REPORTED PANEL (%d): %s"
              % (len(nostate), ", ".join(nostate)))
        for t in nostate:
            why = PANEL_SOURCE.get(t) or "no panel artefact found"
            if str(why).startswith("SKIPPED:"):
                print("     %-8s CORRECTLY DID NOT RUN — %s" % (t, why[8:].strip()))
            elif str(why).startswith("UNREADABLE:"):
                print("     %-8s %s" % (t, why[11:].strip()))
            else:
                print("     %-8s panel read from %s and it yielded no origin in the "
                      "declared window" % (t, why))
        print("     A SKIP IS NOT A DEBT and an unreadable panel is not an absent one.")
        print("     Where a run commits a panel this reader cannot open, the fix is a")
        print("     NAMED ADAPTER in PANEL_ADAPTER — not a re-run of the walk-forward.")

    noshares = sum(1 for c in cells.values() if not c["shares"])
    if noshares == len(cells):
        print("\n  NO ORIGIN HAS A SHARE COUNT (%d of %d cells), and that alone stops"
              % (noshares, len(cells)))
        print("     every score. A model equity value cannot meet a share price")
        print("     without one, and today's count is not a substitute: share counts")
        print("     change on capital increases, so carrying the current one back to")
        print("     a 2013 origin is right only by luck — fabricated in vintage and")
        print("     invisible afterwards, which is the error the macro archive exists")
        print("     to refuse.")
        print("     WHAT CLOSES IT: the equity note of the filings these walk-forwards")
        print("     already fetched gives issued capital and par value at each")
        print("     year-end, and their quotient is the count. It is a defined piece")
        print("     of work on those runs, not an unanswerable gap.")

    print("\n  A cell short of anything is DROPPED by the scorer, never filled. "
          "Every\n  gap above is an origin the calibration does not get, which is "
          "the point:\n  a thin panel shows up as fewer cells rather than as a "
          "fuller-looking one.")
    return cells


if __name__ == "__main__":
    report(sys.argv[1] if len(sys.argv) > 1 else "EG")
