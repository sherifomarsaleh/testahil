#!/usr/bin/env python3
"""Adapter for GB Corp's OWN quarterly earnings releases (ir.gb-corporation.com).

A NAMED ADAPTER PER SOURCE SHAPE, never a reader that guesses: these releases lay a
table out as a label line followed by six value lines — quarter prior, quarter current,
per-cent change, full year prior, full year current, per-cent change — and a reader
built for the annual reports' label-then-two-columns shape silently finds nothing here
and reports that as a result.
"""
from __future__ import annotations
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E                                            # noqa: E402

PCT = re.compile(r'^\(?-?[\d.]+%\)?$|^-$|^–$')
NUM = re.compile(r'^\(?\s*-?[\d][\d, .]*\)?$')


def table(doc, page):
    """[(label, [v0..v5])] from one release page."""
    import pymupdf
    d = pymupdf.open(os.path.join(E.SRC, doc))
    lines = [x.strip() for x in d[page - 1].get_text().split('\n') if x.strip()]
    out, lab, buf = [], None, []
    for s in lines:
        if PCT.match(s) or NUM.match(s):
            if PCT.match(s) and not NUM.match(s):
                buf.append(None)                                 # a per-cent column
            else:
                buf.append(E.tonum(s))
            continue
        if lab is not None:
            out.append((lab, buf))
        lab, buf = s, []
    if lab is not None:
        out.append((lab, buf))
    return out


def fy(rws, *pats, exclude=()):
    """The FULL-YEAR CURRENT column: index 4 of the six-column shape."""
    for lab, vals in rws:
        low = lab.lower()
        if any(x.lower() in low for x in exclude):
            continue
        if all(re.search(p, low) for p in pats):
            v = [x for x in vals]
            if len(v) >= 5 and v[4] is not None:
                return lab, v[4], v[3]
            if len(v) >= 2 and v[1] is not None:                 # two-column shape
                return lab, v[1], v[0]
    return None, None, None
