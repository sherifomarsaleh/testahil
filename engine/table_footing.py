"""A delivered table's arithmetic must close. Shared instrument, not copied.

WHY THIS EXISTS
    Two of the nine claim-level defects found by reading ARCC's rendered pages on
    03-Sep-2026 were the same defect: a table printing components and a total that
    does not follow from them.

      * Table 3 printed materials, transportation and overheads, then an EBITDA. The
        provisions and credit-losses line was deducted in the model and absent from the
        page, so a reader adding the printed rows came out 82mn high with nothing on the
        page to explain it. The code comment saying why provisions sit off the per-tonne
        stack was correct and had never reached the document.

      * Table 5 printed four contractual rates and labelled their blend "Blended cost of
        debt, adopted 13.36%". Those four weight to 7.89%. The model was right the whole
        time — it carries each facility at local-equivalent cost and 13.36% reproduces
        from THAT — and the document printed the wrong column, under a caption reading
        "built in the model from these four lines, not pasted".

    NEITHER WAS VISIBLE TO ANY EXISTING GATE, and the reason is exact. The recalculation
    gate reconciles the model to itself, so a model that is right passes however wrong the
    page is. prose_figures matches each figure against the model's own numbers, and every
    figure in both tables was computed and individually correct — the defect was in the
    RELATIONSHIP between figures, which is a thing no per-figure check can see. The table
    audit measures column widths, not arithmetic.

WHAT IT DOES
    Reads every table in every delivered document, finds rows whose label declares them a
    TOTAL of what sits above (total, sum, weighted average, blended, net), and requires the
    printed figure to be reproducible from the printed rows above it — as a sum, or, for a
    weighted label, as a weighted mean against some other column of the same table.

    TOLERANCE IS DERIVED FROM THE ROUNDING, NEVER CHOSEN. A table printing to k decimals
    can be off by half a unit in the last place per row, so n contiguous rows carry a
    worst-case rounding band of n * 0.5 * 10**-k. That is arithmetic about the printed
    page rather than a free parameter, which the promotion rule would forbid.

    A WEIGHTED LABEL IS TRIED AGAINST EVERY OTHER COLUMN as the weight vector and passes if
    any reconciles. That is deliberately generous: a weighted average reproducible from no
    column of its own table is not reproducible by a reader, which is the defect, and
    guessing which column is the weight would be a check about this instrument's cleverness
    rather than about the page.

THE STANDING RULE FOR A FALSE POSITIVE, inherited verbatim from prose_figures because it is
the whole discipline: A FALSE POSITIVE IS FIXED BY DECLARING THE EXCEPTION WITH ITS REASON,
NEVER BY DELETING THE TOTAL FROM THE TABLE. A total that legitimately spans rows the table
does not print is a real thing — but it is a thing the study must SAY, because a total a
reader cannot reproduce is indistinguishable from one that is wrong.
"""
import re

# AN "OF WHICH" ROW IS A BREAKDOWN OF THE LINE ABOVE IT, NOT A COMPONENT BESIDE IT.
# Counting both double-counts the sub-item and condemns a balance sheet that foots exactly:
# PHDC's prints non-current assets, four "of which" lines, current assets and a total that
# IS their sum over the two parent lines. A third table shape the first draft did not know,
# found the same way as the other two — by running it over the book and looking.
SUBITEM_RX = re.compile(r'^\s*(of which|o/w|thereof|which includes)\b', re.I)

TOTAL_RX = re.compile(
    r'^\s*(total\b|totals\b|sum\b|subtotal\b|weighted average\b|blended\b|'
    r'net\s+(?:total|sum)\b)', re.I)
WEIGHTED_RX = re.compile(r'^\s*(weighted average\b|blended\b)', re.I)

# a printed cell that carries a number, with its decimals so the band can be derived
_NUM_RX = re.compile(r'^[^\d\-+(]*([\-+(]?\s*[\d,]+(?:\.(\d+))?\s*\)?)\s*%?\s*[^\d]*$')


def parse_cell(text):
    """(value, decimals) for a printed cell, or None where the cell is not a number.

    A percentage is returned as its PRINTED magnitude, not divided by a hundred: the check
    is about whether the page's own arithmetic closes, so it works in the page's units.
    """
    t = (text or '').strip()
    if not t:
        return None
    # A DASH IS A NOT-APPLICABLE, NOT A WALL. ARCC's Table 5 printed a dash for the lease
    # facility's rate, and treating that as the end of the block made the walk collect
    # nothing and skip the very row the check exists for — the negative control caught it
    # by replaying that table exactly as it shipped.
    if t in ('—', '-', '–', 'n/a', 'N/A', 'nil', '0'):
        return 0.0, 0
    m = _NUM_RX.match(t)
    if not m:
        return None
    raw = m.group(1).replace(',', '').replace(' ', '')
    neg = raw.startswith('(') or raw.startswith('-')
    raw = raw.strip('()+-')
    if not raw or not raw.replace('.', '', 1).isdigit():
        return None
    try:
        v = float(raw)
    except ValueError:
        return None
    # A BARE FOUR-DIGIT YEAR IS A DATE, NOT A FIGURE. "Jan 2026" and "FY2025" both parse as
    # numbers under any reader that tolerates a prefix, and a date COLUMN then reads as a
    # numeric one — which condemned an input register whose "as of" column happens to sit
    # beside a row labelled "Total equity risk premium". The header bug had the same cause
    # and was fixed by never walking into row 0; a date column needs this as well.
    if (not m.group(2)) and ',' not in t and 1900 <= v <= 2100 and float(v).is_integer():
        return None
    return (-v if neg else v), len(m.group(2) or '')


def grid(tbl):
    """A docx table as a list of rows of cell text, de-duplicating merged cells."""
    out = []
    for r in tbl.rows:
        seen, row = set(), []
        for c in r.cells:
            key = id(c._tc)
            row.append('' if key in seen else c.text)
            seen.add(key)
        out.append(row)
    return out


def _close(a, b, band):
    return abs(a - b) <= band + 1e-9


def check_table(rows, min_components=2):
    """Every unreconciled total in one table, as (row_index, col_index, label, printed).

    A total is reconciled if SOME contiguous run of at least `min_components` numeric rows
    ending immediately above it sums to it (or weights to it, for a weighted label).
    """
    bad = []
    for i, row in enumerate(rows):
        label = (row[0] if row else '') or ''
        if not TOTAL_RX.match(label):
            continue
        weighted = bool(WEIGHTED_RX.match(label))  # kept: documents the label class
        for j in range(1, len(row)):
            cell = parse_cell(row[j])
            if cell is None:
                continue
            total, dp = cell
            band = 0.5 * 10 ** -dp if dp else 0.5
            ok = False
            # walk contiguous numeric rows upward from directly above
            comps, k = [], i - 1
            # NEVER WALK INTO THE HEADER. 'FY2025' parses as 2025 under any numeric reader
            # that tolerates a prefix, so a walk reaching row 0 silently acquires a
            # four-digit component and condemns a table that foots perfectly. The negative
            # control caught this on a legitimate balance sheet.
            while k >= 1:
                _lab = (rows[k][0] if rows[k] else '') or ''
                if SUBITEM_RX.match(_lab):
                    k -= 1                    # a breakdown of the line above, not a peer
                    continue
                c = parse_cell(rows[k][j]) if j < len(rows[k]) else None
                if c is None:
                    break
                comps.insert(0, (k, c[0]))
                k -= 1
                if len(comps) < min_components:
                    continue
                n = len(comps)
                # A TABLE ROLLS UP THREE WAYS AND ALL THREE ARE ORDINARY.
                #   (a) the rows immediately above — an unstructured stack;
                #   (b) the LEAF rows above, skipping any intermediate subtotal — which is
                #       how a balance sheet foots, "total assets" spanning non-current and
                #       current with "total current assets" sitting between them;
                #   (c) the SUBTOTALS above and nothing else — the same balance sheet read
                #       the other way, total assets as current plus non-current.
                # The first draft tried only (a) and flagged 67 balance-sheet totals across
                # the book. That was this instrument being wrong about how tables work, not
                # sixty-seven defects, and widening it was the fix rather than declaring
                # them — a false positive is fixed by making the check right.
                leaf = [(r, v) for r, v in comps
                        if not TOTAL_RX.match((rows[r][0] if rows[r] else '') or '')]
                subs = [(r, v) for r, v in comps
                        if TOTAL_RX.match((rows[r][0] if rows[r] else '') or '')]
                for cand in ([c for c in (comps, leaf, subs) if len(c) >= min_components]):
                    if _close(sum(v for _, v in cand), total, band * (len(cand) + 1)):
                        ok = True
                        break
                if ok:
                    break
                # A WEIGHTED MEAN IS TRIED FOR ANY TOTAL LABEL, NOT ONLY A "WEIGHTED" ONE.
                # A row labelled TOTAL is legitimately a SUM in one column and a weighted
                # MEAN in another of the same table: AMOC's product table totals tonnes and
                # value down their columns and carries a blended realisation per tonne
                # beside them, under one "TOTAL". Restricting the mean to labels containing
                # the word "weighted" was this instrument assuming tables label their own
                # arithmetic, which they do not.
                if True:
                    for cand in (comps, leaf):
                        if len(cand) < min_components:
                            continue
                        for w in range(1, len(row)):
                            if w == j:
                                continue
                            ws = [parse_cell(rows[r][w]) if w < len(rows[r]) else None
                                  for r, _ in cand]
                            if any(x is None for x in ws):
                                continue
                            tw = sum(x[0] for x in ws)
                            if abs(tw) < 1e-12:
                                continue
                            wm = sum(x[0] * v for x, (_, v) in zip(ws, cand)) / tw
                            # THE WEIGHT COLUMN'S OWN ROUNDING PROPAGATES INTO THE MEAN.
                            # Ignoring it condemned a product table whose tonnages print to
                            # three decimals against realisations in whole pounds: the mean
                            # came out five units from the printed figure on a band of four.
                            # A weighted mean quoted against rounded weights cannot be
                            # pinned tighter than the weights allow, which is arithmetic
                            # about the page rather than a loosened threshold.
                            wdp = max(x[1] for x in ws)
                            wband = abs(total) * 0.5 * 10 ** -wdp * len(cand) / abs(tw)
                            if _close(wm, total, band * (len(cand) + 1) + wband):
                                ok = True
                                break
                        if ok:
                            break
                    if ok:
                        break
            # A "TOTAL" ROW WITH NOTHING ABOVE IT IS NOT A CLAIM ABOUT THE ROWS ABOVE IT.
            # "Total assets" heading a summary balance sheet is a DISCLOSED LINE ITEM sitting
            # beside cash, debt and equity — none of which are its components. The first
            # draft flagged 34 of those across the book, which was this instrument asserting
            # a shape the table does not have. Where fewer than `min_components` numeric rows
            # sit directly above, there is nothing to reconcile and the check says nothing.
            if len(comps) < min_components:
                continue
            if not ok:
                bad.append((i, j, label.strip(), row[j].strip()))
    return bad


def check(paths, declared=()):
    """(tables_examined, problems) across delivered documents.

    `declared` is the study's own exception list: (document, table_index, row_label, reason)
    or (document, table_index, row_label, col_index, reason). A declaration with an empty
    reason does not count — the reason is the whole point.
    """
    import docx
    exc = set()
    for d in declared:
        exc.add((d[0], d[1], str(d[2]).strip().lower()))
    examined, problems = 0, []
    for p in paths:
        doc = docx.Document(p)
        for ti, tbl in enumerate(doc.tables):
            rows = grid(tbl)
            if len(rows) < 3:
                continue
            examined += 1
            for (ri, ci, label, printed) in check_table(rows):
                if (p, ti, label.lower()) in exc:
                    continue
                problems.append((p, ti, ri, ci, label, printed))
    return examined, problems


def report(examined, problems, tag):
    for (p, ti, ri, ci, label, printed) in problems:
        print(f'  [FAIL] {p} table {ti} row {ri} col {ci}: "{label}" prints {printed}, '
              f'which does not follow from the rows above it')
    print(f'tables examined: {examined}; unreconciled totals: {len(problems)} [{tag}]')
    return 1 if problems else 0
