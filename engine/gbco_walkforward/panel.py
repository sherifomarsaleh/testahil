#!/usr/bin/env python3
"""GBCO fundamental walk-forward [R-FCAL-01] — the historical panel.

SIGCM CLAUSE 1. Every figure is taken from a GB Auto / GB Corp document published by
the company itself on ir.gb-corporation.com and downloaded into engine/gbco_study/src/.
No vendor, no broker, no press-as-a-numbers-source.

THE ROUTE, RECORDED. The audited consolidated statements for FY2022-FY2025 and the
2026 interims are SCANNED and carry no text layer at all (0 characters across 51-60
pages). The SAME audited statements, with the same auditor's report and the same
figures, are reproduced inside the company's own annual report for each of those
years, and those DO carry a text layer. So the route for every annual figure here is
the PDF TEXT LAYER of the annual report, and the document is the audited consolidated
statement it reproduces. Where the two are both available (FY2020, FY2021) the figures
were cross-read against the standalone audited PDF and agree to the pound.

ARITHMETIC IS THE ARBITER: every year is footed against the statement's own additions
before it enters the panel, and a year that does not foot is REPORTED, never patched.

POINT-IN-TIME. Each origin sees the figures AS ORIGINALLY REPORTED for that year. The
prior-year column of a later filing is recorded separately where it was restated, and
the restatement is noted beside rather than substituted.
"""
from __future__ import annotations
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E                                            # noqa: E402

# fiscal year -> (annual report reproducing that year's audited statements, tier)
AR = {
    2013: 'GB_Annual_Report_2013.pdf', 2014: 'GB_Annual_Report_2014.pdf',
    2015: 'GB_Annual_Report_2015.pdf', 2016: 'GB_Annual_Report_2016.pdf',
    2017: 'GB_Annual_Report_2017.pdf', 2018: 'GB_Annual_Report_2018.pdf',
    2019: 'GB_Annual_Report_2019.pdf', 2020: 'GB_Annual_Report_2020.pdf',
    2021: 'GB_Annual_Report_2021.pdf', 2022: 'GB_Annual_Report_2022.pdf',
    2023: 'GB_Annual_Report_2023.pdf', 2024: 'GB_Annual_Report_2024.pdf',
    2025: 'GB_Corp_Annual_Report_2025.pdf',
}

# Label alternatives, in the order the filings have used them over fourteen years.
IS_LINES = {
    'revenue':      [r'^operating revenue$', r'^revenue$', r'^sales$'],
    'cost':         [r'^operating costs?$', r'^cost of revenue$', r'^cost of sales$'],
    'gross_profit': [r'^gross profit$'],
    'other_income': [r'^other income$'],
    'selling':      [r'^selling and marketing expenses$'],
    'admin':        [r'^general and administrative expenses$', r'^administration expenses$',
                     r'^administrative expenses$'],
    'operating_profit': [r'^operating profit$', r'^operating results$'],
    'finance_net':  [r'^finance costs? \(net\)$', r'^finance costs? - net$'],
    'ebt':          [r'^net \(?loss\)? ?/? ?profit for the year before income tax$',
                     r'^net profit for the year before income tax$',
                     r'^net profit for the year before tax$', r'^net profit before tax$'],
    'net_profit':   [r'^net profit for the year after income tax$',
                     r'^net profit for the year after tax$',
                     r'^net \(?loss\)? ?/? ?profit for the year$',
                     r'^net profit for the year$'],
}
BS_LINES = {
    'ppe':        [r'^property, plant', r'^property,? plant and equipment$'],
    'cash':       [r'^cash and cash equivalents$', r'^cash on hand and at banks$'],
    'inventories': [r'^inventories'],
    'total_assets': [r'^total\s+assets$'],
    'issued_capital': [r'^issued and paid up capital$', r'^share capital$'],
    'total_equity': [r'^total equity$'],
    'loans_nc':   [r'^loans$', r'^loans and borrowings$'],
    'loans_c':    [r'^loans, borrowings and overdrafts$', r'^loans and borrowings$'],
}


def _val(vals):
    """current-year column. Note numbers arrive as a leading negative integer, so the
    year's two columns are the LAST two numbers on the row."""
    if not vals:
        return None
    return vals[-2] if len(vals) >= 2 else vals[-1]


def _prior(vals):
    return vals[-1] if len(vals) >= 2 else None


def scan(doc):
    out = []
    for i, t in enumerate(E.pages(doc)):
        for lab, vals in E.rows(t):
            out.append((i + 1, lab.strip(), vals))
    return out


def find(rws, pats, minabs=0.0, page=None):
    for pg, lab, vals in rws:
        if page and pg != page:
            continue
        low = lab.lower().strip()
        for p in pats:
            if re.search(p, low) and vals and abs(_val(vals) or 0) >= minabs:
                return pg, lab, _val(vals), _prior(vals)
    return None, None, None, None


# --------------------------------------------------------------- the two adapters
# FY2019-FY2025: the company's own 4Q earnings release for that year, i.e. the figures
# AS ORIGINALLY REPORTED at the origin. FY2012-FY2018: the annual report reproducing
# that year's audited consolidated statements, the only route that exists — the IR
# archive's earnings releases start at 1Q20.
RELEASE = {                       # fiscal year -> (release pdf, income-statement page)
    2019: ('GB_Corp_ER_4Q20_-_E_-_FINAL.pdf', 14),     # prior-year column
    2020: ('GB_Corp_ER_4Q20_-_E_-_FINAL.pdf', 14),
    2021: ('GB_Corp_ER_4Q21_-_E_-_FINAL.pdf', 14),
    2022: ('GB_Corp_ER_4Q22_-_E_-_FINAL.pdf', 14),
    2023: ('GB_Corp_ER_4Q23_-_ER_-_FINAL.pdf', 16),
    2024: ('GB_Corp_ER_4Q24-_E_-_Final.pdf', 4),
    2025: ('GB_Corp_ER_4Q25-_E_-_Final.pdf', 4),
}

REL_LINES = {  # every label spelling the releases have used, FY19 vintage to FY25
    'revenue':      [r'^total sales revenues?$'],
    'gross_profit': [r'^total gross profit$'],
    'selling':      [r'^selling and marketing$'],
    'admin':        [r'^administration expenses$'],
    'other_income': [r'^other income'],
    'provisions':   [r'^provisions \(net\)$', r'^net provisions'],
    'operating_profit': [r'^operating profit$'],
    'associates':   [r'^investment gains from associates$', r'^investment gains \(losses\)$',
                     r'^income from associates$'],
    'ebit':         [r'^ebit$'],
    'fx':           [r'^foreign exchange'],
    'finance_net':  [r'^net finance cost'],
    'ebt':          [r'^earnings before tax$'],
    'tax':          [r'^income taxes$'],
    'npbmi':        [r'^net profit before minority', r'^net profit / loss before minority'],
    'minority':     [r'^minority interest$'],
    'net_profit':   [r'^net profit$', r'^net income/loss$'],
    'seg_pc':       [r'^egypt passenger cars revenues?$'],
    'seg_moto':     [r'^egypt motorcycles'],
    'seg_cv':       [r'^egypt commercial vehicles', r'^equipment revenue$'],
    'seg_tires':    [r'^egypt tires revenues?$'],
    'seg_capital':  [r'^gb capital .*revenues?$'],
    'seg_after':    [r'^egypt after-?sales revenues?$'],
    'seg_regional': [r'^regional revenues?$'],
    'seg_other':    [r'^others revenues?$'],
}
