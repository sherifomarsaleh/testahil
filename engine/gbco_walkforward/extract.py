#!/usr/bin/env python3
"""GBCO fundamental walk-forward — figure extraction from the company's own filings.

SIGCM clause 1. Every figure here comes from a GB Auto / GB Corp document downloaded
from the company's OWN investor-relations site (ir.gb-corporation.com) into
engine/gbco_study/src/. No vendor, no broker, no press. The route for every figure in
this module is the PDF TEXT LAYER (pymupdf); the audited-statement PDFs for FY2022-FY2025
carry no text layer at all, and the SAME audited statements are reproduced verbatim inside
the annual reports for those years, which do — so the annual report is the route and the
statement it reproduces is the document.

ARITHMETIC IS THE ARBITER. Nothing extracted here is used until foot() has reconciled it
against the statement's own additions.
"""
from __future__ import annotations
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "gbco_study", "src")

_num = re.compile(r'^\(?\s*-?[\d][\d\s, ]*\)?$')


def pages(doc):
    import pymupdf
    d = pymupdf.open(os.path.join(SRC, doc))
    return [d[i].get_text() for i in range(d.page_count)]


def tonum(s):
    s = s.strip().replace(' ', ' ')
    neg = s.startswith('(') and s.endswith(')')
    s = s.strip('()').replace(',', '').replace(' ', '')
    if s in ('', '-', '–'):
        return 0.0
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def rows(text):
    """[(label, [numbers...])] — the layout these filings use is label line, then one
    line per column. A label is a line that is not a number; its columns are the
    consecutive numeric lines that follow it."""
    out, lab, buf = [], None, []
    for raw in text.split('\n'):
        s = raw.strip()
        if not s:
            continue
        if _num.match(s) or s in ('-', '–'):
            v = tonum(s)
            if v is not None:
                buf.append(v)
                continue
        if lab is not None:
            out.append((lab, buf))
        lab, buf = s, []
    if lab is not None:
        out.append((lab, buf))
    return out


def pick(rws, *patterns, col=0, exclude=()):
    """The first row whose label matches, and its col-th number."""
    for lab, vals in rws:
        low = lab.lower()
        if any(x.lower() in low for x in exclude):
            continue
        if all(re.search(p, low) for p in patterns) and len(vals) > col:
            return lab, vals
    return None, None


def foot(name, parts, total, tol=1.5):
    """A statement is accepted only if it foots against its own arithmetic."""
    s = sum(parts)
    ok = abs(s - total) <= max(tol, abs(total) * 1e-6)
    return ok, "%s: parts %.1f vs stated %.1f (diff %.1f)" % (name, s, total, s - total)
