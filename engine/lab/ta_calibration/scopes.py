"""scopes.py — the three levels a technical lesson can be learned at.

Mirrors the Lessons Register's own ladder: EVERY STUDY / A CLASS OF / ONE
COMPANY ONLY. A lesson is useless until you know how far it carries, and the
middle rung is the one that has to be earned rather than assumed.

TWO CANDIDATE CLASSES, AND THEY ARE NOT EQUALLY DEFENSIBLE.

  MARKET/EXCHANGE — the mechanistic one. Tick size, daily price limits, the
  trading week and typical liquidity are properties of the venue, and every one
  of them acts directly on what a chart can do. The engine already fits per
  market for the same reason.

  SECTOR — the one the fundamental register uses, and it does not transfer
  cleanly here. assets/coverage.js carries a sector for 84 of 92 names across
  THIRTY-TWO labels, most of them holding one to three names: "Banks" sits
  beside "Financials" and "Financial Services"; "Telecom", "Telecommunications"
  and "Communication Services" are three names for one thing. Normalised below
  into coarse buckets, it becomes testable — but a class with three members
  cannot carry a class-level finding, and that is reported rather than hidden.

Whether either class earns its place is a question for the evidence, not for
this file. Both are computed; the report says which one the data supports.
"""
from __future__ import annotations
import json, os, re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, '..', '..', '..'))

# Coarse buckets. The mapping is deliberately blunt: the point is to get classes
# big enough to test, not to reproduce a GICS tree on 92 names.
_BUCKET = [
    (r'bank|financ',                    'Financials'),
    (r'real estate|hospitality',        'Real Estate'),
    (r'material|chemical|metal|mining|building', 'Materials'),
    (r'energy|utilit',                  'Energy & Utilities'),
    (r'telecom|communication',          'Telecom'),
    (r'tech|it services|payment',       'Technology'),
    (r'health',                         'Healthcare'),
    (r'consumer|food|automobile|durable', 'Consumer'),
    (r'industrial|capital goods|construction|engineering', 'Industrials'),
    (r'holding|diversified',            'Holdings'),
]


def sector_map():
    """{ticker: coarse sector} from assets/coverage.js, the repo's own source."""
    path = os.path.join(_ROOT, 'assets', 'coverage.js')
    t = open(path, encoding='utf-8').read()
    i = t.index('const COVERAGE_EN')
    j = t.index('const COVERAGE_AR') if 'const COVERAGE_AR' in t else len(t)
    raw = dict(re.findall(r'\{tk:"([^"]+)"[^{}]*?sector:"([^"]+)"', t[i:j], re.S))
    out = {}
    for tk, s in raw.items():
        low = s.lower()
        for pat, bucket in _BUCKET:
            if re.search(pat, low):
                out[tk] = bucket
                break
        else:
            out[tk] = 'Other'
    return out


MARKET_LABEL = {'EG': 'Egypt (EGX)', 'AE': 'UAE (ADX & DFM)', 'SA': 'Saudi (Tadawul)',
                'QA': 'Qatar (QSE)', 'KR': 'Korea (KRX)', 'IN': 'India (NSE)',
                'US': 'US (NASDAQ)', 'XAU': 'Precious metals', 'XPT': 'Precious metals'}


def annotate(df):
    """Add market_label and sector columns to a claims frame."""
    sm = sector_map()
    df = df.copy()
    df['market_label'] = df.market.map(MARKET_LABEL).fillna(df.market)
    df['sector'] = df.ticker.map(sm).fillna('Unclassified')
    df['key'] = df.market + '/' + df.ticker
    return df
