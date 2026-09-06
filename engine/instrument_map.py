"""Where a covered name's raw price library lives, resolved one way.

THE EXCHANGE PREFIX IN assets/data.js DECIDES THE MARKET, never the folder a file
happens to sit in and never the filename: market AE spans ADX and DFM, and a
Tadawul code is numeric (TADAWUL:1120) so the ticker key and the raw filename
genuinely differ on some names. Both facts are recorded here rather than
rediscovered per script.

OUTSTANDING, STATED RATHER THAN HIDDEN: engine/build_name_calibration.py carries
its own copy of PREFIX_MARKET and SPECIAL_RAW. Folding it onto this module is a
one-line change that cannot be verified by import in an environment without
numpy/scipy, so it is left for a pass that can run that builder — a rule this
repo already knows: verify by import, not by parse.
"""
from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PREFIX_MARKET = {"EGX": "EG", "ADX": "AE", "DFM": "AE", "TADAWUL": "SA",
                 "QSE": "QA", "KRX": "KR", "NSE": "IN", "NASDAQ": "US"}
SPECIAL_RAW = {"2POINTZERO": "TWOPOINTZERO", "ALRAJHI": "RAJHI"}


def market_of(code: str):
    """'EGX:PHDC' -> 'EG'. None where the prefix is not a registered exchange."""
    if not code or ":" not in code:
        return None
    return PREFIX_MARKET.get(code.split(":", 1)[0].strip().upper())


def raw_path(key: str, code: str):
    """The OHLC library for one covered name, or None — NEVER a guess.

    A miss is returned as None so the caller can NAME it; a resolver that quietly
    drops what it cannot place reports clean having examined less than it claims.
    """
    mkt = market_of(code)
    if not mkt:
        return None
    p = os.path.join(ROOT, "engine", "raw_ohlc", mkt,
                     SPECIAL_RAW.get(key, key) + ".csv")
    return p if os.path.exists(p) else None
