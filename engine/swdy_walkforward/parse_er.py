"""Parse SWDY's own earnings releases into the panel's income-statement and
balance-sheet cells, per fiscal year, AS FIRST REPORTED.

Tier A COMPANY_IR — the company's own investor-relations documents, tagged distinctly
from the audited-statement tag because a reader is owed the difference. Every figure is
cross-checked against the audited consolidated statements wherever those parse and foot;
where the two disagree the disagreement is RECORDED, never averaged.

POINT-IN-TIME IS ABSOLUTE. Each fiscal year is read out of ITS OWN year's release, which
is what a forecaster standing at that origin could see. The following year's release
frequently RE-PRESENTS the comparative — FY2015 revenue is 20,571,703,734 in the FY2015
audited statements and 18,894,528 thousand in the FY2016 release, a re-presentation of
8.1% — and the restated figure is carried BESIDE the original, never substituted for it.

Units differ by vintage and are read off the page rather than assumed: releases from 2016
print EGP (000)'s, the earlier ones print whole EGP. A scale read wrongly is a thousand-
fold error that foots perfectly against itself.
"""
import re, os, json, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_fs import numbers, big, load

HERE = os.path.dirname(os.path.abspath(__file__))

# The label a line carries changes across sixteen vintages; every spelling below was read
# off the releases themselves [L-355]. A matcher built from what a release OUGHT to say
# finds nothing and reports it as a clean absence.
IS_LABELS = {
    'revenue':      [r'^\s*Total Sales\b', r'^\s*Sales\s{2,}', r'^\s*Revenue\s*$',
                     r'^\s*Revenues?\b(?!.*from)'],
    'cogs':         [r'^\s*COGS\b', r'^\s*Cost of (revenue|sales|goods)'],
    'gross_profit': [r'^\s*Gross Profit\s*(?!Margin)', r'^\s*Gross profits?\b(?!.*margin)'],
    'impair_inv':   [r'^\s*Impairment In Inventory'],
    'sga':          [r'^\s*SG\s*&\s*A\b', r'^\s*SG&A\b'],
    'other_op_inc': [r'^\s*Other Operating Income\s{2,}'],
    'other_op_exp': [r'^\s*Other Operating Expense'],
    'inv_income':   [r'^\s*Income from Investments'],
    'ebitda':       [r'^\s*EBITDA\s*(?!Margin)'],
    'dna':          [r'^\s*Depreciation( & Amortization| and Amortization)?\s*(?!.*margin)'],
    'fx':           [r'^\s*Fx Gain'],
    'ebit':         [r'^\s*EBIT\s*(?!DA)'],
    'interest_exp': [r'^\s*Interest Expense'],
    'interest_inc': [r'^\s*Interest Income\s*(?!/)'],
    'ebt':          [r'^\s*EBT\b', r'^\s*Net profits? .*before tax'],
    'tax':          [r'^\s*Tax\b', r'^\s*Income tax'],
    'net_income':   [r'^\s*Net Income\s*$', r'^\s*Net Income\s{2,}'],
    'minority':     [r'^\s*Minority Interest'],
    'npat_owners':  [r'^\s*Net Income After Minority(?! Margin)',
                     r'^\s*Net Profit After Minority(?! Margin)'],
}

BS_LABELS = {
    'fixed_assets':   [r'^\s*Fixed Assets\b', r'^\s*Property,? plant'],
    'total_lt_assets':[r'^\s*Total Long ?term Assets'],
    'inventories':    [r'^\s*Inventor(y|ies)\b'],
    'receivables':    [r'^\s*Receivables\b', r'^\s*Trade receivables'],
    'cash':           [r'^\s*Cash & Cash Equivalents', r'^\s*Cash and cash equivalents'],
    'total_ca':       [r'^\s*Total Current Assets'],
    'total_assets':   [r'^\s*Total Assets'],
    'st_debt':        [r'^\s*Bank Overdraft', r'^\s*Banks? (overdraft|facilities)'],
    'payables':       [r'^\s*Accounts Payable', r'^\s*Trade (and other )?payables'],
    'total_cl':       [r'^\s*Total Current Liabilities'],
    'lt_debt':        [r'^\s*Long ?Term Loans?', r'^\s*Long ?term (bank )?(loans|borrowings)'],
    'total_ltl':      [r'^\s*Total Long ?term Liabilities'],
    'capital':        [r'^\s*Issued and Paid( |-)?(up )?Capital'],
    'parent_equity':  [r"^\s*Total Parent'?s? Shareholders'? Equity",
                       r'^\s*Total (equity )?attributable to (the )?owners'],
    'minority_bs':    [r'^\s*Minority Interest\s*$', r'^\s*Non-?controlling interests?\s*$'],
    'total_equity':   [r'^\s*Total Equity'],
}


def scale_of(txt, at):
    """EGP (000)'s or whole EGP — read off the page, never assumed."""
    window = txt[max(0, at - 400):at + 600]
    # Every spelling below is one this archive actually uses: "EGP (000)'s" from 2016,
    # "000's L.E" from 2011, "L.E (000)" from the middle vintages. A scale read wrongly
    # is a thousand-fold error that foots perfectly against itself, which is why the unit
    # is read off the page and never inferred from the magnitude.
    if re.search(r"EGP\s*\(000\)|EGP\s*'?000|L\.?E\s*\(000\)|\(000\)\s*'?s"
                 r"|000\s*'?s\s*L\.?E|000\s*'?s\b", window, re.I):
        return 1000.0
    return 1.0


def block(txt, header_pats, stop_pats, maxlines=90):
    lines = txt.splitlines()
    starts = [i for i, l in enumerate(lines) if any(re.search(p, l, re.I) for p in header_pats)]
    if not starts:
        return None, None, None
    i = starts[-1]                      # the FULL statement, not the summary above it
    j = i + 1
    while j < len(lines) and j - i < maxlines:
        if any(re.search(p, lines[j], re.I) for p in stop_pats):
            break
        j += 1
    at = sum(len(l) + 1 for l in lines[:i])
    return lines[i:j], at, i


def pick(lines, pats, col, minabs):
    for ln in lines:
        for p in pats:
            if re.search(p, ln, re.I):
                v = big(ln, minabs)
                if len(v) > col:
                    return v[col], ln.rstrip()
    return None, None


# ---------------------------------------------------------------------------
# COLUMNS ARE RESOLVED BY POSITION ON THE PAGE, NEVER BY COUNTING NUMBERS.
#
# The releases put the fiscal-year column in a different place in every vintage —
# FY2012 prints FY | FY | Q4 | Q4 and FY2016 prints Q4 | Q4 | %chg | FY | FY | %chg —
# so an n-th-number rule reads the fourth quarter as the year on half the archive and
# nothing about the result looks wrong. The header row carries the period labels WITH
# their x-positions; every figure is assigned to the header it sits under.
# ---------------------------------------------------------------------------
# The earliest releases head the annual column with a BARE YEAR — "2010  2009  Q4-10" —
# and the later ones with "FY-2010". A matcher requiring the FY prefix reads FY2010 and
# FY2011 as having no annual column at all and reports two clean absences [R-ENF-04].
HDR = re.compile(r'(FY[- ]?\d{4}|\dQ[- ]?\d{4}|Q\d[- ]?\d{4}|\d{2}-\d{2}-\d{2}'
                 r'|(?<![\d-])(?:19|20)\d{2}(?![\d-]))', re.I)


def header_columns(lines, want_year):
    """[(x, label)] for the period columns of the first header line that names want_year."""
    for ln in lines[:8]:
        cols = []
        for m in HDR.finditer(ln):
            g = m.group(0)
            cols.append((m.start(), g))
        if len(cols) >= 2 and any(str(want_year) in c[1] for c in cols):
            return ln, cols
    return None, []


def value_at(line, x, tol=26, minabs=1.0):
    """The figure whose printed span is nearest x. None if nothing is within tol."""
    best, bd = None, 10 ** 9
    for v, s in numbers(line):
        if abs(v) < minabs:
            continue
        d = abs(s - x)
        if d < bd:
            best, bd = v, d
    return best if bd <= tol else None


def annual_column(hdr_line, cols, year):
    """The x of the FULL-YEAR column for `year` — never a quarter."""
    for x, lab in cols:                       # explicit FY label first
        if re.match(r'FY', lab, re.I) and str(year) in lab:
            return x
    for x, lab in cols:                       # then a bare year, which is annual by shape
        if lab == str(year):
            return x
    return None


# ---------------------------------------------------------------------------
# The annual release of each fiscal year, as first reported. One file per year.
# ---------------------------------------------------------------------------
ANNUAL_ER = {
    2010: '2010Q4__El-Sewedy-Electric-reports-year-end-2010-results.txt',
    2011: '2011Q4__FY-2011-Earnings-Press-Release.txt',
    2012: '2012Q4__FY-2012-Earnings-Press-Release.txt',
    2013: '2013Q4__FY-2013-Earnings-Press-Release.txt',
    2014: '2014Q4__FY-2014-Earnings-Press-Release.txt',
    2015: '2015Q4__FY-2015-Earnings-Press-Release.txt',
    2016: '2016Q4__El-Sewedy-FY-2016-Earnings-Release.txt',
    2017: '2017Q4__El-Sewedy-4Q-2017-Earnings-Release-E-FINAL-2.txt',
    2018: '2018Q4__4Q-Earnings-Release-E-FINAL.txt',
    2019: '2019Q4__El-Sewedy-FY-2019-Earnings-Release-E-Final1.txt',
    2020: '2020Q4__El-Sewedy-4Q20-Earnings-Release-E-Final.txt',
    2021: '2021Q4__Elsewedy-Electric-FY-2021-ER-En-.txt',
    2022: '2022Q4__Elsewedy-Electric-ER-FY2022-En-.txt',
    2023: '2023Q4__Elsewedy-Electric-ER-4Q2023-E-Final.txt',
    2024: '2024Q4__Elsewedy-Electric-ER-4Q2024-En.txt',
    2025: '2025Q4__Elsewedy-Electric-ER-4Q2025-E-.txt',
}

IS_HDR = [r'^\s*Consolidated Income Statement', r'^\s*Income Statement\s*$']
IS_STOP = [r'^\s*Consolidated Balance Sheet', r'^\s*Balance Sheet\s*$',
           r'EARNINGS RELEASE\s*$', r'^\s*Consolidated Cash Flow']
BS_HDR = [r'^\s*Consolidated Balance Sheet', r'^\s*Balance Sheet\s*$']
BS_STOP = [r'^\s*Consolidated Cash Flow', r'EARNINGS RELEASE\s*$', r'^\s*Disclaimer']


def read_year(year, which='is'):
    """Every labelled line of one statement, resolved by column position, in EGP."""
    fn = ANNUAL_ER[year]
    txt = load(fn)
    if txt is None:
        return None
    hdr, stop, labels = ((IS_HDR, IS_STOP, IS_LABELS) if which == 'is'
                         else (BS_HDR, BS_STOP, BS_LABELS))
    lines, at, _ = block(txt, hdr, stop, maxlines=110)
    if not lines:
        return None
    scale = scale_of(txt, at)
    hline, cols = header_columns(lines, year)
    if not cols:
        return None
    if which == 'is':
        x = annual_column(hline, cols, year)
    else:
        # a balance sheet is dated, not periodic: the column is the LAST one naming the year
        x = None
        for cx, lab in cols:
            if str(year) in lab or lab.endswith(str(year)[-2:]):
                x = cx
        if x is None:
            x = cols[-1][0]
    if x is None:
        return None
    out = {}
    for key, pats in labels.items():
        for i, ln in enumerate(lines):
            if not any(re.search(p, ln, re.I) for p in pats):
                continue
            # A LABEL THAT WRAPS PUTS ITS FIGURES ON THE NEXT LINE. FY2017 prints
            # "Net Income After Minority" alone and its five figures beneath it; a
            # reader that only looks at the label's own line records the whole line
            # as absent and the year as missing a profit.
            v = value_at(ln, x, tol=30, minabs=100)
            src = ln
            if v is None and i + 1 < len(lines):
                v = value_at(lines[i + 1], x, tol=30, minabs=100)
                src = ln.rstrip() + ' / ' + lines[i + 1].strip()
            if v is not None:
                out[key] = dict(value=v * scale, line=src.rstrip()[:150])
                break
    out['_meta'] = dict(file=fn, scale=scale, column_x=x, header=hline.rstrip()[:160],
                        tier='A', tier_reason="the company's own earnings release",
                        route='text_layer')
    return out
