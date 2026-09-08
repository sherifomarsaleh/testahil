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


# These records state their unit in the field name and the reader ignored it, which
# put a factor of a million into the denominator of a per-share value. The files hold
# `shares_mn` — MILLIONS — and the counts landed in the same slot as the blocks'
# counts in UNITS, so a name drawing some origins from each ran two units in one
# series. MEASURED RATHER THAN INFERRED FROM THE NAME: ARCC records 2015-2017 in both
# places and 378.7397 x 1e6 is 378,739,700 exactly, the footed count its own block
# commits for those same years; PHDC's 2308.949726 is likewise its committed
# 2,308,949,726. Two independent records agreeing to the unit is what settles it.
#
# IT REACHED A NUMBER AND NOT A CRASH, which is why nothing caught it: ARCC scores no
# cell in the declared run, so the defect only ever surfaced in the disclosed-life
# SENSITIVITY, where it printed a fair value of EGP 201,953,701 per share against a
# price of 7.63 and was read as evidence against that basis. A unit error one million
# wide is not subtle in its output and is invisible in its input [R-TERM-01: where a
# quantity carries a UNIT, the unit is the thing to check].
SHARES_MN_TO_UNITS = 1e6


def _shares():
    """Point-in-time share counts, per name, from the committed OCR records.

    Returned in UNITS, converted from the millions these files state.
    """
    out = {}
    for p in sorted(glob.glob(os.path.join(HERE, "shares_*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        tk = (d.get("ticker") or "").upper()
        if not tk:
            continue
        out[tk] = {y: rec["shares_mn"] * SHARES_MN_TO_UNITS
                   for y, rec in (d.get("shares_mn") or {}).items()
                   if isinstance(rec.get("shares_mn"), (int, float))
                   and rec["shares_mn"] > 0}
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
        # BOTH KEYS, AND READING ONLY THE FIRST WAS THE SAME READER DEFECT THE LENS
        # NEXT DOOR ALREADY FIXED [L-355]: a run's `origins` are the years it TESTED
        # and `prior_year_anchor` holds years committed to feed a window reaching back
        # past the first origin. cashflow_lens.block() reads both and says so in its
        # own comment; this reader did not, so every anchor year's FOOTED count was
        # invisible here and the year fell through to the millions file above — which
        # is how one name came to run two units across one series.
        # `origins` WINS on a collision, the same precedence the lens uses, because
        # what a run tested is what it tested.
        blocks = {}
        for src in ("prior_year_anchor", "origins"):
            blocks.update(doc.get(src) or {})
        for key, block in blocks.items():
            # An anchor mapping carries narrative keys beside its years — `_`,
            # `source_class`, `basis` — and those are strings, so the year filter
            # cannot wait until after the lookup the way it did when this read one
            # key whose members happened to be uniform.
            if not isinstance(block, dict):
                continue
            rec = block.get("shares")
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

OHLC = os.path.join(ENGINE, "raw_ohlc")


def runs():
    out = {}
    for d in sorted(glob.glob(os.path.join(ENGINE, "*_walkforward"))):
        out[os.path.basename(d).replace("_walkforward", "").upper()] = d
    return out


def _panel(rundir):
    """The walk-forward's as-reported panel, keyed by year, or {}."""
    # The runs do not agree on a filename — PHDC writes panel.json, TMGH
    # panel_annual.json — so the search is by SHAPE (a dict keyed by
    # four-digit years) across the candidates, and the file that answered
    # is recorded so a reader knows which artefact a cell stands on.
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
        # A RUN MAY NEST ITS YEARS UNDER A NAMED KEY, and the shape search above
        # only looks at the top level — so SWDY, which wraps its seventeen years
        # in {"years": {...}} beside its own provenance fields, read as a run with
        # no panel at all and every one of its cells reported NOT READY. That is
        # [L-355] on this very module: a reader that guesses a shape silently
        # finds nothing and reports it as a result. The wrapper keys are NAMED
        # rather than searched for, because a search that descends into any dict
        # would eventually find a four-digit key somewhere that is not a year.
        for wrap in ("years", "annual", "fy"):
            inner = d.get(wrap) if isinstance(d, dict) else None
            if isinstance(inner, dict) and any(
                    k.isdigit() and len(k) == 4 for k in inner):
                return ({int(k): v for k, v in inner.items() if k.isdigit()},
                        "%s[%s]" % (fn, wrap))
    return {}, None


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
    cells, names = {}, runs()
    for tk, rundir in names.items():
        panel, panel_src = _panel(rundir)
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
        print("\n  NO AS-REPORTED PANEL COMMITTED (%d): %s"
              % (len(nostate), ", ".join(nostate)))
        print("     These walk-forwards ran and scored, but they left no year-keyed")
        print("     panel of as-reported figures in the repository — their statements")
        print("     came from engine/*_walkforward/filings/, which is gitignored. So a")
        print("     later job cannot rebuild a value at their past origins from what")
        print("     is committed, and the calibration cannot use them however good the")
        print("     original run was. That is a REPRODUCIBILITY gap, not a data one:")
        print("     the fix is for those runs to commit the panel PHDC and TMGH did.")

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
