"""
Testahil — OHLC loader for the investing.com CSV export format.

Columns: Date, Price (=close), Open, High, Low, Vol., Change %. Rows arrive newest-first and
numbers may carry thousands commas or quotes; this normalizes to an ascending-by-date dict of
float arrays: {'date', 'open', 'high', 'low', 'close'}.
"""
from __future__ import annotations
import csv
import numpy as np
from datetime import datetime


def _num(x):
    if x is None:
        return np.nan
    s = str(x).strip().strip('"').replace(",", "")
    if s in ("", "-", "N/A"):
        return np.nan
    return float(s)


def _date(x):
    s = str(x).strip().strip('"')
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y", "%b %d, %Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date: {x!r}")


def load_ohlc(path: str) -> dict:
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        # normalize header keys (strip BOM/quotes/whitespace)
        keymap = {k: k.strip().strip('"') for k in reader.fieldnames}
        for raw in reader:
            r = {keymap[k]: v for k, v in raw.items()}
            try:
                rows.append((
                    _date(r["Date"]),
                    _num(r["Open"]), _num(r["High"]), _num(r["Low"]), _num(r["Price"]),
                ))
            except (ValueError, KeyError):
                continue
    rows.sort(key=lambda t: t[0])                      # ascending by date
    dates = [t[0] for t in rows]
    o = np.array([t[1] for t in rows]); h = np.array([t[2] for t in rows])
    l = np.array([t[3] for t in rows]); c = np.array([t[4] for t in rows])
    # drop any row with a missing OHLC field
    ok = ~(np.isnan(o) | np.isnan(h) | np.isnan(l) | np.isnan(c))
    return {
        "date": [d for d, k in zip(dates, ok) if k],
        "open": o[ok], "high": h[ok], "low": l[ok], "close": c[ok],
    }


def trailing_realized_vol(close, window: int = 252) -> float:
    """Annualized close-to-close realized vol over the last `window` sessions (benchmark input)."""
    c = np.asarray(close, float)
    r = np.diff(np.log(c))[-window:]
    from mc_v2 import TRADING_DAYS
    return float(r.std() * np.sqrt(TRADING_DAYS))
