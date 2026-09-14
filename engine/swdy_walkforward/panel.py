"""The SWDY walk-forward panel — one row per fiscal year, four fields on every cell.

Sources, in the order of preference [R-FCAL-01] §1 / SIGCM clause 1:
  A_AUDITED   the company's own audited consolidated financial statements
  A_IR        the company's own earnings releases and investor sheets

Nothing else is admitted. Nothing is estimated, interpolated or inferred to fill a gap:
a year that cannot be sourced is left out and the window shortens.

EVERY CELL FOOTS OR IT DOES NOT ENTER. The income statement is accepted only where
revenue less cost of revenue (less any separately printed impairment line) reproduces
the printed gross profit, and the three revenue legs are accepted only where they
reproduce the printed total. Both tests are run at build time and both are recorded.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse_fs import numbers, big, load
import parse_er as E

OUT = os.path.join(HERE, 'panel.json')

# The three legs that survive both segment re-cuts. Every spelling is one the archive
# actually uses; a matcher built from what a release OUGHT to say finds nothing [L-355].
# A FOOTNOTE MARKER IS PART OF THE LABEL ON THE PAGE. The FY2025 release prints
# "Electrical Products4" and "Digital Solutions3", the superscript having flattened into
# the text, so a pattern ending in \b matches "Digital Solutions3" (no boundary is
# required after "Solutions" when the next character is a digit... there is one, between
# "s" and "3", only if the pattern ends there) and FAILS on "Electrical Products4" for
# exactly the same reason it succeeds elsewhere - which is why four of the five FY2025
# segments were read and the fifth, worth EGP 17.7bn, was silently dropped and the legs
# missed their own total by 6.3%. The footing test caught it; no reader would have
# [L-355]. Every label below therefore tolerates a trailing marker explicitly.
_M = r'\d?\s'          # an optional flattened footnote marker, then whitespace
LEGS = {
    'cables':      [r'^\s*Wires? ?&? ?Cables?' + _M, r'^\s*Wire, ?Cable ?& ?Accessories'],
    'contracting': [r'^\s*Turnkey Projects?' + _M, r'^\s*Engineering ?& ?Construction'],
    'other':       [r'^\s*Electrical Products' + _M, r'^\s*Meters' + _M,
                    r'^\s*Transformers' + _M, r'^\s*Renewables',
                    r'^\s*Digital Solutions', r'^\s*Infrastructure Investment'],
}

# Fiscal years whose income statement is read from the AUDITED statements rather than
# from an earnings release, because the modern releases print only a summary.
AUDITED_IS = {
    2025: ('2025Q4__EE-Consolidated-En-FS-31-December-2025.filled.txt', 0),
    2024: ('2025Q4__EE-Consolidated-En-FS-31-December-2025.filled.txt', 1),
    2023: ('2024Q4__EE-Consalidated-English-FS-31-December-2024.filled.txt', 1),
}

AUD_LABELS = {
    'revenue':      [r'^\s*Revenues\s'],
    'cogs':         [r'^\s*Cost of revenue\s'],
    'gross_profit': [r'^\s*Gross profit\s'],
    'other_op_inc': [r'^\s*Other income\s'],
    'selling':      [r'^\s*Selling and distribution expenses'],
    'admin':        [r'^\s*General and administrative expenses'],
    'impair_recv':  [r'^\s*Net impairment loss on trade'],
    'other_op_exp': [r'^\s*Other expenses\s'],
    'operating':    [r'^\s*Operating profit\s'],
    'finance_inc':  [r'^\s*Finance income\s'],
    'finance_cost': [r'^\s*Finance costs\s'],
    'assoc':        [r"^\s*Group's share of profit of equity-accounted"],
    'ebt':          [r'^\s*Profit for the year before tax'],
    'tax':          [r'^\s*Income tax expense'],
    # "Net profit for the year" in the FY2025 filing, "Profit for the year" in FY2024.
    # One vintage apart, same line; a single spelling reads one of the two as absent.
    'net_income':   [r'^\s*Net profit for the year', r'^\s*Profit for the year\s{2,}'],
    'npat_owners':  [r'^\s*Owners of the parent company'],
    'nci':          [r'^\s*Non-controlling interests\s'],
    'eps':          [r'^\s*Basic earning per share'],
}


def audited_is(fname, col):
    """The consolidated statement of profit or loss out of an audited filing.

    SCOPED TO THE STATEMENT, not to the document. A first draft searched the whole
    filing and read "Non-controlling interests" off the BALANCE SHEET - EGP 5,118,978,381
    of equity where the profit line is EGP 1,856,305,067, a figure 2.8x too large that
    parses cleanly and sits in the right units. The same label appears in both statements
    because both statements are about the same claim; only the block tells them apart.
    """
    txt = load(fname)
    if txt is None:
        return None
    lines_all = txt.splitlines()
    # THE CONTENTS PAGE CARRIES THE SAME HEADING AS THE STATEMENT. Taking the first
    # match gives a one-line block ("Consolidated statement of profit or loss   2"),
    # every label misses, and the filing reads as carrying no income statement at all -
    # an absent answer in a clean answer's clothes [R-ENF-04]. The block is the one
    # that is actually FOLLOWED by a revenue line.
    start = None
    for i, ln in enumerate(lines_all):
        if re.search(r'Consolidated Statement of Profit or Loss', ln, re.I):
            if any(re.search(r'^\s*Revenues\s', lines_all[k])
                   for k in range(i + 1, min(i + 30, len(lines_all)))):
                start = i
                break
    if start is None:
        return None
    stop = len(lines_all)
    for j in range(start + 1, min(start + 120, len(lines_all))):
        if re.search(r'Consolidated Statement of Comprehensive Income', lines_all[j], re.I):
            stop = j
            break
    scope = lines_all[start:stop]
    out = {}
    for key, pats in AUD_LABELS.items():
        for ln in scope:
            if not any(re.search(p, ln, re.I) for p in pats):
                continue
            # EPS is a small number in a statement of large ones, so it cannot share
            # the magnitude filter; it is taken as the LAST decimal figure on its line,
            # note references being integers printed to its left.
            if key == 'eps':
                # Note references are printed to the LEFT of the figures and parse as
                # integers, so the per-share figures are the DECIMAL ones and they are
                # taken from the right. "(40),(45-13)  7.22  4.26" is four numbers and
                # only the last two are earnings.
                v = [x for x, _ in numbers(ln)
                     if 0.01 <= abs(x) < 1000 and re.search(r'\d\.\d', ln)]
                v = [x for x in v if x != int(x)] or v
            else:
                v = [x for x, _ in numbers(ln) if abs(x) >= 1e6]
            if len(v) > col:
                out[key] = dict(value=v[col], line=ln.rstrip()[:150],
                                source=fname, tier='A_AUDITED', route='text_layer')
                break
    return out or None


def er_is(year):
    if year not in E.ANNUAL_ER:
        return None
    r = E.read_year(year, 'is')
    if not r:
        return None
    meta = r.pop('_meta', {})
    out = {}
    for k, v in r.items():
        out[k] = dict(value=v['value'], line=v['line'], source=meta.get('file'),
                      tier='A_IR', route='text_layer')
    return out


def er_legs(year, total_revenue=None, total_gp=None):
    """The three legs' REVENUE and, where disclosed, their GROSS PROFIT.

    The vintages disagree about where the segment split lives AND about what unit it is
    printed in. FY2011-FY2022 print a full "Consolidated Income Statement" in whole EGP
    with segment rows under "Sales"; FY2023-FY2025 print only a "Summary Income
    Statement" in EGP thousands. The FY2021 SUMMARY states no unit anywhere on its own
    page - the unit sentence belongs to the full statement four hundred lines below -
    so a scale read off the nearest text is 1 where it should be 1,000 and the legs come
    out a thousandfold small while looking perfectly ordinary.

    ARITHMETIC PICKS THE BLOCK. Every candidate block is read, and the one whose legs
    reproduce the year's own printed total is the one kept. A block that reproduces
    nothing is not kept at a guessed scale; it is dropped and recorded.
    """
    fn = E.ANNUAL_ER.get(year)
    if fn is None:
        return None
    txt = load(fn)
    cands = []
    for hdr in ([r'^\s*Consolidated Income Statement'], [r'^\s*Summary Income Statement'],
                [r'^\s*Income Statement\s*$']):
        lines, at, _ = E.block(txt, hdr, E.IS_STOP, maxlines=120)
        if not lines:
            continue
        h, cols = E.header_columns(lines, year)
        if not cols:
            continue
        x = E.annual_column(h, cols, year)
        if x is None:
            continue
        got = _legs_from(lines, x, E.scale_of(txt, at), fn)
        if got:
            got['_header'] = hdr[0]
            cands.append(got)
    if not cands:
        return None

    def foots(c, kind, target):
        if target is None or kind not in c:
            return None
        tot = sum(v['value'] for v in c[kind].values())
        return abs(tot - target) / abs(target)

    best_rev = None
    for c in cands:
        r = foots(c, 'revenue', total_revenue)
        if r is not None and r < 5e-6:
            best_rev = c
            break
    if best_rev is None:
        # nothing reproduces the printed total: report it rather than carry a guess
        best_rev = min(cands, key=lambda c: (foots(c, 'revenue', total_revenue)
                                             if foots(c, 'revenue', total_revenue) is not None
                                             else 9e9))
        best_rev['_unfooted'] = True
    out = dict(revenue=best_rev['revenue'], _lines=best_rev.get('_lines', {}),
               _header=best_rev['_header'])
    if best_rev.get('_unfooted'):
        out['_unfooted'] = True
    # gross profit from whichever block reproduces the printed gross profit
    for c in cands:
        g = foots(c, 'gross_profit', total_gp)
        if g is not None and g < 5e-6:
            out['gross_profit'] = c['gross_profit']
            out['_gp_header'] = c['_header']
            break
    return out


def _legs_from(lines, x, sc, fn):
    """Segment rows following each aggregate line, mapped onto the three legs."""
    AGG = {'revenue': [r'^\s*Total Sales\b', r'^\s*Sales\s*$', r'^\s*Revenues?\s'],
           'gross_profit': [r'^\s*Gross Profit\s*(?!Margin)']}
    out = {}
    for kind, pats in AGG.items():
        anchors = [i for i, ln in enumerate(lines)
                   if any(re.search(p, ln, re.I) for p in pats)]
        for a in anchors:
            acc, used = {}, []
            for j in range(a + 1, min(a + 14, len(lines))):
                ln = lines[j]
                if not ln.strip():
                    continue
                hit = None
                for leg, lp in LEGS.items():
                    if any(re.search(p, ln, re.I) for p in lp):
                        hit = leg
                        break
                if hit is None:
                    # a non-segment line ends the block, unless it is a bare aggregate
                    if re.search(r'^\s*(Total Sales|COGS|Gross Profit|Cost of)', ln, re.I):
                        break
                    continue
                v = E.value_at(ln, x, tol=30, minabs=100)
                if v is not None:
                    acc[hit] = acc.get(hit, 0.0) + v * sc
                    used.append(ln.strip()[:70])
            if len(acc) >= 2:
                out[kind] = {k: dict(value=v, source=fn, tier='A_IR', route='text_layer')
                             for k, v in acc.items()}
                out.setdefault('_lines', {})[kind] = used
                break
    # the older vintages print segments under "Sales" only; keep the shape either way
    if 'revenue' not in out:
        return None
    return out


def rap_units(year):
    """Cable tonnes, price per tonne and cost per tonne from the company's own
    'results at a glance' investor sheet. Tier A COMPANY_IR — the audited statements
    carry no tonne, and this is the finest disclosed level on this name.

    The sheets run FY2012 to 3Q2022 and were then discontinued: the unit drivers'
    definition window is a fact about the disclosure, not a choice, and a driver is
    scored only inside its own window.
    """
    import glob
    cands = sorted(glob.glob(os.path.join(HERE, 'text', '%dQ4__RAP*.txt' % year)))
    if not cands:
        return None
    fn = cands[0]
    txt = open(fn, encoding='utf-8', errors='replace').read()
    lines = txt.splitlines()
    # the column is headed "FY <year>" or "<year>" on the sheet's own header row
    hdr = None
    for ln in lines[:6]:
        if re.search(r'FY ?%d|(?<!\d)%d(?!\d)' % (year, year), ln):
            hdr = ln
            break
    if hdr is None:
        return None
    x = None
    for m in re.finditer(r'FY ?%d|(?<!\d)%d(?!\d)' % (year, year), hdr):
        x = m.start()          # the LAST occurrence is the full-year column
    # THE ARITHMETIC PICKED THESE LABELS, NOT THE READER. A first draft paired the
    # tonnes and the price per tonne with "Total Cable Revenue" and the identity missed
    # by 35-42% in every one of nine years - a residual far too large and far too stable
    # to be rounding. It is not an error in the sheet: "Total Cable Revenue" is the
    # CABLES + RAW MATERIAL block, which adds copper rod sold as metal rather than drawn
    # into cable, and no tonnage of cable multiplies up to it. The cable identity closes
    # against the "Cable Revenue" line of the Total-cables block. The raw-material total
    # is kept BESIDE it, never in place of it.
    want = {'cable_volume_t':   r'^\s*Cable Sales Volume\b',
            'cable_price_t':    r'^\s*Cable Price per ton\b',
            'cable_cost_t':     r'^\s*Cable Cost per ton\b',
            'cable_revenue':    r'^\s*Cable Revenue\b',
            'cable_cost':       r'^\s*Cable Costs\b',
            'cable_plus_rawmat_revenue': r'^\s*Total Cable Revenue\b',
            'cable_plus_rawmat_cost':    r'^\s*Total Cable Costs\b'}
    out = {}
    for key, pat in want.items():
        for ln in lines:
            if re.search(pat, ln, re.I):
                v = E.value_at(ln, x, tol=30, minabs=100)
                if v is not None:
                    out[key] = dict(value=v, line=ln.strip()[:110],
                                    source=os.path.basename(fn), tier='A_IR',
                                    route='text_layer')
                break
    return out or None


def build():
    rows = {}
    checks = []
    for y in range(2009, 2026):
        row = {}
        aud = AUDITED_IS.get(y)
        if aud:
            r = audited_is(*aud)
            if r:
                row.update(r)
        if 'revenue' not in row:
            r = er_is(y)
            if r:
                row.update(r)
        if y == 2009:
            # FY2009 is carried by the comparative column of the FY2010 release, which
            # is the earliest company document in the archive that states it. Recorded
            # as a comparative rather than as its own release.
            fn = E.ANNUAL_ER[2010]
            txt = load(fn)
            lines, at, _ = E.block(txt, E.IS_HDR, E.IS_STOP, maxlines=60)
            sc = E.scale_of(txt, at)
            h, cols = E.header_columns(lines, 2010)
            x = E.annual_column(h, cols, 2009)
            if x is not None:
                for key, pats in E.IS_LABELS.items():
                    for ln in lines:
                        if any(re.search(p, ln, re.I) for p in pats):
                            v = E.value_at(ln, x, tol=30, minabs=100)
                            if v is not None:
                                row[key] = dict(value=v * sc, line=ln.rstrip()[:120],
                                                source=fn, tier='A_IR', route='text_layer',
                                                note='comparative column of the FY2010 release')
                            break
        legs = er_legs(y, (row.get('revenue') or {}).get('value'),
                       (row.get('gross_profit') or {}).get('value'))
        if legs:
            row['legs'] = legs
        u = rap_units(y)
        if u:
            # THE UNIT BLOCK IS CARRIED ONLY IF ITS OWN IDENTITY CLOSES. Tonnes times
            # price per tonne must reproduce the sheet's own cable revenue. The FY2021
            # sheet has no text layer and its OCR loses the column alignment, which
            # produced a "cable volume" of 34,296,133,426 tonnes - and the identity
            # could not fire on it because the price field was missing, so a block of
            # nonsense would have entered the panel through the gap in its own test.
            # A TEST THAT ONLY RUNS WHEN EVERY FIELD IS PRESENT IS A TEST THAT SKIPS
            # EXACTLY THE BROKEN CASES [R-ENF-04].
            need = ('cable_volume_t', 'cable_price_t', 'cable_revenue')
            if all(k in u for k in need):
                imp = u['cable_volume_t']['value'] * u['cable_price_t']['value']
                act = u['cable_revenue']['value']
                ok = abs(imp - act) / abs(act) < 0.02
            else:
                ok = False
            if ok:
                row['units'] = u
            else:
                row['units_refused'] = dict(
                    reason=('the unit identity does not close, or a field the identity '
                            'needs is absent — the block is not carried'),
                    fields_present=sorted(u),
                    source=next(iter(u.values()))['source'])
        ss = segment_sheet(y)
        if ss:
            pt = ss.get('_printed_total') or {}
            legs_only = {k: v for k, v in ss.items() if not k.startswith('_')}
            keep = {}
            for field in ('sales', 'gross_profit', 'selling_expense', 'depreciation'):
                tot = sum((v.get(field) or {}).get('value', 0.0) for v in legs_only.values())
                target = pt.get(field)
                if target and abs(tot - target) / abs(target) < 5e-6:
                    keep[field] = True
                    checks.append(dict(year=str(y), test='segment sheet %s foots to its own total' % field,
                                       residual=tot - target, rel=(tot - target) / target,
                                       verdict='PASS'))
                else:
                    checks.append(dict(year=str(y), test='segment sheet %s foots to its own total' % field,
                                       residual=(tot - target) if target else None,
                                       rel=((tot - target) / target) if target else None,
                                       verdict='UNFOOTED — field not carried'))
            row['segment_sheet'] = {
                leg: {f: v[f] for f in keep if f in v} for leg, v in legs_only.items()}
            row['segment_sheet']['_not_allocated_raw'] = ss.get('_not_allocated_raw')
            row['segment_sheet']['_unmapped_rows'] = ss.get('_unmapped_rows')
            row['segment_sheet']['_fields_carried'] = sorted(keep)
        if row:
            rows[str(y)] = row
    # ---- the two footing tests, run at build time -------------------------------
    for y, row in sorted(rows.items()):
        g = lambda k: (row.get(k) or {}).get('value')
        rev, gp = g('revenue'), g('gross_profit')
        cg = g('cogs')
        im = g('impair_inv') or 0.0
        if rev and gp and cg:
            gap = rev - abs(cg) - abs(im) - gp
            checks.append(dict(year=y, test='gross profit foots',
                               residual=gap, rel=gap / rev,
                               verdict='PASS' if abs(gap / rev) < 5e-6 else 'FAIL'))
        if row.get('legs', {}).get('revenue') and rev:
            tot = sum(v['value'] for v in row['legs']['revenue'].values())
            gap = tot - rev
            checks.append(dict(year=y, test='revenue legs foot to total',
                               residual=gap, rel=gap / rev,
                               verdict='PASS' if abs(gap / rev) < 5e-6 else 'FAIL'))
        u = row.get('units')
        if u and 'cable_volume_t' in u and 'cable_price_t' in u and 'cable_revenue' in u:
            implied = u['cable_volume_t']['value'] * u['cable_price_t']['value']
            act = u['cable_revenue']['value']
            checks.append(dict(year=y, test='cable tonnes x price reproduces cable revenue',
                               residual=implied - act, rel=(implied - act) / act,
                               verdict='PASS' if abs((implied - act) / act) < 0.02 else 'FAIL'))
    out = dict(
        _='SWDY fundamental walk-forward panel. INTERNAL - never shown to a reader.',
        built='2026-09-07', ticker='SWDY', currency='EGP',
        tiers=dict(A_AUDITED="the company's own audited consolidated financial statements",
                   A_IR="the company's own earnings releases and investor sheets"),
        years=rows, footing=checks)
    json.dump(out, open(OUT, 'w'), indent=1)
    npass = sum(1 for c in checks if c['verdict'] == 'PASS')
    print('panel: %d fiscal years, %d footing tests, %d pass, %d FAIL'
          % (len(rows), len(checks), npass, len(checks) - npass))
    for c in checks:
        if c['verdict'] == 'FAIL':
            print('  FAIL %s %s residual %.6g (%.4f%%)' % (c['year'], c['test'], c['residual'],
                                                           c['rel'] * 100))
    return out




# The segment-analysis sheets publish, per segment, sales / gross profit / selling
# expense / DEPRECIATION — the only per-leg depreciation this company discloses
# anywhere. Their taxonomy splits "Raw Material" (copper rod sold as metal rather than
# drawn into cable) out of "Cables", where the earnings release reports the two together
# as "Wires & Cables"; the two are added back for the leg and the split is kept, because
# a rod is not a cable and the unit drivers only speak to the cable.
SEG_SHEET = {
    'cables':      [r'^\s*Raw Material\b', r'^\s*Cables\b'],
    'contracting': [r'^\s*Turnkey\b'],
    'other':       [r'^\s*Meters\b', r'^\s*Transformers\b', r'^\s*Electrical products\b',
                    r'^\s*Renewables', r'^\s*Digital', r'^\s*Infrastructure'],
}
SEG_COLS = ['sales', 'gross_profit', 'gp_pct', 'selling_expense', 'depreciation']


def segment_sheet(year):
    """Per-leg sales, gross profit, selling expense and DEPRECIATION off the sheet.

    THE PERCENTAGE COLUMN IS REMOVED BEFORE THE FIGURES ARE COUNTED, and that is the
    whole trick. The sheet prints Sales | GP | GP% | Selling Exp | Depreciation and then
    the SAME five columns again for the comparative year. GP% is a percentage, so any
    magnitude filter drops it and an ordinal reader silently shifts one place left:
    depreciation then reads the COMPARATIVE YEAR'S SALES - in FY2016 that is EGP 18.89bn
    of "depreciation" against a real figure two orders of magnitude smaller, a number in
    the right units, in the right column of the right sheet, and the wrong quantity
    entirely. Matching the header by x-position was tried first and is worse: the labels
    are left-set and the figures right-aligned, so "Sales" sits nearest the GP column's
    digits and every leg reads its own gross profit as its revenue.

    Stripping the percent token restores the printed order exactly, and the sheet's OWN
    printed Total row is then the check.
    """
    import glob
    cands = sorted(glob.glob(os.path.join(HERE, 'text', '%dQ4__Segment*.txt' % year)))
    if not cands:
        return None
    fn = cands[0]
    lines = open(fn, encoding='utf-8', errors='replace').read().splitlines()
    starts = [i for i, ln in enumerate(lines) if re.search(r'^\s*FY-?%d\s' % year, ln)]
    if not starts:
        return None
    i = starts[-1]                      # the LAST FY block is the full-year one
    cols = ['sales', 'gross_profit', 'selling_expense', 'depreciation']

    def figs(ln):
        # NO MAGNITUDE FILTER, and that is deliberate. FY2014's "Wind" row prints a
        # selling expense of exactly 0, and a filter at any positive threshold drops
        # that zero, shifts depreciation into its place and loses the depreciation
        # column entirely - which showed up as the legs missing the sheet's own printed
        # depreciation total by 1-2% for six straight years, small enough to read as
        # rounding. A ZERO IS A FIGURE. The percent column is already gone by the time
        # this runs, so printed order alone identifies the columns.
        return [x for x, _ in numbers(re.sub(r'-?\d+(?:\.\d+)?\s*%', ' ', ln))]

    out, printed_total, unmapped, not_allocated_raw = {}, None, [], []
    for j in range(i + 1, min(i + 14, len(lines))):
        ln = lines[j]
        if re.search(r'^\s*Total\b', ln):
            v = figs(ln)
            printed_total = dict(zip(cols, v[:4]))
            break
        v = figs(ln)[:4]
        if not ln.strip() or not v:
            continue
        leg = next((k for k, ps in SEG_SHEET.items()
                    if any(re.search(p, ln, re.I) for p in ps)), None)
        if leg is None:
            # A SEGMENT NOBODY NAMED IS STILL A SEGMENT. FY2014 carries a "Wind" row
            # (EGP 30.5mn of sales at a NEGATIVE gross profit) and several years carry
            # "Not Allocated" depreciation; a reader that skips what it does not
            # recognise loses them silently and the legs then miss their own printed
            # total by a little, which looks like rounding. Unmatched rows go to OTHER
            # and are NAMED, and the unallocated bucket is kept apart from all three
            # legs because it belongs to none of them.
            label = re.split(r'\s{2,}', ln.strip())[0][:40]
            if re.match(r'Not Allocated', label, re.I):
                # THE ROW IS BLANK ON THE LEFT AND ITS FIGURES ARE RIGHT-SET, so which
                # column each belongs to cannot be read from printed order the way every
                # other row can. FY2016 prints two figures here and an order-based reader
                # calls them sales and gross profit, which then breaks a total that the
                # legs alone reproduce exactly. The figures are kept RAW and UNASSIGNED:
                # a quantity whose column is not known is not a quantity, and guessing
                # the column is the interpolation this method forbids.
                not_allocated_raw.extend(v)
                unmapped.append(label)
                continue
            leg = 'other'
            unmapped.append(label)
        if len(v) < 2:
            continue
        acc = out.setdefault(leg, {})
        for c, x in zip(cols, v):
            acc[c] = acc.get(c, 0.0) + x
    if not out:
        return None
    res = {leg: {c: dict(value=v, source=os.path.basename(fn), tier='A_IR',
                         route='text_layer')
                 for c, v in vals.items()}
           for leg, vals in out.items()}
    res['_printed_total'] = printed_total
    res['_unmapped_rows'] = unmapped
    res['_not_allocated_raw'] = not_allocated_raw
    return res


if __name__ == '__main__':
    build()
